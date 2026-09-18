#!/usr/bin/env python3
import csv,datetime,hashlib,json,re,statistics,sys
from pathlib import Path
out=Path(sys.argv[1]);rows=json.loads((out/'summary.json').read_text())
groups={}
for r in rows:groups.setdefault((r['shape'],r['variant']),[]).append(r['median_ms'])
med={k:statistics.median(v) for k,v in groups.items()}
result={'results':[{'shape':s,'official_ms':med[s,0],'clone_ms':med[s,1],'guarded_ms':med[s,2],
 'reduction_vs_official_percent':100*(1-med[s,2]/med[s,0]),
 'reduction_vs_clone_percent':100*(1-med[s,2]/med[s,1]),
 'paired_round_reduction_vs_clone_percent':[100*(1-next(r['median_ms'] for r in rows if (r['shape'],r['round'],r['variant'])==(s,i,2))/next(r['median_ms'] for r in rows if (r['shape'],r['round'],r['variant'])==(s,i,1))) for i in range(3)]} for s in range(3)]}
instructions={}
for part in (out/'sass.stdout.log').read_text().split('Function : ')[1:]:
    match=re.match(r'_Z14bounded_kernelILi([012])ELb1EE',part)
    if not match:continue
    lines=[re.sub(r'/\*.*?\*/','',line).strip() for line in part.splitlines() if re.match(r'\s*/\*[0-9a-f]+\*/.*;',line)]
    instructions[int(match[1])]='\n'.join(lines)
result['sass']={v:{'instruction_lines':len(t.splitlines()),'normalized_sha256':hashlib.sha256(t.encode()).hexdigest()} for v,t in instructions.items()}
result['official_clone_normalized_instructions_identical']=instructions[0]==instructions[1]
m=json.loads((out/'manifest.json').read_text())
start=datetime.datetime.fromisoformat(next(x['utc_start'] for x in m['steps'] if x['label']=='measure'))
samples=[]
with (out/'gpu.csv').open() as f:
    for row in csv.DictReader(f,skipinitialspace=True):
        ts=datetime.datetime.strptime(row['timestamp'],'%Y/%m/%d %H:%M:%S.%f').replace(tzinfo=datetime.timezone(datetime.timedelta(hours=8)))
        if ts>=start:samples.append(int(row['clocks.current.sm [MHz]'].split()[0]))
result['measurement_sm_mhz']={'samples':len(samples),'min':min(samples),'max':max(samples),'counts':{s:samples.count(s) for s in sorted(set(samples))}}
(out/'analysis.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
