# lemma_ad6.py kmax : the private-wire lemma (ag-7.md section 4) tested on ad-6's circuit for degree 2 (selector and
# atoms), read modulo 2.  That circuit shares its helpers heavily (most outputs are helper + helper), so the graph H+
# is far from a star.  Claim to test: no gate adds two outputs, no wire labels two outputs, no cycle shorter than
# delta - 2 = 6 in H+ (vertices: wires that are not outputs, and z; one edge per output).
import sys
from itertools import combinations
sys.path.insert(0, __file__.rsplit('/', 1)[0] + '/../ad-6-twohelpers')
import circuit2
class F:
    __slots__=('m',)
    def __init__(s,m): s.m=m
gates=[]
def add(u,v,s=1):
    if v is None: return u
    if u is None: return v
    r=F(u.m^v.m); gates.append((u.m,v.m,r.m)); return r
circuit2.add=add
def girth(edges):
    adj={}
    for a,b in edges: adj.setdefault(a,[]).append(b); adj.setdefault(b,[]).append(a)
    best=10**9
    for s in adj:
        dist={s:0}; par={s:None}; q=[s]
        for x in q:
            if 2*dist[x]>=best: break
            for y in adj[x]:
                if y not in dist: dist[y]=dist[x]+1; par[y]=x; q.append(y)
                elif par[x]!=y: best=min(best,dist[x]+dist[y]+1)
    return best
for k in range(3,int(sys.argv[1])+1):
    gates.clear()
    pairs=list(combinations(range(k),2))
    c=F(1); lin={p:F(1<<(1+p)) for p in range(k)}; quad={pq:F(1<<(1+k+i)) for i,pq in enumerate(pairs)}
    out=circuit2.eval2(c,lin,quad,list(range(k)))
    N=1<<k; D=1+k+len(pairs)
    # the outputs are right modulo 2
    for x in range(N):
        S=[i for i in range(k) if x>>i&1]
        want=1
        for p in S: want^=1<<(1+p)
        for i,pq in enumerate(pairs):
            if pq[0] in S and pq[1] in S: want^=1<<(1+k+i)
        assert out[x].m==want
    Out=set(o.m for o in out.values()); inputs=set(1<<i for i in range(D))
    first={}
    for u,v,r in gates:
        if u==0 or v==0 or r==0: continue
        if r in inputs or r in first: continue
        first[r]=(u,v)
    wires=inputs|set(first)
    W=wires-Out
    typec=0; labels=[]; edges=[]
    for o in Out:
        if o in inputs: continue
        u,v=first[o]; iu=u in Out; iv=v in Out
        if iu and iv: typec+=1
        elif iu or iv: lab=v if iu else u; labels.append(lab); edges.append(('z',lab))
        else: edges.append((u,v))
    rep=len(labels)-len(set(labels)); repe=len(edges)-len(set(map(frozenset,edges)))
    g=girth(edges); g0=girth([e for e in edges if e[0]!='z'])
    print(f"k={k} N={N}: gates modulo 2 = {len(first)}, wires that are not outputs V = {len(W)} ({len(W)/N:.3f} N), outputs by kind a / b / c = {len(labels)} / {len(edges)-len(labels)} / {typec}, repeated labels {rep}, repeated edges {repe}, shortest cycle of H+ = {'none' if g>=10**9 else g}, shortest cycle that avoids z = {'none' if g0>=10**9 else g0}",flush=True)
