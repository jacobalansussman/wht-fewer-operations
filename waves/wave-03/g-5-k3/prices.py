#!/usr/bin/env python3
"""prices.py (g-5-k3): the two reductions with tonight's best prices for the transform in count (G).
e2-0.md (read, not re-verified by me): T(N) <= (3/4) N log2 N + N/4, i.e. 7, 20, 52, 128, 304 at 4..64 points."""
from math import comb
def T34(s): return 0 if s == 0 else (2 if s == 1 else (3 * s * 2 ** s + 2 ** s) // 4)
def T78(s): return (s // 2) * 7 * 2 ** (s - 2) + (s % 2) * 2 ** s if s >= 2 else (2 if s == 1 else 0)
def c3(T, r): return 2 * sum(comb(r, j) * T(r - j) for j in range(r + 1))
print('K3 power on 3^r numbers, by "two layers of transforms" (count G):')
print(' r  textbook  with 7-gate bricks  with e2-0 prices  ratio(e2-0)/textbook   [replayed by me: r=2: 22; r=3: 98 (7-gate bricks), 96 (two layers of the 12-gate brick)]')
for r in range(1, 11):
    tb = 4 * r * 3 ** (r - 1); print(' %2d  %8d  %8d  %8d   %.4f' % (r, tb, c3(T78, r), c3(T34, r), c3(T34, r) / tb))
print('closed form with e2-0 prices: r 3^r + 3^r / 2 - (terms from sizes 1, 2):', [(r, c3(T34, r), r * 3 ** r + 3 ** r // 2) for r in (4, 6, 8)])
print()
print('transform on 8^t points by the pair route with the 12-gate brick, orbit and antisymmetric transforms at e2-0 prices, against e2-0 direct:')
for t in (1, 2, 3, 4, 8, 16, 64):
    inn = sum(comb(t, s) * 4 ** t // 2 ** s * T34(s) for s in range(t + 1))
    mid = sum(comb(t, a) * ((a * 12 * 6 ** (a - 1) * 2 ** (t - a) if a else 0) + 6 ** a * T34(t - a)) for a in range(t + 1))
    tot = 2 * inn + mid; text = 3 * t * 8 ** t
    print(' t=%2d: pair route %.5f of textbook ; e2-0 direct %.5f ; product of 7-gate bricks %.5f' % (t, tot / text, T34(3 * t) / text, T78(3 * t) / text))
print('gates per bit of determinant (2 = butterflies): 7-gate brick %.3f ; 12-gate brick for K3(x)H2 (7 bits) %.3f ; e2-0 at 8, 16, 64 points %.3f %.3f %.3f ; e2-0 limit 1.5'
      % (7 / 4, 12 / 7, 20 / 12, 52 / 32, 304 / 192))
