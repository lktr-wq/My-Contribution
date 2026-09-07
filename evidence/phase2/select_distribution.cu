// Local screening harness, not a modification of the official benchmark or CUB.
#include <cub/device/device_select.cuh>
#include <nvbench/nvbench.cuh>
#include <nvbench/cuda_call.cuh>
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <random>
#include <stdexcept>
#include <vector>

struct allocation {
  void* p = nullptr;
  explicit allocation(std::size_t n) { NVBENCH_CUDA_CALL(cudaMalloc(&p,n)); }
  ~allocation() { if(p) (void)cudaFree(p); }
  allocation(const allocation&) = delete;
  allocation& operator=(const allocation&) = delete;
};

void select_distribution(nvbench::state& state) {
  const auto code=state.get_int64("Case");
  if(code<0 || code>5) throw std::runtime_error("Invalid case");
  const int n=1 << (code/3==0 ? 20 : 22);
  const int pattern=code%3;
  std::vector<int> input(n),expected;
  std::vector<unsigned char> flags(n);
  expected.reserve(n/2);
  for(int i=0;i<n;++i) {
    input[i]=i-n/2; // unique signed values expose ordering/duplication errors
    flags[i]=pattern==0 ? i%2 : i<n/2;
  }
  if(pattern==2) {
    std::mt19937 generator(6721);
    std::shuffle(flags.begin(),flags.end(),generator);
  }
  for(int i=0;i<n;++i) if(flags[i]) expected.push_back(input[i]);
  if(expected.size()!=std::size_t(n/2)) throw std::runtime_error("Invalid selection count");
  allocation in(n*sizeof(int)),flag(n),out((n+2)*sizeof(int)),count(sizeof(std::int64_t));
  auto stream=state.get_cuda_stream().get_stream();
  auto* dst=static_cast<int*>(out.p)+1;
  NVBENCH_CUDA_CALL(cudaMemcpy(in.p,input.data(),n*sizeof(int),cudaMemcpyHostToDevice));
  NVBENCH_CUDA_CALL(cudaMemcpy(flag.p,flags.data(),n,cudaMemcpyHostToDevice));
  NVBENCH_CUDA_CALL(cudaMemset(out.p,0xa5,(n+2)*sizeof(int)));
  std::size_t bytes=0;
  auto call=[&](void* scratch) {
    NVBENCH_CUDA_CALL(cub::DeviceSelect::Flagged(scratch,bytes,
      static_cast<const int*>(in.p),static_cast<const unsigned char*>(flag.p),dst,
      static_cast<std::int64_t*>(count.p),std::int64_t(n),stream));
  };
  call(nullptr);
  allocation scratch(bytes);
  auto check=[&] {
    NVBENCH_CUDA_CALL(cudaStreamSynchronize(stream));
    std::int64_t selected=-1;
    NVBENCH_CUDA_CALL(cudaMemcpy(&selected,count.p,sizeof(selected),cudaMemcpyDeviceToHost));
    std::vector<int> actual(n+2);
    NVBENCH_CUDA_CALL(cudaMemcpy(actual.data(),out.p,actual.size()*sizeof(int),cudaMemcpyDeviceToHost));
    if(selected!=n/2 || !std::equal(expected.begin(),expected.end(),actual.begin()+1))
      throw std::runtime_error("CPU/GPU count or stable output mismatch");
    const int sentinel=static_cast<int>(0xa5a5a5a5u);
    if(actual.front()!=sentinel || !std::all_of(actual.begin()+1+n/2,actual.end(),
      [=](int x){return x==sentinel;})) throw std::runtime_error("Output guard changed");
  };
  call(scratch.p);
  check();
  state.add_element_count(n);
  state.add_global_memory_reads<int>(n);
  state.add_global_memory_reads<unsigned char>(n);
  state.add_global_memory_writes<int>(n/2);
  state.exec(nvbench::exec_tag::gpu | nvbench::exec_tag::no_batch,
    [&](nvbench::launch&){call(scratch.p);});
  check();
  std::printf("CHECK Case=%lld N=%d pattern=%d selected=%d before=PASS after=PASS guards=PASS\n",
    static_cast<long long>(code),n,pattern,n/2);
}
NVBENCH_BENCH(select_distribution).add_int64_axis("Case",{0,1,2,3,4,5});
NVBENCH_MAIN
