#!/usr/bin/env python3
# e-2-density/ext8.py: take the minimal circuit found for 6 outputs of the 8-point transform (16 gates, count G), turn it from its dual form
# into the ordinary form (transposition), and ask exhaustively over GF(p): how many more gates do outputs 6 and 7 need, if every value
# of that circuit may be reused?  22 is the best known count for all 8 outputs, so "16 + fewer than 6" would be news.
import sys, re, subprocess, os
p=int(sys.argv[1]); kmax=int(sys.argv[2]); tmo=float(sys.argv[3])
S=(0,1,2,3,4,5); m=6
pc=lambda v: bin(v).count("1")
txt=open("circ_m6_0-1-2-3-4-5_p%d.txt"%p).read()
pts=[[1 if i==j else 0 for j in range(m)] for i in range(m)]; gates=[]
for mm in re.finditer(r"g(\d+)\s+(TARGET|inter)\s+= \[([\d ]+)\]\s+from #(\d+) \+ (\d+)\*#(\d+)",txt):
    i=int(mm.group(1)); vec=[int(x) for x in mm.group(3).split()]; u=int(mm.group(4)); b=int(mm.group(5)); v=int(mm.group(6))
    assert i==len(pts)
    raw=[(pts[u][k]+b*pts[v][k])%p for k in range(m)]
    lam=next(l for l in range(1,p) if [(l*x)%p for x in raw]==vec)       # vec = lam*(P_u + b P_v)
    pts.append(vec); gates.append((i,u,lam,v,(lam*b)%p,mm.group(2)=="TARGET"))
tx={tuple((1 if not pc(s&x)&1 else p-1) for s in S):x for x in range(8)}
users={i:[] for i in range(len(pts))}
for (i,u,a,v,b,isT) in gates: users[u].append((i,a)); users[v].append((i,b))
val={}; seeds=[]; ngates=0
for i in range(len(pts)-1,-1,-1):
    terms=[]
    if tuple(pts[i]) in tx and i>=m: e=[0]*8; e[tx[tuple(pts[i])]]=1; terms.append(e)
    for (w,c) in users[i]: terms.append([(c*x)%p for x in val[w]])
    acc=terms[0][:]
    for t in terms[1:]:
        acc=[(a+b)%p for a,b in zip(acc,t)]; seeds.append(acc[:]); ngates+=1
    val[i]=acc
for s in range(m):
    row=[(1 if not pc(S[s]&x)&1 else p-1) for x in range(8)]
    assert any([(l*v)%p for v in val[s]]==row for l in range(1,p)), (s,val[s],row)
print("[ran] transposed circuit: %d gates compute outputs 0..5 of the 8-point transform over GF(%d) (replayed: each output is its row of +-1)"%(ngates,p))

# exact replay over the integers: lift every coefficient to the residue of least absolute value and redo the transposed circuit
def lift(c): return c if c<=p//2 else c-p
valZ={}
for i in range(len(pts)-1,-1,-1):
    acc=[0]*8
    if tuple(pts[i]) in tx and i>=m: acc[tx[tuple(pts[i])]]+=1
    for (w,c) in users[i]: acc=[a+lift(c)*x for a,x in zip(acc,valZ[w])]
    valZ[i]=acc
okZ=True
for s_ in range(m):
    row=[(1 if not pc(S[s_]&x)&1 else -1) for x in range(8)]
    sc=valZ[s_][0]
    if sc==0 or [sc*r for r in row]!=valZ[s_]: okZ=False
    print("   output %d over the integers: %s  (%s)"%(s_,valZ[s_],"= %d x its row"%sc if sc and [sc*r for r in row]==valZ[s_] else "NOT its row"))
print("[ran] exact integer replay of the %d-gate circuit for outputs 0..5: %s"%(ngates,"PASS" if okZ else "FAIL (a modular accident)"))
open("seeds_p%d.txt"%p,"w").write("\n".join(" ".join(map(str,s)) for s in seeds)+"\n")
for tg,name in (([6],"output 6 alone"),([7],"output 7 alone"),([6,7],"outputs 6 and 7")):
    open("tgt.txt","w").write("\n".join(" ".join(str(1 if not pc(s&x)&1 else -1) for x in range(8)) for s in tg)+"\n")
    for k in range(kmax+1):
        try:
            o=subprocess.run(["./mincirc_seed",str(p),"8",str(k),"tgt.txt"],capture_output=True,text=True,timeout=tmo,env=dict(os.environ,SEEDS="seeds_p%d.txt"%p)).stdout
        except subprocess.TimeoutExpired:
            print("  %s: k=%d timed out (so: at least %d more gates, GF(%d), reusing this one circuit)"%(name,k,len(tg)+k,p)); break
        if "YES" in o:
            print("  %s: %d more gates suffice and %d do not (GF(%d), exhaustive, reusing this one circuit): total %d"%(name,len(tg)+k,len(tg)+k-1,p,ngates+len(tg)+k)); break
        else: print("    %s: NO with %d more gates"%(name,len(tg)+k),flush=True)
