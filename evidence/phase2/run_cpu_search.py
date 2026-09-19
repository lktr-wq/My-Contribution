import subprocess,json,statistics,sys,os,time,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False);(out/'build').mkdir()
(out/'.gitattributes').write_text('* -text\n');cccl=Path('/home/lktr/src/cccl');src=root/'evidence/phase2/cpu_search.cpp'
cpu=min(os.sched_getaffinity(0));m={'cpu_affinity':cpu,'steps':[],'completed':False}
def run(label,args):
    t=time.monotonic();p=subprocess.run(args,capture_output=True,text=True,timeout=60)
    (out/(label+'.stdout.log')).write_text(p.stdout);(out/(label+'.stderr.log')).write_text(p.stderr)
    m['steps'].append(dict(label=label,args=args,returncode=p.returncode,seconds=time.monotonic()-t));assert p.returncode==0,p.stderr
    print(label,flush=True);return p.stdout
try:
    m['head']=run('head',['git','-C',str(cccl),'rev-parse','HEAD']).strip()
    assert m['head']=='f747ef146b77ed1e8f38fe8cb3c67effaf7793f2'
    assert not run('status-before',['git','-C',str(cccl),'status','--porcelain']).strip()
    run('compiler',['g++','--version']);run('cpu',['lscpu'])
    m['source_sha256']=hashlib.sha256(src.read_bytes()).hexdigest()
    for mode in ['baseline','overlay']:
        args=['g++','-O3','-std=c++17','-fno-lto']
        if mode=='overlay':args+=['-I'+str(root/'evidence/phase2/bounded_overlay')]
        args+=['-I'+str(cccl/'libcudacxx/include')]
        deps=run(mode+'-dependencies',args+['-M',str(src)])
        assert ('bounded_overlay/cuda/std/__algorithm/lower_bound.h' in deps)==(mode=='overlay')
        run(mode+'-compile',args+[str(src),'-o',str(out/'build'/mode)])
    data={}
    for r in range(5):
      for mode in (['baseline','overlay'] if r%2==0 else ['overlay','baseline']):
        text=run(f'{mode}-{r}',['taskset','-c',str(cpu),str(out/'build'/mode)])
        assert 'PASS per-query oracle and timed totals' in text
        groups={}
        for line in text.splitlines():
          if line.startswith('SAMPLE '):
            _,n,s,i,ns=line.split();groups.setdefault((int(n),int(s)),[]).append(float(ns))
        assert len(groups)==12 and all(len(v)==9 for v in groups.values())
        for key,v in groups.items():data[mode,r,*key]=statistics.median(v)
    rows=[]
    for n in [1,32,257,4096,20000,65536]:
      for s in range(2):
        a=statistics.median(data['baseline',r,n,s] for r in range(5));b=statistics.median(data['overlay',r,n,s] for r in range(5))
        rows.append(dict(n=n,shape=s,baseline_ns=a,overlay_ns=b,slowdown_percent=100*(b/a-1),paired_slowdowns=[100*(data['overlay',r,n,s]/data['baseline',r,n,s]-1) for r in range(5)]))
    (out/'summary.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows))
    assert not run('status-after',['git','-C',str(cccl),'status','--porcelain']).strip();m['completed']=True
finally:(out/'manifest.json').write_text(json.dumps(m,indent=2))
