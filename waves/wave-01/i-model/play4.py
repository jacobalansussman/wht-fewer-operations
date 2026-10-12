# i-model play 4: slice theorem over a spread.  WHT of length N=q^2 = (q+1 folds onto q numbers) + (q+1 WHTs of length q).  exact integers.
import random, itertools
random.seed(5)
def wht(x):
    x=list(x); n=len(x); h=1
    while h<n:
        for i in range(0,n,2*h):
            for j in range(i,i+h):
                a,b=x[j],x[j+h]; x[j],x[j+h]=a+b,a-b
        h*=2
    return x
def gf_mul(a,b,m,poly):
    r=0
    while b:
        if b&1: r^=a
        b>>=1; a<<=1
        if a>>m: a^=poly
    return r
def dot(u,v): return bin(u&v).count("1")&1
def run(m,poly):
    q=1<<m; N=q*q
    # spread of F_2^{2m}: M_a={(y,a*y)}, M_inf={(0,z)} ; vector (y,z) -> index y + q*z
    spread=[[y+q*gf_mul(a,y,m,poly) for y in range(q)] for a in range(q)]+[[q*z for z in range(q)]]
    cover=sorted(v for M in spread for v in M if v)
    assert cover==list(range(1,N)), "not a spread"
    x=[random.randrange(-99,100) for _ in range(N)]; X=wht(x)
    out=[None]*N; folds=0; small=0; lines=set()
    for M in spread:
        Mperp=[v for v in range(N) if all(dot(v,w)==0 for w in M)]
        # cosets of Mperp, labelled by the vector of dot products with a basis of M
        basis=[]; span={0}
        for w in M:
            if w not in span:
                basis.append(w); span|={s^w for s in span}
        c=[0]*q
        for v in range(N):
            lab=sum(dot(v,b)<<i for i,b in enumerate(basis)); c[lab]+=x[v]
        folds+=N-q
        for lab in range(q): lines.add(frozenset(v for v in range(N) if sum(dot(v,b)<<i for i,b in enumerate(basis))==lab))
        C=wht(c); small+=q*m
        for w in M:
            # coordinates of w in the basis
            for coef in range(q):
                ww=0
                for i,b in enumerate(basis):
                    if (coef>>i)&1: ww^=b
                if ww==w: break
            v=C[coef]
            if out[w] is None: out[w]=v
            else: assert out[w]==v
    return out==X, N, len(lines), folds, small, N*2*m
for m,poly in ((1,0b11),(2,0b111),(3,0b1011),(4,0b10011)):
    ok,N,nl,folds,small,text=run(m,poly)
    print("slice theorem q=%d N=%d: exact=%s ; distinct lines=%d (q^2+q=%d) ; naive fold adds=%d ; small-transform adds=%d ; textbook adds=%d"%(1<<m,N,ok,nl,N+(1<<m),folds,small,text))
