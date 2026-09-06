#!/usr/bin/env python3
"""Bounded local A/B: prepare (build, oracle, memcheck, SASS), then measure.
Reuses existing pinned compiler/linker flags and dependencies; no network/install.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import random
import re
import statistics
import subprocess
import time

from audit_reduce_measurements import records
from probe_reduce_boundaries import BUILD, CCCL, HEAD, POWER, TURBO, capture

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(__file__).resolve().parent
SIZES = [720*4096+d for d in [-4096,-2048,-32,-4,-1,0,1]]
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def run(out, stage, prepared_from=None):
    if stage == 'retest':
        assert prepared_from is not None
        previous = json.loads((prepared_from/'manifest.json').read_text())
        assert previous['prepared']
        out.mkdir(parents=True, exist_ok=False)
        manifest = {key:previous[key] for key in ['sizes','cccl_head','decision_rule','limits','source_sha256',
                    'nvbench_lib_sha256','compiler','binary_sha256','memcheck_status','target_static_vector_load_sites']}
        manifest.update(utc_start=dt.datetime.now(dt.timezone.utc).isoformat(),steps=[],prepared=True,
                        reused_binary=str(prepared_from/'build/tail_ab'),
                        preparation_manifest=str(prepared_from/'manifest.json'),
                        preparation_manifest_sha256=sha(prepared_from/'manifest.json'),
                        environmental_change='User confirmed wallpaper paused/exited after earlier clock warning; new six-round batch, no historical pooling.')
        (out/'.gitattributes').write_text('* -text\n')
    elif stage == 'prepare':
        out.mkdir(parents=True, exist_ok=False)
        (out/'build').mkdir()
        manifest = {'utc_start': dt.datetime.now(dt.timezone.utc).isoformat(), 'steps': [],
                    'sizes': SIZES, 'cccl_head': capture(['git','-C',str(CCCL),'rev-parse','HEAD']).strip(),
                    'decision_rule': 'Exploratory only: B-1 variant faster in >=5/6 rounds and median paired delta <= -2%; full-tile B-4096 and B median paired regressions <=2%. No significance claim.',
                    'limits': 'Each compile <=300 s; memcheck <=180 s; each measured process <=120 s; six rounds, no automatic retuning/repeats.'}
        (out/'.gitattributes').write_text('* -text\n')
    else:
        manifest = json.loads((out/'manifest.json').read_text())
        if (stage == 'measure' and not manifest.get('prepared')) or manifest.get('measurement_started'):
            raise RuntimeError('Preparation incomplete or measurement already attempted')
    def save():
        (out/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    assert manifest['cccl_head'] == HEAD
    assert capture(['git','-C',str(CCCL),'status','--porcelain']).strip() == ''
    save()
    env = dict(os.environ, LD_LIBRARY_PATH=f'{BUILD}/lib:/usr/lib/wsl/lib:/usr/local/cuda/lib64', CCCL_EXPERIMENTAL_LOGGING='0')
    def execute(label, args, timeout=120, gpu=False, trace=False):
        step = {'label': label, 'command': args, 'gpu': gpu, 'trace_only': trace}
        manifest['steps'].append(step)
        if gpu:
            step['power_before'] = capture(POWER)
            if TURBO not in step['power_before'].replace('\x00',''):
                save()
                raise RuntimeError('Turbo not active')
            step['gpu_before'] = capture(['/usr/lib/wsl/lib/nvidia-smi','--query-gpu=temperature.gpu,power.draw,clocks.sm,utilization.gpu','--format=csv'])
        save()
        start = time.monotonic()
        with (out/(label+'.stdout.log')).open('wb') as stdout, (out/(label+'.stderr.log')).open('wb') as stderr:
            try:
                p = subprocess.run(args, cwd=BUILD, env=dict(env, CCCL_EXPERIMENTAL_LOGGING='1' if trace else '0'),
                                   stdout=stdout, stderr=stderr, timeout=timeout)
                step['returncode'] = p.returncode
            except subprocess.TimeoutExpired:
                step['error'] = 'timeout; process killed by subprocess.run'
                save()
                raise
        step['elapsed_s'] = time.monotonic()-start
        logs = '\n'.join((out/(label+'.'+stream+'.log')).read_text(errors='replace') for stream in ['stdout','stderr'])
        step['warnings'] = [line for line in logs.splitlines() if any(s in line.lower() for s in ['warn:', 'error:', 'deadlock'])]
        if gpu:
            step['power_after'] = capture(POWER)
            step['gpu_after'] = capture(['/usr/lib/wsl/lib/nvidia-smi','--query-gpu=temperature.gpu,power.draw,clocks.sm,utilization.gpu','--format=csv'])
        save()
        print(f'{label}: {step["elapsed_s"]:.2f}s exit={p.returncode}', flush=True)
        if p.returncode or (gpu and TURBO not in step['power_after'].replace('\x00','')):
            raise RuntimeError(f'{label} failed; outputs preserved')
        return step, logs

    binary = Path(manifest.get('reused_binary',str(out/'build/tail_ab')))
    if stage == 'prepare':
        prior = json.loads((ROOT/'evidence/raw/phase2/2026-09-05-fixed-input-reduce-v2/manifest.json').read_text())
        original_compile = next(s['command'] for s in prior['steps'] if s['label']=='compile')
        original_link = next(s['command'] for s in prior['steps'] if s['label']=='link')
        files = [SOURCE/'tail_ab_api.h', SOURCE/'tail_ab_wrapper.cu', SOURCE/'tail_ab_bench.cu',
                 SOURCE/'tail_ab_overlay/tail_ab_partial.cuh', SOURCE/'tail_ab_overlay/cub/agent/agent_reduce.cuh']
        manifest['source_sha256'] = {str(f.relative_to(ROOT)):sha(f) for f in files}
        manifest['nvbench_lib_sha256'] = sha(BUILD/'lib/libnvbench.so')
        manifest['compiler'] = capture(['/usr/local/cuda/bin/nvcc','--version'])
        base_header = (CCCL/'cub/cub/agent/agent_reduce.cuh').read_text()
        overlay = (SOURCE/'tail_ab_overlay/cub/agent/agent_reduce.cuh').read_text()
        assert overlay.replace('#include <tail_ab_partial.cuh>\n','') == base_header
        objects = []
        for name, enabled in [('baseline',0),('vector',1),('bench',None)]:
            args = list(original_compile)
            obj = out/f'build/{name}.o'
            objects.append(str(obj))
            args[args.index('-c')+1] = str(SOURCE/('tail_ab_bench.cu' if enabled is None else 'tail_ab_wrapper.cu'))
            args[args.index('-o')+1] = str(obj)
            if enabled is not None:
                args[1:1] = [f'-I{SOURCE}/tail_ab_overlay',f'-DTAIL_AB_ENABLED={enabled}',
                             f'-DTHRUST_CUB_WRAPPED_NAMESPACE=tail_{name}',f'-DREDUCE_ENTRY=reduce_{name}']
            execute('compile-'+name,args,timeout=300)
        link = list(original_link)
        old_obj = next(i for i,a in enumerate(link) if a.endswith('fixed_input_reduce.o'))
        link[old_obj:old_obj+1] = objects
        link[link.index('-o')+1] = str(binary)
        execute('link',link)
        manifest['binary_sha256'] = sha(binary)
        _, logs = execute('correctness',[str(binary),'--check-only'],gpu=True)
        assert 'CORRECTNESS_PASS cases=896' in logs and len(re.findall(r'^ORACLE ',logs,re.M))==896
        try:
            _, logs = execute('memcheck',['/usr/local/cuda/bin/compute-sanitizer','--tool','memcheck','--error-exitcode','99',str(binary),'--check-only'],timeout=180,gpu=True)
            assert 'CORRECTNESS_PASS cases=896' in logs and 'ERROR SUMMARY: 0 errors' in logs
            manifest['memcheck_status'] = 'passed'
        except RuntimeError:
            logs = (out/'memcheck.stdout.log').read_text()
            errors = re.findall(r'^========= Error: (.*)$', logs, re.M)
            assert len(errors)==2 and errors[0].startswith('Failed to initialize WDDM debugger interface.') and errors[1].startswith('Device not supported.')
            assert manifest['steps'][-1]['returncode']==99 and 'CORRECTNESS_PASS cases=896' in logs and 'ERROR SUMMARY: 2 errors' in logs
            manifest['memcheck_status'] = 'unavailable: WDDM debugger interface; not a sanitizer pass'
            manifest['validation_scope_change'] = 'Exploratory timing only after GPU oracle and exhaustive host mapping; no upstream-ready safety claim.'
            execute('host-mapping',['python3','-B',str(SOURCE/'check_tail_ab_mapping.py'),str(out/'host-mapping-check.json')])
        save()

    if stage == 'resume-after-debugger-block':
        assert sha(binary) == manifest['binary_sha256']
        failed = next(s for s in manifest['steps'] if s['label']=='memcheck')
        assert failed['returncode'] == 99
        logs = (out/'memcheck.stdout.log').read_text()
        errors = re.findall(r'^========= Error: (.*)$', logs, re.M)
        assert len(errors)==2 and errors[0].startswith('Failed to initialize WDDM debugger interface.') and errors[1].startswith('Device not supported.')
        assert 'CORRECTNESS_PASS cases=896' in logs and 'ERROR SUMMARY: 2 errors' in logs
        mapping = json.loads((out/'host-mapping-check.json').read_text())
        assert mapping['eligible_lengths_checked']==3072 and mapping['each_valid_element_visited_exactly_once']
        manifest['memcheck_status'] = 'unavailable: WDDM debugger interface; not a sanitizer pass'
        manifest['validation_scope_change'] = 'Proceed only with exploratory performance after GPU oracle and host indexing check; no system changes or upstream-ready safety claim.'
        save()

    if stage in ['prepare','resume-after-debugger-block']:
        for name in ['baseline','vector']:
            execute('sass-'+name,['/usr/local/cuda/bin/cuobjdump','--dump-sass',str(out/f'build/{name}.o')])
            execute('resources-'+name,['/usr/local/cuda/bin/cuobjdump','--dump-resource-usage',str(out/f'build/{name}.o')])
        targets = {}
        for name in ['baseline','vector']:
            dump = (out/f'sass-{name}.stdout.log').read_text()
            chunks = re.split(r'Function\s*:\s*',dump)
            selected = [s for s in chunks if s.splitlines() and '18DeviceReduceKernel' in s.splitlines()[0]]
            assert len(selected)==1
            instructions = [line.strip() for line in selected[0].splitlines() if re.match(r'\s*/\*[0-9a-f]+\*/',line)]
            targets[name] = instructions
            (out/f'target-{name}-sass.txt').write_text('\n'.join(instructions)+'\n')
        assert targets['baseline'] != targets['vector'], 'Candidate branch did not change target kernel'
        counts = {name:sum('LDG.E.128' in line for line in lines) for name,lines in targets.items()}
        assert counts['vector'] > counts['baseline'], counts
        manifest['target_static_vector_load_sites'] = counts
        execute('trace',[str(binary),'-a','Case=[8,9]','--profile'],gpu=True,trace=True)
        manifest['prepared'] = True
        save()
        return

    assert sha(binary) == manifest['binary_sha256']
    for path,digest in manifest['source_sha256'].items():
        assert sha(ROOT/path) == digest
    manifest['measurement_started'] = True
    manifest['paired_results'] = []
    save()
    for round_index in range(6):
        order = list(range(7))
        random.Random(6400+round_index).shuffle(order)
        variants = [0,1] if round_index%2==0 else [1,0]
        codes = [2*i+v for i in order for v in variants]
        label = f'round{round_index+1}'
        args = [str(binary),'-d','0','-a','Case=['+','.join(map(str,codes))+']',
                '--stopping-criterion','sample-count','--target-samples','1000','--cold-warmup-runs','20',
                '--timeout','15','--json',str(out/(label+'.json')),'--md',str(out/(label+'.md'))]
        step,logs = execute(label,args,gpu=True)
        checks = re.findall(r'CHECK Case=(\d+) N=(\d+) variant=(\d+) before=(-?\d+) after=(-?\d+) input=(\S+) output=(\S+) scratch=(\S+) stream=(\S+)',logs)
        assert len(checks)==14 and [int(c[0]) for c in checks]==codes
        assert len({tuple(c[5:]) for c in checks})==1 and all(c[3]==c[4] for c in checks)
        assert not step['warnings'], step['warnings']
        rows = records(out/(label+'.json'))
        assert len(rows)==14 and all(r['samples']==1000 and not r['at_timeout_boundary'] for r in rows)
        step.update(rows=rows, checks=checks, case_order=codes)
        by_case = {int(r['axes']['Case']):r for r in rows}
        for i,n in enumerate(SIZES):
            a,b = by_case[2*i],by_case[2*i+1]
            manifest['paired_results'].append({'round':round_index+1,'n':n,'baseline_median_us':a['median_s']*1e6,
                'variant_median_us':b['median_s']*1e6,'delta_pct':(b['median_s']/a['median_s']-1)*100})
        save()
    manifest['summary'] = []
    for n in SIZES:
        pairs = [r for r in manifest['paired_results'] if r['n']==n]
        deltas = [r['delta_pct'] for r in pairs]
        manifest['summary'].append({'n':n,'paired_median_delta_pct':statistics.median(deltas),
                                    'faster_rounds':sum(d<0 for d in deltas),'deltas_pct':deltas})
    lookup = {r['n']:r for r in manifest['summary']}
    target = lookup[720*4096-1]
    manifest['exploratory_gate_passed'] = target['faster_rounds']>=5 and target['paired_median_delta_pct']<=-2 and all(lookup[n]['paired_median_delta_pct']<=2 for n in [720*4096-4096,720*4096])
    manifest['upstream_status_after'] = capture(['git','-C',str(CCCL),'status','--porcelain'])
    assert not manifest['upstream_status_after'].strip()
    manifest['completed'] = True
    save()
    print(json.dumps(manifest['summary'],indent=2),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage',choices=['prepare','resume-after-debugger-block','measure','retest'])
    parser.add_argument('output',type=Path)
    parser.add_argument('--prepared-from',type=Path)
    args=parser.parse_args()
    run(args.output.resolve(),args.stage,args.prepared_from.resolve() if args.prepared_from else None)
