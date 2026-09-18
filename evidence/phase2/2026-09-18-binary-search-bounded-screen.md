# Bounded search workload screen — 2026-09-18

## Outcome

The gain survives shuffled and mixed queries at several lengths, but is strongly size-dependent. No measured cell has a negative paired-round median reduction; this is not proof of no regressions outside this screen. Do not generalize the earlier roughly 28% reduction to all calls. Continue with a less repetitive execution pattern before attempting an upstream patch.

## Method and correctness

- Reused the same three kernel templates and unchanged bounded algorithm header: official / wide clone / guarded32. The earlier benchmark entry is preserved by renaming its main in this separate translation unit. No upstream source edits.
- Seven runtime lengths: 1, 8, 32, 257, 4,096, 20,000, 65,536. Sorted haystack contains `2*i`.
- 4,096 queries per cell, deterministic xorshift generation plus Fisher-Yates shuffle. Shape 0: randomly selected even-valued hits with replacement. Shape 1: exactly half even hits, half odd misses, shuffled. Odd misses are within value gaps except those following the final element. At N=1, the all-hit shape is necessarily constant.
- Unlike the earlier 4,096-block/N-query benchmark, this bounded screen uses 512 blocks and a fixed 4,096-query list per block. This keeps work manageable and comparable across lengths. Do not compare its absolute milliseconds directly with the previous run.
- Each sample times a batch of three kernel launches and divides by three. Thirty samples, three rotated-order rounds, 20 warmup launches per variant. 14 cells × 3 variants × 3 rounds × 30 = 3,780 retained samples. Full discarded preheat run precedes the retained run.
- Check-only validates 172,032 individual outputs against CPU `std::binary_search` and 21,504 per-block hit totals, with output guards. Each preheat/measurement run repeats 172,032 per-query checks and 129,024 pre/post block checks; all passed.
- Compilation 5.588 s; check-only 0.373 s; discarded preheat 2.628 s; retained measurement 2.526 s.
- Turbo confirmed before and after. Initial GPU snapshot P8, 40 C, 6% utilization. Fifteen telemetry samples during/after retained-run start report 2,580 MHz (10) or 2,565 MHz (5), range 0.585%. The roughly 200-ms telemetry cannot attribute clock/load to every short cell or kernel. No timing samples were removed.

## Results

Elapsed-time reduction versus official, using median of three round medians. Positive means less time. Full times, clone controls and per-round reductions are retained in `summary.json` and `rounds.json`.

| Length | Shuffled hits | Shuffled 50% hit/miss |
|---:|---:|---:|
| 1 | 8.78% | 7.28% |
| 8 | 21.03% | 20.18% |
| 32 | 22.98% | 22.25% |
| 257 | 24.50% | 24.40% |
| 4,096 | 1.74% | 2.55% |
| 20,000 | 24.30% | 24.42% |
| 65,536 | 4.62% | 4.57% |

At N=20,000, official/guarded times are 0.201557/0.152576 ms for hits and 0.202747/0.153227 ms for mixed queries. The benefit is therefore not limited to monotonically ordered queries or all-hit input in this repeated-work setting.

At N=4,096 and 65,536, reductions are below the project's continuation threshold for a standalone candidate; do not sell them as substantial gains or spend this stage explaining/tuning them. At N=8 some paired rounds fall below 20%, despite aggregate reductions near 20%. The stronger cells N=32, 257 and 20,000 remain above 20% in all three paired rounds. N=1 samples are short and relatively noisy (hit reductions span 6.7–16.3% across paired rounds).

No aggregate-average speedup across these arbitrarily selected cells is reported. Size dependence is observed; the mechanism behind it is not established by this screen.

## Evidence and reproduction

Sources: `binary_search_bounded_screen.cu`, `run_bounded_screen.py`, existing bounded header and benchmark kernel source. Raw directory: `evidence/raw/phase2/2026-09-18-bounded-screen/`, containing source hashes, exact commands, successful manifest, compile output, check/preheat/measurement logs, telemetry and summaries.

```powershell
wsl -d CCCL-Ubuntu -u lktr -- python3 '/mnt/d/Projects/Open-Source Contribution/evidence/phase2/run_bounded_screen.py' '<new absolute WSL output directory>'
```

Pinned CCCL remains clean at `f747ef146b77ed1e8f38fe8cb3c67effaf7793f2`. The three repeated kernels each report 28 registers and no spills in this build. SASS identity was established in the preceding stage, not re-extracted here. Executable SHA256 `0fead7ee98a6b436dd4d6879cf2dfea0f0bec69eee689e38ac2fb21affcac8df`.

## Limits and next stage

One GPU/compiler, one deterministic seed per cell, small repeated/cached datasets, a shared atomic counter, and batches of launches remain artificial. This is not a direct measurement of one isolated search or of dispatch overhead without repeated work. Short launches include inter-launch overhead in the three-launch batch average. Generic correctness and the unavailable WDDM Compute Sanitizer are documented in the preceding stage; no sanitizer success is claimed here.

Recommended next ten-minute stage after confirmation: use the already available one-query-per-thread kernel, without per-block repeated queries or shared hit aggregation, on a small selection of the same lengths. Validate every query and compare the same three implementations. This checks whether the benefit persists beyond the issue reproducer's repeated-work structure; stop/pivot based on that result, rather than immediately preparing an upstream change. No system changes, upstream edits or public messages are authorized by this report.
