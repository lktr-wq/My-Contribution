# #11412 bounded-length design review — 2026-09-18

## Outcome and scope

Proceed to a local, official-structure prototype, not an upstream patch. This stage inspected source and existing tests and designed the isolation experiment. No new algorithm implementation, compilation, correctness test, or performance measurement was performed.

Source checkout `/home/lktr/src/cccl` remains clean at `f747ef146b77ed1e8f38fe8cb3c67effaf7793f2`. Prior reference-loop gains are motivation, not evidence that the proposed official-loop change helps.

## Source findings

Paths below are relative to that pinned checkout:

- `libcudacxx/include/cuda/std/__algorithm/binary_search.h`: calls public `lower_bound` using `__comp_ref_type`, then evaluates `first != last && !comp(value, *first)`.
- `libcudacxx/include/cuda/std/__algorithm/lower_bound.h`: internal `__lower_bound` obtains the iterator's distance type with `_IterOps<Policy>::distance`. Its loop tracks a moving iterator and remaining length, computes `__half_positive(len)`, advances a midpoint iterator, and updates `len`. There is no early-hit return.
- `libcudacxx/include/cuda/std/__algorithm/half_positive.h`: integral arguments are converted to the corresponding unsigned type before dividing by two, then converted back. Preserve this expression rather than copying signed `/2` from the earlier reference.
- `libcudacxx/include/cuda/std/__iterator/advance.h`: classic `advance` converts its input count to the iterator's `difference_type` before `+=` for random access. A narrow length therefore does not remove wide pointer/iterator arithmetic. SASS must verify what actually changes.
- `libcudacxx/include/cuda/std/__algorithm/equal_range.h`: `__equal_range` also calls internal `__lower_bound`. Changing the shared helper has an impact beyond binary_search.
- Existing binary-search and lower-bound tests cover pointers, forward/bidirectional/random-access wrappers, host/device-only wrappers and constexpr execution. Read `binary_search_comp.pass.cpp` and `lower_bound.pass.cpp` under `libcudacxx/test/libcudacxx/std/algorithms/alg.sorting/alg.binary.search/`. These are inspected tests, not tests executed in this stage.

## Proposed local experiment

Keep the existing official benchmark and reference results intact. Add a separate local implementation outside namespace `cuda::std` and outside the upstream checkout. Preserve the official moving-iterator loop, unsigned-half calculation, midpoint advance, comparison order, comparator references, projection invocation and final binary_search test.

Compare three entries:

1. Unmodified official binary_search.
2. Local official-structure loop with the original difference type throughout (clone control).
3. The same local loop with a runtime bounded-length dispatch; only eligible lengths use signed 32-bit loop arithmetic.

The clone control is mandatory: if it differs materially from official, investigate that difference before crediting index width. Reuse the exact input, launch geometry and timing method. Do not add early exit, change comparator semantics, replace pointer advancement with index-based addressing, or remove hit accounting in this comparison.

The runtime guard must remain in the measured code. Feed runtime length rather than specializing the kernel for a compile-time 20,000-element range. Preserve a genuine wide fallback and inspect both its instantiation and generated narrow path.

## Eligibility and fallback

For the first prototype, restrict the optimization to classic random-access iterators with an integral signed difference type wider in value bits than `int32_t`. Compute distance once in its original type, then check `0 <= length <= INT32_MAX` in that wide type **before** narrowing. Other iterator categories, nonstandard difference types, already-narrow types and larger ranges keep the original loop.

This restriction is conservative scope control, not a claim that forward iterators can never benefit. Keep host and constexpr semantics testable; host-versus-device deployment of an eventual library patch remains undecided. Do not introduce device-only intrinsics or launch-state checks into the algorithm.

For valid input, loop invariant: `0 <= len <= INT32_MAX`. With `len > 0`, `half = floor(len/2)`, hence `0 <= half < len`, `half + 1 <= len`, and `0 <= len - (half + 1) < len`. Both update branches stay representable. Advance operates on the original iterator, so a 32-bit element count is not a 32-bit address or byte offset. Valid-range and representable-distance preconditions still apply; this proposal does not repair invalid iterator ranges.

An unsigned-32 path up to UINT32_MAX is intentionally deferred: it adds another design choice without being necessary to test the current hypothesis.

## Correctness acceptance before timing

- Match official lower_bound positions as well as binary_search bool results on empty/singleton arrays, even/odd lengths, powers of two and adjacent sizes, duplicates, all-equal values, hits, below/above-range misses and interior misses.
- Ascending and descending comparators; equivalent-but-not-identical records; heterogeneous element/query comparison without operator==; comparator state/reference behavior.
- Inputs partitioned for the queried value but not globally sorted: e.g. `[2, 0, 1, 3, 3, 6, 4, 5]` for query 3. Preserve the original comparison sequence and result.
- Pointer and random-access wrapper narrow-path checks; forward/bidirectional wrapper fallback checks; host, device and constexpr execution where supported. Projection behavior must be covered if prototyping the internal helper.
- Use a valid synthetic random-access counting iterator with 64-bit position/difference and on-demand values to test lengths INT32_MAX-1, INT32_MAX, INT32_MAX+1 and a larger length without allocating billions of elements. Include first/last/interior queries and absent values. Explicitly assert selected path; matching outputs alone cannot show that fallback was exercised.
- Test the dispatch predicate separately for negative values, but do not feed invalid negative-distance ranges to the search API.

## Performance gate and stop rule

Only after correctness passes: use the three existing shapes and three rotated rounds, fresh power/GPU evidence, preheat and bounded execution. First establish clone-control comparability; then measure guarded32 versus clone64. Inspect SASS for whether length arithmetic really narrows despite advance's conversion. Include tiny lengths in a later dispatch-overhead screen before claiming a generally beneficial patch.

The previous project's 20% screen is a continuation heuristic, not statistical significance. A large reference32-versus-reference64 gap does not bypass this official-structure screen. If the guarded official-structure path loses the benefit or creates meaningful regressions, stop this route rather than expanding it indefinitely.

## Next stage (confirmation required)

Within ten minutes, implement the separate three-entry prototype and execute bounded host/device correctness checks, including synthetic large-range fallback cases. If compilation or generic cases need more work, report that checkpoint; do not silently skip them to start timing. Do not modify the shared lower_bound helper or submit upstream changes. A later successful patch would need regression coverage for both lower_bound and equal_range and refreshed upstream duplicate checking.
