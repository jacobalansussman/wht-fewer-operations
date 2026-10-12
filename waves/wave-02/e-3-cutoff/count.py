#!/usr/bin/env python3
# e-3-cutoff, experiment 3: growth laws by exact counting, and three small exact matrix checks.
from math import comb, log2, sqrt
from fractions import Fraction as F
import random
wt = lambda v: bin(v).count("1")
def gbin(n, r):
    num = 1
    for q in range(r): num *= (n - q)
    f = 1
    for q in range(2, r + 1): f *= q
    return num // f
def cle(i, d): return sum(comb(i, j) for j in range(min(i, d) + 1))
def sums_cost(k, d): return sum(cle(i, d) << (k - i - 1) for i in range(k))          # additions of the counted program (checked in mat.py)
def window(k, target):
    p = [comb(k, t) * 3 ** (k - t) for t in range(k + 1)]; tot = 4 ** k
    best = None; lo = 0; s = 0
    for hi in range(k + 1):
        s += p[hi]
        while (s - p[lo]) * target.denominator >= target.numerator * tot: s -= p[lo]; lo += 1
        if s * target.denominator >= target.numerator * tot and (best is None or hi - lo < best[1] - best[0]): best = (lo, hi)
    return best
print("(1) the cut-off form at the 99% and 99.99% windows: additions of sums + spread, over N; against k (textbook, k N in (G) and (O))")
for k in (16, 64, 256, 1024, 4096):
    N = 1 << k; row = []
    for tg in (F(99, 100), F(9999, 10000)):
        a, b = window(k, tg); d = b - a
        M = cle(k, d); tot = 2 * sums_cost(k, d) - N + M
        row.append((d, float(F(tot, N)), log2(M)))
    print("  k=%5d   99%%: d=%3d cost %.1f N = %.2f sqrt(k) N, waist 2^%.0f   |  99.99%%: d=%3d cost %.1f N = %.2f sqrt(k) N, waist 2^%.0f   | k N: %d N"
          % (k, row[0][0], row[0][1], row[0][1] / sqrt(k), row[0][2], row[1][0], row[1][1], row[1][1] / sqrt(k), row[1][2], k))
print("(2) the exact two-piece program  H = cut-off(lower window d) + N * inverse of H on the heavy block  (heavy block = signs * ball of radius k-d-1, done by Moebius sums on the ball)")
for k in (16, 64, 256):
    N = 1 << k; best = None
    for d in range(0, k + 1):
        M = cle(k, d); w = k - d - 1
        ball = 2 * sum(j * comb(k, j) for j in range(0, w + 1)) if w >= 0 else 0
        tot = 2 * sums_cost(k, d) - N + M + ball
        if best is None or tot < best[0]: best = (tot, d)
        if d in (0, k // 4, k // 2, 3 * k // 4, k): print("    k=%d d=%d: total %.3f k N" % (k, d, float(F(tot, k * N))))
    print("  k=%d  cheapest at d=%d: %.4f k N" % (k, best[1], float(F(best[0], k * N))))
print("(3) weight classes: share of entries in class pairs (w,v) where at most d+1 overlaps occur, d = the 99% degree; and the degree needed for 99% when each class pair has its own window")
for k in (16, 64, 256):
    a, b = window(k, F(99, 100)); d = b - a
    thin = sum(comb(k, w) * comb(k, v) for w in range(k + 1) for v in range(k + 1) if min(w, v, k - w, k - v) <= d)
    # own window per class pair: overlap t given (w,v) is hypergeometric C(w,t)C(k-w,v-t)/C(k,v)
    need = None
    for dd in range(0, d + 1):
        cov = 0
        for w in range(k + 1):
            for v in range(k + 1):
                lo, hi = max(0, w + v - k), min(w, v)
                pr = [comb(w, t) * comb(k - w, v - t) for t in range(lo, hi + 1)]
                if len(pr) <= dd + 1: bestw = sum(pr)
                else:
                    s = sum(pr[:dd + 1]); bestw = s
                    for q in range(dd + 1, len(pr)):
                        s += pr[q] - pr[q - dd - 1]; bestw = max(bestw, s)
                cov += comb(k, w) * bestw            # = number of pairs (x,y) of this class pair inside its best window
        if cov * 100 >= 99 * 4 ** k: need = dd; break
    print("  k=%3d  global 99%% degree %2d;  share of entries in thin class pairs %.2e;  own window per class pair reaches 99%% at degree %s (%.2f sqrt k)" % (k, d, thin / 4 ** k, need, need / sqrt(k)))
print("(4) the ball blocks A_w = H restricted to addresses of weight <= w: size M, cost 2*sum_{j<=w} j C(k,j) additions by sums on the ball; against M log2 M")
for k in (64, 1024, 2 ** 14):
    for w in (1, 2, 3, 8, int(sqrt(k)), k // 8):
        M = cle(k, w); c = 2 * sum(j * comb(k, j) for j in range(w + 1))
        print("  k=%5d w=%4d  log2 M=%7.1f  cost per point %.2f  = %.3f of log2 M;  log2|det| per point %.2f" % (k, w, log2(M), c / M, c / M / log2(M), c / 2 / M))
# exact run of the ball program at k=8
k = 8; N = 1 << k; random.seed(3)
for w in (1, 2, 3):
    ball = [x for x in range(N) if wt(x) <= w]; inb = set(ball)
    v = {x: random.randint(-9, 9) for x in ball}; u = dict(v); ops = 0
    for i in range(k):
        for x in ball:
            if x >> i & 1: u[x ^ (1 << i)] += u[x]; ops += 1
    u = {S: (-2) ** wt(S) * u[S] for S in ball}
    for i in range(k):
        for x in ball:
            if x >> i & 1: u[x] += u[x ^ (1 << i)]; ops += 1
    want = {x: sum((-1) ** wt(x & y) * v[y] for y in ball) for x in ball}
    print("  [ran] k=8 w=%d: ball program equals H on the ball: %s   M=%d  additions %d = %.2f M   (M log2 M = %.0f)" % (w, u == want, len(ball), ops, ops / len(ball), len(ball) * log2(len(ball))))
# (5) in the Walsh basis the cheap part sits in a corner: H T H is zero outside (weight<=d) x (weight<=d)
k = 6; N = 1 << k
H = [[(-1) ** wt(x & y) for y in range(N)] for x in range(N)]
for (a, d) in ((0, 2), (1, 2), (1, 3)):
    c = [(-1) ** a * sum((-2) ** i * gbin(-a, i - j) for i in range(j, d + 1)) for j in range(d + 1)]
    pv = [sum(c[j] * comb(t, j) for j in range(d + 1)) for t in range(k + 1)]
    T = [[pv[wt(x & y)] for y in range(N)] for x in range(N)]
    HT = [[sum(H[x][z] * T[z][y] for z in range(N)) for y in range(N)] for x in range(N)]
    HTH = [[sum(HT[x][z] * H[z][y] for z in range(N)) for y in range(N)] for x in range(N)]
    outside = sum(1 for x in range(N) for y in range(N) if HTH[x][y] and wt(x | y) > d)
    inside = sum(1 for x in range(N) for y in range(N) if HTH[x][y])
    dep = all(len({HTH[x][y] * (-1) ** (wt(x) + wt(y)) for x in range(N) for y in range(N) if wt(x | y) == u}) == 1 for u in range(k + 1))
    print("  [ran] k=6 window [%d,%d]: H*T*H nonzero entries %d, of which with |x union y| > d: %d ; entry = (-1)^(|x|+|y|) * function of |x union y| only: %s" % (a, a + d, inside, outside, dep))
