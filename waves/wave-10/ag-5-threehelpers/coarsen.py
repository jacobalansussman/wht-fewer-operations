# ag-5: search from the FINE side. Start from h partitions into single points (good for every degree, 3N classes) and merge two
# classes of one partition whenever the family stays good for degree d. Goodness test in floating point during the walk
# (distance of RM(d) from the column space), then an EXACT check (whole numbers) of the final family.
import sys, random, numpy as np
from tool import Rmat, carried, per_degree, hall_small
def good(M,Qr,tol=1e-7):
    u,s,vt=np.linalg.svd(M,full_matrices=False)
    r=int((s>1e-9*s[0]).sum()); Q=u[:,:r]
    P=Q.T@Qr
    return Qr.shape[1]-float((P*P).sum())<tol
def coarsen(k,d,h,rng,fails=4000,init=None):
    N=1<<k
    R=Rmat(k,d).astype(float); Qr,_=np.linalg.qr(R)
    if init is None: cls=[[[y] for y in range(N)] for _ in range(h)]
    else: cls=[[list(c) for c in P] for P in init]
    def build():
        cols=[]
        for P in cls:
            for c in P:
                v=np.zeros(N); v[c]=1; cols.append(v)
        return np.array(cols).T
    M=build(); assert good(M,Qr)
    f=0
    while f<fails:
        i=rng.randrange(h); P=cls[i]
        if len(P)<2: f+=1; continue
        a,b=rng.sample(range(len(P)),2)
        ca,cb=P[a],P[b]
        P2=[c for j,c in enumerate(P) if j not in (a,b)]+[ca+cb]
        cls[i]=P2; M2=build()
        if good(M2,Qr): M=M2; f=0
        else: cls[i]=P; f+=1
    return cls
if __name__=="__main__":
    k=int(sys.argv[1]); d=int(sys.argv[2]); h=int(sys.argv[3]); runs=int(sys.argv[4]); seed=int(sys.argv[5]); fails=int(sys.argv[6]) if len(sys.argv)>6 else 3000
    N=1<<k; best=None
    for r in range(runs):
        rng=random.Random(seed*1000+r)
        cls=coarsen(k,d,h,rng,fails)
        V=sum(len(P) for P in cls)
        labs=[]
        for P in cls:
            lab=[0]*N
            for j,c in enumerate(P):
                for y in c: lab[y]=j
            labs.append(lab)
        ex=carried(labs,k,d)
        print("k",k,"d",d,"h",h,"run",r,"classes",V,"of N",N,"sizes",[len(P) for P in cls],"exact (classes, rank, dimRM, missing):",ex,flush=True)
        if ex[3]==0 and (best is None or V<best[0]): best=(V,cls,labs)
    if best:
        V,cls,labs=best
        print("BEST k",k,"d",d,"h",h,"classes",V,"of N",N,"| class sizes per partition:",[sorted(len(c) for c in P) for P in cls])
        print("  exact, degree d+1:",carried(labs,k,d+1),"| smallest set of outputs touching fewer classes (cap 6):",hall_small(labs,6))
        print("  CLS=",cls)
