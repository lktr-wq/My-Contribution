# Official-structure bounded-length benchmark — 2026-09-18

## Decision

Continue to a bounded regression/workload screen. The guarded local prototype reduces time about 27.5–28.1% versus official for the three measured shapes. This is a **local diagnostic result**, not an upstream patch, merged contribution or general workload claim. It does not establish that every binary_search call benefits.

## Controls and execution

- Three entries: official (0), same-structure wide clone (1), same-structure guarded32 clone (2). No early exit added.
- Runtime haystack length is a 64-bit kernel argument read from the command line; the benchmark was not compiled with a fixed 20,000 length. The host allocation limit does not specialize device code. The guarded kernel retains both narrow and wide paths.
- N=20,000, 4,096 blocks, 256 threads/block, every block repeats the entire query list; shared atomic hit counting is unchanged across entries. Shapes: ascending distributed hits, all misses above maximum, identical midpoint hits.
- CUDA events time only each kernel launch. Three rounds with variant-order rotation, 20 warmups and 30 samples per variant/shape/round; 810 retained samples. A full discarded run immediately precedes the retained run. No samples were filtered.
- Windows reported Turbo before execution; initial snapshot P8, 40 C, 7% utilization. Retained-run telemetry has 46 samples: 44 at 2565 MHz, 2 at 2580 MHz (0.585% range). Telemetry is roughly 200-ms polling and does not prove every individual kernel was disturbance-free.
- Check-only: 180,000 per-query checks and 36,864 block-count checks passed. Each warm/measurement run: 180,000 per-query checks plus 221,184 pre/post block-count checks passed, with output guards. The known shape formulas supply exact expected bool/count results. Previous generic/large-range correctness evidence remains separate.
- Build 5.587 s; check 0.473 s; SASS extraction 0.622 s; preheat 9.347 s; measurement 9.348 s. Upstream checkout remains clean at `f747ef146b77ed1e8f38fe8cb3c67effaf7793f2`.

## Results

Milliseconds per launch; median of three round medians. Improvement means reduction in elapsed time, not percentage increase in throughput.

| Shape | Official | Wide clone | Guarded32 | Reduction vs official | Reduction vs clone |
|---|---:|---:|---:|---:|---:|
| Distributed hits | 7.303680 | 7.416240 | 5.275984 | 27.76% | 28.86% |
| All high misses | 6.793120 | 6.915072 | 4.883456 | 28.11% | 29.38% |
| Midpoint hits | 6.818304 | 6.840240 | 4.943872 | 27.49% | 27.72% |

All paired rounds improve over clone64: distributed hits 27.74–31.21%; misses 23.86–30.10%; midpoint hits 27.50–27.96%. There is noise: despite identical normalized instructions, one distributed-hit clone round reaches 7.669488 ms while its official counterpart is 7.289760 ms. Do not interpret sub-percent differences or report the most favorable single round. The repeated >20% gap supports continuation, not a final confidence interval or production guarantee.

## Generated-code inspection

- Official and clone64 repeated-search kernels have **identical normalized instruction sequences**, including registers, predicates and branch targets after removing address/encoding comments. SHA256 `0a3fbaeca0b329393f0d39f9c3a687339512ae063765a7d20f98ee0794e16055`.
- All three repeated kernels use 28 registers with zero spills. Narrowing did not reduce the reported register count in this experiment.
- Guarded32 SASS retains the `0x7fffffff` comparison and a branch to the wide path at relative address `0x660`. The narrow loop uses a 32-bit unsigned right shift for the half-length calculation; pointer addressing remains wide.
- Static instruction-line counts: official/clone64 128 each; guarded32 192, including padding and both paths. Larger static code is a potential tradeoff, not evidence of more dynamically executed work. Normalized text identity is not a claim that every binary scheduling/control bit was separately compared.

## Failed initial compile and reproducibility

The first source version included an older correctness `.cu` with its main renamed. NVCC failed with an internal assertion in `src_seq.c` / `recycle_src_seq_entry`. Removing that unnecessary inclusion and declaring the small CUDA error/RAII helpers locally compiled successfully. The algorithm header was unchanged. This is an observed workaround, not a diagnosed NVCC root cause or a compiler bug report.

- Failed attempt: `evidence/raw/phase2/2026-09-18-bounded-bench/`.
- Successful build, checks, SASS, preheat, samples, telemetry, summaries and hashes: `evidence/raw/phase2/2026-09-18-bounded-bench-r2/`.
- Executable SHA256: `b9efe5ecd1db4baf1b015e9eda27b56a5d4bedbe1c0bad3e753edfbe1aab5e60`.
- `run_bounded_bench.py` compiles, checks, dumps SASS, preheats, measures and summarizes. `analyze_bounded_bench.py` computes reductions, normalized instruction hashes and retained-window frequency summary. GPU timestamp parsing assumes the recorded Asia/Shanghai timezone.
- The runner also hashes the old correctness source for provenance, but the successful benchmark no longer includes or executes it. It uses the unchanged bounded prototype header verified in the preceding stage.

```powershell
wsl -d CCCL-Ubuntu -u lktr -- python3 '/mnt/d/Projects/Open-Source Contribution/evidence/phase2/run_bounded_bench.py' '<new absolute WSL output directory>'
wsl -d CCCL-Ubuntu -u lktr -- python3 '/mnt/d/Projects/Open-Source Contribution/evidence/phase2/analyze_bounded_bench.py' '<same output directory>'
```

## Remaining limits and next stage

Compute Sanitizer remains unavailable because of the WDDM debugger-interface failure recorded in the preceding stage; do not claim sanitizer validation. These are cache-friendly repeated searches, sorted query order or uniform queries, one GPU/compiler, one length, classic pointer iterators, sequential rotated measurement groups, and no long-term noise study. Physical huge arrays and wide-fallback performance were not measured.

Next stage, after confirmation, at most ten minutes: extend the screen to a small selection of tiny/medium lengths and shuffled/mixed hit-miss queries, keeping total work/time bounded. Check whether dispatch overhead or less coherent queries erase the gain. This step does not authorize tuning indefinitely or modifying upstream code. If robust, only then prepare an isolated overlay and targeted upstream regression tests, refresh duplicate/maintainer status, and assess submission suitability.
