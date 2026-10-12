#!/usr/bin/env python3
# e-3-cutoff, experiment 2: real matrices at k = 8 (and counts at 10).  Exact integers; ranks modulo P = 2^61-1
# (a rank modulo a prime is a LOWER bound on the true rank; every rank below is also pinned from above by an argument, see report).
import sys, random
from math import comb
from itertools import combinations
P = (1 << 61) - 1
wt = lambda v: bin(v).count("1")
def gbin(n, r):
    num = 1
    for q in range(r): num *= (n - q)
    f = 1
    for q in range(2, r + 1): f *= q
    return num // f
def rank_mod(M):
    M = [[x % P for x in row] for row in M]; r = 0; rows = len(M); cols = len(M[0]) if M else 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i][c]), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]; inv = pow(M[r][c], P - 2, P); Mr = [x * inv % P for x in M[r]]; M[r] = Mr
        for i in range(rows):
            if i != r and M[i][c]:
                f = M[i][c]; Mi = M[i]; M[i] = [(a - f * b) % P for a, b in zip(Mi, Mr)]
        r += 1
        if r == rows: break
    return r
# ---------- (a) the cut-off sums as a counted program: "fold when the bit is not in S, restrict when it is"
def cutoff_sums(v, k, d):
    """returns ({S(bitmask): sum of v over x containing S} for |S|<=d, number of additions)   count (O)=(G): additions only"""
    ops = 0; out = {}
    def rec(arr, bits_left, S, size):
        nonlocal ops
        if bits_left == 0: out[S] = arr[0]; return
        h = len(arr) // 2; b = bits_left - 1          # top remaining bit is bit b
        lo, hi = arr[:h], arr[h:]
        fold = [x + y for x, y in zip(lo, hi)]; ops += h
        rec(fold, b, S, size)
        if size < d: rec(hi, b, S | (1 << b), size + 1)
    rec(list(v), k, 0, 0); return out, ops
def spread(g, k, d):
    """transpose: out[x] = sum of g[S] over S inside x, |S|<=d; counted additions"""
    ops = 0
    def rec(bits_left, S, size):
        nonlocal ops
        if bits_left == 0: return [g[S]]
        b = bits_left - 1
        A = rec(b, S, size)
        if size < d:
            B = rec(b, S | (1 << b), size + 1); ops += len(A); return A + [x + y for x, y in zip(A, B)]
        return A + A
    return rec(k, 0, 0), ops
def coeffs(a, d):       # p = (-1)^t on [a,a+d], in the basis C(t,j)
    return [(-1) ** a * sum((-2) ** i * gbin(-a, i - j) for i in range(j, d + 1)) for j in range(d + 1)]
