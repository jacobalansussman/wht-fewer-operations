# Hybrid 4: the window. (-1)^m, m = number of common ones of input and output address, needs degree k as a polynomial in m
# on all of 0..k, but only (window length - 1) on a window of values of m. How much of the matrix does a window cover?
from fractions import Fraction as F
from math import comb, log2
for k in (16, 64, 256, 1024, 4096):
    mass = [comb(k, m) * 3 ** (k - m) for m in range(k + 1)]; tot = 4 ** k
    for dl in (F(1, 10), F(1, 100), F(1, 10 ** 6)):
        lo = hi = max(range(k + 1), key=lambda m: mass[m]); s = mass[lo]
        while s < (1 - dl) * tot:
            if lo > 0 and (hi == k or mass[lo - 1] >= mass[hi + 1]): lo -= 1; s += mass[lo]
            else: hi += 1; s += mass[hi]
        d = hi - lo; rk = sum(comb(k, j) for j in range(d + 1))
        print(f"k={k}: window m={lo}..{hi} covers all but {float(1 - F(s, tot)):.2e} of the entries; degree {d} of {k}; "
              f"rank at most 2^{log2(rk):.1f} of 2^{k}")
# exact check at 64 points
k = 6; N = 64; W = [0, 1, 2, 3]
def p(m):
    s = F(0)
    for a in W:
        t = F((-1) ** a)
        for b in W:
            if b != a: t *= F(m - b, a - b)
        s += t
    return s
pv = [p(m) for m in range(k + 1)]
cm = lambda x, y: bin(x & y).count('1')
P = [[pv[cm(x, y)] for x in range(N)] for y in range(N)]
bad = sum(1 for x in range(N) for y in range(N) if P[y][x] != (-1) ** cm(x, y))
def rank(M):
    M = [r[:] for r in M]; rk = 0
    for c in range(len(M[0])):
        q = next((r for r in range(rk, len(M)) if M[r][c] != 0), None)
        if q is None: continue
        M[rk], M[q] = M[q], M[rk]
        for r in range(len(M)):
            if r != rk and M[r][c] != 0:
                f = M[r][c] / M[rk][c]; M[r] = [a - f * b for a, b in zip(M[r], M[rk])]
        rk += 1
    return rk
print(f"64 points, window m=0..3 (degree 3): entries where the polynomial differs from the transform {bad} of {N*N} "
      f"({bad/N/N:.3f}); rank of the polynomial part {rank(P)} (bound {sum(comb(6,j) for j in range(4))}); values of p at m=0..6: {[str(v) for v in pv]}")
