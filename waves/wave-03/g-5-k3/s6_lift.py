#!/usr/bin/env python3
"""s6_lift.py (g-5-k3): the 11-gate circuit for the symmetric square S6 of K3 found over GF(5) by mincirc_odd, lifted by hand
to the rationals and replayed exactly.  Count (G).  Coordinates: x00, x01, x02, x11, x12, x22 of a symmetric 3 x 3 array."""
from fractions import Fraction as F
S6 = [[1, 2, 2, 1, 2, 1], [2, 2, 0, 0, -2, -2], [1, 0, 2, -1, 0, 1], [4, 0, -8, 0, 0, 4], [2, -2, 0, 0, 2, -2], [1, -2, 2, 1, -2, 1]]
rows = [[F(int(i == j)) for j in range(6)] for i in range(6)]
def gate(u, v, a, b): rows.append([a * x + b * y for x, y in zip(rows[u], rows[v])]); return len(rows) - 1
g6 = gate(1, 4, 1, 1)        # x01 + x12
g7 = gate(0, 5, 1, 1)        # x00 + x22
g8 = gate(g7, 2, 1, -2)      # row 11 / 4
g9 = gate(g8, 3, 1, -1)
g10 = gate(g9, 2, 1, 4)      # row 02
g11 = gate(g7, g6, 1, 1)
g12 = gate(g11, g9, 2, -1)   # row 00
g13 = gate(g12, g6, 1, -4)   # row 22
g14 = gate(g11, 1, 1, -2)
g15 = gate(g14, 0, 1, -2)    # - row 01 / 2
g16 = gate(g14, 5, 1, -2)    # row 12 / 2
def prop(a, b):
    k = None
    for x, y in zip(a, b):
        if (x == 0) != (y == 0): return False
        if y != 0:
            if k is None: k = x / y
            elif x != k * y: return False
    return True
outs = {0: g12, 1: g15, 2: g10, 3: g8, 4: g16, 5: g13}
print('gates:', len(rows) - 6, '; every row of S6 proportional to its node:', all(prop(rows[outs[i]], [F(x) for x in S6[i]]) for i in range(6)))
print('route K3 (x) K3 = split by the swap of the two factors (6) + S6 (11) + antisymmetric square = -2 K3^T (4) + merge (6) =', 6 + 11 + 4 + 6, 'against 24 (butterflies) and 22 (bricks)')
