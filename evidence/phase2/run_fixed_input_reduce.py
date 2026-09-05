#!/usr/bin/env python3
"""Build one local diagnostic TU from existing flags/dependencies; run bounded checks.

No configure, download, upstream source edit, or timing-data deletion.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import time

from audit_reduce_measurements import records
from probe_reduce_boundaries import BUILD, CCCL, HEAD, POWER, TURBO, capture

CENTER = 720 * 4096
SIZES = [CENTER-4096, CENTER-2048, CENTER-32, CENTER-4, CENTER-1, CENTER, CENTER+1]


def run(out):
    out.mkdir(parents=True, exist_ok=False)
    build = out/'build'
    build.mkdir()
    source = Path(__file__).with_name('fixed_input_reduce.cu').resolve()
    binary = build/'fixed_input_reduce'
    obj = build/'fixed_input_reduce.o'
    manifest = {'scope': 'fixed input/output/scratch/stream within process; patterned I32 sum',
                'source': str(source), 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                'head': capture(['git', '-C', str(CCCL), 'rev-parse', 'HEAD']).strip(),
                'upstream_status': capture(['git', '-C', str(CCCL), 'status', '--short']), 'steps': []}
    def save():
        (out/'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    save()
    if manifest['head'] != HEAD or manifest['upstream_status'].strip():
        raise RuntimeError('Source guard failed')
    commands = capture(['ninja', '-C', str(BUILD), '-t', 'commands', 'cub.bench.reduce.sum.base']).splitlines()
    original_compile = next(line for line in commands if ' -c ' in line and line.endswith('sum.cu.o'))
    compile_args = shlex.split(original_compile)
    filtered = []
    i = 0
    while i < len(compile_args):
        token = compile_args[i]
        if token in ['-MT', '-MF']:
            i += 2
            continue
        if token == '-MD':
            i += 1
            continue
        filtered.append(token)
        i += 1
    filtered[filtered.index('-c')+1] = str(source)
    filtered[filtered.index('-o')+1] = str(obj)
    original_link = next(line for line in commands if ' -o bin/cub.bench.reduce.sum.base ' in line)
    link = shlex.split(original_link.removeprefix(': && ').removesuffix(' && :'))
    link = [token for token in link if token != 'lib/libnvbench_main.a']
    link = [str(obj) if token.endswith('/bench/reduce/sum.cu.o') else token for token in link]
    link[link.index('-o')+1] = str(binary)
    env = dict(os.environ, LD_LIBRARY_PATH=f'{BUILD}/lib:/usr/lib/wsl/lib:/usr/local/cuda/lib64',
               CCCL_EXPERIMENTAL_LOGGING='0')
    manifest.update(original_compile=original_compile, original_link=original_link,
                    nvbench_head=capture(['git', '-C', str(BUILD/'_deps/nvbench-src'), 'rev-parse', 'HEAD']).strip(),
                    nvbench_lib_sha256=hashlib.sha256((BUILD/'lib/libnvbench.so').read_bytes()).hexdigest(),
                    ld_library_path=env['LD_LIBRARY_PATH'])

    def execute(label, args, timeout=180, trace=False, gpu=False):
        entry = {'label': label, 'command': args, 'trace_only': trace, 'gpu': gpu}
        manifest['steps'].append(entry)
        if gpu:
            entry['power_before'] = capture(POWER)
            if TURBO not in entry['power_before'].replace('\x00', ''):
                save()
                raise RuntimeError('Turbo required')
        save()
        start = time.monotonic()
        with (out/f'{label}.stdout.log').open('wb') as stdout, (out/f'{label}.stderr.log').open('wb') as stderr:
            try:
                p = subprocess.run(args, cwd=BUILD, env=dict(env, CCCL_EXPERIMENTAL_LOGGING='1' if trace else '0'),
                                   stdout=stdout, stderr=stderr, timeout=timeout)
            except subprocess.TimeoutExpired:
                entry['abort'] = 'Process timeout'
                save()
                raise
        entry.update(returncode=p.returncode, elapsed_s=time.monotonic()-start)
        logs = '\n'.join((out/f'{label}.{suffix}.log').read_text(errors='replace') for suffix in ['stdout', 'stderr'])
        entry['warnings'] = [line for line in logs.splitlines() if any(x in line.lower() for x in ['warn:', 'deadlock', 'error:'])]
        save()
        if p.returncode or 'deadlock' in logs.lower():
            raise RuntimeError(f'{label} failed; evidence retained')
        if gpu:
            entry['power_after'] = capture(POWER)
            checks = re.findall(r'CHECK N=(\d+) expected=(\d+) before=(\d+) after=(\d+) input=(\S+) output=(\S+) scratch=(\S+) stream=(\S+)', logs)
            prechecks = re.findall(r'PRECHECK N=(\d+) expected=(\d+) actual=(\d+)', logs)
            entry.update(checks=checks, prechecks=prechecks)
            save()
            if (TURBO not in entry['power_after'].replace('\x00', '') or len(checks) != 7 or len(prechecks) != 12
                    or sorted(int(c[0]) for c in checks) != SIZES
                    or any(c[1] != c[2] or c[1] != c[3] for c in checks)
                    or any(c[1] != c[2] for c in prechecks) or len({tuple(c[4:]) for c in checks}) != 1):
                raise RuntimeError('Correctness/fixed-buffer/power guard failed')
            if not trace:
                rows = records(out/f'{label}.json')
                entry['rows'] = rows
                save()
                if len(rows) != 7 or any(r['samples'] != 1000 or r['at_timeout_boundary'] for r in rows):
                    raise RuntimeError('Sampling guard failed')
        print(f'{label}: {entry["elapsed_s"]:.2f}s, exit={p.returncode}, warnings={len(entry["warnings"])}', flush=True)

    execute('compile', filtered, timeout=300)
    execute('link', link, timeout=120)
    manifest['binary_sha256'] = hashlib.sha256(binary.read_bytes()).hexdigest()
    manifest['gpu_before'] = capture(['/usr/lib/wsl/lib/nvidia-smi'])
    for label, sizes, trace in [('trace', SIZES, True), ('round1', SIZES, False),
                                ('round2', list(reversed(SIZES)), False), ('round3', SIZES[3:]+SIZES[:3], False)]:
        args = [str(binary), '-d', '0', '-a', 'Elements{io}=['+','.join(map(str, sizes))+']',
                '--json', str(out/f'{label}.json'), '--md', str(out/f'{label}.md')]
        args += ['--profile'] if trace else ['--stopping-criterion', 'sample-count', '--target-samples', '1000',
                                           '--cold-warmup-runs', '20', '--timeout', '15']
        execute(label, args, gpu=True, trace=trace)
    manifest['gpu_after'] = capture(['/usr/lib/wsl/lib/nvidia-smi'])
    manifest['upstream_status_after'] = capture(['git', '-C', str(CCCL), 'status', '--short'])
    save()
    for n in SIZES:
        rows = [r for step in manifest['steps'] for r in step.get('rows', []) if int(r['axes']['Elements{io}']) == n]
        print(json.dumps({'n': n, 'medians_us': [r['median_s']*1e6 for r in rows],
                          'means_us': [r['mean_s']*1e6 for r in rows], 'noise_pct': [r['noise']*100 for r in rows]}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    run(args.output.resolve())
