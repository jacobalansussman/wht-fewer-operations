# 16 points, S form. Full-neighbourhood descent on  cost(frame) + cost(dual frame)  (greedy, count G), with plateau moves.
# Family: all cheap eigenvectors (subgroup sizes 2,4,8) PLUS, with flag 'wide', sums/differences of two of the 16 sparsest ones.
import sys, random, time; sys.path.insert(0,'waves/wave-02/e-1-vcycle')
from lib import *
seed=int(sys.argv[1]); budget=float(sys.argv[2]); wide=len(sys.argv)>3
random.seed(seed); t0=time.time()
k=4; N=16; S=sympS(k); m=6
fam={}
for D,a,b,f in atoms(k,(2,4,8)):
    v=canon(lin(4,f,-1,mv(S,f)))
    if v is not None: fam[v]=1
if wide:
    sp=[v for v in fam if nnz(v)==6]
    for a in sp:
        for b in sp:
            for s in (1,-1):
                v=canon(lin(1,a,s,b))
                if v is not None: fam[v]=1
V=sorted(fam); n=len(V); print('family',n,flush=True)
def dual_of(rows):
    g=[[ip(a,b) for b in rows] for a in rows]; gi=inv_exact(g)
    if gi is None: return None
    out=[]
    for i in range(m):
        v=[sum(gi[i][j]*rows[j][t] for j in range(m)) for t in range(N)]
        den=1
        for t in v: den=den*t.denominator//gcd(den,t.denominator)
        out.append(canon([int(t*den) for t in v]))
    return out
cache={}
def score(cur):
    key=tuple(sorted(cur))
    if key not in cache:
        rows=[V[i] for i in key]; d=dual_of(rows)
        cache[key]=None if d is None else (cse_cost(rows)+cse_cost(d),cse_cost(rows),cse_cost(d))
    return cache[key]
best=None
while time.time()-t0<budget:
    cur=random.sample(range(n),m); sc=score(cur)
    if sc is None: continue
    stall=0
    while time.time()-t0<budget and stall<3:
        moved=False
        for pos in random.sample(range(m),m):
            cands=random.sample(range(n),min(n,80))
            for cand in cands:
                if cand in cur: continue
                new=cur[:pos]+[cand]+cur[pos+1:]; sn=score(new)
                if sn is None: continue
                if sn[0]<sc[0] or (sn[0]==sc[0] and random.random()<0.15):
                    if sn[0]<sc[0]: moved=True
                    cur,sc=new,sn
            if time.time()-t0>budget: break
        stall=0 if moved else stall+1
    if best is None or sc[0]<best[0][0]:
        best=(sc,list(cur)); print('  local optimum',sc,' t=%.0fs'%(time.time()-t0),flush=True)
sc,cur=best
print('best found: cost(frame)+cost(dual) =',sc[0],'=',sc[1],'+',sc[2],'| program =',sc[0]+m,'against 56 known, 64 textbook')
for i in cur: print('   ',V[i])
