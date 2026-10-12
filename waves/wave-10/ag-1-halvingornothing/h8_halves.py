# ag-1: the 19-gate circuit for the 8-point transform (g-1, count (G)), exact whole numbers.
# (1) which pairs of its wires agree modulo 2, and what their halves (u - s*v)/2^e are (s = +-1, +-3);
# (2) exchange search with a FORCED halving: add one half h that is not a wire, remove any two (or any one) of the 11 helpers;
#     is the transform still computed (every wire kept must lie on a line through two wires derived before it)?
#     18 gates = 19 + 1 - 2.  Exact rational collinearity.
import itertools, sys
from fractions import Fraction
from math import gcd
N=8
def e(i): v=[0]*N; v[i]=1; return v
def lc(a,u,b,v): return [a*x+b*y for x,y in zip(u,v)]
x=[e(i) for i in range(N)]
g={}
g[1]=lc(1,x[0],1,x[7]); g[2]=lc(1,x[1],1,x[6]); g[3]=lc(1,x[2],-1,x[5]); g[4]=lc(1,x[3],-1,x[4])
g[5]=lc(1,g[1],-1,g[2]); g[6]=lc(1,g[3],1,g[4]); g[7]=lc(1,g[5],-1,g[6])
g[8]=lc(1,g[7],-2,x[7]); g[9]=lc(1,g[7],-2,x[5]); g[10]=lc(1,g[8],2,x[6]); g[11]=lc(1,g[9],-2,x[4])
y={}
y[7]=lc(1,g[10],2,g[4]); y[3]=lc(1,g[9],2,x[3]); y[5]=lc(-1,y[3],2,g[5]); y[1]=lc(1,g[10],2,g[3])
y[6]=lc(1,g[11],2,g[2]); y[2]=lc(1,g[8],2,x[1]); y[4]=lc(1,y[2],2,g[6]); y[0]=lc(-1,g[11],2,g[1])
for j in range(N): assert y[j]==[(-1)**bin(j&i).count('1') for i in range(N)], j
def norm(v):
    c=0
    for t in v: c=gcd(c,abs(t))
    if c==0: return None
    v=[t//c for t in v]
    for t in v:
        if t: 
            if t<0: v=[-q for q in v]
            break
    return tuple(v)
inputs=[norm(v) for v in x]; helpers=[norm(g[i]) for i in range(1,12)]; outs=[norm(y[j]) for j in range(N)]
wires=inputs+helpers+outs; names=['x%d'%i for i in range(N)]+['g%d'%i for i in range(1,12)]+['y%d'%j for j in range(N)]
assert len(set(wires))==27
def res(v): return tuple(t&1 for t in v)
def collinear(a,b,c):
    for i in range(N):
        for j in range(i+1,N):
            d=a[i]*b[j]-a[j]*b[i]
            if d:
                al=Fraction(c[i]*b[j]-c[j]*b[i],d); be=Fraction(a[i]*c[j]-a[j]*c[i],d)
                return all(al*a[t]+be*b[t]==c[t] for t in range(N))
    return False
classes={}
for w,nm in zip(wires,names): classes.setdefault(res(w),[]).append(nm)
print("classes of wires with the same residue modulo 2 (size > 1):")
for r,l in classes.items():
    if len(l)>1: print("  ",''.join(map(str,r)),l)
idx={w:i for i,w in enumerate(wires)}
halves={}; npairs=0; old=0; onegate=0
for a in range(27):
    for b in range(a):
        if res(wires[a])!=res(wires[b]): continue
        npairs+=1
        for s in (1,-1,3,-3):
            d=[p-s*q for p,q in zip(wires[a],wires[b])]; h=norm(d)
            if h is None: continue
            c=0
            for t in d: c=gcd(c,abs(t))
            if c%2: continue
            if h in idx: old+=1; continue
            halves.setdefault(h,[]).append((names[a],names[b],s,c))
print("pairs of wires that agree modulo 2:",npairs,"; halves that are already wires (with repeats):",old,"; distinct new halves:",len(halves))
# how many of the new halves are one ordinary gate away from the 27 wires
cheap=0
for h in halves:
    ok=any(collinear(wires[a],wires[b],h) and res(wires[a])!=res(wires[b]) for a in range(27) for b in range(a))
    cheap+=ok
print("new halves that are also one ordinary gate (two wires with different residues) from the circuit's wires:",cheap,"of",len(halves))

# fast closure: precomputed collinear triples among the 27 wires, and for each half h the pairs (a, b) with h on their line
tri27=[[] for _ in range(27)]
for a in range(27):
    for b in range(a):
        for c in range(b):
            if collinear(wires[a],wires[b],wires[c]): tri27[a].append((b,c)); tri27[b].append((a,c)); tri27[c].append((a,b))
def works_idx(keep, hpairs, huses):
    """keep: set of indices (of the 27) kept; index 27 = the half h, with hpairs = pairs deriving it and huses[w] = wires a such that (a, h) derive w"""
    der=set(range(N)); todo=[i for i in keep if i>=N]+([27] if hpairs is not None else []); ch=True
    while ch and todo:
        ch=False; rest=[]
        for w in todo:
            if w==27: ok=any(a in der and b in der for a,b in hpairs)
            else:
                ok=any(a in der and b in der for a,b in tri27[w])
                if not ok and 27 in der: ok=any(a in der for a in huses.get(w,()))
            if ok: der.add(w); ch=True
            else: rest.append(w)
        todo=rest
    return all(i in der for i in range(19,27)), len(der)-N
H=list(range(8,19)); O=list(range(19,27)); allk=set(range(27))
print("control: the 19-gate circuit replays:",works_idx(allk,None,None))
print("control: remove any one helper, add nothing:",sum(works_idx(allk-{r},None,None)[0] for r in H),"of 11 still compute the transform")
print("control: remove any two helpers, add nothing:",sum(works_idx(allk-{r1,r2},None,None)[0] for r1,r2 in itertools.combinations(H,2)),"of 55")
found=0; tested=0; best1=0; usedh=0
for h,why in halves.items():
    hp=[(a,b) for a in range(27) for b in range(a) if collinear(wires[a],wires[b],h)]
    hu={}
    for a,b in hp: hu.setdefault(a,[]).append(b); hu.setdefault(b,[]).append(a)
    for r in H:
        ok,nd=works_idx(allk-{r},hp,hu)
        if ok and nd==19: best1+=1
    for r1,r2 in itertools.combinations(H,2):
        ok,nd=works_idx(allk-{r1,r2},hp,hu); tested+=1
        if ok: found+=1; print("18 GATES OR FEWER (%d):"%nd,h,why,"removed",names[r1],names[r2])
print("exchange with a forced half: %d states (add one of %d new halves, remove two helpers): %d circuits with 18 gates"%(tested,len(halves),found))
print("add one new half, remove ONE helper: %d of %d states compute the transform in 19 gates with the half derived"%(best1,len(halves)*11))
