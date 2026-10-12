#!/usr/bin/env python3
"""quad2.py (p-3-hatch32): can g-6's quadric pair at 32 points be the TOP of two trees?  One level down, exhaustive.

g-6 Lemma A: in a two-step word, every node S of the first tree and every node U of the second have nu(S, U) <= 4,
nu(S, U) = rank H[S, U] + rank H[S, complement of U] - |S|.
The quadric pair S = {x0 x1 + x2 = 0}, U = {y1 y3 + y4 = 0} has nu = 4 (not periodic).  The first tree must split S into
two nodes S1, S2 (sizes a, 16 - a), and each must again have nu(S1, U) <= 4.  Here: every subset S1 of S (all sizes 1..15),
against U; and every subset U1 of U against S (nu with the roles exchanged = rank H[S, U1] + rank H[S^c, U1] - |U1|).
Ranks modulo p = 2^31 - 1 are lower bounds for the true ranks, so a rejection (nu mod p > 4) is rigorous; acceptances
are recomputed with exact fractions.
"""
import sys, itertools
from fractions import Fraction as Fr
P = (1 << 31) - 1
N = 32
def bit(x, i): return (x >> i) & 1
def dot(a, b): return bin(a & b).count("1") & 1
H = [[-1 if dot(x, y) else 1 for y in range(N)] for x in range(N)]

def rank_mod(rows):
    M = [[v % P for v in r] for r in rows]; rk = 0; ncol = len(M[0])
    for c in range(ncol):
        piv = next((i for i in range(rk, len(M)) if M[i][c]), None)
        if piv is None: continue
        M[rk], M[piv] = M[piv], M[rk]
        iv = pow(M[rk][c], P - 2, P); pr = M[rk]
        for i in range(rk + 1, len(M)):
            f = M[i][c] * iv % P
            if f:
                Mi = M[i]; M[i] = [(a - f * b) % P for a, b in zip(Mi, pr)]
        rk += 1
        if rk == len(M): break
    return rk
def rank_exact(rows):
    M = [[Fr(v) for v in r] for r in rows]; rk = 0; ncol = len(M[0])
    for c in range(ncol):
        piv = next((i for i in range(rk, len(M)) if M[i][c] != 0), None)
        if piv is None: continue
        M[rk], M[piv] = M[piv], M[rk]
        for i in range(rk + 1, len(M)):
            if M[i][c] != 0:
                f = M[i][c] / M[rk][c]; M[i] = [a - f * b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk
def nu(S1, U, Uc, rk):
    return rk([[H[x][y] for y in U] for x in S1]) + rk([[H[x][y] for y in Uc] for x in S1]) - len(S1)

def stab(S):
    Ss = set(S); return [d for d in range(N) if all((x ^ d) in Ss for x in S)]

def scan(name, S, U, sizes):
    Uc = [y for y in range(N) if y not in U]
    print(f"{name}: nu(S, U) = {nu(S, U, Uc, rank_exact)} (exact)", flush=True)
    for a in sizes:
        tot = ok = 0; keep = []
        for S1 in itertools.combinations(S, a):
            tot += 1
            if nu(S1, U, Uc, rank_mod) <= 4:
                v = nu(S1, U, Uc, rank_exact)
                if v <= 4:
                    ok += 1
                    if len(keep) < 3: keep.append((S1, v, len(stab(S1))))
        print(f"  subsets of size {a}: {tot} tried, {ok} with nu <= 4; first ones (set, nu, size of its stabiliser): {keep}", flush=True)

if __name__ == "__main__":
    S = [x for x in range(N) if (bit(x, 0) & bit(x, 1)) ^ bit(x, 2) == 0]
    U = [y for y in range(N) if (bit(y, 1) & bit(y, 3)) ^ bit(y, 4) == 0]
    sizes = [int(v) for v in sys.argv[1:]] or [8]
    scan("first tree: subsets S1 of the quadric S against the quadric U", S, U, sizes)
    # roles exchanged: H is symmetric, so nu'(U1, S) = rank H[U1, S] + rank H[U1, S^c] - |U1|
    scan("second tree: subsets U1 of the quadric U against the quadric S", U, S, sizes)
