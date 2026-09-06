#!/usr/bin/env python3
"""One six-round batch with NVBench's normal low-frequency sample rejection.
Protocol revision: occasional rejected trials do not invalidate the whole process.
The binary, thresholds, target samples, warmups, and effect gate are unchanged.
"""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import random
import re
import statistics
import subprocess
import sys
import time
from audit_reduce_measurements import records
from probe_reduce_boundaries import BUILD, CCCL, HEAD, POWER, TURBO, capture

root = Path(__file__).resolve().parents[2]
prepared = root/'evidence/raw/phase2/2026-09-06-tail-ab-v2'
prior = json.loads((prepared/'manifest.json').read_text())
binary = prepared/'build/tail_ab'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert prior['prepared'] and sha(binary) == prior['binary_sha256']
assert capture(['git','-C',str(CCCL),'rev-parse','HEAD']).strip() == HEAD
assert capture(['git','-C',str(CCCL),'status','--porcelain']).strip() == ''
for path,digest in prior['source_sha256'].items():
    assert sha(root/path) == digest
assert sha(BUILD/'lib/libnvbench.so') == prior['nvbench_lib_sha256']
out = Path(sys.argv[1]).resolve()
out.mkdir(parents=True,exist_ok=False)
(out/'.gitattributes').write_text('* -text\n')
manifest = {'utc_start':dt.datetime.now(dt.timezone.utc).isoformat(),'binary':str(binary),
 'binary_sha256':sha(binary),'preparation_manifest':str(prepared/'manifest.json'),
 'preparation_manifest_sha256':sha(prepared/'manifest.json'), 'memcheck_status':prior['memcheck_status'],
 'protocol_revision':'Keep default 75% throttle threshold and NVBench rejected-trial handling. Admit <=1% rejected attempts per state. Flag the whole batch inconclusive if any paired accepted-sample mean frequency differs by >2%. Six rounds only; no automatic repeat.',
 'decision_rule':prior['decision_rule'],'runs':[],'pairs':[],'completed':False}
