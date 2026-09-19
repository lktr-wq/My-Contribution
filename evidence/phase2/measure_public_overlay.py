#!/usr/bin/env python3
import datetime,difflib,hashlib,json,re,statistics,subprocess,sys,time
from pathlib import Path
root=Path(__file__).resolve().parents[2];cccl=Path('/home/lktr/src/cccl');phase=root/'evidence/phase2'
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False);(out/'build').mkdir();(out/'.gitattributes').write_text('* -text\n')
overlay=phase/'bounded_overlay';header=Path('cuda/std/__algorithm/lower_bound.h');src=phase/'binary_search_bounded_single.cu'
capture=lambda a:subprocess.check_output(a,timeout=10).decode().strip()
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
m={'start':utc(),'completed':False,'steps':[],'head':capture(['git','-C',str(cccl),'rev-parse','HEAD']),
 'status_before':capture(['git','-C',str(cccl),'status','--porcelain']),
 'hashes':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [src,overlay/header,phase/'binary_search_bounded.cuh',phase/'binary_search_bounded_bench.cu',Path(__file__)]}}
save=lambda:(out/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
def run(label,args,limit=60):
    e={'label':label,'command':args,'utc_start':utc()};m['steps'].append(e);save();t=time.monotonic()
    with (out/(label+'.stdout.log')).open('wb') as a,(out/(label+'.stderr.log')).open('wb') as b:p=subprocess.run(args,stdout=a,stderr=b,timeout=limit)
    e.update(returncode=p.returncode,elapsed_s=time.monotonic()-t);save();print(label,p.returncode,flush=True);assert p.returncode==0
monitor=None
try:
    assert m['head']=='f747ef146b77ed1e8f38fe8cb3c67effaf7793f2' and not m['status_before']
    original=(cccl/'libcudacxx/include'/header).read_text();changed=(overlay/header).read_text()
    (out/'overlay.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True),changed.splitlines(True),fromfile='a/libcudacxx/include/'+str(header),tofile='b/libcudacxx/include/'+str(header))))
    for mode in ['baseline','overlay']:
        args=['/usr/local/cuda/bin/nvcc','-O3','-std=c++17','-arch=sm_89','--ptxas-options=-v','-DPUBLIC_API_ONLY']
        if mode=='overlay':args+=['-I'+str(overlay)]
        args+=['-I'+str(cccl/'libcudacxx/include')]
        run(mode+'-dependencies',args+['-M',str(src)])
        expected=overlay/header if mode=='overlay' else cccl/'libcudacxx/include'/header
        assert str(expected) in (out/(mode+'-dependencies.stdout.log')).read_text().replace('\\ ',' ')
        run(mode+'-compile',args+[str(src),'-o',str(out/'build'/mode)],120)
        run(mode+'-check',[str(out/'build'/mode),'--check'])
        assert 'PASS queries=33554432 timed=0' in (out/(mode+'-check.stdout.log')).read_text()
        run(mode+'-sass',['/usr/local/cuda/bin/cuobjdump','--dump-sass',str(out/'build'/mode)])
    with (out/'gpu.csv').open('wb') as gpu,(out/'gpu.stderr.log').open('wb') as err:
        monitor=subprocess.Popen(['/usr/lib/wsl/lib/nvidia-smi','--query-gpu=timestamp,pstate,temperature.gpu,utilization.gpu,power.draw,clocks.sm,clocks.mem','--format=csv','-lms','200'],stdout=gpu,stderr=err)
        for mode in ['baseline','overlay']:run(mode+'-preheat',[str(out/'build'/mode),'--measure'])
        for r in range(3):
            for mode in (['baseline','overlay'] if r%2==0 else ['overlay','baseline']):
                run(f'{mode}-round{r}',[str(out/'build'/mode),'--measure'])
    monitor.terminate();monitor.wait(timeout=5);monitor=None
    med={};rounds=[]
    for r in range(3):
      for mode in ['baseline','overlay']:
        text=(out/f'{mode}-round{r}.stdout.log').read_text();assert 'PASS queries=67108864 timed=1' in text
        groups={}
        for n,s,rr,v,i,ms in re.findall(r'SAMPLE n=(\d+) shape=(\d+) round=(\d+) variant=(\d+) sample=(\d+) ms=([\d.]+)',text):
            assert rr=='0' and v=='0';groups.setdefault((int(n),int(s)),[]).append(float(ms))
        assert len(groups)==8 and all(len(x)==30 for x in groups.values())
        for (n,s),vals in groups.items():
            med[mode,r,n,s]=statistics.median(vals);rounds.append(dict(mode=mode,round=r,n=n,shape=s,median_ms=med[mode,r,n,s],min_ms=min(vals),max_ms=max(vals)))
    rows=[]
    for n in [32,4096,20000,65536]:
      for s in range(2):
        a=statistics.median(med['baseline',r,n,s] for r in range(3));b=statistics.median(med['overlay',r,n,s] for r in range(3))
        rows.append(dict(n=n,shape=s,baseline_ms=a,overlay_ms=b,reduction_percent=100*(1-b/a),paired=[100*(1-med['overlay',r,n,s]/med['baseline',r,n,s]) for r in range(3)]))
    (out/'rounds.json').write_text(json.dumps(rounds,indent=2)+'\n');(out/'summary.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows),flush=True)
    m['binary_hashes']={mode:hashlib.sha256((out/'build'/mode).read_bytes()).hexdigest() for mode in ['baseline','overlay']}
    m['status_after']=capture(['git','-C',str(cccl),'status','--porcelain']);assert not m['status_after'];m['completed']=True
except Exception as e:m['error']=repr(e);raise
finally:
    if monitor is not None:
        monitor.terminate()
        try:monitor.wait(timeout=5)
        except subprocess.TimeoutExpired:monitor.kill();monitor.wait()
    save()
