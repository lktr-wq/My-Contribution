#!/usr/bin/env python3
"""Generate a formatting-preserving diff; verify token equivalence and applyability."""
import difflib,hashlib,json,re,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parents[2];cccl=Path('/home/lktr/src/cccl');out=Path(sys.argv[1])
rel='libcudacxx/include/cuda/std/__algorithm/lower_bound.h'
original=(cccl/rel).read_text();measured=(root/'evidence/phase2/bounded_overlay/cuda/std/__algorithm/lower_bound.h').read_text()
start=original.index('_CCCL_EXEC_CHECK_DISABLE');end=original.index('template <class _ForwardIterator')
new_functions=measured[measured.index('_CCCL_EXEC_CHECK_DISABLE'):measured.index('template <class _ForwardIterator')]
candidate=original[:start]+new_functions+'\n'+original[end:]
extra=''.join('#include <cuda/std/'+s+'>\n' for s in ['__type_traits/is_integral.h','__type_traits/is_signed.h','__type_traits/is_same.h','cstdint','limits'])
needle='#include <cuda/std/__type_traits/remove_reference.h>\n'
candidate=candidate.replace(needle,needle+extra)
normalize=lambda s:re.sub(r'\s+','',re.sub(r'//[^\n]*|/\*.*?\*/','',s,flags=re.S))
assert normalize(candidate)==normalize(measured),'Semantic token sequence changed'
patch=''.join(difflib.unified_diff(original.splitlines(True),candidate.splitlines(True),fromfile='a/'+rel,tofile='b/'+rel))
(out/'minimal.patch').write_text(patch);(out/'minimal-lower_bound.h').write_text(candidate)
cmd=['git','-C',str(cccl),'apply','--check',str(out/'minimal.patch')]
p=subprocess.run(cmd,capture_output=True,text=True,timeout=10)
(out/'minimal-apply.stdout.log').write_text(p.stdout);(out/'minimal-apply.stderr.log').write_text(p.stderr)
result={'token_equivalent_to_measured_overlay':True,'command':cmd,'returncode':p.returncode,
 'candidate_sha256':hashlib.sha256(candidate.encode()).hexdigest(),
 'measured_overlay_sha256':hashlib.sha256(measured.encode()).hexdigest()}
(out/'minimal-patch-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));assert p.returncode==0
