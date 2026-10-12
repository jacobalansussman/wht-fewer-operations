# ag-1: least total weight of a FLAT circuit for the 4-point transform, halvings allowed and free.   Count (G), exact.
# Wires: the 40 vectors with entries 0, +-1 up to sign.  Gate w = (a*u + b*v)/c: weight 1000 (u +- v), 1585 (u +- 2v), 0 (halving).
# Question: is there a flat circuit with total weight below 8 (in units of 1000)?  The determinant needs 4; the textbook spends 8.
import itertools, sys
from math import gcd
n=4
def norm(v):
    for t in v:
        if t: return tuple(v) if t>0 else tuple(-q for q in v)
    return None
V=sorted({norm(v) for v in itertools.product((-1,0,1),repeat=n)}-{None}); idx={v:i for i,v in enumerate(V)}
der=[[] for _ in V]     # der[w] = list of (mask of the two operands, weight)
for i,u in enumerate(V):
    for j in range(i):
        v=V[j]
        for a,b in itertools.product(range(-3,4),repeat=2):
            if a==0 or b==0 or gcd(a,b)!=1: continue
            w=[a*p+b*q for p,q in zip(u,v)]; c=0
            for t in w: c=gcd(c,abs(t))
            if c==0: continue
            wp=norm([t//c for t in w])
            if wp in idx and wp!=u and wp!=v:
                f=(abs(a)+abs(b),c); wt={(2,1):1000,(3,1):1585,(2,2):0}[f]
                der[idx[wp]].append(((1<<i)|(1<<j),wt))
inputs=0
for i in range(n): inputs|=1<<idx[norm([1 if k==i else 0 for k in range(n)])]
outs=[idx[norm([(-1)**bin(j&i).count('1') for i in range(n)])] for j in range(n)]
omask=0
for o in outs: omask|=1<<o
def close(S):
    ch=True
    while ch:
        ch=False
        for w in range(len(V)):
            if not S>>w&1 and any(wt==0 and (S&m)==m for m,wt in der[w]): S|=1<<w; ch=True
    return S
LIMIT=int(sys.argv[1]) if len(sys.argv)>1 else 7999
best=[10**9,None]; seen={}; nodes=0
def dfs(S,wt,path):
    global nodes
    S=close(S)
    if (S&omask)==omask:
        if wt<best[0]: best[0]=wt; best[1]=list(path)
        return
    missing=bin(omask&~S).count('1')
    if wt+1000*missing>LIMIT: return
    if seen.get(S,10**9)<=wt: return
    seen[S]=wt; nodes+=1
    for w in range(len(V)):
        if S>>w&1: continue
        c=min((x for m,x in der[w] if x>0 and (S&m)==m),default=None)
        if c is None: continue
        path.append((V[w],c)); dfs(S|(1<<w),wt+c,path); path.pop()
dfs(inputs,0,[])
print("flat circuits for the 4-point transform, halvings free: search limit %d; states visited %d"%(LIMIT,nodes))
print("least weight found within the limit:",best[0] if best[1] else "NONE within the limit", best[1] if best[1] else "")
