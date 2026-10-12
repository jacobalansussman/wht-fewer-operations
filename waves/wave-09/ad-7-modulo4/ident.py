#!/usr/bin/env python3
"""ident.py [ad-7]  Three modulo-2 savings as the constant term of one binomial expansion (whole numbers, k = 2..5).
 (a) transform: H = sum over sets S of address bits of (-2)^|S| (E on the bits of S, all-ones J on the others), E = [[0,0],[0,1]]
 (b) subset sums relabelled: M = [[1,1],[1,0]], (M tensor k)^3 = sum over S of 2^|S| (M on the bits of S, identity elsewhere)
 (c) neighbour sums: A^2 = k + 2 A_2 (A_2 = sums over the addresses at distance 2), and A A_j = (j+1) A_(j+1) + (k-j+1) A_(j-1)"""
import itertools
def kron(A, B): return [[a * b for a in ra for b in rb] for ra in A for rb in B]
def mul(A, B): return [[sum(a * b for a, b in zip(r, c)) for c in zip(*B)] for r in A]
def add(A, B, s=1): return [[a + s * b for a, b in zip(r, q)] for r, q in zip(A, B)]
def tens(fs):
    M = [[1]]
    for f in fs: M = kron(M, f)
    return M
I2 = [[1, 0], [0, 1]]; J2 = [[1, 1], [1, 1]]; E = [[0, 0], [0, 1]]; H2 = [[1, 1], [1, -1]]; Mm = [[1, 1], [1, 0]]
for k in range(2, 6):
    N = 1 << k
    H = tens([H2] * k); S1 = [[0] * N for _ in range(N)]; S2 = [[0] * N for _ in range(N)]
    for bits in itertools.product((0, 1), repeat=k):
        w = sum(bits)
        T1 = tens([E if b else J2 for b in bits]); S1 = add(S1, [[(-2) ** w * c for c in r] for r in T1])
        T2 = tens([Mm if b else I2 for b in bits]); S2 = add(S2, [[2 ** w * c for c in r] for r in T2])
    Mk = tens([Mm] * k); M3 = mul(Mk, mul(Mk, Mk))
    Aj = [[[1 if bin(x ^ y).count('1') == j else 0 for x in range(N)] for y in range(N)] for j in range(k + 2)]
    okc = all(mul(Aj[1], Aj[j]) == add([[(j + 1) * c for c in r] for r in Aj[j + 1]], [[(k - j + 1) * c for c in r] for r in Aj[j - 1]]) for j in range(1, k + 1))
    print("k=%d: (a) %s  (b) %s  (c) %s" % (k, H == S1, M3 == S2, okc))
