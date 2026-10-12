#!/usr/bin/env python3
"""mixtest.py (ag-8): class test of a 16-point wiring over a RANDOM SAMPLE of the frames that keep H (inputs x -> A x + b, outputs
w -> A^-T w + c), plus the identity.  A sample cannot prove 'special'; it can only fail to find a frame.  usage: mixtest.py file seconds"""
import sys, random, time
import wsolve
from wsolve import parse, outputs, solve, P
random.seed(16)
N, gates, val = parse(sys.argv[1]); out = outputs(N, gates, val); k = N.bit_length() - 1
assert len(out) == N
budget = float(sys.argv[2]); t0 = time.time(); tau = random.randrange(2, P - 2)
print(sys.argv[1], 'N=%d gates=%d' % (N, len(gates)), '| control tau=-1 identity:', solve(N, gates, out, P - 1)[0], '| generic tau identity:', solve(N, gates, out, tau)[0], flush=True)
def app(rows, x): return sum(((bin(rows[i] & x).count('1') & 1) << i) for i in range(k))
def randA():
    while True:
        rows = [random.randrange(1, N) for _ in range(k)]
        img = sorted(app(rows, x) for x in range(N))
        if img == list(range(N)): return rows
n = yes = und = 0
while time.time() - t0 < budget:
    A = randA(); img = [app(A, x) for x in range(N)]; inv = [0] * N
    for x in range(N): inv[img[x]] = x
    AT = [sum(((bin(w & inv[1 << i]).count('1') & 1) << i) for i in range(k)) for w in range(N)]
    b = random.randrange(N); c = random.randrange(N)
    r = solve(N, gates, out, tau, [img[x] ^ b for x in range(N)], [AT[w] ^ c for w in range(N)]); n += 1
    if r[0] == 'YES': yes += 1
    elif r[0] != 'NO': und += 1
print('   frames sampled: %d  YES: %d  undecided: %d  (%.0f s)' % (n, yes, und, time.time() - t0))
