#!/usr/bin/env python3
"""check_eig.py [ab-1-fewerblocks]  EXACT (Gaussian rationals).  A direct test of section 4.1 on the engine's own matrices,
block size m = 2 and 3: build dir(z) = (1+i)/2 + (1-i)/2 shift(z) on one column, take for a quadratic form Q the columns
prescribed in the report (two columns e_i for a term z_i; columns e_i, e_j and three times e_i + e_j for a term z_i z_j),
and check on the product eigenvector that every dir(z) acts as (-1)^Q(z), every shift as +1, and the kernel
dir(e_1)...dir(e_m) as (-1)^(Q(e_1)+...+Q(e_m)).  Done column by column: on the sign pattern x -> (-1)^(y.x) the matrix
dir(z) has an exact eigenvalue, computed here from the matrix itself, and the eigenvalue on f columns is the product."""
import itertools
from fractions import Fraction as Fr
class G:                                           # Gaussian rationals
    def __init__(s, a, b=0): s.a, s.b = Fr(a), Fr(b)
    def __add__(s, o): return G(s.a + o.a, s.b + o.b)
    def __mul__(s, o): return G(s.a * o.a - s.b * o.b, s.a * o.b + s.b * o.a)
    def __eq__(s, o): return s.a == o.a and s.b == o.b
par = lambda x: bin(x).count("1") & 1
A, B = G(Fr(1, 2), Fr(1, 2)), G(Fr(1, 2), Fr(-1, 2))
def eig(mat, y, N):                                # eigenvalue of mat on the pattern chi_y, checked on every row
    chi = [G(1 - 2 * par(y & x)) for x in range(N)]
    out = None
    for x in range(N):
        v = G(0)
        for x2 in range(N): v = v + mat[x][x2] * chi[x2]
        lam = v * chi[x]                           # chi is +-1, so dividing is multiplying
        assert out is None or out == lam
        out = lam
    return out
def mul(M1, M2, N): return [[sum((M1[i][k] * M2[k][j] for k in range(N)), G(0)) for j in range(N)] for i in range(N)]
ok = True; tested = 0
for m in (2, 3):
    N = 1 << m
    dirm = {z: [[(A if x == x2 else G(0)) + (B if x2 == x ^ z else G(0)) for x2 in range(N)] for x in range(N)] for z in range(1, N)}
    shm = {z: [[G(1) if x2 == x ^ z else G(0) for x2 in range(N)] for x in range(N)] for z in range(1, N)}
    ker = dirm[1]
    for i in range(1, m): ker = mul(ker, dirm[1 << i], N)
    idx = [(i, j) for i in range(m) for j in range(i, m)]
    for q in itertools.product(range(2), repeat=len(idx)):
        cols = []
        for t, (i, j) in enumerate(idx):
            if not q[t]: continue
            cols += [1 << i] * 2 if i == j else [1 << i, 1 << j] + [(1 << i) | (1 << j)] * 3
        Q = lambda z: sum(q[t] & (z >> i & 1) & (z >> j & 1) for t, (i, j) in enumerate(idx)) & 1
        def prod(mat):
            v = G(1)
            for y in cols: v = v * eig(mat, y, N)
            return v
        for z in range(1, N):
            ok &= prod(dirm[z]) == G(1 - 2 * Q(z)); ok &= prod(shm[z]) == G(1)
        ok &= prod(ker) == G(1 - 2 * (sum(Q(1 << i) for i in range(m)) & 1)); tested += 1
    print("m = %d : %d quadratic forms; on the prescribed columns every move acts as (-1)^Q(z), every shift as +1, the kernel as (-1)^<Q,I>: %s" % (m, tested, ok))
