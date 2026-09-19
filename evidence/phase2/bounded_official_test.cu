#define main upstream_main
#include TEST_SOURCE
#undef main
#include <cuda_runtime.h>
#include <cstdio>
__global__ void device_tests() {
  test();
#ifdef EXTRA_POINTER_TEST
  test<const int*>();
#endif
}
int main(int argc,char** argv) {
  if(upstream_main(argc,argv)!=0)return 2;
  device_tests<<<1,1>>>();
  auto launch=cudaGetLastError();auto result=cudaDeviceSynchronize();
  if(launch!=cudaSuccess || result!=cudaSuccess){std::fprintf(stderr,"CUDA %s / %s\n",cudaGetErrorString(launch),cudaGetErrorString(result));return 3;}
  std::puts("PASS official host/device/constexpr source");return 0;
}
