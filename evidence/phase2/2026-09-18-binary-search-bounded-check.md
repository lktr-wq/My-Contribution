# Bounded-length prototype correctness — 2026-09-18

## Outcome

Implemented an independent local prototype preserving the official moving-iterator lower_bound loop, plus a wide clone control and bounded-32 dispatch. Normal host/device checks and compile-time assertions pass. **No performance measurement was performed. Compute Sanitizer did not initialize successfully, so memory-sanitizer validation remains unavailable.** No upstream source was modified.

Files:

- `binary_search_bounded.cuh`: local namespace, original-length loop and conditional int32 length loop; distance computed once, guard before narrowing, original iterator advancement/comparison/projection/final membership check preserved.
- `binary_search_bounded_check.cu`: host/device correctness harness and synthetic iterators.
- `check_binary_search_bounded.py`: pinned-checkout/hash recording, bounded compilation/execution and attempted memcheck.

## Verified results

Both normal invocations reported:

```text
HOST cases=23798 failures=0 narrow=12802 fallback=10974
DEVICE cases=23798 failures=0 narrow=12802 fallback=10974
PASS constexpr host device; performance_tested=false
```

Each ordinary case compares lower_bound positions and binary_search bool results for the wide and guarded clones against official functions, and checks dispatch choice. The case total additionally includes heterogeneous-comparator and projection checks. Narrow/fallback counters apply to ordinary cases only; they do not sum to the full total because the 22 special checks are counted separately.

Coverage:

- Lengths 0, 1, 2, 3, 7, 8, 9, 31, 32, 33, 255, 256, 257; ascending even values, duplicate groups, all-equal input and descending input; queries span below, within and above the values.
- Pointers and random-access wrapper use the narrow path; forward/bidirectional wrappers retain the original length type.
- Partitioned-but-not-globally-sorted input for query 3.
- Synthetic random-access sequence `value(position) = 2 * position` with 64-bit position/difference and lengths 2,147,483,646; 2,147,483,647; 2,147,483,648; 4,294,967,313. Six queries per length, comparing official results and explicitly asserting narrow/fallback selection. This tests arithmetic and dispatch without enormous allocations; it is not a test of physical multi-billion-element GPU storage.
- Heterogeneous record/query comparator with no record equality operator; duplicate keys with different payloads; exact comparator call-count matching against official binary_search.
- Projection returning the record key, checked against an independent linear position oracle.
- Compile-time membership assertions plus negative-length and already-int32 eligibility predicate checks. Invalid negative-distance ranges were not passed to the search algorithms.

## Sanitizer limitation

The second run rebuilt successfully and repeated the normal checks successfully, then invoked:

```text
/usr/local/cuda/bin/compute-sanitizer --tool memcheck --error-exitcode 3 <binary>
```

Exit code 3, diagnostics:

```text
Error: Failed to initialize WDDM debugger interface. Please run EnableDebuggerInterface.bat as an administrator
Error: Device not supported. Please refer to the "Supported Devices" section of the sanitizer documentation
ERROR SUMMARY: 2 errors
```

The target printed passing functional checks, but sanitizer initialization failed; these are tool/environment errors, not successful memory checks and not evidence of a particular algorithm memory defect. No registry, driver or system debugger settings were changed. Do not rerun repeatedly or claim memcheck passed. The second manifest deliberately remains `completed: false` with the failure captured.

## Evidence and remaining boundaries

- First success logs: `evidence/raw/phase2/2026-09-18-bounded-check/`. Compile 6.089 s, normal execution 0.473 s.
- Rebuild, repeated success and failed sanitizer logs: `evidence/raw/phase2/2026-09-18-bounded-check-memcheck/`.
- Both compile with `nvcc -O3 -std=c++17 -arch=sm_89`, using pinned CCCL `f747ef146b77ed1e8f38fe8cb3c67effaf7793f2`. Source hashes and exact commands are recorded. The first run predates adding the memcheck step to the runner; header and harness are unchanged between runs.
- This is a classic-iterator diagnostic, not a generic ranges/sentinel replacement. No full upstream regression suite, host/device-only callable matrix, exhaustive nonstandard difference-type validation, or equal_range integration testing was done.
- Host execution is from the NVCC-built executable, not a separate host compiler/version matrix. Comparator tests check result and call count, not a full trace of every comparison argument.
- Synthetic large-range correctness cannot establish performance for large physical datasets.

## Next stage

After confirmation, within ten minutes: add the three-entry timing harness (official / same-structure wide clone / guarded clone), verify timed-kernel outputs, inspect generated code and run a bounded three-round warm measurement if environment checks pass. Keep the runtime guard inside measured code. First check that the wide clone resembles official performance; then attribute only the guarded-versus-wide difference to this change. Explicitly carry the unavailable memcheck limitation forward; do not modify system settings merely to enable it.
