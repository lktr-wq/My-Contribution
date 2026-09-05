#!/usr/bin/env python3
"""Read NVBench summaries; optionally run a bounded, unmodified-binary warmup probe.

Run under CCCL-Ubuntu. No third-party Python dependencies. Raw JSON is never edited.
The emitted statistics are descriptive, NOT confidence intervals or bug detection.
"""
import argparse
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path
import statistics
import subprocess
import time


def records(path):
    doc = json.loads(path.read_text(encoding="utf-8-sig"))
    rows = []
    seen = set()
    for bench in doc["benchmarks"]:
        for state in bench["states"]:
            axes = {a["name"]: a["value"] for a in state["axis_values"]}
            key = (bench["name"], state["device"], tuple(sorted(axes.items())))
            if key in seen:
                raise ValueError(f"Duplicate state in {path}: {key}")
            seen.add(key)
            if state.get("is_skipped"):
                raise ValueError(f"Skipped state in {path}: {state['name']}")
            vals = {s["tag"]: float(next(d["value"] for d in s["data"]
                                         if d["name"] == "value"))
                    for s in state["summaries"]}
            wanted = {"samples": "sample_size", "walltime_s": "walltime",
                      "mean_s": "time/gpu/mean", "median_s": "time/gpu/median",
                      "noise": "time/gpu/stdev/relative", "iqr": "time/gpu/iqr/relative",
                      "min_s": "time/gpu/min", "max_s": "time/gpu/max"}
            row = {k: vals["nv/cold/" + v] for k, v in wanted.items()}
            if not all(math.isfinite(v) for v in row.values()):
                raise ValueError(f"Nonfinite metric in {path}: {state['name']}")
            if row["median_s"] <= 0 or row["mean_s"] <= 0 or row["samples"] < 1:
                raise ValueError(f"Invalid metric in {path}: {state['name']}")
            row.update(name=state["name"], axes=axes, timeout_s=state["timeout"],
                       warmups=state["cold_warmup_runs"])
            # Boundary flag only: JSON does not expose the actual termination reason.
            row["at_timeout_boundary"] = row["walltime_s"] >= state["timeout"]
            rows.append(row)
    return rows


def audit(paths):
    output = []
    for path in paths:
        rows = records(path)
        output.append({"file": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                       "states": len(rows), "noise_over_5pct": sum(r["noise"] > .05 for r in rows),
                       "noise_over_20pct": sum(r["noise"] > .20 for r in rows),
                       "timeout_boundary_states": [r["name"] for r in rows if r["at_timeout_boundary"]],
                       "sample_range": [min(r["samples"] for r in rows), max(r["samples"] for r in rows)],
                       "rows": rows})
    return output


