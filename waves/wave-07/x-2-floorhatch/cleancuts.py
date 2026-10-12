# x-2-floorhatch/cleancuts.py : for circuits found by hatch.c, count the CLEAN cuts: the ways c of cutting the addresses in two
# parallel halves for which no gate is new at both halves (B = 0).  A circuit under the floor can have no clean cut at its top
# level [x-2.md section 2].  Count (G).  usage: python3 -B cleancuts.py N file ...
import sys
from math import gcd
def cut(v, X):
    c = [v[i] for i in X]; g = 0
    for t in c: g = gcd(g, t)
    if g == 0: return None
    s = next(t for t in c if t); s = g if s > 0 else -g
    return tuple(t // s for t in c)
def newset(vecs, X):
    seen = set(); nx = set()
    for g, v in enumerate(vecs):
        c = cut(v, X)
        if c is None or sum(1 for t in c if t) < 2 or c in seen: continue
        seen.add(c); nx.add(g)
    return nx
N = int(sys.argv[1]); tally = {}
for path in sys.argv[2:]:
    vecs = [[int(t) for t in line[2:].split(':')[1].split()] for line in open(path) if line.startswith('w ')]
    if not vecs: continue
    Bs = []; Es = []
    for c in range(1, N):
        L = [x for x in range(N) if bin(x & c).count('1') % 2 == 0]; R = [x for x in range(N) if bin(x & c).count('1') % 2]
        nl, nr = newset(vecs, L), newset(vecs, R); Bs.append(len(nl & nr)); Es.append(len(vecs) - len(nl | nr)); assert Es[-1] >= N // 2 + 1
    sup = {frozenset(i for i in range(N) if v[i]) for v in vecs}
    lam = all(a <= b or b <= a or not (a & b) for a in sup for b in sup)
    key = (len(vecs), Bs.count(0), lam); tally[key] = tally.get(key, 0) + 1
    print('%s: gates %d; clean cuts %d of %d; B over the cuts %s; sets pairwise nested or disjoint: %s; distinct sets %d' % (path.split('/')[-1], len(vecs), Bs.count(0), N - 1, sorted(Bs), lam, len(sup)))
for key in sorted(tally): print('TALLY gates %d, clean cuts %d, sets nested or disjoint %s: %d circuits' % (*key, tally[key]))
