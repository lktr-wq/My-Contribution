// Timing entry prepared separately from the unchanged correctness harness.
#define main integer_correctness_main
#include "binary_search_11412.cu"
#undef main
#include <cstring>
#include <numeric>

template<int V> __device__ bool evaluate(const int* a,int n,int value) {
  if constexpr(V==0) return cuda::std::binary_search(a,a+n,value);
  if constexpr(V==1) return reference_search<std::int64_t,false>(a,n,value);
  if constexpr(V==2) return reference_search<std::int64_t,true>(a,n,value);
  if constexpr(V==3) return reference_search<std::int32_t,false>(a,n,value);
  if constexpr(V==4) return reference_search<std::int32_t,true>(a,n,value);
}
// Preserve the issue reproducer's repeated queries and shared atomic accounting.
template<int V> __global__ void repeated_search(const int* a,int n,const int* queries,int count,int* output) {
  __shared__ int found_count;
  if(threadIdx.x==0) found_count=0;
  __syncthreads();
  for(int i=threadIdx.x;i<count;i+=blockDim.x)
    if(evaluate<V>(a,n,queries[i])) atomicAdd(&found_count,1);
  __syncthreads();
  if(threadIdx.x==0) output[blockIdx.x]=found_count;
}
void repeat_launch(int v,const int* a,int n,const int* q,int count,int* out,int blocks) {
  switch(v) {
    case 0: repeated_search<0><<<blocks,256>>>(a,n,q,count,out);break;
    case 1: repeated_search<1><<<blocks,256>>>(a,n,q,count,out);break;
    case 2: repeated_search<2><<<blocks,256>>>(a,n,q,count,out);break;
    case 3: repeated_search<3><<<blocks,256>>>(a,n,q,count,out);break;
    case 4: repeated_search<4><<<blocks,256>>>(a,n,q,count,out);break;
    default: throw std::runtime_error("Invalid variant");
  }
  checked(cudaGetLastError());
}
struct events {
  cudaEvent_t start{},stop{};
  events(){checked(cudaEventCreate(&start));checked(cudaEventCreate(&stop));}
  ~events(){(void)cudaEventDestroy(start);(void)cudaEventDestroy(stop);}
};
int main(int argc,char** argv) try {
  const bool measure=argc==2 && std::strcmp(argv[1],"--measure")==0;
  if(argc>1 && !measure && !(argc==2 && std::strcmp(argv[1],"--check")==0))
    throw std::runtime_error("Use --check or --measure");
  if(integer_correctness_main()!=0) return 2;
  constexpr int n=20000,full_blocks=4096;
  std::vector<int> a(n),queries(n),actual(n+2);
  std::iota(a.begin(),a.end(),0);
  device_buffer<int> da(n),dq(n),output(n+2);
  checked(cudaMemcpy(da.p,a.data(),n*sizeof(int),cudaMemcpyHostToDevice));
  int oracle_checks=0,block_checks=0;
  for(int shape=0;shape<3;++shape) {
    for(int i=0;i<n;++i) queries[i]=shape==0 ? i : shape==1 ? n+1+i : n/2;
    checked(cudaMemcpy(dq.p,queries.data(),n*sizeof(int),cudaMemcpyHostToDevice));
    const int expected_count=shape==1 ? 0 : n;
    for(int v=0;v<5;++v) {
      checked(cudaMemset(output.p,0xff,(n+2)*sizeof(int)));
      launch(v,da.p,n,dq.p,n,output.p+1);
      checked(cudaDeviceSynchronize());
      checked(cudaMemcpy(actual.data(),output.p,(n+2)*sizeof(int),cudaMemcpyDeviceToHost));
      for(int i=0;i<n;++i) {
        const int expected=std::binary_search(a.begin(),a.end(),queries[i])?1:0;
        if(actual[i+1]!=expected) throw std::runtime_error("Per-query oracle mismatch");
        ++oracle_checks;
      }
      if(actual.front()!=-1 || actual.back()!=-1) throw std::runtime_error("Query guard changed");
      const int blocks=measure?full_blocks:4;
      checked(cudaMemset(output.p,0xff,(n+2)*sizeof(int)));
      repeat_launch(v,da.p,n,dq.p,n,output.p+1,blocks);
      checked(cudaDeviceSynchronize());
      checked(cudaMemcpy(actual.data(),output.p,(n+2)*sizeof(int),cudaMemcpyDeviceToHost));
      for(int i=0;i<blocks;++i) {
        if(actual[i+1]!=expected_count) throw std::runtime_error("Block count mismatch");
        ++block_checks;
      }
      if(actual.front()!=-1 || !std::all_of(actual.begin()+blocks+1,actual.end(),[](int x){return x==-1;}))
        throw std::runtime_error("Block output guard changed");
    }
    if(measure) {
      events ev;
      for(int round=0;round<3;++round) {
        // Rotate variants each round; same data and work for every variant.
        for(int order=0;order<5;++order) {
          const int v=(order+2*round)%5;
          for(int warm=0;warm<20;++warm) repeat_launch(v,da.p,n,dq.p,n,output.p+1,full_blocks);
          checked(cudaDeviceSynchronize());
          for(int sample=0;sample<30;++sample) {
            checked(cudaEventRecord(ev.start));
            repeat_launch(v,da.p,n,dq.p,n,output.p+1,full_blocks);
            checked(cudaEventRecord(ev.stop));checked(cudaEventSynchronize(ev.stop));
            float ms=0;checked(cudaEventElapsedTime(&ms,ev.start,ev.stop));
            std::printf("SAMPLE shape=%d round=%d variant=%d sample=%d ms=%.9f\n",shape,round,v,sample,ms);
          }
          checked(cudaMemcpy(actual.data(),output.p,(full_blocks+2)*sizeof(int),cudaMemcpyDeviceToHost));
          for(int i=0;i<full_blocks;++i) if(actual[i+1]!=expected_count) throw std::runtime_error("Post-timing count mismatch");
          if(actual.front()!=-1 || actual[full_blocks+1]!=-1) throw std::runtime_error("Post-timing guard changed");
        }
      }
    }
  }
  std::printf("BENCH_CHECK oracle=%d blocks=%d timed=%d PASS\n",oracle_checks,block_checks,int(measure));
  return 0;
} catch(const std::exception& e) {std::fprintf(stderr,"ERROR: %s\n",e.what());return 1;}
