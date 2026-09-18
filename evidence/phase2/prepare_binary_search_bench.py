#!/usr/bin/env python3
"""Build timing entry, run check-only, preserve SASS. Never starts --measure."""
import datetime,hashlib,json,re,subprocess,sys,time
from pathlib import Path
root=Path(__file__).resolve().parents[2]
cccl=Path('/home/lktr/src/cccl')
out=Path(sys.argv[1]).resolve();out.mkdir(parents=True,exist_ok=False)
(out/'build').mkdir();(out/'.gitattributes').write_text('* -text\n')
source=root/'evidence/phase2/binary_search_11412_bench.cu'
binary=out/'build/binary_search_bench'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def capture(args):return subprocess.check_output(args,timeout=15).decode(errors='replace').strip()
m={'utc_start':datetime.datetime.now(datetime.timezone.utc).isoformat(),
   'head':capture(['git','-C',str(cccl),'rev-parse','HEAD']),
   'status_before':capture(['git','-C',str(cccl),'status','--porcelain']),
   'source_hashes':{p.name:sha(p) for p in [source,source.with_name('binary_search_11412.cu'),Path(__file__)]},
   'steps':[],'completed':False,'performance_tested':False}
save=lambda:(out/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
save()
try:
    assert m['head']=='f747ef146b77ed1e8f38fe8cb3c67effaf7793f2' and not m['status_before']
    commands=[('compile',['/usr/local/cuda/bin/nvcc','-O3','-std=c++17','-arch=sm_89','--ptxas-options=-v',
      '-I'+str(cccl/'libcudacxx/include'),'-I'+str(cccl/'cub'),'-I'+str(cccl/'thrust'),str(source),'-o',str(binary)],120),
      ('correctness',[str(binary),'--check'],30),
      ('sass',['/usr/local/cuda/bin/cuobjdump','--dump-sass',str(binary)],30)]
    for label,args,limit in commands:
        e={'label':label,'command':args};m['steps'].append(e);save();start=time.monotonic()
        with (out/(label+'.stdout.log')).open('wb') as a,(out/(label+'.stderr.log')).open('wb') as b:
            p=subprocess.run(args,stdout=a,stderr=b,timeout=limit)
        e.update(returncode=p.returncode,elapsed_s=time.monotonic()-start);save();print(e,flush=True)
        assert p.returncode==0,label+' failed'
    assert 'BENCH_CHECK oracle=300000 blocks=60 timed=0 PASS' in (out/'correctness.stdout.log').read_text()
    # Normalize addresses and instruction encodings, retain registers/predicates/branch operands.
    sass=(out/'sass.stdout.log').read_text()
    kernels=[]
    for section in re.split(r'Function : ',sass)[1:]:
        name=section.splitlines()[0].strip()
        if 'repeated_search' not in name:continue
        instructions=[]
        for line in section.splitlines():
            if re.match(r'\s*/\*[0-9a-fA-F]+\*/',line) and ';' in line:
                instructions.append(re.sub(r'/\*.*?\*/','',line).strip())
        normalized='\n'.join(instructions)
        kernels.append({'name':name,'instruction_count':len(instructions),
          'instruction_sha256':hashlib.sha256(normalized.encode()).hexdigest(),
          'opcodes':sorted(set(line.split()[1 if line.startswith('@') else 0] for line in instructions))})
    assert len(kernels)==5
    m['kernels']=kernels;m['binary_sha256']=sha(binary)
    m['status_after']=capture(['git','-C',str(cccl),'status','--porcelain']);assert not m['status_after']
    m['completed']=True;save();print(json.dumps(kernels,indent=2))
except Exception as error:m['failure']=repr(error);save();raise
