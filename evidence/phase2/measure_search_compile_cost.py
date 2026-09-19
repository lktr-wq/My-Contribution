"""Focused compile/code-size screen. Does not execute GPU code."""
import argparse
import hashlib
import json
import re
import shutil
import statistics
import subprocess
import time
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("output", type=Path)
p.add_argument("--cccl", type=Path, default=Path("/home/lktr/src/cccl"))
p.add_argument("--cuda", type=Path, default=Path("/usr/local/cuda"))
p.add_argument("--source", type=Path)
p.add_argument("--expected-kernels", type=int, default=1)
a = p.parse_args()
root = Path(__file__).resolve().parent
a.output.mkdir(parents=True, exist_ok=False)
build = a.output / "build"
build.mkdir()
records = []

def run(label, cmd):
    start = time.perf_counter()
    result = subprocess.run([str(x) for x in cmd], capture_output=True, timeout=60)
    elapsed = time.perf_counter() - start
    (a.output / (label + ".stdout.log")).write_bytes(result.stdout)
    (a.output / (label + ".stderr.log")).write_bytes(result.stderr)
    records.append(dict(label=label, command=[str(x) for x in cmd], seconds=elapsed,
                        returncode=result.returncode))
    (a.output / "commands.json").write_text(json.dumps(records, indent=2))
    result.check_returncode()
    return elapsed, result.stdout.decode()

_, head = run("head", ["git", "-C", a.cccl, "rev-parse", "HEAD"])
_, status = run("status", ["git", "-C", a.cccl, "status", "--porcelain"])
assert head.strip() == "f747ef146b77ed1e8f38fe8cb3c67effaf7793f2" and not status.strip()
run("nvcc-version", [a.cuda / "bin/nvcc", "--version"])
run("host-version", ["g++", "--version"])
run("system", ["uname", "-a"])
source = a.source.resolve() if a.source else root / "search_compile_cost.cu"
overlay = root / "bounded_overlay"
hashes = {str(f): hashlib.sha256(f.read_bytes()).hexdigest()
          for f in [source, overlay / "cuda/std/__algorithm/lower_bound.h", Path(__file__)]}
shutil.copy2(source, build / source.name)
shutil.copytree(overlay, build / "overlay")
source = build / source.name
overlay = build / "overlay"
summary = {}
for kind, flag, suffix in [("object", "-c", ".o"), ("cubin", "--cubin", ".cubin")]:
    timings = {"baseline": [], "overlay": []}
    for r in range(-1, 6):  # one untimed warmup pair, six alternating measured pairs
        for mode in (["baseline", "overlay"] if r % 2 == 0 else ["overlay", "baseline"]):
            cmd = [a.cuda / "bin/nvcc", "-O3", "-std=c++17", "-arch=sm_89", "--ptxas-options=-v"]
            if mode == "overlay":
                cmd += ["-I" + str(overlay)]
            cmd += ["-I" + str(a.cccl / "libcudacxx/include")]
            if r == -1:
                _, deps = run(kind + "-" + mode + "-dependencies", cmd + ["-M", source])
                expected = (overlay if mode == "overlay" else a.cccl / "libcudacxx/include") / "cuda/std/__algorithm/lower_bound.h"
                assert str(expected) in deps.replace("\\ ", " ")
            elapsed, _ = run(f"{kind}-{mode}-{r}", cmd + [flag, source, "-o", build / (mode + suffix)])
            if r >= 0:
                timings[mode].append(elapsed)
            print(kind, mode, r, round(elapsed, 3), flush=True)
    med = {m: statistics.median(v) for m, v in timings.items()}
    summary[kind] = dict(seconds=timings, median_seconds=med,
                         median_increase_percent=100 * (med["overlay"] / med["baseline"] - 1))
for mode in ["baseline", "overlay"]:
    cubin = build / (mode + ".cubin")
    _, sections = run(mode + "-sections", ["readelf", "-SW", cubin])
    run(mode + "-sass", [a.cuda / "bin/cuobjdump", "--dump-sass", cubin])
    run(mode + "-resources", [a.cuda / "bin/cuobjdump", "--dump-resource-usage", cubin])
    matches = re.findall(r"\.text\.(search_cost\w*)\s+PROGBITS\s+\S+\s+\S+\s+([0-9a-fA-F]+)", sections)
    assert len(matches) == a.expected_kernels
    sizes = {name: int(size, 16) for name, size in matches}
    summary[mode] = dict(kernel_text_bytes=sum(sizes.values()), per_kernel_text_bytes=sizes, cubin_bytes=cubin.stat().st_size,
                         object_bytes=(build / (mode + ".o")).stat().st_size)
summary["source_hashes"] = hashes
summary["note"] = "Public binary_search instantiations; runtime length; no GPU execution. Warm filesystem caches; six alternating pairs per build mode."
summary["expected_kernels"] = a.expected_kernels
(a.output / "summary.json").write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2), flush=True)
