#!/usr/bin/env python3
# h-5 / mkpool.py : writes pool.txt for pairex.c : the pair class at 8 points with entries 0,+-1 (352 wires) and its gates
# (collinear triples over the rationals: third points u+-v, u+-2v, 2u+-v).  mode 'gf3' adds every triple that is collinear modulo 3.
import sys, itertools
from math import gcd
N = 8; mode = sys.argv[1] if len(sys.argv) > 1 else 'q'
def norm(v):
    g = 0
    for a in v: g = gcd(g, abs(a))
    if g == 0: return None
    v = tuple(a // g for a in v)
    for a in v:
        if a: return v if a > 0 else tuple(-b for b in v)
def cutrank1(w, i):
    lo = [w[x] for x in range(N) if not (x >> i) & 1]; hi = [w[x] for x in range(N) if (x >> i) & 1]
    return all(lo[a] * hi[b] == lo[b] * hi[a] for a in range(4) for b in range(a + 1, 4))
ws = sorted({norm(v) for v in itertools.product((-1, 0, 1), repeat=N) if any(v) and any(cutrank1(v, i) for i in range(3))})
idx = {w: i for i, w in enumerate(ws)}
def n3(v):
    v = tuple(((a + 1) % 3) - 1 for a in v)
    return norm(v) if any(v) else None
trip = set()
for i in range(len(ws)):
    for j in range(i + 1, len(ws)):
        if mode == 'gf3': third = [n3(tuple(x + y for x, y in zip(ws[i], ws[j]))), n3(tuple(x - y for x, y in zip(ws[i], ws[j])))]
        else: third = [norm(tuple(a * x + b * y for x, y in zip(ws[i], ws[j]))) for a, b in ((1, 1), (1, -1), (1, 2), (1, -2), (2, 1), (2, -1))]
        for w in third:
            if w in idx and idx[w] not in (i, j): trip.add(tuple(sorted((i, j, idx[w]))))
ins = [idx[tuple(int(i == x) for x in range(N))] for i in range(N)]
outs = [idx[norm(tuple((-1) ** bin(c & x).count('1') for x in range(N)))] for c in range(N)]
with open('pool_%s.txt' % mode, 'w') as f:
    f.write('%d %d\n' % (len(ws), len(trip)))
    for w in ws: f.write(' '.join(map(str, w)) + '\n')
    f.write(' '.join(map(str, ins)) + '\n' + ' '.join(map(str, outs)) + '\n')
    for t in sorted(trip): f.write('%d %d %d\n' % t)
print(mode, len(ws), 'wires', len(trip), 'collinear triples')
