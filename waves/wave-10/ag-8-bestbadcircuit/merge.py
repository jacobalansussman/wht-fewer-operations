#!/usr/bin/env python3
"""merge.py (ag-8): put together the censuses cen2_<p>_<m>_<tauG>.pkl.  A shape is ROBUSTLY GENERIC if it exists at every generic
(p, tau) run.  A helper set of the transform is OF THE CLASS if one of its wirings has a robustly generic shape, SPECIAL if none of
its wirings has a shape seen at ANY generic run, IN BETWEEN otherwise.  Shapes are compared across primes (they are strings)."""
import sys, pickle, glob
m = int(sys.argv[1]); runs = [pickle.load(open(f, 'rb')) for f in sorted(glob.glob('cen2_*_%d_*.pkl' % m))]
Gs = [set(r['G']) for r in runs]; inter = set.intersection(*Gs); union = set.union(*Gs)
print('generic runs:', [(r['p'], r['tG'], len(r['G'])) for r in runs], '| shapes in all:', len(inter), '| in some:', len(union))
byp = {}
for r in runs: byp.setdefault(r['p'], r)
allH = {}
for p, r in sorted(byp.items()):
    cl = sp = mid = 0; spsh = {}; hshapes = set()
    for S, cs in r['HSETS']:
        hshapes |= set(cs)
        if any(c in inter for c in cs): cl += 1
        elif any(c in union for c in cs): mid += 1
        else:
            sp += 1; k = min(cs); spsh.setdefault(k, [0, S, len(cs)]); spsh[k][0] += 1
    allH[p] = (hshapes, spsh)
    print('p=%d transform: %d irredundant sets: %d OF THE CLASS, %d in between, %d SPECIAL in %d kinds (kind = least shape of the set); shapes at the transform %d, of them robustly generic %d'
          % (p, len(r['HSETS']), cl, mid, sp, len(spsh), len(hshapes), len(hshapes & inter)))
ps = sorted(allH)
if len(ps) > 1:
    a, b = allH[ps[0]], allH[ps[1]]
    print('transform shapes: p=%d %d, p=%d %d, common %d' % (ps[0], len(a[0]), ps[1], len(b[0]), len(a[0] & b[0])))
    print('special kinds: p=%d %d, p=%d %d, common %d' % (ps[0], len(a[1]), ps[1], len(b[1]), len(set(a[1]) & set(b[1]))))
    print('robustly generic shapes NOT seen at the transform at either prime:', len([c for c in inter if c not in a[0] and c not in b[0]]))
p0 = ps[0]; r = byp[p0]
T0 = 4 + m
def show(pts, w): return ' | '.join('%s%d=%s<-(%d,%d)' % ('h' if n < T0 else 'T', n, ','.join(map(str, pts[n])), w[n][0], w[n][1]) for n in sorted(w))
print('\nSPECIAL shapes, one labelled specimen each (p=%d):' % p0)
for i, (k, (n, S, nc)) in enumerate(sorted(allH[p0][1].items(), key=lambda kv: -kv[1][0])):
    print('SP%03d sets=%d shapes_of_specimen=%d' % (i, n, nc)); print('    ' + show(*r['HS'][k]))
print('\nCOMMON shapes, specimens')
import random; random.seed(3)
com = sorted(c for c in allH[p0][0] if c in inter); random.shuffle(com)
for i, c in enumerate(com[:10]):
    print('CO%03d' % i); print('    ' + show(*r['HS'][c]))
print('\nshapes absent at the transform, specimens')
ab = sorted(c for c in inter if all(c not in allH[q][0] for q in ps)); random.shuffle(ab)
for i, c in enumerate(ab[:10]):
    print('AB%03d' % i); print('    ' + show(*r['G'][c]))
