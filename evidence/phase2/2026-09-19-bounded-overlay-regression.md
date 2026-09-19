# Bounded lower_bound overlay and official regressions — 2026-09-19

## Outcome

Prepared a local header overlay and passed six official regression source files on baseline and overlay, exercising host, GPU and constexpr evaluation. Extended diagnostic cases also pass with the overlay. No upstream checkout edits, public comments, commits to NVIDIA/cccl, or PRs were made. This is an experimental integration, not a submission-ready patch or new performance result.

## Live upstream check

- The GitHub issue page for [#11412](https://github.com/NVIDIA/cccl/issues/11412) exposed state OPEN, updatedAt `2026-09-16T13:46:58Z`, with 12 comments. No newer update was visible versus the previous investigation.
- `git ls-remote` reported main `2fcc3f06c0df16f274fbe83cd140393a56cbb09b`.
- Fetched [lower_bound.h at that exact commit](https://github.com/NVIDIA/cccl/blob/2fcc3f06c0df16f274fbe83cd140393a56cbb09b/libcudacxx/include/cuda/std/__algorithm/lower_bound.h). Its Git blob SHA1 is `d96b05e6f67fc93b0b294e11f731c6d04556af16`, identical to the local pinned file.
- GitHub PR searches for `binary_search` (10 latest results) and `lower_bound` (5 latest results) did not show a directly overlapping implementation. The former included older CUB/c.parallel PR #8642, not this libcu++ helper.
- Limitation: the web reader failed to fetch the page, and unauthenticated REST issue/comment endpoints hit a rate limit. The normal issue HTML and search endpoints were available. This was a bounded check, not exhaustive PR/commit discovery, and it does not prove nobody is working on the issue. Page metadata and raw-source hashing were inspected through read-only commands; no full page archive was saved. Refresh again before any external submission.

## Integration

Overlay path: `evidence/phase2/bounded_overlay/cuda/std/__algorithm/lower_bound.h`.

Extracted the existing loop into a local counted helper without changing its comparison or iterator-advance steps. Internal `__lower_bound` computes distance once and selects int32 only for classic random-access traversal with signed integral difference type wider than 31 value bits and a nonnegative length at most INT32_MAX. Other cases retain the original length type. Public signatures, projection invocation and comparator reference flow are preserved. The helper name currently has a `_local` suffix; this is diagnostic code, not final upstream style.

The overlay is inserted before pinned libcu++ include paths. A compiler dependency listing confirms the actual overlay path is loaded. The shared helper is used by lower_bound, binary_search and equal_range, hence all three APIs are covered. The overlay also applies on host; host performance has not been measured and deployment policy is still undecided.

## Official test results

From pinned CCCL `f747ef146b77ed1e8f38fe8cb3c67effaf7793f2`, directory `libcudacxx/test/libcudacxx/std/algorithms/alg.sorting/alg.binary.search/`:

| Source | Baseline | Overlay |
|---|---|---|
| binary.search/binary_search.pass.cpp | PASS | PASS |
| binary.search/binary_search_comp.pass.cpp | PASS | PASS |
| lower.bound/lower_bound.pass.cpp | PASS | PASS |
| lower.bound/lower_bound_comp.pass.cpp | PASS | PASS |
| equal.range/equal_range.pass.cpp | PASS | PASS |
| equal.range/equal_range_comp.pass.cpp | PASS | PASS |

Each source is included unchanged into `bounded_official_test.cu`, with its main renamed and called on host. A one-thread kernel calls the test entry on device. The equal_range comparator source's extra pointer test is also called on device. Its existing static_assert checks compile as part of inclusion. Tests include pointer/forward/bidirectional/random-access and host/device-only iterator cases according to the source's compilation conditions. Build: NVCC `-O2 -std=c++17 -arch=sm_89`, assertions enabled. This is direct execution of selected official test sources, not the full upstream lit/CI suite or a multi-compiler matrix.

The extended local harness was then compiled against the overlay and reported:

```text
HOST cases=23798 failures=0 narrow=12802 fallback=10974
DEVICE cases=23798 failures=0 narrow=12802 fallback=10974
PASS constexpr host device; performance_tested=false
```

This covers the prior heterogeneous comparator/projection, partitioned input and synthetic >INT32_MAX cases through the replaced public APIs as well as the local diagnostic helper. Dispatch counters belong to the local helper, not instrumentation inside the overlay. The overlay result agrees with the previously baseline-checked helper; this is not an independent proof of every possible generic iterator contract.

## Runner correction and raw evidence

The first run completed all six baseline tests, then its dependency-path assertion failed because NVCC escaped the workspace's space as `\ `. The dependency output actually contained the overlay path. Fixed only normalization of escaped spaces, then ran overlay tests without repeating the successful baseline set.

- `evidence/raw/phase2/2026-09-19-bounded-overlay/`: baseline successes and original dependency-check assertion failure.
- `evidence/raw/phase2/2026-09-19-bounded-overlay-r2/`: successful dependency verification and all six overlay tests.
- `evidence/raw/phase2/2026-09-19-bounded-overlay-extended/`: successful extended build/run.

`check_bounded_overlay.py` defaults to baseline plus overlay; `--overlay-only` skips baseline and `--extended-only` runs the local extended harness. Each invocation requires a new output directory, records commands/source hashes, bounds compilation/execution, and checks that upstream remains clean. Runner versions differ between logs because the escaped-path fix and extended mode were added during this stage; the overlay header itself did not change after creation.

## Remaining work and proposed next stage

Compute Sanitizer remains unavailable for the previously documented WDDM reason. No actual-overlay timing, host performance, alternate compiler/GPU validation, or full regression suite was run. The prior performance evidence concerns the local prototype, so do not silently attribute those timings to this integrated header.

Next ten-minute stage after confirmation: run a bounded baseline-versus-overlay timing check through the actual public API on the previously strong and weak cells, and produce a minimal reviewable semantic diff. Confirm the integration retains the gain and does not introduce new material regressions before discussing upstream submission. Continue to preserve the original checkout and do not post publicly without separate authorization.
