#!/usr/bin/env python3
# e-2-density/replay21.py: EXACT replay over the rationals of the candidate circuit in ext67_p5.txt (found modulo 5):
# 8 inputs, 21 gates, every gate one combination a*u + b*v (count G).  Claim to test: its values contain all 8 rows of the
# 8-point Walsh-Hadamard matrix up to a non-zero factor.  Nothing modular is trusted: each gate's vector is lifted to integers,
# then a, b are solved exactly and the gate is recomputed from its two operands.
import re, sys
from fractions import Fraction as Fr
p=5; n=8
txt=open(sys.argv[1] if len(sys.argv)>1 else "ext67_p5.txt").read()
pts=[[Fr(1 if i==j else 0) for j in range(n)] for i in range(n)]
def solve2(u,v,w):
    # find a,b with a*u+b*v = lam*w for some lam != 0, exactly: try every pair of coordinates for a 2x2 solve of a*u+b*v=w
    for i in range(n):
        for j in range(i+1,n):
            det=u[i]*v[j]-u[j]*v[i]
            if det==0: continue
            a=(w[i]*v[j]-w[j]*v[i])/det; b=(u[i]*w[j]-u[j]*w[i])/det
            if all(a*u[k]+b*v[k]==w[k] for k in range(n)): return a,b
            return None
    return None
specs=[]
for mm in re.finditer(r"g(\d+)\s+(TARGET|inter)\s+= \[([\d ]+)\]\s+from #(\d+) \+ (\d+)\*#(\d+)",txt):
    specs.append((int(mm.group(1)),[int(x) for x in mm.group(3).split()],int(mm.group(4)),int(mm.group(6))))
def lifts(res):
    alts=[[]]
    for x in res:
        c=[0] if x==0 else [1] if x==1 else [-1] if x==4 else [2,-3] if x==2 else [-2,3]
        alts=[a+[y] for a in alts for y in c]
    return alts
gates=[]
def dfs(k):
    # depth-first over the possible integer lifts of each gate (a lift that works for one gate may fail a later one)
    if k==len(specs): return True
    i,res,u,v=specs[k]; assert i==len(pts)
    for w in lifts(res):
        w=[Fr(y) for y in w]; sol=solve2(pts[u],pts[v],w)
        if sol is None: continue
        a,b=sol; val=[a*x+b*y for x,y in zip(pts[u],pts[v])]; assert val==w
        pts.append(val); gates.append((i,u,a,v,b))
        if dfs(k+1): return True
        pts.pop(); gates.pop()
    return False
ok=dfs(0)
if not ok: print("NO exact lift of the whole circuit")
for (i,u,a,v,b) in gates: print("  g%-2d = (%s)*#%d + (%s)*#%d = %s"%(i,a,u,b,v,[int(x) for x in pts[i]]))
if ok:
    pc=lambda z: bin(z).count("1")
    rows={s:[(-1)**(pc(s&x)&1) for x in range(8)] for s in range(8)}
    got={}
    for s,row in rows.items():
        for i in range(n,len(pts)):
            lam=pts[i][0]
            if lam!=0 and [lam*r for r in row]==pts[i]: got[s]=(i,lam)
    for s in range(8): print("  output %d (row %s): %s"%(s,rows[s],"gate g%d, factor %s"%got[s] if s in got else "MISSING"))
    ng=len(gates); nscal=sum(1 for (_,u,a,v,b) in gates if abs(a)!=abs(b))
    print("RESULT: %s  gates (count G) = %d ; gates whose two coefficients differ in size (each needs one scalar multiplication in count O) = %d ; largest |coefficient| = %s"%(
        "ALL 8 OUTPUTS PRESENT, EXACT" if len(got)==8 else "INCOMPLETE",ng,nscal,max(max(abs(a),abs(b)) for (_,u,a,v,b) in gates)))
