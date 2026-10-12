# the first run's test (all normalised entries +-1, rank 4) is NOT "Hadamard": add row orthogonality.
from fractions import Fraction as Fr
from itertools import permutations, product
def mul(A,B): return [[sum(a*b for a,b in zip(r,c)) for c in zip(*B)] for r in A]
def T(d): return [[1 if j<=i else 0 for j in range(d)] for i in range(d)]
vals=[Fr(a,b)*s for a,b in [(1,1),(2,1),(3,1),(1,2),(1,3),(3,2),(2,3),(4,1),(1,4)] for s in (1,-1)]
T4=T(4);T4t=[list(r) for r in zip(*T4)]
def norm(G):
    if any(x==0 for r in G for x in r): return None
    return [[G[i][j]*G[0][0]/(G[i][0]*G[0][j]) for j in range(4)] for i in range(4)]
def orth(Gn): return all(sum(a*b for a,b in zip(Gn[i],Gn[j]))==0 for i in range(4) for j in range(i))
for A,B,name in [(T4,T4,'T.M.T'),(T4,T4t,'T.M.Tt'),(T4t,T4,'Tt.M.T')]:
    pm16=0;had=0;ex=None;maxorth=0
    for P in permutations(range(4)):
        for dv in product(vals,repeat=3):
            Dv=(Fr(1),)+dv
            PD=[[Dv[j] if P[j]==i else 0 for j in range(4)] for i in range(4)]
            Gn=norm(mul(mul(A,PD),B))
            if Gn is None: continue
            if all(x in (1,-1) for r in Gn for x in r):
                pm16+=1
                no=sum(1 for i in range(4) for j in range(i) if sum(a*b for a,b in zip(Gn[i],Gn[j]))==0)
                maxorth=max(maxorth,no)
                if orth(Gn): had+=1; ex=(P,[str(x) for x in Dv])
    print(name,": all-+-1 after normalising:",pm16,"  orthogonal row pairs at best:",maxorth,"of 6   true Hadamard:",had,ex)
# h=3 with passes T, Tt, T and the two middle monomials restricted to signs/2-powers times any permutation
small=[Fr(1),Fr(-1),Fr(2),Fr(-2),Fr(1,2),Fr(-1,2)]
import random
random.seed(1)
perms=list(permutations(range(4)));had3=0;ex3=None;tried=0
for P1 in perms:
    for d1 in product(small,repeat=3):
        PD1=[[((Fr(1),)+d1)[j] if P1[j]==i else 0 for j in range(4)] for i in range(4)]
        X=mul(T4,PD1)
        for _ in range(6):
            P2=random.choice(perms); d2=[random.choice(small) for _ in range(4)]
            PD2=[[d2[j] if P2[j]==i else 0 for j in range(4)] for i in range(4)]
            for B in (T4,T4t):
              for Mid in (T4,T4t):
                Gn=norm(mul(mul(mul(X,Mid),PD2),B)); tried+=1
                if Gn and all(x in (1,-1) for r in Gn for x in r) and orth(Gn): had3+=1; ex3=(P1,[str(x) for x in d1],P2,[str(x) for x in d2],Mid is T4,B is T4)
print("h=3 sample:",tried,"products tried; true Hadamard:",had3,ex3)
