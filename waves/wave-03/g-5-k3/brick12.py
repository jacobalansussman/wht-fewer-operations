#!/usr/bin/env python3
"""brick12.py (g-5-k3): the 12-gate circuit for K3 (x) H2 on 6 numbers (count G), found by mincirc_odd over GF(5), lifted by hand
to the rationals, replayed exactly here; then what it gives at 8 points (the transform, by the pair route) and at 27 points (K3 cubed)."""
import itertools, sys
from fractions import Fraction as F
from math import comb
from k3 import Circ, K3, kron, kpow, proportional, butterfly, brick4

H2 = [[1, 1], [1, -1]]

class SC(Circ):
    """Circ with a recorded scale per node: node = scale * (the form the caller means).  gate() takes coefficients for the meant
    forms and divides by the scales, so bricks whose outputs come out with a factor (here: one output with factor -1) compose.
    Scalings are free in count (G); this only keeps the coefficients honest for the exact replay."""
    def __init__(self, n): super().__init__(n); self.scale = {}
    def gate(self, u, v, a, b):
        return super().gate(u, v, F(a) / self.scale.get(u, 1), F(b) / self.scale.get(v, 1))

def brick12(c, a0, a1, b0, b1, c0, c1):
    """returns {(i, j): node} with node proportional to (row i of K3) (x) (row j of H2); 12 gates."""
    g6 = c.gate(c0, c1, 1, 1)
    g8 = c.gate(g6, a1, 1, 1)            # a1 + c0 + c1
    h = c.gate(a0, g8, 1, -1)            # helper a0 - a1 - c0 - c1 : the 7-gate brick's helper on the rows a, c
    t10 = c.gate(h, a1, 1, 2)            # (a0 + a1) - (c0 + c1)
    t11 = c.gate(h, c1, 1, 2)            # (a0 - a1) - (c0 - c1)
    g7 = c.gate(b0, b1, 1, 1)
    h1 = c.gate(h, g7, 1, 1)             # second helper: +a0 -a1 +b0 +b1 -c0 -c1 (flat)
    t00 = c.gate(h1, g8, 1, 2)           # all ones
    t20 = c.gate(h1, a0, 1, -2)          # -(a+ - b+ + c+)
    if hasattr(c, 'scale'): c.scale[t20] = -1
    h2 = c.gate(h1, c0, 1, 2)            # third helper: +a0 -a1 +b0 +b1 +c0 -c1 (flat)
    t01 = c.gate(h2, b1, 1, -2)
    t21 = c.gate(h2, b0, 1, -2)
    return {(1, 0): t10, (1, 1): t11, (0, 0): t00, (2, 0): t20, (0, 1): t01, (2, 1): t21}

def k3plain(c, a, b, cc):
    s, d = butterfly(c, a, cc); o0, o2 = butterfly(c, s, b); return {0: o0, 1: d, 2: o2}

