// Twelve public API instantiations; no timing or GPU execution in this probe.
#include <cuda/std/algorithm>
#include <cuda/std/cstdint>
#include <cuda/std/functional>

#define SEARCH_PROBE(NAME, TYPE, COMP)                                      \
extern "C" __global__ void search_cost_##NAME(                              \
  const TYPE* values, cuda::std::int64_t length,                            \
  const TYPE* queries, int count, int* output)                              \
{                                                                         \
  const int i = blockIdx.x * blockDim.x + threadIdx.x;                       \
  if (i < count)                                                          \
    output[i] = cuda::std::binary_search(                                  \
      values, values + length, queries[i], cuda::std::COMP<TYPE>{});        \
}

SEARCH_PROBE(i32_less, int, less)
SEARCH_PROBE(i32_greater, int, greater)
SEARCH_PROBE(u32_less, unsigned int, less)
SEARCH_PROBE(u32_greater, unsigned int, greater)
SEARCH_PROBE(i64_less, long long, less)
SEARCH_PROBE(i64_greater, long long, greater)
SEARCH_PROBE(u64_less, unsigned long long, less)
SEARCH_PROBE(u64_greater, unsigned long long, greater)
SEARCH_PROBE(f32_less, float, less)
SEARCH_PROBE(f32_greater, float, greater)
SEARCH_PROBE(f64_less, double, less)
SEARCH_PROBE(f64_greater, double, greater)
#undef SEARCH_PROBE
