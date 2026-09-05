// Local diagnostic harness. Uses unmodified, pinned CCCL and NVBench.
#define NVBENCH_MAIN_INITIALIZE_CUSTOM_POST(argc, argv) fixture_cleanup_guard fixture_guard
#include <cub/device/device_reduce.cuh>
#include <nvbench/nvbench.cuh>
#include <nvbench/cuda_call.cuh>
#include <cuda/std/functional>

#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <memory>
#include <stdexcept>
#include <vector>

namespace {
constexpr int center = 720 * 4096;
constexpr int capacity = center + 1;

struct device_memory {
  void* ptr = nullptr;
  explicit device_memory(std::size_t bytes) { NVBENCH_CUDA_CALL(cudaMalloc(&ptr, bytes)); }
  ~device_memory() { if (ptr) { (void) cudaFree(ptr); } }
  device_memory(const device_memory&) = delete;
  device_memory& operator=(const device_memory&) = delete;
};

struct fixture {
  nvbench::cuda_stream stream;
  device_memory input{capacity * sizeof(std::int32_t)};
  device_memory output{sizeof(std::int32_t)};
  std::size_t temporary_bytes = 0;
  std::vector<std::int64_t> prefix;
  // Allocated once after querying storage requirements.
  void* temporary = nullptr;

  fixture() : prefix(capacity + 1, 0) {
    int device = -1;
    NVBENCH_CUDA_CALL(cudaGetDevice(&device));
    if (device != 0) { throw std::runtime_error("This harness supports GPU 0 only"); }
    std::vector<std::int32_t> host(capacity);
    for (int i = 0; i < capacity; ++i) {
      host[i] = 1 + i % 17;
      prefix[i+1] = prefix[i] + host[i];
    }
    // All terms are positive and total < 51 million; every partial sum fits I32.
    NVBENCH_CUDA_CALL(cudaMemcpy(input.ptr, host.data(), host.size()*sizeof(host[0]), cudaMemcpyHostToDevice));
    NVBENCH_CUDA_CALL(cub::DeviceReduce::Reduce(nullptr, temporary_bytes, in(), out(), capacity,
                                               cuda::std::plus<>{}, std::int32_t{0}, stream.get_stream()));
    NVBENCH_CUDA_CALL(cudaMalloc(&temporary, temporary_bytes));
  }
  ~fixture() { if (temporary) { (void) cudaFree(temporary); } }
  fixture(const fixture&) = delete;
  fixture& operator=(const fixture&) = delete;
  std::int32_t* in() { return static_cast<std::int32_t*>(input.ptr); }
  std::int32_t* out() { return static_cast<std::int32_t*>(output.ptr); }

  void reduce(int n) {
    auto available = temporary_bytes;
    NVBENCH_CUDA_CALL(cub::DeviceReduce::Reduce(temporary, available, in(), out(), n,
                                               cuda::std::plus<>{}, std::int32_t{0}, stream.get_stream()));
  }
  std::int32_t read_and_check(int n) {
    std::int32_t actual = -1;
    NVBENCH_CUDA_CALL(cudaMemcpyAsync(&actual, out(), sizeof(actual), cudaMemcpyDeviceToHost, stream.get_stream()));
    NVBENCH_CUDA_CALL(cudaStreamSynchronize(stream.get_stream()));
    if (actual != prefix.at(n)) { throw std::runtime_error("GPU reduction differs from CPU I64 prefix sum"); }
    return actual;
  }
  std::int32_t check(int n) {
    std::size_t needed = 0;
    NVBENCH_CUDA_CALL(cub::DeviceReduce::Reduce(nullptr, needed, in(), out(), n,
                                               cuda::std::plus<>{}, std::int32_t{0}, stream.get_stream()));
    if (needed > temporary_bytes) { throw std::runtime_error("Fixed scratch buffer too small"); }
    NVBENCH_CUDA_CALL(cudaMemsetAsync(out(), 0xff, sizeof(std::int32_t), stream.get_stream()));
    reduce(n);
    return read_and_check(n);
  }
};

std::unique_ptr<fixture> data_owner;
struct fixture_cleanup_guard {
  // The NVBench main scope destroys this before CUDA-context finalization,
  // including stack unwinding. The global pointer is then empty at process exit.
  ~fixture_cleanup_guard() { data_owner.reset(); }
};

void fixed_reduce(nvbench::state& state) {
  const auto raw_n = state.get_int64("Elements{io}");
  if (raw_n < 0 || raw_n > capacity) { throw std::runtime_error("Length outside fixed allocation"); }
  const int n = static_cast<int>(raw_n);
  if (!data_owner) { data_owner = std::make_unique<fixture>(); }
  auto& data = *data_owner;
  static const bool initial_checks = [&] {
    for (const int size : {0, 1, 4095, 4096, 4097, center-4096, center-2048, center-32,
                           center-4, center-1, center, center+1}) {
      const auto actual = data.check(size);
      std::printf("PRECHECK N=%d expected=%lld actual=%d\n", size,
                  static_cast<long long>(data.prefix[size]), actual);
    }
    return true;
  }();
  (void) initial_checks;
  state.set_cuda_stream(nvbench::make_cuda_stream_view(data.stream.get_stream()));
  const auto before = data.check(n);
  state.add_element_count(n);
  state.add_global_memory_reads<std::int32_t>(n, "Size");
  state.add_global_memory_writes<std::int32_t>(1);
  state.exec(nvbench::exec_tag::gpu | nvbench::exec_tag::no_batch, [&](nvbench::launch&) {
    data.reduce(n);
  });
  const auto after = data.read_and_check(n);
  std::printf("CHECK N=%d expected=%lld before=%d after=%d input=%p output=%p scratch=%p stream=%p\n",
              n, static_cast<long long>(data.prefix[n]), before, after, data.input.ptr,
              data.output.ptr, data.temporary, static_cast<void*>(data.stream.get_stream()));
}
} // namespace

NVBENCH_BENCH(fixed_reduce).set_name("fixed_input_reduce")
  .add_int64_axis("Elements{io}", {center-4096, center-2048, center-32, center-4, center-1, center, center+1});

NVBENCH_MAIN
