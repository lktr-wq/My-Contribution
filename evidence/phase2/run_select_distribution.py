#!/usr/bin/env python3
"""Bounded stock-CUB screening, run inside CCCL-Ubuntu. No dependency downloads."""
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
source=root/'evidence/phase2/select_distribution.cu'
binary=out/'build/select_distribution'
sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
manifest={'utc_start':dt.datetime.now(dt.timezone.utc).isoformat(),
  'scope':'Stock I32/I64 out-of-place DeviceSelect::Flagged, U8 flags, exactly 50 percent selected; baseline screening only',
  'gate':'For a size and pattern versus alternating, absolute median delta >=20 percent in all 3 rounds with the same sign; paired mean SM clock difference <=2 percent; all checks pass; <=1 percent discarded attempts per state. Not an optimization gain.',
  'source_sha256':sha(source),'head':capture(['git','-C',str(CCCL),'rev-parse','HEAD']).strip(),
  'upstream_status':capture(['git','-C',str(CCCL),'status','--porcelain']),
  'nvbench_lib_sha256':sha(BUILD/'lib/libnvbench.so'),'steps':[], 'runs':[], 'completed':False}
save=lambda: (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
save()
env=dict(os.environ,LD_LIBRARY_PATH=f'{BUILD}/lib:/usr/lib/wsl/lib:/usr/local/cuda/lib64',CCCL_EXPERIMENTAL_LOGGING='0')
def execute(label,args,timeout):
    entry={'label':label,'command':args}
    manifest['steps'].append(entry)
    save()
    start=time.monotonic()
    with (out/(label+'.stdout.log')).open('wb') as a,(out/(label+'.stderr.log')).open('wb') as b:
        p=subprocess.run(args,cwd=BUILD,env=env,stdout=a,stderr=b,timeout=timeout)
    entry.update(returncode=p.returncode,elapsed_s=time.monotonic()-start)
    save()
    print(f'{label}: exit={p.returncode}, {entry["elapsed_s"]:.2f}s',flush=True)
    if p.returncode: raise RuntimeError(f'{label} failed; see logs')
try:
    assert manifest['head']==HEAD and not manifest['upstream_status'].strip()
    prior=json.loads((root/'evidence/raw/phase2/2026-09-05-fixed-input-reduce-v2/manifest.json').read_text())
    oldsource=prior['source']
    oldobject=prior['steps'][0]['command'][-1]
    oldbinary=prior['steps'][1]['command'][prior['steps'][1]['command'].index('-o')+1]
    mapping={oldsource:str(source),oldobject:str(binary.with_suffix('.o')),oldbinary:str(binary)}
    for step in prior['steps'][:2]:
        execute(step['label'],[mapping.get(x,x) for x in step['command']],180)
    manifest['binary_sha256']=sha(binary)
    for index,order in enumerate([[0,1,2,3,4,5],[5,4,3,2,1,0],[2,0,1,4,5,3]],1):
        label=f'round{index}'
        entry={'round':index,'order':order,'power_before':capture(POWER)}
        assert TURBO in entry['power_before'].replace('\x00','')
        manifest['runs'].append(entry)
        args=[str(binary),'-d','0','-a','Case=['+','.join(map(str,order))+']',
          '--stopping-criterion','sample-count','--target-samples','1000','--cold-warmup-runs','20',
          '--timeout','15','--json',str(out/(label+'.json')),'--md',str(out/(label+'.md'))]
        execute(label,args,100)
        entry['power_after']=capture(POWER)
        assert TURBO in entry['power_after'].replace('\x00','')
        logs='\n'.join((out/(label+ext)).read_text(errors='replace') for ext in ['.stdout.log','.stderr.log'])
        checks=re.findall(r'CHECK Case=(\d+) N=(\d+) pattern=(\d+) selected=(\d+) before=PASS after=PASS guards=PASS',logs)
        assert [int(x[0]) for x in checks]==order
        discarded={x:0 for x in order}
        current=None
        for line in logs.splitlines():
            match=re.search(r'Run:.*Case=(\d+)',line)
            if match: current=int(match[1])
            if 'Warn:' in line:
                assert current is not None and line.startswith('Warn: GPU throttled below threshold') and 'Discarding previous trial' in line
                discarded[current]+=1
            assert 'Error:' not in line
        rows=records(out/(label+'.json'))
        assert len(rows)==6 and all(r['samples']==1000 and not r['at_timeout_boundary'] for r in rows)
        assert all(d/(1000+d)<=.01 for d in discarded.values())
        doc=json.loads((out/(label+'.json')).read_text())
        freq={}
        for bench in doc['benchmarks']:
            for state in bench['states']:
                code=int(next(a['value'] for a in state['axis_values'] if a['name']=='Case'))
                summary=next(s for s in state['summaries'] if s['tag']=='nv/cold/sm_clock_rate/mean')
                freq[code]=float(next(d['value'] for d in summary['data'] if d['name']=='value'))
        entry.update(rows=rows,checks=checks,discarded=discarded,mean_sm_clock=freq)
        save()
    manifest['comparisons']=[]
    for base in [0,3]:
        for variant in [base+1,base+2]:
            deltas=[]; clocks=[]
            for run in manifest['runs']:
                bycase={int(r['axes']['Case']):r for r in run['rows']}
                deltas.append(100*(bycase[variant]['median_s']/bycase[base]['median_s']-1))
                clocks.append(100*(run['mean_sm_clock'][variant]/run['mean_sm_clock'][base]-1))
            manifest['comparisons'].append({'base_case':base,'variant_case':variant,'delta_pct':deltas,
              'paired_median_delta_pct':statistics.median(deltas),'clock_delta_pct':clocks,
              'screen_gate_passed':(all(x>=20 for x in deltas) or all(x<=-20 for x in deltas)) and all(abs(x)<=2 for x in clocks)})
    manifest['upstream_status_after']=capture(['git','-C',str(CCCL),'status','--porcelain'])
    assert not manifest['upstream_status_after'].strip()
    manifest['completed']=True
    save()
    print(json.dumps(manifest['comparisons'],indent=2),flush=True)
except Exception as error:
    manifest['failure']=repr(error)
    save()
    raise
