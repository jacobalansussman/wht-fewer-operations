# The 16 sparsest minus vectors at 16 points: are their supports quadrics, are they d-4's "free third" (minus part), and are they a tight frame?
import sys; sys.path.insert(0,'waves/wave-02/e-1-vcycle')
from lib import *
k=4; N=16; S=sympS(k)
u=(1,-1,-1,-1)
def kron(a,b): return tuple(x*y for x in a for y in b)
E=[tuple(int(i==j) for i in range(4)) for j in range(4)]
V=[]
for i in range(4):
    for j in range(4):
        V.append(lin(1,kron(u,E[j]),-u[i]*u[j],kron(E[i],u)))
kinds={}
for v in V:
    g=tuple(-1 if t else 1 for t in v)            # sign function of the support
    Sg=mv(S,g)
    kind='+4' if Sg==tuple(4*t for t in g) else '-4' if Sg==tuple(-4*t for t in g) else 'neither'
    Tv=tuple(a*b for a,b in zip(g,v))             # T = diag(sign function); T v = -v since v lives where g = -1
    kinds[kind]=kinds.get(kind,0)+1
    assert Tv==tuple(-t for t in v) and mv(S,v)==tuple(-4*t for t in v)   # S = 4 T on v
print('sign function of each support is an eigenvector of S with eigenvalue:',kinds,' (so each support is a quadric), and S v = 4 T v on all 16')
# tight frame: sum v v^T = c * projector on the minus space = c (I - S/4)/2
M=[[sum(v[i]*v[j] for v in V) for j in range(N)] for i in range(N)]
print('sum of v v^T == 8 I - 2 S (= 16 * projector):',M==[[8*(i==j)-2*S[i][j] for j in range(N)] for i in range(N)])
G=[[ip(a,b) for b in V] for a in V]
print('Gram values',sorted(set(t for r_ in G for t in r_)),' -> 16 equiangular lines in a 6-dimensional space, cosine 1/3')
# V as a 16 x 16 matrix: rank, and the 8-contraction factorisation V^T = C * [P;Q]
print('rank of the 16 x 16 matrix of these vectors:',rank_exact(V))
