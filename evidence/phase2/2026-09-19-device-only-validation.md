# Device-only bounded 32-bit search: implementation and results

## Outcome

This experiment follows the bounded 32-bit dispatch approach already discussed in [NVIDIA/cccl#11412](https://github.com/NVIDIA/cccl/issues/11412). It adds implementation and validation evidence, rather than introducing the observation that 32-bit indexing can improve GPU search performance. The compile-time and code-size concerns raised in that discussion remain open.

On an RTX 4060 Laptop GPU, the modified public `cuda::std::binary_search` reduced elapsed time by about 24% for the tested 20,000-element workloads. Other tested sizes were essentially unchanged or improved by about 23%, as shown below. These are comparisons on the same GPU, not direct comparisons with the issue author's measurements.

Restricted bounded-32 dispatch to GPU execution with `NV_IF_TARGET(NV_IS_DEVICE, (...))`. CPU retains original-width iteration through the extracted counted helper. The previously observed CPU singleton regression disappears, and the tested GPU benefit remains. This does not make the optimization universally cost-free: GPU code/register costs and flat/slightly slower workloads remain.

The baseline is CCCL commit `f747ef146b77ed1e8f38fe8cb3c67effaf7793f2`. The experimental header is supplied through an include-path overlay; the upstream checkout is unchanged. Results were collected on 2026-09-19.

## What changed

The [experimental header](bounded_overlay/cuda/std/__algorithm/lower_bound.h) uses a signed 32-bit loop counter on the device when the classic algorithm policy uses a random-access iterator with a wider signed integral distance type and the range length fits in `INT32_MAX`. Other cases retain the original-width path. Pointer addresses are not narrowed.

The search steps and comparator order are unchanged. This does **not** add early exit on a match: `binary_search` still uses `lower_bound`. The shared helper also affects device calls from `lower_bound` and `equal_range`.

## CPU: stronger evidence than timing alone

Repeated the GCC 13.3.0 `-O3 -std=c++17 -fno-lto` CPU screen, pinned to a guest CPU, five alternating rounds, six lengths and two shapes. All per-query oracle and timed-total checks passed.

The baseline and device-only-overlay **complete CPU executables are byte-identical**, both SHA256:

`e1b648c1caf9f120323855a2d4829c2d1d2c69354cba145bbafb271e44fd841e`

N=1 all-hit median cost is 1.107727 ns/query baseline versus 1.107422 overlay (about -0.03% slowdown); the old roughly +21% regression is gone. N=1 mixed is 3.871719 versus 3.808716 ns/query, with direction-changing paired variation. Other cell aggregate differences range roughly -1.21% to +0.49%. Since executables are identical, those timings do not demonstrate an algorithmic CPU improvement or regression. Guest affinity is not dedicated physical-core/frequency control. Binary identity applies to this benchmark/compiler/configuration, not every host compiler or application.

The CPU manifest records the overlay source hash. [CPU results and commands](../raw/phase2/2026-09-19-device-only-cpu/).

## Correctness integration

Six upstream test source files were compiled and run against the device-only overlay: binary_search, lower_bound and equal_range, each default and comparator overload. All passed host execution, device execution and existing constexpr assertions through the [test wrapper](bounded_official_test.cu). The device-only run retested the overlay; baseline results were collected in the earlier comparison.

Extended harness also passed:

```text
HOST cases=23798 failures=0 narrow=12802 fallback=10974
DEVICE cases=23798 failures=0 narrow=12802 fallback=10974
PASS constexpr host device; performance_tested=false
```

The printed dispatch counters belong to the independent diagnostic helper, not instrumentation of the device-only public header. Public API results are compared against that previously baseline-validated helper. Coverage includes comparator/projection behavior, partitioned input, wrapper iterators and synthetic lengths above INT32_MAX. No full CI, NVRTC/tile/other-compiler matrix or successful Compute Sanitizer run is claimed.

[Upstream-test results](../raw/phase2/2026-09-19-device-only-regression/) and [extended-check results](../raw/phase2/2026-09-19-device-only-extended/).

## Actual API GPU performance

The baseline and overlay are built from the same source with CUDA 13.3, `-O3 -std=c++17 -arch=sm_89 -DPUBLIC_API_ONLY`, in WSL2. Only the overlay build adds the experimental include directory before CCCL's headers. Both timed kernels call the public `cuda::std::binary_search` API.

The benchmark uses one query per thread, 4,194,304 queries/launch, shuffled hits or half hits/odd misses, 50 warmups, 30 averages of 50 launches per cell, and three alternating process-order rounds. The input array contains distinct ascending even integers. Outputs/guards passed in both builds before and after timing. One preliminary measurement run per build was excluded as preheating; no samples from the three reported rounds were filtered.

Median of three round medians, elapsed-time reduction versus baseline:

| Length | Hits | Mixed |
|---:|---:|---:|
| 32 | 22.76% | 22.72% |
| 4,096 | -0.18% | -0.10% |
| 20,000 | 24.02% | 24.38% |
| 65,536 | -0.24% | -0.02% |

N=20,000: baseline/overlay 0.389591/0.296018 ms for hits and 0.389621/0.294647 ms for mixed queries. All paired rounds retain more than 23.8% reduction for hits and 24.1% for mixed. Negative values at other sizes are retained as small measured slowdowns, not proof of a significant generic regression or grounds to claim zero cost.

All 48 timed windows contain GPU telemetry; readings range 2550–2580 MHz (1.18%). Approximate 200-ms polling still cannot exclude every transient. The laptop was in Turbo mode at the start of measurement; initial GPU utilization was 10%.

The measured public-API GPU kernel's normalized SASS instruction sequence is identical to the previous shared-overlay kernel (comments/encodings stripped; registers/predicates/branch targets retained). SHA256: `d60c5a804f4e2a1ce623044f6b9ca5a4a6b6301b07798522456f1807c9aa6133`. This supports the intended separation: host code restored, tested GPU instruction sequence retained. It does not compare every binary scheduling bit or establish other architectures' behavior.

[GPU evidence](../raw/phase2/2026-09-19-device-only-gpu/) includes samples, summaries, clock windows, SASS, manifests and `device-only-codegen.json`. The [code-generation check](verify_device_only_codegen.py) records executable/instruction identity checks.

## Implementation and reproduction resources

The [minimal patch](../raw/phase2/2026-09-19-device-only-gpu/minimal.patch) preserves upstream formatting. Its comment/whitespace-normalized text matches the measured overlay, and `git apply --check` passed against the pinned checkout. It is an experimental patch, not a submission-ready change; the helper still has a local diagnostic name.

The [benchmark source](binary_search_bounded_single.cu), its [kernel definitions](binary_search_bounded_bench.cu), and the [runner](measure_public_overlay.py) are included. The [GPU manifest](../raw/phase2/2026-09-19-device-only-gpu/manifest.json) records exact build/run commands and source hashes; [summary.json](../raw/phase2/2026-09-19-device-only-gpu/summary.json) contains all eight result cells.

The runner currently assumes a Linux/WSL checkout at `/home/lktr/src/cccl`, CUDA tools under `/usr/local/cuda/bin`, and WSL's `nvidia-smi` at `/usr/lib/wsl/lib/nvidia-smi`. These paths and `sm_89` must be adapted for another environment. It requires the pinned, clean CCCL checkout and a new output-directory argument. These are experiment scripts, not yet a portable reproduction package.

## Limitations and next measurements

Known boundaries: GPU specificity, one GPU/compiler, limited pointer/int workloads, reused data between launches, no physical huge-array performance test, and unavailable WDDM sanitizer. CPU compilation overhead and untested targets are not covered by executable identity.

The next measurements will address compilation time and generated device-code size, rather than assume the observed runtime improvement is free. The existing benchmark source also includes earlier experimental variants, so whole-executable size alone would not isolate this change's cost. A focused comparison is needed before drawing conclusions about those tradeoffs.
