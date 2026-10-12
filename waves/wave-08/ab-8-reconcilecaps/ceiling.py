#!/usr/bin/env python3
"""ceiling.py [ab-8-reconcilecaps]  The ORDER BOUND (derived in ab-8.md section 4; exact fractions) fed into the price law (floats).
For EVERY family of labels (P, L) of class (h, r), any complement L, in x-6's design (scatter matrix M, M_tt = 1,
M_ts != 0 only if P_s inside L_t, copies cost h * rank M):   rank M >= v (2^r - 1) / (2^r + 2^(h-r) - 2),  so
     kappa <= K(h, r) = 1 + (2^(h-r) - 1) / (2^r - 1),     loss ratio >= h / (K r).
Optional file argument: lines 'TYPE h r type kappa' from knows.py give the sharper single-type ceilings for h <= 9."""
import sys, glob, functools
print = functools.partial(print, flush=True)
from fractions import Fraction as Fr
from price import sav
K = lambda h, r: 1 + Fr(2 ** (h - r) - 1, 2 ** r - 1)
star = {}; lonely = {}
for f in sorted(glob.glob('knows_*.out')):
    for line in open(f):
        if 'knows: nobody' in line:
            hh, rr = f[len('knows_'):-4].split('_'); lonely.setdefault((int(hh), int(rr)), set()).add(line.split()[4])
        if line.startswith('TYPE') and line.split()[4] != 'none':
            _, h, r, ty, k = line.split()[:5]; star.setdefault((int(h), int(r)), {})[ty] = float(k)
print('== A. the classes computed exactly (h <= 9).  order = the order bound; types = best explicit set per type (knows.py); kappa* = ceiling used')
print('   three-stage gain at all needs loss ratio < 2/3, five-stage < 0.8.  Savings: copies at the floor, helpers 0.')
for (h, r) in sorted(star):
    kb = float(K(h, r)); st = star[(h, r)]
    # single-type sub-families: best type; mixed: min(order bound, sum of types)
    live = {t: k for t, k in st.items() if t not in lonely.get((h, r), ())}       # a type that knows nobody is a set of isolated ports
    kap = min(kb, sum(live.values())) if live else 1.0
    lam = h / (kap * r)
    print('   (%d,%d) rho %.3f  order %.3f  types %s  kappa* <= %.3f  loss ratio >= %.3f | 3-stage B1 %.4f C0 %.4f A2 %.4f | 5-stage A5 %.4f B1 %.4f | copies free: B1 %.4f C0 %.4f'
          % (h, r, r / h, kb, ' '.join('%s %.3f' % kv for kv in sorted(st.items())), kap, lam, sav(h, r, 3, lam), sav(h, r, 3, lam, 0, 'C0'), sav(h, r, 3, lam, 0, 'A2'), sav(h, r, 5, lam, 0, 'A5'), sav(h, r, 5, lam, 0, 'B1'), sav(h, r, 3), sav(h, r, 3, 0, 0, 'C0')))
print('== B. growth law under the order bound alone: best saving over r for each block width h (helpers 0; copies at h/(K r))')
def Kf(h, r):
    return float(K(h, r)) if h < 200 else 1 + 2.0 ** (h - 2 * r)