random.seed(7)
for k in (8, 10):
    N = 1 << k
    print("=== k=%d N=%d   count used: additions (the same number in (G) and (O)); the M scalings in the middle are extra in (O), free in (G)" % (k, N))
    v = [random.randint(-9, 9) for _ in range(N)]
    for d in range(0, k + 1):
        g, ops = cutoff_sums(v, k, d)
        M = sum(comb(k, j) for j in range(d + 1))
        assert len(g) == M
        if d <= 3: assert all(g[S] == sum(v[x] for x in range(N) if x & S == S) for S in g)
        law = sum(sum(comb(i, j) for j in range(min(i, d) + 1)) * (1 << (k - i - 1)) for i in range(k))
        a = max(0, k // 4 - d // 2); c = coeffs(a, d)
        w = {S: c[wt(S)] * g[S] for S in g}
        out, ops2 = spread(w, k, d)
        if k == 8 or d in (2, 3, 4):
            pv = [sum(c[j] * comb(t, j) for j in range(d + 1)) for t in range(k + 1)]
            want = [sum(pv[wt(x & y)] * v[y] for y in range(N)) for x in range(N)]
            assert out == want
        print("  d=%d  M=C(k,<=d)=%4d  sums: %6d adds = %.3f N (law %d, (d+1)N=%d)   spread: %6d adds = %.3f N (= sums - N + M: %s)   whole cut-off form %.3f N  against k N = %d N"
              % (d, M, ops, ops / N, law, (d + 1) * N, ops2, ops2 / N, ops2 == ops - N + M, (ops + ops2) / N, k))
        assert ops == law
k = 8; N = 1 << k
H = [[(-1) ** (wt(x & y) & 1) for y in range(N)] for x in range(N)]
ov = [[wt(x & y) for y in range(N)] for x in range(N)]
print("=== k=8: leftover of the LOWER window [0,d]:  is it N times the inverse of H on the heavy addresses (weight > d)?")
for d in range(0, k):
    r = [sum((-2) ** j * comb(t, j) for j in range(d + 1, t + 1)) for t in range(k + 1)]
    heavy = [x for x in range(N) if wt(x) > d]
    if len(heavy) > 170: 
        # check on a random sample of rows to keep the run short
        rows = random.sample(heavy, 12)
    else: rows = heavy
    ok = True
    for x in rows:
        Rx = [r[ov[x][z]] for z in heavy]
        for y in heavy:
            s = sum(a * H[z][y] for a, z in zip(Rx, heavy))
            if s != (N if x == y else 0): ok = False; break
        if not ok: break
    nz = sum(1 for x in heavy for y in heavy if r[ov[x][y]] != 0)
    print("  d=%d  heavy addresses %3d   R_HH * H_HH = N*I on %d rows checked: %s   nonzero entries of R: %d of %d" % (d, len(heavy), len(rows), ok, nz, N * N))
print("=== k=8: centred window, ranks (mod P) of the cheap part and of the leftover")
for (a, d) in ((0, 2), (1, 2), (1, 3), (0, 3), (0, 4), (1, 4)):
    c = coeffs(a, d); pv = [sum(c[j] * comb(t, j) for j in range(d + 1)) for t in range(k + 1)]
    r = [(-1) ** t - pv[t] for t in range(k + 1)]
    R = [[r[ov[x][y]] for y in range(N)] for x in range(N)]
    wrong = sum(1 for x in range(N) for y in range(N) if R[x][y])
    lv = [j for j in range(d + 1) if c[j] == (-2) ** j]
    pred = N - sum(comb(k, j) for j in lv)
    print("  window [%d,%d]  c=%s  wrong entries %5d (%.1f%%)  rank leftover (mod P) %d  predicted N - sum of C(k,j) over levels with c_j=(-2)^j: %d   leftover r(t), t=0..k: %s"
          % (a, a + d, c, wrong, 100 * wrong / N / N, rank_mod(R), pred, r))
print("=== k=8: weight-class pairs (w,v), w<=v.  window [1,3] (d=2).  columns: overlaps that occur; rank of H block; rank of leftover block; wrong entries; share")
a, d = 1, 2
c = coeffs(a, d); pv = [sum(c[j] * comb(t, j) for j in range(d + 1)) for t in range(k + 1)]
r = [(-1) ** t - pv[t] for t in range(k + 1)]
cls = [[x for x in range(N) if wt(x) == w] for w in range(k + 1)]
thin = 0
for w in range(k + 1):
    for v2 in range(w, k + 1):
        lo, hi = max(0, w + v2 - k), min(w, v2)
        Hb = [[H[x][y] for y in cls[v2]] for x in cls[w]]
        Rb = [[r[ov[x][y]] for y in cls[v2]] for x in cls[w]]
        wr = sum(1 for row in Rb for z in row if z)
        n = hi - lo + 1
        if n <= d + 1: thin += (1 if w == v2 else 2) * len(cls[w]) * len(cls[v2])
        print("  (%d,%d) size %2dx%2d  overlaps %d..%d (%d values)  rank H %2d  rank leftover %2d  wrong %4d of %4d   one own form of degree %d is exact%s"
              % (w, v2, len(cls[w]), len(cls[v2]), lo, hi, n, rank_mod(Hb), rank_mod(Rb), wr, len(cls[w]) * len(cls[v2]), n - 1, "  <= d: yes" if n <= d + 1 else ""))
print("  share of all entries in class pairs with at most d+1=%d overlaps: %.4f" % (d + 1, thin / N / N))