def probe(outdir):
    build = Path("/home/lktr/src/cccl/build/cub-benchmark")
    binary = build / "bin/cub.bench.reduce.sum.base"
    powercfg = "/mnt/c/Windows/System32/powercfg.exe"
    turbo = "6fecc5ae-f350-48a5-b669-b472cb895ccf"
    env = dict(os.environ, LD_LIBRARY_PATH=f"{build}/lib:/usr/lib/wsl/lib:/usr/local/cuda/lib64")
    outdir.mkdir(parents=True, exist_ok=False)
    manifest = {"utc_start": dt.datetime.now(dt.timezone.utc).isoformat(),
                "binary": str(binary), "binary_sha256": hashlib.sha256(binary.read_bytes()).hexdigest(),
                "ld_library_path": env["LD_LIBRARY_PATH"], "runs": [],
                "limits": "six processes, two states each, 1000 accepted samples/state, 15 s/state, 90 s/process",
                "scope": "warmup diagnostic only; no source change, no performance-fix claim"}
    def capture(cmd):
        p = subprocess.run(cmd, capture_output=True, timeout=20)
        return {"command": cmd, "returncode": p.returncode,
                "stdout": p.stdout.decode("utf-8", errors="replace"),
                "stderr": p.stderr.decode("utf-8", errors="replace")}
    def save():
        (outdir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    manifest["cccl_head"] = capture(["git", "-C", "/home/lktr/src/cccl", "rev-parse", "HEAD"])
    manifest["nvbench_head"] = capture(["git", "-C", str(build / "_deps/nvbench-src"), "rev-parse", "HEAD"])
    manifest["gpu_before"] = capture(["/usr/lib/wsl/lib/nvidia-smi"])
    save()
    # AB BA AB: time order retained; three independent processes per setting.
    for index, warmups in enumerate([1, 20, 20, 1, 1, 20], 1):
        prefix = outdir / f"run{index}-warmup{warmups}"
        mode = capture([powercfg, "/getactivescheme"])
        if turbo not in mode["stdout"].replace("\x00", ""):
            manifest["abort"] = {"reason": "Turbo not active", "mode": mode}
            save()
            raise RuntimeError("Turbo not active; no further GPU work")
        cmd = [str(binary), "-d", "0", "-a", "T{ct}=I32", "-a", "OffsetT{ct}=I32",
               "-a", "Elements{io}[pow2]=[16,24]", "--stopping-criterion", "sample-count",
               "--target-samples", "1000", "--cold-warmup-runs", str(warmups),
               "--timeout", "15", "--json", str(prefix.with_suffix(".json")),
               "--md", str(prefix.with_suffix(".md"))]
        entry = {"command": cmd, "power_before": mode, "warmups": warmups,
                 "utc_start": dt.datetime.now(dt.timezone.utc).isoformat()}
        manifest["runs"].append(entry)
        save()
        start = time.monotonic()
        with prefix.with_suffix(".stdout.log").open("wb") as stdout, prefix.with_suffix(".stderr.log").open("wb") as stderr:
            try:
                p = subprocess.run(cmd, env=env, cwd=build, stdout=stdout, stderr=stderr, timeout=90)
                entry["returncode"] = p.returncode
            except subprocess.TimeoutExpired:
                entry["abort"] = "90 second process limit exceeded"
                save()
                raise
        entry["elapsed_s"] = time.monotonic() - start
        entry["power_after"] = capture([powercfg, "/getactivescheme"])
        logs = "\n".join(prefix.with_suffix(ext).read_text(errors="replace")
                         for ext in [".stdout.log", ".stderr.log", ".md"] if prefix.with_suffix(ext).exists())
        entry["deadlock_detected"] = "deadlock" in logs.lower()
        entry["rows"] = records(prefix.with_suffix(".json")) if p.returncode == 0 else []
        save()
        print(f"run {index}/6 warmups={warmups}: {entry['elapsed_s']:.2f}s, exit={p.returncode}", flush=True)
        if (p.returncode != 0 or entry["deadlock_detected"] or len(entry["rows"]) != 2
                or any(r["samples"] != 1000 for r in entry["rows"])
                or turbo not in entry["power_after"]["stdout"].replace("\x00", "")):
            raise RuntimeError("Probe guard failed; inspect manifest; no further GPU work")
    manifest["gpu_after"] = capture(["/usr/lib/wsl/lib/nvidia-smi"])
    manifest["groups"] = []
    for n in [65536, 16777216]:
        for warmups in [1, 20]:
            rows = [r for run in manifest["runs"] if run["warmups"] == warmups
                    for r in run["rows"] if int(r["axes"]["Elements{io}"]) == n]
            medians = [r["median_s"] * 1e6 for r in rows]
            means = [r["mean_s"] * 1e6 for r in rows]
            manifest["groups"].append({"elements": n, "warmups": warmups,
                "medians_us": medians, "means_us": means,
                "median_span_pct": 100 * (max(medians) - min(medians)) / statistics.median(medians),
                "noise_pct": [100 * r["noise"] for r in rows],
                "iqr_pct": [100 * r["iqr"] for r in rows]})
    save()
    print(json.dumps(manifest["groups"], indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_files", nargs="*", type=Path)
    parser.add_argument("--probe-dir", type=Path)
    args = parser.parse_args()
    if args.probe_dir:
        probe(args.probe_dir)
    elif args.json_files:
        print(json.dumps(audit(args.json_files), indent=2))
    else:
        parser.error("provide input JSON paths or --probe-dir")
