#!/usr/bin/env python3
"""Compile and run correctness only. No dependency downloads or timing benchmark."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

root=Path(__file__).resolve().parents[2]
cccl=Path('/home/lktr/src/cccl')
out=Path(sys.argv[1]).resolve()
out.mkdir(parents=True,exist_ok=False)
(out/'build').mkdir()
source=root/'evidence/phase2/binary_search_11412.cu'
binary=out/'build/binary_search_11412'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def capture(args):
    return subprocess.check_output(args,timeout=15).decode(errors='replace').strip()
m={'utc_start':datetime.datetime.now(datetime.timezone.utc).isoformat(),
   'scope':'correctness only; stock CCCL + four local integer reference variants',
   'source_sha256':sha(source),'driver_sha256':sha(Path(__file__)),
   'cccl_head':capture(['git','-C',str(cccl),'rev-parse','HEAD']),
   'status_before':capture(['git','-C',str(cccl),'status','--porcelain']),
   'nvcc_version':capture(['/usr/local/cuda/bin/nvcc','--version']),
   'gpu':capture(['/usr/lib/wsl/lib/nvidia-smi','--query-gpu=name,driver_version','--format=csv,noheader']),
   'steps':[],'completed':False}
save=lambda:(out/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
save()
try:
    assert m['cccl_head']=='f747ef146b77ed1e8f38fe8cb3c67effaf7793f2' and not m['status_before']
    commands=[('compile',['/usr/local/cuda/bin/nvcc','-O3','-std=c++17','-arch=sm_89',
        '-I'+str(cccl/'libcudacxx/include'),'-I'+str(cccl/'cub'),'-I'+str(cccl/'thrust'),
        str(source),'-o',str(binary)],120),('correctness',[str(binary)],30)]
    for label,args,limit in commands:
        entry={'label':label,'command':args,'timeout_s':limit};m['steps'].append(entry);save()
        start=time.monotonic()
        with (out/(label+'.stdout.log')).open('wb') as a,(out/(label+'.stderr.log')).open('wb') as b:
            p=subprocess.run(args,stdout=a,stderr=b,timeout=limit)
        entry.update(returncode=p.returncode,elapsed_s=time.monotonic()-start);save()
        print(label,entry,flush=True)
        if p.returncode:raise RuntimeError(label+' failed')
    log=(out/'correctness.stdout.log').read_text()
    assert 'SUMMARY configurations=165 comparisons=2595 status=PASS performance_tested=false' in log
    m['binary_sha256']=sha(binary)
    m['status_after']=capture(['git','-C',str(cccl),'status','--porcelain'])
    assert not m['status_after']
    m['completed']=True;save()
except Exception as error:
    m['failure']=repr(error);save();raise
