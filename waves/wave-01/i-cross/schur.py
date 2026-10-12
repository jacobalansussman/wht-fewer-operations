# i-cross hybrid 2: the Jordan basis of the add-one-element operator U (d-0) IS the total-spin / valence-bond basis (d-7).
# Exact integers. In that basis: U = weighted shift on each string, Z = exp(U) = Pascal blocks, H = (-2)^pairs * Krawtchouk blocks.
import sys
from fractions import Fraction as Fr
from math import comb, log2
def build(k):
    N=1<<k; groups={}
    for x in range(N):
        st=[]; pr=[]
        for pos in range(k):
            if (x>>pos)&1: st.append(pos)
            elif st: pr.append((st.pop(),pos))
        groups.setdefault(tuple(sorted(pr)),None)
    cols=[]; lab=[]
    for M in groups:
        matched=set(p for pq in M for p in pq); free=[p for p in range(k) if p not in matched]; u=len(free)
        pv={0:1}                                    # antisymmetric pairs
        for (a,b) in M:
            nv={}
            for idx,c in pv.items():
                nv[idx|(1<<a)]=nv.get(idx|(1<<a),0)+c; nv[idx|(1<<b)]=nv.get(idx|(1<<b),0)-c
            pv=nv
        for i in range(u+1):
            v=[0]*N
            for s in range(1<<u):
                if bin(s).count("1")!=i: continue
                add=sum(1<<free[t] for t in range(u) if (s>>t)&1)
                for idx,c in pv.items(): v[idx|add]+=c
            cols.append(v); lab.append((M,u,i))
    return cols, lab
def kraw(u,j,i): return sum((-1)**l*comb(j,l)*comb(u-j,i-l) for l in range(0,i+1) if l<=j and i-l<=u-j)
def wht(v,k):
    v=v[:]
    for j in range(k):
        h=1<<j
        for x in range(len(v)):
            if not x&h: a,b=v[x],v[x|h]; v[x],v[x|h]=a+b,a-b
    return v
def zeta(v,k):
    v=v[:]
    for j in range(k):
        h=1<<j
        for x in range(len(v)):
            if x&h: v[x]+=v[x^h]
    return v
def up(v,k):
    o=[0]*len(v)
    for T,c in enumerate(v):
        if c:
            for j in range(k):
                if not (T>>j)&1: o[T|(1<<j)]+=c
    return o
def comb_of(cols,terms,N):
    o=[0]*N
    for n,c in terms:
        if c:
            col=cols[n]
            for x in range(N):
                if col[x]: o[x]+=c*col[x]
    return o
for k in range(2,9):
    N=1<<k; cols,lab=build(k); pos={l:n for n,l in enumerate(lab)}
    okU=okH=okZ=True
    for (M,u,i),n in pos.items():
        v=cols[n]
        okU&= up(v,k)==comb_of(cols,[(pos[(M,u,i+1)],i+1)] if i<u else [],N)
        okZ&= zeta(v,k)==comb_of(cols,[(pos[(M,u,j)],comb(j,i)) for j in range(i,u+1)],N)
        okH&= wht(v,k)==comb_of(cols,[(pos[(M,u,j)],(-2)**len(M)*kraw(u,j,i)) for j in range(u+1)],N)
    p=2147483629; A=[[cols[c][r]%p for c in range(N)] for r in range(N)]; r=0
    for c in range(N):
        piv=next((i for i in range(r,N) if A[i][c]),None)
        if piv is None: continue
        A[r],A[piv]=A[piv],A[r]; inv=pow(A[r][c],p-2,p); Ar=A[r]
        for i in range(r+1,N):
            f=A[i][c]
            if f:
                f=f*inv%p; A[i]=[(x-f*y)%p for x,y in zip(A[i],Ar)]
        r+=1
    print("k=%d N=%d strings=%d rank mod p=%d  U=weighted shift:%s  Z=Pascal blocks:%s  H=(-2)^pairs*Krawtchouk blocks:%s  nonzeros of basis per entry %.2f" % (k,N,len(set(l[0] for l in lab)),r,okU,okZ,okH,sum(1 for c in cols for x in c if x)/N))
    sys.stdout.flush()
print("ledger of the middle, per entry (multiplicity f = C(k,w) - C(k,w-1), block size m = k - 2w + 1):")
for k in (4,16,64,256,1024):
    N=2**k; dense=0; fast=0; band=0
    for w in range(k//2+1):
        f=comb(k,w)-(comb(k,w-1) if w else 0); m=k-2*w+1
        dense+=f*m*m; fast+=float(Fr(f*m,N))*(log2(m) if m>1 else 0); band+=f*(m*(m-1)+m)
    print("  k=%4d  dense blocks %.2f   Pascal-diag-Pascal with plain Pascal passes %.2f   m*log2(m) model (fast Taylor shift) %.2f   log2 k = %.1f, sqrt k = %.1f" % (k, float(Fr(dense,N)), float(Fr(band,N)), fast, log2(k), k**0.5))
print("tie of the digit-swap route at textbook prices: T(q^2) = 2(q^2-q) + 2T(q) + 4(q-1)T(q/2), T(q) = q*log2 q")
for a in range(1,11):
    q=2**a; print("  q=%5d: route %d  textbook %d" % (q, 2*(q*q-q)+2*q*a+4*(q-1)*(q//2)*(a-1), q*q*2*a))
