# x-2-floorhatch/outside.py : the all-cuts bookkeeping (alldirs.py) on the night's circuits that are NOT in the one-tree class
# (wires that are not sign vectors, sets of several chains).  It tests the two general claims of x-2.md section 1 on them:
# E >= N/2 + 1 in every cut, and e = waste - B + (E - N/2 - 1).  Exact (Fractions, then whole numbers).  Count (G).
import sys, os, glob
from math import gcd
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'alldirs.py')).read().split('\nt2 = [')[0]
exec(src)
def ints(v):
    l = 1
    for t in v: l = l * t.denominator // gcd(l, t.denominator)
    return [int(t * l) for t in v]
def load(path):
    g = parse(path); N = npts(g); W = replay(g, N)
    rows = {tuple((-1) ** bin(y & x).count('1') for x in range(N)) for y in range(N)}
    vecs = [ints(W[name]) for (name, *_) in g]
    got = {cut(v, list(range(N))) for v in vecs}
    return vecs, N, rows <= got
for path in sorted(glob.glob(ID + 'u-4-zdz/hubparity*.txt') + glob.glob(ID + 'u-4-zdz/zdz_cat3_*.txt') + glob.glob(ID + 'h-6-classhub/drain21.txt')):
    try: vecs, N, ok = load(path)
    except Exception as ex: print(path.split('/')[-1], 'not parsed:', type(ex).__name__); continue
    if not ok: print(path.split('/')[-1], 'does not hold all rows of the transform; skipped'); continue
    mx = max(abs(t) for v in vecs for t in v); nonform = sum(1 for v in vecs if max(abs(t) for t in v) > 1)
    print('%s: largest entry %d, wires that are not sign vectors %d' % (path.split('/')[-1], mx, nonform))
    run(path.split('/')[-1][:13], vecs, N, False)
