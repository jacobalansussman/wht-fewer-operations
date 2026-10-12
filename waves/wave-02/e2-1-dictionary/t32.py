# e2-1-dictionary / t32.py : 32 points, extraspecial plus type. ALL 496 dictionaries that differ from the affine one by a single transposition:
# non-zeros of the bridge (affine: 80), and the rank of (bridge - affine bridge)  [derived: H P_tau H^-1 = I - h h^T / N is a rank-one change].
import itertools
from fractions import Fraction
from collections import Counter
exec(open("b32.py").read().split("random.seed(7)")[0])
ident=[addr(a,b,c) for (a,b,c) in G]
B0=bridge(ident)
def rank(M):
    M=[[Fraction(v) for v in r] for r in M]; rk=0
    for c in range(len(M[0])):
        p=next((i for i in range(rk,len(M)) if M[i][c]),None)
        if p is None: continue
        M[rk],M[p]=M[p],M[rk]
        for i in range(rk+1,len(M)):
            if M[i][c]:
                f=M[i][c]/M[rk][c]; M[i]=[a-f*b for a,b in zip(M[i],M[rk])]
        rk+=1
    return rk
seen=Counter(); rks=Counter()
for n,(i,j) in enumerate(itertools.combinations(range(32),2)):
    s=ident[:]; s[i],s[j]=s[j],s[i]
    B=bridge(s); nz=sum(1 for r in B for v in r if v); seen[nz]+=1
    if n%25==0: rks[rank([[x-y for x,y in zip(r,r0)] for r,r0 in zip(B,B0)])]+=1
print("all 496 single transpositions of the affine dictionary: non-zeros of the bridge:",sorted(seen.items()),"(affine: 80)")
print("rank of (bridge - affine bridge), 20 of them:",sorted(rks.items()))
