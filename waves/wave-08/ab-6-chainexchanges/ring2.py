#!/usr/bin/env python3
"""ring2.py [ab-6-chainexchanges]  EXACT formal replay (same machine as ring.py, 9 address bits, coordinate directions).
The odd-even ring of four arrays, two rounds of exchanges in FIVE stages instead of six: stage 3 is at once the third
shear of round A (pairs (0,1), (2,3), ports a, b) and the first shear of round B (pairs (2,1), (0,3), ports c, d).
Stage k: the sources climb U_k, a copy descends the block span(port, U_k), the targets read it and climb U_k afterwards.
Legal word of the engine's sub-game (additions, shifts, blocks); ONE source per total, so it LOSES moves: it shows the
shape (stages per round, blocks per array), not a unit.  Then: the price law for the what-if block lists of that shape."""
import sys, math
from fractions import Fraction as Fr
h = 9; N = 1 << h
wt = lambda x: bin(x).count("1"); PAR = [[wt(y & (1 << j)) & 1 for y in range(N)] for j in range(h)]
QF = tuple(wt(y) % 4 for y in range(N))
class Machine:
    def __init__(s, nlive, nscratch):
        s.n = nlive + nscratch; s.live = nlive; s.a = [dict() for _ in range(s.n)]
        for l in range(nlive): s.a[l][(l, (0,) * N)] = Fr(1)
        s.blocks = [[] for _ in range(s.n)]
    def block(s, r, js, sg):
        add = [sum(sg * PAR[j][y] for j in js) for y in range(N)]
        s.a[r] = {(l, tuple((q[y] + add[y]) % 4 for y in range(N))): c for (l, q), c in s.a[r].items()}; s.blocks[r].append(len(js))
    def shift(s, r, j): s.a[r] = {(l, tuple((q[y] + 2 * PAR[j][y]) % 4 for y in range(N))): c for (l, q), c in s.a[r].items()}
    def add(s, t, coef, src):
        for k, c in list(s.a[src].items()):
            v = s.a[t].get(k, 0) + Fr(coef) * c
            if v: s.a[t][k] = v
            else: s.a[t].pop(k, None)
    def copy(s, t, src): s.a[t] = dict(s.a[src])
    def ok(s): return all(s.a[l] == {(l, QF): Fr(1)} for l in range(s.live))
    def moves(s): return sum(sum(b) for b in s.blocks)
U = [0, 1, 2, 3, 4]; a, b, c, d = 5, 6, 7, 8
M = Machine(4, 1); S = 4
def shear(src, tgt, port, k, kind):          # kind +1: tgt += x src ; kind -1: tgt -= x^-1 src ; x = (move along port)^-1
    M.copy(S, src); M.block(S, [port, U[k]], -1)
    if kind == -1: M.shift(S, port)
    M.add(tgt, kind, S)
climb = lambda r, ks: M.block(r, [U[k] for k in ks], +1)
climb(0, [0]); climb(2, [0]); shear(0, 1, a, 0, +1); shear(2, 3, b, 0, +1)                                   # stage 1, evens -> odds
climb(1, [0, 1]); climb(3, [0, 1]); shear(1, 0, a, 1, -1); shear(3, 2, b, 1, -1)                             # stage 2, odds -> evens
climb(0, [1, 2]); climb(2, [1, 2]); shear(0, 1, a, 2, +1); shear(2, 3, b, 2, +1); shear(2, 1, c, 2, +1); shear(0, 3, d, 2, +1)   # stage 3, shared
climb(1, [2, 3]); climb(3, [2, 3]); shear(1, 2, c, 3, -1); shear(3, 0, d, 3, -1)                             # stage 4, odds -> evens
climb(0, [3, 4]); climb(2, [3, 4]); shear(2, 1, c, 4, +1); shear(0, 3, d, 4, +1)                             # stage 5, evens -> odds
pure = all(len(M.a[r]) == 1 for r in range(4))
print("after five stages every array holds ONE term (one content at one level):", pure)
got = {}
for r in range(4):
    (l, q), co = next(iter(M.a[r].items())); got[r] = (l, co)
owes = {0: [a, c], 1: [a, d], 2: [b, d], 3: [b, c]}        # array r holds a content that never received these two ports
# odd arrays: last climb U_5 and the two owed port moves in ONE block; even arrays: the owed moves after their last read
for r in (1, 3): M.block(r, [U[4]] + owes[r], +1)
for r in (0, 2): M.block(r, owes[r], +1)
import itertools
final = [None] * 4
for r in range(4):
    (l, q), co = next(iter(M.a[r].items())); fix = None
    for T in itertools.chain.from_iterable(itertools.combinations((a, b, c, d), n) for n in range(5)):
        if all((q[y] + 2 * sum(PAR[j][y] for j in T) - QF[y]) % 4 == 0 for y in range(N)): fix = T; break
    assert fix is not None, "array %d is not at the kernel up to shifts" % r
    for j in fix: M.shift(r, j)
    final[l] = ({k: v / co for k, v in M.a[r].items()})
M.a[:4] = final
print("contents found in arrays 0..3:", [got[r][0] for r in range(4)], "; all four live arrays end at the kernel of their own input:", M.ok())
print("moves %d (plain schedule %d); blocks per live array %s ; scratch blocks: %d of rank 2" % (M.moves(), 4 * h, M.blocks[:4], len(M.blocks[4])))
# ---- the price law for what-if block lists of this shape (FLOATS) ----
def root(blocks, m, W):
    f = lambda e: sum(n * (r / m) ** (1 - e) for r, n in blocks) / W
    if f(0.0) >= 1: return 0.0
    lo, hi = 0.0, 1.0
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) < 1 else (lo, mid)
    return lo
print("WHAT-IF block lists (no network behind them): odd-even ring, R rounds in S = 2R + 1 stages, stage size h, port size r;")
print("  per pair of arrays: even array blocks (h-r), R x 2(h-r), (R+1) r ; odd array blocks R x 2(h-r), (h-r) + (R+1) r ; shears: 3 per exchange, 3R per pair of arrays")
print("  'free' = shears and helpers cost nothing; 'kappa' = every shear pays h/kappa moves in blocks of rank h (helpers still free)")
for rho0, hh, rr in ((1/3, 9, 3), (0.2, 10, 2), (1/9, 9, 1)):
    for R in (1, 2, 3, 5, 10):
        Sg = 2 * R + 1; m = Sg * hh; d = hh - rr
        data = [(d, 1), (2 * d, R), ((R + 1) * rr, 1), (2 * d, R), (d + (R + 1) * rr, 1)]
        line = "  r/h = %.3f R = %2d S = %2d : skipped share %.4f, blocks per array %.1f, saving free %.4f" % (rho0, R, Sg, R * rr / m, (2 * R + 3) / 2, root(data, m, 2))
        for kap in (60, 15, 5):
            line += " ; kappa %d: %.4f" % (kap, root(data + [(hh, 3.0 * R / kap)], m, 2))      # 3 shears per exchange, one exchange per pair of arrays per round
        print(line)
print("  compare: plain exchange as x-6 counted it (3 blocks of h-r and one of 2r): r/h = 1/3: %.4f ; 1/9: %.4f" % (root([(6, 3), (6, 1)], 27, 1), root([(8, 3), (2, 1)], 27, 1)))
