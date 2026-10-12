# d-4's free third, split by eigenspace.  For the hyperbolic form Q0 = x0 x1 + x2 x3 (+ x4 x5), T = diag((-1)^Q0):
# minus part = vectors of the minus space supported where Q0 = 1 ; plus part = vectors of the plus space supported where Q0 = 0.
# predicted dimensions ((N+2)/3 -+ sqrt N)/2.
import sys; sys.path.insert(0,'waves/wave-02/e-1-vcycle')
from lib import *
for k in (2,4,6):
    N=1<<k; r=1<<(k//2); S=sympS(k)
    Q=[sum(((x>>i)&1)&((x>>(i+1))&1) for i in range(0,k,2))&1 for x in range(N)]
    g=[1-2*q for q in Q]; assert mv(S,g)==tuple(r*t for t in g)
    one=[x for x in range(N) if Q[x]]; zero=[x for x in range(N) if not Q[x]]
    A=[[S[y][x]+r*(y==x) for x in one] for y in range(N)]      # (S + r) restricted to columns where Q0 = 1
    B=[[S[y][x]-r*(y==x) for x in zero] for y in range(N)]
    dm=len(one)-rank_exact(A) if one else 0; dp=len(zero)-rank_exact(B)
    print('N =',N,': points with Q0 = 1:',len(one),'| minus part of the free third: dim',dm,'| plus part: dim',dp,'| predicted',((N+2)//3-r)//2,((N+2)//3+r)//2,'| total',dm+dp,'= (N+2)/3 =',(N+2)//3)
