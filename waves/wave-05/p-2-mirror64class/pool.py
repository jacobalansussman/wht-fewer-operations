#!/usr/bin/env python3
"""pool.py (p-2-mirror64class): a structured pool of helper points for the read side of the subset-sum mirror at 4^m points.
In one base-4 digit: R = I - u w^T, u = (1,1,1,0), w = (0,1,1,-1); R u = -u; R fixes e0 and the differences of
eps1 = e1, eps2 = e2, eps3 = -e3.  Pool (minus side) at level m = targets, the points on two secants at level 2, and every
(plus atom) (x) (minus pool of level m-1) and u (x) (plus pool of level m-1), the new factor put at any digit position.
All points are checked to be in the mirror (R^(x)m v = -v).  usage: pool.py m outfile"""
import sys, itertools
import numpy as np
from math import gcd
from fractions import Fraction as Fr
m = int(sys.argv[1])
e = np.eye(4, dtype=np.int64); eps = {1: e[1], 2: e[2], 3: -e[3]}
u = e[0] + e[1] + e[2]; w = np.array([0, 1, 1, -1])
R1 = np.eye(4, dtype=np.int64) - np.outer(u, w)
atoms = [e[0], eps[1]-eps[2], eps[1]-eps[3], eps[2]-eps[3], 2*eps[1]-u, 2*eps[2]-u, 2*eps[3]-u]
assert (R1 @ u == -u).all() and all((R1 @ a == a).all() for a in atoms)
def prim(v):
    v = [int(x) for x in v]; g = 0
    for x in v: g = gcd(g, abs(x))
    if g == 0: return None
    s = next(x for x in v if x != 0); s = 1 if s > 0 else -1
    return tuple(s*x//g for x in v)
def Rpow(mm):
    M = R1
    for _ in range(mm-1): M = np.kron(M, R1)
    return M
def targets(mm, sign):
    M = np.eye(4**mm, dtype=np.int64) - sign*Rpow(mm)
    out = []
    for j in range(4**mm):
        p = prim(M[:, j])
        if p is not None and p not in out: out.append(p)
    return out
def irank(rows):
    A = [[Fr(x) for x in r] for r in rows]; r = 0
    for cc in range(len(A[0])):
        p = next((i for i in range(r, len(A)) if A[i][cc] != 0), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]
        for i in range(r+1, len(A)):
            if A[i][cc] != 0:
                f = A[i][cc]/A[r][cc]; A[i] = [x - f*y for x, y in zip(A[i], A[r])]
        r += 1
    return r
def two_secant_points(T):
    out = set()
    sec = list(itertools.combinations(range(len(T)), 2))
    for (a, b), (c, d) in itertools.combinations(sec, 2):
        if len({a, b, c, d}) < 4: continue
        if irank([T[a], T[b], T[c], T[d]]) != 3: continue
        # intersection: solve x a + y b = z c + t d
        A = np.array([T[a], T[b], T[c], T[d]], dtype=object).T
        # nullspace by fractions
        rows = [[Fr(int(x)) for x in r] for r in A]; piv = []; rr = 0
        for cc in range(4):
            p = next((i for i in range(rr, len(rows)) if rows[i][cc] != 0), None)
            if p is None: continue
            rows[rr], rows[p] = rows[p], rows[rr]; f = rows[rr][cc]; rows[rr] = [x/f for x in rows[rr]]
            for i in range(len(rows)):
                if i != rr and rows[i][cc] != 0:
                    f = rows[i][cc]; rows[i] = [x - f*y for x, y in zip(rows[i], rows[rr])]
            piv.append(cc); rr += 1
        free = [cc for cc in range(4) if cc not in piv]
        if len(free) != 1: continue
        z = [Fr(0)]*4; z[free[0]] = Fr(1)
        for i, cc in enumerate(piv): z[cc] = -rows[i][free[0]]
        if z[0] == 0 and z[1] == 0: continue
        v = [z[0]*x + z[1]*y for x, y in zip(T[a], T[b])]
        den = 1
        for x in v: den = den*x.denominator//gcd(den, x.denominator)
        p = prim([int(x*den) for x in v])
        if p is not None and p not in T: out.add(p)
    return out
def embed(pos, atom, v, mm):
    V = np.array(v, dtype=np.int64).reshape((4,)*(mm-1)) if mm > 1 else np.array(1)
    X = np.multiply.outer(atom, V); X = np.moveaxis(X, 0, pos)
    return prim(X.reshape(-1))
Wm = {1: {prim(u)}}; Wp = {1: {prim(a) for a in atoms}}
for mm in range(2, m+1):
    Tm, Tp = targets(mm, +1), targets(mm, -1)       # columns of I - R^m (mirror), I + R^m (the other space)
    A = set(Tm); B = set(Tp)
    if mm == 2: A |= two_secant_points(Tm); B |= two_secant_points(Tp)
    for pos in range(mm):
        for a in atoms:
            A |= {embed(pos, a, v, mm) for v in Wm[mm-1]}; B |= {embed(pos, a, v, mm) for v in Wp[mm-1]}
        A |= {embed(pos, u, v, mm) for v in Wp[mm-1]}; B |= {embed(pos, u, v, mm) for v in Wm[mm-1]}
    RM = Rpow(mm)
    assert all((RM @ np.array(v) == -np.array(v)).all() for v in A), "minus pool leaves the mirror"
    assert all((RM @ np.array(v) == np.array(v)).all() for v in B), "plus pool leaves the other space"
    Wm[mm], Wp[mm] = A, B
    print("level", mm, ": minus targets", len(Tm), " minus pool", len(A), " plus targets", len(Tp), " plus pool", len(B))
T = set(targets(m, +1))
with open(sys.argv[2], "w") as f:
    for v in sorted(Wm[m] - T): f.write(" ".join(map(str, v)) + "\n")
print("wrote", len(Wm[m] - T), "helper candidates")
