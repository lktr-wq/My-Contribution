# CPU cost screen — 2026-09-19

## Decision

The current shared host/device overlay is not a pure-benefit change. The single-element all-hit CPU workload regressed consistently across five alternating baseline/overlay rounds: 20.63–21.98%, with aggregate median query cost increasing from 1.114 to 1.344 ns (about 0.230 ns/query). Consider retaining the original host path and restricting the optimization to device execution. That change is not implemented in this stage.

## Method

WSL CCCL-Ubuntu, GCC 13.3.0, `-O3 -std=c++17 -fno-lto`. Separate baseline and actual-overlay executables compiled from identical source. Dependency listings verify header selection. Each process is pinned using taskset to the first CPU allowed by sched_getaffinity (recorded in manifest). WSL CPU affinity limits guest scheduling; it does not guarantee a dedicated physical core or constant host frequency.

Six array lengths (1,32,257,4096,20000,65536), sorted even values; 65,536 deterministically shuffled queries per case, either all hits or half hits/odd misses. Every query is checked against host std::binary_search before timing. Timed batches return a hit total, checked against the oracle total and consumed through a volatile sink. The query-batch function is noinline; no LTO. Three warmup batches and nine timed batches per cell/process, five alternating process-order rounds. Reported ns/query is batch wall time divided by query count, not isolated single-call latency. No samples filtered.

All per-query correctness and timed-total checks passed. Upstream remained clean at f747ef146b77ed1e8f38fe8cb3c67effaf7793f2. No GPU benchmark or system configuration change was performed.

## Results

Median of five round medians; positive means slower with overlay.

| Length | All-hit slowdown | Mixed-query slowdown |
|---:|---:|---:|
| 1 | +20.65% | +10.09% |
| 32 | -0.03% | +0.46% |
| 257 | +2.44% | -2.71% |
| 4096 | -0.87% | -0.75% |
| 20000 | -2.11% | -1.29% |
| 65536 | -0.64% | -2.64% |

N=1 mixed is slower in every paired round, but the magnitude varies from 1.02% to 12.07%. N=1 hits is the clearest regression. Several other cells change direction across rounds; small aggregate differences should not be sold as reliable general CPU improvements. N=257 mixed improves in all rounds in this screen, but one round is only 0.20%. No statistical significance, compiler-independent result, or cycle-level cause is claimed. No CPU frequency locking/telemetry or instruction-level profiling was performed.

## Evidence and limitations

Sources: cpu_search.cpp and run_cpu_search.py. Successful logs, compiler/CPU metadata, commands, round sample outputs and summary.json: evidence/raw/phase2/2026-09-19-cpu-search-r2/.

The first attempt stopped at dependency verification because `-MM` excludes system-marked headers. Changed to `-M`, which includes them, then reran the full screen. Initial logs are preserved at evidence/raw/phase2/2026-09-19-cpu-search/. No algorithm changes were made between attempts.

This is one compiler, one machine, cached/reused query data, integer pointers and limited sizes. CPU results do not invalidate measured GPU benefits, but they do invalidate describing the current shared patch as cost-free. Register/code-size costs recorded in GPU reports also remain.

Next stage after user confirmation: create a device-only dispatch while leaving host execution on the original path, then re-run CPU correctness/control checks and targeted GPU checks. Do not publish the current shared patch as universally beneficial.
