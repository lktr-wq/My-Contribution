// Local diagnostic only. Loop adapted from NVIDIA/cccl lower_bound.h at
// f747ef146b77ed1e8f38fe8cb3c67effaf7793f2 (Apache-2.0 WITH LLVM-exception).
#pragma once
#include <cuda/std/algorithm>
#include <cuda/std/functional>
#include <cuda/std/iterator>
#include <cuda/std/limits>
#include <cuda/std/type_traits>
#include <cstdint>
namespace bounded_diagnostic {
template<class It, class D>
__host__ __device__ constexpr bool eligible(D n) {
  if constexpr(cuda::std::is_integral_v<D> && cuda::std::is_signed_v<D> &&
    cuda::std::numeric_limits<D>::digits>31 &&
    cuda::std::is_base_of_v<cuda::std::random_access_iterator_tag,
      typename cuda::std::iterator_traits<It>::iterator_category>)
    return n>=0 && n<=static_cast<D>(2147483647);
  else return false;
}
template<class It,class D,class T,class Comp,class Proj>
__host__ __device__ constexpr It loop(It first,D len,const T& value,Comp& comp,Proj& proj) {
  while(len!=0) {
    auto half=cuda::std::__half_positive(len);
    It mid=first;
    cuda::std::advance(mid,half);
    if(cuda::std::invoke(comp,cuda::std::invoke(proj,*mid),value)) {
      first=++mid;
      len-=half+1;
    } else len=half;
  }
  return first;
}
template<bool Narrow,class It,class T,class Comp,class Proj>
__host__ __device__ constexpr It lower(It first,It last,const T& value,Comp& comp,Proj& proj,bool* selected=nullptr) {
  auto len=cuda::std::distance(first,last);
  if constexpr(Narrow) {
    if(eligible<It>(len)) {
      if(selected) *selected=true;
      return loop(first,static_cast<std::int32_t>(len),value,comp,proj);
    }
  }
  if(selected) *selected=false;
  return loop(first,len,value,comp,proj);
}
template<bool Narrow,class It,class T,class Comp>
__host__ __device__ constexpr bool search(It first,It last,const T& value,Comp comp) {
  cuda::std::identity proj;
  first=lower<Narrow>(first,last,value,comp,proj);
  return first!=last && !comp(value,*first);
}
}
