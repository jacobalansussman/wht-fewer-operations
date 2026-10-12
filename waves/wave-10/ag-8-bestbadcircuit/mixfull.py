#!/usr/bin/env python3
"""mixfull.py (ag-8): class test of a 16-point mixed-pairing butterfly network over ALL frames up to the network's own symmetries.
Frames that keep H: inputs x -> A x + b, outputs w -> A^-T w + c (A an invertible 4 x 4 bit matrix).  The network is carried to
itself by every output shift c and by the input shifts inside a block (the two low bits) [derived, see report], so it is enough to
try the 20,160 matrices A with b in {0, 4, 8, 12}, c = 0: 80,640 frames.  General kernel at a random tau modulo 2^61-1.
usage: mixfull.py file part nparts seconds"""
import sys, random, time
import wsolve
from wsolve import parse, outputs, solve, P
random.seed(160)
N, gates, val = parse(sys.argv[1]); out = outputs(N, gates, val); k = 4
part = int(sys.argv[2]); nparts = int(sys.argv[3]); budget = float(sys.argv[4]); start = int(sys.argv[5]) if len(sys.argv) > 5 else 0; t0 = time.time(); tau = random.randrange(2, P - 2)
def app(rows, x): return sum(((bin(rows[i] & x).count('1') & 1) << i) for i in range(k))
def mats():
    def rec(rows):
        if len(rows) == k: yield rows; return
        span = {0}
        for r in rows: span |= {s ^ r for s in span}
        for r in range(1, N):
            if r not in span: yield from rec(rows + [r])
    yield from rec([])
n = yes = und = 0; idx = -1; first = None; complete = True
for A in mats():
    idx += 1
    if idx % nparts != part or idx < start: continue
    if time.time() - t0 > budget: complete = False; break
    img = [app(A, x) for x in range(N)]; inv = [0] * N
    for x in range(N): inv[img[x]] = x
    AT = [sum(((bin(w & inv[1 << i]).count('1') & 1) << i) for i in range(k)) for w in range(N)]
    for b in (0, 4, 8, 12):
        r = solve(N, gates, out, tau, [img[x] ^ b for x in range(N)], AT); n += 1
        if r[0] == 'YES':
            yes += 1
            if first is None: first = (A, b)
        elif r[0] != 'NO': und += 1
print('start index %d;' % start, '%s part %d/%d: matrices reached %d of 20160, frames tried %d, YES %d, undecided %d, complete=%s (%.0f s) first YES %s'
      % (sys.argv[1], part, nparts, idx + 1, n, yes, und, complete, time.time() - t0, first), flush=True)
