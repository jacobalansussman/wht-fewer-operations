#!/usr/bin/env python3
"""ac-2/price2.py  Own re-implementation of the price law (floats for the root; K exact).  Per pair: 2 data arrays (3 stages) or 4 (5 stages).
Shapes as ab-8 describes them: B1 = per data array s... blocks: 2s blocks of rank h-r per pair + one idle block per data array;
C0 = per data array blocks h-r, h, h ; A5 = the published five-stage bank.  Copies: s/kappa blocks per pair, each of rank c (ab-8: c = h).
Root z of  sum (rank/m)^z = W  by bisection; saving = 1 - z."""
import math, sys
from fractions import Fraction as Fr
def saving(blocks, m, W):
    f = lambda z: sum(n * (rk / m) ** z for rk, n in blocks if n > 0 and rk > 0) - W
    if f(1.0) >= 0: return 0.0
    lo, hi = 0.0, 1.0                     # f decreasing in z ; f(0) = number of blocks - W > 0
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) > 0: lo = mid
        else: hi = mid
    return 1 - lo
def shape(h, r, s, idle, ntot, c, hp=0.0):
    m = s * h; nd = s - 1; W = nd + hp
    bl = [(h, s * hp), (c, s * ntot)]
    if idle == 'C0': bl += [(h - r, nd), (h, 2 * nd)]
    elif idle == 'A5': bl += [(h - r, 10), (2 * (h - r) + 4 * r, 2), (2 * (h - r), 2), (h - r, 2), (4 * r, 2)]
    else:
        idlem = nd * (m - r) - 2 * s * (h - r); k = nd if idle == 'B1' else 2 * nd
        bl += [(h - r, 2 * s), (idlem / k, k)]
    return saving(bl, m, W)
K = lambda h, r: 1 + Fr(2 ** (h - r) - 1, 2 ** r - 1)
Kf = lambda h, r: float(K(h, r)) if h < 400 else (1 + 2.0 ** (h - 2 * r) if h - 2 * r < 1000 else float('inf'))
p = lambda *a: print(*a, flush=True)
p('== controls: corner r = h/2, copies free: 3-stage B1 %.4f  C0 %.4f  A2 %.4f ; 5-stage B1 %.4f  A5 %.4f ; one helper per pair B1: 3-stage %.4f 5-stage %.4f ; r = h/3 3-stage B1 %.4f  C0 %.4f  5-stage A5 %.4f'
  % (shape(8, 4, 3, 'B1', 0, 8), shape(8, 4, 3, 'C0', 0, 8), shape(8, 4, 3, 'A2', 0, 8), shape(8, 4, 5, 'B1', 0, 8), shape(8, 4, 5, 'A5', 0, 8), shape(8, 4, 3, 'B1', 0, 8, 1.0), shape(8, 4, 5, 'B1', 0, 8, 1.0), shape(9, 3, 3, 'B1', 0, 9), shape(9, 3, 3, 'C0', 0, 9), shape(9, 3, 5, 'A5', 0, 9)))
p('   (6,3) loss ratio .5144: A2 3-stage %.4f, B1 %.4f ; .487: B1 3-stage %.4f 5-stage %.4f ; with one helper %.4f %.4f' % (shape(6, 3, 3, 'A2', .5144 * 3 / 6, 6), shape(6, 3, 3, 'B1', .5144 * 3 / 6, 6), shape(6, 3, 3, 'B1', .487 * 3 / 6, 6), shape(6, 3, 5, 'B1', .487 * 3 / 6, 6), shape(6, 3, 3, 'B1', .487 * 3 / 6, 6, 1.0), shape(6, 3, 5, 'B1', .487 * 3 / 6, 6, 1.0)))
p('   E8 (9,1) 5-stage A5: copies free %.4e ; loss ratio .6 %.4e ; .6 with 116/120 and 37/120 helpers %.4e %.4e ; 55/120 with 8/120 helpers A5 %.4e B1 %.4e' % (shape(9, 1, 5, 'A5', 0, 9), shape(9, 1, 5, 'A5', .6 / 9, 9), shape(9, 1, 5, 'A5', .6 / 9, 9, 116 / 120), shape(9, 1, 5, 'A5', .6 / 9, 9, 37 / 120), shape(9, 1, 5, 'A5', 55 / 120 / 9, 9, 8 / 120), shape(9, 1, 5, 'B1', 55 / 120 / 9, 9, 8 / 120)))
p('== A. every class with h <= 9, order bound alone (number of totals per pair = 1/K, each one block of rank h per stage): best over r')
for h in range(2, 13):
    row = []
    for s, idle in ((3, 'B1'), (3, 'C0'), (3, 'A2'), (5, 'B1'), (5, 'A5')):
        b = max((shape(h, r, s, idle, 1 / float(K(h, r)), h), r) for r in range(1, h))
        row.append('%d-%s %.4f (r=%d)' % (s, idle, b[0], b[1]))
    p('   h = %2d : ' % h + ' ; '.join(row))
