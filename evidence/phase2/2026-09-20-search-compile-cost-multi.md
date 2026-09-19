# Bounded search cost: twelve type/comparator instantiations

## Summary

Expanding the focused compilation probe to twelve public `binary_search` instantiations preserves the code-size tradeoff: summed kernel text grows by 66.18%, and each kernel uses 3–5 additional registers. Object compilation time is essentially unchanged in this run; standalone cubin compilation has a 5.05% higher median, with five of six paired rounds slower. This is limited evidence of a device compilation cost, not a large-project estimate or a claim of statistical significance.

## Scope and method

The [source](search_compile_cost_multi.cu) contains six value types (`int`, `unsigned int`, `long long`, `unsigned long long`, `float`, `double`), each with `cuda::std::less<T>` and `cuda::std::greater<T>`. All twelve kernels take raw pointers and a runtime signed 64-bit range length. They call only the public API. They do not add early exit or alternative search implementations.

The [runner](measure_search_compile_cost.py) uses the same settings as the [single-instantiation probe](2026-09-19-search-compile-cost.md): clean CCCL `f747ef146b77ed1e8f38fe8cb3c67effaf7793f2`, CUDA 13.3.73, `-O3 -std=c++17 -arch=sm_89 --ptxas-options=-v`, WSL2, Linux-filesystem source/headers/output, one warmup pair and six alternating measured pairs per compilation mode. Header dependencies were checked. All compiler invocations succeeded. No GPU execution or new correctness/performance test was performed.

## Results

| Measurement | Baseline | Overlay | Change |
|---|---:|---:|---:|
| Object compilation median | 3.8270 s | 3.8178 s | -0.24% |
| Standalone cubin compilation median | 1.4574 s | 1.5311 s | +5.05% |
| Sum of twelve kernel text sections | 17,408 bytes | 28,928 bytes | +66.18% |
| Complete cubin | 39,520 bytes | 53,088 bytes | +34.33% |
| Complete object | 94,240 bytes | 108,416 bytes | +15.04% |

Per-kernel allocation is the same for less/greater within each type:

| Type | Text bytes, baseline → overlay | Registers/thread, baseline → overlay |
|---|---:|---:|
| int / unsigned int | 1,408 → 2,432 | 25 → 28 |
| long long / unsigned long long | 1,536 → 2,432 | 26 → 30 |
| float | 1,408 → 2,432 | 25 → 28 |
| double | 1,408 → 2,304 | 25 → 30 |

All kernels have zero stack frame and zero spill stores/loads. Text-section sizes include alignment/padding; file sizes also contain metadata and other sections. Register allocation is not a direct occupancy or runtime measurement.

## Interpretation and limits

The added kernel text totals 11,520 bytes across twelve kernels, versus 1,024 bytes for the earlier single-int probe. This is consistent with duplicated search paths adding code across instantiations; the percentage increase is not larger than in the single-instantiation case. It does not establish a scaling law, since the type/comparator mix also changed.

The object and cubin compiler commands are separate measurements: do not subtract their times to estimate host compilation cost. The 5.05% cubin median increase is a small absolute difference (about 74 ms), measured in a shared environment with only six pairs. No large translation unit, complex comparator, iterator wrapper, multi-architecture build, or link-time optimization is covered. Floating-point inputs, including NaNs, were not executed or validated here. The runtime improvements reported previously apply only to those previous workloads.

These results support treating automatic bounded dispatch as a tradeoff, not a universally free optimization. They do not determine whether CCCL should accept it. An opt-in approach or maintainer feedback can be considered before further broadening the experiment.

## Reproduction and evidence

With a pinned clean CCCL checkout, CUDA tools, and a new Linux-filesystem output directory:

```sh
python3 evidence/phase2/measure_search_compile_cost.py /tmp/search-cost-multi-new \
  --cccl /path/to/cccl --cuda /usr/local/cuda \
  --source evidence/phase2/search_compile_cost_multi.cu --expected-kernels 12
```

The target is hardcoded to `sm_89`. [Raw evidence](../raw/phase2/2026-09-20-search-compile-cost-multi/) includes all retained command timings, source hashes, dependency checks, SASS, section sizes and resource reports. Temporary binaries are not committed.
