#!/usr/bin/env python3
"""Derive a single PTX entry and address-indexed SASS from saved offline dumps."""
import hashlib
import json
from pathlib import Path
import re
import sys

out = Path(sys.argv[1])
manifest = json.loads((out/'manifest.json').read_text())
ptx = (out/'binary-reduce-ptx.txt').read_text()
# cuobjdump 13.3 --function filters SASS but does not filter the dumped PTX modules.
needle = '.visible .entry '+manifest['symbol']+'('
assert ptx.count(needle) == 1
start = ptx.index(needle)
body = ptx.index('{', start)
depth = 0
end = None
for i in range(body, len(ptx)):
    depth += (ptx[i] == '{') - (ptx[i] == '}')
    if depth == 0:
        end = i+1
        break
assert end is not None
target = ptx[start:end]+'\n'
selected = out/'target-reduce.ptx'
assert not selected.exists()
selected.write_text(target)
sass = (out/'binary-reduce-sass.txt').read_text()
assert len(re.findall(r'Function\s*:', sass)) == 1
lines = [line.strip() for line in sass.splitlines() if re.match(r'\s*/\*[0-9a-f]+\*/', line)]
(out/'target-sass-instructions.txt').write_text('\n'.join(lines)+'\n')
result = {
    'ptx_source_start_line': ptx[:start].count('\n')+1,
    'ptx_source_end_line': ptx[:end].count('\n')+1,
    'ptx_entry_count': target.count('.visible .entry'),
    'static_sass_instruction_count': len(lines),
    'dynamic_instruction_counts_measured': False,
    'derived_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in [selected, out/'target-sass-instructions.txt']},
}
(out/'derived-manifest.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
