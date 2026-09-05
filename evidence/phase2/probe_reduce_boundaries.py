#!/usr/bin/env python3
"""Bounded boundary exploration using the existing official binary, no source edits.

Run in CCCL-Ubuntu with a new output directory. Profile/logging run is path
evidence only; its timings are deliberately excluded from performance summaries.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import statistics
import subprocess
import time

from audit_reduce_measurements import records

CCCL = Path('/home/lktr/src/cccl')
BUILD = CCCL / 'build/cub-benchmark'
BINARY = BUILD / 'bin/cub.bench.reduce.sum.base'
POWER = ['/mnt/c/Windows/System32/powercfg.exe', '/getactivescheme']
TURBO = '6fecc5ae-f350-48a5-b669-b472cb895ccf'
HEAD = 'f747ef146b77ed1e8f38fe8cb3c67effaf7793f2'
N = 2**24
SIZES = [4095, 4096, 4097, N-4096, N-1, N, N+1, N+4095, N+4096]


def capture(cmd):
    p = subprocess.run(cmd, capture_output=True, timeout=20)
    if p.returncode:
        raise RuntimeError(f'Check failed: {cmd}: {p.stderr!r}')
    return p.stdout.decode('utf-8', errors='replace')


def run(out, suite='tile'):
    if suite == 'grid-cap':
        # 719 -> 720 blocks; first extra tile; second extra tile per block.
        centers = [719*4096, 720*4096, 1440*4096]
        sizes_to_run = [center+delta for center in centers for delta in [-1, 0, 1]]
        trace_sizes = sizes_to_run
    else:
        sizes_to_run = SIZES
        trace_sizes = [4095, 4096, 4097, N, N+1]
    out.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ, LD_LIBRARY_PATH=f'{BUILD}/lib:/usr/lib/wsl/lib:/usr/local/cuda/lib64',
               CCCL_EXPERIMENTAL_LOGGING='0')
    manifest = {'utc_start': dt.datetime.now(dt.timezone.utc).isoformat(),
                'scope': 'official I32/I32, 9 sizes, 3 orders, no correctness assertion',
                'suite': suite, 'sizes': sizes_to_run,
                'cccl_head': capture(['git', '-C', str(CCCL), 'rev-parse', 'HEAD']).strip(),
                'cccl_status': capture(['git', '-C', str(CCCL), 'status', '--short']),
                'binary_sha256': hashlib.sha256(BINARY.read_bytes()).hexdigest(),
                'nvbench_head': capture(['git', '-C', str(BUILD/'_deps/nvbench-src'), 'rev-parse', 'HEAD']).strip(),
                'env_overrides': {k: env[k] for k in ['LD_LIBRARY_PATH', 'CCCL_EXPERIMENTAL_LOGGING']},
                'gpu_before': capture(['/usr/lib/wsl/lib/nvidia-smi']), 'runs': []}
    source_paths = ['cub/benchmarks/bench/reduce/base.cuh', 'cub/benchmarks/bench/reduce/sum.cu',
                    'cub/cub/device/device_reduce.cuh', 'cub/cub/device/dispatch/tuning/tuning_reduce.cuh',
                    'cub/cub/device/dispatch/dispatch_reduce.cuh', 'cub/cub/grid/grid_even_share.cuh',
                    'cub/cub/agent/agent_reduce.cuh', 'cub/cub/util_arch.cuh', 'cub/cub/detail/logging.cuh']
    manifest['source_sha256'] = {p: hashlib.sha256((CCCL/p).read_bytes()).hexdigest() for p in source_paths}
    def save():
        (out/'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    save()
    if manifest['cccl_head'] != HEAD or manifest['cccl_status'].strip():
        raise RuntimeError('Source version/cleanliness guard failed')

    def execute(label, sizes, trace=False):
        prefix = out/label
        entry = {'label': label, 'sizes_requested': sizes, 'trace_only': trace,
                 'power_before': capture(POWER), 'utc_start': dt.datetime.now(dt.timezone.utc).isoformat()}
        manifest['runs'].append(entry)
        save()
        if TURBO not in entry['power_before'].replace('\x00', ''):
            raise RuntimeError('Turbo required; no more GPU work')
        args = [str(BINARY), '-d', '0', '-a', 'T{ct}=I32', '-a', 'OffsetT{ct}=I32',
                '-a', 'Elements{io}=['+','.join(map(str, sizes))+']',
                '--json', str(prefix.with_suffix('.json')), '--md', str(prefix.with_suffix('.md'))]
        args += ['--profile'] if trace else ['--stopping-criterion', 'sample-count', '--target-samples',
                                           '1000', '--cold-warmup-runs', '20', '--timeout', '15']
        run_env = dict(env, CCCL_EXPERIMENTAL_LOGGING='1' if trace else '0')
        entry.update(command=args, logging=run_env['CCCL_EXPERIMENTAL_LOGGING'])
        save()
        start = time.monotonic()
        with prefix.with_suffix('.stdout.log').open('wb') as stdout, prefix.with_suffix('.stderr.log').open('wb') as stderr:
            try:
                p = subprocess.run(args, cwd=BUILD, env=run_env, stdout=stdout, stderr=stderr, timeout=180)
            except subprocess.TimeoutExpired:
                entry['abort'] = '180 second process limit exceeded'
                save()
                raise
        entry.update(returncode=p.returncode, elapsed_s=time.monotonic()-start, power_after=capture(POWER))
        logs = '\n'.join(prefix.with_suffix(ext).read_text(errors='replace') for ext in ['.stdout.log', '.stderr.log'])
        entry['warning_lines'] = [line for line in logs.splitlines() if any(w in line.lower() for w in ['warn:', 'deadlock', 'error:'])]
        save()
        if p.returncode or 'deadlock' in logs.lower() or TURBO not in entry['power_after'].replace('\x00', ''):
            raise RuntimeError('Execution guard failed; inspect manifest')
        if trace:
            if 'Dispatching DeviceReduce' not in logs:
                raise RuntimeError('Runtime dispatch logging unavailable; inspect before timing')
            if suite == 'grid-cap':
                blocks = re.findall(r'Invoking DeviceReduceKernel<<<(\d+), 256,.*?6 SM occupancy', logs)
                expected = [min((n+4095)//4096, 720) for n in sizes]
                actual = list(map(int, blocks))
                entry.update(grid_expected=expected, grid_actual=actual)
                save()
                if actual != expected or '.items_per_thread = 16, .vec_size = 4' not in logs:
                    raise RuntimeError('Grid/tuning assumption failed; no timing runs')
        else:
            rows = records(prefix.with_suffix('.json'))
            entry['rows'] = rows
            entry['sizes_actual'] = [int(r['axes']['Elements{io}']) for r in rows]
            save()
            if (sorted(entry['sizes_actual']) != sorted(sizes)
                    or any(r['samples'] != 1000 or r['at_timeout_boundary']
                           or r['axes']['T{ct}'] != 'I32' or r['axes']['OffsetT{ct}'] != 'I32' for r in rows)):
                raise RuntimeError('Sample/axis guard failed; no further runs')
        print(f'{label}: {entry["elapsed_s"]:.2f}s, exit {p.returncode}, warnings {len(entry["warning_lines"])}', flush=True)

    execute('dispatch-trace', trace_sizes, trace=True)
    orders = [sizes_to_run, list(reversed(sizes_to_run)), sizes_to_run[4:]+sizes_to_run[:4]]
    for i, sizes in enumerate(orders, 1):
        execute(f'round{i}', sizes)
    groups = []
    for n in sizes_to_run:
        rows = [r for trial in manifest['runs'] if not trial['trace_only'] for r in trial['rows']
                if int(r['axes']['Elements{io}']) == n]
        medians = [r['median_s']*1e6 for r in rows]
        groups.append({'elements': n, 'medians_us': medians,
                       'median_of_medians_us': statistics.median(medians),
                       'span_pct': (max(medians)-min(medians))/statistics.median(medians)*100,
                       'noise_pct': [r['noise']*100 for r in rows],
                       'means_us': [r['mean_s']*1e6 for r in rows]})
    manifest['groups'] = groups
    manifest['gpu_after'] = capture(['/usr/lib/wsl/lib/nvidia-smi'])
    manifest['cccl_status_after'] = capture(['git', '-C', str(CCCL), 'status', '--short'])
    manifest['utc_end'] = dt.datetime.now(dt.timezone.utc).isoformat()
    save()
    print(json.dumps(groups, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output_directory', type=Path)
    parser.add_argument('--suite', choices=['tile', 'grid-cap'], default='tile')
    args = parser.parse_args()
    run(args.output_directory.resolve(), args.suite)
