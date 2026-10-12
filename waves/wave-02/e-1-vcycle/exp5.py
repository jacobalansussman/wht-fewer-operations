# The frame built around d-4's "free third": minus eigenvectors of S supported on a quadric {Q = 1} (6 points at N = 16).
# These are the sparsest vectors of the minus space. Frames of six of them: cost, Gram matrix, its inverse.
import sys, itertools; sys.path.insert(0,'waves/wave-02/e-1-vcycle')
from lib import *
k=4; N=16; S=sympS(k); m=6
fam={}
for D,a,b,f in atoms(k,(4,)):
    v=canon(lin(4,f,-1,mv(S,f)))
    if v is not None and nnz(v)==6: fam[v]=1
V=sorted(fam); print('minus vectors with 6 non-zeros:',len(V),'rank',rank_exact(V))
for v in V: print('  ',v,' support',[i for i,t in enumerate(v) if t])
G=[[ip(a,b) for b in V] for a in V]
print('inner products between them (values: count):',{t:sum(r_.count(t) for r_ in G) for t in sorted(set(x for r_ in G for x in r_))})
best=[]
for cl in itertools.combinations(range(len(V)),m):
    rows=[V[i] for i in cl]
    if rank_exact(rows)<m: continue
    g=[[ip(a,b) for b in rows] for a in rows]; gi=inv_exact(g)
    best.append((cse_cost(rows),sum(1 for r_ in g for t in r_ if t),sum(1 for r_ in gi for t in r_ if t),cl))
best.sort(); print('independent 6-subsets:',len(best))
hist={}
for c,z,zi,cl in best: hist[(c,z,zi)]=hist.get((c,z,zi),0)+1
print('(greedy s_R, non-zeros of Gram, non-zeros of inverse Gram): count')
for key in sorted(hist): print('  ',key,hist[key])
c,z,zi,cl=best[0]; rows=[V[i] for i in cl]
g=[[ip(a,b) for b in rows] for a in rows]; gi=inv_exact(g)
print('best: s_R',c); 
for r_ in g: print('   Gram',r_)
for r_ in gi: print('   inverse',[str(t) for t in r_])
# dual frame: R = G^-1 L^T has rows in the minus space too; how sparse / cheap is it?
dual=[[sum(gi[i][j]*rows[j][t] for j in range(m)) for t in range(N)] for i in range(m)]
den=1
for r_ in dual:
    for t in r_: den=den*t.denominator//gcd(den,t.denominator)
dual=[[int(t*den) for t in r_] for r_ in dual]
print('dual frame (the R that makes R L = identity): non-zeros',sum(nnz(v) for v in dual),'greedy cost',cse_cost(dual))
print('program with this pair: s_R(dual) + [s_R(L) + m] =',cse_cost(dual)+c+m,' (no middle at all); known 56')
