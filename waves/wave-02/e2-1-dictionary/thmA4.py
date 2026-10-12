# e2-1-dictionary / thmA4.py : brute-force check of Theorem A at 4 points (k = 2), exact.
# Pool "coset": the 20 coset characters. Pool "stab": the same plus quadratic sign patterns on the whole plane (24 vectors).
# A program = a set S of non-input pool vectors that can be ordered so that each lies on a line through two earlier ones (or inputs).
# Least |S| containing the targets (the 4 characters; for "stab" also the 4 characters times the quadratic sign pattern, a free input scaling).
import itertools, sys
from fractions import Fraction
N=4
def par(x): return bin(x).count("1")&1
def pool(stab):
    P={}
    subs=[[0],[0,1],[0,2],[0,3],[0,1,2,3]]
    for W in subs:
        for t in range(4):
            C=sorted({w^t for w in W})
            for y in range(4):
                for q in ((0,1) if (stab and len(C)==4) else (0,)):
                    v=[0]*4
                    for x in C: v[x]=(-1)**(par(x&y)^(q&(x&1)&(x>>1)))
                    f=next(a for a in v if a)
                    v=tuple(a*f for a in v)          # sign-normalised
                    P[v]=len(C).bit_length()-1
    return P
def rank2(u,v,w):
    M=[list(map(Fraction,r)) for r in (u,v,w)]; rk=0
    for c in range(4):
        p=next((i for i in range(rk,3) if M[i][c]),None)
        if p is None: continue
        M[rk],M[p]=M[p],M[rk]
        for i in range(rk+1,3):
            if M[i][c]:
                f=M[i][c]/M[rk][c]; M[i]=[a-f*b for a,b in zip(M[i],M[rk])]
        rk+=1
    return rk==2
for name in ("coset","stab"):
    P=pool(name=="stab"); vecs=list(P)
    inputs=[v for v in vecs if P[v]==0]; others=[v for v in vecs if P[v]>0]
    allv=inputs+others; n_in=len(inputs); m=len(others)
    idx={v:i for i,v in enumerate(allv)}
    # for each non-input j: list of pairs (a,b) of indices (in allv) whose line contains it
    makers=[[] for _ in range(m)]
    for j,w in enumerate(others):
        for a,b in itertools.combinations(range(len(allv)),2):
            if a==n_in+j or b==n_in+j: continue
            if rank2(allv[a],allv[b],w): makers[j].append((a,b))
    full_in=(1<<n_in)-1
    build=bytearray(1<<m); build[0]=1
    for S in range(1,1<<m):
        ok=0
        for j in range(m):
            if S>>j&1 and build[S^(1<<j)]:
                held=full_in | ((S^(1<<j))<<n_in)
                for a,b in makers[j]:
                    if held>>a&1 and held>>b&1: ok=1; break
                if ok: break
        build[S]=ok
    def best(targets):
        tm=0
        for t in targets: tm|=1<<(idx[t]-n_in)
        return min(bin(S).count("1") for S in range(1<<m) if build[S] and S&tm==tm)
    chars=[tuple((-1)**par(x&y) for x in range(4)) for y in range(4)]
    norm=lambda v: tuple(a*next(b for b in v if b) for a in v)
    print(f"pool {name}: {len(allv)} vectors (levels {sorted(P.values()).count(0)},{sorted(P.values()).count(1)},{sorted(P.values()).count(2)}); "
          f"least gates for the 4 characters: {best([norm(c) for c in chars])}", end="")
    if name=="stab":
        qc=[norm(tuple(c[x]*(-1)**((x&1)&(x>>1)) for x in range(4))) for c in chars]
        print(f"; for the 4 characters times the sign pattern (-1)^(x1 x2): {best(qc)}")
    else: print()
