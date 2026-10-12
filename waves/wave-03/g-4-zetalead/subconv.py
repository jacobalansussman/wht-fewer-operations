# g-4-zetalead / subconv.py : (1) subset convolution run through the three-call word, against the direct 3^k sum; exact rationals.
#                             (2) two identities for the cube's "add one element" operator U, exact integers.
# Subset convolution: (f*g)(S) = sum over T inside S of f(T) g(S minus T).
# Method of Bjorklund, Husfeldt, Kaski and Koivisto (2007): split f and g by set size ("rank"), take the subset-sum transform of
# every slice, multiply the two polynomials in the rank variable at every set S, invert every slice, read slice |S| at S.
# Here every subset-sum transform and every inverse is done by THREE Walsh-Hadamard transforms and four scalings.
from fractions import Fraction as Fr
import random, sys

def fwht(x, cnt):
    x = list(x); n = len(x); h = 1
    while h < n:
        for i in range(0, n, 2 * h):
            for j in range(i, i + h):
                u, v = x[j], x[j + h]; x[j], x[j + h] = u + v, u - v; cnt[0] += 2
        h *= 2
    return x
def scale(x, r, cnt):
    out = []
    for i, v in enumerate(x):
        c = r ** bin(i).count("1")
        if c != 1: cnt[0] += 1
        out.append(c * v)
    return out
ZETA = (Fr(5, 4), Fr(1, 3), Fr(-1, 2), Fr(3, 5))        # applied in this order, a transform between consecutive scalings
MOEB = (Fr(-5, 4), Fr(1, 3), Fr(-1, 2), Fr(-3, 5))
def by_word(x, w, cnt):
    y = scale(x, w[0], cnt)
    for r in w[1:]:
        y = scale(fwht(y, cnt), r, cnt)
    return y

random.seed(9)
print("== 1. subset convolution through the word ==")
print("   k    N   transforms used   operations in the transforms   = 3(k+1) (3kN + 4(N-1))   Yates would use 3(k+1) k N/2   rank products (schoolbook)   equal to the direct sum")
for k in range(1, 8):
    N = 1 << k
    f = [Fr(random.randint(-5, 5), random.randint(1, 4)) for _ in range(N)]
    g = [Fr(random.randint(-5, 5), random.randint(1, 4)) for _ in range(N)]
    direct = []
    for S in range(N):
        t = S; acc = Fr(0)
        while True:
            acc += f[t] * g[S ^ t]
            if t == 0: break
            t = (t - 1) & S
        direct.append(acc)
    cnt = [0]; pc = [bin(S).count("1") for S in range(N)]
    fh = [by_word([f[S] if pc[S] == j else Fr(0) for S in range(N)], ZETA, cnt) for j in range(k + 1)]
    gh = [by_word([g[S] if pc[S] == j else Fr(0) for S in range(N)], ZETA, cnt) for j in range(k + 1)]
    prods = 0; hh = [[Fr(0)] * N for _ in range(k + 1)]
    for S in range(N):
        for i in range(k + 1):
            for j in range(i + 1):
                hh[i][S] += fh[j][S] * gh[i - j][S]; prods += 1
    out = [None] * N
    for i in range(k + 1):
        m = by_word(hh[i], MOEB, cnt)
        for S in range(N):
            if pc[S] == i: out[S] = m[S]
    ok = out == direct
    print("  %2d %4d %12d %22d %30d %30d %25d %20s" % (k, N, 3 * (k + 1), cnt[0], 3 * (k + 1) * (3 * k * N + 4 * (N - 1)), 3 * (k + 1) * k * N // 2, prods, ok))
    assert ok and cnt[0] == 3 * (k + 1) * (3 * k * N + 4 * (N - 1))

print("== 2. the 'add one element' operator U of the cube ==")
# U x at S = sum of x at S minus one element.  A = U + U^T = sum over the k neighbours.  W = diag(|S|).
# (i)  U = (A + W A - A W) / 2      (so U costs two neighbour sums, and a neighbour sum is two transforms and one scaling)
# (ii) A = (1/N) H diag(k - 2|S|) H
# (iii) W Z - Z W = U Z             (the subset-sum transform is exp(U); scaling it by t^|S| on both sides moves along the flow)
def mm(A, B):
    n = len(A); Bt = list(zip(*B))
    return [[sum(a * b for a, b in zip(r, c) if a and b) for c in Bt] for r in A]
for k in range(1, 7):
    N = 1 << k
    U = [[1 if (S & T) == T and bin(S ^ T).count("1") == 1 else 0 for T in range(N)] for S in range(N)]
    A = [[U[i][j] + U[j][i] for j in range(N)] for i in range(N)]
    Wd = [bin(S).count("1") for S in range(N)]
    WA = [[Wd[i] * A[i][j] for j in range(N)] for i in range(N)]
    AW = [[A[i][j] * Wd[j] for j in range(N)] for i in range(N)]
    i1 = all(2 * U[i][j] == A[i][j] + WA[i][j] - AW[i][j] for i in range(N) for j in range(N))
    Hm = [[1 - 2 * (bin(i & j).count("1") & 1) for j in range(N)] for i in range(N)]
    HD = [[Hm[i][j] * (k - 2 * Wd[j]) for j in range(N)] for i in range(N)]
    i2 = mm(HD, Hm) == [[N * A[i][j] for j in range(N)] for i in range(N)]
    Zm = [[1 if (S & T) == T else 0 for T in range(N)] for S in range(N)]
    WZ = [[Wd[i] * Zm[i][j] for j in range(N)] for i in range(N)]
    ZW = [[Zm[i][j] * Wd[j] for j in range(N)] for i in range(N)]
    UZ = mm(U, Zm)
    i3 = all(WZ[i][j] - ZW[i][j] == UZ[i][j] for i in range(N) for j in range(N))
    print("   k=%d  U = (A + WA - AW)/2: %s   N A = H diag(k-2|S|) H: %s   WZ - ZW = UZ: %s" % (k, i1, i2, i3))
    assert i1 and i2 and i3
print("done")
