#!/usr/bin/env python3
"""Exhaustive host model of eligible tile sizes; NOT a device sanitizer substitute."""
import json
from pathlib import Path
import sys

lengths = 0
for valid in range(1024,4096):
    visits = [0]*valid
    for lane in range(256):
        group_count = 0
        for group in range(lane,valid//4,256):
            first = group*4
            assert first%4 == 0 and first+3 < valid
            for index in range(first,first+4):
                visits[index] += 1
            group_count += 1
        assert group_count >= 1
        tail = (valid//4)*4+lane
        if tail < valid:
            visits[tail] += 1
    assert all(v==1 for v in visits)
    lengths += 1
out = Path(sys.argv[1])
assert not out.exists()
result = {'eligible_lengths_checked':lengths,'minimum':1024,'maximum':4095,
          'each_valid_element_visited_exactly_once':True,'vector_reads_within_valid_end':True,
          'each_thread_has_an_initial_vector':True,'device_sanitizer_verified':False,
          'limitation':'This models source index arithmetic, not compiler-generated runtime memory accesses.'}
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
