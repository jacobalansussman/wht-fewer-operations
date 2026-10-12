#!/usr/bin/env python3
"""ag-9 spec4.py: a 5 x 4 whole-number matrix built so that sqrt 2 saves a gate (count (G)).
Four inputs e1..e4.  Helpers with entries a + b*sqrt2 (b != 0), each ONE gate from two inputs:
  h1 = e1 + a*e2, h2 = e2 + b*e3, h3 = e3 + c*e1, h4 = e1 + d*e4.
Outputs T_ij = the point where the line h_i h_j meets its conjugate line (sqrt2 -> -sqrt2) for the pairs 12, 13, 23, 14, 34
(pairs whose edges of the tetrahedron share a vertex, so the two lines lie in one plane).  T_ij is fixed by the conjugation,
hence rational.  Over Q(sqrt2): 4 helpers + 5 outputs = 9 gates.  Every output has three non-zero entries, so alone it costs 2.
Exact arithmetic: pairs of Fractions (x, y) = x + y*sqrt2.   usage: spec4.py a0 a1 b0 b1 c0 c1 d0 d1"""
from fractions import Fraction as F
from math import gcd
import sys, itertools
def add(x, y): return (x[0] + y[0], x[1] + y[1])
def sub(x, y): return (x[0] - y[0], x[1] - y[1])
def mul(x, y): return (x[0]*y[0] + 2*x[1]*y[1], x[0]*y[1] + x[1]*y[0])
def inv(x): n = x[0]*x[0] - 2*x[1]*x[1]; return (x[0]/n, -x[1]/n)
def conj(x): return (x[0], -x[1])
def K(a, b=0): return (F(a), F(b))
Z = K(0); ONE = K(1)
def rank(rows):
    M = [list(r) for r in rows]; rk = 0
    for col in range(4):
        piv = next((i for i in range(rk, len(M)) if M[i][col] != Z), None)
        if piv is None: continue
        M[rk], M[piv] = M[piv], M[rk]; iv = inv(M[rk][col])
        for i in range(len(M)):
            if i != rk and M[i][col] != Z:
                f = mul(M[i][col], iv); M[i] = [sub(M[i][k], mul(f, M[rk][k])) for k in range(4)]
        rk += 1
    return rk
def meet(u, v):
    """the point of line(u, v) that also lies on line(conj u, conj v): solve x*u + y*v = z*cu + w*cv"""
    cu, cv = [conj(t) for t in u], [conj(t) for t in v]
    # unknowns (x, y, z, w): 4 equations, one-dimensional kernel expected
    A = [[u[k], v[k], sub(Z, cu[k]), sub(Z, cv[k])] for k in range(4)]
    # kernel by elimination
    M = [r[:] for r in A]; piv_cols = []; rk = 0
    for col in range(4):
        piv = next((i for i in range(rk, 4) if M[i][col] != Z), None)
        if piv is None: continue
        M[rk], M[piv] = M[piv], M[rk]; iv = inv(M[rk][col]); M[rk] = [mul(t, iv) for t in M[rk]]
        for i in range(4):
            if i != rk and M[i][col] != Z:
                f = M[i][col]; M[i] = [sub(M[i][k], mul(f, M[rk][k])) for k in range(4)]
        piv_cols.append(col); rk += 1
    free = [c for c in range(4) if c not in piv_cols]
    assert len(free) == 1, "lines do not meet in one point"
    sol = [Z]*4; sol[free[0]] = ONE
    for i, c in enumerate(piv_cols): sol[c] = sub(Z, M[i][free[0]])
    pt = [add(mul(sol[0], u[k]), mul(sol[1], v[k])) for k in range(4)]
    for t in (ONE, K(0, 1)):
        w = [mul(t, x) for x in pt]
        lead = next(x for x in w if x != Z); w = [mul(x, inv(lead)) for x in w]
        if all(x[1] == 0 for x in w):
            r = [x[0] for x in w]; den = 1
            for x in r: den = den * x.denominator // gcd(den, x.denominator)
            r = [int(x * den) for x in r]; g = 0
            for x in r: g = gcd(g, x)
            return [x // g for x in r]
    raise SystemExit("meeting point not rational")
par = [int(x) for x in sys.argv[1:9]] if len(sys.argv) >= 9 else [0, 1, 1, 1, 3, 1, 2, -1]
a, b, c, d = K(par[0], par[1]), K(par[2], par[3]), K(par[4], par[5]), K(par[6], par[7])
h = {1: [ONE, a, Z, Z], 2: [Z, ONE, b, Z], 3: [c, Z, ONE, Z], 4: [ONE, Z, Z, d]}
pairs = [(1, 2), (1, 3), (2, 3), (1, 4), (3, 4)]
T = {p: meet(h[p[0]], h[p[1]]) for p in pairs}
ok = all(rank([[K(x) for x in T[p]], h[p[0]], h[p[1]]]) == 2 for p in pairs)
print("# parameters a, b, c, d (x,y = x + y*sqrt2):", par)
print("# exact replay over Q(sqrt2): every output lies on the line of its two helpers:", ok, "; 9 gates = 4 helpers + 5 outputs")
print("# number of non-zero entries of each output:", [sum(1 for x in T[p] if x) for p in pairs])
for p in pairs: print(" ".join(str(x) for x in T[p]))
