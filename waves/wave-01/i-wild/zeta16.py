#!/usr/bin/env python3
# i-wild, experiment D/E.  Exact integers / fractions.
# (i)   H = zeta^T diag((-2)^|S|) zeta      (zeta[S][v] = 1 if S subset of v)
# (ii)  truncation to |S|<=d is exact on every pair with overlap <= d; count exact entries
# (iii) zeta_2 = [[1,0],[1,1]] as a word in H_2 and diagonals (so zeta and H cost the same up to a factor 4 and O(N))
# (iv)  operation count of the "fold or restrict" program for zeta restricted to |S|<=d
# (v)   window width needed to cover most pairs, large k;  (vi) Schur-Weyl block cost against N k
from fractions import Fraction as F
from math import comb
wt=lambda v: bin(v).count('1')
def check(k):
    N=1<<k
    H=[[(-1)**(wt(v&w)&1) for w in range(N)] for v in range(N)]
    print("k=%d N=%d"%(k,N))
    for d in range(k+1):
        ok_all=True; exact=0; ok_window=True
        for v in range(N):
            for w in range(N):
                t=wt(v&w)
                val=sum(comb(t,j)*(-2)**j for j in range(d+1))   # = sum over S subset of v&w, |S|<=d
                if val==H[v][w]: exact+=1
                elif t<=d: ok_window=False
        print("  d=%d  exact on all pairs with overlap<=d: %s   entries exact: %d of %d (%.3f)   zeta_d ops (fold/restrict): %d = %.2f N"%(
            d,ok_window,exact,N*N,exact/(N*N),zops(k,d),zops(k,d)/N))
def zops(k,d,memo={}):
    # additions to get sum_{v superset S} x(v) for all |S|<=d on 2^k entries: fold on the last bit, then recurse
    if (k,d) in memo: return memo[(k,d)]
    if k==0: r=0
    elif d==0: r=(1<<k)-1
    else: r=(1<<(k-1))+zops(k-1,d)+zops(k-1,d-1)
    memo[(k,d)]=r; return r
check(4); check(6)
# (iii)
def mm(A,B): return [[sum(A[i][t]*B[t][j] for t in range(2)) for j in range(2)] for i in range(2)]
def dg(a,b): return [[F(a),F(0)],[F(0),F(b)]]
H2=[[F(1),F(1)],[F(1),F(-1)]]
W=dg(F(-1,15),F(-1,6))
for M in (H2,dg(F(3,2),F(-1,2)),H2,dg(1,2),H2,dg(F(-3,2),F(5,2)),H2): W=mm(W,M)
print("zeta_2 = D H D H D H D H:",W==[[1,0],[1,1]],[[str(x) for x in r] for r in W])
# (v) smallest window of consecutive overlaps holding a given share of all ordered pairs; P(t)=C(k,t)3^(k-t)/4^k
print("k   width for 90%   99%   99.99%    (sqrt k)")
for k in (16,64,256,1024,4096):
    p=[F(comb(k,t)*3**(k-t),4**k) for t in range(k+1)]
    out=[]
    for target in (F(9,10),F(99,100),F(9999,10000)):
        best=None; lo=0; s=F(0)
        for hi in range(k+1):
            s+=p[hi]
            while s-p[lo]>=target: s-=p[lo]; lo+=1
            if s>=target and (best is None or hi-lo+1<best): best=hi-lo+1
        out.append(best)
    print("%5d %8d %8d %8d    %.1f"%(k,out[0],out[1],out[2],k**0.5))
# (vi) Schur-Weyl: blocks of size k-2j+1 repeated C(k,j)-C(k,j-1) times
print("k   sum mult*size^2 / N   against k   ratio")
for k in (4,8,16,64,256,1024):
    N=1<<k; tot=sum((comb(k,j)-(comb(k,j-1) if j else 0))*(k-2*j+1)**2 for j in range(k//2+1))
    chk=sum((comb(k,j)-(comb(k,j-1) if j else 0))*(k-2*j+1) for j in range(k//2+1))
    assert chk==N
    print("%5d %14.2f %10d %8.3f"%(k,float(F(tot,N)),k,float(F(tot,N*k))))
