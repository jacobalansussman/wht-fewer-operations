# ag-5: kernel-first search, second generator: exact cover by balanced pairs and irreducible balanced 4-sets (random DFS).
# usage: balanced2.py k d Kname n4a,n4b,n4c tries seed      (classes of partition i = n4_i fours + (N - 4 n4_i)/2 pairs)
import sys, random
sys.setrecursionlimit(10000)
from balanced import pc, chi, exact_rank, incid, missing, setup
def cover(N,n4,fours_at,partner,rng,budget=20000):
    n2=(N-4*n4)//2; cl=[]; used=[False]*N; nodes=[0]
    def rec(n4l,n2l):
        nodes[0]+=1
        if nodes[0]>budget: return False
        y=0
        while y<N and used[y]: y+=1
        if y==N: return True
        opts=[]
        if n2l>0: opts+=[(y,z) for z in partner[y] if not used[z]]
        if n4l>0:
            F=[f for f in fours_at[y] if not (used[f[0]] or used[f[1]] or used[f[2]] or used[f[3]])]
            rng.shuffle(F); opts+=F[:6]
        rng.shuffle(opts)
        for c in opts:
            for z in c: used[z]=True
            cl.append(c)
            if rec(n4l-(len(c)==4),n2l-(len(c)==2)): return True
            cl.pop()
            for z in c: used[z]=False
        return False
    for _ in range(30):
        nodes[0]=0; cl.clear()
        for i in range(N): used[i]=False
        if rec(n4,n2): return list(cl)
    return None
if __name__=="__main__":
    k=int(sys.argv[1]); d=int(sys.argv[2]); name=sys.argv[3]; n4s=[int(v) for v in sys.argv[4].split(",")]; tries=int(sys.argv[5]); seed=int(sys.argv[6])
    N=1<<k; full=N-1
    if name.startswith("top"): r=int(name[3:]); U=[full]+[full&~(1<<i) for i in range(r)]
    elif name.startswith("sup"): c=int(name[3:]); base=(1<<c)-1; U=[S for S in range(N) if (S&base)==base and pc(S)>d]
    elif name.startswith("set"): U=[int(v,2) for v in name[3:].split("+")]
    assert all(pc(S)>d for S in U)
    rng=random.Random(seed)
    gam,partner,fours=setup(k,U)
    fours_at=[[] for _ in range(N)]
    for f in fours:
        for y in f: fours_at[y].append(f)
    print("k",k,"d",d,"K =",name,"dim K",len(U),"| balanced pairs",sum(len(p) for p in partner)//2,"irreducible balanced 4-sets",len(fours),"| target rank N - dim K =",N-len(U),"| classes wanted",[n4+(N-4*n4)//2 for n4 in n4s],flush=True)
    best=None
    for t in range(tries):
        parts=[cover(N,n4,fours_at,partner,rng) for n4 in n4s]
        if any(P is None for P in parts): print("  no exact cover found with",n4s,"fours (random DFS, not exhaustive)"); break
        V=sum(len(P) for P in parts); r=exact_rank(incid(parts,N))
        if best is None or r>best[0]: best=(r,V,parts)
        if r==N-len(U): break
    if best:
        r,V,parts=best
        print("  tries",t+1,"best rank",r,"classes",V,"of N =",N,"sizes",[len(P) for P in parts],"| good iff rank =",N-len(U))
        if r==N-len(U):
            for dd in (d,d+1):
                r0,miss=missing(parts,k,dd); print("  EXACT CHECK degree",dd,": rank M",r0,"missing dimensions",miss)
            print("  PARTS=",parts)
