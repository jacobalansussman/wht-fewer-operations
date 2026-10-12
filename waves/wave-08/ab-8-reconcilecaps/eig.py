#!/usr/bin/env python3
"""eig.py [ab-8-reconcilecaps]  FLOATS (numpy eigenvalues of an exact 0/1 matrix).  Knows graph of one TYPE of ports of class (h, r).
Inside one type the graph is regular of degree d and its automorphism group is transitive on vertices and on ordered knowing pairs
[derived: Witt-type gluing], so Lovasz's theta equals Hoffman's ratio:  alpha <= theta = n |lmin| / (d + |lmin|).
Reading: (a) no set of ports no two of which know each other is larger than theta, so the alpha-ceiling on kappa is at least 1 + d/|lmin|;
(b) a symmetric positive scatter (the published kind) has kappa <= n / theta = 1 + d / |lmin|   [x-6 section 5; Lovasz sandwich]."""
import sys, itertools, numpy as np
h, r, want = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
N = 1 << h; ALL = N - 1
PC = np.array([bin(x).count('1') & 1 for x in range(N)], dtype=np.uint8)
def subspaces(h, r):
    for piv in itertools.combinations(range(h - 1, -1, -1), r):
        lists = []
        for p in piv:
            free = [b for b in range(p) if b not in piv]
            lists.append([(1 << p) | sum(1 << b for i, b in enumerate(free) if mask >> i & 1) for mask in range(1 << len(free))])
        yield from itertools.product(*lists)
def nondeg(B):
    rows = [sum(int(PC[a & b]) << j for j, b in enumerate(B)) for a in B]; rk = 0
    for c in range(len(B)):
        pv = next((i for i in range(rk, len(rows)) if rows[i] >> c & 1), None)
        if pv is None: return False
        rows[rk], rows[pv] = rows[pv], rows[rk]
        for i in range(len(rows)):
            if i != rk and rows[i] >> c & 1: rows[i] ^= rows[rk]
        rk += 1
    return True
def span(B):
    S = [0]
    for b in B: S += [s ^ b for s in S]
    return S
ports = []
for B in subspaces(h, r):
    if not nondeg(B): continue
    ty = 'alt' if not any(PC[b] for b in B) else ('one' if ALL in span(B) else 'gen')
    if ty == want: ports.append(B)
n = len(ports); P = np.array(ports, dtype=np.int64)
A = np.ones((n, n), dtype=bool)
for i in range(r):
    for j in range(r):
        A &= PC[P[:, i][:, None] & P[:, j][None, :]] == 0
np.fill_diagonal(A, False)
deg = A.sum(1); d = int(deg[0]); assert (deg == d).all()
w = np.linalg.eigvalsh(A.astype(np.float64)); vals = sorted(set(np.round(w, 6)))
lmin = w[0]
print('class (%d,%d) type %s: %d ports, each knows %d of its type; distinct eigenvalues %s' % (h, r, want, n, d, [float(x) for x in vals[:6]] + (['...'] if len(vals) > 6 else [])))
if d: print('   theta = n|lmin|/(d+|lmin|) = %.3f ; kappa of a symmetric positive scatter <= 1 + d/|lmin| = %.4f ; clique bound floor(h/r) or less' % (n * -lmin / (d - lmin), 1 + d / -lmin))
