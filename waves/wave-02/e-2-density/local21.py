#!/usr/bin/env python3
# e-2-density/local21.py: is the 21-gate circuit locally best?  Delete a set D of its gates (closed upwards: a deleted gate takes its
# users with it), keep the rest as free values, and ask exhaustively over GF(5) whether all 8 outputs can be completed with |D| - 1
# gates (that would be a 20-gate circuit).  D runs over all upward closures of one or two gates with |D| - 1 - (missing outputs) <= KMAX helpers.
import re, sys, subprocess, os, itertools
p=5; KMAX=int(sys.argv[1]); tmo=float(sys.argv[2])
env={}; order=[]; ops={}
for i in range(8): env["x%d"%i]=[1 if j==i else 0 for j in range(8)]
outs={}
for line in open("h8_21gates.txt"):
    line=line.split("#")[0].strip()
    if not line: continue
    name,expr=[t.strip() for t in line.split("=")]
    toks=re.findall(r"([+-]?)\s*(?:(\d+)\*)?([xgy]\d+)",expr); acc=[0]*8
    for sg,c,v in toks:
        k=(int(c) if c else 1)*(-1 if sg=="-" else 1); acc=[a+k*b for a,b in zip(acc,env[v])]
    env[name]=acc
    if name.startswith("g"): order.append(name); ops[name]=[v for _,_,v in toks]
    else: outs[name]=toks[0][2]
users={g:set() for g in order}
for g in order:
    for v in ops[g]:
        if v in users: users[v].add(g)
def up(roots):
    D=set(roots); st=list(roots)
    while st:
        g=st.pop()
        for w in users[g]:
            if w not in D: D.add(w); st.append(w)
    return frozenset(D)
pc=lambda z: bin(z).count("1")
open("tgt_all.txt","w").write("\n".join(" ".join(str((-1)**(pc(s&x)&1)) for x in range(8)) for s in range(8))+"\n")
sets=set()
for r in range(1,3):
    for roots in itertools.combinations(order,r): sets.add(up(roots))
res={}; done=0; skipped=0
for D in sorted(sets,key=lambda D:(len(D),sorted(D))):
    d=len(D); t=sum(1 for y,g in outs.items() if g in D); k=d-1-t
    if k<0 or k>KMAX: skipped+=1; continue
    open("seeds_loc.txt","w").write("\n".join(" ".join(str(x%p) for x in env[g]) for g in order if g not in D)+"\n")
    try:
        o=subprocess.run(["./mincirc_seed",str(p),"8",str(k),"tgt_all.txt"],capture_output=True,text=True,timeout=tmo,env=dict(os.environ,SEEDS="seeds_loc.txt")).stdout
    except subprocess.TimeoutExpired:
        res["timeout"]=res.get("timeout",0)+1; continue
    done+=1
    if "YES" in o:
        print("IMPROVEMENT CANDIDATE (modulo 5): delete",sorted(D),"-> completed with",d-1,"gates; total",21-1,flush=True)
        open("local_candidate_%d.txt"%done,"w").write("deleted: "+" ".join(sorted(D))+"\n"+o); res["yes"]=res.get("yes",0)+1
    else: res[(d,t)]=res.get((d,t),0)+1
print("[ran] deletion sets tried: %d (skipped as out of reach: %d). outcomes: %s"%(done,skipped,sorted(res.items(),key=str)))
print("      keys (d, t): d gates deleted of which t are outputs; every such case: NO completion with d - 1 gates, exhaustive over GF(5)")
