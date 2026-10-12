# first.py (ab-7): the first experiment. Exact whole numbers / fractions.
# P = Pascal matrix C(s,t); Z = P mod 2 (subset sums); H = transform.
# A. P D' P^T against H for D' = (-2)^t and D'' = (-2)^(ones of t): agreement modulo 4, 8, 16; ranks.
# B. W = Z^-1 P (the correction between the row and the cube): closed form, size, 2-adic picture.
import sys
from math import comb
from fractions import Fraction
def ones(t): return bin(t).count("1")
def mul(A,B):
    n=len(A); m=len(B[0]); Bt=list(zip(*B))
    return [[sum(a*b for a,b in zip(r,c)) for c in Bt] for r in A]
def tr(A): return [list(r) for r in zip(*A)]
def rankQ(M):
    M=[[Fraction(x) for x in r] for r in M]; r=0; n=len(M); m=len(M[0])
    for c in range(m):
        p=None
        for i in range(r,n):
            if M[i][c]!=0: p=i;break
        if p is None: continue
        M[r],M[p]=M[p],M[r]
        for i in range(n):
            if i!=r and M[i][c]!=0:
                f=M[i][c]/M[r][c]; M[i]=[a-f*b for a,b in zip(M[i],M[r])]
        r+=1
    return r
def rank2(M):
    rows=[sum((x&1)<<j for j,x in enumerate(r)) for r in M]; r=0
    for bit in range(len(M[0])):
        p=None
        for i in range(r,len(rows)):
            if rows[i]>>bit&1: p=i;break
        if p is None: continue
        rows[r],rows[p]=rows[p],rows[r]
        for i in range(len(rows)):
            if i!=r and rows[i]>>bit&1: rows[i]^=rows[r]
        r+=1
    return r
def val2(x):
    if x==0: return 99
    v=0
    while x%2==0: x//=2; v+=1
    return v
for k in (2,3,4,5):
    N=1<<k
    P=[[comb(s,t) for t in range(N)] for s in range(N)]
    Z=[[1 if (s&t)==t else 0 for t in range(N)] for s in range(N)]
    H=[[(-1)**ones(s&t) for t in range(N)] for s in range(N)]
    assert all((P[s][t]-Z[s][t])%2==0 for s in range(N) for t in range(N))   # Lucas
    Dz=[(-2)**ones(t) for t in range(N)]
    assert mul([[Z[s][t]*Dz[t] for t in range(N)] for s in range(N)],tr(Z))==H
    print(f"== N={N}")
    for name,D in (("D'=(-2)^t",[(-2)**t for t in range(N)]),("D''=(-2)^ones(t)",Dz)):
        M=mul([[P[s][t]*D[t] for t in range(N)] for s in range(N)],tr(P))
        E=[[M[s][t]-H[s][t] for t in range(N)] for s in range(N)]
        v=min(val2(x) for r in E for x in r)
        line=f"  {name}: largest entry {max(abs(x) for r in M for x in r)}; difference from H: 2-adic valuation {v}, rank over Q {rankQ(E)}"
        for m in (4,8,16):
            bad=sum(1 for r in E for x in r if x%m)
            line+=f"; entries wrong mod {m}: {bad}/{N*N}"
        Ev=[[x>>v for x in r] for r in E]
        line+=f"; rank mod 2 of difference/2^{v}: {rank2(Ev)}"
        print(line)
        if N==4: print("   P D P^T =",M)
    # B. W = Z^-1 P
    Zi=[[(-1)**(ones(s)-ones(t)) if (s&t)==t else 0 for t in range(N)] for s in range(N)]
    W=mul(Zi,P)
    # closed form: row t = coefficients of prod_{i in t} ((1+y)^(2^i) - 1)
    for t in range(N):
        pol=[1]
        for i in range(k):
            if t>>i&1:
                f=[comb(1<<i,j) for j in range((1<<i)+1)]; f[0]-=1
                new=[0]*(len(pol)+len(f)-1)
                for a,x in enumerate(pol):
                    for b,y in enumerate(f): new[a+b]+=x*y
                pol=new
        pol=pol+[0]*(N-len(pol))
        assert pol[:N]==W[t], (t,pol,W[t])
    nz=sum(1 for r in W for x in r if x)
    E=[[(W[s][t]-(s==t)) for t in range(N)] for s in range(N)]
    assert all(x%2==0 for r in E for x in r)
    E2=[[x//2 for x in r] for r in E]
    print(f"  W = Z^-1 P: closed form checked; non-zeros {nz} (Z has {3**k}, P has {N*(N+1)//2}); largest entry {max(abs(x) for r in W for x in r)}; W = I mod 2; rank mod 2 of (W-I)/2: {rank2(E2)}; non-zeros of (W-I)/2 mod 2: {sum(1 for r in E2 for x in r if x%2)}; rank over Q of W-I: {rankQ(E)}")
    # P - Z itself
    F=[[(P[s][t]-Z[s][t])//2 for t in range(N)] for s in range(N)]
    print(f"  (P-Z)/2: rank over Q {rankQ(F)}, rank mod 2 {rank2(F)}, odd entries {sum(1 for r in F for x in r if x%2)}, non-zero entries {sum(1 for r in F for x in r if x)}")
    # middle matrix of H in the row basis: Mid = W^-1 D W^-T  (H = P Mid P^T)
    if N<=16:
        Pi=[[(1 if (s-t)%2==0 else -1)*comb(s,t) for t in range(N)] for s in range(N)]
        Mid=mul(mul(Pi,H),tr(Pi))
        offd=sum(1 for s in range(N) for t in range(N) if s!=t and Mid[s][t])
        print(f"  H = P Mid P^T: Mid has {offd} off-diagonal non-zeros of {N*N-N}; diagonal {[Mid[s][s] for s in range(N)]}")
        if N==4: print("   Mid =",Mid)
