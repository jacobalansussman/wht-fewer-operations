# w-cross hybrids 1-3, exact whole-number / Gaussian-integer checks. No floats.
import itertools, sys
from fractions import Fraction
from math import comb

def pop(x): return bin(x).count("1")
def H(k): 
    N=1<<k
    return [[1-2*(pop(x&y)&1) for y in range(N)] for x in range(N)]
def matmul(A,B):
    n=len(A); m=len(B[0]); Bt=list(zip(*B))
    return [[sum(a*b for a,b in zip(r,c)) for c in Bt] for r in A]
def transpose(A): return [list(r) for r in zip(*A)]

print("== HYBRID 1: the transform as one function of the neighbour-sum operator ==")
# Gaussian integers as (re,im)
def gmul(a,b): return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])
def gpow_minus_i(d): return [(1,0),(0,-1),(-1,0),(0,1)][d%4]
for k in (2,3,4,5,6):
    N=1<<k
    # product over i of (1 - i X_i) built by k passes, as an N x N Gaussian matrix
    M=[[(1,0) if x==y else (0,0) for y in range(N)] for x in range(N)]
    for i in range(k):
        M2=[[None]*N for _ in range(N)]
        for x in range(N):
            for y in range(N):
                a=M[x][y]; b=M[x^(1<<i)][y]      # (1 - i X_i) M
                M2[x][y]=(a[0]+b[1], a[1]-b[0])   # a - i*b
        M=M2
    ok=all(M[x][y]==gpow_minus_i(pop(x^y)) for x in range(N) for y in range(N))
    # symmetric chirp q(z) = (-1)^C(|z|,2); claim H(x,(J-I)y) = q(x) q(x^y) q(y)   (k even: J-I invertible)
    q=[1-2*(comb(pop(z),2)&1) for z in range(N)]
    def JmI(y):
        par=pop(y)&1; r=0
        for i in range(k):
            bit=(par ^ ((y>>i)&1))
            r|=bit<<i
        return r
    perm=[JmI(y) for y in range(N)]
    bij=len(set(perm))==N
    ok2=all(q[x]*q[x^y]*q[y]==1-2*(pop(x&perm[y])&1) for x in range(N) for y in range(N))
    # the convolution C_q = sum_j q_j A_j as a polynomial in A = A_1: degree of the interpolating polynomial
    # eigenvalue of A on weight w: k-2w ; eigenvalue of C_q: qhat_w = sum_z q(z)(-1)^{y.z}, |y|=w
    qhat=[]
    for w in range(k+1):
        y=(1<<w)-1
        qhat.append(sum(q[z]*(1-2*(pop(y&z)&1)) for z in range(N)))
    # divided differences on nodes k-2w
    xs=[k-2*w for w in range(k+1)]; dd=[Fraction(v) for v in qhat]; deg=0
    coeffs=[dd[0]]
    for j in range(1,k+1):
        dd=[(dd[i+1]-dd[i])/(xs[i+j]-xs[i]) for i in range(len(dd)-1)]
        coeffs.append(dd[0])
    deg=max(j for j,c in enumerate(coeffs) if c!=0)
    print(f"k={k} N={N}: prod(1 - i X_j) == (-i)^distance: {ok};  J-I a bijection: {bij};  H(x,(J-I)y)=q(x)q(x+y)q(y): {ok2};"
          f"  spectrum of C_q by weight: {qhat};  degree of C_q as a polynomial in A: {deg} (of at most {k})")

print()
print("== HYBRID 2: a diagonalising basis that costs half a transform (plus N/2) ==")
def kron(A,B):
    return [[a*b for a in ra for b in rb] for ra in A for rb in B]
for k in (2,4,6):
    N=1<<k; h=k//2; s=1<<h
    Hs=H(h); I=[[1 if i==j else 0 for j in range(s)] for i in range(s)]
    # paired transform H'(x,y) = (-1)^(a.b' + b.a'), x=(a,b): the plain transform with the two halves of the output address exchanged
    def sw(y): return ((y & (s-1))<<h) | (y>>h)
    Hp=[[1-2*(pop(x&sw(y))&1) for y in range(N)] for x in range(N)]
    F=kron(Hs,I)     # transform on the high half of the bits only
    # B: for a<b rows e_(a,b)+e_(b,a) and e_(a,b)-e_(b,a); for a=b row e_(a,a)
    B=[]; nb=0
    for a in range(s):
        for b in range(s):
            if a==b:
                r=[0]*N; r[(a<<h)|b]=1; B.append(r)
            elif a<b:
                r=[0]*N; r[(a<<h)|b]=1; r[(b<<h)|a]=1; B.append(r)
                r=[0]*N; r[(a<<h)|b]=1; r[(b<<h)|a]=-1; B.append(r); nb+=1
    V=matmul(B,F)
    G=matmul(matmul(V,Hp),transpose(V))
    diag=all(G[i][j]==0 for i in range(N) for j in range(N) if i!=j)
    vals=sorted(set(G[i][i] for i in range(N)))
    # V^T D^-1 V == H' * const ?
    # check: V^T diag(1/G_ii) V * (something) = inverse... use: H' = V^-1 G V^-T; verify V^T X V = c H' with X=diag(G_ii^-1)*?
    VT=transpose(V)
    X=[[Fraction(1,G[i][i]) if i==j else 0 for j in range(N)] for i in range(N)]
    R=matmul(matmul(VT,X),V)
    # R should be the inverse of H' up to... H'^-1 = H'/N
    okr=all(R[i][j]*N==Hp[i][j] for i in range(N) for j in range(N))
    print(f"N={N}: V = (butterflies on exchanged pairs)(half transform);  V H' V^T diagonal: {diag}, values {vals};"
          f"  H' = N V^T diag^-1 V: {okr};  pair gates: 2 x {nb}")
