# e2-1-dictionary / b32.py : 32 points, exact integers. Extraspecial group of order 32, plus type, elements g=(a,b,c), a,b in Z_2^2, c in Z_2,
# big representation rho(a,b,c) = (-1)^c X^a Z^b (4 x 4, monomial), 16 characters of (a,b).  Group law irrelevant here: only the 32 rows of F matter.
# F rows: 16 characters (-1)^(u.a+v.b)  [c-even], 16 matrix coefficients (i,j): (-1)^c (-1)^(b.j) [a == i^j].
# Bridge up to free column scalings: B'[y][row] = sum_g H[y][sigma(g)] F[row][g].  Recorded: non-zeros per row, block sizes.
import random, itertools
from collections import Counter
def par(x): return bin(x).count("1")&1
G=[(a,b,c) for a in range(4) for b in range(4) for c in range(2)]
F=[]
for u in range(4):
    for v in range(4):
        F.append([(-1)**(par(u&a)^par(v&b)) for (a,b,c) in G])
for i in range(4):
    for j in range(4):
        F.append([ ((-1)**(c^par(b&j)) if a==(i^j) else 0) for (a,b,c) in G])
def addr(a,b,c): return (a<<3)|(b<<1)|c
def bridge(sig):
    B=[]
    for y in range(32):
        hy=[(-1)**par(y&sig[g]) for g in range(32)]
        B.append([sum(h*f for h,f in zip(hy,fr)) for fr in F])
    return B
def blocks(B):
    n=len(B); par_=list(range(2*n))
    def f(a):
        while par_[a]!=a: par_[a]=par_[par_[a]]; a=par_[a]
        return a
    for i in range(n):
        for j in range(n):
            if B[i][j]: par_[f(i)]=f(n+j)
    return sorted(Counter(f(i) for i in range(n)).values())
def report(name,sig):
    assert sorted(sig)==list(range(32))
    B=bridge(sig)
    rs=Counter(sum(1 for v in r if v) for r in B)
    nz=sum(k*v for k,v in rs.items())
    vals=Counter(abs(v) for r in B for v in r if v)
    print(f"{name:58s} nnz {nz:4d}  rows by support {sorted(rs.items())}  blocks {blocks(B)}  |entries| {sorted(vals.items())}")
    return nz
random.seed(7)
ident=[addr(a,b,c) for (a,b,c) in G]
report("1 identity (affine control)",ident)
def q1(a,b): return (a&1)&(b&1)
def q2(a,b): return ((a&1)&(b&1))^((a>>1)&(b>>1))
def q3(a,b): return (a&1)&(a>>1)
def q4(b): return (b&1)&(b>>1)
report("2a central bit += a1*b1",[addr(a,b,c^q1(a,b)) for (a,b,c) in G])
report("2b central bit += a1*b1+a2*b2 (the group's own cocycle)",[addr(a,b,c^q2(a,b)) for (a,b,c) in G])
report("2c central bit += a1*a2",[addr(a,b,c^q3(a,b)) for (a,b,c) in G])
report("2d central bit += b1*b2",[addr(a,b,c^q4(b)) for (a,b,c) in G])
report("2e b1 += a1*a2 (twist of a non-central bit by a)",[addr(a,b^q3(a,b),c) for (a,b,c) in G])
report("2f a1 += b1*b2 (twist of an a bit by b)",[addr(a^q4(b),b,c) for (a,b,c) in G])
report("2g a1 += c*b1 (twist of an a bit by centre x b)",[addr(a^(c&b&1),b,c) for (a,b,c) in G])
# 3. flat-wise affine: on each coset a = a0 of the abelian subgroup {(0,b,c)} use its own invertible linear map of (b,c)
def gl3():
    while True:
        M=[random.randrange(1,8) for _ in range(3)]
        S={0}
        for m in M: S|={s^m for s in S}
        if len(S)==8: return M
def ap(M,x): 
    r=0
    for i in range(3):
        if x>>i&1: r^=M[i]
    return r
for t in range(3):
    Ms=[gl3() for _ in range(4)]
    report(f"3a flat-wise linear, own map of (b,c) on each a-coset  #{t}",[(a<<3)|ap(Ms[a],(b<<1)|c) for (a,b,c) in G])
for t in range(2):
    Ms=[]
    while len(Ms)<4:
        M=gl3()
        if M[0]==1: Ms.append(M)              # keep the central direction: c -> c
    report(f"3b same, but every map fixes the central direction     #{t}",[(a<<3)|ap(Ms[a],(b<<1)|c) for (a,b,c) in G])
# 3c flats in two directions: a in {0,1} -> flats {x4=0, x3=a&1}, a in {2,3} -> flats {x4=1, x2 = a&1}  (bits x4 x3 x2 x1 x0)
def twodir(a,b,c):
    w=(b<<1)|c
    if a<2: return (0<<4)|((a&1)<<3)|w
    lo=w&3; hi=w>>2
    return (1<<4)|(hi<<3)|((a&1)<<2)|lo
report("3c flats in two directions (not a guillotine of one chain)",[twodir(a,b,c) for (a,b,c) in G])
# 4. chain-respecting scrambles
pi=list(range(16)); random.shuffle(pi)
report("4a respects pairs {g, gz}: (a,b) scrambled, c kept",[(pi[(a<<2)|b]<<1)|c for (a,b,c) in G])
sig=[]
for a in range(4):
    p8=list(range(8)); random.shuffle(p8)
    sig+= [ (a<<3)|p8[(b<<1)|c] for b in range(4) for c in range(2)]
report("4b respects a-cosets, arbitrary inside each",sig)
sig=[]
for a in range(4):
    p4=list(range(4)); random.shuffle(p4)
    sig+= [ (a<<3)|(p4[b]<<1)|c for b in range(4) for c in range(2)]
report("4c respects a-cosets and pairs: b permuted inside each",sig)
r=list(range(32)); random.shuffle(r)
report("5 random bijection",r)
# hill-climb: start from identity, swap two addresses, keep if nnz does not go up and bridge changes class (nnz<80 would be news)
best=None
cur=ident[:]; curnz=80; seen=Counter()
for it in range(400):
    i,j=random.sample(range(32),2); s=cur[:]; s[i],s[j]=s[j],s[i]
    B=bridge(s); nz=sum(1 for r_ in B for v in r_ if v); seen[nz]+=1
print("single transpositions applied to the identity dictionary: nnz of the bridge ->",sorted(seen.items()))
