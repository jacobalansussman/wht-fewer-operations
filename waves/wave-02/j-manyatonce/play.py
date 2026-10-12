#!/usr/bin/env python3
"""play.py : exact integer checks for j-manyatonce (seconds)."""
from fractions import Fraction as Fr
import itertools, random
def had(k):
    N = 1 << k
    return [[(-1) ** bin(i & j).count("1") for j in range(N)] for i in range(N)]
def mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def ident(n): return [[int(i == j) for j in range(n)] for i in range(n)]
random.seed(7)
# 1. N shifted copies: X[a][b] = x[a^b]  =>  H X = diag(Hx) H   and   H X H = N diag(Hx)
for k in (2, 3, 4):
    N = 1 << k; H = had(k); x = [random.randint(-9, 9) for _ in range(N)]
    X = [[x[a ^ b] for b in range(N)] for a in range(N)]
    xh = [sum(H[w][a] * x[a] for a in range(N)) for w in range(N)]
    HX = mul(H, X)
    ok1 = all(HX[w][b] == xh[w] * H[w][b] for w in range(N) for b in range(N))
    HXH = mul(HX, H)
    ok2 = all(HXH[w][v] == (N * xh[w] if w == v else 0) for w in range(N) for v in range(N))
    print(f"shifted copies N={N}: HX = diag(Hx)H {ok1};  HXH = N diag(Hx) {ok2}")
# 2. general batch in 'shift-and-sign' coordinates: X = sum_c Z^c Circ(m_c)  =>  HX = sum_c S^c diag(Hm_c) H
for k in (2, 3):
    N = 1 << k; H = had(k)
    m = [[random.randint(-5, 5) for _ in range(N)] for c in range(N)]          # m[c][a]
    X = [[sum(H[c][a] * m[c][a ^ b] for c in range(N)) for b in range(N)] for a in range(N)]   # Z^c = diag(H[c])
    HX = mul(H, X)
    mh = [[sum(H[w][a] * m[c][a] for a in range(N)) for w in range(N)] for c in range(N)]
    R = [[sum(mh[c][w ^ c] * H[w ^ c][b] for c in range(N)) for b in range(N)] for w in range(N)]
    print(f"general batch N={N}: HX = sum_c S^c diag(H m_c) H  {HX == R}")
# 3. two copies as three shears (Whitehead): diag(H, H^-1) = [[I,H],[0,I]] [[I,0],[-H^-1,I]] [[I,H],[0,I]] [[0,-I],[I,0]]
for k in (1, 2, 3):
    N = 1 << k; H = [[Fr(v) for v in r] for r in had(k)]; Hi = [[v / N for v in r] for r in H]
    I = [[Fr(v) for v in r] for r in ident(N)]; Z = [[Fr(0)] * N for _ in range(N)]
    def blk(A, B, C, D): return [A[i] + B[i] for i in range(N)] + [C[i] + D[i] for i in range(N)]
    neg = lambda A: [[-v for v in r] for r in A]
    U = blk(I, H, Z, I); L = blk(I, Z, neg(Hi), I); W = blk(Z, neg(I), I, Z)
    P = mul(mul(mul(U, L), U), W)
    print(f"three shears N={N}: equals diag(H, H^-1) {P == blk(H, Z, Z, Hi)}")
# 4. product form: gates to transform a sum of r product terms, r = generic rank ceil(2^k/(k+1)); tensor-train count
for k in (3, 4, 8, 16, 20):
    N = 1 << k; r = -(-N // (k + 1))
    tt = sum(2 * min(2 ** (j - 1), 2 ** (k - j + 1)) * min(2 ** j, 2 ** (k - j)) for j in range(1, k + 1))
    print(f"k={k:2d} N={N}: textbook {N*k} | sum of {r} products: {2*k*r} gates ({2*k*r/N:.3f} N) | tensor-train entries {tt} ({tt/N:.3f} N)")
# 5. the ladder: discount theta at N copies  <->  exponent z = log2(1 + theta)
import math
for z in (1 - 8.7625e-4, 0.99, 0.9, 0.5, 0.1):
    print(f"z = {z:.6f}  <->  N copies of the N-point transform for theta = {2**z - 1:.5f} of N separate ones")
