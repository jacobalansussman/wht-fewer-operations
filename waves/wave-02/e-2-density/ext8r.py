#!/usr/bin/env python3
# e-2-density/ext8r.py: as ext8.py, but the order in which each value of the transposed circuit adds up its terms is shuffled
# (the 16 gates differ from order to order, the 6 outputs do not).  For each order: can outputs 6 and 7 be had with <= 4 more gates
# (total 20), exhaustively over GF(5)?   usage: ext8r.py <number of orders>
import sys, re, subprocess, os, random
p=5; S=(0,1,2,3,4,5); m=6; tries=int(sys.argv[1])
pc=lambda v: bin(v).count("1")
txt=open("circ_m6_0-1-2-3-4-5_p%d.txt"%p).read()
pts=[[1 if i==j else 0 for j in range(m)] for i in range(m)]; gates=[]
for mm in re.finditer(r"g(\d+)\s+(TARGET|inter)\s+= \[([\d ]+)\]\s+from #(\d+) \+ (\d+)\*#(\d+)",txt):
    i=int(mm.group(1)); vec=[int(x) for x in mm.group(3).split()]; u=int(mm.group(4)); b=int(mm.group(5)); v=int(mm.group(6))
    raw=[(pts[u][k]+b*pts[v][k])%p for k in range(m)]
    lam=next(l for l in range(1,p) if [(l*x)%p for x in raw]==vec)
    pts.append(vec); gates.append((i,u,lam,v,(lam*b)%p))
tx={tuple((1 if not pc(s&x)&1 else p-1) for s in S):x for x in range(8)}
users={i:[] for i in range(len(pts))}
for (i,u,a,v,b) in gates: users[u].append((i,a)); users[v].append((i,b))
open("tgt67.txt","w").write("1 1 -1 -1 -1 -1 1 1\n1 -1 -1 1 -1 1 1 -1\n")
hist={}
for tr in range(tries):
    rnd=random.Random(tr); val={}; seeds=[]
    for i in range(len(pts)-1,-1,-1):
        terms=[]
        if tuple(pts[i]) in tx and i>=m: e=[0]*8; e[tx[tuple(pts[i])]]=1; terms.append(e)
        for (w,c) in users[i]: terms.append([(c*x)%p for x in val[w]])
        if tr: rnd.shuffle(terms)
        acc=terms[0][:]
        for t in terms[1:]:
            acc=[(a+b)%p for a,b in zip(acc,t)]; seeds.append(acc[:])
        val[i]=acc
    assert len(seeds)==16
    fn="seeds_r%d.txt"%tr; open(fn,"w").write("\n".join(" ".join(map(str,s)) for s in seeds)+"\n")
    best=None
    for k in range(0,4):
        o=subprocess.run(["./mincirc_seed",str(p),"8",str(k),"tgt67.txt"],capture_output=True,text=True,env=dict(os.environ,SEEDS=fn)).stdout
        if "YES" in o:
            best=2+k
            if best<5: open("ext67_r%d.txt"%tr,"w").write(o)
            break
    hist[best]=hist.get(best,0)+1
    if best is None or best>=5: os.remove(fn)
    else: print("order %d: outputs 6 and 7 with %d more gates -> total %d  (candidate modulo 5, file ext67_r%d.txt)"%(tr,best,16+best,tr),flush=True)
print("[ran] over %d orders, least number of extra gates for outputs 6 and 7 (None = more than 5): %s"%(tries,sorted(hist.items(),key=str)))
