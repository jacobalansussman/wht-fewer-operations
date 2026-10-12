#!/usr/bin/env python3
"""flatsearch.py seconds seed [ad-1-linesums]  First look at "which flat basis is cheapest" at 16 points.
A flat basis = 16 flats (cosets of subspaces of the 4 address bits) with independent indicators.  Then
H = P * sizes * B^-1 (flatbasis.py).  Crude size (NOT a gate count): non-zeros of P (= sum of 16 / |flat|) plus non-zeros
of B^-1.  Yates' subcubes: 81 + 81 = 162.  The plane's lines: 64 + 121 = 185.  Points: 256 + 16 = 272.
Hill climb with restarts over all 307 flats, exact fractions."""
import sys, random, time
from fractions import Fraction as F
secs = float(sys.argv[1]); rnd = random.Random(int(sys.argv[2])); N = 16
subs = set()
for a in range(N):
    for b in range(N):
        for c in range(N):
            S = {0}
            for g in (a, b, c): S |= {s ^ g for s in S}
            subs.add(frozenset(S))
flats = sorted({frozenset(s ^ c for s in S) for S in subs for c in range(N)}, key=lambda f: (len(f), sorted(f)))
print("flats:", len(flats), "by size", {n: sum(1 for f in flats if len(f) == n) for n in (1, 2, 4, 8, 16)})
def nnz_inv(fl):
    n = N; A = [[F(1 if x in f else 0) for f in fl] + [F(int(x == c)) for c in range(n)] for x in range(n)]
    for c in range(n):
        p = next((i for i in range(c, n) if A[i][c] != 0), None)
        if p is None: return None
        A[c], A[p] = A[p], A[c]; iv = 1 / A[c][c]; A[c] = [v * iv for v in A[c]]
        for i in range(n):
            if i != c and A[i][c] != 0:
                f_ = A[i][c]; A[i] = [u - f_ * v for u, v in zip(A[i], A[c])]
    return sum(1 for r in A for v in r[n:] if v != 0), max(abs(v) for r in A for v in r[n:])
def score(fl):
    r = nnz_inv(fl)
    if r is None: return None
    return sum(N // len(f) for f in fl) + r[0], r
t0 = time.time(); best = (10 ** 9, None); seen = {}
while time.time() - t0 < secs:
    cur = rnd.sample(flats, N); sc = score(cur)
    if sc is None: continue
    stall = 0
    while stall < 150 and time.time() - t0 < secs:
        new = list(cur); new[rnd.randrange(N)] = rnd.choice(flats)
        if len(set(new)) < N: continue
        s2 = score(new)
        if s2 is not None and s2[0] <= sc[0]:
            if s2[0] < sc[0]: stall = 0
            cur, sc = new, s2
        stall += 1
    prof = tuple(sorted(len(f) for f in cur))
    seen[(sc[0], prof)] = seen.get((sc[0], prof), 0) + 1
    if sc[0] < best[0]:
        best = (sc[0], cur, sc[1]); print("t %5.0f  crude size %d = P %d + inverse %d (largest entry %s) sizes of the flats %s" % (time.time() - t0, sc[0], sum(N // len(f) for f in cur), sc[1][0], sc[1][1], prof), flush=True)
print("local optima reached (crude size, flat sizes): count ; ten smallest:")
for kv in sorted(seen.items())[:10]: print("  ", kv)
print("best basis:", [sorted(f) for f in best[1]])
