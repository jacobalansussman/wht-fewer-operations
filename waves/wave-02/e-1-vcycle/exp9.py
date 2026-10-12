# 64 points, S form: how cheap can the ANALYSIS of a frame of the 28-dimensional minus space be (count G, greedy upper bound),
# using the sparsest cheap eigenvectors (12 non-zeros)?  Pattern to test: 3 gates at 4 points, 24 at 16 = (3/8) N log2 N -> 144 at 64.
# Then the cost of the dual frame for the best one.
import sys, random, time; sys.path.insert(0,'waves/wave-02/e-1-vcycle')
from lib import *
random.seed(int(sys.argv[1])); budget=float(sys.argv[2]); t0=time.time()
k=6; N=64; m=28; S=sympS(k)
def fast_cse(rows):
    rows=[dict(rw) for rw in rows]; gates=0; nxt=10**6
    while True:
        cnt={}
        for rw in rows:
            if len(rw)<2: continue
            it=sorted(rw.items())
            for x in range(len(it)):
                i,ci=it[x]
                for y in range(x+1,len(it)):
                    j,cj=it[y]; g=gcd(ci,cj); a=ci//g; b=cj//g
                    if a<0: a=-a; b=-b
                    key=(i,j,a,b); cnt[key]=cnt.get(key,0)+1
        if not cnt: break
        (i,j,a,b),c=max(cnt.items(),key=lambda kv:(kv[1],-kv[0][0],-kv[0][1]))
        for rw in rows:
            if i in rw and j in rw:
                ci=rw[i]; cj=rw[j]
                if ci*b==cj*a:
                    del rw[i]; del rw[j]
                    if ci%a: 
                        for q in list(rw): rw[q]*=a
                        ci*=a
                    rw[nxt]=ci//a
        nxt+=1; gates+=1
    return gates
def sparse(v): return {i:t for i,t in enumerate(v) if t}
# the three-scale family of exp4 (subgroup sizes 2, 8, 32), kept: all with 12 non-zeros and a sample of those with 16
r=8
def sw(y):
    z=0
    for i in range(0,k,2): z|=(((y>>(i+1))&1)<<i)|(((y>>i)&1)<<(i+1))
    return z
SW=[sw(y) for y in range(N)]; PAR=[bin(x).count('1')&1 for x in range(N)]
fam={}
for D in [D for D in subspaces(k) if len(D)==8]:
    gens=[]; span={0}
    for d in D:
        if d not in span: gens.append(d); span|={s_^d for s_ in span}
    got=set(); cos=[]
    for a in range(N):
        if a in got: continue
        c=[a^d for d in D]; got|=set(c); cos.append((a,c))
    chars={}
    for b in range(N):
        key=tuple(PAR[b&d] for d in gens)
        if key not in chars: chars[key]=b
    for a,c in cos:
        for b in chars.values():
            v=[0]*N
            for x in c: v[x]=r*(1-2*PAR[b&x])
            sgn_a=PAR[b&a]
            for y in range(N):
                sy=SW[y]
                if all(PAR[b&d]==PAR[d&sy] for d in gens): v[y]-=8*(1-2*(sgn_a^PAR[a&sy]))
            cv=canon(v)
            if cv is not None: fam[cv]=1
V12=sorted(v for v in fam if nnz(v)==12); V16=sorted(v for v in fam if nnz(v)==16)
V=V12+random.sample(V16,600); n=len(V)
assert all(mv(S,v)==tuple(-8*t for t in v) for v in random.sample(V,30))
print('minus vectors kept:',len(V12),'with 12 non-zeros (rank',rank_exact(V12),') and 600 of the',len(V16),'with 16; rank of all kept',rank_exact(V),flush=True)
SPV=[sparse(v) for v in V]
def pick():
    order=random.sample(range(n),n); cur=[]; rows=[]
    for i in order:
        if rank_exact(rows+[V[i]])==len(rows)+1: cur.append(i); rows.append(V[i])
        if len(cur)==m: break
    return cur
best=None
while time.time()-t0<budget:
    cur=pick()
    if len(cur)<m: print('rank too small'); break
    c=fast_cse([SPV[i] for i in cur]); moved=True
    while moved and time.time()-t0<budget:
        moved=False
        for pos in random.sample(range(m),m):
            for cand in random.sample(range(n),25):
                if cand in cur: continue
                new=cur[:pos]+[cand]+cur[pos+1:]; cn=fast_cse([SPV[i] for i in new])
                if cn<c and rank_exact([V[i] for i in new])==m: cur,c=new,cn; moved=True
            if time.time()-t0>budget: break
    if best is None or c<best[0]: best=(c,list(cur)); print('  analysis cost',c,' t=%.0fs'%(time.time()-t0),flush=True)
c,cur=best; rows=[V[i] for i in cur]
print('64 points: cheapest analysis found for a frame of the minus space:',c,'gates  | (3/8) N log2 N = 144 | tensor orthogonal frame 246 | non-zeros',sum(nnz(v) for v in rows),flush=True)
g=[[ip(a,b) for b in rows] for a in rows]; gi=inv_exact(g)
print('Gram: non-zeros',sum(1 for r_ in g for t in r_ if t),'of',m*m,'| inverse non-zeros',sum(1 for r_ in gi for t in r_ if t),flush=True)
dual=[]
for i in range(m):
    v=[sum(gi[i][j]*rows[j][t] for j in range(m)) for t in range(N)]
    den=1
    for t in v: den=den*t.denominator//gcd(den,t.denominator)
    dual.append(canon([int(t*den) for t in v]))
cd=fast_cse([sparse(v) for v in dual])
print('dual frame: non-zeros',sum(nnz(v) for v in dual),'greedy cost',cd,'| program = frame + dual + m =',c+cd+m,'| references: 336 (one reflection per digit, G), 384 textbook',flush=True)
import json; json.dump({'frame':rows,'analysis':c,'dual':cd},open('exp9.frame.%s.json'%sys.argv[1],'w'))
