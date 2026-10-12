#!/usr/bin/env python3
"""mux16.py [ad-3]  16 points.  Parts 1 to 3 exact fractions; part 4 FLOATS (a potential, not a proof).
 1. The dictionary for ANY set T unchanged by u (not only flats): C[f after the exchange] = Phi C[f] Phi,
    Phi = I - 2 diag([u.x=1]) Pi_T, and on the half u.x = 1 Phi is the reflection whose spectrum is -1 on T.
 2. The exchange as a controlled swap.  Split the addresses by the bit along u (here u = e0): f0 = f on y0 = 0, f1 = f on
    y0 = 1 (functions of the other 3 bits).  After the exchange the two halves are mux(t; f0, f1) and mux(t; f1, f0).
 3. One exchange from the quadric (ANY T) leaves the quadric untouched on the half where its derivative along u is 0.
 4. Ailon's potential (minus the sum of M_ij^2 log2 M_ij^2 over an orthogonal matrix M) after each stage of the 86-gate product."""
from fractions import Fraction as F
import random, math
k = 4; N = 16; rnd = random.Random(7)
def dot(x, y): return bin(x & y).count("1") & 1
H = [[1 - 2 * dot(x, y) for y in range(N)] for x in range(N)]
def conv(s): return [[sum(F(H[x][y] * s[y] * H[y][z]) for y in range(N)) / N for z in range(N)] for x in range(N)]
def mul(A, B): return [[sum(A[i][l] * B[l][j] for l in range(N)) for j in range(N)] for i in range(N)]
def phi(u, T):
    Pi = conv([1 if y in T else 0 for y in range(N)])
    return [[(1 if x == z else 0) - 2 * dot(u, x) * Pi[x][z] for z in range(N)] for x in range(N)]
bad1 = bad2 = 0; trials = 60
for _ in range(trials):
    u = rnd.randrange(1, N); T = set()
    for y in range(N):
        if rnd.random() < 0.4: T.add(y); T.add(y ^ u)
    f = [rnd.randrange(2) for _ in range(N)]
    g = [f[y ^ u] if y in T else f[y] for y in range(N)]          # f after the exchange: g(y) = f(pi(y))
    P = phi(u, T)
    bad1 += mul(mul(P, conv([1 - 2 * v for v in f])), P) != conv([1 - 2 * v for v in g])
    # g = f + t * (f(y) + f(y+u))
    bad2 += any(g[y] != f[y] ^ ((y in T) & (f[y] ^ f[y ^ u])) for y in range(N))
print("1. C[f after exchange] = Phi C[f] Phi for random f and random sets T unchanged by u: %d trials, %d failures ; f after = f + t (f(y)+f(y+u)): %d failures" % (trials, bad1, bad2))
bad = 0
for _ in range(trials):
    u = 1; T = set()
    for y in range(0, N, 2):
        if rnd.random() < 0.5: T.add(y); T.add(y ^ 1)
    f = [rnd.randrange(2) for _ in range(N)]
    g = [f[y ^ u] if y in T else f[y] for y in range(N)]
    for y in range(0, N, 2):
        t = y in T
        bad += g[y] != (f[y ^ 1] if t else f[y]); bad += g[y ^ 1] != (f[y] if t else f[y ^ 1])
print("2. halves after the exchange are mux(t; f0, f1) and mux(t; f1, f0): %d failures" % bad)
quad = [((y & 1) & (y >> 1 & 1)) ^ ((y >> 2 & 1) & (y >> 3 & 1)) for y in range(N)]
bad = 0
for _ in range(trials):
    u = rnd.randrange(1, N); T = set()
    for y in range(N):
        if rnd.random() < 0.5: T.add(y); T.add(y ^ u)
    g = [quad[y ^ u] if y in T else quad[y] for y in range(N)]
    bad += any(g[y] != quad[y] for y in range(N) if quad[y] == quad[y ^ u])
    d = [quad[y] ^ quad[y ^ u] for y in range(N)]
    bad += sum(d) != 8                                               # the derivative of a quadric is a hyperplane
print("3. one exchange (any T) changes the quadric only where quadric(y) != quadric(y+u), a hyperplane's worth of points: %d failures" % bad)
# 4. potential, floats
def pot(M): return -sum(float(v) ** 2 * math.log2(float(v) ** 2) for row in M for v in row if v != 0)
A0 = frozenset([4, 6, 8, 10, 12, 14]); u1, T1 = 1, frozenset([0, 1, 4, 5]); u2, T2 = 3, frozenset([0, 3, 8, 11])
P1 = phi(u1, T1); P2 = phi(u2, T2); C0 = conv([-1 if y in A0 else 1 for y in range(N)])
stages = [("Phi2", P2, 14), ("Phi1", P1, 14), ("C_start", C0, 30), ("Phi1", P1, 14), ("Phi2", P2, 14)]
M = [[F(1 if i == j else 0) for j in range(N)] for i in range(N)]; prev = 0.0
print("4. FLOATS. Ailon's potential of the product so far (0 at the start, N log2 N = 64 for the transform):")
for name, S, gates in stages:
    M = mul(S, M); p = pot(M)
    print("     after %-8s potential %7.3f   gained %7.3f bits with %2d gates : %.3f bits per gate" % (name, p, p - prev, gates, (p - prev) / gates)); prev = p
print("     total 64 bits with 86 gates: %.3f bits per gate (textbook: 64 bits with 64 gates, 1 bit per gate)" % (64 / 86))
