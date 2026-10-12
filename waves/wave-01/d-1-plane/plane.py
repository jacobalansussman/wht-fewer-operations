# d-1-plane play 1: the affine plane over F_q inside F_N (N=q^2) in multiplicative (log-polar) coordinates. exact integers / fractions.
import random, itertools, sys
from fractions import Fraction
random.seed(7)
POLY={2:0b111,4:0b10011,6:0b1000011,8:0b100011101}
def field(k):
    N=1<<k; ex=[0]*(2*N); lg=[None]*N; x=1
    for i in range(N-1):
        ex[i]=x; lg[x]=i; x<<=1
        if x>>k: x^=POLY[k]
    assert x==1 and all(lg[v] is not None for v in range(1,N)), "not primitive"
    for i in range(N-1,2*N): ex[i]=ex[i-(N-1)]
    mul=lambda a,b: 0 if (a==0 or b==0) else ex[lg[a]+lg[b]]
    def pw(a,n):
        return 0 if a==0 else ex[(lg[a]*n)%(N-1)]
    return N,ex,lg,mul,pw
def tr(x,k,d,pw):   # trace from F_{2^k} to F_{2^d}
    r=0
    for i in range(k//d): r^=pw(x,(1<<d)**i)
    return r
def rank_and_null(rows):
    m=[[Fraction(v) for v in r] for r in rows]; nr=len(m); nc=len(m[0]); piv=[]; r=0
    for c in range(nc):
        p=next((i for i in range(r,nr) if m[i][c]!=0),None)
        if p is None: continue
        m[r],m[p]=m[p],m[r]; inv=1/m[r][c]; m[r]=[v*inv for v in m[r]]
        for i in range(nr):
            if i!=r and m[i][c]!=0:
                f=m[i][c]; m[i]=[a-f*b for a,b in zip(m[i],m[r])]
        piv.append(c); r+=1
    return r
def polymod(coefs,phi):   # integer poly remainder by monic phi (lists low->high)
    c=list(coefs)
    for i in range(len(c)-1,len(phi)-2,-1):
        f=c[i]
        if f:
            for j,p in enumerate(phi): c[i-(len(phi)-1)+j]-=f*p
    return c[:len(phi)-1]
def cyclo(n,cache={}):
    if n in cache: return cache[n]
    num=[-1]+[0]*(n-1)+[1]
    for d in range(1,n):
        if n%d==0:
            den=cyclo(d); q=[0]*(len(num)-len(den)+1); num=list(num)
            for i in range(len(q)-1,-1,-1):
                q[i]=num[i+len(den)-1]
                for j,p in enumerate(den): num[i+j]-=q[i]*p
            num=q
    cache[n]=num; return num
for k in (2,4,6,8):
    e=k//2; q=1<<e; N,ex,lg,mul,pw=field(k)
    print("==== N=%d q=%d ===="%(N,q))
    Fq=[x for x in range(N) if pw(x,q)==x]; assert len(Fq)==q
    # all lines of the plane F_N over F_q, as frozensets of field elements
    lines=set()
    for d in range(1,N):
        for c in range(N): lines.add(frozenset(c^mul(d,l) for l in Fq))
    assert len(lines)==N+q
    D=sorted(j for j in range(N-1) if tr(ex[j],k,e,pw)==1)
    nonorigin=set(L for L in lines if 0 not in L)
    circ=set(frozenset(ex[(j+i)%(N-1)] for j in D) for i in range(N-1))
    print("lines:",len(lines)," not through origin:",len(nonorigin)," = the N-1 cyclic shifts of one set D of logs:",circ==nonorigin)
    if N<=64: print("D (logs base theta, Tr_{N/q}=1) =",D)
    diff={}
    for a in D:
        for b in D:
            if a!=b: diff[(a-b)%(N-1)]=diff.get((a-b)%(N-1),0)+1
    print("differences: each value once:",set(diff.values())=={1}," missing exactly the multiples of q+1 (the subgroup F_q^*):",sorted(set(range(1,N-1))-set(diff))==[(q+1)*i for i in range(1,q-1)])
    # tower law in the group ring: D_{k/1} = D_{k/e} * D_{e/1}
    Dk1=sorted(j for j in range(N-1) if tr(ex[j],k,1,pw)==1)
    De1=sorted(j for j in range(N-1) if pw(ex[j],q)==ex[j] and tr(ex[j],e,1,pw)==1)
    prod={}
    for a in D:
        for b in De1: prod[(a+b)%(N-1)]=prod.get((a+b)%(N-1),0)+1
    print("tower law  {Tr_{N/2}=1} = {Tr_{N/q}=1} * {s in F_q: Tr_{q/2}(s)=1}  with every coefficient 1:",sorted(prod)==Dk1 and set(prod.values())=={1}," sizes %d = %d * %d"%(len(Dk1),len(D),len(De1)))
    # polar coordinates: log j = alpha*(q+1) + beta*(q-1)
    pol=[]
    for j in D:
        for al in range(q-1):
            be=[b for b in range(q+1) if (al*(q+1)+b*(q-1))%(N-1)==j]
            if be: pol.append((al,be[0]))
    radii=sorted(set(al for al,be in pol)); angs=sorted(be for al,be in pol)
    tr1=sorted(set(lg[s]//(q+1)%(q-1) for s in Fq if s and tr(s,e,1,pw)==1)) if e>1 else [0]
    print("polar: one point of D on each non-trivial angle:",angs==list(range(1,q+1))," ; symmetric under angle -> -angle:",all(((al,(-be)%(q+1)) in pol) for al,be in pol)," ; radii used = trace-one set of F_q:",radii==tr1, " (%d radii)"%len(radii))
    if N<=64: print("  D as (radius log, angle log):",sorted(pol,key=lambda t:t[1]))
    # cyclotomic components of D(t) mod t^(N-1)-1
    Dpoly=[0]*(N-1)
    for j in D: Dpoly[j]=1
    out=[]
    for d in range(1,N):
        if (N-1)%d==0:
            r=polymod(Dpoly,cyclo(d)); nz=[(i,v) for i,v in enumerate(r) if v]
            kind="angular only" if (q+1)%d==0 else ("radial only" if (q-1)%d==0 else "mixed")
            out.append("d=%d[%s]: %d terms%s"%(d,kind,len(nz),(" "+str(nz)) if len(nz)<=4 else ""))
    print("components of D modulo cyclotomic polynomials Phi_d:"); print("   "+" | ".join(out))
    # 16-point: incidence matrix, rank, relations
    if N==16:
        L=sorted(lines,key=lambda s:sorted(s)); R=[[1 if p in l else 0 for p in range(N)] for l in L]
        print("20x16 incidence: rank over Q =",rank_and_null(R)," so relations among the 20 line sums =",len(R)-rank_and_null(R))
        RtR=[[sum(R[l][a]*R[l][b] for l in range(len(R))) for b in range(N)] for a in range(N)]
        print("R^T R = q I + J:",all(RtR[a][b]==(q+1 if a==b else 1) for a in range(N) for b in range(N)))
    # line sums through the transform, exact
    x=[random.randrange(-50,50) for _ in range(N)]
    chi=lambda w,p: -1 if bin(tr(mul(w,p),k,1,pw)).count("1")&1 else 1
    if N<=64:
        X=[sum(chi(w,p)*x[p] for p in range(N)) for w in range(N)]
        ok=True
        for d in set(min(mul(d0,l) for l in Fq if l) for d0 in range(1,N)):
            dinv=pw(d,N-2); cls=[mul(dinv,l) for l in Fq]
            for c in range(N):
                s=sum(chi(w,c)*X[w] for w in cls); ok&=(s%q==0 and s//q==sum(x[c^mul(d,l)] for l in Fq))
        print("line sum over c + d F_q  =  (1/q) sum over w in d^-1 F_q of chi_w(c) X(w):",ok)
    naive=q**3-q
    print("Rad upper bounds: naive folds %d ; through transforms, count O: %d + %d*%d + %d scalings = %d ; count G (16 points = 56): see note"%(naive,N*k,q+1,q*e,N+q,N*k+(q+1)*q*e+N+q))
