# #11412 local measurement — 2026-09-18

## Decision

The reported performance gap reproduces on this RTX 4060 Laptop for the diagnostic workload. Continue investigating bounded index width in the official implementation. **This is not an upstream-ready optimization or a general binary_search speedup claim.** Early exit is input-dependent and is not the preferred blanket change.

## Execution and checks

- User confirmed enhanced mode. Windows reported Turbo (`6fecc5ae-f350-48a5-b669-b472cb895ccf`) before and after execution.
- Initial GPU snapshot: P8, 41 C, 5% utilization, 210 MHz. No system settings were changed by the runner.
- Ran the previously verified binary, SHA256 `9eb1023c3093e5084690d5b9e2a5dd8d96c1b9ead006183b8281546c800f72ec`.
- First measurement completed in 9.997 seconds. Its telemetry included startup clock ramping, so a second run used a complete discarded preheat pass immediately before measurement.
- Preheat plus retained second measurement completed in 20.082 seconds. Each measured run contains 1,350 samples: 3 query shapes × 3 rounds × 5 variants × 30 samples. Each variant also has 20 warmup launches per round.
- Each run passed the original 165-configuration / 2,595-comparison suite, 300,000 additional per-query checks, 61,440 pre-timing block checks, post-timing block counts, and output guards. No CUDA errors were reported.
- Warm measurement started at 14:13:34.784 UTC. The 48 telemetry samples after that timestamp report 2565 MHz (46 samples) or 2580 MHz (2 samples), a 0.585% range. Telemetry is sampled every approximately 200 ms, not per kernel; it cannot prove absence of every transient or unrelated GPU activity. No individual timing samples were filtered.

## Results

Milliseconds per launch, median of the three round medians, **warm run**. Each launch uses 4,096 blocks × 20,000 queries, with 256 threads per block and shared atomic hit counting. The small haystack and query list are repeatedly reused.

| Input | Official | Reference lower64 | Reference early64 | Reference lower32 | Reference early32 |
|---|---:|---:|---:|---:|---:|
| Distributed hits | 7.410176 | 5.197824 | 4.719024 | 3.008512 | 3.654000 |
| All misses above maximum | 6.873984 | 4.778832 | 3.812176 | 2.697728 | 2.633616 |
| All queries hit initial midpoint | 6.997504 | 4.875648 | 0.477024 | 2.778528 | 0.414032 |

Interpretation:

- Distributed hits: lower32 takes about 59.4% less time than official (2.46× throughput for fixed work). But the reference loop differs from official, so this comparison does **not** isolate index width.
- Within the otherwise matching lower-bound reference template, 64→32-bit index reduces time by about 42.1% on distributed hits; similar reductions occur in both other shapes. This supports examining a bounded-width path, including the compiler effects of changing the type.
- Adding early exit to lower32 makes distributed hits about 21.5% slower. At 64-bit width it makes that input about 9.2% faster. Therefore the effects are not simply additive.
- Midpoint-only input gives early exit an intentionally favorable case: about 90.2% less time for early64 versus lower64. This is not a typical-workload gain.
- Even on all-miss input, the early variant differs in speed although it never takes a successful early exit. Generated control flow and final-check differences matter; do not explain every difference as fewer search iterations.
- All three rounds agree on the main rankings. Official distributed-hit round medians range 7.394176–7.559680 ms; lower32 ranges 3.007856–3.011584 ms. Some single samples have latency spikes. The first run has the same main rankings.

## Evidence and reproduction

Runner: `evidence/phase2/measure_binary_search.py`. It checks the executable hash, applies a 180-second timeout to each benchmark invocation, saves raw output and GPU telemetry, and checks sample counts and successful correctness completion. With preheat enabled, there are two separately bounded invocations, not a single 180-second global deadline.

```powershell
wsl -d CCCL-Ubuntu -u lktr -- python3 '/mnt/d/Projects/Open-Source Contribution/evidence/phase2/measure_binary_search.py' '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-18-binary-search-measure-warm' --preheat
```

Use a new output directory for reruns. Raw evidence directories:

- `evidence/raw/phase2/2026-09-18-binary-search-measure/` — initial measurement, without full preheat.
- `evidence/raw/phase2/2026-09-18-binary-search-measure-warm/` — preheat logs, retained samples, per-round summary, telemetry and manifest.

The initial run used the runner before the optional preheat branch and measurement-start timestamp were added. The benchmark executable was identical throughout. Raw logs remain unfiltered.

## Next stage, requires confirmation

Within ten minutes, inspect the official iterator/difference-type dispatch and design a local bounded-index prototype that preserves its search structure. For eligible random-access ranges whose length fits a chosen index type, use narrow arithmetic; retain the original path for other iterators or larger ranges. Confirm overflow and generic comparator/iterator constraints before implementation. Prefer testing official64 versus official-bounded32 rather than attributing the full reference-loop gap to index width.

This stage did not change upstream code, submit a PR/comment, claim a generic fix, or establish production-workload gains. Existing unrelated working-tree changes were preserved.
