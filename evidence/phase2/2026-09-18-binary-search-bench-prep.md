# #11412 benchmark preparation — 2026-09-18

## Outcome

Prepared the local CUDA-event benchmark entry and checked generated SASS. **No performance measurements were run.** No upstream implementation was modified.

- Pinned CCCL: `f747ef146b77ed1e8f38fe8cb3c67effaf7793f2`; source checkout clean before and after.
- Compilation: CUDA 13.3, `-O3 -std=c++17 -arch=sm_89 --ptxas-options=-v`.
- Existing correctness suite: 165 configurations / 2,595 comparisons passed.
- Added benchmark-input checks: 300,000 per-query comparisons and 60 per-block count checks passed, including output guards.
- Compile/check/SASS extraction took 5.236 / 0.473 / 0.573 seconds respectively.

## Benchmark structure

`binary_search_11412_bench.cu` reuses the existing correctness implementation and adds five repeated-search kernels: official, lower64, early64, lower32, early32. As in the original report, each block searches the same query list; hits are accumulated through a shared counter.

Inputs contain 20,000 sorted integers. Query shapes are distributed hits, all misses, and repeated midpoint hits. Check mode runs four blocks per variant/shape and also checks each query separately against the CPU oracle.

The unexecuted `--measure` path uses 4,096 blocks, three rounds, rotated variant order, 20 warmups and 30 CUDA-event samples per variant/shape/round. Allocation and copies are outside the timed interval. It checks outputs before and after timing. Before executing this path, add a bounded runner and collect fresh power/GPU environment evidence.

## Generated-code evidence, not speed evidence

| Variant | Registers | Static SASS instruction lines |
|---|---:|---:|
| official | 26 | 120 |
| lower64 | 16 | 88 |
| early64 | 14 | 72 |
| lower32 | 12 | 64 |
| early32 | 10 | 64 |

All five kernels have zero spill stores/loads. Their normalized instruction hashes differ. The 64-bit reference variants retain `SHF.R.S64` and carry/high-word operations; 32-bit references do not contain that shift opcode. Pointer addressing still uses 64-bit operations.

Static instruction counts include padding/NOPs and are not executed instruction counts. Register counts and differing code do not establish a runtime benefit or isolate every compiler effect.

## Reproduction and evidence

From Windows PowerShell:

```powershell
wsl -d CCCL-Ubuntu -u lktr -- python3 '/mnt/d/Projects/Open-Source Contribution/evidence/phase2/prepare_binary_search_bench.py' '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-18-binary-search-bench-prep'
```

Raw logs, exact commands, source/binary hashes, kernel hashes and checkout status are under `evidence/raw/phase2/2026-09-18-binary-search-bench-prep/`. The executable is excluded from Git. The manifest explicitly records `performance_tested: false`.

## Boundaries and next stage

These are diagnostic integer/sorted-array experiments, not a generic library replacement or official NVBench result. Generic comparator/iterator and partition-contract coverage remains outside this stage. Repeated small inputs favor cache residency. Sequential rotated variants are not fully randomized interleaving.

At 14:07 UTC, Windows reported the Silent power scheme. Do not use this check run for performance claims. Next stage, subject to user confirmation: plugged-in/enhanced mode and paused dynamic wallpaper, fresh GPU/environment check, then a deadline-bounded three-round measurement and summary. Stop after at most ten minutes; partial or noisy data must be labeled accordingly. No public submission is authorized.
