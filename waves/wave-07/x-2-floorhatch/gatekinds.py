# x-2-floorhatch/gatekinds.py : EVERY gate w = a*u + b*v between primitive whole-number vectors with entries of size at most M,
# exhaustively at a small number n of coordinates.  Exact (Fractions).  Count (G).  Printed: the list of coefficient pairs
# (|a|, |b|) that occur, and the largest |a| + |b|.  Morgenstern: the largest determinant of N wires grows by at most the factor
# |a| + |b| per gate, and the transform has determinant N^(N/2); so  gates >= (N/2) log2 N / log2(largest |a| + |b|).
# For sign vectors (M = 1) the hand list [x-2.md section 4] is: (1,1) join / un-merge / symmetric difference, (1,2) and (2,1)
# shift, (1/2,1/2) quotient.
import sys, itertools
from fractions import Fraction as F
from math import gcd, log2
def run(n, M):
    pool = []
    for v in itertools.product(range(-M, M + 1), repeat=n):
        nz = [t for t in v if t]
        if not nz or nz[0] < 0: continue
        g = 0
        for t in v: g = gcd(g, t)
        if g == 1: pool.append(v)
    S = set(pool); kinds = {}; best = F(0); wit = None
    vals = range(-M, M + 1)
    for iu in range(len(pool)):
        u = pool[iu]
        for iv in range(iu + 1, len(pool)):
            v = pool[iv]; piv = None
            for i in range(n):
                for j in range(i + 1, n):
                    d = u[i] * v[j] - u[j] * v[i]
                    if d: piv = (i, j, d); break
                if piv: break
            i, j, d = piv
            for wi in vals:
                for wj in vals:
                    a = F(wi * v[j] - wj * v[i], d); b = F(u[i] * wj - u[j] * wi, d)
                    if a == 0 or b == 0: continue
                    w = tuple(a * u[t] + b * v[t] for t in range(n))
                    if any(x.denominator != 1 or abs(x) > M for x in w): continue
                    wt = tuple(int(x) for x in w); g = 0
                    for x in wt: g = gcd(g, x)
                    if g != 1: continue
                    key = tuple(sorted((abs(a), abs(b)))); kinds[key] = kinds.get(key, 0) + 1
                    if abs(a) + abs(b) > best: best = abs(a) + abs(b); wit = (u, v, a, b, wt)
    print('n=%d, entries of size at most %d: %d vectors; coefficient pairs that occur: %s' % (n, M, len(pool), ', '.join('(%s,%s)' % k for k in sorted(kinds))))
    print('   largest |a| + |b| = %s  (for example %s*%s + %s*%s = %s);  gates >= %.3f x N log2 N by Morgenstern, if this is the largest at every n' % (best, wit[2], wit[0], wit[3], wit[1], wit[4], 0.5 / log2(best)))
for n, M in ((3, 1), (4, 1), (5, 1), (6, 1), (3, 2), (4, 2), (3, 3)):
    run(n, M)
