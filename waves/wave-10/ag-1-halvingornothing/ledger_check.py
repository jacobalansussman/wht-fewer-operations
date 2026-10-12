# ag-1: check of the determinant ledger on random circuits WITH halvings, exact whole numbers, n = 4 inputs.
# Every wire primitive.  Gate: w = (a*u + b*v)/c, a, b coprime, c = common factor of a*u + b*v.
# D = largest |minor| over all square submatrices of the wire matrix.  Claim: D_new <= max(1, (|a|+|b|)/c) * D_old.
import random, itertools
from fractions import Fraction
from math import gcd
def det(M):
    n=len(M)
    if n==1: return M[0][0]
    if n==2: return M[0][0]*M[1][1]-M[0][1]*M[1][0]
    return sum((-1)**j*M[0][j]*det([r[:j]+r[j+1:] for r in M[1:]]) for j in range(n) if M[0][j])
def maxminor(W,n):
    best=1
    for r in range(1,n+1):
        for rows in itertools.combinations(range(len(W)),r):
            for cols in itertools.combinations(range(n),r):
                d=abs(det([[W[i][j] for j in cols] for i in rows]))
                if d>best: best=d
    return best
random.seed(1); n=4; viol=0; ngates=0; nhalv=0; tight=0; kinds={}
for trial in range(400):
    W=[[1 if i==j else 0 for j in range(n)] for i in range(n)]; D=1
    for g in range(6):
        for attempt in range(200):
            u,v=random.sample(W,2); a,b=random.choice([(1,1),(1,-1),(1,2),(1,-2),(2,1),(1,3),(1,-3),(3,-1),(1,4),(3,5)])
            w=[a*x+b*y for x,y in zip(u,v)]; c=0
            for t in w: c=gcd(c,abs(t))
            if c==0: continue
            w=[t//c for t in w]
            if w in W or [-t for t in w] in W: continue
            if c%2==0 or random.random()<0.3: break     # prefer halvings when they occur
        else: break
        W.append(w); Dn=maxminor(W,n); f=Fraction(abs(a)+abs(b),c); ngates+=1
        if c%2==0: nhalv+=1
        if Dn>max(Fraction(1),f)*D: viol+=1
        if Dn==max(Fraction(1),f)*D: tight+=1
        if c%2==0 and Dn>D: kinds[(a,b,c)]=kinds.get((a,b,c),0)+1
        D=Dn
print("random circuits: %d gates, %d of them halvings (even common factor); violations of D_new <= max(1,(|a|+|b|)/c) D_old: %d; gates where the bound is attained: %d"%(ngates,nhalv,viol,tight))
print("halvings after which the largest minor grew (coefficients a, b, common factor c: count):",kinds)
