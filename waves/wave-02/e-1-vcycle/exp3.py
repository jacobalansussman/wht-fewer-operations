# (1) exact checks of identities; (2) cheapest NON-orthogonal frames at 16 points and what the middle R L then is.
import sys, random; sys.path.insert(0,'waves/wave-02/e-1-vcycle')
from lib import *
random.seed(1)
# ---- identity A: plus space of plain H_N is the graph of Gamma = (2/sqrt N) h - I  (N = 16, 64)
for k in (4,6):
    N=1<<k; r=1<<(k//2); H=plainH(k); h=plainH(k-1); n=N//2
    ok=True
    for t in range(n):
        u=[int(i==t) for i in range(n)]
        hu=mv(h,u); v=[Fraction(2*a,r)-b for a,b in zip(hu,u)]
        x=list(u)+v; y=mv(H,x)
        ok&=all(a==r*b for a,b in zip(y,x))
    print('identity A (plus space = graph of (2/sqrt N) h - I) at N =',N,':',ok)
# ---- identity B: tensor orthogonal frame at 16, S = 4 I - 2 L D^-1 L^T, hand count 32+32+6 = 70
k=4; N=16; S=sympS(k)
u=(1,-1,-1,-1); W=[(1,1,0,0),(0,0,1,-1),(1,-1,1,1)]
def kron(a,b): return tuple(x*y for x in a for y in b)
Lc=[kron(u,w) for w in W]+[kron(w,u) for w in W]
print('tensor frame: all in minus space',all(mv(S,v)==tuple(-4*t for t in v) for v in Lc),
      '| Gram diagonal',all(ip(Lc[i],Lc[j])==0 for i in range(6) for j in range(6) if i!=j),
      '| norms',[ip(v,v) for v in Lc],'| greedy s_R',cse_cost(Lc))
rec=[[4*(i==j)-sum(Fraction(2*4*v[i]*v[j],ip(v,v)) for v in Lc) for j in range(N)] for i in range(N)]
print('  S == 4I - 8 * sum v v^T/|v|^2 :',rec==S)
# ---- cheapest frames, orthogonal or not
def minus_vectors(M,sizes,r):
    out={}
    for D,a,b,f in atoms(k,sizes):
        v=canon(lin(r,f,-1,mv(M,f)))
        if v is not None and v not in out: out[v]=(len(D),a,b)
    return out
for name,M,m in (('S',S,6),('H',plainH(k),8)):
    V=sorted(minus_vectors(M,(2,4,8),4)); n=len(V)
    best=None
    for trial in range(40):
        while True:
            cur=random.sample(range(n),m)
            if rank_exact([V[i] for i in cur])==m: break
        c=cse_cost([V[i] for i in cur])
        improved=True
        while improved:
            improved=False
            for pos in random.sample(range(m),m):
                for cand in random.sample(range(n),60):
                    if cand in cur: continue
                    new=cur[:pos]+[cand]+cur[pos+1:]
                    cn=cse_cost([V[i] for i in new])
                    if cn<c and rank_exact([V[i] for i in new])==m:
                        cur,c=new,cn; improved=True
        if best is None or c<best[0]: best=(c,list(cur))
    c,cur=best; rows=[V[i] for i in cur]
    G=[[ip(a,b) for b in rows] for a in rows]; Gi=inv_exact(G)
    print('==',name,'cheapest frame found by local search (greedy count G): s_R =',c,'non-zeros',sum(nnz(v) for v in rows))
    for v in rows: print('   ',v)
    print('   middle G = R L (R = L^T): non-zeros',sum(1 for r_ in G for t in r_ if t),'of',m*m,'| inverse non-zeros',sum(1 for r_ in Gi for t in r_ if t))
    for r_ in G: print('     ',r_)
    print('   program if the middle is applied densely: 2*s_R + m + (nnz(G^-1) - m) =',2*c+sum(1 for r_ in Gi for t in r_ if t))
