# i-model play 3: is the cyclic DFT of length m^2 a monomial matrix in the Zak basis?  exact, modulo a prime p = 1 mod n
# (identities among n-th roots of unity that hold in Z[zeta] hold mod p; a claimed ZERO entry mod p could be a false zero,
#  so nonzero counts mod p can only undercount; the monomial claim is checked as: exactly one nonzero per row AND matrix invertible.)
def isprime(q):
    if q<2: return False
    i=2
    while i*i<=q:
        if q%i==0: return False
        i+=1
    return True
def setup(n,start=0):
    p=n*(start//n)+n+1
    while not isprime(p): p+=n
    g=2
    while True:
        z=pow(g,(p-1)//n,p)
        if all(pow(z,n//q,p)!=1 for q in range(2,n+1) if n%q==0 and isprime(q)): return p,z
        g+=1
def matmul(A,B,p): 
    Bt=list(zip(*B)); return [[sum(a*b for a,b in zip(r,c))%p for c in Bt] for r in A]
def inv(A,p):
    n=len(A); M=[list(r)+[1 if i==j else 0 for j in range(n)] for i,r in enumerate(A)]
    for c in range(n):
        piv=next(r for r in range(c,n) if M[r][c]%p)
        M[c],M[piv]=M[piv],M[c]; iv=pow(M[c][c],-1,p); M[c]=[v*iv%p for v in M[c]]
        for r in range(n):
            if r!=c and M[r][c]:
                f=M[r][c]; M[r]=[(a-f*b)%p for a,b in zip(M[r],M[c])]
    return [r[n:] for r in M]
import itertools
for m,start in itertools.product((2,3,4,5,6),(0,10**6,10**9)):
    n=m*m; p,z=setup(n,start); w=pow(z,m,p)
    F=[[pow(z,x*y,p) for x in range(n)] for y in range(n)]
    Z=[[0]*n for _ in range(n)]
    for j in range(m):
        for th in range(m):
            for l in range(m):
                Z[j*m+th][j+m*l]=pow(w,(-l*th)%m,p)
    Zi=inv(Z,p); M=matmul(matmul(Z,F,p),Zi,p)
    rows=[sum(1 for v in r if v) for r in M]; cols=[sum(1 for v in c if v) for c in zip(*M)]
    nnzZ=sum(1 for r in Z for v in r if v)
    print("Zak m=%d n=%d p=%d: nonzeros per row of Z F Z^-1: %s ; per column: %s ; nnz(Z)=%d"%(m,n,p,sorted(set(rows)),sorted(set(cols)),nnzZ))
# Bell basis for two bits
H4=[[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]]
B=[[1,0,0,1],[1,0,0,-1],[0,1,1,0],[0,1,-1,0]]
from fractions import Fraction as Fr
def invq(A):
    n=len(A); M=[[Fr(v) for v in r]+[Fr(1 if i==j else 0) for j in range(n)] for i,r in enumerate(A)]
    for c in range(n):
        piv=next(r for r in range(c,n) if M[r][c]!=0); M[c],M[piv]=M[piv],M[c]; iv=1/M[c][c]; M[c]=[v*iv for v in M[c]]
        for r in range(n):
            if r!=c and M[r][c]!=0:
                f=M[r][c]; M[r]=[a-f*b for a,b in zip(M[r],M[c])]
    return [r[n:] for r in M]
Bi=invq(B)
def mm(A,Bm): return [[sum(a*b for a,b in zip(r,c)) for c in zip(*Bm)] for r in A]
print("Bell: B H4 B^-1 =",[[str(v) for v in r] for r in mm(mm(B,H4),Bi)])
