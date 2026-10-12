# Is x-8's second basis (rows (0,0,0,1),(0,0,1,-1),(0,1,-1,1),(1,-1,0,1), diagonal (1,2,-2,-4) up to order) a member of the walked family?
from fractions import Fraction as Fr
import itertools
def pop(x): return bin(x).count("1")
H=[[1-2*(pop(x&y)%2) for y in range(4)] for x in range(4)]
R=[[0,0,0,1],[0,0,1,-1],[0,1,-1,1],[1,-1,0,1]]
def mm(A,B): return [[sum(a*b for a,b in zip(r,c)) for c in zip(*B)] for r in A]
def tr(A): return [list(r) for r in zip(*A)]
def inv(A):
    n=len(A); M=[[Fr(x) for x in r]+[Fr(int(i==j)) for j in range(n)] for i,r in enumerate(A)]
    for c in range(n):
        p=next(r for r in range(c,n) if M[r][c]!=0); M[c],M[p]=M[p],M[c]
        M[c]=[x/M[c][c] for x in M[c]]
        for r in range(n):
            if r!=c and M[r][c]!=0: M[r]=[a-M[r][c]*b for a,b in zip(M[r],M[c])]
    return [r[n:] for r in M]
def isdiag(G): return all(G[i][j]==0 for i in range(4) for j in range(4) if i!=j)
for name,A in (("R",R),("R^T",tr(R)),("R^-1",inv(R)),("R^-T",tr(inv(R)))):
    # (i) A H A^T diagonal?   (ii) A^-1 H A^-T diagonal, i.e. H = A D A^T ?
    G1=mm(mm(A,H),tr(A)); Ai=inv(A); G2=mm(mm(Ai,H),tr(Ai))
    # allow a relabelling of the rows of H as well: try all 24 orders of the addresses on both sides together
    hit=[]
    for perm in itertools.permutations(range(4)):
        Hp=[[H[perm[i]][perm[j]] for j in range(4)] for i in range(4)]
        if isdiag(mm(mm(A,Hp),tr(A))): hit.append(("A H A^T",perm,[mm(mm(A,Hp),tr(A))[i][i] for i in range(4)]))
        if isdiag(mm(mm(Ai,Hp),tr(Ai))): hit.append(("H = A D A^T",perm,[mm(mm(Ai,Hp),tr(Ai))[i][i] for i in range(4)]))
    print(name, "det", "ok", "; hits:", [(h[0],h[1],[str(x) for x in h[2]]) for h in hit[:3]], "number of hits", len(hit))
