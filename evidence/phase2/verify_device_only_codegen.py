import hashlib,json,re,sys
from pathlib import Path
cpu,gpu,prior=map(Path,sys.argv[1:4])
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def instructions(path):
    for part in path.read_text().split('Function : ')[1:]:
        if part.startswith('_Z14bounded_kernelILi0ELb0EE'):
            return '\n'.join(re.sub(r'/\*.*?\*/','',line).strip() for line in part.splitlines() if re.match(r'\s*/\*[0-9a-f]+\*/.*;',line))
    raise ValueError('Measured public API kernel not found')
a=instructions(gpu/'overlay-sass.stdout.log');b=instructions(prior/'overlay-sass.stdout.log')
r={'cpu_baseline_sha256':sha(cpu/'build/baseline'),'cpu_overlay_sha256':sha(cpu/'build/overlay'),
   'gpu_measured_normalized_instruction_identity_to_previous_overlay':a==b,
   'gpu_normalized_sha256':hashlib.sha256(a.encode()).hexdigest()}
r['cpu_executables_identical']=r['cpu_baseline_sha256']==r['cpu_overlay_sha256']
(gpu/'device-only-codegen.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
assert r['cpu_executables_identical']
