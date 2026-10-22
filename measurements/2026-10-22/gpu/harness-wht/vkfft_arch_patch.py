#!/usr/bin/env python3
"""vkfft_arch_patch.py CMakeLists.txt SM  (ay-k0): VkFFT 066a17c hard-codes CUDA_ARCHITECTURES 60 70 75 80 86 and
-gencode compute_60..86, which overrides -DCMAKE_CUDA_ARCHITECTURES and fails on a CUDA 13 toolkit (no sm < 75).
Replace both with the GPU's own architecture. Idempotent."""
import re, sys
p, sm = sys.argv[1], sys.argv[2]
s = open(p).read()
s2 = s.replace('CUDA_ARCHITECTURES 60 70 75 80 86', f'CUDA_ARCHITECTURES {sm}')
s2 = re.sub(r'(\t-gencode arch=compute_\d+,code=compute_\d+[ \t]*\n)+\t-gencode arch=compute_\d+,code=compute_\d+>"\)',
            f'\t-gencode arch=compute_{sm},code=sm_{sm}>")', s2)
print('vkfft_arch_patch:', 'patched' if s2 != s else 'nothing to patch', 'for sm_' + sm)
open(p, 'w').write(s2)
