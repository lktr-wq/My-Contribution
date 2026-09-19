# Device-only bounded search validation — 2026-09-19

## Outcome

Restricted bounded-32 dispatch to GPU execution with `NV_IF_TARGET(NV_IS_DEVICE, (...))`. CPU retains original-width iteration through the extracted counted helper. The previously observed CPU singleton regression disappears, and the tested GPU benefit remains. This does not make the optimization universally cost-free: GPU code/register costs and flat/slightly slower workloads remain.

Only the local header overlay was modified; pinned upstream checkout remains clean at `f747ef146b77ed1e8f38fe8cb3c67effaf7793f2`. No external publication or system-setting changes occurred.

## CPU: stronger evidence than timing alone

Repeated the GCC 13.3.0 `-O3 -std=c++17 -fno-lto` CPU screen, pinned to a guest CPU, five alternating rounds, six lengths and two shapes. All per-query oracle and timed-total checks passed.

The baseline and device-only-overlay **complete CPU executables are byte-identical**, both SHA256:

`e1b648c1caf9f120323855a2d4829c2d1d2c69354cba145bbafb271e44fd841e`

N=1 all-hit median cost is 1.107727 ns/query baseline versus 1.107422 overlay (about -0.03% slowdown); the old roughly +21% regression is gone. N=1 mixed is 3.871719 versus 3.808716 ns/query, with direction-changing paired variation. Other cell aggregate differences range roughly -1.21% to +0.49%. Since executables are identical, those timings do not demonstrate an algorithmic CPU improvement or regression. Guest affinity is not dedicated physical-core/frequency control. Binary identity applies to this benchmark/compiler/configuration, not every host compiler or application.

CPU runner now records the overlay source hash in its manifest. Evidence: `evidence/raw/phase2/2026-09-19-device-only-cpu/`.

## Correctness integration

Recompiled/reran six official source files against the device-only overlay: binary_search, lower_bound and equal_range, each default and comparator overload. All passed host execution, device execution and existing constexpr assertions through the previous wrapper. This stage reran the overlay side; baseline results are from the preceding stage.

Extended harness also passed:

```text
HOST cases=23798 failures=0 narrow=12802 fallback=10974
DEVICE cases=23798 failures=0 narrow=12802 fallback=10974
PASS constexpr host device; performance_tested=false
```

The printed dispatch counters belong to the independent diagnostic helper, not instrumentation of the device-only public header. Public API results are compared against that previously baseline-validated helper. Coverage includes comparator/projection behavior, partitioned input, wrapper iterators and synthetic lengths above INT32_MAX. No full CI, NVRTC/tile/other-compiler matrix or successful Compute Sanitizer run is claimed.

Evidence: `2026-09-19-device-only-regression/` and `2026-09-19-device-only-extended/` under `evidence/raw/phase2/`.

## Actual API GPU performance

Reused the public-API-only baseline/overlay two-executable benchmark: one query per thread, 4,194,304 queries/launch, shuffled hits or half hits/odd misses, 50 warmups, 30 averages of 50 launches per cell, three alternating process-order rounds. Outputs/guards passed in both builds before and after timing. No samples were filtered.

Median of three round medians, elapsed-time reduction versus baseline:

| Length | Hits | Mixed |
|---:|---:|---:|
| 32 | 22.76% | 22.72% |
| 4,096 | -0.18% | -0.10% |
| 20,000 | 24.02% | 24.38% |
| 65,536 | -0.24% | -0.02% |

N=20,000: baseline/overlay 0.389591/0.296018 ms for hits and 0.389621/0.294647 ms for mixed queries. All paired rounds retain more than 23.8% reduction for hits and 24.1% for mixed. Negative values at other sizes are retained as small measured slowdowns, not proof of a significant generic regression or grounds to claim zero cost.

All 48 timed windows contain GPU telemetry; readings range 2550–2580 MHz (1.18%). Approximate 200-ms polling still cannot exclude every transient. Turbo was active at stage start; initial GPU utilization was 10%. No power or proxy configuration changed.

The measured public-API GPU kernel's normalized SASS instruction sequence is identical to the previous shared-overlay kernel (comments/encodings stripped; registers/predicates/branch targets retained). SHA256: `d60c5a804f4e2a1ce623044f6b9ca5a4a6b6301b07798522456f1807c9aa6133`. This supports the intended separation: host code restored, tested GPU instruction sequence retained. It does not compare every binary scheduling bit or establish other architectures' behavior.

Evidence: `evidence/raw/phase2/2026-09-19-device-only-gpu/`, including samples, summaries, clock windows, SASS, manifests and `device-only-codegen.json`. `verify_device_only_codegen.py` records executable/instruction identity checks.

## Patch and next step

Regenerated `minimal.patch` and its formatting-preserving candidate header in the GPU evidence directory. Text normalization matches the measured overlay; nonmutating `git apply --check` passes. The patch remains local and includes the diagnostic helper name, not final upstream formatting. Existing unrelated user edits were preserved.

Known boundaries: GPU specificity, one GPU/compiler, limited pointer/int workloads, reused data between launches, no physical huge-array performance test, and unavailable WDDM sanitizer. CPU compilation overhead and untested targets are not covered by executable identity.

Suggested next ten-minute stage, after confirmation: prepare a local English issue-comment draft with the device-only patch, concise reproduction instructions, strong and weak results, and validation limits. Ask for maintainer feedback on whether this device-only lower_bound optimization fits the library. No comment or PR should be published without explicit approval.
