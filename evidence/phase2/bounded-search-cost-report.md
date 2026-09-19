# Device-only bounded search: runtime benefit and compilation costs

Updated 2026-09-20. Follow-up to the bounded 32-bit dispatch discussed in [NVIDIA/cccl#11412](https://github.com/NVIDIA/cccl/issues/11412).

## Conclusion

The experimental device-only dispatch has a measurable tradeoff. Earlier RTX 4060 Laptop measurements showed about 24% lower elapsed time for the tested 20,000-element searches, with some other lengths essentially unchanged. Focused compilation tests now show larger GPU kernel text and increased register allocation. They do not show a large object-compilation slowdown in these small translation units.

These findings do not establish that automatic dispatch should be enabled by default. They supplement the existing discussion with measurements of one implementation, compiler and target.

## Implementation

The [overlay](bounded_overlay/cuda/std/__algorithm/lower_bound.h) uses a signed 32-bit loop counter for eligible device-side random-access ranges whose lengths fit in `INT32_MAX`, retaining the original-width path otherwise. CPU execution retains the original-width path. Pointer addresses are not narrowed, and the search/comparator sequence is unchanged: no early-exit-on-match optimization is added.

Baseline: CCCL `f747ef146b77ed1e8f38fe8cb3c67effaf7793f2`. Cost measurements use CUDA 13.3.73 under WSL2, targeting `sm_89`, with `-O3 -std=c++17 --ptxas-options=-v`.

## Runtime evidence, measured separately

The [runtime and correctness report](2026-09-19-device-only-validation.md) compares the public API with and without the overlay on the same GPU. At length 20,000, elapsed time decreased by 24.02% for shuffled hits and 24.38% for mixed hits/misses; lengths 4,096 and 65,536 were essentially unchanged. The tested CPU executables were byte-identical after restricting dispatch to the device. That CPU result does not establish unchanged compilation costs across applications.

The following cost probes are separate programs. They were compiled, not executed; the previous runtime results must not be generalized to their additional types and comparators.

## Compilation and generated-code results

| Measurement | One int-pointer search | Twelve type/comparator combinations |
|---|---:|---:|
| Object compile median, baseline → overlay | 2.9988 → 2.9911 s (-0.26%) | 3.8270 → 3.8178 s (-0.24%) |
| Cubin compile median, baseline → overlay | 1.2120 → 1.1820 s (-2.48%) | 1.4574 → 1.5311 s (+5.05%) |
| Summed kernel text, baseline → overlay | 1,408 → 2,432 bytes (+72.73%) | 17,408 → 28,928 bytes (+66.18%) |
| Complete cubin, baseline → overlay | 7,968 → 9,184 bytes (+15.26%) | 39,520 → 53,088 bytes (+34.33%) |
| Registers per thread | 25 → 28 | +3 to +5, depending on type |
| Stack frame / spill loads / spill stores | Zero in both builds | Zero for all kernels in both builds |

The twelve combinations cover six types (`int`, `unsigned int`, `long long`, `unsigned long long`, `float`, `double`), each with `less<T>` and `greater<T>`. All use raw pointers and a runtime signed 64-bit length. The source contains no alternative search implementations.

Each compilation mode has one warmup pair and six measured pairs with alternating build order. Source, overlay headers and output were staged on the Linux filesystem, as was the upstream checkout. Header dependency output verifies which implementation was compiled. All retained rounds are included.

Kernel text is measured from cubin ELF sections, including padding/alignment; complete file sizes include metadata and other sections. Register and spill figures come from cuobjdump/ptxas. Object compilation and standalone cubin compilation are separate commands, not additive phases whose times can be subtracted to isolate host overhead.

## Interpretation and limitations

- Code growth is consistent across the probes: an additional 1,024 bytes for the single kernel and 11,520 bytes across twelve kernels. This is not a scaling law, since the type mix also changes.
- Object compilation is essentially unchanged in these runs. Small negative timing differences are not evidence of a compilation speedup.
- The twelve-kernel cubin median is about 74 ms higher; five of six paired rounds are slower. This is limited evidence of a device compilation cost, not a significance claim or a large-project estimate.
- Extra registers are a resource cost, but their effect on occupancy or execution time was not measured by these probes. Zero spills does not imply zero cost.
- Coverage excludes large translation units, complex comparators, diverse iterator wrappers, multiple architectures and link-time optimization. Six timing pairs in a shared host environment cannot characterize all build workloads.

The measurements therefore support discussing the runtime/code-size tradeoff or an opt-in approach, rather than describing this as a universally cost-free optimization.

## Reproduction and detailed evidence

Both detailed reports include commands, methodology and links to unfiltered logs and source hashes:

- [Single-instantiation report](2026-09-19-search-compile-cost.md), [source](search_compile_cost.cu), [raw evidence](../raw/phase2/2026-09-19-search-compile-cost/).
- [Twelve-instantiation report](2026-09-20-search-compile-cost-multi.md), [source](search_compile_cost_multi.cu), [raw evidence](../raw/phase2/2026-09-20-search-compile-cost-multi/).
- [Shared compilation runner](measure_search_compile_cost.py). Supply a clean pinned CCCL checkout and a new Linux-filesystem output directory. CUDA location is configurable; the target is currently fixed to `sm_89`.

No additional runtime tests or implementation changes were made for this consolidation.
