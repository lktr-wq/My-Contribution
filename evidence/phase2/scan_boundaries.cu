// Local baseline screening. Stock CUB; no tuning or library modification.
#include <cub/device/device_scan.cuh>
#include <nvbench/nvbench.cuh>
#include <nvbench/cuda_call.cuh>
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <stdexcept>
#include <vector>

struct allocation {
  void* p=nullptr;
  explicit allocation(std::size_t n) { NVBENCH_CUDA_CALL(cudaMalloc(&p,n)); }
  ~allocation() { if(p) (void)cudaFree(p); }
  allocation(const allocation&)=delete;
  allocation& operator=(const allocation&)=delete;
};
void scan_boundaries(nvbench::state& state) {
  const auto raw=state.get_int64("N");
  if(raw<1 || raw>245761) throw std::runtime_error("N outside bounded scope");
  const int n=static_cast<int>(raw);
  std::vector<int> input(n),expected(n);
  std::int64_t sum=0;
  for(int i=0;i<n;++i) {
    input[i]=1+i%17;
    expected[i]=static_cast<int>(sum);
    sum+=input[i]; // total < 4.2 million; no I32 partial-sum overflow
  }
  allocation in(n*sizeof(int)),out((n+2)*sizeof(int));
  auto* dst=static_cast<int*>(out.p)+1;
  auto stream=state.get_cuda_stream().get_stream();
  NVBENCH_CUDA_CALL(cudaMemcpy(in.p,input.data(),n*sizeof(int),cudaMemcpyHostToDevice));
  NVBENCH_CUDA_CALL(cudaMemset(out.p,0xa5,(n+2)*sizeof(int)));
  std::size_t bytes=0;
  auto call=[&](void* scratch) {
    NVBENCH_CUDA_CALL(cub::DeviceScan::ExclusiveSum(scratch,bytes,
      static_cast<const int*>(in.p),dst,std::int64_t(n),stream));
  };
  call(nullptr);
  allocation scratch(bytes);
  auto check=[&] {
    NVBENCH_CUDA_CALL(cudaStreamSynchronize(stream));
    std::vector<int> actual(n+2);
    NVBENCH_CUDA_CALL(cudaMemcpy(actual.data(),out.p,actual.size()*sizeof(int),cudaMemcpyDeviceToHost));
    if(!std::equal(expected.begin(),expected.end(),actual.begin()+1))
      throw std::runtime_error("CPU I64 oracle / GPU output mismatch");
    const int guard=static_cast<int>(0xa5a5a5a5u);
    if(actual.front()!=guard || actual.back()!=guard) throw std::runtime_error("Output guard changed");
  };
  call(scratch.p);
  check();
  // Bound process-start GPU ramp-up outside timing. No forced clock or power changes.
  static bool warmed=false;
  if(!warmed) {
    const auto start=std::chrono::steady_clock::now();
    do {
      call(scratch.p);
      NVBENCH_CUDA_CALL(cudaStreamSynchronize(stream));
    } while(std::chrono::steady_clock::now()-start<std::chrono::milliseconds(500));
    warmed=true;
  }
  state.add_element_count(n);
  state.add_global_memory_reads<int>(n);
  state.add_global_memory_writes<int>(n);
  state.exec(nvbench::exec_tag::gpu | nvbench::exec_tag::no_batch,
    [&](nvbench::launch&){call(scratch.p);});
  check();
  std::printf("CHECK N=%d before=PASS after=PASS guards=PASS\n",n);
}
NVBENCH_BENCH(scan_boundaries).add_int64_axis("N",{1919,1920,1921,46079,46080,46081,245759,245760,245761});
NVBENCH_MAIN
