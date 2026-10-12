#!/usr/bin/env python3
"""fourier_check.py: the Fourier form of Lemma A (g-6.md section 3), exact integers, 32 points.
Identity claimed:  sum over d != 0 of f_U(d)^2 * |S minus (S+d)|  =  || H[S,U] H[S^c,U]^T ||_F^2   (= N^2 * sum of sin^2 cos^2),
and the bound  <= N^2 * nu / 4.   f_U(d) = sum over y in U of (-1)^(y.d)."""
import random
from quad import exact_rank
N = 32
b = lambda v, i: (v >> i) & 1
sgn = lambda x, y: 1 - 2 * (bin(x & y).count("1") & 1)
def check(name, S, U):
    Sc = [x for x in range(N) if x not in S]
    f = [sum(sgn(y, d) for y in U) for d in range(N)]
    Ss = set(S)
    lhs = sum(f[d] ** 2 * sum(1 for x in S if (x ^ d) not in Ss) for d in range(1, N))
    G = [[sum(sgn(x, y) * sgn(x2, y) for y in U) for x2 in Sc] for x in S]
    rhs = sum(v * v for row in G for v in row)
    M = [[sgn(x, y) for y in U] for x in S]
    E = [[sum(a * c for a, c in zip(r1, r2)) for r2 in M] for r1 in M]
    F = [[sum(E[i][t] * ((N if t == j else 0) - E[t][j]) for t in range(len(S))) for j in range(len(S))] for i in range(len(S))]
    nu = exact_rank(F)
    print(f"{name}: left side {lhs}, Frobenius side {rhs}, equal {lhs == rhs}; nu={nu}, bound N^2 nu/4 = {N*N*nu//4}, holds {lhs <= N*N*nu/4}")
check("quadric pair", [x for x in range(N) if (b(x,0)&b(x,1))^b(x,2)==0], [y for y in range(N) if (b(y,1)&b(y,3))^b(y,4)==0])
check("tight hyperplanes", [x for x in range(N) if b(x,0)==0], [y for y in range(N) if b(y,1)==0])
rnd = random.Random(5)
for i in range(3):
    check(f"random pair {i}", sorted(rnd.sample(range(N), 16)), sorted(rnd.sample(range(N), 16)))
check("random 8 against 16", sorted(rnd.sample(range(N), 8)), sorted(rnd.sample(range(N), 16)))
