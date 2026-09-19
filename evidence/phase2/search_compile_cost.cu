// Focused code-generation probe: one public API instantiation, runtime length.
#include <cuda/std/algorithm>
#include <cuda/std/cstdint>

extern "C" __global__ void search_cost(
  const int* values, cuda::std::int64_t length,
  const int* queries, int count, int* output)
{
  const int i = blockIdx.x * blockDim.x + threadIdx.x;
  if (i < count)
    output[i] = cuda::std::binary_search(values, values + length, queries[i]);
}
