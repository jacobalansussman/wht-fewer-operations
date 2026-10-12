# x-7-rotate120 / n16.py : exact checks at 16 and 64 points (whole numbers; matrices kept times a power of 2).
# R = D H / sqrt(N).  Checks: the starting facts; the size of the family; the "rows then columns" pair; the swap pair;
# how many non-zeros each mirror has; the three mirrors S, S R, S R^2 of each.
import sys
from fractions import Fraction as Fr
def pop(v): return bin(v).count('1')
def build(n):
    k = 2 * n; N = 1 << k
    Q = lambda x: sum(((x >> (2 * i)) & 1) * ((x >> (2 * i + 1)) & 1) for i in range(n)) & 1
    sw = lambda x: sum((((x >> (2 * i)) & 1) << (2 * i + 1)) | (((x >> (2 * i + 1)) & 1) << (2 * i)) for i in range(n))
    H = [[Fr((-1) ** pop(x & sw(y))) for y in range(N)] for x in range(N)]
    D = [[Fr((-1) ** Q(x)) if x == y else Fr(0) for y in range(N)] for x in range(N)]
    return N, H, D
def mul(A, B):
    n = len(A); m = len(B[0]); Bt = list(zip(*B))
    return [[sum(a * b for a, b in zip(r, c) if a and b) for c in Bt] for r in A]
def sc(A, s): return [[x * s for x in r] for r in A]
def eye(N): return [[Fr(int(i == j)) for j in range(N)] for i in range(N)]
def kron(A, B): return [[a * b for a in ra for b in rb] for ra in A for rb in B]
def nnz(A): return sum(1 for r in A for x in r if x)
def rownnz(A): return sorted(set(sum(1 for x in r if x) for r in A))
def tr(A): return sum(A[i][i] for i in range(len(A)))
def rank(M):
    M = [r[:] for r in M]; rk = 0
    for c in range(len(M[0])):
        s = next((i for i in range(rk, len(M)) if M[i][c]), None)
        if s is None: continue
        M[rk], M[s] = M[s], M[rk]
        for i in range(rk + 1, len(M)):
            if M[i][c]:
                f = M[i][c] / M[rk][c]; M[i] = [a - f * b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk
def info(name, S, R, Rinv, I):
    ok = mul(S, S) == I and mul(mul(S, R), S) == Rinv
    N = len(S)
    return '%-34s mirror=%s trace=%s row non-zeros=%s total=%d' % (name, ok, tr(S), rownnz(S), nnz(S))
N4, H4, D4 = build(1)
R4 = sc(mul(D4, H4), Fr(1, 2)); I4 = eye(4)
assert mul(mul(R4, R4), R4) == I4
for n in (1, 2, 3):
    N, H, D = build(n); I = eye(N); s = Fr(1, 1 << n)
    R = sc(mul(D, H), s); Rinv = sc(mul(H, D), s)
    assert mul(R, Rinv) == I and mul(mul(R, R), R) == I
    print('N=%d  R^3 = 1: True ; trace R = %s' % (N, tr(R)))
    # the family: X with X R = R^-1 X  (X = D g, g commuting with R)
    if N <= 16:
        rows = []
        for i in range(N):
            for j in range(N):
                r = [Fr(0)] * (N * N)
                for t in range(N):
                    r[i * N + t] += R[t][j]; r[t * N + j] -= Rinv[i][t]
                rows.append(r)
        d = N * N - rank(rows)
        f = (N + 2) // 3; m = (N - 1) // 3
        print('  dimension of {X : X R = R^-1 X} = %d ; expected (fixed)^2 + 2 (rest/2)^2 = %d' % (d, f * f + 2 * m * m))
    # trivial triple
    print('  ' + info('D', D, R, Rinv, I))
    print('  ' + info('D R = H/sqrt N', mul(D, R), R, Rinv, I))
    print('  ' + info('D R^2 = D H D/sqrt N', mul(mul(D, R), R), R, Rinv, I))
    if n >= 2:
        # R_N = R_4 (x) R_(N/4) as a tensor product?  (address = first pair of bits, then the rest; check the order)
        Nb, Hb, Db = build(n - 1); sb = Fr(1, 1 << (n - 1)); Rb = sc(mul(Db, Hb), sb)
        for nm, T in (('R_4 (x) R_rest', kron(R4, Rb)), ('R_rest (x) R_4', kron(Rb, R4))):
            print('  %s == R : %s' % (nm, T == R))
        # the "rows then columns" pair: S1 = D_a (x) (D R^2)_b , S2 = (D R)_a (x) D_b   with the factorisation that holds
        A_D, A_DR, A_DR2 = D4, mul(D4, R4), mul(mul(D4, R4), R4)
        B_D, B_DR, B_DR2 = Db, mul(Db, Rb), mul(mul(Db, Rb), Rb)
        if kron(R4, Rb) == R: K = kron
        else: K = lambda a, b: kron(b, a)
        S1 = K(A_D, B_DR2); S2 = K(A_DR, B_D)
        print('  rows-then-columns pair:  S1 S2 == R : %s' % (mul(S1, S2) == R))
        print('  ' + info('S1 = D (x) D H D/sqrt', S1, R, Rinv, I))
        print('  ' + info('S2 = H/sqrt (x) D', S2, R, Rinv, I))
        print('  ' + info('third mirror S1 R^2', mul(mul(S1, R), R), R, Rinv, I))
        S1b = K(A_DR2, B_D); S2b = K(A_D, B_DR)
        print('  other split: S1 S2 == R : %s ; %s ; %s' % (mul(S1b, S2b) == R, info('', S1b, R, Rinv, I).strip(), info('', S2b, R, Rinv, I).strip()))
    if n == 2:
        # swap pair: S1 = SWAP (a (x) a^-1), with a any map that inverts R_4 (a = D R^j, or a = D g)
        def swapmat():
            P = [[Fr(0)] * 16 for _ in range(16)]
            for x in range(4):
                for y in range(4): P[4 * x + y][4 * y + x] = Fr(1)
            return P
        SW = swapmat()
        for nm, a, ainv in (('a = D', D4, D4), ('a = D R (= H/2)', mul(D4, R4), mul(D4, R4)), ('a = R^... D R^2', mul(mul(D4, R4), R4), mul(mul(D4, R4), R4))):
            S1 = mul(SW, kron(a, ainv)); S2 = mul(S1, R)
            print('  swap pair, %s: %s ; partner %s' % (nm, info('', S1, R, Rinv, I).strip(), info('', S2, R, Rinv, I).strip()))
        # a mixed one: change the sign of S on part of the fixed space of R (both mirrors change together)
        P0 = sc([[I[i][j] + R[i][j] + mul(R, R)[i][j] for j in range(N)] for i in range(N)], Fr(1, 3))
        # projector onto the part of the fixed space where D = -1  (vectors on Q = 1): P0m = P0 (1 - D)/2
        P0m = sc(mul(P0, [[I[i][j] - D[i][j] for j in range(N)] for i in range(N)]), Fr(1, 2))
        flip = [[I[i][j] - 2 * P0m[i][j] for j in range(N)] for i in range(N)]
        S1 = mul(D, flip); S2 = mul(S1, R)
        print('  D with the sign flipped on the fixed vectors living on Q = 1: %s ; partner %s' % (info('', S1, R, Rinv, I).strip(), info('', S2, R, Rinv, I).strip()))
