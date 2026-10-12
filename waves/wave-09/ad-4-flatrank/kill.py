#!/usr/bin/env python3
"""kill.py [ad-4-flatrank]  For decompositions g = sum of r signed flats (candidates printed by fr, replayed exactly by verify.py):
the least number of flats that survive (a) a RESTRICTION to a non-degenerate flat W of codimension 2, W = {B(u1,z) = c1, B(u2,z) = c2},
B(u1,u2) = 1 (a flat survives if it meets W), and (b) the dual operation, a PROJECTION along a hyperbolic pair (v1, v2) with a sign rule
(a flat is killed when it contains a direction v of the pair's plane along which its own sign differs from the rule).
Whole numbers only."""
import sys
def quad(z, K): return sum(((z >> i) & 1) & ((z >> (i + 1)) & 1) for i in range(0, K, 2)) & 1
def Bf(a, b, K):
    s = 0
    for i in range(0, K, 2): s ^= (((a >> i) & 1) & ((b >> (i + 1)) & 1)) ^ (((a >> (i + 1)) & 1) & ((b >> i) & 1))
    return s
from collections import Counter
for fn in sys.argv[1:]:
    hist = Counter()
    for line in open(fn):
        if not line.startswith("CANDIDATE"): continue
        head = line.split("(")[0].split(); r = int(head[1].split("=")[1]); K = int(head[2].split("=")[1]); N = 1 << K
        fl = []
        for t in line.split("):")[1].split():
            sup, neg = (int(x, 16) for x in t.split(":")); pts = [z for z in range(N) if (sup >> z) & 1]; a = pts[0]
            V = set(p ^ a for p in pts); sgn = {p: (-1 if (neg >> p) & 1 else 1) for p in pts}
            fl.append((sup, a, V, sgn))
        planes = set()
        for u1 in range(1, N):
            for u2 in range(u1 + 1, N):
                if Bf(u1, u2, K): planes.add(frozenset((u1, u2, u1 ^ u2)))
        bestp = r; bestd = r
        for P in planes:
            u1, u2 = sorted(P)[:2]
            for c1 in (0, 1):
                for c2 in (0, 1):
                    Wm = 0
                    for z in range(N):
                        if Bf(u1, z, K) == c1 and Bf(u2, z, K) == c2: Wm |= 1 << z
                    s = sum(1 for (sup, a, V, sgn) in fl if sup & Wm)
                    bestp = min(bestp, s)
                    # dual: rule tau(u1) = c1, tau(u2) = c2, tau(u1+u2) = c1+c2 ; a flat dies if a direction v of P lies in V and its sign ratio along v is not (-1)^tau(v)
                    tau = {u1: c1, u2: c2, u1 ^ u2: c1 ^ c2}; s = 0
                    for (sup, a, V, sgn) in fl:
                        dead = any(v in V and sgn[a ^ v] * sgn[a] != (-1) ** tau[v] for v in tau)
                        s += not dead
                    bestd = min(bestd, s)
        hist[(r, K, bestp, bestd)] += 1
    for (r, K, bp, bd), n in sorted(hist.items()):
        print("%s: r=%d K=%d: least survivors of a restriction %d, of a projection %d  (%d decompositions; %d hyperbolic planes x 4 rules)" % (fn, r, K, bp, bd, n, len(planes)))
