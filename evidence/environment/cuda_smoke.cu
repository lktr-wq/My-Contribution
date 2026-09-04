#include <cuda_runtime.h>

#include <cstdio>

__global__ void write_answer(int* output)
{
  *output = 42;
}

int main()
{
  int* device_output = nullptr;
  int host_output    = 0;

  if (cudaMalloc(&device_output, sizeof(int)) != cudaSuccess)
  {
    std::fprintf(stderr, "cudaMalloc failed\n");
    return 1;
  }

  write_answer<<<1, 1>>>(device_output);
  if (cudaGetLastError() != cudaSuccess || cudaDeviceSynchronize() != cudaSuccess)
  {
    std::fprintf(stderr, "kernel execution failed\n");
    cudaFree(device_output);
    return 2;
  }

  if (cudaMemcpy(&host_output, device_output, sizeof(int), cudaMemcpyDeviceToHost) != cudaSuccess)
  {
    std::fprintf(stderr, "cudaMemcpy failed\n");
    cudaFree(device_output);
    return 3;
  }

  cudaFree(device_output);
  std::printf("CUDA_SMOKE_RESULT=%d\n", host_output);
  return host_output == 42 ? 0 : 4;
}
