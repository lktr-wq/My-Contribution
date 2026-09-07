#!/usr/bin/env python3
"""Stock scan baseline; new output directory required, bounded execution."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import statistics
import subprocess
import sys
import time
from audit_reduce_measurements import records
from probe_reduce_boundaries import BUILD, CCCL, HEAD, POWER, TURBO, capture

root=Path(__file__).resolve().parents[2]
out=Path(sys.argv[1]).resolve()
out.mkdir(parents=True,exist_ok=False)
(out/'build').mkdir()
(out/'.gitattributes').write_text('* -text\n')
source=root/'evidence/phase2/scan_boundaries.cu'
binary=out/'build/scan_boundaries'
sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
sizes=[1919,1920,1921,46079,46080,46081,245759,245760,245761]
m={'utc_start':dt.datetime.now(dt.timezone.utc).isoformat(),'scope':'Stock ExclusiveSum I32/I64, three tile-count boundaries, not optimization A/B',
   'gate':'N+1 versus N at each center: >=20% same-direction increase in all 3 rounds; paired mean SM clocks differ <=2%; <=1% discarded attempts per state; checks pass. This is candidate screening, not a bug proof.',
   'source_sha256':sha(source),'driver_sha256':sha(Path(__file__)),
   'head':capture(['git','-C',str(CCCL),'rev-parse','HEAD']).strip(),
   'upstream_status':capture(['git','-C',str(CCCL),'status','--porcelain']),
   'nvbench_lib_sha256':sha(BUILD/'lib/libnvbench.so'),'steps':[],'runs':[],'completed':False}
save=lambda: (out/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
env=dict(os.environ,LD_LIBRARY_PATH=f'{BUILD}/lib:/usr/lib/wsl/lib:/usr/local/cuda/lib64',CCCL_EXPERIMENTAL_LOGGING='0')
def execute(label,args,timeout,logging=False):
    entry={'label':label,'command':args,'logging':logging};m['steps'].append(entry);save()
    start=time.monotonic()
    with (out/(label+'.stdout.log')).open('wb') as a,(out/(label+'.stderr.log')).open('wb') as b:
        p=subprocess.run(args,cwd=BUILD,env=dict(env,CCCL_EXPERIMENTAL_LOGGING='1' if logging else '0'),stdout=a,stderr=b,timeout=timeout)
    entry.update(returncode=p.returncode,elapsed_s=time.monotonic()-start);save()
    print(f'{label}: exit={p.returncode}, {entry["elapsed_s"]:.2f}s',flush=True)
    if p.returncode: raise RuntimeError(f'{label} failed; see logs')
try:
    assert m['head']==HEAD and not m['upstream_status'].strip()
    prior=json.loads((root/'evidence/raw/phase2/2026-09-05-fixed-input-reduce-v2/manifest.json').read_text())
    oldbinary=prior['steps'][1]['command'][prior['steps'][1]['command'].index('-o')+1]
    mapping={prior['source']:str(source),prior['steps'][0]['command'][-1]:str(binary.with_suffix('.o')),oldbinary:str(binary)}
    for step in prior['steps'][:2]:
        execute(step['label'],[mapping.get(x,x) for x in step['command']],180)
    m['binary_sha256']=sha(binary)
    assert TURBO in capture(POWER).replace('\x00','')
    # Logging/profile run checks launch path only; no times enter performance summaries.
    execute('path',[str(binary),'-d','0','-a','N=[1920,1921,245760,245761]','--profile'],40,True)
    orders=[sizes,list(reversed(sizes)),sizes[3:6]+sizes[:3]+sizes[6:]]
    for index,order in enumerate(orders,1):
        label=f'round{index}';entry={'round':index,'order':order,'power_before':capture(POWER)}
        assert TURBO in entry['power_before'].replace('\x00','')
        m['runs'].append(entry)
        args=[str(binary),'-d','0','-a','N=['+','.join(map(str,order))+']','--stopping-criterion','sample-count',
          '--target-samples','1000','--cold-warmup-runs','20','--timeout','15','--json',str(out/(label+'.json')),'--md',str(out/(label+'.md'))]
        execute(label,args,100)
        entry['power_after']=capture(POWER)
        assert TURBO in entry['power_after'].replace('\x00','')
        logs='\n'.join((out/(label+x)).read_text(errors='replace') for x in ['.stdout.log','.stderr.log'])
        checks=re.findall(r'CHECK N=(\d+) before=PASS after=PASS guards=PASS',logs)
        assert list(map(int,checks))==order
        discarded={n:0 for n in order};current=None
        for line in logs.splitlines():
            match=re.search(r'Run:.*N=(\d+)',line)
            if match:current=int(match[1])
            if 'Warn:' in line:
                assert current is not None and line.startswith('Warn: GPU throttled below threshold') and 'Discarding previous trial' in line
                discarded[current]+=1
            assert 'Error:' not in line
        rows=records(out/(label+'.json'))
        assert len(rows)==9 and all(r['samples']==1000 and not r['at_timeout_boundary'] for r in rows)
        assert all(d/(1000+d)<=.01 for d in discarded.values())
        doc=json.loads((out/(label+'.json')).read_text());freq={}
        for bench in doc['benchmarks']:
            for state in bench['states']:
                n=int(next(a['value'] for a in state['axis_values'] if a['name']=='N'))
                summary=next(s for s in state['summaries'] if s['tag']=='nv/cold/sm_clock_rate/mean')
                freq[n]=float(next(d['value'] for d in summary['data'] if d['name']=='value'))
        entry.update(rows=rows,checks=checks,discarded=discarded,mean_sm_clock=freq);save()
    m['comparisons']=[]
    for center in [1920,46080,245760]:
        deltas=[];clocks=[]
        for run in m['runs']:
            byn={int(r['axes']['N']):r for r in run['rows']}
            deltas.append(100*(byn[center+1]['median_s']/byn[center]['median_s']-1))
            clocks.append(100*(run['mean_sm_clock'][center+1]/run['mean_sm_clock'][center]-1))
        m['comparisons'].append({'center':center,'delta_pct':deltas,'paired_median_delta_pct':statistics.median(deltas),
           'clock_delta_pct':clocks,'screen_gate_passed':all(x>=20 for x in deltas) and all(abs(x)<=2 for x in clocks)})
    m['upstream_status_after']=capture(['git','-C',str(CCCL),'status','--porcelain'])
    assert not m['upstream_status_after'].strip()
    m['completed']=True;save();print(json.dumps(m['comparisons'],indent=2),flush=True)
except Exception as error:
    m['failure']=repr(error);save();raise
