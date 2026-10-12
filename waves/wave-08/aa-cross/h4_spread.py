#!/usr/bin/env python3
"""h4_spread.py [aa-cross]  Projection-slice on a spread.  N = q^2 points, q = 2^j, addresses = F_q^2 written in bits.
A spread: the q + 1 lines through 0 of the plane F_q^2, each a subspace S_i of j address bits; together they cover every
address, and two of them meet only in 0.  V_i = the perpendicular of S_i (bit dot product).  LINE SUMS: for every i, the sums
of the input over the q cosets of V_i (q^2 + q sums in all: the lines of an affine plane of order q).
Claim checked here in whole numbers: the transform at the outputs in S_i is the q-point transform of the i-th family of line
sums.  So T(N) <= R(N) + (q + 1) T(q), with R(N) the least number of gates for all line sums."""
import random, sys
from fractions import Fraction
POLY = {2: 0b111, 3: 0b1011, 4: 0b10011}
def gmul(a, b, j):
    r = 0
    for i in range(j):
        if (b >> i) & 1: r ^= a << i
    for i in range(2 * j - 2, j - 1, -1):
        if (r >> i) & 1: r ^= POLY[j] << (i - j)
    return r
def dot(x, y): return bin(x & y).count("1") & 1
def rank_frac(rows):
    M = [[Fraction(v) for v in r] for r in rows]; rk = 0; nc = len(M[0])
    for c in range(nc):
        piv = None
        for i in range(rk, len(M)):
            if M[i][c] != 0: piv = i; break
        if piv is None: continue
        M[rk], M[piv] = M[piv], M[rk]; inv = 1 / M[rk][c]; M[rk] = [v * inv for v in M[rk]]; R = M[rk]
        for i in range(len(M)):
            if i != rk and M[i][c] != 0:
                f = M[i][c]; M[i] = [a - f * b for a, b in zip(M[i], R)]
        rk += 1
    return rk
def rank_p(rows, p):
    M = [[v % p for v in r] for r in rows]; rk = 0; nc = len(M[0])
    for c in range(nc):
        piv = None
        for i in range(rk, len(M)):
            if M[i][c]: piv = i; break
        if piv is None: continue
        M[rk], M[piv] = M[piv], M[rk]; inv = pow(M[rk][c], p - 2, p); M[rk] = [v * inv % p for v in M[rk]]; R = M[rk]
        for i in range(len(M)):
            if i != rk and M[i][c]:
                f = M[i][c]; M[i] = [(a - f * b) % p for a, b in zip(M[i], R)]
        rk += 1
    return rk
T = {4: 7, 8: 19, 16: 52, 64: 304, 256: None}
for j in (2, 3, 4):
    q = 1 << j; k = 2 * j; N = q * q; rnd = random.Random(j)
    spread = [[a | (gmul(m, a, j) << j) for a in range(q)] for m in range(q)] + [[b << j for b in range(q)]]
    cover = sorted(x for S in spread for x in S if x)
    assert cover == list(range(1, N)), "not a spread"
    f = [rnd.randrange(-9, 10) for _ in range(N)]
    Hf = [sum((-1) ** dot(x, y) * f[x] for x in range(N)) for y in range(N)]
    lines = []; ok = True; selfperp = 0; perp_in_spread = 0
    for S in spread:
        V = [x for x in range(N) if all(dot(x, s) == 0 for s in S)]
        assert len(V) == q
        if sorted(V) == sorted(S): selfperp += 1
        if any(sorted(V) == sorted(S2) for S2 in spread): perp_in_spread += 1
        seen = set(); cos = []
        for x in range(N):
            if x in seen: continue
            c = sorted(x ^ v for v in V); seen.update(c); cos.append(c)
        sums = [sum(f[x] for x in c) for c in cos]; lines += cos
        for y in S:                                  # (-1)^(x.y) is constant on a coset of V because y is in S = V-perp
            if Hf[y] != sum((-1) ** dot(c[0], y) * s for c, s in zip(cos, sums)): ok = False
    M = [[1 if x in set(c) else 0 for x in range(N)] for c in lines]
    pair2 = sum(1 for a in range(len(lines)) for b in range(a) if len(set(lines[a]) & set(lines[b])) > 1)
    rq = rank_frac(M) if N <= 64 else rank_p(M, 1000003)
    print("q=%2d N=%3d : spread of %d subspaces ok ; slice identity on all %d outputs: %s ; lines %d, points per line %d ; pairs of lines sharing 2 points: %d" % (q, N, q + 1, N, ok, len(lines), q, pair2))
    print("        rank of the line-sum matrix: %d (%s), modulo 2: %d, modulo 3: %d ; subspaces equal to their own perpendicular: %d ; perpendicular again in the spread: %d of %d" % (
        rq, "rationals" if N <= 64 else "modulo 1000003", rank_p(M, 2), rank_p(M, 3), selfperp, perp_in_spread, q + 1))
    print("        adding-only cost of the line sums (no two lines share two points): (q^2+q)(q-1) = %d ; textbook N log2 N = %d" % ((q * q + q) * (q - 1), N * k))
print("== the recursion T(N) <= R(N) + (sqrt N + 1) T(sqrt N): gates per point if R(N) <= beta N at every size (beta = 1, 2), N = 2^(2^t)")
for beta in (1, 2):
    c = 0.5; out = []                      # T(2)/2 = 1/2
    for t in range(1, 9):
        Nn = 2.0 ** (2 ** t); c = beta + (1 + Nn ** -0.5) * c; out.append("2^%d: %.2f (textbook %d)" % (2 ** t, c, 2 ** t))
    print("   beta = %d : " % beta + " ; ".join(out))
