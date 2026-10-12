#!/usr/bin/env python3
"""d-7-spin: (1) the pair scheme checked exactly at 4, 16, 64 points; (2) exact determinant of the valence-bond basis."""
from fractions import Fraction as Fr
from math import log2
import spin

def kron(A, B):
    return [[a * b for a in ra for b in rb] for ra in A for rb in B]
def mul(A, B):
    Bt = list(zip(*B)); return [[sum(x * y for x, y in zip(r, c) if x and y) for c in Bt] for r in A]
h = [[1, 1], [1, -1]]
H4 = kron(h, h)
# coordinates after 'in' on one pair, ordered (x00, x01+x10, x11 ; x01-x10)
b = [[1, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 1], [0, 1, -1, 0]]
binv = [[1, 0, 0, 0], [0, Fr(1, 2), 0, Fr(1, 2)], [0, Fr(1, 2), 0, Fr(-1, 2)], [0, 0, 1, 0]]
assert mul(b, binv) == [[int(i == j) for j in range(4)] for i in range(4)]
m = mul(mul(b, H4), binv)
print("one pair: b H4 b^-1 =", [[int(v) for v in r] for r in m])
B, Bi, M, H = [[1]], [[1]], [[1]], [[1]]
for pairs in (1, 2, 3):
    B, Bi, M, H = kron(B, b), kron(Bi, binv), kron(M, m), kron(H, H4)
    ok = mul(mul(Bi, M), B) == H
    N = 4 ** pairs
    # 'in' restricted to a swap orbit with s unequal pairs is the 2^s-point Walsh matrix: count orbit sizes
    nb = sum(sum(1 for v in r if v) - 1 for r in B)          # additions if every row is summed term by term
    print("pairs=%d N=%d  B^-1 M B == H: %s   nnz(M)=%d (%.3f per entry)" % (pairs, N, ok, sum(1 for r in M for v in r if v), sum(1 for r in M for v in r if v) / N))

def det_bareiss(A):
    n = len(A); A = [r[:] for r in A]; prev = 1; sign = 1
    for i in range(n - 1):
        if A[i][i] == 0:
            p = next((r for r in range(i + 1, n) if A[r][i]), None)
            if p is None: return 0
            A[i], A[p] = A[p], A[i]; sign = -sign
        for r in range(i + 1, n):
            for c in range(i + 1, n):
                A[r][c] = (A[r][c] * A[i][i] - A[r][i] * A[i][c]) // prev
        prev = A[i][i]
    return sign * A[-1][-1]
print("exact determinant of the valence-bond basis S (it cancels between in and out; the transform's own is 2^(kN/2))")
for k in (2, 3, 4, 5, 6):
    N = 1 << k
    A = [[0] * N for _ in range(N)]
    for x in range(N):
        arcs, U, t = spin.skeleton(x, k)
        for y, c in spin.vb_vector(arcs, U, t, k).items(): A[y][x] = c
    dt = abs(det_bareiss(A))
    f, q, fac = dt, 2, {}
    while q * q <= f:
        while f % q == 0: fac[q] = fac.get(q, 0) + 1; f //= q
        q += 1
    if f > 1: fac[f] = fac.get(f, 0) + 1
    print("   k=%d |det S| = %d = %s   log2/N = %.4f   (transform: k/2 = %.1f)" % (k, dt, fac, log2(dt) / N, k / 2))
