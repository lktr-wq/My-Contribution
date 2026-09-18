#include "binary_search_bounded.cuh"
#include <cuda_runtime.h>
#include <cstdio>
#include <stdexcept>
using I64=std::int64_t;
// A real random-access value sequence without giant allocations; non-random
// categories use the same storage adapter to exercise the fallback dispatch.
template<class Category> struct Iter {
  using value_type=I64; using difference_type=I64; using reference=I64;
  using pointer=void; using iterator_category=Category;
  const I64* data; I64 pos;
  __host__ __device__ constexpr I64 operator*() const {return data?data[pos]:pos*2;}
  __host__ __device__ constexpr Iter& operator++(){++pos;return *this;}
  __host__ __device__ constexpr Iter operator++(int){auto x=*this;++*this;return x;}
  __host__ __device__ constexpr Iter& operator--(){--pos;return *this;}
  __host__ __device__ constexpr Iter operator--(int){auto x=*this;--*this;return x;}
  __host__ __device__ constexpr Iter& operator+=(I64 n){pos+=n;return *this;}
  __host__ __device__ constexpr Iter& operator-=(I64 n){pos-=n;return *this;}
  __host__ __device__ constexpr Iter operator+(I64 n) const {auto x=*this;return x+=n;}
  __host__ __device__ friend constexpr Iter operator+(I64 n,Iter x){return x+=n;}
  __host__ __device__ constexpr Iter operator-(I64 n) const {auto x=*this;return x-=n;}
  __host__ __device__ constexpr I64 operator-(Iter b) const{return pos-b.pos;}
  __host__ __device__ constexpr I64 operator[](I64 n) const{return *(*this+n);}
  __host__ __device__ constexpr bool operator==(Iter b) const{return pos==b.pos && data==b.data;}
  __host__ __device__ constexpr bool operator!=(Iter b) const{return !(*this==b);}
  __host__ __device__ constexpr bool operator<(Iter b) const{return pos<b.pos;}
  __host__ __device__ constexpr bool operator>(Iter b) const{return b<*this;}
  __host__ __device__ constexpr bool operator<=(Iter b) const{return !(b<*this);}
  __host__ __device__ constexpr bool operator>=(Iter b) const{return !(*this<b);}
};
using RA=Iter<cuda::std::random_access_iterator_tag>;
using FW=Iter<cuda::std::forward_iterator_tag>;
using BI=Iter<cuda::std::bidirectional_iterator_tag>;
struct Stats {int cases=0,failures=0,narrow=0,fallback=0;};
template<class It,class T,class Comp>
__host__ __device__ void check(Stats& s,It first,It last,T value,Comp comp,bool expected_narrow) {
  cuda::std::identity proj;
  const auto oracle=cuda::std::lower_bound(first,last,value,comp);
  bool path=false;
  const auto a=bounded_diagnostic::lower<false>(first,last,value,comp,proj);
  const auto b=bounded_diagnostic::lower<true>(first,last,value,comp,proj,&path);
  const bool found=cuda::std::binary_search(first,last,value,comp);
  const bool x=bounded_diagnostic::search<false>(first,last,value,comp);
  const bool y=bounded_diagnostic::search<true>(first,last,value,comp);
  ++s.cases;
  s.failures+=(a!=oracle || b!=oracle || x!=found || y!=found || path!=expected_narrow);
  path?++s.narrow:++s.fallback;
}
struct Record {I64 key; int payload;};
struct Hetero {
  int* calls;
  __host__ __device__ bool operator()(const Record& a,I64 b) const {++*calls;return a.key<b;}
  __host__ __device__ bool operator()(I64 a,const Record& b) const {++*calls;return a<b.key;}
};
struct Key {__host__ __device__ constexpr I64 operator()(const Record& r) const{return r.key;}};
__host__ __device__ Stats suite() {
  Stats s;
  I64 data[257];
  const int sizes[]={0,1,2,3,7,8,9,31,32,33,255,256,257};
  for(int n:sizes) for(int shape=0;shape<4;++shape) {
    for(int i=0;i<n;++i) data[i]=shape==0?2*i:shape==1?i/4:shape==2?7:2*(n-i);
    for(I64 q=-1;q<=2*n+1;++q) {
      if(shape==3) check(s,data,data+n,q,cuda::std::greater<I64>{},true);
      else {
        auto comp=cuda::std::less<I64>{};
        check(s,data,data+n,q,comp,true);
        check(s,RA{data,0},RA{data,n},q,comp,true);
        check(s,FW{data,0},FW{data,n},q,comp,false);
        check(s,BI{data,0},BI{data,n},q,comp,false);
      }
    }
  }
  I64 partitioned[]={2,0,1,3,3,6,4,5};
  check(s,partitioned,partitioned+8,I64(3),cuda::std::less<I64>{},true);
  for(I64 n:{I64(2147483646),I64(2147483647),I64(2147483648),I64(4294967313)})
    for(I64 q:{I64(-1),I64(0),I64(1),n,2*(n-1),2*n})
      check(s,RA{nullptr,0},RA{nullptr,n},q,cuda::std::less<I64>{},n<=2147483647);
  Record records[]={{1,9},{3,2},{3,5},{8,1}};
  for(I64 q=-1;q<=9;++q) {
    int a=0,b=0,c=0;
    bool x=cuda::std::binary_search(records,records+4,q,Hetero{&a});
    bool y=bounded_diagnostic::search<false>(records,records+4,q,Hetero{&b});
    bool z=bounded_diagnostic::search<true>(records,records+4,q,Hetero{&c});
    ++s.cases; s.failures+=(x!=y || x!=z || a!=b || a!=c);
    auto cmp=cuda::std::less<I64>{};Key proj;
    auto p=bounded_diagnostic::lower<true>(records,records+4,q,cmp,proj);
    auto oracle=records;while(oracle!=records+4 && oracle->key<q) ++oracle;
    ++s.cases;s.failures+=(p!=oracle);
  }
  return s;
}
constexpr bool constant_check() {
  I64 a[]={0,2,2,6};
  auto comp=cuda::std::less<I64>{};
  return bounded_diagnostic::search<true>(a,a+4,I64(2),comp) &&
    !bounded_diagnostic::search<true>(a,a+4,I64(3),comp) &&
    !bounded_diagnostic::eligible<I64*>(I64(-1)) &&
    !bounded_diagnostic::eligible<I64*>(int(10));
}
static_assert(constant_check());
__global__ void run(Stats* result){if(threadIdx.x==0 && blockIdx.x==0)*result=suite();}
void checked(cudaError_t e){if(e!=cudaSuccess)throw std::runtime_error(cudaGetErrorString(e));}
int main() try {
  auto h=suite();Stats d;Stats* ptr=nullptr;
  checked(cudaMalloc(&ptr,sizeof(Stats)));run<<<1,1>>>(ptr);
  checked(cudaGetLastError());checked(cudaDeviceSynchronize());
  checked(cudaMemcpy(&d,ptr,sizeof(d),cudaMemcpyDeviceToHost));checked(cudaFree(ptr));
  std::printf("HOST cases=%d failures=%d narrow=%d fallback=%d\n",h.cases,h.failures,h.narrow,h.fallback);
  std::printf("DEVICE cases=%d failures=%d narrow=%d fallback=%d\n",d.cases,d.failures,d.narrow,d.fallback);
  if(h.failures || d.failures || h.cases!=d.cases)return 2;
  std::puts("PASS constexpr host device; performance_tested=false");return 0;
} catch(const std::exception& e){std::fprintf(stderr,"ERROR %s\n",e.what());return 1;}
