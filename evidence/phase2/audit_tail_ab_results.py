#!/usr/bin/env python3
"""Offline independent consistency checks for the completed A/B evidence batch."""
import hashlib
import json
from pathlib import Path
import statistics
from audit_reduce_measurements import records

root=Path(__file__).resolve().parents[2]
out=root/'evidence/raw/phase2/2026-09-06-tail-ab-recovery'
m=json.loads((out/'manifest.json').read_text())
assert m['completed'] and len(m['runs'])==6 and len(m['pairs'])==42
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(Path(m['binary']))==m['binary_sha256']
assert sha(Path(m['preparation_manifest']))==m['preparation_manifest_sha256']
total=0
for run in m['runs']:
    rows=records(out/f'round{run["round"]}.json')
    assert sorted(int(r['axes']['Case']) for r in rows)==list(range(14))
    assert all(r['samples']==1000 and not r['at_timeout_boundary'] for r in rows)
    by_case={int(r['axes']['Case']):r for r in rows}
    for i,p in enumerate(p for p in m['pairs'] if p['round']==run['round']):
        a,b=by_case[i*2],by_case[i*2+1]
        assert abs(p['delta_pct']-(b['median_s']/a['median_s']-1)*100)<1e-9
    total+=sum(r['samples'] for r in rows)
assert total==84000
assert sum(len(r['warnings']) for r in m['runs'])==6
for s in m['summary']:
    deltas=[p['delta_pct'] for p in m['pairs'] if p['n']==s['n']]
    assert abs(statistics.median(deltas)-s['paired_median_delta_pct'])<1e-9
assert not m['frequency_gate_passed'] and not m['effect_gate_passed'] and not m['exploratory_gate_passed']
result={'accepted_samples':int(total),'discarded_trials':6,'pairs':42,'raw_json_summary_agreement':True,
        'binary_hash_verified':True,'effect_gate_passed':False,'frequency_gate_passed':False,
        'runtime_s':sum(r['elapsed_s'] for r in m['runs']),
        'artifact_sha256':{p.name:sha(p) for p in out.iterdir() if p.is_file()}}
dest=out/'audit.json'
assert not dest.exists()
dest.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='artifact_sha256'},indent=2))
