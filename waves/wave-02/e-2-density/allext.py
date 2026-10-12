#!/usr/bin/env python3
# e-2-density/allext.py: every least circuit (reversed form, 6 helpers, GF(5)) for six outputs of the 8-point transform that
# mincirc_all printed -> reverse it (16 gates) -> exhaustive search for outputs 6 and 7 with at most 4 more gates (total 20).
import sys, re, subprocess, os, itertools
p=int(sys.argv[3]); m=6; S=(0,1,2,3,4,5)
pc=lambda v: bin(v).count("1")
def canon(v):
    f=next((x for x in v if x%p),None)
    if f is None: return None
    inv=pow(f,p-2,p); return tuple((x*inv)%p for x in v)
units=[tuple(1 if i==j else 0 for j in range(m)) for i in range(m)]
targ={canon([(1 if not pc(s&x)&1 else p-1) for s in S]):x for x in range(8)}
sets=[]
for line in open(sys.argv[1]):
    if "example" in line:
        sets.append([tuple(int(c) for c in w) for w in re.findall(r"\[(\d+)\]",line)])
print("least circuits listed:",len(sets))
open("tgt67.txt","w").write("1 1 -1 -1 -1 -1 1 1\n1 -1 -1 1 -1 1 1 -1\n")
hist={}
for si,inter in enumerate(sets[:int(sys.argv[2])]):
    pts=list(units); gates=[]; pend=set(inter)|set(targ)
    while pend:
        prog=False
        for w in list(pend):
            hit=None
            for iu in range(len(pts)):
                for iv in range(iu):
                    for a in range(1,p):
                        for b in range(1,p):
                            if tuple((a*x+b*y)%p for x,y in zip(pts[iu],pts[iv]))==w: hit=(iu,a,iv,b); break
                        if hit: break
                    if hit: break
                if hit: break
            if hit: gates.append((len(pts),)+hit); pts.append(w); pend.discard(w); prog=True
        if not prog: break
    if pend: hist["unbuildable?"]=hist.get("unbuildable?",0)+1; continue
    users={i:[] for i in range(len(pts))}
    for (i,u,a,v,b) in gates: users[u].append((i,a)); users[v].append((i,b))
    val={}; seeds=[]
    for i in range(len(pts)-1,-1,-1):
        terms=[]
        if pts[i] in targ and i>=m: e=[0]*8; e[targ[pts[i]]]=1; terms.append(e)
        for (w,c) in users[i]: terms.append([(c*x)%p for x in val[w]])
        acc=terms[0][:]
        for t in terms[1:]:
            acc=[(a+b)%p for a,b in zip(acc,t)]; seeds.append(acc[:])
        val[i]=acc
    assert len(seeds)==16, len(seeds)
    fn="seeds_all.txt"; open(fn,"w").write("\n".join(" ".join(map(str,s)) for s in seeds)+"\n")
    best=None
    for k in range(0,4):
        o=subprocess.run(["./mincirc_seed",str(p),"8",str(k),"tgt67.txt"],capture_output=True,text=True,env=dict(os.environ,SEEDS=fn)).stdout
        if "YES" in o:
            best=2+k
            if best<5:
                open("ext67_all%d.txt"%si,"w").write(o); print("circuit %d: outputs 6 and 7 with %d more gates -> TOTAL %d (candidate modulo 5; file ext67_all%d.txt)"%(si,best,16+best,si),flush=True)
            break
    hist[best]=hist.get(best,0)+1
print("[ran] extra gates needed for outputs 6 and 7, over the listed least circuits (None = more than 5):",sorted(hist.items(),key=str))
