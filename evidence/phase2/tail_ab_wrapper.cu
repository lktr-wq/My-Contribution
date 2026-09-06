// Compiled twice with distinct supported CUB/Thrust wrapper namespaces.
#include <cub/device/device_reduce.cuh>
#include <cuda/std/functional>
#include "tail_ab_api.h"
extern "C" cudaError_t REDUCE_ENTRY(void* temp, std::size_t& bytes, int* in, int* out,
                                   int n, cudaStream_t stream)
{
  return CUB_NS_QUALIFIER::DeviceReduce::Reduce(temp, bytes, in, out, n,
                                               cuda::std::plus<>{}, int{0}, stream);
}
