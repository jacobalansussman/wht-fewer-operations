# e2-1-dictionary / hubs.py : how many targets can one hub serve by a single sign flip on a small flat?  exact, bit masks.
# hub g = a +-1 pattern of algebraic degree <= r on all N = 2^k points; targets = the N characters times a fixed quadratic pattern q0 (free input signs);
# "served" = g and +-target differ exactly on a flat of codimension c >= 2 (codimension 1 is the ordinary butterfly).
import itertools, sys
from collections import Counter
def run(k,r):
    N=1<<k; FULL=(1<<N)-1
    def mono(S): return sum(1<<x for x in range(N) if all(x>>i&1 for i in S))
    lin=[mono((i,)) for i in range(k)]
    quad=[mono(S) for S in itertools.combinations(range(k),2)]
    cub=[mono(S) for S in itertools.combinations(range(k),3)] if r>=3 else []
    def span(gens):
        s={0}
        for g in gens: s|={x^g for x in s}
        return s
    chars=sorted(span(lin))                      # N masks: where the character is -1
    flats={}                                     # mask -> codimension, for flats of codim 2..k
    subs=set()
    for d in range(0,k-1):
        for gens in itertools.combinations(range(1,N),d):
            S=span(gens)
            if len(S)==1<<d: subs.add(frozenset(S))
    for W in subs:
        d=len(W).bit_length()-1
        for t in range(N):
            flats[sum(1<<(w^t) for w in W)]=k-d
    res=Counter()
    qs=sorted(span(quad)); cs=sorted(span(cub)) if cub else [0]
    for q0 in qs[:8]:                            # target class (a few)
        for qg in qs:
            for cg in cs:
                g=qg^cg
                by=Counter()
                for ch in chars:
                    t=q0^ch
                    for dset in (g^t, (g^t)^FULL):
                        if dset in flats: by[flats[dset]]+=1
                for c,n in by.items(): res[(c,n)]+=1
                if not by: res[("none",0)]+=1
    print(f"k={k}, hubs of degree <= {r}: (codimension of the flipped flat, number of targets served by one hub): number of (hub, target class) pairs")
    for kx,v in sorted(res.items(),key=str): print("   ",kx,v)
run(3,2); run(3,3); run(4,2); run(4,3)
