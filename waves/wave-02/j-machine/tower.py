#!/usr/bin/env python3
"""tower.py -- exact integers.  H = 1*c^T - 2E with c a bent centre.  Check: row weights of E, E*E^T = (N/4) I + rank<=2,
and how sparse the pairwise combinations of rows of E are (the next level of the tower)."""
from fractions import Fraction as F
from collections import Counter
def rank(M):
    M=[[F(x) for x in r] for r in M]; r=0
    for c in range(len(M[0])):
        p=next((i for i in range(r,len(M)) if M[i][c]!=0),None)
        if p is None: continue
        M[r],M[p]=M[p],M[r]
        for i in range(r+1,len(M)):
            if M[i][c]!=0:
                f=M[i][c]/M[r][c]; M[i]=[a-f*b for a,b in zip(M[i],M[r])]
        r+=1
    return r
for m in (2,4,6):
    N=1<<m
    H=[[(-1)**bin(x&y).count('1') for y in range(N)] for x in range(N)]
    def q(x): return sum(((x>>(2*i))&1)*((x>>(2*i+1))&1) for i in range(m//2))&1
    c=[(-1)**q(x) for x in range(N)]
    E=[[(c[y]-H[x][y])//2 for y in range(N)] for x in range(N)]
    w=Counter(sum(1 for v in r if v) for r in E)
    G=[[sum(a*b for a,b in zip(E[i],E[j])) for j in range(N)] for i in range(N)]
    R=[[G[i][j]-(N//4 if i==j else 0) for j in range(N)] for i in range(N)]
    pw=Counter()
    for i in range(N):
        for j in range(i+1,N):
            pw[min(sum(1 for a,b in zip(E[i],E[j]) if a!=b), sum(1 for a,b in zip(E[i],E[j]) if a!=-b))]+=1
    print('N',N,'row weights of E',dict(w),'| rank(E)',rank(E),'| rank(E E^T - N/4 I)',rank(R),'| weight of sparsest E_i -/+ E_j over pairs',dict(sorted(pw.items())))
