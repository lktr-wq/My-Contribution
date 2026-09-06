// Same-process paired baseline/variant experiment, not an upstream benchmark.
#define NVBENCH_MAIN_INITIALIZE_CUSTOM_PRE(argc, argv) \
  if (argc == 2 && std::string(argv[1]) == "--check-only") return correctness()
#define NVBENCH_MAIN_INITIALIZE_CUSTOM_POST(argc, argv) cleanup_guard guard
#include <nvbench/nvbench.cuh>
#include <nvbench/cuda_call.cuh>
#include "tail_ab_api.h"
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>

namespace {
constexpr int center = 720 * 4096;
constexpr std::array<int, 7> sizes{center-4096, center-2048, center-32, center-4, center-1, center, center+1};
constexpr std::array<reduce_fn, 2> functions{reduce_baseline, reduce_vector};
struct memory {
  void* ptr = nullptr;
  explicit memory(std::size_t n) { NVBENCH_CUDA_CALL(cudaMalloc(&ptr, std::max(n, std::size_t{1}))); }
  ~memory() { if (ptr) (void) cudaFree(ptr); }
  memory(const memory&) = delete;
  memory& operator=(const memory&) = delete;
};
struct fixture {
  nvbench::cuda_stream stream;
  memory input, output{sizeof(int)};
  std::unique_ptr<memory> scratch;
  std::size_t scratch_bytes = 0;
  int offset;
  std::vector<std::int64_t> prefix;
  fixture(int capacity, int misalign, int pattern)
      : input(std::size_t(capacity + misalign) * sizeof(int)), offset(misalign), prefix(capacity+1, 0) {
    std::vector<int> host(capacity + misalign, 0);
    for (int i=0; i<capacity; ++i) {
      const int value = pattern == 0 ? 1+i%17 : pattern == 1 ? (i%31)-15
                        : pattern == 2 ? 0 : ((i%257 == 0) ? 23 : -1);
      host[i+misalign] = value;
      prefix[i+1] = prefix[i] + value;
    }
    if (!host.empty()) NVBENCH_CUDA_CALL(cudaMemcpy(input.ptr, host.data(), host.size()*sizeof(int), cudaMemcpyHostToDevice));
    for (auto fn : functions) {
      std::size_t needed = 0;
      NVBENCH_CUDA_CALL(fn(nullptr, needed, in(), out(), capacity, stream.get_stream()));
      scratch_bytes = std::max(scratch_bytes, needed);
    }
    scratch = std::make_unique<memory>(scratch_bytes);
  }
  int* in() { return static_cast<int*>(input.ptr)+offset; }
  int* out() { return static_cast<int*>(output.ptr); }
  void reduce(int variant, int n) {
    auto available = scratch_bytes;
    NVBENCH_CUDA_CALL(functions.at(variant)(scratch->ptr, available, in(), out(), n, stream.get_stream()));
  }
  int verify(int n) {
    int actual = 0;
    NVBENCH_CUDA_CALL(cudaMemcpyAsync(&actual, out(), sizeof(int), cudaMemcpyDeviceToHost, stream.get_stream()));
    NVBENCH_CUDA_CALL(cudaStreamSynchronize(stream.get_stream()));
    if (actual != prefix.at(n)) throw std::runtime_error("GPU result differs from I64 CPU prefix");
    return actual;
  }
  int check(int variant, int n) {
    NVBENCH_CUDA_CALL(cudaMemsetAsync(out(), 0xa5, sizeof(int), stream.get_stream()));
    reduce(variant, n);
    return verify(n);
  }
};

int correctness() {
  const std::vector<int> lengths{0,1,3,4,255,256,257,1023,1024,1025,2047,4092,4093,4094,
    4095,4096,4097,8191,8192,8193,center-4096,center-2048,center-32,center-4,center-3,center-1,center,center+1};
  int count = 0;
  for (int n : lengths) for (int offset=0; offset<4; ++offset) for (int pattern=0; pattern<4; ++pattern) {
    // The valid end equals the allocation end: sanitizer can detect vector overreads.
    fixture data(n, offset, pattern);
    for (int variant=0; variant<2; ++variant) {
      const int actual = data.check(variant, n);
      std::printf("ORACLE N=%d offset=%d pattern=%d variant=%d result=%d\n", n, offset, pattern, variant, actual);
      ++count;
    }
  }
  std::printf("CORRECTNESS_PASS cases=%d\n", count);
  return 0;
}

std::unique_ptr<fixture> owner;
struct cleanup_guard { ~cleanup_guard() { owner.reset(); } };
void benchmark(nvbench::state& state) {
  const int code = static_cast<int>(state.get_int64("Case"));
  if (code < 0 || code >= 14) throw std::runtime_error("Invalid case");
  const int variant = code%2;
  const int n = sizes.at(code/2);
  if (!owner) {
    owner = std::make_unique<fixture>(center+1, 0, 0);
    for (int len : sizes) for (int v=0; v<2; ++v) owner->check(v, len);
    // Equal untimed startup work for both versions, before any NVBench state.
    for (int i=0; i<200; ++i) for (int v=0; v<2; ++v) owner->reduce(v, center);
    NVBENCH_CUDA_CALL(cudaStreamSynchronize(owner->stream.get_stream()));
  }
  auto& data = *owner;
  state.set_cuda_stream(nvbench::make_cuda_stream_view(data.stream.get_stream()));
  const int before = data.check(variant, n);
  state.add_element_count(n);
  state.add_global_memory_reads<int>(n);
  state.add_global_memory_writes<int>(1);
  state.exec(nvbench::exec_tag::gpu | nvbench::exec_tag::no_batch,
             [&](nvbench::launch&) { data.reduce(variant, n); });
  const int after = data.verify(n);
  std::printf("CHECK Case=%d N=%d variant=%d before=%d after=%d input=%p output=%p scratch=%p stream=%p\n",
    code,n,variant,before,after,data.in(),data.out(),data.scratch->ptr,static_cast<void*>(data.stream.get_stream()));
}
} // namespace
NVBENCH_BENCH(benchmark).set_name("tail_ab").add_int64_axis("Case", {0,1,2,3,4,5,6,7,8,9,10,11,12,13});
NVBENCH_MAIN
