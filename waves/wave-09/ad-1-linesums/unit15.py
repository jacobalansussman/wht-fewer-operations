#!/usr/bin/env python3
"""unit15.py [ad-1-linesums]  16 points, the mixed part (15th roots of unity, degree 8).  d-1's guess: the mask D = t + t^2 + t^4 + t^8
is (a unit) x (the field's trinomial)^2.  Exact, fractions.  Finds the trinomial, the unit, and the shortest product of two-term
factors (1 - t^b)^(+-1) equal to the unit, exponents searched in [-3, 3]."""
from fractions import Fraction as F
import itertools
PHI = [1, -1, 0, 1, -1, 1, 0, -1, 1]          # x^8 - x^7 + x^5 - x^4 + x^3 - x + 1, low to high
def red(p):
    p = list(p) + [F(0)] * max(0, 8 - len(p))
    for d in range(len(p) - 1, 7, -1):
        c = p[d]
        if c:
            for i in range(9): p[d - 8 + i] -= c * PHI[i]
    return tuple(p[:8])
def mul(a, b):
    r = [F(0)] * 15
    for i, x in enumerate(a):
        if x:
            for l, y in enumerate(b): r[i + l] += x * y
    return red(r)
def mono(e):
    p = [F(0)] * (e % 15 + 1); p[e % 15] = F(1); return red(p)
def poly(exps, coefs=None):
    r = [F(0)] * 8
    for i, e in enumerate(exps):
        m = mono(e); c = F(1) if coefs is None else F(coefs[i])
        r = [u + c * v for u, v in zip(r, m)]
    return tuple(r)
def matrix(a): return [list(mul(a, mono(i))) for i in range(8)]
def det(M):
    M = [r[:] for r in M]; d = F(1)
    for c in range(8):
        p = next((i for i in range(c, 8) if M[i][c] != 0), None)
        if p is None: return F(0)
        if p != c: M[c], M[p] = M[p], M[c]; d = -d
        d *= M[c][c]
        for i in range(c + 1, 8):
            f = M[i][c] / M[c][c]
            if f: M[i] = [u - f * v for u, v in zip(M[i], M[c])]
    return d
def inv(a):
    M = matrix(a); n = 8                      # solve x * a = 1 : sum_i x_i (a t^i) = 1
    A = [[M[i][r] for i in range(n)] + [F(1 if r == 0 else 0)] for r in range(n)]
    for c in range(n):
        p = next(i for i in range(c, n) if A[i][c] != 0); A[c], A[p] = A[p], A[c]
        A[c] = [v / A[c][c] for v in A[c]]
        for i in range(n):
            if i != c and A[i][c]: A[i] = [u - A[i][c] * v for u, v in zip(A[i], A[c])]
    return tuple(A[i][n] for i in range(n))
D = poly([1, 2, 4, 8]); print("norm of D on the order-15 part:", det(matrix(D)), "= 2^8")
one = mono(0); best = None
for (e, f) in [(1, 4), (3, 4), (1, 12), (11, 12), (2, 8), (7, 8)]:
    pi = poly([0, e, f]); nrm = det(matrix(pi))
    u = mul(D, inv(mul(pi, pi)))
    integral = all(x.denominator == 1 for x in u)
    print("trinomial 1 + t^%d + t^%d : norm %s ; D / trinomial^2 has whole coefficients: %s ; its norm: %s" % (e, f, nrm, integral, det(matrix(u)) if integral else "-"))
    if integral and abs(det(matrix(u))) == 1 and best is None: best = ((e, f), u)
if best:
    (e, f), u = best
    print("so D = u * (1 + t^%d + t^%d)^2 with u a unit; u =" % (e, f), [int(x) for x in u], "(coefficients of 1, t, ..., t^7)")
    gens = [poly([0, b], [1, -1]) for b in (1, 2, 4, 7)]
    pows = [{0: one} for _ in gens]
    for gi, g in enumerate(gens):
        gi_inv = inv(g); a = one; b = one
        for x in range(1, 4):
            a = mul(a, g); b = mul(b, gi_inv); pows[gi][x] = a; pows[gi][-x] = b
    found = []
    for ex in itertools.product(range(-3, 4), repeat=4):
        p = one
        for gi, x in enumerate(ex): p = mul(p, pows[gi][x])
        for sh in range(15):
            q = mul(p, mono(sh))
            if q == u: found.append((sum(abs(x) for x in ex), ex, sh, +1))
            if tuple(-x for x in q) == u: found.append((sum(abs(x) for x in ex), ex, sh, -1))
    found.sort()
    print("u as  sign * t^shift * (1-t)^a (1-t^2)^b (1-t^4)^c (1-t^7)^d , exponents in [-3,3]: %d ways; shortest:" % len(found), found[:3])
