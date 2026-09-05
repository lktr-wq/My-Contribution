#!/usr/bin/env python3
"""Read-only validation of the saved evidence; writes a fresh validation record."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

root = Path(__file__).resolve().parents[2]
out = root/'evidence/raw/phase2/2026-09-06-reduce-sass'
up = root/'evidence/raw/phase2/2026-09-06-reduce-upstream'
m = json.loads((out/'manifest.json').read_text())
for name, digest in m['artifact_sha256'].items():
    assert hashlib.sha256((out/name).read_bytes()).hexdigest() == digest, name
obj = (out/'object-sass.txt').read_text()
segment = obj.split('Function : '+m['symbol'], 1)[1].split('Function :', 1)[0]
instructions = lambda s: [l.strip() for l in s.splitlines() if re.match(r'\s*/\*[0-9a-f]+\*/', l)]
assert instructions(segment) == instructions((out/'binary-reduce-sass.txt').read_text())
src = Path('/home/lktr/src/cccl')
paths = ['cub/cub/agent/agent_reduce.cuh', 'cub/cub/warp/specializations/warp_reduce_shfl.cuh', 'cub/cub/block/specializations/block_reduce_warp_reductions.cuh']
equal = {}
for path in paths:
    equal[path] = (src/path).read_bytes() == (up/('main-'+Path(path).name)).read_bytes()
assert all(equal.values())
run = lambda *args: subprocess.check_output(['git', '-C', str(src), *args], text=True).strip()
assert run('rev-parse', 'HEAD') == 'f747ef146b77ed1e8f38fe8cb3c67effaf7793f2'
assert run('status', '--porcelain') == ''
history = run('log', '-5', '--format=%H %cs %s', '--', paths[1])
result = {'object_and_measured_binary_target_sass_equal': True,
          'dump_hashes_verified': True, 'pinned_wsl_checkout_clean': True,
          'live_main_ref_observed': '486de1c44daf7d1a343cbbf0f5477e9bea8ad600',
          'latest_upstream_source_equal_to_pinned': equal,
          'warp_reduce_local_history': history,
          'gpu_work_launched': False}
dest = out/'validation.json'
assert not dest.exists()
dest.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