p('   overall maximum for h <= 9: ' + ' ; '.join('%d-%s %.4f' % (s, idle, max(shape(h, r, s, idle, 1 / float(K(h, r)), h) for h in range(2, 10) for r in range(1, h))) for s, idle in ((3, 'B1'), (3, 'C0'), (3, 'A2'), (5, 'B1'), (5, 'A5'))))
p('== B. first width at which the order bound stops excluding 1e-1, and the growth law')
for s, idle in ((3, 'B1'), (3, 'C0'), (3, 'A2'), (5, 'B1'), (5, 'A5')):
    hit = None
    for h in list(range(2, 800)):
        b = max((shape(h, r, s, idle, 1 / Kf(h, r), h), r) for r in range(max(1, int(.25 * h)), h // 2 + 1))
        if b[0] >= 0.1: hit = (h, b[1], b[0], Kf(h, b[1])); break
    p('   %d-stage %s : ' % (s, idle) + ('h = %d r = %d saving %.5f ; K there = %.1f ; one width earlier %.5f' % (hit + (max(shape(hit[0] - 1, r, s, idle, 1 / Kf(hit[0] - 1, r), hit[0] - 1) for r in range(1, hit[0] // 2 + 1)),)) if hit else 'never below width 800'))
p('   growth (3-stage B1 / C0): ' + ' ; '.join('h=%d: %.4f / %.4f' % (h, max(shape(h, r, 3, 'B1', 1 / Kf(h, r), h) for r in range(1, h // 2 + 1)), max(shape(h, r, 3, 'C0', 1 / Kf(h, r), h) for r in range(1, h // 2 + 1))) for h in (9, 12, 20, 32, 48, 80, 200, 500, 1000, 4000)))
p('   limit shapes, copies free: B1 at r = h/2: %.5f ; C0 at r = h/2: %.5f' % (shape(1000, 500, 3, 'B1', 0, 1000), shape(1000, 500, 3, 'C0', 0, 1000)))
p('   fit: 0.1198 - saving(h), times h / ln h, for B1: ' + ' ; '.join('h=%d: %.3f' % (h, (shape(1000, 500, 3, 'B1', 0, 1000) - max(shape(h, r, 3, 'B1', 1 / Kf(h, r), h) for r in range(1, h // 2 + 1))) * h / math.log(h)) for h in (50, 100, 200, 500, 1000, 4000)))
p('== C. HATCH H1 quantified: the NUMBER of totals is kept at the order bound (1/K per pair per stage), but a total is ONE block of rank c < h.')
p('   best saving over all classes with h <= 9, by c:')
for s, idle in ((3, 'B1'), (3, 'C0'), (5, 'B1')):
    row = []
    for c in (1, 2, 3, 4, 6, 9):
        b = max((shape(h, r, s, idle, 1 / float(K(h, r)), min(c, h)), h, r) for h in range(2, 10) for r in range(1, h))
        row.append('c=%d: %.4f at (%d,%d)' % ((c,) + b))
    p('   %d-stage %s : ' % (s, idle) + ' ; '.join(row))
p('   and with the number of totals free as well (copies cost nothing), h <= 9: ' + ' ; '.join('%d-%s %.4f at (%d,%d)' % ((s, idle) + max((shape(h, r, s, idle, 0, h), h, r) for h in range(2, 10) for r in range(1, h))) for s, idle in ((3, 'B1'), (3, 'C0'), (5, 'B1'))))
p('== D. what the corner r = h/2 needs: kappa <= 2 there for every h.  Saving at r = h/2 with 1/2 total per pair per stage of rank c, h = 8 and h = 64:')
for h in (8, 64):
    p('   h = %d : ' % h + ' ; '.join('c=%s: B1 %.4f C0 %.4f' % (c, shape(h, h // 2, 3, 'B1', .5, c), shape(h, h // 2, 3, 'C0', .5, c)) for c in (1, 2, h // 4, h // 2, h)))
