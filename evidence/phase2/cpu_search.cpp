#include <cuda/std/algorithm>
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <vector>
volatile std::uint64_t sink=0;
__attribute__((noinline)) std::uint64_t queries(const int* a,std::int64_t n,const int* q,int count){
  std::uint64_t hits=0;
  for(int i=0;i<count;++i)hits+=cuda::std::binary_search(a,a+n,q[i]);
  return hits;
}
std::uint32_t rng(std::uint32_t& x){x^=x<<13;x^=x>>17;x^=x<<5;return x;}
int main(){
  constexpr int count=65536;
  for(std::int64_t n:{1,32,257,4096,20000,65536})for(int shape=0;shape<2;++shape){
    std::vector<int>a(n),q(count);for(int i=0;i<n;++i)a[i]=2*i;
    std::uint32_t seed=1234567+n+shape;
    for(int i=0;i<count;++i)q[i]=2*(rng(seed)%n)+(shape && i%2);
    for(int i=count-1;i>0;--i)std::swap(q[i],q[rng(seed)%(i+1)]);
    std::uint64_t expected=0;
    for(int v:q){bool x=std::binary_search(a.begin(),a.end(),v);if(x!=cuda::std::binary_search(a.data(),a.data()+n,v))return 2;expected+=x;}
    for(int w=0;w<3;++w)sink=queries(a.data(),n,q.data(),count);
    for(int s=0;s<9;++s){
      auto start=std::chrono::steady_clock::now();
      auto hits=queries(a.data(),n,q.data(),count);
      auto stop=std::chrono::steady_clock::now();sink=hits;if(hits!=expected)return 3;
      double ns=std::chrono::duration<double,std::nano>(stop-start).count()/count;
      std::printf("SAMPLE %lld %d %d %.6f\n",(long long)n,shape,s,ns);
    }
  }
  std::puts("PASS per-query oracle and timed totals");
}
