# x-0-twojobs/budget.py : the largest budget log2((|a|+|b|)/g) of ONE gate w = (a u + b v)/g between primitive whole-number
# vectors whose entries are at most M in absolute value (a, b coprime, g = common factor of a u + b v).  Exhaustive in dimension
# 2 (and 3 for small M as a check that more coordinates do not raise it).  Also: w a form (entries 0, +1, -1), and u, v on
# disjoint sets (a merge).   Bound derived in the report: (|a|+|b|)/g <= 4 M^2 ; w a form: <= 4 M ; merge: max(|a|,|b|) <= M.
import sys, itertools, math
from math import gcd
from fractions import Fraction as F
def prims(M, n):
    out = []
    for t in itertools.product(range(-M, M + 1), repeat=n):
        g = 0
        for x in t: g = gcd(g, abs(x))
        if g != 1: continue
        l = next(x for x in t if x)
        if l > 0: out.append(t)
    return out
def run(M, n):
    P = prims(M, n); best = (0, None); bestform = (0, None); bestmerge = (0, None)
    for u in P:
        for v in P:
            if v <= u: continue
            # all w in the pool on the line through u, v : solve from two coordinates
            piv = None
            for i in range(n):
                for j in range(i + 1, n):
                    D = u[i] * v[j] - u[j] * v[i]
                    if D: piv = (i, j, D); break
                if piv: break
            if not piv: continue
            i, j, D = piv
            for w in P:
                if w == u or w == v: continue
                for s in (1, -1):
                    ww = tuple(s * x for x in w)
                    al = ww[i] * v[j] - ww[j] * v[i]; be = u[i] * ww[j] - u[j] * ww[i]
                    if any(D * ww[l] != al * u[l] + be * v[l] for l in range(n)): continue
                    g0 = gcd(gcd(abs(al), abs(be)), abs(D)); a, b, g = abs(al) // g0, abs(be) // g0, abs(D) // g0
                    if a == 0 or b == 0: continue
                    c = F(a + b, g)
                    if c > best[0]: best = (c, (u, v, ww, a, b, g))
                    if max(abs(x) for x in ww) == 1 and c > bestform[0]: bestform = (c, (u, v, ww, a, b, g))
                    if all(x == 0 or y == 0 for x, y in zip(u, v)) and c > bestmerge[0]: bestmerge = (c, (u, v, ww, a, b, g))
    def show(t): return '%s = %.3f units  e.g. u=%s v=%s w=%s = (%d u, %d v)/%d' % (t[0], math.log2(t[0]), *t[1]) if t[1] else 'none'
    print('M=%d dimension %d (%d primitive vectors): bound 4M^2 = %d' % (M, n, len(P), 4 * M * M))
    print('   any gate      : largest (|a|+|b|)/g = ' + show(best))
    print('   w a form      : largest             = ' + show(bestform))
    print('   merge (u, v on disjoint sets): largest = ' + show(bestmerge))
for M, n in ((1, 2), (1, 3), (2, 2), (2, 3), (3, 2), (4, 2), (5, 2), (7, 2)):
    run(M, n); sys.stdout.flush()
