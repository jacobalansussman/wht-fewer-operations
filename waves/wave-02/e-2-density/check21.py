#!/usr/bin/env python3
# e-2-density/check21.py: independent check of h8_21gates.txt.  Each gate line is parsed as text, evaluated on the 8 unit inputs
# (so each value is its exact integer coefficient vector), and the outputs are compared with the rows of the 8-point matrix.
import re
env={}
for i in range(8): env["x%d"%i]=[1 if j==i else 0 for j in range(8)]
ng=0; nscal=0
for line in open("h8_21gates.txt"):
    line=line.split("#")[0].strip()
    if not line: continue
    name,expr=[t.strip() for t in line.split("=")]
    toks=re.findall(r"([+-]?)\s*(?:(\d+)\*)?([xgy]\d+)",expr)
    acc=[0]*8; cs=[]
    for sg,c,v in toks:
        k=(int(c) if c else 1)*(-1 if sg=="-" else 1); cs.append(abs(k))
        acc=[a+k*b for a,b in zip(acc,env[v])]
    if name.startswith("g"):
        assert len(toks)==2, line           # one gate = one combination of exactly two earlier values
        ng+=1; nscal+=(cs[0]!=cs[1])
    else: assert len(toks)==1
    env[name]=acc
pc=lambda z: bin(z).count("1")
ok=all(env["y%d"%s]==[(-1)**(pc(s&x)&1) for x in range(8)] for s in range(8))
print("gates:",ng,"| all 8 outputs equal their rows exactly:",ok,"| gates needing a scalar multiplication in count (O):",nscal,"-> count (O) =",ng+nscal,"(textbook 24)")
