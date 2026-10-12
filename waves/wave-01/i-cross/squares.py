# i-cross hybrid 3: symmetric and antisymmetric squares of the q-point transform, in "sum-and-difference of addresses" coordinates.
# 16 points = 4 x 4 array F, transform = H F H (H the Sylvester 4-point matrix). Swap of the two digits = transpose of F.
# Exact integer arithmetic. Builds the 10 x 10 and 6 x 6 middles, replays explicit circuits gate by gate, writes rows for mincirc.
import itertools, sys
q=4
H=[[(-1)**bin(x&y).count("1") for y in range(q)] for x in range(q)]
def mm(A,B): return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def tr(F): return mm(mm(H,F),H)
pairs=[(i,j) for i in range(q) for j in range(i+1,q)]
symc=[(i,i) for i in range(q)]+pairs
def unit(i,j,s):
    F=[[0]*q for _ in range(q)]; F[i][j]+=1
    if i!=j: F[j][i]+=s
    return F
S2=[[0]*len(symc) for _ in symc]; A2=[[0]*len(pairs) for _ in pairs]
for c,(i,j) in enumerate(symc):
    G=tr(unit(i,j,1))
    assert all(G[a][b]==G[b][a] for a in range(q) for b in range(q))
    for r,(a,b) in enumerate(symc): S2[r][c]=G[a][b]
for c,(i,j) in enumerate(pairs):
    G=tr(unit(i,j,-1))
    assert all(G[a][b]==-G[b][a] for a in range(q) for b in range(q))
    for r,(a,b) in enumerate(pairs): A2[r][c]=G[a][b]
print("antisymmetric square (rows/cols = pairs %s):" % pairs)
for r in A2: print("  ", r)
print("non-zeros per row:", [sum(1 for v in r if v) for r in A2], " A2*A2 = 16 I:", mm(A2,A2)==[[16*(i==j) for j in range(6)] for i in range(6)])
print("symmetric square non-zeros per row:", [sum(1 for v in r if v) for r in S2], " S2*S2 = 16 I:", mm(S2,S2)==[[16*(i==j) for j in range(10)] for i in range(10)])
with open("rows_alt4.txt","w") as fh:
    for r in A2: fh.write(" ".join(str(v//2) for v in r)+"\n")
with open("rows_sym4.txt","w") as fh:
    for r in S2: fh.write(" ".join(str(v) for v in r)+"\n")
# ---- explicit circuits, replayed as linear forms; a gate = a*u + b*v ----
class Circ:
    def __init__(s,n): s.n=n; s.g=0
    def inp(s,i): v=[0]*s.n; v[i]=1; return v
    def gate(s,a,u,b,v): s.g+=1; return [a*x+b*y for x,y in zip(u,v)]
def prop(u,v):
    k=[(x,y) for x,y in zip(u,v) if x or y]
    return all(x*k[0][1]==y*k[0][0] for x,y in k) and any(y for _,y in k)
def h4(c,x):      # 7-gate 4-point transform (free scalings): returns forms proportional to the rows of H in order 0..3
    w1=c.gate(1,x[0],1,x[1]); w2=c.gate(1,x[2],1,x[3]); y0=c.gate(1,w1,1,w2); y2=c.gate(1,w1,-1,w2)
    w3=c.gate(2,x[0],-1,y0); y3=c.gate(1,w3,2,x[3]); y1=c.gate(1,w3,2,x[2]); return [y0,y1,y2,y3]
def bf(c,u,v): return c.gate(1,u,1,v), c.gate(1,u,-1,v)
# antisymmetric: coordinates A(x,y), x<y. slice m = x^y != 0, representative x with x < x^m.
c=Circ(6); X={p:c.inp(i) for i,p in enumerate(pairs)}
That={}
for m in (1,2,3):
    reps=[x for x in range(q) if x<x^m]            # two reps
    u,v=X[(reps[0],reps[0]^m)],X[(reps[1],reps[1]^m)]
    That[m]=bf(c,u,v)                               # (sum, difference) over the quotient by m
outs=[]
for w in (1,2,3):
    ms=[m for m in (1,2,3) if bin(m&w).count("1")%2==1]   # the two slices that reach frequency difference w
    # the antisymmetric slice m is odd under x -> x+m, so only its "difference" part can be non-zero at w; try all 4 choices
    ok=False
    for i0 in (0,1):
        for i1 in (0,1):
            s,d=[c2 for c2 in bf(Circ(6),That[ms[0]][i0],That[ms[1]][i1])]
            tg=[A2[r] for r,(a,b) in enumerate(pairs) if a^b==w]
            if (prop(s,tg[0]) and prop(d,tg[1])) or (prop(s,tg[1]) and prop(d,tg[0])): ok=True; pick=(i0,i1)
    assert ok
    s,d=bf(c,That[ms[0]][pick[0]],That[ms[1]][pick[1]]); outs+=[s,d]
good=all(any(prop(o,r) for o in outs) for r in A2)
print("antisymmetric square: %d gates, all 6 rows produced: %s" % (c.g, good))
# only the parts actually used: count unused first-layer outputs
# symmetric: coordinates S(x,y), x<=y.
c=Circ(10); X={p:c.inp(i) for i,p in enumerate(symc)}
T0=h4(c,[X[(x,x)] for x in range(q)])              # transform of the diagonal slice m = 0: frequencies w = 0..3
Th={}
for m in (1,2,3):
    reps=[x for x in range(q) if x<x^m]
    Th[m]=bf(c,X[(reps[0],reps[0]^m)],X[(reps[1],reps[1]^m)])
outs=[]
# frequency difference w = 0 (diagonal outputs): 4-point transform over the slices of their w = 0 parts (the sums)
sc=lambda v:[2*x for x in v]   # free scaling: each pair of the full array is one coordinate here
outs+=h4(c,[T0[0],sc(Th[1][0]),sc(Th[2][0]),sc(Th[3][0])])
for w in (1,2,3):
    mw=[m for m in (1,2,3) if bin(m&w).count("1")%2==0][0]
    tg=[S2[r] for r,(a,b) in enumerate(symc) if a^b==w]
    found=None
    for coef in (1,2,-1,-2,4,-4):
        cc=Circ(10); s=cc.gate(1,T0[w],coef,Th[mw][1]); d=cc.gate(1,T0[w],-coef,Th[mw][1])
        if (prop(s,tg[0]) and prop(d,tg[1])) or (prop(s,tg[1]) and prop(d,tg[0])): found=coef
    assert found is not None, w
    outs+=[c.gate(1,T0[w],found,Th[mw][1]), c.gate(1,T0[w],-found,Th[mw][1])]
good=all(any(prop(o,r) for o in outs) for r in S2)
print("symmetric square: %d gates, all 10 rows produced: %s" % (c.g, good))
print("16 points by this route: split 12 + middle (sym) + middle (antisym) + merge 12")
