#!/usr/bin/env python3
"""symbolic.py [ai-0]  The helper claim of ag-0 at sizes nobody can enumerate (y of 2,058 or 2,059 bits), by coefficients.

For a tower (Lr real colours, atoms of s bits) take one RANDOM quadratic Q_c in y per colour (whole numbers; this is
more than degree 3 asks for).  Build the quadratic A' of my formula (ai-0.md section 2).  Then E_c = Q_c - A' must not
depend on the atom that colour c forgets, on every piece.  A multilinear polynomial does not depend on a bit exactly
when no monomial containing that bit survives, so the test is, for every bit p of level c (its atom is active where the
lower bits equal iota(p)):
   (i)  coefficient of y_p y_q in E_c is 0 for every q that is not a lower bit;
   (ii) (coefficient of y_p) + sum over lower bits q set in iota(p) of (coefficient of y_p y_q) is 0.
Every identity is linear in the random numbers (drawn below 2^20), so a false identity survives with chance < 2^-19.
Second, independent test: E_c evaluated at random points y and at y with the active atom redrawn (python whole numbers).
Control: the same with A' = 0 must fail.
usage: symbolic.py Lr s extra
"""
import sys, random, time
import numpy as np

def levels(Lr, s):
    offs = []; m = 0
    for j in range(Lr):
        offs.append(m); m += s * (1 if j == 0 else (1 << m))
    return offs, m

Lr, s, extra = map(int, sys.argv[1:4]); t0 = time.time()
offs, mt = levels(Lr, s); m = mt + extra
rng = np.random.default_rng(20261011); random.seed(20261011)
INF = 99
lev = np.full(m, INF, dtype=np.int64); iota = np.zeros(m, dtype=np.int64)
for j in range(Lr):
    width = s * (1 if j == 0 else (1 << offs[j]))
    b = np.arange(offs[j], offs[j] + width); lev[b] = j; iota[b] = (b - offs[j]) // s
print("tower: %d colours, atoms of %d bits, %d extra bits: y has %d bits; level starts %s" % (Lr, s, extra, m, offs), flush=True)

Q = []; lin = []
for c in range(Lr):
    U = np.triu(rng.integers(-(1 << 20), 1 << 20, size=(m, m), dtype=np.int64), 1)
    Q.append(U + U.T); lin.append(rng.integers(-(1 << 20), 1 << 20, size=m, dtype=np.int64))
minlev = np.minimum.outer(lev, lev)
A2 = np.zeros((m, m), dtype=np.int64)
for c in range(Lr): A2 += np.where(minlev == c, Q[c], 0)
alin = np.zeros(m, dtype=np.int64)
IO = {}
for l in range(Lr):
    bits = np.nonzero(lev == l)[0]; low = offs[l]
    io = ((iota[bits][:, None] >> np.arange(low)[None, :]) & 1) if low else np.zeros((len(bits), 0), dtype=np.int64)
    IO[l] = (bits, io)
    alin[bits] = lin[l][bits] + (io * (Q[l][bits][:, :low] - A2[bits][:, :low])).sum(axis=1)

def test(A2, alin, tag):
    worst = 0; checked = 0
    for c in range(Lr):
        E = Q[c] - A2; el = lin[c] - alin; bits, io = IO[c]; low = offs[c]
        blk = E[bits][:, low:]                                   # (i): partners that are not lower bits
        bad1 = int(np.count_nonzero(blk)); checked += blk.size
        r = el[bits] + (io * E[bits][:, :low]).sum(axis=1)       # (ii)
        bad2 = int(np.count_nonzero(r)); checked += r.size
        # independent: random points, active atom redrawn
        bad3 = 0; Ei = None
        for _ in range(60):
            y = np.array([random.getrandbits(1) for _ in range(m)], dtype=np.int64)
            idx = int(sum(int(y[p]) << p for p in range(low)))
            a0 = low + s * idx
            y2 = y.copy(); y2[a0:a0 + s] = [random.getrandbits(1) for _ in range(s)]
            if (y2 == y).all(): y2[a0] ^= 1
            v1 = int(y @ E @ y) // 2 + int(el @ y); v2 = int(y2 @ E @ y2) // 2 + int(el @ y2)
            if v1 != v2: bad3 += 1
        print("   %s colour %d: %d atoms; (i) non-zero %d of %d ; (ii) non-zero %d of %d ; random points that differ %d of 60" % (
            tag, c, len(bits) // s, bad1, blk.size, bad2, r.size, bad3), flush=True)
        worst += bad1 + bad2 + bad3
    return worst, checked

w, n = test(A2, alin, "formula:")
print("FORMULA: %s (%d coefficient identities checked)   (%.0f s)" % ("holds" if w == 0 else "FAILS", n, time.time() - t0), flush=True)
w0, _ = test(np.zeros_like(A2), np.zeros_like(alin), "control A' = 0:")
print("CONTROL: %s" % ("fails as it must" if w0 else "PASSED: the test has no teeth"), flush=True)
# int64 safety: |entries| < 2^21 after one subtraction; sums of at most 2,059 of them < 2^33; y E y < 2^21 * 2059^2 < 2^44.
