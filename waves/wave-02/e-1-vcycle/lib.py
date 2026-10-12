# e-1-vcycle: common tools. Exact integer arithmetic throughout (numpy int64; entries stay tiny).
import itertools, sys
from math import gcd
from functools import reduce
from fractions import Fraction

def dot2(a,b): return bin(a&b).count('1')&1

def subspaces(k):
    """all subspaces of F_2^k as sorted tuples of elements"""
    N=1<<k; seen={(0,)}; frontier=[(0,)]
    while frontier:
        new=[]
        for D in frontier:
            Ds=set(D)
            for v in range(1,N):
                if v in Ds: continue
                E=tuple(sorted(Ds|{d^v for d in D}))
                if E not in seen: seen.add(E); new.append(E)
        frontier=new
    return sorted(seen,key=lambda D:(len(D),D))

def plainH(k):
    N=1<<k
    return [[(-1)**dot2(x,y) for y in range(N)] for x in range(N)]

def sympS(k):
    """symplectic form of the transform: bits paired (0,1),(2,3),...; diagonal all +1"""
    N=1<<k
    def sw(y):
        z=0
        for i in range(0,k,2):
            b0=(y>>i)&1; b1=(y>>(i+1))&1
            z|=(b1<<i)|(b0<<(i+1))
        return z
    return [[(-1)**dot2(x,sw(y)) for y in range(N)] for x in range(N)]

def atoms(k,sizes):
    """coset atoms: (-1)^(b.x) on the coset a+D, for subgroups D with |D| in sizes.
    returns list of (D, a, b, vector) with one representative per (coset, restricted character), sign normalised"""
    N=1<<k; out=[]; seen=set()
    for D in subspaces(k):
        if len(D) not in sizes: continue
        Ds=set(D)
        cos=[]; got=set()
        for a in range(N):
            if a in got: continue
            c=[a^d for d in D]; got|=set(c); cos.append((a,c))
        chars={}
        for b in range(N):
            key=tuple(dot2(b,d) for d in D)
            if key not in chars: chars[key]=b
        for a,c in cos:
            for b in chars.values():
                v=[0]*N
                for x in c: v[x]=(-1)**dot2(b,x)
                if next(t for t in v if t)<0: v=[-t for t in v]
                t=tuple(v)
                if t in seen: continue
                seen.add(t); out.append((D,a,b,t))
    return out

def rank_exact(M):
    """exact rank over Q of an integer matrix (fraction-free Bareiss on python ints)"""
    A=[list(map(int,r)) for r in M]; 
    if not A: return 0
    m=len(A); n=len(A[0]); r=0; prev=1
    for c in range(n):
        p=None
        for i in range(r,m):
            if A[i][c]!=0: p=i; break
        if p is None: continue
        A[r],A[p]=A[p],A[r]
        for i in range(r+1,m):
            if A[i][c]!=0 or True:
                Ai=A[i]; Ar=A[r]; f=Ai[c]; g=Ar[c]
                A[i]=[(g*Ai[j]-f*Ar[j])//prev for j in range(n)]
        prev=A[r][c]; r+=1
        if r==m: break
    return r

def inv_exact(M):
    n=len(M); A=[[Fraction(int(M[i][j])) for j in range(n)]+[Fraction(int(i==j)) for j in range(n)] for i in range(n)]
    for c in range(n):
        p=next((i for i in range(c,n) if A[i][c]!=0),None)
        if p is None: return None
        A[c],A[p]=A[p],A[c]
        iv=1/A[c][c]; A[c]=[a*iv for a in A[c]]
        for i in range(n):
            if i!=c and A[i][c]!=0:
                f=A[i][c]; A[i]=[a-f*b for a,b in zip(A[i],A[c])]
    return [r[n:] for r in A]

def cse_cost(M):
    """Upper bound, count (G): gates a*u+b*v with free scalings, to compute all rows of M (rows = outputs, cols = inputs).
    Greedy: repeatedly merge the pair of columns (i,j) with ratio rho used by the most rows."""
    rows=[{j:Fraction(int(v)) for j,v in enumerate(r) if v!=0} for r in M]
    gates=0; nxt=len(M[0]) if len(M) else 0
    while True:
        cnt={}
        for r in rows:
            if len(r)<2: continue
            ks=sorted(r)
            for x in range(len(ks)):
                for y in range(x+1,len(ks)):
                    key=(ks[x],ks[y],r[ks[y]]/r[ks[x]])
                    cnt[key]=cnt.get(key,0)+1
        if not cnt: break
        (i,j,rho),c=max(cnt.items(),key=lambda kv:(kv[1],-kv[0][0],-kv[0][1]))
        for r in rows:
            if i in r and j in r and r[j]/r[i]==rho:
                ci=r[i]; del r[i]; del r[j]; r[nxt]=ci
        nxt+=1; gates+=1
    # identical rows (up to scale) are the same wire: no extra cost
    return gates

def mv(M,v): return tuple(sum(a*b for a,b in zip(r,v) if b) for r in M)
def lin(a,u,b,v): return tuple(a*x+b*y for x,y in zip(u,v))
def ip(u,v): return sum(a*b for a,b in zip(u,v))
def nnz(v): return sum(1 for t in v if t)
def canon(v):
    g=reduce(gcd,(abs(t) for t in v))
    if g==0: return None
    v=[t//g for t in v]
    if next(t for t in v if t)<0: v=[-t for t in v]
    return tuple(v)
def matmul(A,B):
    Bt=list(zip(*B)); return [[sum(a*b for a,b in zip(r,c)) for c in Bt] for r in A]
def transpose(A): return [list(r) for r in zip(*A)]
