# ag-1: every gate between wires with entries 0, +1, -1 (primitive, up to sign).  Count (G).  Exact.
# For all non-parallel u, v and all w on their line with entries 0, +-1:  w = (a*u + b*v)/c, a, b coprime whole numbers, c > 0.
# Claim checked: (|a| + |b|)/c is 2 (u +- v), 3 (u +- 2v) or 1 (the halving (u +- v)/2), and the halving occurs exactly when
# u and v are the same vector modulo 2.
import itertools, sys
from fractions import Fraction
from math import gcd
n=int(sys.argv[1])
def norm(v):
    for t in v:
        if t: return tuple(v) if t>0 else tuple(-q for q in v)
    return None
V=sorted({norm(v) for v in itertools.product((-1,0,1),repeat=n)}-{None}); S=set(V)
hist={}; bad=0; tested=0
for i,u in enumerate(V):
    for v in V[:i]:
        # all w = (a u + b v)/c in the set: a/c, b/c are determined by two coordinates; enumerate candidate ratios
        seen=set()
        for a,b in itertools.product(range(-4,5),repeat=2):
            if (a,b)==(0,0) or gcd(a,b)!=1 or a==0 or b==0: continue
            w=[a*p+b*q for p,q in zip(u,v)]; c=0
            for t in w: c=gcd(c,abs(t))
            if c==0: continue
            wp=norm([t//c for t in w])
            if wp in S and wp not in seen:
                seen.add(wp); tested+=1
                same=all((p-q)%2==0 for p,q in zip(u,v))
                key=(abs(a)+abs(b),c,"same residue" if same else "different residues")
                hist[key]=hist.get(key,0)+1
print("n=%d: %d wires, %d gates (u, v, w) with all three flat"%(n,len(V),tested))
for k in sorted(hist): print("   |a|+|b| = %d, content c = %d, operands of %s: %d gates ; weight factor %s"%(k[0],k[1],k[2],hist[k],Fraction(k[0],k[1])))
