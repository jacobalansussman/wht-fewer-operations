# x-7-rotate120 / fused.py : exact (fractions) at 4, 16, 64 points.
# (1) the three mirrors add up to something that lives on the fixed space of R:  S + S R + S R^2 = 3 S P0,  P0 = (1 + R + R^2)/3
# (2) S R = R S R^-1 : the second mirror is the first one turned by R (so is the third)
# (3) rank(R - 1) = 2(N-1)/3 ; with mirrors that are +1 on the whole fixed space, each S = 1 - 2 P with rank P = (N-1)/3, and
#     R = 1 - 2 P1 - 2 P2 + 4 P1 P2   (the pair used at once, not one after the other)
# (4) uncertainty for a pair: for an eigenvector v of S2, supp(v) * supp(S1 v) >= N  (checked on the columns of P2 and 1 - P2)
import sys
sys.path.insert(0, '.')
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
    Bt = list(zip(*B)); return [[sum(a * b for a, b in zip(r, c) if a and b) for c in Bt] for r in A]
def lin(*terms):
    N = len(terms[0][1]); return [[sum(c * M[i][j] for c, M in terms) for j in range(N)] for i in range(N)]
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
for n in (1, 2, 3):
    N, H, D = build(n); I = [[Fr(int(i == j)) for j in range(N)] for i in range(N)]; s = Fr(1, 1 << n)
    R = [[x * s for x in r] for r in mul(D, H)]; R2 = mul(R, R)
    P0 = lin((Fr(1, 3), I), (Fr(1, 3), R), (Fr(1, 3), R2))
    S, S2, S3 = D, mul(D, R), mul(D, R2)
    print('N=%d  (1) S + S R + S R^2 == 3 S P0 : %s   (2) S R == R S R^-1 : %s   rank P0 = %d  rank(R - 1) = %d = 2(N-1)/3 = %d' % (
        N, lin((1, S), (1, S2), (1, S3)) == mul(lin((3, S)), P0), S2 == mul(mul(R, S), R2), rank(P0), rank(lin((1, R), (-1, I))), 2 * (N - 1) // 3))
    # mirrors that are +1 on the whole fixed space: S1 = D (1 - 2 P0m), P0m = part of P0 where D = -1
    P0m = lin((Fr(1, 2), mul(P0, lin((1, I), (-1, D)))))
    S1 = mul(D, lin((1, I), (-2, P0m))); S2 = mul(S1, R)
    assert mul(S1, S1) == I and mul(S2, S2) == I and mul(mul(S1, R), S1) == R2
    P1 = lin((Fr(1, 2), I), (Fr(-1, 2), S1)); P2 = lin((Fr(1, 2), I), (Fr(-1, 2), S2))
    fused = lin((1, I), (-2, P1), (-2, P2), (4, mul(P1, P2)))
    print('      (3) mirrors +1 on the fixed space: rank P1 = %d, rank P2 = %d, (N-1)/3 = %d ; R == 1 - 2P1 - 2P2 + 4 P1 P2 : %s ; non-zeros of P1: %d, of P2: %d ; row weights of S1: %s' % (
        rank(P1), rank(P2), (N - 1) // 3, fused == R, sum(1 for r in P1 for x in r if x), sum(1 for r in P2 for x in r if x), sorted(set(sum(1 for x in r if x) for r in S1))))
    # (4) columns of P2 are anti-mirror vectors of S2, columns of 1 - P2 mirror vectors: check supp(v) * supp(S1 v) >= N
    worst = None
    for Mx in (P2, lin((1, I), (-1, P2))):
        Mt = list(zip(*Mx)); SMt = list(zip(*mul(S1, Mx)))
        for v, w in zip(Mt, SMt):
            a = sum(1 for x in v if x); b = sum(1 for x in w if x)
            if a and (worst is None or a * b < worst[0]): worst = (a * b, a, b)
    print('      (4) least supp(v) * supp(S1 v) over those eigenvectors of S2: %d = %d * %d   (N = %d)' % (worst + (N,)))
