// Reuse the exact three kernels; keep the previous benchmark entry unchanged.
#define main original_benchmark_main
#include "binary_search_bounded_bench.cu"
#undef main
std::uint32_t next_random(std::uint32_t& state){state^=state<<13;state^=state>>17;state^=state<<5;return state;}
int main(int argc,char** argv) try {
  if(argc!=2 || (std::strcmp(argv[1],"--check") && std::strcmp(argv[1],"--measure")))
    throw std::runtime_error("Use --check|--measure");
  const bool measure=std::strcmp(argv[1],"--measure")==0;
  constexpr int count=4096,blocks=512,batch=3;
  const std::int64_t sizes[]={1,8,32,257,4096,20000,65536};
  cudaEvent_t start,stop;checked(cudaEventCreate(&start));checked(cudaEventCreate(&stop));
  int query_checks=0,block_checks=0;
  for(auto n:sizes) {
    std::vector<int>a(n),q(count),oracle(count),got(count+2);
    for(int i=0;i<n;++i)a[i]=2*i;
    device_buffer<int>da(n),dq(count),out(count+2);
    checked(cudaMemcpy(da.p,a.data(),n*sizeof(int),cudaMemcpyHostToDevice));
    for(int shape=0;shape<2;++shape) {
      std::uint32_t rng=0x5eed1234u+static_cast<std::uint32_t>(n)+shape;
      for(int i=0;i<count;++i)q[i]=2*static_cast<int>(next_random(rng)%n)+(shape==1 && i%2);
      for(int i=count-1;i>0;--i)std::swap(q[i],q[next_random(rng)%(i+1)]);
      int expected=0;
      for(int i=0;i<count;++i){oracle[i]=std::binary_search(a.begin(),a.end(),q[i]);expected+=oracle[i];}
      if(expected!=(shape==0?count:count/2))throw std::runtime_error("generator");
      checked(cudaMemcpy(dq.p,q.data(),count*sizeof(int),cudaMemcpyHostToDevice));
      auto validate=[&](bool repeated) {
        checked(cudaDeviceSynchronize());
        checked(cudaMemcpy(got.data(),out.p,got.size()*sizeof(int),cudaMemcpyDeviceToHost));
        int len=repeated?blocks:count;
        for(int i=0;i<len;++i)if(got[i+1]!=(repeated?expected:oracle[i]))throw std::runtime_error("result mismatch");
        if(got[0]!=-1 || !std::all_of(got.begin()+len+1,got.end(),[](int x){return x==-1;}))throw std::runtime_error("guard");
        if(repeated)block_checks+=blocks;else query_checks+=count;
      };
      for(int v=0;v<3;++v) {
        checked(cudaMemset(out.p,0xff,got.size()*sizeof(int)));
        launch_bounded<false>(v,da.p,n,dq.p,count,out.p+1,(count+255)/256);validate(false);
      }
      for(int r=0;r<(measure?3:1);++r) for(int order=0;order<3;++order) {
        int v=(order+r)%3;
        checked(cudaMemset(out.p,0xff,got.size()*sizeof(int)));
        launch_bounded<true>(v,da.p,n,dq.p,count,out.p+1,blocks);validate(true);
        if(measure) {
          for(int w=0;w<20;++w)launch_bounded<true>(v,da.p,n,dq.p,count,out.p+1,blocks);
          checked(cudaDeviceSynchronize());
          for(int i=0;i<30;++i) {
            checked(cudaEventRecord(start));
            for(int b=0;b<batch;++b)launch_bounded<true>(v,da.p,n,dq.p,count,out.p+1,blocks);
            checked(cudaEventRecord(stop));checked(cudaEventSynchronize(stop));
            float ms;checked(cudaEventElapsedTime(&ms,start,stop));
            std::printf("SAMPLE n=%lld shape=%d round=%d variant=%d sample=%d ms=%.9f\n",(long long)n,shape,r,v,i,ms/batch);
          }
          validate(true);
        }
      }
    }
  }
  checked(cudaEventDestroy(start));checked(cudaEventDestroy(stop));
  std::printf("PASS queries=%d blocks=%d timed=%d\n",query_checks,block_checks,int(measure));return 0;
} catch(const std::exception& e){std::fprintf(stderr,"ERROR %s\n",e.what());return 1;}
