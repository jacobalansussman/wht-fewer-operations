# v-0: the true game of the class at 4 points, exhaustive, gates found by brute force (no taxonomy of moves).
# wire = integer vector over 4 inputs, up to scaling; allowed iff entries in {0,+c,-c} and support is a node of the tree.
# gate = a*u + b*v ; the ratio b/a need only range over +-1, +-2, +-1/2 (any other ratio gives entries of two sizes or a multiple of u or v).
from itertools import combinations, product
N=4; nodes=[(0,),(1,),(2,),(3,),(0,1),(2,3),(0,1,2,3)]
def norm(w):
    nz=[x for x in w if x]
    if not nz: return None
    c=abs(nz[0])
    if any(abs(x)!=c for x in nz): return None
    if tuple(i for i,x in enumerate(w) if x) not in nodes: return None
    s=1 if nz[0]>0 else -1
    return tuple(s*x//c for x in w)
leaves=[tuple(1 if i==j else 0 for i in range(N)) for j in range(N)]
allw=set()
for nd in nodes:
    if len(nd)==1: continue
    for sg in product([1,-1],repeat=len(nd)-1):
        w=[0]*N; w[nd[0]]=1
        for i,s in zip(nd[1:],sg): w[i]=s
        allw.add(tuple(w))
allw=sorted(allw)
rows=[norm(tuple((-1)**bin(x&y).count('1') for x in range(N))) for y in range(N)]
coef=[(1,1),(1,-1),(1,2),(1,-2),(2,1),(2,-1)]
def gates(u,v):
    out=set()
    for a,b in coef:
        r=norm(tuple(a*p+b*q for p,q in zip(u,v)))
        if r: out.add(r)
    return out
G={}
pool=leaves+allw
for u in pool:
    for v in pool:
        G[(u,v)]=gates(u,v)
def derivable(S):
    held=set(leaves); S=set(S); ch=True
    while ch:
        ch=False
        for w in list(S-held):
            if any(w in G[(u,v)] for u in held for v in held): held.add(w); ch=True
    return S<=held
print("possible wires above the leaves:",len(allw))
others=[w for w in allw if w not in rows]
for extra in range(0,len(others)+1):
    sols=[c for c in combinations(others,extra) if derivable(list(c)+rows)]
    print("gates =",extra+N,": sets that are legal plays holding all 4 rows:",len(sols))
    if sols: break
