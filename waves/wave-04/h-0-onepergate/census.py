#!/usr/bin/env python3
"""h-0 onepergate / census.py : the census of hubs, ANY coefficients.  Exact integers.
A point (wire up to scale) that is NOT tight but lies on two or more lines, each through two tight wires, is exactly a wire that
can be made by one gate from tight wires and read by a gate with a tight partner giving a tight wire -- with any coefficients
at all (the coefficients are whatever the intersection of the two lines dictates; nothing is bounded in advance).
For every such point: s, s', entangled bits, and the list of tight lines through it with the levels of the tight wires on them.
usage: census.py k            (k = 3: 128 tight wires; k = 4: 1072)
"""
import sys, itertools, math, pickle
import numpy as np
sys.path.insert(0, 'waves/wave-03/g-1-tightwires')
import os
if not os.path.isdir(sys.path[0]): sys.path[0] = os.path.dirname(os.path.abspath(__file__)) + '/g1'
from ref import tight_wires, wht, nz, norm
k = int(sys.argv[1]); N = 1 << k
tw = tight_wires(k); ws = sorted(tw); n = len(ws); lev = [tw[w] for w in ws]
U = np.array(ws, dtype=np.int64); Gm = U @ U.T
def normrows(P):
    """projective normal form of integer rows (gcd 1, first non-zero positive); zero rows stay zero"""
    g = np.gcd.reduce(np.abs(P), axis=1); g[g == 0] = 1; P = P // g[:, None]
    nzm = P != 0; first = np.argmax(nzm, axis=1); sgn = np.sign(P[np.arange(len(P)), first]); sgn[sgn == 0] = 1
    return P * sgn[:, None]
points = {}     # point -> set of line keys
linekey = {}
nl = 0
for i in range(n):
    for j in range(i + 1, n):
        a, b, c = int(Gm[i, i]), int(Gm[i, j]), int(Gm[j, j]); det = a * c - b * b      # > 0: distinct tight wires are independent
        xi = U @ U[i]; xj = U @ U[j]
        # scaled projection off span(u_i, u_j):  det*x - u_i*(c*xi - b*xj) - u_j*(a*xj - b*xi)
        P = det * U - np.outer(c * xi - b * xj, U[i]) - np.outer(a * xj - b * xi, U[j])
        Pn = normrows(P)
        zero = ~np.any(Pn != 0, axis=1)
        members = tuple(np.nonzero(zero)[0].tolist())            # tight wires on the line through i and j
        if members[0] != i or members[1] != j: continue          # handle every line once, from its two smallest tight wires
        nl += 1
        # groups of tight wires with parallel non-zero projections: each pair (p, q) in a group spans a line coplanar with this one
        order = np.lexsort(Pn.T[::-1]); srt = Pn[order]
        same = np.all(srt[1:] == srt[:-1], axis=1)
        start = 0
        for t in range(1, n + 1):
            if t == n or not same[t - 1]:
                grp = order[start:t]
                if len(grp) >= 2 and not zero[grp[0]]:
                    grp = sorted(grp.tolist())
                    for p, q in itertools.combinations(grp, 2):
                        # intersection point: P[p] = lam * P[q]  =>  u_p - lam*u_q lies on the line (i, j)
                        cidx = int(np.nonzero(P[q])[0][0]); num = int(P[p][cidx]); den = int(P[q][cidx])
                        w = norm([den * int(x) - num * int(y) for x, y in zip(ws[p], ws[q])])
                        if w is None or w in tw: continue
                        points.setdefault(w, set()).add(members)
                start = t
print('N = %d: %d tight wires, %d lines through two tight wires' % (N, n, nl))
# the line (p, q) itself is found when it is the base line; so every point collects all its tight lines
pts = {w: L for w, L in points.items() if len(L) >= 2}
print('non-tight points on two or more tight lines: %d' % len(pts))
def ent_bits(v):
    out = []
    for b in range(k):
        idx = [i for i in range(N) if not (i >> b) & 1]
        lo = [v[i] for i in idx]; hi = [v[i | (1 << b)] for i in idx]
        piv = next(j for j in range(len(lo)) if lo[j] != 0 or hi[j] != 0)
        if any(lo[piv] * hi[j] - hi[piv] * lo[j] != 0 for j in range(len(lo))): out.append(b)
    return out
hist = {}; best = {}
for w, L in pts.items():
    s = nz(w); s2 = nz(wht(w)); mags = tuple(sorted({abs(x) for x in w if x}))
    # for each line: the levels of the tight wires on it; "span" of a line = highest - lowest level on it
    spans = sorted((max(lev[t] for t in l) - min(lev[t] for t in l)) for l in L)
    nbig = {d: sum(1 for x in spans if x == d) for d in range(k + 1)}
    key = (s, s2, len(L), mags, tuple(nbig[d] for d in range(k + 1)), len(ent_bits(w)))
    hist[key] = hist.get(key, 0) + 1; best.setdefault(key, w)
print('classes (s, s\', number of tight lines through the point, |entries|, lines by level span 0..k, entangled bits): count, example')
for key in sorted(hist, key=lambda z: (-z[2], z)): print('  ', key, ':', hist[key], list(best[key]))
pickle.dump({'ws': ws, 'lev': lev, 'pts': {w: sorted(L) for w, L in pts.items()}}, open('census_%d.pkl' % k, 'wb'))
