# First experiment (b),(c): 16 points. Frames L from cheap eigenvectors; R = L^T (Gram) first.
# Orthogonal frames = cliques in the orthogonality graph: then R L is diagonal and there is NO middle.
# Program count (G): total = 2*s_R + m, s_R = gates for the m functionals (greedy upper bound), m = dim of minus space.
import sys, random; sys.path.insert(0,'waves/wave-02/e-1-vcycle')
from lib import *
k=4; N=16; r=4
def minus_vectors(M,sizes):
    out={}
    for D,a,b,f in atoms(k,sizes):
        v=canon(lin(r,f,-1,mv(M,f)))
        if v is not None and v not in out: out[v]=(len(D),a,b)
    return out
for name,M,m in (('S',sympS(k),6),('H',plainH(k),8)):
    mvs=minus_vectors(M,(2,4,8)); V=sorted(mvs); n=len(V)
    print('==',name,'minus vectors',n,'target dim',m)
    adj=[set(j for j in range(n) if j!=i and ip(V[i],V[j])==0) for i in range(n)]
    degs=sorted(len(a) for a in adj); print(' orthogonality graph: degrees min/median/max',degs[0],degs[n//2],degs[-1])
    cliques=[]
    def ext(cl,cand):
        if len(cl)==m: cliques.append(tuple(cl)); return
        if len(cl)+len(cand)<m: return
        for v in sorted(cand):
            ext(cl+[v],{w for w in cand if w>v and w in adj[v]})
    ext([],set(range(n)))
    print(' orthogonal frames (cliques of size m):',len(cliques))
    res=[]
    for cl in cliques:
        rows=[V[i] for i in cl]
        res.append((cse_cost(rows),sum(nnz(v) for v in rows),tuple(sorted(mvs[V[i]][0] for i in cl)),cl))
    res.sort()
    hist={}
    for c,z,sc,cl in res: hist[(c,z,sc)]=hist.get((c,z,sc),0)+1
    print(' histogram (s_R greedy, non-zeros, subgroup sizes used): count')
    for key in sorted(hist)[:25]: print('  ',key,hist[key],' total program 2*s_R+m =',2*key[0]+m)
    if res:
        c,z,sc,cl=res[0]
        print(' best frame: s_R',c,'total',2*c+m,'(textbook 64, known 56)')
        for i in cl: print('   ',V[i],mvs[V[i]])
