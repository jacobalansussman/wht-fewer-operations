#!/usr/bin/env python3
"""mid16.py (p-2-mirror64class): at 16 points, over ALL (read start set, write start set) pairs of the x = 3 solutions,
the least number of rows of the middle table with two or more non-zeros (each such row costs at least one gate).
Exact fractions.  usage: mid16.py a b c d"""
import sys, io, contextlib
from fractions import Fraction as Fr
import mir
a, b, c, d = map(int, sys.argv[1:5]); k = [[a, b], [c, d]]
M = mir.mirror(k, 2); n = 16; r = mir.rank(M)
cols = [[M[i][j] for i in range(n)] for j in range(n)]
cp, cm = mir.points(cols); rp, rm = mir.points(M)
xr, solr, Wr, _ = mir.reduced(cp, r, "read"); xw, solw, Ww, _ = mir.reduced(rp, r, "write")
print("x =", xr, " x' =", xw)
def solve(A, v):
    nA = len(A); aug = [[Fr(x) for x in A[i]] + [Fr(v[i])] for i in range(nA)]; piv = []; rr = 0
    for cc in range(nA):
        p = next((i for i in range(rr, nA) if aug[i][cc] != 0), None)
        if p is None: continue
        aug[rr], aug[p] = aug[p], aug[rr]; f = aug[rr][cc]; aug[rr] = [x/f for x in aug[rr]]
        for i in range(nA):
            if i != rr and aug[i][cc] != 0:
                f = aug[i][cc]; aug[i] = [x - f*y for x, y in zip(aug[i], aug[rr])]
        piv.append(cc); rr += 1
    assert all(aug[i][nA] == 0 for i in range(rr, nA))
    z = [Fr(0)]*nA
    for i, cc in enumerate(piv): z[cc] = aug[i][nA]
    return z
zr = [solve(M, v) for v in Wr]                      # read point v = M z
nz = [sum(1 << t for t in range(len(Wr)) if sum(Fr(Ww[s][j])*zr[t][j] for j in range(n)) != 0) for s in range(len(Ww))]
print("pairing table (write point s against read point t, targets first, then pool): non-zeros per write point:", [bin(x).count('1') for x in nz])
Bs = sorted({tuple(sorted(B)) for (_, B) in solr}); Bps = sorted({tuple(sorted(B)) for (_, B) in solw})
print("distinct read start sets", len(Bs), " distinct write start sets", len(Bps))
masks = [sum(1 << t for t in B) for B in Bs]
hist = {}; best = None
for Bp in Bps:
    rows = [nz[s] for s in Bp]
    for bi, bm in enumerate(masks):
        heavy = 0; tot = 0
        for rw in rows:
            cnt = bin(rw & bm).count('1'); tot += cnt; heavy += (cnt >= 2)
            if cnt == 0: heavy = 99; break       # singular middle: not a valid pair (should not occur)
        hist[heavy] = hist.get(heavy, 0) + 1
        if best is None or (heavy, tot) < best[0]: best = ((heavy, tot), Bp, Bs[bi])
print("rows of the middle with >= 2 non-zeros, histogram over all pairs (99 = a zero row):", sorted(hist.items()))
(h, tot), Bp, B = best
nT = len(cp)
print("least: %d heavy rows, %d non-zeros; read start %s ; write start %s" % (h, tot, [("c%d" % t if t < nT else Wr[t]) for t in B], [("e%d" % s if s < len(rp) else Ww[s]) for s in Bp]))
print("middle table:"); 
for s in Bp: print("   ", [str(sum(Fr(Ww[s][j])*zr[t][j] for j in range(n))) for t in B])