save = lambda: (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
save()
env = dict(os.environ,LD_LIBRARY_PATH=f'{BUILD}/lib:/usr/lib/wsl/lib:/usr/local/cuda/lib64',CCCL_EXPERIMENTAL_LOGGING='0')
sizes = prior['sizes']
try:
    for round_index in range(6):
        order = list(range(7))
        random.Random(6400+round_index).shuffle(order)
        variants = [0,1] if round_index%2==0 else [1,0]
        codes = [2*i+v for i in order for v in variants]
        label = f'round{round_index+1}'
        args = [str(binary),'-d','0','-a','Case=['+','.join(map(str,codes))+']',
                '--stopping-criterion','sample-count','--target-samples','1000','--cold-warmup-runs','20',
                '--timeout','15','--json',str(out/(label+'.json')),'--md',str(out/(label+'.md'))]
        entry = {'round':round_index+1,'command':args,'case_order':codes,'power_before':capture(POWER)}
        manifest['runs'].append(entry)
        assert TURBO in entry['power_before'].replace('\x00','')
        entry['gpu_before'] = capture(['/usr/lib/wsl/lib/nvidia-smi','--query-gpu=temperature.gpu,power.draw,clocks.sm,utilization.gpu','--format=csv'])
        save()
        start = time.monotonic()
        with (out/(label+'.stdout.log')).open('wb') as stdout, (out/(label+'.stderr.log')).open('wb') as stderr:
            p = subprocess.run(args,cwd=BUILD,env=env,stdout=stdout,stderr=stderr,timeout=120)
        entry.update(returncode=p.returncode,elapsed_s=time.monotonic()-start,power_after=capture(POWER))
        entry['gpu_after'] = capture(['/usr/lib/wsl/lib/nvidia-smi','--query-gpu=temperature.gpu,power.draw,clocks.sm,utilization.gpu','--format=csv'])
        save()
        assert p.returncode==0 and TURBO in entry['power_after'].replace('\x00','')
        logs = (out/(label+'.stdout.log')).read_text(errors='replace')+'\n'+(out/(label+'.stderr.log')).read_text(errors='replace')
        current = None
        discarded = {code:0 for code in codes}
        warnings = []
        for line in logs.splitlines():
            match = re.search(r'Run:.*Case=(\d+)',line)
            if match: current=int(match[1])
            if 'Warn:' in line:
                warnings.append({'case':current,'text':line})
                assert current is not None and line.startswith('Warn: GPU throttled below threshold') and 'Discarding previous trial' in line
                discarded[current]+=1
            assert 'Error:' not in line and 'deadlock' not in line.lower()
        checks = re.findall(r'CHECK Case=(\d+) N=(\d+) variant=(\d+) before=(-?\d+) after=(-?\d+) input=(\S+) output=(\S+) scratch=(\S+) stream=(\S+)',logs)
        assert [int(c[0]) for c in checks]==codes and all(c[3]==c[4] for c in checks)
        assert len({tuple(c[5:]) for c in checks})==1
        rows=records(out/(label+'.json'))
        assert len(rows)==14 and all(r['samples']==1000 and not r['at_timeout_boundary'] for r in rows)
        doc=json.loads((out/(label+'.json')).read_text())
        freqs={}
        for bench in doc['benchmarks']:
            for state in bench['states']:
                code=int(next(a['value'] for a in state['axis_values'] if a['name']=='Case'))
                summary=next(s for s in state['summaries'] if s['tag']=='nv/cold/sm_clock_rate/mean')
                freqs[code]=float(next(d['value'] for d in summary['data'] if d['name']=='value'))
        entry.update(warnings=warnings,discarded_by_case=discarded,rows=rows,checks=checks,accepted_mean_clock_hz=freqs)
        save()
        assert all(d/(1000+d)<=.01 for d in discarded.values()), 'Too many discarded trials'
        by_case={int(r['axes']['Case']):r for r in rows}
        for i,n in enumerate(sizes):
            a,b=by_case[2*i],by_case[2*i+1]
            manifest['pairs'].append({'round':round_index+1,'n':n,
                'baseline_median_us':a['median_s']*1e6,'variant_median_us':b['median_s']*1e6,
                'delta_pct':(b['median_s']/a['median_s']-1)*100,
                'baseline_mean_us':a['mean_s']*1e6,'variant_mean_us':b['mean_s']*1e6,
                'clock_delta_pct':(freqs[2*i+1]/freqs[2*i]-1)*100,
                'baseline_discards':discarded[2*i],'variant_discards':discarded[2*i+1]})
        save()
        print(f'{label}: {entry["elapsed_s"]:.2f}s, 14 x 1000 accepted, {sum(discarded.values())} discarded trials',flush=True)
    manifest['summary']=[]
    for n in sizes:
        pairs=[p for p in manifest['pairs'] if p['n']==n]
        ds=[p['delta_pct'] for p in pairs]
        manifest['summary'].append({'n':n,'baseline_median_of_medians_us':statistics.median(p['baseline_median_us'] for p in pairs),
            'variant_median_of_medians_us':statistics.median(p['variant_median_us'] for p in pairs),
            'paired_median_delta_pct':statistics.median(ds),'faster_rounds':sum(d<0 for d in ds),'deltas_pct':ds})
    target=next(s for s in manifest['summary'] if s['n']==720*4096-1)
    controls=[s for s in manifest['summary'] if s['n'] in [720*4096-4096,720*4096]]
    manifest['frequency_gate_passed']=all(abs(p['clock_delta_pct'])<=2 for p in manifest['pairs'])
    manifest['effect_gate_passed']=target['faster_rounds']>=5 and target['paired_median_delta_pct']<=-2 and all(s['paired_median_delta_pct']<=2 for s in controls)
    manifest['exploratory_gate_passed']=manifest['frequency_gate_passed'] and manifest['effect_gate_passed']
    manifest['upstream_status_after']=capture(['git','-C',str(CCCL),'status','--porcelain'])
    assert not manifest['upstream_status_after'].strip()
    manifest['completed']=True
    save()
    print(json.dumps(manifest['summary'],indent=2),flush=True)
except Exception as error:
    manifest['failure']=repr(error)
    save()
    raise
