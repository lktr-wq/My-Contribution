#include "binary_search_bounded.cuh"
#include <cuda_runtime.h>
#include <algorithm>
#include <cstdio>
#include <stdexcept>
#include <vector>
#include <cstdlib>
#include <cstring>
#include <numeric>
void checked(cudaError_t e){if(e!=cudaSuccess)throw std::runtime_error(cudaGetErrorString(e));}
template<class T> struct device_buffer {
  T* p=nullptr;
  explicit device_buffer(std::size_t n){checked(cudaMalloc(&p,n*sizeof(T)));}
  ~device_buffer(){if(p)(void)cudaFree(p);}
  device_buffer(const device_buffer&)=delete;
  device_buffer& operator=(const device_buffer&)=delete;
};
template<int V> __device__ bool candidate(const int* a,std::int64_t n,int q) {
  if constexpr(V==0) return cuda::std::binary_search(a,a+n,q);
  else return bounded_diagnostic::search<V==2>(a,a+n,q,cuda::std::less<int>{});
}
template<int V,bool Repeated>
__global__ void bounded_kernel(const int* a,std::int64_t n,const int* queries,int count,int* out) {
  if constexpr(Repeated) {
    __shared__ int hits;
    if(threadIdx.x==0)hits=0;
    __syncthreads();
    for(int i=threadIdx.x;i<count;i+=blockDim.x)
      if(candidate<V>(a,n,queries[i]))atomicAdd(&hits,1);
    __syncthreads();
    if(threadIdx.x==0)out[blockIdx.x]=hits;
  } else {
    int i=blockIdx.x*blockDim.x+threadIdx.x;
    if(i<count)out[i]=candidate<V>(a,n,queries[i]);
  }
}
template<bool Repeated>
void launch_bounded(int v,const int* a,std::int64_t n,const int* q,int count,int* out,int blocks) {
  switch(v) {
    case 0:bounded_kernel<0,Repeated><<<blocks,256>>>(a,n,q,count,out);break;
    case 1:bounded_kernel<1,Repeated><<<blocks,256>>>(a,n,q,count,out);break;
    case 2:bounded_kernel<2,Repeated><<<blocks,256>>>(a,n,q,count,out);break;
    default:throw std::runtime_error("variant");
  }
  checked(cudaGetLastError());
}
int main(int argc,char** argv) try {
  if(argc!=3 || (std::strcmp(argv[1],"--check") && std::strcmp(argv[1],"--measure")))
    throw std::runtime_error("Use --check|--measure runtime_length");
  const bool measure=std::strcmp(argv[1],"--measure")==0;
  char* end=nullptr;const std::int64_t n=std::strtoll(argv[2],&end,10);
  if(*end || n<1 || n>1000000)throw std::runtime_error("diagnostic allocation limit");
  const int count=static_cast<int>(n),blocks=4096;
  std::vector<int>a(count),q(count),got(std::max(count,blocks)+2);
  std::iota(a.begin(),a.end(),0);
  device_buffer<int> da(count),dq(count),out(got.size());
  checked(cudaMemcpy(da.p,a.data(),count*sizeof(int),cudaMemcpyHostToDevice));
  cudaEvent_t start,stop;checked(cudaEventCreate(&start));checked(cudaEventCreate(&stop));
  int query_checks=0,block_checks=0;
  for(int shape=0;shape<3;++shape) {
    for(int i=0;i<count;++i)q[i]=shape==0?i:shape==1?count+1+i:count/2;
    checked(cudaMemcpy(dq.p,q.data(),count*sizeof(int),cudaMemcpyHostToDevice));
    auto validate=[&](int length,int expected) {
      checked(cudaDeviceSynchronize());
      checked(cudaMemcpy(got.data(),out.p,got.size()*sizeof(int),cudaMemcpyDeviceToHost));
      for(int i=1;i<=length;++i)if(got[i]!=expected)throw std::runtime_error("output mismatch");
      if(got[0]!=-1 || !std::all_of(got.begin()+length+1,got.end(),[](int x){return x==-1;}))
        throw std::runtime_error("guard mismatch");
    };
    for(int v=0;v<3;++v) {
      checked(cudaMemset(out.p,0xff,got.size()*sizeof(int)));
      launch_bounded<false>(v,da.p,n,dq.p,count,out.p+1,(count+255)/256);
      validate(count,shape!=1);query_checks+=count;
    }
    for(int round=0;round<(measure?3:1);++round) for(int order=0;order<3;++order) {
      int v=(order+round)%3;
      checked(cudaMemset(out.p,0xff,got.size()*sizeof(int)));
      launch_bounded<true>(v,da.p,n,dq.p,count,out.p+1,blocks);
      validate(blocks,shape==1?0:count);block_checks+=blocks;
      if(measure) {
        for(int i=0;i<20;++i)launch_bounded<true>(v,da.p,n,dq.p,count,out.p+1,blocks);
        checked(cudaDeviceSynchronize());
        for(int i=0;i<30;++i) {
          checked(cudaEventRecord(start));
          launch_bounded<true>(v,da.p,n,dq.p,count,out.p+1,blocks);
          checked(cudaEventRecord(stop));checked(cudaEventSynchronize(stop));
          float ms=0;checked(cudaEventElapsedTime(&ms,start,stop));
          std::printf("SAMPLE shape=%d round=%d variant=%d sample=%d ms=%.9f\n",shape,round,v,i,ms);
        }
        validate(blocks,shape==1?0:count);block_checks+=blocks;
      }
    }
  }
  checked(cudaEventDestroy(start));checked(cudaEventDestroy(stop));
  std::printf("PASS queries=%d blocks=%d timed=%d\n",query_checks,block_checks,int(measure));return 0;
} catch(const std::exception& e){std::fprintf(stderr,"ERROR %s\n",e.what());return 1;}
