# Actual public-API overlay performance — 2026-09-19

## Outcome

The actual lower_bound header overlay retains roughly 24% less elapsed time for N=20,000 through public `cuda::std::binary_search`. N=4,096 and N=65,536 remain effectively flat/slightly slower. This is a local diagnostic result, not a universal improvement, submitted PR or upstream acceptance. This report was saved after an approval-service usage-limit interruption; no measurement was repeated during that recovery.

## Method and validation

Added `PUBLIC_API_ONLY` compile mode to the single-query harness; default three-variant mode remains available. Public mode measures only V=0, which calls the official API. Two separate executables use identical source/flags (`-O3 -std=c++17 -arch=sm_89 -DPUBLIC_API_ONLY`), differing only in the overlay include path. Dependency listings confirm each loads the intended header. Standalone candidate variants are not measured; separate executables avoid mixing differing header definitions in one program.

Each launch handles 4,194,304 queries, one per thread, 256 threads/block, without shared counting or repeated searches within a thread. Haystacks contain sorted even values; queries are shuffled hits or an equal mixture of even hits and odd misses. Four lengths: 32, 4,096, 20,000, 65,536. Copies, CPU oracle generation and allocation are outside timing. Each build passes 33,554,432 check-only comparisons; each preheat/measured process passes 67,108,864 pre/post comparisons against CPU std::binary_search, plus output guards.

Process orders are baseline/overlay, overlay/baseline, baseline/overlay across three rounds. Both builds receive a discarded preheat invocation; every cell has 50 warmups. Thirty samples per cell; final samples average 50 launches each. There are 1,440 retained averages across both builds and three rounds. No samples were filtered.

## Environment and first-attempt limits

Turbo was active. User confirmed background content paused following an initial 29% GPU-utilization snapshot; a subsequent idle snapshot was 5%. No system settings or processes were changed by the agent.

The first attempt averaged three launches and had 2250–2580 MHz readings somewhere during whole-process execution. It lacked per-cell timestamps, so startup/CPU preparation could not be separated from timing. Retain those logs without claiming their frequency gate passed.

One follow-up increased the batch to 50 launches and recorded epoch-millisecond start/end times around each cell's timed sample group. Algorithm and query generation did not change, but timing amortization did. Of 48 measured windows, 47 contain telemetry. One overlay round-2 N=32 mixed window lasted 200 ms and was missed by approximately 200-ms polling. Sampled windows span 2550–2580 MHz (1.18%). All 12 N=20,000 windows have samples in this range. Coarse polling is not proof of zero transient interference. Do not describe every cell as having complete frequency validation.

## Windowed results

Median of three round medians, milliseconds per launch; positive reduction means less time, not percentage throughput increase.

| Length | Shape | Baseline ms | Overlay ms | Time reduction |
|---:|---|---:|---:|---:|
| 32 | hits | 0.168018 | 0.130040 | 22.60% |
| 32 | mixed | 0.165888 | 0.128110 | 22.77% |
| 4,096 | hits | 0.340477 | 0.340716 | -0.07% |
| 4,096 | mixed | 0.340693 | 0.340602 | 0.03% |
| 20,000 | hits | 0.390779 | 0.295575 | 24.36% |
| 20,000 | mixed | 0.389171 | 0.295145 | 24.16% |
| 65,536 | hits | 0.934027 | 0.934626 | -0.06% |
| 65,536 | mixed | 0.932792 | 0.935424 | -0.28% |

N=20,000 paired reductions: 23.98–24.36% (hits), 23.61–24.24% (mixed). Actual-overlay evidence now supports this scoped result independently of standalone-prototype timing. Small negative differences are retained; no assertion of zero regressions is made. Actual API kernel register counts are 23 baseline versus 26 overlay, without spills. SASS is saved; no profiling-based explanation of size dependence is claimed.

## Minimal patch and evidence

`minimal.patch` preserves the original surrounding formatting/license and has three hunks: additional type headers, counted-loop extraction, and bounded dispatch. Its generated candidate matches the compiled overlay after removing comments/whitespace. This is a text-normalization check, not formal language-equivalence proof. `git apply --check` passes against pinned CCCL; no patch was applied to that checkout. The diagnostic helper name and host/device deployment policy are not finalized for submission.

- `measure_public_overlay.py`: build/check/alternate/summarize.
- `check_public_windows.py`: correlate Asia/Shanghai GPU timestamps to timing windows.
- `make_minimal_overlay_patch.py`: generate minimal diff and check applyability.
- `evidence/raw/phase2/2026-09-19-public-overlay/`: initial three-launch attempt.
- `evidence/raw/phase2/2026-09-19-public-overlay-windowed/`: 50-launch attempt, manifest/hashes, raw samples, summary, SASS, dependency lists, `window-clocks.json`, minimal diff and apply-check output.

The source hashes distinguish the first attempt (batch=3, no window timestamps) and follow-up (batch=50, timestamps). A bracket typo in the clock-analysis script was fixed before successful analysis; it did not trigger a benchmark rerun. Previous regression evidence covers six selected official source files and extended cases, not full CI. Compute Sanitizer remains unavailable due to the previously recorded WDDM initialization failure. Host performance, other GPUs/compilers, and large physical-array fallback performance remain untested. Data is reused across timing launches.

## Next stage

Evidence is sufficient to draft a bounded upstream discussion rather than continue open-ended tuning. After user confirmation, prepare an English issue-comment draft and reproduction checklist describing actual-patch gain, flat/slightly slower cases, fallback safety and limitations. Keep it local. Ask maintainers whether the desired scope is shared lower_bound or a device-specific path before expanding the patch. Posting a comment or opening a PR requires separate explicit authorization.
