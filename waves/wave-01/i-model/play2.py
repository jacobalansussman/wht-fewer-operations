# i-model play 2: exact integers / Gaussian integers (pairs of ints).
import itertools, random
random.seed(11)
def wht(x):
    x=list(x); n=len(x); h=1
    while h<n:
        for i in range(0,n,2*h):
            for j in range(i,i+h):
                a,b=x[j],x[j+h]; x[j],x[j+h]=a+b,a-b
        h*=2
    return x
# --- E1b fixed: whole array in ONE integer; O(1) big-int ops per layer (and, or, xor, shift, add, sub)
def packed(k,bits):
    N=1<<k; fb=bits+k+2; B=1<<fb
    x=[random.randrange(-(1<<bits)+1,1<<bits) for _ in range(N)]
    X=sum((v%B)<<(fb*j) for j,v in enumerate(x)); ops=0
    Hb=sum(1<<(fb*j+fb-1) for j in range(N)); ALL=(1<<(fb*N))-1
    for l in range(k):
        s=1<<l
        mask=sum(((1<<(fb*s))-1)<<(fb*2*s*t) for t in range(N//(2*s)))   # a constant; (B^N-1)/(B^(2s)-1)*(B^s-1)
        a=X&mask; b=(X>>(fb*s))&mask
        su=((a&~Hb)+(b&~Hb))^((a^b)&Hb)
        df=((a|Hb)-(b&~Hb))^((a^~b)&Hb&ALL)
        X=(su&mask)|((df&mask)<<(fb*s)); ops+=16
    out=[]
    for j in range(N):
        v=(X>>(fb*j))&(B-1); out.append(v-B if v>=B//2 else v)
    return out==wht(x), ops
for k in (4,8,10): print("E1b one-integer WHT k=%d (ok, big-int ops)"%k, packed(k,8))

# --- E4: H_4 ~ 2I-J (Grover diffusion on 4 points) by signed permutations; rank of H_N-equivalent minus sqrt(N) I
def matmul(A,B): return [[sum(a*b for a,b in zip(r,c)) for c in zip(*B)] for r in A]
H2=[[1,1],[1,-1]]
def kron(A,B): return [[a*b for a in ra for b in rb] for ra in A for rb in B]
H4=kron(H2,H2)
G4=[[ (2 if i==j else 0)-1 for j in range(4)] for i in range(4)]
found=None
for p in itertools.permutations(range(4)):
    for sg in itertools.product((1,-1),repeat=4):
        for q in itertools.permutations(range(4)):
            for tg in itertools.product((1,-1),repeat=4):
                M=[[sg[i]*H4[p[i]][q[j]]*tg[j] for j in range(4)] for i in range(4)]
                if M==G4: found=(p,sg,q,tg);break
            if found:break
        if found:break
    if found:break
print("E4 H_4 -> 2I-J via signed row perm (p,sg) and column perm (q,tg):",found)
def rank_mod(Mx,p=1000003):
    Mx=[[v%p for v in r] for r in Mx]; n=len(Mx); m=len(Mx[0]); rk=0
    for c in range(m):
        piv=None
        for r in range(rk,n):
            if Mx[r][c]: piv=r;break
        if piv is None: continue
        Mx[rk],Mx[piv]=Mx[piv],Mx[rk]; inv=pow(Mx[rk][c],-1,p)
        Mx[rk]=[v*inv%p for v in Mx[rk]]
        for r in range(n):
            if r!=rk and Mx[r][c]:
                f=Mx[r][c]; Mx[r]=[(a-f*b)%p for a,b in zip(Mx[r],Mx[rk])]
        rk+=1
    return rk
G=G4
for f in (1,2,3,4):
    N=4**f; s=2**f
    Mm=[[G[i][j]-(s if i==j else 0) for j in range(N)] for i in range(N)]
    Mp=[[G[i][j]+(s if i==j else 0) for j in range(N)] for i in range(N)]
    print("E4 (2I-J)^{x%d}: N=%d rank(G-sqrtN I)=%d rank(G+sqrtN I)=%d  (N-sqrtN)/2=%d"%(f,N,rank_mod(Mm),rank_mod(Mp),(N-s)//2))
    if f<4: G=kron(G,G4)
# Sylvester form itself for comparison
Hs=H4
for f in (1,2,3):
    N=4**f; s=2**f
    Mm=[[Hs[i][j]-(s if i==j else 0) for j in range(N)] for i in range(N)]
    print("   Sylvester H_%d: rank(H-sqrtN I)=%d"%(N,rank_mod(Mm)))
    Hs=kron(Hs,H4)

# --- E5: restricted product rank.  letters in the plane span{Z,X}: Z, X, Z+iX, Z-iX ; target (Z+X)^{xk}
P=1000033  # prime = 1 mod 4 ? need sqrt(-1)
def find_p():
    p=10**9+9
    while True:
        if p%4==1 and all(p%q for q in range(2,40000) if q*q<=p): return p
        p+=2
p=find_p()
# sqrt(-1) mod p
g=2
while pow(g,(p-1)//2,p)!=p-1: g+=1
I_=pow(g,(p-1)//4,p)
letters={'Z':(1,0),'X':(0,1),'P':(1,I_),'M':(1,p-I_)}   # coordinates in basis (Z,X)
def prodvec(word):
    v=[1]
    for ch in word:
        a,b=letters[ch]; v=[(t*a)%p for t in v]+[(t*b)%p for t in v]
    return v
def in_span(vs,t):
    rows=[v[:] for v in vs]; r0=rank_mod(rows,p); r1=rank_mod(rows+[t],p)
    return r0==r1, r0
for k in (2,3):
    words=[''.join(w) for w in itertools.product('ZXPM',repeat=k)]
    vec={w:prodvec(w) for w in words}; t=[1]*(2**k)
    for q in range(1,k+2):
        hits=[]
        for sub in itertools.combinations(words,q):
            ok,r=in_span([vec[w] for w in sub],t)
            if ok and r==q: hits.append(sub)
        print("E5 k=%d q=%d: number of q-subsets of product letters spanning (Z+X)^{x%d} (mod p=%d): %d"%(k,q,k,p,len(hits)), hits[:3])
        if hits: break
