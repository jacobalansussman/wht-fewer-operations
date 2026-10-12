#!/usr/bin/env python3
"""quad.py: nu(S,U) for the quadric pair S = {x0 x1 + x2 = 0}, U = {y1 y3 + y4 = 0} at N = 2^k points, k >= 5. Exact (Python integers).
nu = rank( E (N - E) ), E = H[S,U] H[S,U]^T.  Prediction of g-6.md: nu = N/8."""
import sys

def exact_rank(M):
    M = [row[:] for row in M]
    n = len(M); m = len(M[0])
    r = 0; prev = 1
    for c in range(m):
        piv = next((i for i in range(r, n) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        for i in range(r + 1, n):
            Mi, Mr, f = M[i], M[r], M[i][c]
            p = Mr[c]
            for j in range(c + 1, m):
                Mi[j] = (Mi[j] * p - f * Mr[j]) // prev
            Mi[c] = 0
        prev = M[r][c]
        r += 1
        if r == n:
            break
    return r

for k in [int(v) for v in sys.argv[1:]]:
    N = 1 << k
    b = lambda v, i: (v >> i) & 1
    S = [x for x in range(N) if (b(x, 0) & b(x, 1)) ^ b(x, 2) == 0]
    U = [y for y in range(N) if (b(y, 1) & b(y, 3)) ^ b(y, 4) == 0]
    M = [[1 - 2 * (bin(x & y).count("1") & 1) for y in U] for x in S]
    E = [[sum(a * c for a, c in zip(r1, r2)) for r2 in M] for r1 in M]
    F = [[sum(E[i][t] * ((N if t == j else 0) - E[t][j]) for t in range(len(S))) for j in range(len(S))] for i in range(len(S))]
    print(f"k={k} N={N}: |S|={len(S)} |U|={len(U)} rank H[S,U]={exact_rank(M)} nu={exact_rank(F)} N/8={N//8}", flush=True)
