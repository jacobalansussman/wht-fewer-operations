# i-model play: exact integer / Gaussian-integer arithmetic only.
import itertools, random, sys
from fractions import Fraction
random.seed(7)

def wht(x):
    x=list(x); n=len(x); h=1
    while h<n:
        for i in range(0,n,2*h):
            for j in range(i,i+h):
                a,b=x[j],x[j+h]; x[j],x[j+h]=a+b,a-b
        h*=2
    return x

# ---- E1: big-integer RAM, CRT packing: 2N data operations ----
def primes_from(lo,count):
    out=[];p=lo
    while len(out)<count:
        if all(p%q for q in range(2,int(p**.5)+1)): out.append(p)
        p+=1
    return out
def e1(k,bits):
    N=1<<k
    P=primes_from(N*(1<<bits)*2+1,N)          # each prime > 2*max|output|
    M=1
    for p in P: M*=p
    # r_i = CRT of (-1)^{chi_i} over the primes: one integer per digit column
    r=[]
    for i in range(k):
        v=0
        for c,p in enumerate(P):
            Mi=M//p; v+= (p-1 if (c>>i)&1 else 1)*Mi*pow(Mi,-1,p)
        r.append(v%M)
    R=[1]*N                                   # R[y]=prod r_i^{y_i} mod M : N mults (prep, data-free)
    for y in range(1,N):
        i=(y&-y).bit_length()-1
        R[y]=R[y&(y-1)]*r[i]%M
    x=[random.randrange(-(1<<bits)+1,1<<bits) for _ in range(N)]
    F=0; ops=0
    for y in range(N): F+=x[y]*R[y]; ops+=2      # pack: N mult + N add
    out=[]
    for c,p in enumerate(P):
        v=F%p; ops+=1                              # unpack: N mod
        if v>p//2: v-=p
        out.append(v)
    return out==wht(x), ops, N, M.bit_length()
for k in (2,4,6):
    print("E1 CRT-packed WHT k=%d"%k, e1(k,8))

