#!/usr/bin/env python3
"""price.py [ab-8-reconcilecaps]  ONE pricing function for every ceiling of the avenues study and of x-6.
FLOATS (bisection on  sum over blocks of (rank/m)^z = W ; the engine's price law).  Every row is a WHAT-IF block list
unless it says 'certificate'.  Units: per v 'pair-indices'; data arrays nd = (s-1) v; each skips r of its m = s h moves.
  lam  = loss ratio = moves spent on copies per stage / (r v)          (copies in blocks of rank h)
  hp   = helper arrays per pair-index, each one block of rank h per stage (the avenues' optimistic helper)
  idle = how the idle moves of a data array are cut:
     'A2'  two equal idle blocks per array        (k-levers; 'bank as published' in v-levers)
     'A5'  x-6's five-stage bank, unequal blocks  (2(h-r)+4r, 2(h-r), h-r, 4r ; two arrays each)   [five stages only]
     'B1'  one idle block per array               (v-levers 'merged'; x-6's plain three-stage shape: catch-up 2r)
     'C0'  no idle block: catch-up merged into the next climb, blocks h-r, h, h  (x-6 'merged')     [three stages only]"""
import math, sys
def root(blocks, m, W):
    def mom(e): return sum(n * (r / m) ** (1 - e) for r, n in blocks if n > 0 and r > 0) / W
    if mom(0.0) >= 1: return 0.0
    lo, hi = 0.0, 1.0
    if mom(hi) < 1: return 1.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if mom(mid) < 1: lo = mid
        else: hi = mid
    return lo
def blocks(h, r, s, lam=0.0, hp=0.0, idle='B1'):
    v = 1.0; m = s * h; nd = (s - 1) * v; W = nd + hp * v
    bl = [(h, s * hp * v)]                                  # helpers
    bl.append((h, s * lam * r * v / h))                     # copies: s * cst moves in blocks of h
    if idle == 'C0':
        assert s == 3
        bl += [(h - r, nd), (h, 2 * nd)]
    elif idle == 'A5':
        assert s == 5
        bl += [(h - r, 10 * v / 4 * 4 / 4 * 4)]            # 10 active roles per 4 arrays -> 2 s v = 10 v roles for nd = 4 v
        bl += [(2 * (h - r) + 4 * r, nd / 2), (2 * (h - r), nd / 2), (h - r, nd / 2), (4 * r, nd / 2)]
    else:
        roles = 2 * s * v; bl.append((h - r, roles))
        idlem = nd * (m - r) - roles * (h - r); nidle = nd if idle == 'B1' else 2 * nd
        bl.append((idlem / nidle, nidle))
    return bl, m, W
def sav(h, r, s, lam=0.0, hp=0.0, idle='B1'):
    bl, m, W = blocks(h, r, s, lam, hp, idle)
    return root(bl, m, W)
