# (1) exact identity checks. (2) 16 points, S form: the search objective with NO middle:
#     program = cost(dual frame as 16->6 functionals) + cost(frame as 16->6 functionals) + 6 ; known 56 ; count (G), greedy upper bounds.
#     Is cost(frame) + cost(dual frame) conserved?
import sys, random, time; sys.path.insert(0,'waves/wave-02/e-1-vcycle')
from lib import *
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 3); t0=time.time()
for k in (4,6):
    N=1<<k; r=1<<(k//2); H=plainH(k); h=plainH(k-1); n=N//2; ok=True
    for t in range(n):
        u=[int(i==t) for i in range(n)]; hu=mv(h,u); v=[Fraction(2*a,r)-b for a,b in zip(hu,u)]
        x=list(u)+v; y=mv(H,x); ok&=all(a==r*b for a,b in zip(y,x))
    print('identity A: plus space of H_N = graph of (2/sqrt N) h_(N/2) - I, N =',N,':',ok,flush=True)
k=4; N=16; S=sympS(k); m=6
u=(1,-1,-1,-1); W=[(1,1,0,0),(0,0,1,-1),(1,-1,1,1)]
def kron(a,b): return tuple(x*y for x in a for y in b)
Lc=[kron(u,w) for w in W]+[kron(w,u) for w in W]
rec=[[4*(i==j)-sum(Fraction(8*v[i]*v[j],ip(v,v)) for v in Lc) for j in range(N)] for i in range(N)]
print('tensor orthogonal frame: in minus space',all(mv(S,v)==tuple(-4*t for t in v) for v in Lc),'| S == 4I - 8 sum v v^T/|v|^2 :',rec==S,'| greedy s_R',cse_cost(Lc),flush=True)
# the 8 signed row / column contractions and the 16 sparsest vectors
E=[tuple(int(i==j) for i in range(4)) for j in range(4)]
P=[kron(u,E[j]) for j in range(4)]; Q=[kron(E[i],u) for i in range(4)]
sp=set()
for i in range(4):
    for j in range(4):
        eps=u[j]*u[i]; v=lin(1,P[j],-eps,Q[i]); assert mv(S,v)==tuple(-4*t for t in v) and nnz(v)==6; sp.add(canon(v))
print('the 16 vectors (column contraction j) -+ (row contraction i): all in the minus space, 6 non-zeros each, distinct:',len(sp),
      '| greedy cost of the 8 contractions',cse_cost(P+Q),flush=True)
def dual_of(rows):
    g=[[ip(a,b) for b in rows] for a in rows]; gi=inv_exact(g)
    if gi is None: return None
    out=[]
    for i in range(len(rows)):
        v=[sum(gi[i][j]*rows[j][t] for j in range(len(rows))) for t in range(N)]
        den=1
        for t in v: den=den*t.denominator//gcd(den,t.denominator)
        out.append(canon([int(t*den) for t in v]))
    return out
fam={}
for D,a,b,f in atoms(k,(2,4,8)):
    v=canon(lin(4,f,-1,mv(S,f)))
    if v is not None: fam[v]=1
V=sorted(fam); n=len(V); print('family:',n,'minus vectors',flush=True)
def score(cur):
    rows=[V[i] for i in cur]; d=dual_of(rows)
    if d is None: return None
    a=cse_cost(rows); b=cse_cost(d); return (a+b,a,b)
hist={}; best=None
budget=float(sys.argv[2]) if len(sys.argv)>2 else 150
while time.time()-t0<budget:
    cur=random.sample(range(n),m); sc=score(cur)
    if sc is None: continue
    hist[sc[0]]=hist.get(sc[0],0)+1
    improved=True
    while improved and time.time()-t0<budget:
        improved=False
        for pos in random.sample(range(m),m):
            for cand in random.sample(range(n),12):
                if cand in cur: continue
                new=cur[:pos]+[cand]+cur[pos+1:]; sn=score(new)
                if sn is not None and sn[0]<sc[0]: cur,sc=new,sn; improved=True
    if best is None or sc<best[0]: best=(sc,list(cur)); print('  local optimum',sc,' t=%.0fs'%(time.time()-t0),flush=True)
print('random frames: histogram of cost(frame)+cost(dual):',dict(sorted(hist.items())))
sc,cur=best
print('best found: cost(frame)+cost(dual) =',sc[0],'=',sc[1],'+',sc[2],'| program =',sc[0]+m,'against 56 known, 64 textbook')
for i in cur: print('   ',V[i])
print('   dual:')
for v in dual_of([V[i] for i in cur]): print('   ',v)