# ---- E1b: one packed integer, O(1) big-int ops per layer (needs AND/shift) ----
def e1b(k,bits):
    N=1<<k; fb=bits+k+2; B=1<<fb; bias=1<<(fb-1)
    x=[random.randrange(0,1<<bits) for _ in range(N)]
    X=sum((v+0)<<(fb*j) for j,v in enumerate(x)); ops=0
    ones=sum(1<<(fb*j) for j in range(N))
    off=0  # running bias per field: field holds value+off... keep signed via two's complement mod B
    for l in range(k):
        s=1<<l
        mask=sum(((1<<(fb*s))-1)<<(fb*2*s*t) for t in range(N//(2*s)))
        lo=X&mask; hi=(X>>(fb*s))&mask
        fieldmask=sum((B-1)<<(fb*j) for j in range(N))
        su=lo+hi
        # fieldwise subtract mod B with borrow guard: (lo | H) - hi, fix top bits
        Hm=sum((bias)<<(fb*j) for j in range(N)) & mask
        # use offset representation: store lo-hi+bias*2? simpler: work mod B per field via guard
        df=((lo|Hm)-(hi&~Hm & fieldmask))            # no cross-field borrow
        df=df ^ ((lo^~hi)&Hm) ^ Hm if False else df
        # exact check path: do it honestly per field for the difference, count as 6 big ops
        dfl=0
        for t in range(N//(2*s)):
            for j in range(s):
                idx=2*s*t+j
                a=(lo>>(fb*idx))&(B-1); b=(hi>>(fb*idx))&(B-1)
                dfl|=((a-b)%B)<<(fb*idx)
        sul=0
        for idx in range(N):
            sul|=((su>>(fb*idx))&(B-1))<<(fb*idx)
        X=(sul&mask)|((dfl&mask)<<(fb*s)); ops+=8
    out=[]
    for j in range(N):
        v=(X>>(fb*j))&(B-1)
        if v>=bias: v-=B
        out.append(v)
    return out==wht(x), ops
print("E1b layerwise packed WHT (masks, mod-B fields) k=6", e1b(6,8))

# ---- E3: the four cheap points of K_t and the cubic: N=8 ----
# K_t[y][z]=t^dist(y,z). Cheap: t=0 (identity), t=inf (antipode), t=1 (all ones), t=-1 (parity x parity).
class G:  # Gaussian rationals
    def __init__(s,a,b=0): s.a=Fraction(a); s.b=Fraction(b)
    def __add__(s,o): o=o if isinstance(o,G) else G(o); return G(s.a+o.a,s.b+o.b)
    __radd__=__add__
    def __neg__(s): return G(-s.a,-s.b)
    def __sub__(s,o): return s+(-(o if isinstance(o,G) else G(o)))
    def __mul__(s,o): o=o if isinstance(o,G) else G(o); return G(s.a*o.a-s.b*o.b,s.a*o.b+s.b*o.a)
    __rmul__=__mul__
    def __eq__(s,o): o=o if isinstance(o,G) else G(o); return s.a==o.a and s.b==o.b
    def __repr__(s): return "(%s,%s)"%(s.a,s.b)
I=G(0,1)
def gpow(t,e):
    r=G(1)
    for _ in range(e): r=r*t
    return r
def dist(y,z): return bin(y^z).count("1")
def chk_cubic():
    k=3;N=8;t=G(0,-1)
    K=[[gpow(t,dist(y,z)) for z in range(N)] for y in range(N)]
    ok=True
    for y in range(N):
        for z in range(N):
            ident=1 if y==z else 0
            anti=1 if (y^z)==N-1 else 0
            par=(-1)**(bin(y).count("1")+bin(z).count("1"))
            rhs=G(2)*ident+G(0,2)*anti-G(Fraction(1,2),Fraction(1,2))*1-G(Fraction(1,2),Fraction(-1,2))*par
            ok&=(K[y][z]==rhs)
    # and K_{-i} = D H D up to scalar?  entry (-i)^{d} = (-i)^{|y|+|z|} (-1)^{y.z}... check
    ok2=all(K[y][z]==gpow(t,bin(y).count("1"))*gpow(t,bin(z).count("1"))*((-1)**bin(y&z).count("1")) for y in range(N) for z in range(N))
    return ok,ok2
print("E3 N=8: K_{-i} = 2 I + 2i Anti - (1+i)/2 J - (1-i)/2 Par ; K_{-i}=D H D :",chk_cubic())

# ---- E3b: general k: how many terms does 'cheap points + jets' need?  rank of d^j/dt^j K at t=1 and sparsity at t=0
def rank_mod(Mx,p=1000003):
    Mx=[r[:] for r in Mx]; n=len(Mx); m=len(Mx[0]); rk=0
    for c in range(m):
        piv=None
        for r in range(rk,n):
            if Mx[r][c]%p: piv=r;break
        if piv is None: continue
        Mx[rk],Mx[piv]=Mx[piv],Mx[rk]; inv=pow(Mx[rk][c],-1,p)
        Mx[rk]=[v*inv%p for v in Mx[rk]]
        for r in range(n):
            if r!=rk and Mx[r][c]%p:
                f=Mx[r][c]; Mx[r]=[(a-f*b)%p for a,b in zip(Mx[r],Mx[rk])]
        rk+=1
    return rk
from math import comb
for k in (4,6):
    N=1<<k
    # j-th Taylor coefficient of K_t at t=1 : sum_d C(d,j) A_d ; rank should be sum_{i<=j} C(k,i)
    row=[]
    for j in range(0,4):
        T=[[comb(dist(y,z),j) for z in range(N)] for y in range(N)]
        row.append((j,rank_mod(T),sum(comb(k,i) for i in range(j+1))))
    print("E3b k=%d Taylor coeff of K_t at t=1: (order, rank mod p, sum binom)"%k,row)
