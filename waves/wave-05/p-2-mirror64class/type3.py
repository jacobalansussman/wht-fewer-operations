#!/usr/bin/env python3
"""type3.py (p-2-mirror64class): replay, with exact integers, of the hand scheme for the read points whose digits are all
non-zero (n digits, 3^n points q_J = eps_J - v_J).  Claims checked: (1) q_J - q_J' = (eps_a - eps_a') (x) q_rest when J, J'
differ in one digit; (2) the 3^n points span 3^n - 2^n dimensions; (3) they are all reached from 3^n - 2^n start points with
h(n) helper points by line gates, h(2) = 2, h(n) = 2 (3^(n-1) + h(n-1)); (4) every point used is in the mirror."""
import itertools, sys
from fractions import Fraction as Fr
e = [[1 if i == j else 0 for j in range(4)] for i in range(4)]
eps = {1: e[1], 2: e[2], 3: [0, 0, 0, -1]}; u = [1, 1, 1, 0]; w = [0, 1, 1, -1]
v = {j: [a - b for a, b in zip(eps[j], u)] for j in (1, 2, 3)}
def ten(*fs):
    out = [1]
    for f in fs: out = [a*b for a in out for b in f]
    return tuple(out)
def sub(a, b): return tuple(x - y for x, y in zip(a, b))
def q(J): return sub(ten(*[eps[j] for j in J]), ten(*[v[j] for j in J])) if len(J) > 1 else tuple(u)
def d(a): return [x - y for x, y in zip(eps[1], eps[a])]
def rank(rows):
    A = [[Fr(x) for x in r] for r in rows]; r = 0
    for c in range(len(A[0])):
        p = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]
        for i in range(r+1, len(A)):
            if A[i][c] != 0:
                f = A[i][c]/A[r][c]; A[i] = [x - f*y for x, y in zip(A[i], A[r])]
        r += 1
    return r
def R_apply(vec, n):          # R^(x)n, R = I - u w^T digit by digit
    vec = list(vec)
    for pos in range(n):
        stride = 4**(n-1-pos); out = vec[:]
        for base in range(len(vec)):
            if (base // stride) % 4 == 0:
                idx = [base + t*stride for t in range(4)]; s = sum(w[t]*vec[idx[t]] for t in range(4))
                for t in range(4): out[idx[t]] = vec[idx[t]] - s*u[t]
        vec = out
    return vec
def scheme(n, prefix=()):
    """returns (start points, gates as (new, p1, p2), all points) for the family  prefix (x) q_J, J in {1,2,3}^n.
    prefix = tuple of 4-vectors (d's) tensored in front."""
    P = lambda J: ten(*prefix, q(J)) if prefix else q(J)
    if n == 1: return [P((1,))], [], [P((1,))]
    start = [P((1,) + Jp) for Jp in itertools.product((1, 2, 3), repeat=n-1)]; gates = []; pts = list(start)
    for a in (2, 3):
        s2, g2, p2 = scheme(n-1, prefix + (d(a),))
        start += s2; gates += g2; pts += p2
        for Jp in itertools.product((1, 2, 3), repeat=n-1):
            new = P((a,) + Jp); par1 = P((1,) + Jp); par2 = ten(*prefix, d(a), q(Jp))
            assert new == sub(par1, par2); gates.append((new, par1, par2)); pts.append(new)
    return start, gates, pts
for n in (2, 3, 4):
    start, gates, pts = scheme(n)
    T = [q(J) for J in itertools.product((1, 2, 3), repeat=n)]
    assert all(R_apply(p, n) == [-x for x in p] for p in pts), "a point is outside the mirror"
    assert len(set(pts)) == len(pts) and set(T) <= set(pts)
    have = set(start)
    for new, p1, p2 in gates: assert p1 in have and p2 in have; have.add(new)
    rk = rank(start) if n < 4 else None
    print("n = %d: targets %d, start points %d (rank %s; 3^n - 2^n = %d), gates %d, helper points %d ; span of the targets: %s"
          % (n, len(T), len(start), rk, 3**n - 2**n, len(gates), len(pts) - len(T), rank(T) if n < 4 else "not run"))
