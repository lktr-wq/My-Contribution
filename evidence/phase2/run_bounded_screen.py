#!/usr/bin/env python3
import datetime,hashlib,json,re,statistics,subprocess,sys,time
from pathlib import Path
root=Path(__file__).resolve().parents[2];cccl=Path('/home/lktr/src/cccl')
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False);(out/'build').mkdir();(out/'.gitattributes').write_text('* -text\n')
src=root/'evidence/phase2/binary_search_bounded_screen.cu';binary=out/'build/screen'
capture=lambda a:subprocess.check_output(a,timeout=10).decode().strip()
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
m={'start':utc(),'completed':False,'steps':[],'head':capture(['git','-C',str(cccl),'rev-parse','HEAD']),
 'status_before':capture(['git','-C',str(cccl),'status','--porcelain']),
 'hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [src,src.with_name('binary_search_bounded.cuh'),src.with_name('binary_search_bounded_bench.cu'),Path(__file__)]}}
save=lambda:(out/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
def run(label,cmd,limit=120):
    e={'label':label,'command':cmd,'utc_start':utc()};m['steps'].append(e);save();t=time.monotonic()
    with (out/(label+'.stdout.log')).open('wb') as a,(out/(label+'.stderr.log')).open('wb') as b:p=subprocess.run(cmd,stdout=a,stderr=b,timeout=limit)
    e.update(returncode=p.returncode,elapsed_s=time.monotonic()-t);save();print(label,p.returncode,flush=True);assert p.returncode==0
monitor=None
try:
    assert m['head']=='f747ef146b77ed1e8f38fe8cb3c67effaf7793f2' and not m['status_before']
    run('compile',['/usr/local/cuda/bin/nvcc','-O3','-std=c++17','-arch=sm_89','--ptxas-options=-v','-I'+str(cccl/'libcudacxx/include'),str(src),'-o',str(binary)])
    run('check',[str(binary),'--check'],60)
    assert 'PASS queries=172032 blocks=21504 timed=0' in (out/'check.stdout.log').read_text()
    with (out/'gpu.csv').open('wb') as gpu,(out/'gpu.stderr.log').open('wb') as err:
        monitor=subprocess.Popen(['/usr/lib/wsl/lib/nvidia-smi','--query-gpu=timestamp,pstate,temperature.gpu,utilization.gpu,power.draw,clocks.sm,clocks.mem','--format=csv','-lms','200'],stdout=gpu,stderr=err)
        run('preheat',[str(binary),'--measure'])
        run('measure',[str(binary),'--measure'])
    content=(out/'measure.stdout.log').read_text();assert 'PASS queries=172032 blocks=129024 timed=1' in content
    groups={}
    for n,s,r,v,i,ms in re.findall(r'SAMPLE n=(\d+) shape=(\d+) round=(\d+) variant=(\d+) sample=(\d+) ms=([\d.]+)',content):
        groups.setdefault(tuple(map(int,(n,s,r,v))),[]).append(float(ms))
    assert len(groups)==126 and all(len(x)==30 for x in groups.values())
    rows=[dict(n=n,shape=s,round=r,variant=v,median_ms=statistics.median(g),min_ms=min(g),max_ms=max(g)) for (n,s,r,v),g in sorted(groups.items())]
    (out/'rounds.json').write_text(json.dumps(rows,indent=2)+'\n')
    cells=[]
    for n in [1,8,32,257,4096,20000,65536]:
      for s in range(2):
        med=[statistics.median([x['median_ms'] for x in rows if (x['n'],x['shape'],x['variant'])==(n,s,v)]) for v in range(3)]
        paired=[100*(1-statistics.median(groups[n,s,r,2])/statistics.median(groups[n,s,r,0])) for r in range(3)]
        cells.append(dict(n=n,shape=s,official_ms=med[0],clone_ms=med[1],guarded_ms=med[2],reduction_percent=100*(1-med[2]/med[0]),paired_reductions=paired))
    (out/'summary.json').write_text(json.dumps(cells,indent=2)+'\n');print(json.dumps(cells),flush=True)
    m['binary_sha256']=hashlib.sha256(binary.read_bytes()).hexdigest()
    m['status_after']=capture(['git','-C',str(cccl),'status','--porcelain']);assert not m['status_after'];m['completed']=True
except Exception as e:m['error']=repr(e);raise
finally:
    if monitor is not None:
        monitor.terminate()
        try:monitor.wait(timeout=5)
        except subprocess.TimeoutExpired:monitor.kill();monitor.wait()
    save()
