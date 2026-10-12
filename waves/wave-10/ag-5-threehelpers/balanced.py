# ag-5: the dual route. h partitions are good for degree d  iff  K := {g : g sums to zero on every class of every partition}
# lies in H_d := span of the characters chi_S with |S| > d.  So: CHOOSE K inside H_d first, then look for partitions into
# K-BALANCED classes (every g in K sums to zero on the class) and ask only that the rank of the incidence matrix be N - dim K.
# Exact: whole numbers only (fraction-free elimination). Pure Python.
import sys, random, itertools
def pc(x): return bin(x).count("1")
def chi(S,y): return -1 if pc(S&y)&1 else 1
def exact_rank(A):
    M=[list(map(int,r)) for r in A]; n=len(M); m=len(M[0]); rk=0; prev=1
    for c in range(m):
        piv=None
        for r in range(rk,n):
            if M[r][c]!=0: piv=r;break
        if piv is None: continue
        M[rk],M[piv]=M[piv],M[rk]; p=M[rk][c]; Mk=M[rk]
        for r in range(rk+1,n):
            f=M[r][c]; Mr=M[r]
            M[r]=[(p*a-f*b)//prev for a,b in zip(Mr,Mk)]
        prev=p; rk+=1
        if rk==n: break
    return rk
def incid(parts,N):
    cols=[]
    for P in parts:
        for C in P:
            v=[0]*N
            for y in C: v[y]=1
            cols.append(v)
    return [list(r) for r in zip(*cols)]
def missing(parts,k,d):
    N=1<<k; M=incid(parts,N); r0=exact_rank(M)
    R=[[1 if (y&S)==S else 0 for S in range(N) if pc(S)<=d] for y in range(N)]
    r1=exact_rank([a+b for a,b in zip(M,R)])
    return r0, r1-r0
def setup(k,U):
    N=1<<k
    gam=[tuple(chi(S,y) for S in U) for y in range(N)]
    neg={}
    for y in range(N): neg.setdefault(gam[y],[]).append(y)
    partner=[neg.get(tuple(-a for a in gam[y]),[]) for y in range(N)]
    # irreducible balanced 4-sets: zero sum, no balanced pair inside
    ps={}
    for a in range(N):
        for b in range(a+1,N):
            s=tuple(x+z for x,z in zip(gam[a],gam[b]))
            if any(s): ps.setdefault(s,[]).append((a,b))
    fours=set()
    for s,L in ps.items():
        t=tuple(-x for x in s)
        if t in ps and s<t:
            for (a,b) in L:
                for (c,e) in ps[t]:
                    if len({a,b,c,e})==4: fours.add(tuple(sorted((a,b,c,e))))
    return gam,partner,sorted(fours)
def match(rest,partner,rng):
    # perfect matching of `rest` by balanced pairs (augmenting paths), random order
    rest=set(rest); mate={}
    adj={y:[z for z in partner[y] if z in rest] for y in rest}
    for y in adj: rng.shuffle(adj[y])
    def aug(u,seen):
        for v in adj[u]:
            if v in seen: continue
            seen.add(v)
            if v not in mate or aug(mate[v],seen):
                mate[v]=u; mate[u]=v; return True
        return False
    order=list(rest); rng.shuffle(order)
    for u in order:
        if u not in mate:
            if not aug(u,{u}): return None
    return [tuple(sorted((u,v))) for u,v in mate.items() if u<v]
def rand_partition(N,n4,fours,partner,rng,tries=200):
    for _ in range(tries):
        used=set(); cl=[]
        idx=list(range(len(fours))); rng.shuffle(idx)
        for i in idx:
            F=fours[i]
            if used.isdisjoint(F):
                cl.append(F); used.update(F)
                if len(cl)==n4: break
        if len(cl)<n4: continue
        m=match([y for y in range(N) if y not in used],partner,rng)
        if m is None: continue
        return cl+m
    return None
if __name__=="__main__":
    k=int(sys.argv[1]); d=int(sys.argv[2]); name=sys.argv[3]; n4s=[int(v) for v in sys.argv[4].split(",")]; tries=int(sys.argv[5]); seed=int(sys.argv[6])
    N=1<<k; full=N-1
    if name.startswith("top"):      # K = parity times span{1, x_1..x_r}: U = {all, all minus i for i<r}
        r=int(name[3:]); U=[full]+[full&~(1<<i) for i in range(r)]
    elif name.startswith("sup"):    # K = span of chi_S for S containing the first c bits and |S| > d
        c=int(name[3:]); base=(1<<c)-1; U=[S for S in range(N) if (S&base)==base and pc(S)>d]
    elif name.startswith("set"):    # explicit list of masks
        U=[int(v,2) for v in name[3:].split("+")]
    assert all(pc(S)>d for S in U)
    rng=random.Random(seed)
    gam,partner,fours=setup(k,U)
    npairs=sum(len(p) for p in partner)//2
    print("k",k,"d",d,"K =",name,"dim K",len(U),"| balanced pairs",npairs,"irreducible balanced 4-sets",len(fours),"| target rank N - dim K =",N-len(U),flush=True)
    best=None
    for t in range(tries):
        parts=[rand_partition(N,n4,fours,partner,rng) for n4 in n4s]
        if any(P is None for P in parts): print("  no partition with",n4s,"fours"); break
        V=sum(len(P) for P in parts); r=exact_rank(incid(parts,N))
        if best is None or r>best[0]: best=(r,V,parts)
        if r==N-len(U): break
    if best:
        r,V,parts=best
        print("  tries",t+1,"best rank",r,"classes",V,"sizes",[len(P) for P in parts],"| good iff rank = ",N-len(U))
        if r==N-len(U):
            for dd in (d,d+1):
                r0,miss=missing(parts,k,dd); print("  EXACT CHECK degree",dd,": rank M",r0,"missing dimensions",miss, "(0 = every polynomial of degree <= %d is a sum of %d class functions)"%(dd,len(parts)))
            print("  PARTS=",parts)
