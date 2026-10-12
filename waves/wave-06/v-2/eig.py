# v-2: a rank count for reflection boxes A = 1 - 2P, P an orthogonal projection of rank m in K dimensions. Exact fractions.
# A program with r calls to A is a program with r calls to P (glue absorbs the rest), so (A kron A) - Q' = sum of r terms of rank <= m,
# with Q' fixed. Two members A, A' of the family then give rank(A kron A - A' kron A') <= 2 r m, that is r >= that rank / (2m).
from fractions import Fraction as F
import random
def mm(A, B): return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def tr(A): return [list(r) for r in zip(*A)]
def rank(M):
    M = [[F(v) for v in r] for r in M]; rk = 0
    for c in range(len(M[0])):
        p = next((i for i in range(rk, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[rk], M[p] = M[p], M[rk]
        for i in range(len(M)):
            if i != rk and M[i][c] != 0:
                f = M[i][c]/M[rk][c]; M[i] = [a - f*b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk
def inv(M):
    n = len(M); A = [[F(v) for v in r] + [F(int(i == j)) for j in range(n)] for i, r in enumerate(M)]
    for c in range(n):
        p = next(i for i in range(c, n) if A[i][c] != 0); A[c], A[p] = A[p], A[c]; d = A[c][c]; A[c] = [v/d for v in A[c]]
        for i in range(n):
            if i != c and A[i][c] != 0: f = A[i][c]; A[i] = [a - f*b for a, b in zip(A[i], A[c])]
    return [r[n:] for r in A]
def refl(K, m, rng):
    B = [[F(rng.randint(-4, 4)) for _ in range(m)] for _ in range(K)]
    while rank(B) < m: B = [[F(rng.randint(-4, 4)) for _ in range(m)] for _ in range(K)]
    P = mm(mm(B, inv(mm(tr(B), B))), tr(B))
    return [[F(int(i == j)) - 2*P[i][j] for j in range(K)] for i in range(K)]
def kron(A, B): return [[A[i][j]*B[k][l] for j in range(len(A)) for l in range(len(B))] for i in range(len(A)) for k in range(len(B))]
rng = random.Random(3)
print('  K  m   largest rank(A kron A - A\' kron A\') over 6 random rational pairs   calls r >= rank/(2m)   sealed box 2K')
for K, m in ((2, 1), (3, 1), (4, 1), (4, 2), (5, 1), (6, 3), (8, 4)):
    best = 0
    for _ in range(6 if K < 8 else 2):
        A = refl(K, m, rng); A2 = refl(K, m, rng)
        assert mm(A, A) == [[F(int(i == j)) for j in range(K)] for i in range(K)] and A == tr(A)
        kA = kron(A, A); kB = kron(A2, A2); best = max(best, rank([[a - b for a, b in zip(r1, r2)] for r1, r2 in zip(kA, kB)]))
    print('%3d %2d   %6d                                                          %6.1f -> %d            %3d' % (K, m, best, best/(2*m), -((-best)//(2*m)), 2*K), flush=True)
