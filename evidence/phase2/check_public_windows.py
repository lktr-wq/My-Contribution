#!/usr/bin/env python3
import csv,datetime,json,re,sys
from pathlib import Path
out=Path(sys.argv[1]);telemetry=[]
with (out/'gpu.csv').open() as f:
    for r in csv.DictReader(f,skipinitialspace=True):
        t=datetime.datetime.strptime(r['timestamp'],'%Y/%m/%d %H:%M:%S.%f').replace(tzinfo=datetime.timezone(datetime.timedelta(hours=8)))
        telemetry.append((t.timestamp()*1000,int(r['clocks.current.sm [MHz]'].split()[0])))
rows=[]
for mode in ['baseline','overlay']:
  for rnd in range(3):
    text=(out/f'{mode}-round{rnd}.stdout.log').read_text()
    starts={(int(n),int(s)):int(t) for n,s,t in re.findall(r'WINDOW_START n=(\d+) shape=(\d+) epoch_ms=(\d+)',text)}
    ends={(int(n),int(s)):int(t) for n,s,t in re.findall(r'WINDOW_END n=(\d+) shape=(\d+) epoch_ms=(\d+)',text)}
    assert len(starts)==8 and starts.keys()==ends.keys()
    for key,a in starts.items():
        values=[mhz for t,mhz in telemetry if a<=t<=ends[key]]
        rows.append(dict(mode=mode,round=rnd,n=key[0],shape=key[1],duration_ms=ends[key]-a,samples=len(values),min_mhz=min(values) if values else None,max_mhz=max(values) if values else None))
(out/'window-clocks.json').write_text(json.dumps(rows,indent=2)+'\n')
all_mhz=[v for r in rows for v in [r['min_mhz'],r['max_mhz']]] if all(r['samples'] for r in rows) else []
print(json.dumps(dict(windows=len(rows),all_sampled=bool(all_mhz),min_mhz=min(all_mhz) if all_mhz else None,max_mhz=max(all_mhz) if all_mhz else None,missing=[r for r in rows if not r['samples']]),indent=2))
