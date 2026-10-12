#!/usr/bin/env python3
"""lp.py m  -- the covering floor for the engine's units, as a linear programme.  [e2-2-ladder, 2026-10-10]

Model (derived in e2-2.md, section 1; for words of the OLD letters only: local mixing, shifts, blocks):
  * a block on one array with r independent directions z_1..z_r is the symmetric m x m bit matrix
    S = sum z_j z_j^T (rank exactly r, diagonal not all zero);
  * the hidden state of the data is a quadratic form q on F_2^m; the block multiplies its array by (-1)^q(S),
    where q(S) = sum_{i<=j} Q_ij S_ij;  the whole kernel is S = I;
  * for every q with q(I) = 1 at least W blocks must have q(S) = 1   (rank argument).
LP:  minimise  sum_S n_S (rank S / m)^z   subject to   sum_S n_S [q(S) = 1] >= 1 for every q with q(I) = 1.
A unit with exponent z has (moment / W) < 1 and its block counts n_S / W are feasible, so LP(m, z) < 1.
The floor z_LP(m) is the z at which LP(m, z) = 1.
Symmetry: coordinate permutations (they fix I); variables and constraints are reduced to orbits.
Floating point (HiGHS); the numbers are numerical, not exact.
"""
import sys, itertools, math
import numpy as np
from scipy.optimize import linprog

m = int(sys.argv[1])
pairs = [(i, j) for i in range(m) for j in range(i, m)]
M = len(pairs)
pos = {p: k for k, p in enumerate(pairs)}
diagmask = sum(1 << pos[(i, i)] for i in range(m))

def rank_of(mask):
    rows = [0] * m
    for (i, j), k in pos.items():
        if mask >> k & 1:
            rows[i] |= 1 << j
            rows[j] |= 1 << i
    r = 0
    for c in range(m):
        piv = None
        for t in range(r, m):
            if rows[t] >> c & 1:
                piv = t; break
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for t in range(m):
            if t != r and rows[t] >> c & 1:
                rows[t] ^= rows[r]
        r += 1
    return r

N = 1 << M
allm = np.arange(N, dtype=np.int64)
rank = np.array([rank_of(x) for x in range(N)], dtype=np.int64)
def par(a):
    a = a.copy()
    s = 1
    while s < 64:
        a ^= a >> s; s *= 2
    return a & 1
# canonical representative under coordinate permutations
canon = allm.copy()
for pi in itertools.permutations(range(m)):
    img = np.zeros(N, dtype=np.int64)
    for (i, j), k in pos.items():
        a, b = sorted((pi[i], pi[j]))
        img |= ((allm >> k) & 1) << pos[(a, b)]
    canon = np.minimum(canon, img)
hasdiag = (allm & diagmask) != 0
okS = hasdiag & (rank >= 1) & (rank <= m - 1)           # legal single blocks
Sorb, Sinv = np.unique(canon[okS], return_inverse=True)
Sidx = allm[okS]
osize = np.bincount(Sinv)
orank = rank[Sorb]
qI = par(allm & diagmask)
qreps = np.unique(canon[qI == 1])
qsize = np.array([(canon == q).sum() for q in qreps])
print("m = %d: %d symmetric matrices, %d legal blocks in %d orbits; %d forms with q(I)=1 in %d orbits"
      % (m, N, okS.sum(), len(Sorb), (qI == 1).sum(), len(qreps)), flush=True)
A = np.zeros((len(qreps), len(Sorb)))
for a, q in enumerate(qreps):
    hit = par(Sidx & q)
    A[a] = np.bincount(Sinv, weights=hit, minlength=len(Sorb)) / osize   # fraction of the orbit selected by q

def show(mask):
    return "".join(str(mask >> pos[(min(i, j), max(i, j))] & 1) for i in range(m) for j in range(m) if True and (j < m))

def mat(mask):
    return "/".join("".join(str(mask >> pos[(min(i, j), max(i, j))] & 1) for j in range(m)) for i in range(m))

def solve(z, verbose=False):
    c = (orank / m) ** z
    res = linprog(c, A_ub=-A, b_ub=-np.ones(len(qreps)), bounds=(0, None), method="highs")
    if verbose:
        print("  z = %.6f: LP value %.9f" % (z, res.fun))
        y = res.x
        for o in np.argsort(-y):
            if y[o] > 1e-9:
                print("    blocks per array %.6f  rank %d  orbit size %d  example %s  (I+S has rank %d)"
                      % (y[o], orank[o], osize[o], mat(int(Sorb[o])), rank[int(Sorb[o]) ^ diagmask]))
        mu = -res.ineqlin.marginals
        for a in np.argsort(-mu):
            if mu[a] > 1e-9:
                print("    dual weight %.6f on form orbit (size %d) example Q = %s (rank of its bilinear form: see text)"
                      % (mu[a], qsize[a], mat(int(qreps[a]))))
    return res.fun

v1 = solve(1.0, True)
print("LP(m=%d, z=1) = %.9f   (the plain schedule has value 1)" % (m, v1))
for z in (0.9, 0.5, 0.0):
    print("LP(m=%d, z=%.1f) = %.9f" % (m, z, solve(z)))
if v1 < 1 - 1e-7:
    lo, hi = 0.0, 1.0            # LP(lo) >= 1 > LP(hi)?  LP decreases with z
    if solve(0.0) < 1:
        print("LP(z=0) < 1: no floor from this LP")
    else:
        for _ in range(40):
            mid = (lo + hi) / 2
            if solve(mid) >= 1: lo = mid
            else: hi = mid
        print("FLOOR z_LP(m=%d) = %.6f  (saving at most %.6f)" % (m, lo, 1 - lo))
        solve(hi, True)
else:
    print("LP(z=1) = 1: at z = 1 the plain schedule is LP-optimal; looking just below 1")
    for z in (0.999, 0.99):
        print("LP(m=%d, z=%.3f) = %.9f" % (m, z, solve(z)))
