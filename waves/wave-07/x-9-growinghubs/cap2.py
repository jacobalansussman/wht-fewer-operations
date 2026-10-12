#!/usr/bin/env python3
"""x-9-growinghubs/cap2.py: same exhaustive count as cap.py, split by the kind of wire:
'sign' = all nonzero entries equal up to sign (one magnitude);  'weighted' = at least two magnitudes among the nonzero entries.
Question: does a weighted wire ever serve as many rows, with witnesses as small, as a sign wire?  (8 points modulo 5 and 7-point check modulo 3.)"""
import itertools, sys
def rowsH(N): return [tuple(-1 if bin(w & x).count('1') & 1 else 1 for x in range(N)) for w in range(N)]
for N, p in ((4, 5), (4, 7), (8, 3), (8, 5)):
    R = [tuple(v % p for v in r) for r in rowsH(N)]
    best = {'sign': [0] * (N + 1), 'weighted': [0] * (N + 1)}; arg = {'sign': [None] * (N + 1), 'weighted': [None] * (N + 1)}
    for M in itertools.product(range(p), repeat=N):
        if not any(M): continue
        mags = {min(x, p - x) for x in M if x}
        kind = 'sign' if len(mags) == 1 else 'weighted'
        mins = []
        for O in R:
            m = N
            for al in range(1, p):
                d = 0
                for i in range(N):
                    if (al * M[i] - O[i]) % p: d += 1
                if d < m: m = d
            mins.append(m)
        for s in range(N + 1):
            c = sum(1 for m in mins if m <= s)
            if c > best[kind][s]: best[kind][s] = c; arg[kind][s] = M
    print('N=%d modulo %d: most rows one gate away with a witness of support <= s' % (N, p))
    for s in range(1, N // 2 + 1):
        f = lambda M: [x if x <= p // 2 else x - p for x in M] if M else None
        print('   s=%d: sign wires %d   weighted wires %d   (e.g. weighted %s)' % (s, best['sign'][s], best['weighted'][s], f(arg['weighted'][s])))
    sys.stdout.flush()
