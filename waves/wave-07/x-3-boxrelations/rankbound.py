# x-3 boxrelations: the telescoping bound, exact (fractions).
# LEMMA. A call program with r calls whose output is F(A) satisfies rank(F(A) - F(A')) <= r * rank(A - A') for ANY two boxes A, A'.
#   (c_j - c'_j = (A - A') w_j + A' sum_i M_ji (c_i - c'_i), so F(A) - F(A') = sum_j P''_j (A - A') w_j.)
# So a program that is right on a family needs r >= rank(A (x) A - A' (x) A') / rank(A - A') for every pair A, A' in the family.
# This file computes that number for the closest pairs of each family, K = 2, 4, 6, 8.
from fractions import Fraction as F
import sys
def rank(M):
    M = [r[:] for r in M]; rk = 0; rows = len(M); cols = len(M[0])
    for c in range(cols):
        p = next((i for i in range(rk, rows) if M[i][c] != 0), None)
        if p is None: continue
        M[rk], M[p] = M[p], M[rk]; pv = M[rk][c]
        for i in range(rk + 1, rows):
            if M[i][c] != 0:
                f = M[i][c]/pv; M[i] = [a - f*b for a, b in zip(M[i], M[rk])]
        rk += 1
        if rk == rows: break
    return rk
def kron(A, B):
    K = len(A); return [[A[i][j]*B[k][l] for j in range(K) for l in range(K)] for i in range(K) for k in range(K)]
def sub(A, B): return [[a - b for a, b in zip(r, s)] for r, s in zip(A, B)]
def mm(A, B): return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def eye(K): return [[F(int(i == j)) for j in range(K)] for i in range(K)]
def plane(K, a, b, c, s):
    R = eye(K); R[a][a] = c; R[b][b] = c; R[a][b] = -s; R[b][a] = s; return R
def tr(A): return [list(r) for r in zip(*A)]
print('family            K  rank(A-A\')  rank(A(x)A - A\'(x)A\')  calls needed >=   textbook 2K')
for K in (2, 4, 6, 8):
    c, s = F(3, 5), F(4, 5); h = K//2
    A0 = [[F(int(i == j))*(1 if i < K - h else -1) for j in range(K)] for i in range(K)]
    import random; random.seed(100 + K); G = [[F(random.randint(-9, 9)) for j in range(K)] for i in range(K)]; assert rank(G) == K   # a fixed invertible matrix without structure
    Gs = [[G[i][j] + G[j][i] for j in range(K)] for i in range(K)]
    cases = []
    E = [[F(0)]*K for _ in range(K)]; E[0][K-1] = F(1)
    cases.append(('generic', G, [[G[i][j] + E[i][j] for j in range(K)] for i in range(K)]))
    E2 = [[F(0)]*K for _ in range(K)]; E2[0][0] = F(1)
    cases.append(('symmetric', Gs, [[Gs[i][j] + E2[i][j] for j in range(K)] for i in range(K)]))
    Ai = [[A0[i][j] - 2*E[i][j] for j in range(K)] for i in range(K)]; assert mm(Ai, Ai) == eye(K)
    cases.append(('involution', A0, Ai))
    R = plane(K, 0, 1, c, s); cases.append(('rotation', eye(K), R))
    R2 = plane(K, 0, K - 1, c, s); Ar = mm(mm(R2, A0), tr(R2)); assert mm(Ar, Ar) == eye(K) and Ar == tr(Ar)
    cases.append(('reflection', A0, Ar))
    cases.append(('scalings t*A0', A0, [[2*v for v in r] for r in A0]))
    for name, A, B in cases:
        r1 = rank(sub(A, B)); r2 = rank(sub(kron(A, A), kron(B, B)))
        print('%-16s %2d  %6d  %14d  %18d  %12d' % (name, K, r1, r2, -(-r2//r1), 2*K), flush=True)
