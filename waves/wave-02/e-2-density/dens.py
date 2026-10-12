#!/usr/bin/env python3
# e-2-density/dens.py: the table f(S) = least gate count (count G) of the outputs S of the 16-point Walsh-Hadamard transform,
# for one representative S of every orbit of m-subsets of the 4-cube under its affine symmetries.
# DUAL FORM [derived, transposition principle]: f(S) = 16 - m + g(S), g(S) = least gates to build, from the m unit vectors,
# the 2^r "sign vectors" t_x = (chi_s(x))_{s in S} (r = affine dimension of S); g(S) = 2^r + iota(S), iota = helper points.
# upper bounds: U(S) by dynamic programming over two families of circuits (trie and walk); exact iota over GF(p) by d-0's mincirc.
import sys, itertools, subprocess, time, os
from functools import lru_cache
n=4; N=16
MINC="waves/wave-01/d-0-zeta/mincirc"
pc=lambda v: bin(v).count("1")
def affdim(S):
    S=list(S); t0=S[0]; basis=[]
    for t in S[1:]:
        v=t^t0
        for b in basis: v=min(v,v^b)
        if v: basis.append(v)
    return len(basis)
def orbits(m):
    subs=[sum(1<<i for i in c) for c in itertools.combinations(range(N),m)]
    idx={s:i for i,s in enumerate(subs)}; par=list(range(len(subs)))
    def find(a):
        while par[a]!=a: par[a]=par[par[a]]; a=par[a]
        return a
    gens=[]
    gens.append([v^1 for v in range(N)])                                   # a translation
    for i in range(n):
        for j in range(n):
            if i!=j: gens.append([v^(((v>>j)&1)<<i) for v in range(N)])     # x_i += x_j
    for g in gens:
        for s in subs:
            t=sum(1<<g[i] for i in range(N) if s>>i&1)
            a,b=find(idx[s]),find(idx[t])
            if a!=b: par[a]=b
    reps={}
    for s in subs:
        r=find(idx[s]); reps.setdefault(r,[]).append(s)
    out=[]
    for r,l in reps.items():
        rep=min(x for x in l if x&1)            # contains the point 0
        out.append((tuple(i for i in range(N) if rep>>i&1),len(l)))
    return sorted(out)
@lru_cache(None)
def U(S):                                         # S: sorted tuple; upper bound on g(S), and which family won
    if len(S)==1: return (0,"unit")
    r=affdim(S); best=None
    # trie: split S by a linear functional d; every target is (piece on S0) +- (piece on S1): 2^r gates
    slices={}
    for d in range(1,N):
        S1=tuple(s for s in S if pc(s&d)&1); S0=tuple(s for s in S if not pc(s&d)&1)
        if not S1 or not S0: continue
        slices[d]=(S0,S1)
        c=(1<<r)+U(S0)[0]+U(S1)[0]
        if best is None or c<best[0]: best=(c,"trie")
    # walk: first target (m-1 gates), then every other target = earlier target - 2*(that target on the slice S1(d) or S0(d)), d in a basis
    cost=sorted((min(U(S0)[0],U(S1)[0]),d) for d,(S0,S1) in slices.items())
    K=[d for d in range(1,N) if d not in slices]   # directions that do not change the target (projectively)
    basis=[]
    def red(v):
        for b in basis: v=min(v,v^b)
        return v
    for k in K:
        v=red(k)
        if v: basis.append(v)
    tot=0; cnt=0
    for c,d in cost:
        v=red(d)
        if v: basis.append(v); tot+=c; cnt+=1
    assert cnt==r
    c=(len(S)-1)+((1<<r)-1)+tot
    if c<best[0]: best=(c,"walk")
    return best
def targets(S):
    return [[(-1)**(pc(s&x)&1) for s in S] for x in range(N)]
def minc(S,p,k,tmo):
    m=len(S); nn=m+(m&1)
    rows="\n".join(" ".join(map(str,t+[0]*(nn-m))) for t in targets(S))+"\n"
    try:
        o=subprocess.run([MINC,str(p),str(nn),str(k)],input=rows,capture_output=True,text=True,timeout=tmo).stdout
    except subprocess.TimeoutExpired:
        return None,""
    if "RESULT" not in o: return None,o
    return ("YES" in o.split("RESULT")[1].split("\n")[0]), o
if __name__=="__main__":
    ms=[int(a) for a in sys.argv[1].split(",")]; primes=[int(a) for a in sys.argv[2].split(",")]; tmo=float(sys.argv[3])
    print("count G throughout. f = 16 - m + 2^r + iota.  sub = subspace law 16+(d-1)2^d in count O where m = 2^d")
    for m in ms:
        for S,size in orbits(m):
            r=affdim(S); nT=(1<<r) if m>1 else 0
            lb=max(14+m, 16-m+nT); u,fam=U(S)
            line="m=%d S=%s orbit=%d r=%d | trivial lower bound f>=%d | constructions: g<=%d (%s) so f<=%d iota<=%d |"%(m,S,size,r,lb,u,fam,16-m+u,u-nT)
            for p in primes:
                res=None
                for k in range(0,u-nT+1):
                    t0=time.time(); ok,o=minc(S,p,k,tmo)
                    if ok is None: res="GF(%d): iota>=%d proved, k=%d timed out"%(p,k,k); break
                    if ok:
                        res="GF(%d): iota=%d EXACT, f=%d"%(p,k,16-m+nT+k)
                        open("circ_m%d_%s_p%d.txt"%(m,"-".join(map(str,S)),p),"w").write(o); break
                if res is None: res="GF(%d): no circuit up to k=%d ?!"%(p,u-nT)
                line+=" "+res+" |"
            print(line,flush=True)
