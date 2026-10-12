#!/usr/bin/env python3
# e-3-cutoff, experiment 3b: the parts of count.py after its crash (a float overflow in a print at k=16384, w=128), unchanged.
from math import comb, log2, sqrt
import random
wt = lambda v: bin(v).count("1")
def gbin(n, r):
    num = 1
    for q in range(r): num *= (n - q)
    f = 1
    for q in range(2, r + 1): f *= q
    return num // f
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
