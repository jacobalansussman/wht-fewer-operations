# i-fields: small exact plays. Pure Python, exact rationals / integers.
from fractions import Fraction as Fr
from itertools import permutations, product
from math import comb
import sys

def rank(M):
    M=[[Fr(x) for x in r] for r in M]; r=0; rows=len(M); cols=len(M[0]) if M else 0
    for c in range(cols):
        p=None
        for i in range(r,rows):
            if M[i][c]!=0: p=i;break
        if p is None: continue
        M[r],M[p]=M[p],M[r]
        for i in range(rows):
            if i!=r and M[i][c]!=0:
                f=M[i][c]/M[r][c]; M[i]=[a-f*b for a,b in zip(M[i],M[r])]
        r+=1
    return r
def mul(A,B): return [[sum(a*b for a,b in zip(r,c)) for c in zip(*B)] for r in A]
def T(d): return [[1 if j<=i else 0 for j in range(d)] for i in range(d)]
def had(k): return [[(-1)**bin(y&z).count('1') for z in range(1<<k)] for y in range(1<<k)]

print("== 1. rise of ONE running-sum pass w.r.t. the diagonal of two digit columns (floor note's F)")
for d in range(2,9):
    Td=T(d)
    diag=[[1 if (a==x and b==x) else 0 for a in range(d) for b in range(d)] for x in range(d)]
    img=[[Td[a][x]*Td[b][x] for a in range(d) for b in range(d)] for x in range(d)]
    print(" d=%d  F(running sum)=%d   F(full kernel)=d-1=%d"%(d, rank(diag+img)-d, d-1))

print("== 2. WHT = subset-sum . diag((-2)^|S|) . superset-sum  (k=4, exact)")
k=4;N=1<<k
L=[[1 if (t&s)==t else 0 for t in range(N)] for s in range(N)]      # zeta: sum over subsets t of s
D=[[(-2)**bin(s).count('1') if s==t else 0 for t in range(N)] for s in range(N)]
U=[list(r) for r in zip(*L)]
print(" identity holds:", mul(mul(L,D),U)==had(k))

print("== 3. running-sum length of H_4: is  T P D T  monomially equivalent to a +-1 Hadamard matrix? (h=2)")
vals=[Fr(a,b)*s for a,b in [(1,1),(2,1),(3,1),(1,2),(1,3),(3,2),(2,3),(4,1),(1,4)] for s in (1,-1)]
T4=T(4); hits=0; fullsupp=0; best=None
def monoH(G):
    if any(x==0 for r in G for x in r): return None
    Gn=[[G[i][j]*G[0][0]/(G[i][0]*G[0][j]) for j in range(4)] for i in range(4)]
    return Gn
for P in permutations(range(4)):
    for dv in product(vals,repeat=3):
        Dv=(Fr(1),)+dv
        PD=[[Dv[j] if P[j]==i else 0 for j in range(4)] for i in range(4)]
        G=mul(mul(T4,PD),T4)
        Gn=monoH(G)
        if Gn is None: continue
        fullsupp+=1
        pm=sum(1 for r in Gn for x in r if x in (1,-1))
        if best is None or pm>best[0]: best=(pm,P,Dv,Gn)
        if pm==16 and rank(Gn)==4: hits+=1
print(" full-support products:",fullsupp," Hadamard-equivalent hits:",hits," most +-1 entries after normalising:",best[0],"of 16, at P=",best[1],"D=",[str(x) for x in best[2]])
# also: which T-like single passes? try h=2 with the two passes being T and T^t (lower then upper), any P, D
hits2=0;best2=None
T4t=[list(r) for r in zip(*T4)]
for A,B,name in [(T4,T4t,'T..Tt'),(T4t,T4,'Tt..T')]:
    for P in permutations(range(4)):
        for dv in product(vals,repeat=3):
            Dv=(Fr(1),)+dv
            PD=[[Dv[j] if P[j]==i else 0 for j in range(4)] for i in range(4)]
            Gn=monoH(mul(mul(A,PD),B))
            if Gn is None: continue
            pm=sum(1 for r in Gn for x in r if x in (1,-1))
            if best2 is None or pm>best2[0]: best2=(pm,name,P,[str(x) for x in Dv])
            if pm==16 and rank(Gn)==4: hits2+=1
print(" with one lower and one upper pass: hits",hits2," best",best2)
# d=2 sanity
T2=T(2);T2t=[list(r) for r in zip(*T2)]
print(" d=2: T diag(1,-2) T^t == H_2:", mul(mul(T2,[[1,0],[0,-2]]),T2t)==had(1))

print("== 4. Schur-Weyl: the middle of the WHT in an isotypic basis")
for k in (4,16,64,256,1024):
    tot=0;mid=0;single=0
    for twoj in range(k%2,k+1,2):
        a=(k-twoj)//2
        f=comb(k,a)-(comb(k,a-1) if a>=1 else 0)
        tot+=f*(twoj+1); mid+=f*(twoj+1)**2
        if twoj==0: single=f
    assert tot==1<<k
    print(" k=%4d  dense middle per entry = %.2f   (textbook %d)   sqrt(k)=%.1f   share of entries where the transform is a scalar = %.4f"%(k, mid/tot, k, k**.5, single/tot))
