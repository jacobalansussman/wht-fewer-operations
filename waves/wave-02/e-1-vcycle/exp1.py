# First experiment (a): 16 points, cheap eigenvectors (coset atom) - (its image), what they span.
import sys; sys.path.insert(0,'waves/wave-02/e-1-vcycle')
from lib import *
k=4; N=16; r=4
for name,M in (('S (relabelled, minus space 6)',sympS(k)),('H (plain, minus space 8)',plainH(k))):
    assert matmul(M,M)==[[N*(i==j) for j in range(N)] for i in range(N)]
    print('==',name,' trace',sum(M[i][i] for i in range(N)))
    for sizes in ((2,),(4,),(8,),(2,8),(2,4,8),(1,16),(1,2,4,8,16)):
        At=atoms(k,sizes)
        minus=[]; plus=[]; hist={}
        for D,a,b,f in At:
            g=mv(M,f)
            vm=lin(r,f,-1,g); vp=lin(r,f,1,g)
            if any(vm): minus.append(vm)
            if any(vp): plus.append(vp)
            nzm=nnz(vm); hist[nzm]=hist.get(nzm,0)+1
        ms=sorted(set(canon(v) for v in minus)); ps=sorted(set(canon(v) for v in plus))
        print(' sizes',sizes,'atoms',len(At),'| minus vectors (distinct up to scale)',len(ms),'rank',rank_exact(ms),
              '| plus',len(ps),'rank',rank_exact(ps),'| non-zeros of minus vector: histogram',dict(sorted(hist.items())))
