# Bounded search: initial compilation and device-code cost comparison

## Result

The device-only bounded-width implementation has a measurable code-generation cost in this focused test: kernel text grows from 1,408 to 2,432 bytes (+72.73%), and register allocation grows from 25 to 28 registers per thread. Both builds have zero stack frame and zero spill loads/stores. Repeated compilation did not show a clear time penalty in this small translation unit. This is not evidence that the change is cost-free, nor a prediction for larger applications.

This follows the [runtime and correctness experiment](2026-09-19-device-only-validation.md) and the compile-time/code-size concerns in [CCCL issue #11412](https://github.com/NVIDIA/cccl/issues/11412).

## Method

The [probe](search_compile_cost.cu) contains one externally visible kernel calling public `cuda::std::binary_search` on `const int*`, with the range length supplied as a signed 64-bit kernel argument. There is no host launcher, early-exit alternative, or diagnostic search implementation. Runtime length prevents specialization to a known small array. No GPU execution or additional runtime-performance claim is part of this test.

Both builds use CCCL `f747ef146b77ed1e8f38fe8cb3c67effaf7793f2`, CUDA 13.3.73, `-O3 -std=c++17 -arch=sm_89 --ptxas-options=-v`, under WSL2. The overlay build adds the experimental header directory first. Dependency output verifies the selected header. The upstream checkout was clean before testing.

The [runner](measure_search_compile_cost.py) stages the source and overlay on the Linux filesystem, where the upstream checkout also resides. For each compilation mode, one warmup pair precedes six measured pairs, alternating baseline/overlay order. Each invocation overwrites its output and performs a fresh compiler invocation; filesystem caches are not flushed. Timings cover the complete compiler command, not just the modified template. Object compilation includes host/device compilation but no executable link; cubin compilation generates a standalone device binary.

An initial attempt mixed a Windows-mounted overlay with a Linux upstream checkout. It showed much longer overlay compilation and was stopped because filesystem placement confounded the comparison. Those timings are not included below. The retained run uses the consistent filesystem setup described above.

## Measurements

| Measurement | Baseline | Overlay | Change |
|---|---:|---:|---:|
| Object compilation, median of six | 2.9988 s | 2.9911 s | -0.26% |
| Cubin compilation, median of six | 1.2120 s | 1.1820 s | -2.48% |
| Kernel `.text.search_cost` section | 1,408 bytes | 2,432 bytes | +72.73% |
| Complete cubin file | 7,968 bytes | 9,184 bytes | +15.26% |
| Complete object file | 27,368 bytes | 28,744 bytes | +5.03% |
| Registers per thread | 25 | 28 | +3 |
| Stack frame / spill stores / spill loads | 0 / 0 / 0 bytes | 0 / 0 / 0 bytes | unchanged |

Kernel text sizes come from `readelf -SW` on the cubin, not from the entire object file. They include section padding/alignment and are not counts of executed instructions. Resource usage and spill reports come from cuobjdump and ptxas. The full cubin/object sizes include metadata and other sections and must not be described as kernel instruction size.

The small negative compilation-time changes are not evidence of an improvement: the experiment has only six pairs, runs under an uncontrolled shared host, and has overlapping timings. It shows no clear slowdown for this one instantiation, not that duplication has no compilation cost. Extra registers may affect occupancy in other kernels; this probe does not measure that effect. Its absolute register counts differ from the earlier benchmark, whose kernel source is different.

## Evidence and reproduction

[Raw logs and summary](../raw/phase2/2026-09-19-search-compile-cost/) include every retained compile command/time, dependency output, compiler versions, device SASS, ELF section listings, resource reports, and source hashes. The temporary build binaries are not committed.

With the pinned clean CCCL checkout and CUDA installed, run from Linux/WSL using a new output directory on the Linux filesystem:

```sh
python3 evidence/phase2/measure_search_compile_cost.py /tmp/search-cost-new \
  --cccl /path/to/cccl --cuda /usr/local/cuda
```

The script targets `sm_89`; edit that setting for another target. It does not execute the kernel. The prior correctness and GPU timing tests remain separate evidence.

## Interpretation

The previous runtime benefit has a real device-code tradeoff. This screen does not establish whether that tradeoff is acceptable for CCCL. A broader compilation-cost study would need multiple iterator/comparator/value-type instantiations and representative translation units. These results should be shared as a limited measurement, not as a refutation of the maintainer's concerns or a universal cost estimate.
