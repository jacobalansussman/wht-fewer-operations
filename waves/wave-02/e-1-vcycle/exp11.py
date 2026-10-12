# Question B at 16 points: an invertible K whose rows are coset atoms (any subgroups, any mix, not necessarily perpendicular),
# minimising cost(K) + cost(K S)   (count G, greedy).   Tree accounting predicts N log2 N = 64 for every basis from one tree.
# Baseline: K = identity gives 0 + greedy cost of S itself.
import sys, random, time; sys.path.insert(0,'waves/wave-02/e-1-vcycle')
from lib import *
random.seed(int(sys.argv[1])); budget=float(sys.argv[2]); t0=time.time()
k=4; N=16; S=sympS(k)
At=[f for D,a,b,f in atoms(k,(1,2,4,8,16))]; n=len(At)
SA=[canon(mv(S,f)) for f in At]
size=[nnz(f) for f in At]
ident=[i for i in range(n) if size[i]==1]
def cost(cur): return cse_cost([At[i] for i in cur])+cse_cost([SA[i] for i in cur])
base=cost(ident); print('atoms',n,'| K = identity: 0 +',base,'(greedy cost of S itself)',flush=True)
best=(base,list(ident)); hist={}
starts=0
while time.time()-t0<budget:
    if starts==0: cur=list(ident)
    else:
        cur=[]; rows=[]
        for i in random.sample(range(n),n):
            if rank_exact(rows+[At[i]])==len(rows)+1: cur.append(i); rows.append(At[i])
            if len(cur)==N: break
    starts+=1
    c=cost(cur); hist[c]=hist.get(c,0)+1 if starts>1 else hist.get(c,0)
    moved=True
    while moved and time.time()-t0<budget:
        moved=False
        for pos in random.sample(range(N),N):
            for cand in random.sample(range(n),40):
                if cand in cur: continue
                new=cur[:pos]+[cand]+cur[pos+1:]
                cn=cost(new)
                if cn<c and rank_exact([At[i] for i in new])==N: cur,c=new,cn; moved=True
            if time.time()-t0>budget: break
    if c<best[0] or starts==1:
        best=(c,list(cur)) if c<=best[0] else best
        sc={}
        for i in cur: sc[size[i]]=sc.get(size[i],0)+1
        print('  local optimum',c,'= ',cse_cost([At[i] for i in cur]),'+',cse_cost([SA[i] for i in cur]),'| atom sizes',dict(sorted(sc.items())),' t=%.0fs'%(time.time()-t0),flush=True)
print('random bases of atoms: histogram of cost(K)+cost(K S):',dict(sorted(hist.items())))
c,cur=best; print('best:',c,'against 64 (tree accounting), 56 (best known program for S)')
for i in cur: print('   ',At[i])
