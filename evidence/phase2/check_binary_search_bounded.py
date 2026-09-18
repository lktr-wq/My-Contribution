#!/usr/bin/env python3
import datetime,hashlib,json,subprocess,sys,time
from pathlib import Path
root=Path(__file__).resolve().parents[2]
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False);(out/'build').mkdir()
(out/'.gitattributes').write_text('* -text\n')
src=root/'evidence/phase2/binary_search_bounded_check.cu'
cccl=Path('/home/lktr/src/cccl')
binary=out/'build/bounded_check'
capture=lambda args:subprocess.check_output(args,timeout=10).decode().strip()
m={'utc_start':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completed':False,
   'performance_tested':False,'head':capture(['git','-C',str(cccl),'rev-parse','HEAD']),
   'status_before':capture(['git','-C',str(cccl),'status','--porcelain']),
   'hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
             [src,src.with_name('binary_search_bounded.cuh'),Path(__file__)]},'steps':[]}
save=lambda:(out/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
save()
try:
    assert m['head']=='f747ef146b77ed1e8f38fe8cb3c67effaf7793f2' and not m['status_before']
    for label,cmd,limit in [
      ('compile',['/usr/local/cuda/bin/nvcc','-O3','-std=c++17','-arch=sm_89',
       '-I'+str(cccl/'libcudacxx/include'),str(src),'-o',str(binary)],120),
      ('check',[str(binary)],60),
      ('memcheck',['/usr/local/cuda/bin/compute-sanitizer','--tool','memcheck','--error-exitcode','3',str(binary)],60)]:
        start=time.monotonic()
        with (out/(label+'.stdout.log')).open('wb') as a,(out/(label+'.stderr.log')).open('wb') as b:
            p=subprocess.run(cmd,stdout=a,stderr=b,timeout=limit)
        m['steps'].append({'label':label,'command':cmd,'returncode':p.returncode,'elapsed_s':time.monotonic()-start});save()
        print(label,p.returncode,flush=True)
        assert p.returncode==0
    print((out/'check.stdout.log').read_text(),flush=True)
    assert 'PASS constexpr host device' in (out/'check.stdout.log').read_text()
    m['status_after']=capture(['git','-C',str(cccl),'status','--porcelain']);assert not m['status_after']
    m['completed']=True
except Exception as e:m['error']=repr(e);raise
finally:save()
