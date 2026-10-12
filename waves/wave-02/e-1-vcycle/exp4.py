# 64 points: orthogonal frames of the 28-dimensional minus space from cheap eigenvectors of three scales (subgroup sizes 2, 8, 32),
# against the tensor frame.  Count (G), greedy upper bound.  Exact integers.
import sys, random, time; sys.path.insert(0,'waves/wave-02/e-1-vcycle')
from lib import *
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 7)
t0=time.time()
k=6; N=64; r=8; m=28
def sw(y):
    z=0
    for i in range(0,k,2): z|=(((y>>(i+1))&1)<<i)|(((y>>i)&1)<<(i+1))
    return z
SW=[sw(y) for y in range(N)]
PAR=[bin(x).count('1')&1 for x in range(N)]
def fast_cse(rows):
    """same greedy as lib.cse_cost, integer keys; rows: list of dict col->int"""
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
                    del rw[i]; del rw[j]; rw[nxt]=ci//a if ci%a==0 else Fraction(ci,a)
        # keep integers: rescale any row holding a Fraction
        for rw in rows:
            if any(isinstance(v,Fraction) for v in rw.values()):
                den=1
                for v in rw.values():
                    if isinstance(v,Fraction): den=den*v.denominator//gcd(den,v.denominator)
                for q in list(rw): rw[q]=int(rw[q]*den)
        nxt+=1; gates+=1
    return gates
def sparse(v): return {i:t for i,t in enumerate(v) if t}
# --- the family
fam={}
subs=[D for D in subspaces(k) if len(D) in (2,8,32)]
print('subgroups of sizes 2, 8, 32:',len(subs),' t=%.0fs'%(time.time()-t0),flush=True)
for D in subs:
    gens=[]; span={0}
    for d in D:
        if d not in span: gens.append(d); span|={s^d for s in span}
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
            # image under S: supported on y with (b.d + B(d,y)) = 0 for the generators d of D
            sgn_a=PAR[b&a]
            for y in range(N):
                sy=SW[y]
                if all(PAR[b&d]==PAR[d&sy] for d in gens):
                    v[y]-=len(D)*(1-2*(sgn_a^PAR[a&sy]))
            cv=canon(v)
            if cv is not None and cv not in fam: fam[cv]=len(D)
V=list(fam); n=len(V)
print('minus vectors, distinct up to scale:',n,' t=%.0fs'%(time.time()-t0),flush=True)
S=sympS(k)
chk=random.sample(V,20); print('  spot check S v = -8 v on 20:',all(mv(S,v)==tuple(-8*t for t in v) for v in chk))
hist={}
for v in V: hist[nnz(v)]=hist.get(nnz(v),0)+1
print('  non-zeros histogram',dict(sorted(hist.items())),flush=True)
SP=[sorted(sparse(v).items()) for v in V]
# --- tensor orthogonal frame
u=(1,-1,-1,-1); W=[(1,1,0,0),(0,0,1,-1),(1,-1,1,1)]
def kron(a,b): return tuple(x*y for x in a for y in b)
T=[kron(kron(u,u),u)]
for w1 in W:
    for w2 in W:
        T+= [kron(kron(u,w1),w2),kron(kron(w1,u),w2),kron(kron(w1,w2),u)]
assert len(T)==m and all(mv(S,v)==tuple(-8*t for t in v) for v in T) and all(ip(T[i],T[j])==0 for i in range(m) for j in range(i))
c=fast_cse([sparse(v) for v in T])
print('tensor orthogonal frame: non-zeros',sum(nnz(v) for v in T),'greedy s_R',c,'| program 2*s_R+m =',2*c+m,'| law (N-m)+m*log2(N) =',N-m+m*k,' t=%.0fs'%(time.time()-t0),flush=True)
# --- random orthogonal frames from the three-scale family
found=0
for trial in range(200):
    if time.time()-t0>430 or found>=3: break
    cand=list(range(n)); random.shuffle(cand); frame=[]
    while cand and len(frame)<m:
        # prefer sparse vectors with probability 1/2, to see both kinds
        i=cand[0] if trial%2 else min(cand[:50],key=lambda q:len(SP[q]))
        frame.append(i); d=V[i]
        cand=[j for j in cand if j!=i and sum(d[p]*t for p,t in SP[j])==0]
    if len(frame)<m: 
        if trial<6: print('  trial',trial,'stuck at',len(frame),flush=True)
        continue
    found+=1
    rows=[V[i] for i in frame]
    assert rank_exact(rows)==m
    c=fast_cse([sparse(v) for v in rows])
    sc={}
    for i in frame: sc[fam[V[i]]]=sc.get(fam[V[i]],0)+1
    print('orthogonal frame from the family (trial %d): subgroup sizes used'%trial,dict(sorted(sc.items())),'non-zeros',sum(nnz(v) for v in rows),
          'greedy s_R',c,'| program 2*s_R+m =',2*c+m,' t=%.0fs'%(time.time()-t0),flush=True)
print('references at 64 points: textbook 384 (O), one-reflection-per-digit 336 (G)')
