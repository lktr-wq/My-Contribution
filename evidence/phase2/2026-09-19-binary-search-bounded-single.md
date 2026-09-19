# One-query-per-thread bounded search — 2026-09-19

## Outcome

The gain is not exclusive to repeated-per-block queries or shared atomic hit counting. In the larger-query follow-up, N=32 and N=20,000 retain more than 20% reduction in every paired round for both query shapes. N=257 has about 25% aggregate reduction, but one mixed-query round is only 15.5%. N=4,096 has a small measured slowdown; N=65,536 is essentially unchanged. **Do not claim a universal improvement or no regressions.**

This stage added only local diagnostics. The upstream checkout and bounded algorithm header were unchanged.

## Method

- Uses the existing `bounded_kernel<V, false>`: each thread searches exactly one query and writes its bool result. No per-block query loop, shared hit counter or atomic aggregation in this path.
- Official, wide clone and guarded clone; runtime 64-bit length. N=1, 32, 257, 4,096, 20,000, 65,536; even-valued sorted arrays, deterministic shuffled all-hit and 50% hit/odd-miss query lists.
- Three rotated-order rounds, 30 samples per variant/cell/round, three kernel launches per sample with elapsed time divided by three. All launches independently search their query list; repeated launches are timing repetitions, not repeated searches within a thread.
- Timed work excludes allocations, copies and CPU oracle generation. Every query output is checked against CPU `std::binary_search` before and after timing, plus two output guards.

## First attempt: not accepted as performance evidence

262,144 queries/launch, 20 warmups. All normal checks passed, but kernels were short and several cells had large, direction-changing timing fluctuations. The six telemetry samples at/after retained-run start included three at 2250 MHz and three at 2580 MHz. This failed the stable-frequency screening condition. Keep these logs, but do not use apparent large regressions or gains as reliable findings.

Raw directory: `evidence/raw/phase2/2026-09-19-bounded-single/`. The original source/runner hashes are recorded. This version differed from the final version by query count (262,144 versus 4,194,304), warmups (20 versus 50), and the corresponding expected validation counts in the runner.

## One bounded follow-up

Increased independent queries to 4,194,304 per launch and warmups to 50; algorithm and kernels unchanged. This increases the query/output working set and changes workload scale, so it is not a same-size confirmation of the original short-kernel measurements. A full discarded run immediately preceded retained measurement.

- Check-only: 150,994,944 query comparisons passed.
- Each preheat/measurement invocation: 905,969,664 pre/post query comparisons passed, including output guards.
- 3,240 retained sample averages (12 cells × 3 variants × 3 rounds × 30). No samples removed.
- Compile approximately 5.84 s, check 3.13 s, preheat 9.65 s, measurement 9.45 s; exact commands/durations in manifest.
- Turbo reported before and after this stage. Retained-window telemetry: 48 samples, 27 at 2565 MHz and 21 at 2580 MHz, 0.585% range. Sampling is approximately 200 ms, not per-kernel proof against interference.

## Larger-query results

Elapsed-time reduction versus official from median of three round medians; positive means faster. Not percentage throughput increase.

| Haystack length | Shuffled hits | Shuffled half hit/miss |
|---:|---:|---:|
| 1 | 12.12% | -0.35% |
| 32 | 23.70% | 24.37% |
| 257 | 25.47% | 25.75% |
| 4,096 | -0.21% | -0.35% |
| 20,000 | 26.41% | 26.63% |
| 65,536 | 0.02% | 0.00% |

N=20,000: official/guarded approximately 0.384000/0.282592 ms (hits), 0.384277/0.281925 ms (mixed). Paired reductions range 26.27–26.71% and 26.16–26.86%, respectively.

N=4,096: all paired rounds show small negative reductions (roughly -0.20% to -0.57%). This is a measured mild slowdown, not a demonstrated significant/general regression. N=65,536 fluctuates around zero. N=1 remains noisy and the official/wide-clone controls differ materially in one cell; do not treat its 12% aggregate gain as established.

N=257 mixed has one 15.52% paired round. Do not describe every medium-sized case as passing the 20% continuation screen in every round. Robust evidence from N=32 and N=20,000 is sufficient to justify a carefully scoped next step, not indiscriminate deployment.

## Code generation and limits

The official and wide-clone single-query kernels have identical normalized SASS text, including registers/predicates/branch operands after removing address/encoding comments. Their normalized instruction-line counts are 88 each; guarded clone 136. This confirms the control implementations compile alike, not that every timing fluctuation should disappear. Static counts include unused-path/padding effects and are not dynamic counts.

Official and clone64 use 23 registers; guarded32 uses 26, all without spills. More code/registers are real tradeoffs requiring consideration before a generic library change.

The synthetic large-range fallback correctness checks from the prior stage remain relevant, but large physical-array fallback performance, other GPUs/compilers and host performance remain untested. Data is reused between timing launches. The larger query/output buffers also make memory traffic more important; no profiler attribution is claimed. Compute Sanitizer is still unavailable due to the previously recorded WDDM initialization failure. This stage did not alter system/debugger settings.

## Artifacts and next stage

- Sources: `binary_search_bounded_single.cu`, `run_bounded_single.py`.
- Accepted follow-up logs: `evidence/raw/phase2/2026-09-19-bounded-single-large/`, including sample output, per-round/cell summaries, SASS, telemetry, source hashes, binary hash and successful manifest.
- Reproduce by running `run_bounded_single.py` in CCCL-Ubuntu with a new absolute WSL output directory. The final runner uses the larger query count.
- Pinned upstream HEAD remains `f747ef146b77ed1e8f38fe8cb3c67effaf7793f2`, clean before/after.

Recommended next ten-minute stage after confirmation: refresh upstream issue/PR status for duplicate work; if no conflicting implementation is found, prepare an isolated header overlay and run focused official lower_bound/binary_search/equal_range regression tests. Do not modify the source checkout or post publicly. If duplicate work or a meaningful semantic issue appears, stop/pivot rather than add more performance screens indefinitely.
