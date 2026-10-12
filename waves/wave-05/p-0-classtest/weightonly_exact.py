#!/usr/bin/env python3
"""weightonly_exact.py (p-0-classtest): exact replays (fractions) of the circuits for the kernel power on WEIGHT-ONLY data
(data that depend only on the number of 1-bits of the address; columns = weight classes, rows = weight of the output address;
entry (i, j) = sum_m C(i,m) C(k-i,j-m) tau^m; at tau = -1 the Krawtchouk matrix).  Count (G): outputs up to a non-zero factor.
(1) k = 2, every tau: 5 gates.   (2) k = 2, tau = -1: 4 gates.   (3) k = 3, tau = -1: 7 gates (lifted by hand from the GF(13) search)."""
from fractions import Fraction as F
from math import comb
def target(k, t): return [[sum(comb(i, m) * comb(k - i, j - m) * t ** m for m in range(0, min(i, j) + 1) if j - m <= k - i) for j in range(k + 1)] for i in range(k + 1)]
def run(n, prog):
    val = {i: [F(int(i == j)) for j in range(n)] for i in range(n)}
    for nm, a, u, b, v in prog: val[nm] = [F(a) * s + F(b) * w for s, w in zip(val[u], val[v])]
    return val
def prop(y, r):
    i = next(i for i in range(len(r)) if r[i] != 0); f = y[i] / r[i]
    return f != 0 and all(y[j] == f * r[j] for j in range(len(r)))
for t in (F(3), F(2), F(1, 2), F(-2), F(5, 7), F(-1), F(10)):
    v = run(3, [('h1', 1, 0, 2, 1), ('h2', 1, 'h1', t, 2), ('r0', 1, 'h1', 1, 2), ('r1', 1, 'h2', t - 1, 1), ('r2', t, 'h2', 1 - t, 0)])
    T = target(2, t)
    print('(1) k=2 tau=%s: 5 gates, outputs proportional to the rows: %s' % (t, all(prop(v['r%d' % i], T[i]) for i in range(3))))
v = run(3, [('s', 1, 0, 1, 2), ('r1', 1, 0, -1, 2), ('r0', 1, 's', 2, 1), ('r2', 1, 's', -2, 1)]); T = target(2, F(-1))
print('(2) k=2 tau=-1: 4 gates, rows', T, 'ok:', all(prop(v['r%d' % i], T[i]) for i in range(3)))
v = run(4, [('g4', 3, 1, 1, 3), ('g5', 1, 0, -1, 2), ('g6', 3, 'g5', -1, 'g4'), ('y0', 4, 0, -1, 'g6'), ('y2', 1, 'g6', 4, 3), ('y3', 1, 'y0', -2, 'g4'), ('y1', 1, 'y2', -6, 'g5')])
T = target(3, F(-1))
print('(3) k=3 tau=-1: 7 gates, rows', T, 'ok:', all(prop(v['y%d' % i], T[i]) for i in range(4)), '| helper g6 =', [str(z) for z in v['g6']])
