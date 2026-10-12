# e2-1-dictionary / levels.py : which linear relations hold among THREE values of the calculus?  exact (bit masks of 0,+1,-1 vectors).
# family "coset": a character of Z_2^k restricted to a coset of a subgroup (zero elsewhere).   level = log2(support size).
# family "stab" : the same with a quadratic sign pattern allowed on the flat (the 240 real stabiliser states at k=3).
# A gate is a relation w = a*u + b*v with u, v, w in the family. For vectors with entries 0,+-1 the only possible (a,b) up to sign are
# (1,+-1), (1,+-2), (2,+-1), (1/2,+-1/2)  [derived in the report]; all are tried.
import sys, itertools
from collections import Counter
k=int(sys.argv[1]); fam=sys.argv[2]; N=1<<k; FULL=(1<<N)-1
def par(x): return bin(x).count("1")&1
def subspaces(k):
    seen=set()
    for d in range(k+1):
        for gens in itertools.combinations(range(1,1<<k),d):
            S={0}
            for g in gens: S|={s^g for s in S}
            if len(S)==1<<d: seen.add(frozenset(S))
    return seen
states={}   # (supp, signs&supp normalised so lowest point is +) -> level
def norm(supp,neg):
    neg&=supp
    low=supp&-supp
    if neg&low: neg=supp&~neg
    return (supp,neg)
quads=[0]
if fam=="stab":
    pairs=list(itertools.combinations(range(k),2))
    quads=range(1<<len(pairs))
for W in subspaces(k):
    d=len(W).bit_length()-1
    for t in range(N):
        C=frozenset(w^t for w in W)
        supp=sum(1<<x for x in C)
        for y in range(N):
            for qm in quads:
                neg=0
                for x in C:
                    s=par(x&y)
                    if qm:
                        for i,(a,b) in enumerate(pairs):
                            if qm>>i&1 and x>>a&1 and x>>b&1: s^=1
                    if s: neg|=1<<x
                states[norm(supp,neg)]=d
L=list(states.items())
print(f"k={k} family={fam}: {len(L)} values up to sign; by level:",sorted(Counter(states.values()).items()))
pat=Counter()
for i in range(len(L)):
    (su,nu),du=L[i]
    for j in range(i):
        (sv,nv),dv=L[j]
        ov=su&sv
        if ov==0:
            for fl in (0,1):                       # u + v, u - v
                w=norm(su|sv,nu|(nv^(sv if fl else 0)))
                if w in states: pat[tuple(sorted((du,dv)))+(states[w],"disjoint sum")]+=1
            continue
        diff=(nu^nv)&ov                             # where the signs differ on the overlap
        for same in (0,1):
            agree = (diff==0) if same==0 else (diff==ov)   # v == +u on overlap, or v == -u on overlap
            if not agree: continue
            vs = nv^(sv if same else 0)                    # v with the sign that makes it equal to u on the overlap
            # u - v' : cancels on overlap
            sw=(su|sv)&~ov
            if sw:
                w=norm(sw,(nu&~ov)|((vs^sv)&~ov&sv))
                if w in states: pat[tuple(sorted((du,dv)))+(states[w],"cancel on overlap")]+=1
            # flip: bigger - 2*smaller (needs containment)
            if ov==sv and su!=sv:
                w=norm(su,nu^sv)
                if w in states and w!=(su,nu): pat[tuple(sorted((du,dv)))+(states[w],"flip a piece: u-2v")]+=1
            if ov==su and su!=sv:
                w=norm(sv,vs^su)
                if w in states: pat[tuple(sorted((du,dv)))+(states[w],"flip a piece: u-2v")]+=1
        if su==sv and diff!=0 and diff!=ov:
            for part in (ov&~diff, diff):          # (u+v)/2 and (u-v)/2
                w=norm(part,nu&part)
                if w in states: pat[tuple(sorted((du,dv)))+(states[w],"half-sum on equal supports")]+=1
print("  relation patterns (level u, level v, level w, kind): count")
for kx,c in sorted(pat.items()): print("   ",kx,c)
mx=max(max(a,b,c)-min(a,b,c) for (a,b,c,_) in pat)
print("  largest spread of levels inside one relation:",mx)
