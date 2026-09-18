#!/usr/bin/env python3
"""Bounded measurement of the verified binary; preserve samples and telemetry."""
import datetime, hashlib, json, re, statistics, subprocess, sys, time
from pathlib import Path
root = Path(__file__).resolve().parents[2]
prep = root/'evidence/raw/phase2/2026-09-18-binary-search-bench-prep'
binary = prep/'build/binary_search_bench'
out = Path(sys.argv[1]).resolve()
out.mkdir(parents=True, exist_ok=False)
(out/'.gitattributes').write_text('* -text\n')
manifest = {'utc_start':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'timeout_s':180, 'completed':False}
save = lambda: (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
manifest['binary_sha256'] = sha(binary)
assert manifest['binary_sha256'] == json.loads((prep/'manifest.json').read_text())['binary_sha256']
manifest['command'] = [str(binary),'--measure']
save()
monitor = None
start = time.monotonic()
try:
    with (out/'gpu.csv').open('wb') as gpu, (out/'gpu.stderr.log').open('wb') as ge:
        monitor = subprocess.Popen(['/usr/lib/wsl/lib/nvidia-smi',
          '--query-gpu=timestamp,pstate,temperature.gpu,utilization.gpu,power.draw,clocks.sm,clocks.mem',
          '--format=csv','-lms','200'],stdout=gpu,stderr=ge)
        if '--preheat' in sys.argv[2:]:
            with (out/'preheat.stdout.log').open('wb') as a, (out/'preheat.stderr.log').open('wb') as b:
                warm = subprocess.run(manifest['command'],stdout=a,stderr=b,timeout=180)
            assert warm.returncode == 0
            manifest['preheat_completed'] = True
        manifest['measurement_utc_start'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        save()
        with (out/'samples.stdout.log').open('wb') as a, (out/'samples.stderr.log').open('wb') as b:
            p = subprocess.run(manifest['command'],stdout=a,stderr=b,timeout=180)
        manifest['returncode'] = p.returncode
        assert p.returncode == 0
    text = (out/'samples.stdout.log').read_text()
    assert 'BENCH_CHECK oracle=300000 blocks=61440 timed=1 PASS' in text
    groups = {}
    for s,r,v,i,ms in re.findall(r'SAMPLE shape=(\d+) round=(\d+) variant=(\d+) sample=(\d+) ms=([\d.]+)',text):
        groups.setdefault((int(s),int(r),int(v)),[]).append(float(ms))
    assert len(groups)==45 and all(len(g)==30 for g in groups.values())
    rows = [{'shape':s,'round':r,'variant':v,'n':len(g),'median_ms':statistics.median(g),
             'min_ms':min(g),'max_ms':max(g)} for (s,r,v),g in sorted(groups.items())]
    (out/'summary.json').write_text(json.dumps(rows,indent=2)+'\n')
    manifest.update(completed=True,samples=sum(map(len,groups.values())))
    print(json.dumps(rows,indent=2),flush=True)
except Exception as e:
    manifest['error']=repr(e)
    raise
finally:
    if monitor is not None:
        monitor.terminate()
        try: monitor.wait(timeout=5)
        except subprocess.TimeoutExpired: monitor.kill(); monitor.wait()
        manifest['telemetry_returncode']=monitor.returncode
    manifest['elapsed_s']=time.monotonic()-start
    save()
