// Local diagnostics for NVIDIA/cccl #11412; no upstream implementation changes.
// Integer sorted-input experiment only, NOT a generic binary_search replacement.
#include <cuda_runtime.h>
#include <cuda/std/algorithm>
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <stdexcept>
#include <vector>

void checked(cudaError_t e) {
  if(e!=cudaSuccess) throw std::runtime_error(cudaGetErrorString(e));
}
template<class T> struct device_buffer {
  T* p=nullptr;
  explicit device_buffer(std::size_t n) { checked(cudaMalloc(&p,n*sizeof(T))); }
  ~device_buffer() { if(p) (void)cudaFree(p); }
  device_buffer(const device_buffer&)=delete;
  device_buffer& operator=(const device_buffer&)=delete;
};
template<class Index,bool Early>
__device__ bool reference_search(const int* a,Index n,int value) {
  Index lo=0,hi=n;
  while(lo<hi) {
    const Index mid=lo+(hi-lo)/2;
    const int v=a[mid];
    if(v<value) lo=mid+1;
    else {
      // Express equivalence via less-than, not operator==.
      if constexpr(Early) { if(!(value<v)) return true; }
      hi=mid;
    }
  }
  if constexpr(Early) return false;
  else return lo<n && !(value<a[lo]);
}
template<int Variant>
__global__ void search_kernel(const int* a,int n,const int* queries,int qcount,int* output) {
  const int i=blockIdx.x*blockDim.x+threadIdx.x;
  if(i>=qcount) return;
  bool result;
  if constexpr(Variant==0) result=cuda::std::binary_search(a,a+n,queries[i]);
  if constexpr(Variant==1) result=reference_search<std::int64_t,false>(a,n,queries[i]);
  if constexpr(Variant==2) result=reference_search<std::int64_t,true>(a,n,queries[i]);
  if constexpr(Variant==3) result=reference_search<std::int32_t,false>(a,n,queries[i]);
  if constexpr(Variant==4) result=reference_search<std::int32_t,true>(a,n,queries[i]);
  output[i]=result?1:0;
}
void launch(int v,const int* a,int n,const int* q,int count,int* out) {
  const int blocks=(count+127)/128;
  switch(v) {
    case 0: search_kernel<0><<<blocks,128>>>(a,n,q,count,out);break;
    case 1: search_kernel<1><<<blocks,128>>>(a,n,q,count,out);break;
    case 2: search_kernel<2><<<blocks,128>>>(a,n,q,count,out);break;
    case 3: search_kernel<3><<<blocks,128>>>(a,n,q,count,out);break;
    case 4: search_kernel<4><<<blocks,128>>>(a,n,q,count,out);break;
    default: throw std::runtime_error("Invalid variant");
  }
  checked(cudaGetLastError());
}
int main() try {
  static_assert(sizeof(std::ptrdiff_t)==8,"Expected 64-bit pointer difference type");
  const char* names[]={"official","lower64","early64","lower32","early32"};
  int configurations=0,comparisons=0;
  for(int n: {0,1,2,3,31,32,33,255,256,257,20000}) {
    for(int shape=0;shape<3;++shape) {
      std::vector<int> a(n);
      for(int i=0;i<n;++i) a[i]=shape==0 ? 2*i : shape==1 ? i/4 : 7;
      std::vector<int> queries={-2,-1,0,1,2,3,6,7,8,n/2,n,2*n,2*n+1};
      if(n) { queries.push_back(a.front());queries.push_back(a[n/2]);queries.push_back(a.back()); }
      const int count=static_cast<int>(queries.size());
      device_buffer<int> da(std::max(n,1)),dq(count),output(count+2);
      if(n) checked(cudaMemcpy(da.p,a.data(),n*sizeof(int),cudaMemcpyHostToDevice));
      checked(cudaMemcpy(dq.p,queries.data(),count*sizeof(int),cudaMemcpyHostToDevice));
      std::vector<int> got(count+2);
      for(int v=0;v<5;++v) {
        checked(cudaMemset(output.p,0xff,(count+2)*sizeof(int)));
        launch(v,da.p,n,dq.p,count,output.p+1);
        checked(cudaDeviceSynchronize());
        checked(cudaMemcpy(got.data(),output.p,(count+2)*sizeof(int),cudaMemcpyDeviceToHost));
        if(got.front()!=-1 || got.back()!=-1) throw std::runtime_error("Output guard overwritten");
        for(int i=0;i<count;++i) {
          const int expected=std::binary_search(a.begin(),a.end(),queries[i])?1:0;
          if(got[i+1]!=expected) {
            std::fprintf(stderr,"Mismatch N=%d shape=%d variant=%s query=%d expected=%d actual=%d\n",
              n,shape,names[v],queries[i],expected,got[i+1]);
            return 2;
          }
          ++comparisons;
        }
        ++configurations;
        std::printf("PASS N=%d shape=%d variant=%s queries=%d guards=PASS\n",n,shape,names[v],count);
      }
    }
  }
  std::printf("SUMMARY configurations=%d comparisons=%d status=PASS performance_tested=false\n",configurations,comparisons);
  return 0;
} catch(const std::exception& e) {
  std::fprintf(stderr,"ERROR: %s\n",e.what());
  return 1;
}