def best(h, s, idle, hp=0.0, lo=0.0):
    b = (0.0, 0)
    for r in range(max(1, int(lo * h)), h // 2 + 1):
        if sav(h, r, s, 0.0, hp, idle) <= b[0]: continue          # even with free copies it cannot beat the best so far
        lam = h / (Kf(h, r) * r)
        b = max(b, (sav(h, r, s, lam, hp, idle), r))
    return b
for h in (4, 6, 8, 9, 12, 16, 20, 24, 28, 32, 40, 48, 56, 64, 80, 100, 128, 200, 300, 500):
    row = []
    for s, idle in ((3, 'B1'), (3, 'C0'), (3, 'A2'), (5, 'A5'), (5, 'B1')):
        e, r = best(h, s, idle); row.append('%d-%s %.4f (r=%d)' % (s, idle, e, r))
    print('   h = %3d : ' % h + ' ; '.join(row))
print('== C. least block width h at which the order bound stops excluding 1e-1 (helpers hp per pair-index, one block per stage each)')
for s, idle in ((3, 'B1'), (3, 'C0'), (3, 'A2'), (5, 'B1'), (5, 'A5')):
    for hp in (0.0, 0.31, 0.5, 1.0):
        hit = None
        if sav(1000, 500, s, 0.0, hp, idle) >= 0.1:
            for h in list(range(2, 140)) + list(range(140, 1200, 5)):
                e, r = best(h, s, idle, hp, 0.3)
                if e >= 0.1: hit = (h, r, e, Kf(h, r)); break
        print('   %d-stage %s hp %.2f : ' % (s, idle, hp) + ('h = %d, r = %d (saving %.4f; needs a scatter with kappa near %.0f, i.e. about %.0f removals per target or more)' % (hit + (hit[3] - 1,)) if hit else 'never: even with free copies and r = h/2 this shape stays below 1e-1, or no h up to 1200'))
print('== D. largest helpers per pair-index compatible with 1e-1 when copies cost nothing and r = h/2 (dead end, kappa <= 2): ', end='')
for idle in ('B1', 'C0'):
    lo, hi = 0.0, 5.0
    for _ in range(50):
        mid = (lo + hi) / 2
        if sav(1000, 500, 3, 0, mid, idle) >= .1: lo = mid
        else: hi = mid
    print('3-stage %s: %.3f ;' % (idle, lo), end=' ')
print()
print('== E. v-levers corner with one helper per pair-index (B1, (8,4), lam 0): 3-stage %.4f, 5-stage %.4f ; (6,3) lam .487: hp 0: %.4f %.4f ; hp 1: %.4f %.4f' % (sav(8, 4, 3, 0, 1), sav(8, 4, 5, 0, 1), sav(6, 3, 3, .487), sav(6, 3, 5, .487), sav(6, 3, 3, .487, 1), sav(6, 3, 5, .487, 1)))
print('== F. the same thresholds with the sharper ceilings: families of all-even ports (r even):  1 + (2^(h-1-r) - 1)/(2^r - 1)  [order bound inside the even words, derived];')
print('      other ports: 1.34 * 2^(h - r - floor((h-1)/2))  [star of odd words; ESTIMATE: the factor 1.34 is the largest seen in the eight classes computed exactly];  mixed: the sum, capped by the order bound')
def K2(h, r):
    alt = (1 + (2.0 ** (h - 1 - r) - 1) / (2.0 ** r - 1)) if r % 2 == 0 else 0.0
    non = 1.34 * 2.0 ** (h - r - (h - 1) // 2)
    return min(Kf(h, r), alt + non), alt, non
def best2(h, s, idle, hp=0.0, lo=0.3):
    b = (0.0, 0)
    for r in range(max(1, int(lo * h)), h // 2 + 1):
        if sav(h, r, s, 0.0, hp, idle) <= b[0]: continue
        b = max(b, (sav(h, r, s, h / (K2(h, r)[0] * r), hp, idle), r))
    return b
for s, idle, hp in ((3, 'B1', 0.0), (3, 'B1', 0.31), (3, 'C0', 0.0), (3, 'C0', 0.31), (3, 'C0', 0.5), (5, 'B1', 0.0)):
    hit = None
    for h in list(range(2, 200)) + list(range(200, 1200, 4)):
        e, r = best2(h, s, idle, hp)
        if e >= 0.1: hit = (h, r, e) + K2(h, r); break
    print('   %d-stage %s hp %.2f : ' % (s, idle, hp) + ('h = %d, r = %d (saving %.4f; ceiling used %.0f = all-even part %.0f + other part %.0f, capped)' % hit if hit else 'none up to h = 1200'))
print('   best saving under the sharper ceilings by h (3-stage B1 / C0, helpers 0): ' + ' ; '.join('h=%d: %.4f / %.4f' % (h, best2(h, 3, 'B1', 0.0, 0.0)[0], best2(h, 3, 'C0', 0.0, 0.0)[0]) for h in (9, 12, 16, 24, 32, 48, 64, 96, 128)))
