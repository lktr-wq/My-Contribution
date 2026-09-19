#define main prior_benchmark_main
#include "binary_search_bounded_bench.cu"
#undef main
std::uint32_t random_next(std::uint32_t& s){s^=s<<13;s^=s>>17;s^=s<<5;return s;}
int main(int argc,char** argv) try {
  if(argc!=2 || (std::strcmp(argv[1],"--check") && std::strcmp(argv[1],"--measure")))throw std::runtime_error("mode");
  const bool measure=std::strcmp(argv[1],"--measure")==0;
  constexpr int count=4194304,blocks=count/256,batch=3;
  const std::int64_t sizes[]={1,32,257,4096,20000,65536};
  cudaEvent_t start,stop;checked(cudaEventCreate(&start));checked(cudaEventCreate(&stop));
  std::int64_t checks=0;
  for(auto n:sizes) {
    std::vector<int>a(n),q(count),oracle(count),got(count+2);
    for(int i=0;i<n;++i)a[i]=2*i;
    device_buffer<int>da(n),dq(count),out(count+2);
    checked(cudaMemcpy(da.p,a.data(),n*sizeof(int),cudaMemcpyHostToDevice));
    for(int shape=0;shape<2;++shape) {
      std::uint32_t rng=0x5eed1234u+static_cast<std::uint32_t>(n)+shape;
      for(int i=0;i<count;++i)q[i]=2*static_cast<int>(random_next(rng)%n)+(shape==1 && i%2);
      for(int i=count-1;i>0;--i)std::swap(q[i],q[random_next(rng)%(i+1)]);
      int hits=0;
      for(int i=0;i<count;++i){oracle[i]=std::binary_search(a.begin(),a.end(),q[i]);hits+=oracle[i];}
      if(hits!=(shape==0?count:count/2))throw std::runtime_error("generator");
      checked(cudaMemcpy(dq.p,q.data(),count*sizeof(int),cudaMemcpyHostToDevice));
      auto validate=[&] {
        checked(cudaDeviceSynchronize());
        checked(cudaMemcpy(got.data(),out.p,got.size()*sizeof(int),cudaMemcpyDeviceToHost));
        for(int i=0;i<count;++i)if(got[i+1]!=oracle[i])throw std::runtime_error("query result");
        if(got.front()!=-1 || got.back()!=-1)throw std::runtime_error("guard");
        checks+=count;
      };
      for(int r=0;r<(measure?3:1);++r)for(int order=0;order<3;++order) {
        int v=(order+r)%3;
        checked(cudaMemset(out.p,0xff,got.size()*sizeof(int)));
        launch_bounded<false>(v,da.p,n,dq.p,count,out.p+1,blocks);validate();
        if(measure) {
          for(int w=0;w<50;++w)launch_bounded<false>(v,da.p,n,dq.p,count,out.p+1,blocks);
          checked(cudaDeviceSynchronize());
          for(int i=0;i<30;++i) {
            checked(cudaEventRecord(start));
            for(int b=0;b<batch;++b)launch_bounded<false>(v,da.p,n,dq.p,count,out.p+1,blocks);
            checked(cudaEventRecord(stop));checked(cudaEventSynchronize(stop));
            float ms;checked(cudaEventElapsedTime(&ms,start,stop));
            std::printf("SAMPLE n=%lld shape=%d round=%d variant=%d sample=%d ms=%.9f\n",(long long)n,shape,r,v,i,ms/batch);
          }
          validate();
        }
      }
    }
  }
  checked(cudaEventDestroy(start));checked(cudaEventDestroy(stop));
  std::printf("PASS queries=%lld timed=%d\n",(long long)checks,int(measure));return 0;
}catch(const std::exception& e){std::fprintf(stderr,"ERROR %s\n",e.what());return 1;}
