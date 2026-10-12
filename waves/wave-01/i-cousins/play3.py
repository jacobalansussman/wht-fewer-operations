# i-cousins play 3: Grover-diffusion family, monomial-plus-low-rank, entropy per gate. Exact (Fractions) except the entropies (floats, labelled).
from fractions import Fraction as F
import math
def mm(A,B): return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def kron(A,B): return [[x*y for x in ra for y in rb] for ra in A for rb in B]
def rank(M):
    M=[[F(x) for x in r] for r in M]; r=0
    for c in range(len(M[0])):
        pv=next((i for i in range(r,len(M)) if M[i][c]!=0),None)
        if pv is None: continue
        M[r],M[pv]=M[pv],M[r]
        for i in range(len(M)):
            if i!=r and M[i][c]!=0:
                f=M[i][c]/M[r][c]; M[i]=[a-f*b for a,b in zip(M[i],M[r])]
        r+=1
    return r
for d in range(2,10):
    G=[[F(1)-(F(d,2) if i==j else 0) for j in range(d)] for i in range(d)]
    G2=mm(G,G); ok=all(G2[i][j]==(F(d*d,4) if i==j else 0) for i in range(d) for j in range(d))
    flat=len({abs(x) for r in G for x in r})==1
    p=(1-2/d)**2; q=4/d**2
    h=(-p*math.log2(p) if p>0 else 0)-(d-1)*q*math.log2(q)
    gates=2*d-1 if d>2 else 2
    print("d=%d: G_d=J-(d/2)I, G^2=(d^2/4)I %s, flat %s, gates %d, row entropy %.3f bits, bits per gate %.3f"%(d,ok,flat,gates,h,h*d/gates))
R=[[1-(2 if i==j else 0) for j in range(4)] for i in range(4)]
I=lambda n:[[int(i==j) for j in range(n)] for i in range(n)]
S16=kron(R,R); print("rank((J-2I)(x)(J-2I) - 4I) =",rank([[S16[i][j]-4*I(16)[i][j] for j in range(16)] for i in range(16)]),"; (N-sqrtN)/2 =",(16-4)//2)
H=[[1,1],[1,-1]]; H4=kron(H,H); H16=kron(H4,H4)
print("rank(H_4 - 2I) =",rank([[H4[i][j]-2*I(4)[i][j] for j in range(4)] for i in range(4)]),"; rank(H_16 - 4I) =",rank([[H16[i][j]-4*I(16)[i][j] for j in range(16)] for i in range(16)]))
S64=kron(S16,R); print("rank((J-2I)^(x)3 - 8I) =",rank([[S64[i][j]-8*I(64)[i][j] for j in range(64)] for i in range(64)]),"(n=64: trace 64*(-1)^3, so use +8I:)",rank([[S64[i][j]+8*I(64)[i][j] for j in range(64)] for i in range(64)]))
# cost table of the Grover Kronecker family at n = 2^24
n=2**24
for d,k in ((2,24),(4,12),(8,8),(16,6),(64,4),(4096,2)):
    g=(2 if d==2 else 2*d-1)*(n//d)*k
    print("n=2^24 as %d^%d: gates per point %.3f (Hadamard textbook 24)"%(d,k,g/n))
