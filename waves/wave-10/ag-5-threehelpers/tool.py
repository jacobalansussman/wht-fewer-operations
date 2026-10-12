# ag-5 three-helpers: exact goodness test and an annealer. Gate count (G) is not used here: the objects are partitions.
# good(labs, k, d): labs = list of h label arrays (length N = 2^k). Exact (whole numbers, fraction-free elimination).
#   h partitions are GOOD FOR DEGREE d  iff  every monomial of degree <= d lies in the column space of the incidence matrix M
#   iff every g with zero sum on every class of every partition has zero moments up to degree d  (leftker M inside RM(d)-perp).
import sys, random, itertools, math
import numpy as np
def pc(x): return bin(x).count("1")
def monos(k,d): return [S for S in range(1<<k) if pc(S)<=d]
def Rmat(k,d):
    N=1<<k
    return np.array([[1 if (y&S)==S else 0 for S in monos(k,d)] for y in range(N)],dtype=np.int64)
def incid(labs):
    N=len(labs[0]); cols=[]
    for lab in labs:
        vals=sorted(set(lab)); ix={v:i for i,v in enumerate(vals)}
        M=np.zeros((N,len(vals)),dtype=np.int64)
        for y in range(N): M[y,ix[lab[y]]]=1
        cols.append(M)
    return np.concatenate(cols,axis=1)
