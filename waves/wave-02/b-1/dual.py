# dual.py m  [b-1]  floating-point LP (HiGHS) used ONLY to produce a pruning bound; cover.c re-checks the bound in integers.
import sys, numpy as np
from scipy.optimize import linprog
m=int(sys.argv[1]); W=4
pairs=[(i,j) for i in range(m) for j in range(i,m)]; NP=len(pairs)
zz=[sum(((z>>i&1)&(z>>j&1))<<t for t,(i,j) in enumerate(pairs)) for z in range(1<<m)]
diag=sum(1<<t for t,(i,j) in enumerate(pairs) if i==j)
Qs=[Q for Q in range(1<<NP) if bin(Q&diag).count('1')&1]
A=np.array([[bin(Q&zz[z]).count('1')&1 for z in range(1,1<<m)] for Q in Qs],dtype=float)
res=linprog(np.ones(A.shape[1]),A_ub=-A,b_ub=-W*np.ones(len(Qs)),bounds=(0,None),method='highs')
y=-res.ineqlin.marginals
print("LP value per array", res.fun/W, file=sys.stderr)
for Q,v in zip(Qs,y):
    k=int(v*1e7)
    if k>0: print(Q,k)
