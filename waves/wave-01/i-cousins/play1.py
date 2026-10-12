# i-cousins play 1: (1) 2x2 class identities, exact; (2) exhaustive minimum linear circuits at n=4 over GF(5);
# (3) Schur-Weyl block sizes; (4) K_i (x) K_i is diagonal in a Haar basis.
import sys, itertools, math
from fractions import Fraction as F
def mm(A,B): return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def D(a,b): return [[a,0],[0,b]]
H=[[1,1],[1,-1]]; L=[[1,0],[1,1]]; U=[[1,1],[0,1]]
print("(1a) H == L*diag(1,-2)*U :", mm(mm(L,D(1,-2)),U)==H)
# zeta from three Hadamards: H diag(a,b) H diag(c,d) H with (a+b)c=(a-b)d
a,b=F(3,2),F(-1,2); c,d=F(1),F(1,2)   # u=a+b=1, v=a-b=2, uc=1, vd=1
M=mm(mm(mm(mm(H,D(a,b)),H),D(c,d)),H); print("(1b) H D H D H =",[[str(x) for x in r] for r in M],"(one zero => zeta up to free scalings)")
# generic tau: D1 H D2 H D3 has tau=(a+b)^2/(a-b)^2; solve for tau=2? needs sqrt -> over GF(5) instead: squares {1,4}; tau in {2,3} non-squares
print("(1c) tau of H diag(a,b) H is ((a+b)/(a-b))^2: a SQUARE. Non-square tau needs 3 Hadamards or a field extension.")
p=5
def tau(M): return (M[0][0]*M[1][1]*pow(M[0][1]*M[1][0],p-2,p))%p
seen={}
for a in range(1,p):
  for b in range(1,p):
    X=[[ (a+b)%p,(a-b)%p],[(a-b)%p,(a+b)%p]]
    if (a-b)%p and (a+b)%p: seen[tau(X)]=1
print("    GF(5): taus reachable with two Hadamards:",sorted(seen))
# (2) exhaustive search n=4 over GF(5)
n=4
def norm(v):
    for x in v:
        if x%p:
            inv=pow(x,p-2,p); return tuple((y*inv)%p for y in v)
    return None
pts=sorted({norm(v) for v in itertools.product(range(p),repeat=n) if any(v)})
pid={v:i for i,v in enumerate(pts)}
def line(u,v):
    s=set()
    for a in range(p):
        for b in range(p):
            if a or b:
                s.add(pid[norm(tuple((a*x+b*y)%p for x,y in zip(pts[u],pts[v])))])
    return frozenset(s)
LC={}
def L2(u,v):
    k=(u,v) if u<v else (v,u)
    if k not in LC: LC[k]=line(*k)
    return LC[k]
def kron(A,B): return [[(x*y) for x in ra for y in rb] for ra in A for rb in B]
def closure(R,T):
    R=set(R); ch=True
    while ch:
        ch=False
        for t in T:
            if t in R: continue
            Rl=list(R)
            if any(t in L2(Rl[i],Rl[j]) for i in range(len(Rl)) for j in range(i)):
                R.add(t); ch=True
    return frozenset(R)
def mingates(Mat,maxm=4):
    T={pid[norm(tuple(x%p for x in r))] for r in Mat}
    inp=frozenset(pid[norm(tuple(1 if j==i else 0 for j in range(n)))] for i in range(n))
    tnon=len(T-inp)
    start=closure(inp,T)
    if T<=start: return tnon,0
    front={start}
    for m in range(1,maxm+1):
        nf=set()
        for R in front:
            Rl=sorted(R); cand=set()
            for i in range(len(Rl)):
                for j in range(i): cand|=L2(Rl[i],Rl[j])
            for w in cand-R:
                R2=closure(R|{w},T)
                if T<=R2: return tnon+m,m
                nf.add(R2)
        front=nf
        sys.stdout.flush()
    return None,len(front)
Z2=kron(L,L); H2=kron(H,H); G=[[1,1],[1,2]]; G2=kron(G,G)
A2=[[0,1,1,0],[1,0,0,1],[1,0,0,1],[0,1,1,0]]
Haar4=[[1,1,1,1],[1,1,-1,-1],[1,-1,0,0],[0,0,1,-1]]
R1=kron([[1,1],[1,1]],[[1,1],[1,1]])
A2s=[[1,1,1,0],[1,1,0,1],[1,0,1,1],[0,1,1,1]]     # A_2 + I
for name,Mt in [("rank1 J(x)J",R1),("zeta L(x)L",Z2),("Hadamard H(x)H",H2),("generic tau=2 G(x)G",G2),("cube adjacency A_2",A2),("A_2 + I",A2s),("Haar_4",Haar4)]:
    g,m=mingates(Mt,3 if 'gen' in name or 'Had' in name else 4)
    print("(2) n=4 GF(5) min gates  %-22s : %s  (intermediates %s)"%(name,g,m)); sys.stdout.flush()
# (3) Schur-Weyl blocks
for k in (8,16,32,64,128):
    tot=0; s1=F(0); s2=F(0); nb=0
    for j in range(k//2+1):
        mj=math.comb(k,j)-(math.comb(k,j-1) if j else 0); s=k-2*j+1
        tot+=mj*s; nb+=mj; s1+=mj*s*s; s2+=F(mj*s)*F(math.log2(s) if s>1 else 0).limit_denominator(10**6)
    assert tot==2**k
    print("(3) k=%d: blocks %.3g of n, mean block size (dimension-weighted) %.2f, sum m_j s_j log2 s_j / n = %.2f, textbook k=%d"%(k,nb/2**k,float(s1)/2**k,float(s2)/2**k,k))