def exact_rank(A):
    # fraction-free (Bareiss) elimination on Python ints: exact rank over the rationals
    M=[[int(v) for v in row] for row in A]; n=len(M); m=len(M[0]) if n else 0
    rk=0; prev=1
    for c in range(m):
        piv=None
        for r in range(rk,n):
            if M[r][c]!=0: piv=r;break
        if piv is None: continue
        M[rk],M[piv]=M[piv],M[rk]
        p=M[rk][c]
        for r in range(rk+1,n):
            f=M[r][c]
            if f!=0 or True:
                Mr=M[r]; Mk=M[rk]
                M[r]=[(p*a-f*b)//prev for a,b in zip(Mr,Mk)]
        prev=p; rk+=1
        if rk==n: break
    return rk
def carried(labs,k,d):
    # exact: (classes, rank M, dim RM(d), missing dimensions = rank[M R]-rank M)
    M=incid(labs); R=Rmat(k,d)
    r0=exact_rank(M.tolist()); r1=exact_rank(np.concatenate([M,R],axis=1).tolist())
    return M.shape[1], r0, R.shape[1], r1-r0
def per_degree(labs,k,dmax):
    # exact: for each degree j, how many monomials of degree exactly j are NOT in col(M)
    M=incid(labs); r0=exact_rank(M.tolist()); N=1<<k; out={}
    for j in range(dmax+1):
        miss=0; tot=0
        for S in range(N):
            if pc(S)==j:
                tot+=1
                col=np.array([[1 if (y&S)==S else 0] for y in range(N)],dtype=np.int64)
                if exact_rank(np.concatenate([M,col],axis=1).tolist())!=r0: miss+=1
        out[j]=(miss,tot)
    return out
def soft(Mf,Qr):
    # float: sum of sin^2 of the principal angles between RM(d) and col(M); 0 iff good (then checked exactly)
    u,s,vt=np.linalg.svd(Mf,full_matrices=False)
    r=int((s>1e-9*s[0]).sum()); Q=u[:,:r]
    P=Q.T@Qr
    return Qr.shape[1]-float((P*P).sum()), r
def hall_small(labs,cap):
    # the necessary condition of ae-cross, stated as a program, exact up to sets of `cap` outputs:
    # smallest set S of outputs that touches fewer than |S| classes. Returns the size, or None if none of size <= cap.
    N=len(labs[0]); h=len(labs)
    rows=[tuple((i,labs[i][y]) for i in range(h)) for y in range(N)]
    # a minimal violator is connected (shares classes); grow connected sets by DFS with canonical smallest element
    nb={}
    for y in range(N):
        for c in rows[y]: nb.setdefault(c,[]).append(y)
    best=[None]
    def rec(S,cls,frontier_min,size_cap):
        if len(cls)<len(S): return True
        if len(S)>=size_cap: return False
        cand=set()
        for c in cls:
            for y in nb[c]:
                if y>frontier_min and y not in S: cand.add(y)
        for y in sorted(cand):
            S.add(y); new=[c for c in rows[y] if c not in cls]
            for c in new: cls.add(c)
            # prune: each added output may add at most h classes; need |cls| < |S| eventually: |cls|-|S| can drop by at most 1 per step
            if len(cls)-len(S) < (size_cap-len(S))+1:
                if rec(S,cls,frontier_min,size_cap): return True
            S.discard(y)
            for c in new: cls.discard(c)
        return False
    for size in range(2,cap+1):
        for y0 in range(N):
            if rec({y0},set(rows[y0]),y0,size): return size
    return None
def anneal(k,d,Vs,steps,seed,T0=0.6,T1=0.02,init=None,log=None):
    rng=random.Random(seed); N=1<<k; h=len(Vs)
    R=Rmat(k,d).astype(float); Qr,_=np.linalg.qr(R)
    if init is None:
        labs=[]
        for V in Vs:
            l=[i%V for i in range(N)]; rng.shuffle(l); labs.append(l)
    else: labs=[list(l) for l in init]
    off=[0]
    for V in Vs: off.append(off[-1]+V)
    M=np.zeros((N,off[-1]))
    cnt=[[0]*V for V in Vs]
    for i in range(h):
        for y in range(N): M[y,off[i]+labs[i][y]]=1; cnt[i][labs[i][y]]+=1
    E,r=soft(M,Qr); best=E; bestlabs=[list(l) for l in labs]
    for st in range(steps):
        T=T0*(T1/T0)**(st/max(1,steps-1))
        i=rng.randrange(h); y=rng.randrange(N); c=labs[i][y]
        if rng.random()<0.5:
            c2=rng.randrange(Vs[i])
            if c2==c or cnt[i][c]==1: continue
            M[y,off[i]+c]=0; M[y,off[i]+c2]=1
            E2,r2=soft(M,Qr)
            if E2<=E or rng.random()<math.exp((E-E2)/T):
                labs[i][y]=c2; cnt[i][c]-=1; cnt[i][c2]+=1; E=E2
            else:
                M[y,off[i]+c]=1; M[y,off[i]+c2]=0
        else:
            y2=rng.randrange(N); c2=labs[i][y2]
            if c2==c: continue
            M[y,off[i]+c]=0; M[y,off[i]+c2]=1; M[y2,off[i]+c2]=0; M[y2,off[i]+c]=1
            E2,r2=soft(M,Qr)
            if E2<=E or rng.random()<math.exp((E-E2)/T):
                labs[i][y]=c2; labs[i][y2]=c; E=E2
            else:
                M[y,off[i]+c]=1; M[y,off[i]+c2]=0; M[y2,off[i]+c2]=1; M[y2,off[i]+c]=0
        if E<best-1e-9:
            best=E; bestlabs=[list(l) for l in labs]
            if best<1e-7: break
        if log and st%log==0: print("  step",st,"T %.3f"%T,"E %.4f"%E,"best %.4f"%best,flush=True)
    return best,bestlabs
if __name__=="__main__":
    mode=sys.argv[1]
    if mode=="check":
        # controls on cases with known answers
        # (1) ad-6 family, k=5, t=1: P1 forgets a (bit 0); P2: a=0 forgets atom0 = bits {1,2}, a=1 forgets atom1 = bits {3,4}
        k=5; N=32
        P1=[y>>1 for y in range(N)]
        P2=[(y&1, (y>>3) if (y&1)==0 else ((y>>1)&3)) for y in range(N)]
        print("ad-6 family k=5 t=1, degree 2:",carried([P1,P2],k,2),"degree 3:",carried([P1,P2],k,3), "expected 24 classes, missing 0 at degree 2, >0 at degree 3")
        # (2) ae-cross h4_three partitions
        for k in (5,6):
            N=1<<k
            Q1=[('y',x>>1) for x in range(N)]
            Q2=[('a',x&1,x>>2) for x in range(N)]
            Q3=[('b',x&1,x>>1&1,((x>>2)>>1) if (x>>1&1) else ((x>>2)&1)) for x in range(N)]
            print("ae-cross three partitions k=%d:"%k,"deg3",carried([Q1,Q2,Q3],k,3),"deg4",carried([Q1,Q2,Q3],k,4),"expected classes 44/84, missing 0 at degree 3, >0 at 4")
            print("   hall_small cap 6:",hall_small([Q1,Q2,Q3],6))
        # (3) three fixed forgotten bits: degree 2 exactly
        k=5; N=32
        F=[[y & ~(1<<i) for y in range(N)] for i in range(3)]
        print("forget bit 0 / bit 1 / bit 2, k=5:",[carried(F,k,d) for d in (2,3)],"expected missing 0 then 4")
    if mode=="anneal":
        k=int(sys.argv[2]); d=int(sys.argv[3]); Vs=[int(v) for v in sys.argv[4].split(",")]; steps=int(sys.argv[5]); seeds=[int(s) for s in sys.argv[6].split(",")]
        for sd in seeds:
            best,labs=anneal(k,d,Vs,steps,sd,log=max(1,steps//10))
            ex=carried(labs,k,d)
            print("RESULT k",k,"d",d,"Vs",Vs,"seed",sd,"soft best %.5f"%best,"exact (classes, rank, dimRM, missing):",ex,flush=True)
            if ex[3]==0:
                print("GOOD labs=",labs); print("  per degree missing:",per_degree(labs,k,d+1)); print("  hall_small cap 6:",hall_small(labs,6))
            else:
                print("  best labs=",labs)
