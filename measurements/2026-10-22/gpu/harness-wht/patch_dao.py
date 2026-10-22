#!/usr/bin/env python3
"""patch_dao.py SRC DST -- copy Dao's fast-hadamard-transform tree and put the 19-line (8-point) and 52-line (16-point)
steps into its per-thread register stage hadamard_mult_thread<kLogN, kNChunks> (under -DFHT_G19 / -DFHT_G52).
The circuits come from circuits/ through gen_cuda.py.  Nothing else changes (same loads, shuffles, shared memory)."""
import os, shutil, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
src, dst = sys.argv[1], sys.argv[2]
if os.path.exists(dst):
    shutil.rmtree(dst)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns('.git'))
k = subprocess.run([sys.executable, os.path.join(here, 'gen_cuda.py'), 'fht_g19', os.path.join(here, 'circuits/h8_G19.txt'),
                    'fht_g52', os.path.join(here, 'circuits/h16_G52_family.txt')], check=True, capture_output=True, text=True).stdout
open(os.path.join(dst, 'csrc', 'k0_circuits.h'), 'w').write('#pragma once\n' + k)
p = os.path.join(dst, 'csrc', 'fast_hadamard_transform_common.h')
s = open(p).read()
anchor = 'template<int kLogN, int kNChunks>\n__device__ __forceinline__ void hadamard_mult_thread(float x[kNChunks][1 << kLogN]) {\n'
assert s.count(anchor) == 1, 'anchor not found: Dao source changed; check the commit'
patch = anchor + '''#if defined(FHT_G19)
    if constexpr (kLogN == 3) {
        #pragma unroll
        for (int c = 0; c < kNChunks; ++c) { fht_g19(x[c]); }
        return;
    }
#endif
#if defined(FHT_G52)
    if constexpr (kLogN == 4) {
        #pragma unroll
        for (int c = 0; c < kNChunks; ++c) { fht_g52(x[c]); }
        return;
    }
#endif
'''
s = s.replace(anchor, patch)
s = s.replace('constexpr int cilog2(int val)', '#include "k0_circuits.h"\nconstexpr int cilog2(int val)', 1)
open(p, 'w').write(s)
print('patched', p)
