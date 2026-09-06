#pragma once
#include <cuda_runtime_api.h>
#include <cstddef>
using reduce_fn = cudaError_t (*)(void*, std::size_t&, int*, int*, int, cudaStream_t);
extern "C" cudaError_t reduce_baseline(void*, std::size_t&, int*, int*, int, cudaStream_t);
extern "C" cudaError_t reduce_vector(void*, std::size_t&, int*, int*, int, cudaStream_t);