if __name__ == '__main__':
    p = lambda *a, **k: print(*a, **k)
    p('== 1. controls against the two studies own outputs')
    p('k-levers fat (6,3) lam .5144, 3-stage, hp 0 / 1 / 6.5, two idle blocks : %.4e %.4e %.4e   (k.out: 2.2842e-02 1.7204e-02 7.2822e-03)' % tuple(sav(6, 3, 3, .5144, hp, 'A2') for hp in (0, 1, 6.5)))
    p('k-levers fat (6,3) lam .5144, 5-stage, hp 0 / 1 / 6.5, two idle blocks : %.4e %.4e %.4e   (k.out: 2.4829e-02 1.9402e-02 8.8098e-03)' % tuple(sav(6, 3, 5, .5144, hp, 'A2') for hp in (0, 1, 6.5)))
    p('v-levers formula corner (8,4) lam 0 hp 0: 3-stage A2 %.4f  B1 %.4f ; 5-stage A2 %.4f  A5 %.4f  B1 %.4f   (v-levers: 0.107 to 0.120 ; 0.075 to 0.086)' % (sav(8, 4, 3, 0, 0, 'A2'), sav(8, 4, 3, 0, 0, 'B1'), sav(8, 4, 5, 0, 0, 'A2'), sav(8, 4, 5, 0, 0, 'A5'), sav(8, 4, 5, 0, 0, 'B1')))
    p('x-6 shapes rho = .2 .3 .4 .5 : 5-stage A5 ' + ' '.join('%.4f' % sav(10, r, 5, 0, 0, 'A5') for r in (2, 3, 4, 5)) + '   (x-6: 0.0282 0.0430 0.0594 0.0784)')
    p('x-6 shapes rho = .2 .3 .4 .5 : 3-stage B1 ' + ' '.join('%.4f' % sav(10, r, 3, 0, 0, 'B1') for r in (2, 3, 4, 5)) + '   (x-6: 0.0485 0.0707 0.0940 0.1198)')
    p('x-6 merged    rho = .2 .3 1/3 .4 .5 : 3-stage C0 ' + ' '.join('%.4f' % sav(30, r, 3, 0, 0, 'C0') for r in (6, 9, 10, 12, 15)) + '   (x-6: 0.0593 0.0884 0.0980 0.1174 0.1467)')
    p('x-6 r = h/3 : 3-stage B1 %.4f ; 5-stage A5 %.4f   (x-6: 0.078 ; 0.048)' % (sav(9, 3, 3), sav(9, 3, 5, 0, 0, 'A5')))
    p('E8 thin (9,1) lam 0 hp 0 : 5-stage A5 %.4e  (x-6: 1.5758e-02) ; A2 %.4e  B1 %.4e (v-levers R 0 cst 0: 1.6e-2 to 2.0e-2) ; 3-stage B1 %.4e (v-levers 2.85e-2)' % (sav(9, 1, 5, 0, 0, 'A5'), sav(9, 1, 5, 0, 0, 'A2'), sav(9, 1, 5, 0, 0, 'B1'), sav(9, 1, 3)))
    p('E8 thin (9,1) lam 0.6 (cst 72), hp 0 : 5-stage A5 %.4e ; lam 55/120 hp 8/120 A5 %.4e B1 %.4e (k-levers 6.55e-3 ; v-levers to 8.2e-3)' % (sav(9, 1, 5, .6, 0, 'A5'), sav(9, 1, 5, 55 / 120, 8 / 120, 'A5'), sav(9, 1, 5, 55 / 120, 8 / 120, 'B1')))
    p('E8 thin (9,1) lam 0.6 hp 116/120 and 37/120, A5, helper one block : %.4e %.4e   (k.out 3.0644e-03 3.5887e-03)' % (sav(9, 1, 5, .6, 116 / 120, 'A5'), sav(9, 1, 5, .6, 37 / 120, 'A5')))
    p()
    p('== 2. the ladder from 2.3e-2 to 0.12 at r = h/2, three stages: one idealisation at a time')
    p('   start  k-levers  (6,3) lam .5144 hp 0 A2 : %.4f' % sav(6, 3, 3, .5144, 0, 'A2'))
    p('   only the idle block merged (B1)          : %.4f' % sav(6, 3, 3, .5144, 0, 'B1'))
    p('   only copies free (lam 0), A2             : %.4f' % sav(6, 3, 3, 0, 0, 'A2'))
    p('   both (x-6 corner)                        : %.4f' % sav(6, 3, 3, 0, 0, 'B1'))
    p('   and catch-up merged into the climb (C0)  : %.4f' % sav(6, 3, 3, 0, 0, 'C0'))
    p('   from the corner 0.1198 back down, one cost at a time (B1): ' + ' ; '.join('lam %.2f: %.4f' % (l, sav(6, 3, 3, l)) for l in (.1, .2, .3, .4, .5, .6)))
    p('   corner, helpers per pair-index (B1, lam 0): ' + ' ; '.join('hp %.2f: %.4f' % (q, sav(6, 3, 3, 0, q)) for q in (.31, .97, 2, 6.5)))
    p()
    p('== 3. the frontier for 1e-1: largest loss ratio lam that still gives saving >= 0.1, by rho = r/h (h = 1000 r-grid), helpers hp')
    H = 1000
    for s, idle in ((3, 'B1'), (3, 'C0'), (3, 'A2'), (5, 'A5'), (5, 'B1')):
        for hp in (0.0, 0.31, 1.0):
            out = []
            for rho in (.30, .34, .38, .42, .44, .46, .48, .50):
                r = rho * H
                if sav(H, r, s, 0, hp, idle) < .1: out.append('%.2f: none' % rho); continue
                lo, hi = 0.0, 1.0
                for _ in range(50):
                    mid = (lo + hi) / 2
                    if sav(H, r, s, mid, hp, idle) >= .1: lo = mid
                    else: hi = mid
                out.append('%.2f: lam<=%.3f (kappa>=%.1f)' % (rho, lo, 1 / (rho * lo) if lo > 0 else float('inf')))
            p('   %d-stage %s hp %.2f : ' % (s, idle, hp) + ' ; '.join(out))
    p()
    p('== 4. least rho for 1e-1 with everything else free: ' + ' ; '.join('%d-stage %s: %.3f' % (s, idle, min(r for r in range(1, 501) if sav(1000, r, s, 0, 0, idle) >= .1) / 1000) for s, idle in ((3, 'A2'), (3, 'B1'), (3, 'C0'), (5, 'B1')) if any(sav(1000, r, s, 0, 0, idle) >= .1 for r in range(1, 501))))
    if len(sys.argv) > 1:
        p('== 5. class ceilings from knows.py:  h r kappa_max')
        for line in open(sys.argv[1]):
            if not line.startswith('CEIL'): continue
            _, h, r, kap = line.split()[:4]; h = int(h); r = int(r); kap = float(kap); lam = h / (kap * r)
            p('   (%d,%d) kappa <= %.3f  loss ratio >= %.3f : 3-stage B1 %.4f  C0 %.4f  A2 %.4f ; 5-stage A5 %.4f B1 %.4f ; with copies free: B1 %.4f C0 %.4f' % (h, r, kap, lam, sav(h, r, 3, lam), sav(h, r, 3, lam, 0, 'C0'), sav(h, r, 3, lam, 0, 'A2'), sav(h, r, 5, lam, 0, 'A5'), sav(h, r, 5, lam, 0, 'B1'), sav(h, r, 3), sav(h, r, 3, 0, 0, 'C0')))
