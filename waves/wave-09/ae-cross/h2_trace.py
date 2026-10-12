# Hybrid 2: free signs and relabelling cannot bring the transform nearer than (N - sqrt N)/2 reflections to the identity.
from itertools import permutations, product
from fractions import Fraction
def pc(x): return bin(x).count("1")
def rank_frac(M):
    M=[[Fraction(v) for v in r] for r in M]; rk=0
    for c in range(len(M[0])):
        piv=None
        for r in range(rk,len(M)):
            if M[r][c]!=0: piv=r;break
        if piv is None: continue
        M[rk],M[piv]=M[piv],M[rk]
        for r in range(len(M)):
            if r!=rk and M[r][c]!=0:
                f=M[r][c]/M[rk][c]; M[r]=[a-f*b for a,b in zip(M[r],M[rk])]
        rk+=1
    return rk
N=4; H=[[(-1)**pc(x&y) for x in range(N)] for y in range(N)]
best={}
for perm in permutations(range(N)):
    for sa in product((1,-1),repeat=N):
        for sb in product((1,-1),repeat=N):
            M=[[sa[y]*H[y][perm[x]]*sb[x] for x in range(N)] for y in range(N)]
            # M/2 is orthogonal; codimension of its fixed space = rank(M - 2I)
            cod=rank_frac([[M[y][x]-(2 if x==y else 0) for x in range(N)] for y in range(N)])
            tr=sum(M[i][i] for i in range(N))
            best[(cod,tr)]=best.get((cod,tr),0)+1
print("4 points, all 24*16*16 =",24*256,"signed relabelled transforms: (codimension of fixed space, trace) -> count")
for key in sorted(best): print("  ",key,best[key])
print("least codimension:",min(c for c,_ in best),"; bound (N - sqrt N)/2 =",(4-2)//2)
# tensor powers of the brick J - 2P at 16 and 64 points
B=[[2*(1 if x==y else 0)-1 for x in range(4)] for y in range(4)]   # 2I - J = -(J - 2P) with P the identity: a signed relabelled H_4 (ad-4)
def kron(A,C): return [[a*c for a in ra for c in rc] for ra in A for rc in C]
M=B
for k,s in ((2,2),(4,4),(6,8)):
    if k>2: M=kron(M,B)
    n=len(M); cod=rank_frac([[M[y][x]-(s if x==y else 0) for x in range(n)] for y in range(n)])
    orth=all(sum(M[i][t]*M[j][t] for t in range(n))==(n if i==j else 0) for i in range(n) for j in range(n))
    print("brick to the power",k//2,": N =",n,"orthogonal up to scale:",orth,"codimension of fixed space",cod,"bound (N - sqrt N)/2 =",(n-s)//2)
