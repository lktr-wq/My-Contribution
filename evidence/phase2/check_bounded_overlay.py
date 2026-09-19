#!/usr/bin/env python3
import datetime,hashlib,json,subprocess,sys,time
from pathlib import Path
root=Path(__file__).resolve().parents[2];cccl=Path('/home/lktr/src/cccl')
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False);(out/'build').mkdir();(out/'.gitattributes').write_text('* -text\n')
overlay=root/'evidence/phase2/bounded_overlay';wrapper=root/'evidence/phase2/bounded_official_test.cu'
testroot=cccl/'libcudacxx/test/libcudacxx/std/algorithms/alg.sorting/alg.binary.search'
capture=lambda a:subprocess.check_output(a,timeout=10).decode().strip()
m={'start':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completed':False,'steps':[],
 'head':capture(['git','-C',str(cccl),'rev-parse','HEAD']),'status_before':capture(['git','-C',str(cccl),'status','--porcelain'])}
save=lambda:(out/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
def run(label,args,limit=45):
    e={'label':label,'command':args};m['steps'].append(e);save();t=time.monotonic()
    with (out/(label+'.stdout.log')).open('wb') as a,(out/(label+'.stderr.log')).open('wb') as b:p=subprocess.run(args,stdout=a,stderr=b,timeout=limit)
    e.update(returncode=p.returncode,elapsed_s=time.monotonic()-t);save();print(label,p.returncode,flush=True);assert p.returncode==0
try:
    assert m['head']=='f747ef146b77ed1e8f38fe8cb3c67effaf7793f2' and not m['status_before']
    sources=[testroot/d/(n+s+'.pass.cpp') for d,n in [('binary.search','binary_search'),('lower.bound','lower_bound'),('equal.range','equal_range')] for s in ['','_comp']]
    m['hashes']={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources+[wrapper,overlay/'cuda/std/__algorithm/lower_bound.h',Path(__file__)]}
    modes=[] if '--extended-only' in sys.argv[2:] else (['overlay'] if '--overlay-only' in sys.argv[2:] else ['baseline','overlay'])
    for mode in modes:
      for source in sources:
        name=mode+'-'+source.name.split('.')[0];binary=out/'build'/name
        args=['/usr/local/cuda/bin/nvcc','-O2','-std=c++17','-arch=sm_89']
        if mode=='overlay':args+=['-I'+str(overlay)]
        args+=['-I'+str(cccl/'libcudacxx/include'),'-I'+str(cccl/'libcudacxx/test/support'),'-DTEST_SOURCE="'+str(source)+'"']
        if source.name=='equal_range_comp.pass.cpp':args+=['-DEXTRA_POINTER_TEST']
        if mode=='overlay' and source.name=='binary_search.pass.cpp':
            run('overlay-dependencies',args+['-M',str(wrapper)])
            assert str(overlay/'cuda/std/__algorithm/lower_bound.h') in (out/'overlay-dependencies.stdout.log').read_text().replace('\\ ', ' ')
        run(name+'-compile',args+[str(wrapper),'-o',str(binary)])
        run(name+'-run',[str(binary)],20)
    if '--extended-only' in sys.argv[2:]:
        src=root/'evidence/phase2/binary_search_bounded_check.cu'
        m['hashes'][str(src)]=hashlib.sha256(src.read_bytes()).hexdigest()
        binary=out/'build/extended'
        run('extended-compile',['/usr/local/cuda/bin/nvcc','-O2','-std=c++17','-arch=sm_89','-I'+str(overlay),'-I'+str(cccl/'libcudacxx/include'),str(src),'-o',str(binary)])
        run('extended-run',[str(binary)],20)
    m['status_after']=capture(['git','-C',str(cccl),'status','--porcelain']);assert not m['status_after'];m['completed']=True
except Exception as e:m['error']=repr(e);raise
finally:save()