if __name__ == '__main__':
    # 1. the brick itself
    c = Circ(6); out = brick12(c, 0, 1, 2, 3, 4, 5); T = kron(K3, H2)
    ok = all(proportional(c.rows[out[(i, j)]], [F(x) for x in T[2 * i + j]]) is not None for i in range(3) for j in range(2))
    print('1. K3 (x) H2 on 6 numbers: %d gates, every output proportional to its row: %s  (textbook 14; with the 7-gate brick 13)' % (len(c.gates), ok))
    for i, (u, v, a, b) in enumerate(c.gates):
        print('     n%d = (%s)*n%d + (%s)*n%d = %s' % (6 + i, a, u, b, v, [str(x) for x in c.rows[6 + i]]))
    print('     coefficient sizes used: 1 and 2 only; wires flat on all six inputs: n12 (h1), n13 (t00), n14 (t20), n15 (h2), n16, n17')
    # 2. the 8-point transform by the pair route: split bits 1,2 into symmetric / antisymmetric, brick12 + one butterfly, merge
    c = SC(8); idx = lambda x1, x2, x3: 4 * x1 + 2 * x2 + x3
    b_ = {}; d_ = {}
    for x3 in (0, 1): b_[x3], d_[x3] = butterfly(c, idx(0, 1, x3), idx(1, 0, x3))
    mid = brick12(c, idx(0, 0, 0), idx(0, 0, 1), b_[0], b_[1], idx(1, 1, 0), idx(1, 1, 1))
    dp, dm = butterfly(c, d_[0], d_[1])
    outs = {}
    # K3 rows: 0 -> F00, 2 -> F11, 1 -> F01 + F10 (times 1/... free);  antisymmetric line: F01 - F10 = -2 (x01 - x10)
    for j, dd in ((0, dp), (1, dm)):
        outs[(0, 0, j)] = mid[(0, j)]; outs[(1, 1, j)] = mid[(2, j)]
        # mid[(1,j)] is proportional to (a - c)(x)row j ; F01 = (a - c) - D, F10 = (a - c) + D with D = (x01 - x10)(x)row j
        k = proportional(c.rows[mid[(1, j)]], [F(v) for v in [(1 if (x1, x2) == (0, 0) else -1 if (x1, x2) == (1, 1) else 0) * (1 if (j == 0 or x3 == 0) else -1)
                                                           for x1 in (0, 1) for x2 in (0, 1) for x3 in (0, 1)]])
        outs[(0, 1, j)] = c.gate(mid[(1, j)], dd, 1 / k, -1); outs[(1, 0, j)] = c.gate(mid[(1, j)], dd, 1 / k, 1)
    H8 = kpow(H2, 3)
    ok = all(proportional(c.rows[outs[(u1, u2, u3)]], [F(x) for x in H8[idx(u1, u2, u3)]]) is not None for u1 in (0, 1) for u2 in (0, 1) for u3 in (0, 1))
    print('2. 8-point transform = split one pair (4) + brick12 (12) + one butterfly on the antisymmetric line (2) + merge (4): %d gates, correct: %s  (best known 22, textbook 24)' % (len(c.gates), ok))
    # 3. K3 cubed on 27 numbers: (K3 at position 1) (x) (first butterfly of position 2), then (K3 at position 3) (x) (second butterfly of position 2)
    pts = list(itertools.product(range(3), repeat=3)); pos = {p: i for i, p in enumerate(pts)}
    c = SC(27); cur = {p: pos[p] for p in pts}
    for l3 in range(3):
        o = brick12(c, cur[(0, 0, l3)], cur[(0, 2, l3)], cur[(1, 0, l3)], cur[(1, 2, l3)], cur[(2, 0, l3)], cur[(2, 2, l3)])
        for i in range(3):
            cur[(i, 0, l3)] = o[(i, 0)]; cur[(i, 2, l3)] = o[(i, 1)]          # position 2: slot 0 = sum, slot 2 = difference
        o = k3plain(c, cur[(0, 1, l3)], cur[(1, 1, l3)], cur[(2, 1, l3)])
        for i in range(3): cur[(i, 1, l3)] = o[i]
    for i in range(3):
        o = brick12(c, cur[(i, 0, 0)], cur[(i, 1, 0)], cur[(i, 0, 1)], cur[(i, 1, 1)], cur[(i, 0, 2)], cur[(i, 1, 2)])
        new = {}
        for r3 in range(3):
            new[(i, 0, r3)] = o[(r3, 0)]; new[(i, 1, r3)] = o[(r3, 1)]        # position 2: slot 0 -> s + b (row 0), slot 1 -> s - b (row 2)
        o = k3plain(c, cur[(i, 2, 0)], cur[(i, 2, 1)], cur[(i, 2, 2)])
        for r3 in range(3): new[(i, 2, r3)] = o[r3]
        for kk, vv in new.items(): cur[kk] = vv
    rowmap2 = {0: 0, 1: 2, 2: 1}; T27 = kpow(K3, 3)
    ok = all(proportional(c.rows[cur[(i, s2, r3)]], [F(x) for x in T27[pos[(i, rowmap2[s2], r3)]]]) is not None for i in range(3) for s2 in range(3) for r3 in range(3))
    print('3. K3 cubed on 27 numbers with two layers of brick12: %d gates, correct: %s  (textbook 108; with 7-gate bricks 98)' % (len(c.gates), ok))
    # 4. what the brick gives for the transform at large sizes, by formula (count G)
    def bk(s): return (s // 2) * 7 * 2 ** (s - 2) + (s % 2) * 2 ** s if s >= 2 else (2 if s == 1 else 0)
    print('4. formula: 8^t points = split t pairs (orbit transforms) + middle (K3(x)H2 bricks; plain transforms on antisymmetric lines) + merge')
    print('   t  points  textbook  7-gate-brick product  pair route with brick12 (orbit and antisymmetric transforms by 7-gate bricks)  ratio to textbook')
    for t in (1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 128, 256):
        inn = sum(comb(t, s) * 4 ** t // 2 ** s * bk(s) for s in range(t + 1))
        mid = sum(comb(t, a) * ((a * 12 * 6 ** (a - 1) * 2 ** (t - a) if a else 0) + 6 ** a * bk(t - a)) for a in range(t + 1))
        tot = 2 * inn + mid; text = 3 * t * 8 ** t
        print('   %3d  2^%d  ratio brick product %.5f   pair route %.5f   %s' % (t, 3 * t, bk(3 * t) / text, tot / text, 'BELOW the brick product' if tot < bk(3 * t) else ''))
        if t <= 3: print('        exact: textbook %d, brick product %d, pair route %d' % (text, bk(3 * t), tot))
    print('   limits: brick product 7/8 = 0.875 ; this route (10/24)(7/8) + (14/24)(12/14) = 83/96 = %.5f ; applied to itself: 6/7 = %.5f' % (83 / 96, 6 / 7))
