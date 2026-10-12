#!/usr/bin/env python3
"""rename the outputs of o_<N>.txt to y<j> so that e2-0's independent checker ocheck.py (not my code) can read the same program."""
import sys, re
for N in (8, 16, 32, 64, 128, 256, 512):
    L = open('o_%d.txt' % N).read().strip().split('\n'); outs = L[-1].split()[2:]; ren = {n: 'y%d' % j for j, n in enumerate(outs)}
    body = []
    for l in L[1:-1]:
        body.append(' '.join(ren.get(t, t) for t in l.split(' ')))
    open('xcheck/oslp_%d.txt' % N, 'w').write('# count (O) program, %d operations, %d points (h-3-orecord: windows of 3 bits, then butterflies)\n' % (len(body), N) + '\n'.join(body) + '\n')
