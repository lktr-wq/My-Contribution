#!/usr/bin/env python3
"""Offline extraction of the exact tested I32 reduction kernel; never launch GPU work."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


def main(out):
    out.mkdir(parents=True, exist_ok=False)
    root = Path(__file__).resolve().parents[2]
    build = root/'evidence/raw/phase2/2026-09-05-fixed-input-reduce-v2/build'
    binary = build/'fixed_input_reduce'
    obj = build/'fixed_input_reduce.o'
    expected = '0f997ed19d59bd20343f557f7766b53ab8f9ca74248e8df2c61533b98eaa6f95'
    if hashlib.sha256(binary.read_bytes()).hexdigest() != expected:
        raise RuntimeError('Measured binary hash mismatch')
    manifest = {'binary': str(binary), 'binary_sha256': expected, 'commands': []}
    def capture(label, args):
        p = subprocess.run(args, capture_output=True, timeout=60)
        (out/(label+'.txt')).write_bytes(p.stdout)
        (out/(label+'.stderr.log')).write_bytes(p.stderr)
        manifest['commands'].append({'label': label, 'args': args, 'returncode': p.returncode})
        if p.returncode:
            raise RuntimeError(p.stderr.decode(errors='replace'))
        return p.stdout.decode(errors='replace')
    tool = '/usr/local/cuda/bin/cuobjdump'
    sass = capture('object-sass', [tool, '--dump-sass', str(obj)])
    symbols = re.findall(r'Function\s*:\s*(\S+)', sass)
    targets = [s for s in symbols if 'DeviceReduceKernel' in s and 'SingleTile' not in s]
    if len(targets) != 1:
        raise RuntimeError(f'Ambiguous kernel list: {targets}')
    symbol = targets[0]
    manifest['symbol'] = symbol
    manifest['demangled'] = capture('kernel-demangled', ['c++filt', symbol]).strip()
    kernel_sass = capture('binary-reduce-sass', [tool, '--dump-sass', '--function', symbol, str(binary)])
    capture('binary-reduce-ptx', [tool, '--dump-ptx', '--function', symbol, str(binary)])
    capture('binary-reduce-resources', [tool, '--dump-resource-usage', '--function', symbol, str(binary)])
    if symbol not in kernel_sass:
        raise RuntimeError('Selected binary dump is empty')
    manifest['artifact_sha256'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.txt')}
    (out/'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    main(parser.parse_args().output.resolve())
