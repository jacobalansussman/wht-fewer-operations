# Explicit program from a frame, replayed exactly.  16 points, S form.  Count (G): a gate is a*u + b*v, scalings free.
# usage: verify.py <exp6-style output file>   (reads the six vectors after 'best found')
# Program:  c = R x  (R = dual frame, 16 -> 6);   y = x - 2 L c  (22 -> 16);   check y == S x / 4 on every basis vector.
import sys, ast; sys.path.insert(0,'waves/wave-02/e-1-vcycle')
from lib import *
def cse_circuit(M):
    """greedy as lib.cse_cost but returns the gates: (new, i, j, rho) means new = x_i + rho*x_j ; and outputs (var, coef)"""
    rows=[{j:Fraction(int(v)) if not isinstance(v,Fraction) else v for j,v in enumerate(r) if v!=0} for r in M]
    gates=[]; nxt=len(M[0])
    while True:
        cnt={}
        for r in rows:
            if len(r)<2: continue
            ks=sorted(r)
            for x in range(len(ks)):
                for y in range(x+1,len(ks)):
                    key=(ks[x],ks[y],r[ks[y]]/r[ks[x]]); cnt[key]=cnt.get(key,0)+1
        if not cnt: break
        (i,j,rho),c=max(cnt.items(),key=lambda kv:(kv[1],-kv[0][0],-kv[0][1]))
        for r in rows:
            if i in r and j in r and r[j]/r[i]==rho:
                ci=r[i]; del r[i]; del r[j]; r[nxt]=ci
        gates.append((nxt,i,j,rho)); nxt+=1
    outs=[]
    for r in rows:
        assert len(r)==1; (v,c),=r.items(); outs.append((v,c))
    return gates,outs
def run(gates,outs,x):
    val=dict(enumerate(x))
    for new,i,j,rho in gates: val[new]=val[i]+rho*val[j]
    return [c*val[v] for v,c in outs]
k=4; N=16; S=sympS(k); m=6
txt=open(sys.argv[1]).read().split('best found')[1]
vecs=[ast.literal_eval(l.strip()) for l in txt.splitlines() if l.strip().startswith('(')]
L=vecs[:m]
assert all(mv(S,v)==tuple(-4*t for t in v) for v in L) and rank_exact(L)==m
g=[[ip(a,b) for b in L] for a in L]; gi=inv_exact(g)
R=[[sum(gi[i][j]*L[j][t] for j in range(m)) for t in range(N)] for i in range(m)]      # R L = identity
assert all(sum(R[i][t]*L[j][t] for t in range(N))==(i==j) for i in range(m) for j in range(m))
g1,o1=cse_circuit(R)
B=[[Fraction(int(i==t)) for t in range(N)]+[Fraction(-2*L[j][i]) for j in range(m)] for i in range(N)]   # y = x - 2 L c
g2,o2=cse_circuit(B)
ok=True
for t in range(N):
    x=[Fraction(int(i==t)) for i in range(N)]
    c=run(g1,o1,x); y=run(g2,o2,x+c)
    ok&=(y==[Fraction(S[i][t],4) for i in range(N)])
print('frame:'); [print('  ',v) for v in L]
print('analysis circuit (dual frame, 16 -> 6):',len(g1),'gates | synthesis circuit (x - 2 L c, 22 -> 16):',len(g2),'gates | total',len(g1)+len(g2))
print('exact replay on the 16 basis vectors: program == S/4 :',ok)
print('references, count (G): 56 (one reflection per base-4 digit), 64 textbook')
import json; json.dump({'frame':L,'analysis_gates':[(a,b,c,str(d)) for a,b,c,d in g1],'analysis_outputs':[(v,str(c)) for v,c in o1],
  'synthesis_gates':[(a,b,c,str(d)) for a,b,c,d in g2],'synthesis_outputs':[(v,str(c)) for v,c in o2],'total':len(g1)+len(g2),'exact':ok},open(sys.argv[1]+'.program.json','w'))
