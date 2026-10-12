#!/usr/bin/env python3
"""dump_seeds.py (g-5-k3): write the new 22-gate shapes (8-point transform by the pair route; K3 (x) K3 through brick12) as seeds
for the helper-form search, after an exact check."""
import json, itertools
from fractions import Fraction as F
from k3 import K3, kron, kpow, proportional, butterfly
from brick12 import SC, brick12, k3plain
from pairroute import build
c, cur, raws, parts = build(1)
json.dump({'n': 8, 'gates': [[u, v, str(a), str(b)] for (u, v, a, b) in c.gates]}, open('h8_pair22.json', 'w'))
print('H8 seed:', len(c.gates), 'gates')
# K9 = (K3 at position 1) (x) (first butterfly of position 2) by brick12 on columns 0, 2 and plain K3 on column 1; then the second butterfly
pts = list(itertools.product(range(3), repeat=2)); pos = {p: i for i, p in enumerate(pts)}
c = SC(9); cur = {p: pos[p] for p in pts}
o = brick12(c, cur[(0, 0)], cur[(0, 2)], cur[(1, 0)], cur[(1, 2)], cur[(2, 0)], cur[(2, 2)])
for i in range(3): cur[(i, 0)] = o[(i, 0)]; cur[(i, 2)] = o[(i, 1)]
o = k3plain(c, cur[(0, 1)], cur[(1, 1)], cur[(2, 1)])
for i in range(3): cur[(i, 1)] = o[i]
for i in range(3): cur[(i, 0)], cur[(i, 1)] = butterfly(c, cur[(i, 0)], cur[(i, 1)])
rowmap = {0: 0, 1: 2, 2: 1}; T = kron(K3, K3)
ok = all(proportional(c.rows[cur[(i, s)]], [F(x) for x in T[pos[(i, rowmap[s])]]]) is not None for i in range(3) for s in range(3))
print('K9 through brick12:', len(c.gates), 'gates, correct:', ok)
json.dump({'n': 9, 'gates': [[u, v, str(a), str(b)] for (u, v, a, b) in c.gates]}, open('k9_new22.json', 'w'))
