#!/usr/bin/env python3
import datetime,hashlib,json,re,statistics,subprocess,sys,time
from pathlib import Path
root=Path(__file__).resolve().parents[2];cccl=Path('/home/lktr/src/cccl')
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False);(out/'build').mkdir()
(out/'.gitattributes').write_text('* -text\n')
src=root/'evidence/phase2/binary_search_bounded_bench.cu';binary=out/'build/bench'
capture=lambda a:subprocess.check_output(a,timeout=10).decode().strip()
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
m={'start':utc(),'completed':False,'steps':[],
 'head':capture(['git','-C',str(cccl),'rev-parse','HEAD']),
 'status_before':capture(['git','-C',str(cccl),'status','--porcelain']),
 'hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
 [src,src.with_name('binary_search_bounded.cuh'),src.with_name('binary_search_11412.cu'),Path(__file__)]}}
save=lambda:(out/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
def run(label,cmd,limit=60):
    step={'label':label,'command':cmd,'utc_start':utc()};m['steps'].append(step);save();t=time.monotonic()
    with (out/(label+'.stdout.log')).open('wb') as a,(out/(label+'.stderr.log')).open('wb') as b:
        p=subprocess.run(cmd,stdout=a,stderr=b,timeout=limit)
    step.update(returncode=p.returncode,elapsed_s=time.monotonic()-t);save()
    print(label,p.returncode,flush=True);assert p.returncode==0
monitor=None
try:
    assert m['head']=='f747ef146b77ed1e8f38fe8cb3c67effaf7793f2' and not m['status_before']
    run('compile',['/usr/local/cuda/bin/nvcc','-O3','-std=c++17','-arch=sm_89','--ptxas-options=-v',
       '-I'+str(cccl/'libcudacxx/include'),str(src),'-o',str(binary)],120)
    run('check',[str(binary),'--check','20000'])
    assert 'PASS queries=180000 blocks=36864 timed=0' in (out/'check.stdout.log').read_text()
    run('sass',['/usr/local/cuda/bin/cuobjdump','--dump-sass',str(binary)])
    with (out/'gpu.csv').open('wb') as gpu,(out/'gpu.stderr.log').open('wb') as err:
        monitor=subprocess.Popen(['/usr/lib/wsl/lib/nvidia-smi','--query-gpu=timestamp,pstate,temperature.gpu,utilization.gpu,power.draw,clocks.sm,clocks.mem','--format=csv','-lms','200'],stdout=gpu,stderr=err)
        run('preheat',[str(binary),'--measure','20000'],120)
        run('measure',[str(binary),'--measure','20000'],120)
    content=(out/'measure.stdout.log').read_text()
    assert 'PASS queries=180000 blocks=221184 timed=1' in content
    groups={}
    for s,r,v,i,ms in re.findall(r'SAMPLE shape=(\d+) round=(\d+) variant=(\d+) sample=(\d+) ms=([\d.]+)',content):
        groups.setdefault((int(s),int(r),int(v)),[]).append(float(ms))
    assert len(groups)==27 and all(len(x)==30 for x in groups.values())
    rows=[dict(shape=s,round=r,variant=v,median_ms=statistics.median(g),min_ms=min(g),max_ms=max(g)) for (s,r,v),g in sorted(groups.items())]
    (out/'summary.json').write_text(json.dumps(rows,indent=2)+'\n')
    m['binary_sha256']=hashlib.sha256(binary.read_bytes()).hexdigest()
    m['status_after']=capture(['git','-C',str(cccl),'status','--porcelain']);assert not m['status_after']
    m['completed']=True;print(json.dumps(rows),flush=True)
except Exception as e:m['error']=repr(e);raise
finally:
    if monitor is not None:
        monitor.terminate()
        try:monitor.wait(timeout=5)
        except subprocess.TimeoutExpired:monitor.kill();monitor.wait()
    save()
