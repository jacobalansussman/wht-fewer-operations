# second.py (ab-7): exact whole numbers.
# A. the carry law: P = Z (I + 2 G) modulo 4, G = sum over i >= 1 of "row t (bit i set) takes column t - 2^(i-1)".
# B. size of the correction W = Z^-1 P modulo 2^q, q = 1..5: non-zero entries as a function of N.
# C. the q-Pascal identity  x^(s t) = sum_j [s,j][t,j] x^C(j,2) (x-1)^j [j]!  as polynomials in x, and what it gives at x = -1.
# D. volume of P: log2 of the minor rows N/2.., columns N/4.. of size N/4 (a floor for circuits with bounded coefficients).
# E. the spin matrix K = Sym^(N-1) of [[1,1],[1,-1]] (Krawtchouk): K^2 = 2^(N-1); K against H modulo 4.
from math import comb, log2
from fractions import Fraction
def ones(t): return bin(t).count("1")
def wrow(t,k,N,mod):
    pol=[1]
    for i in range(k):
        if t>>i&1:
            f=[comb(1<<i,j)%mod for j in range((1<<i)+1)]; f[0]=(f[0]-1)%mod
            new=[0]*(len(pol)+len(f)-1)
            for a,x in enumerate(pol):
                if x:
                    for b,y in enumerate(f):
                        if y: new[a+b]=(new[a+b]+x*y)%mod
            pol=new
    return (pol+[0]*N)[:N]
print("A/B. W = Z^-1 P, row t = coefficients of prod over the ones i of t of ((1+y)^(2^i) - 1)")
for k in range(2,8):
    N=1<<k
    rows=[wrow(t,k,N,32) for t in range(N)]
    # carry law
    ok=True
    for t in range(N):
        want=[0]*N; want[t]=1
        for i in range(1,k):
            if t>>i&1: want[t-(1<<(i-1))]=(want[t-(1<<(i-1))]+2)%4
        if [x%4 for x in rows[t]]!=want: ok=False
    nz=[sum(1 for r in rows for x in r if x%(1<<q)) for q in range(1,6)]
    print(f"  N={N}: carry law modulo 4 {'holds' if ok else 'FAILS'}; non-zeros of W modulo 2,4,8,16,32: {nz}; Yates gates (N/2)k = {N*k//2}; N + (k-1)N/2 = {N+(k-1)*N//2}")
print("C. q-Pascal")
def padd(a,b):
    n=max(len(a),len(b)); return [(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(n)]
def pmul(a,b):
    r=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b): r[i+j]+=x*y
    return r
def trim(a):
    a=list(a)
    while len(a)>1 and a[-1]==0: a.pop()
    return a
def ev(a,x): 
    r=0
    for c in reversed(a): r=r*x+c
    return r
N=8
G=[[[0] for t in range(N)] for s in range(N)]
for s in range(N):
    G[s][0]=[1]
    for t in range(1,s+1):
        G[s][t]=trim(padd(G[s-1][t-1] if s>0 else [0], [0]*t+ (G[s-1][t] if s>0 else [0])))
fact=[[1]]
for j in range(1,N): fact.append(pmul(fact[-1],[1]*j))
ok=True
for s in range(N):
    for t in range(N):
        tot=[0]
        for j in range(min(s,t)+1):
            term=pmul(pmul(G[s][j],G[t][j]),fact[j])
            for _ in range(j): term=pmul(term,[-1,1])
            term=[0]*(j*(j-1)//2)+term
            tot=padd(tot,term)
        if trim(tot)!=[0]*(s*t)+[1]: ok=False
print(f"  identity x^(st) = sum_j [s,j][t,j] x^C(j,2) (x-1)^j [j]! for s,t < {N}, as polynomials in x: {'holds' if ok else 'FAILS'}")
Pm=[[ev(G[s][t],-1) for t in range(N)] for s in range(N)]
want=[[comb(s>>1,t>>1)*(1 if (s&1)>=(t&1) else 0) for t in range(N)] for s in range(N)]
print(f"  at x = -1 the q-Pascal matrix is (Pascal of size N/2) tensor [[1,0],[1,1]]: {Pm==want}")
P1=[[ev(G[s][t],1) for t in range(N)] for s in range(N)]
print(f"  at x = 1 it is Pascal: {P1==[[comb(s,t) for t in range(N)] for s in range(N)]}")
# x = i (order 4): Gaussian whole numbers; N = 4: Fourier matrix of Z/4 = L D L^T with L = Z mod (1+i)?
I=1j
L=[[ev(G[s][t],I) for t in range(4)] for s in range(4)]
D=[ev(pmul([0]*(j*(j-1)//2)+[1],fact[j]),I)*(I-1)**j for j in range(4)]
F=[[sum(L[s][j]*D[j]*L[t][j] for j in range(4)) for t in range(4)] for s in range(4)]
print("  at x = i, 4 points: L =",[[f"{int(z.real)}{'+' if z.imag>=0 else '-'}{abs(int(z.imag))}i" for z in r] for r in L])
print("   diagonal:",D,"; L D L^T equals the Fourier matrix i^(st):",all(abs(F[s][t]-I**(s*t))<1e-9 for s in range(4) for t in range(4)))
print("   L modulo (1+i) [a+bi -> (a+b) mod 2]:",[[int(z.real+z.imag)%2 for z in r] for r in L]," = subset sums Z:",[[int(z.real+z.imag)%2 for z in r] for r in L]==[[1 if (s&t)==t else 0 for t in range(4)] for s in range(4)])
print("D. volume of Pascal")
def det(M):
    M=[[Fraction(x) for x in r] for r in M]; n=len(M); d=Fraction(1)
    for c in range(n):
        p=next((i for i in range(c,n) if M[i][c]!=0),None)
        if p is None: return Fraction(0)
        if p!=c: M[c],M[p]=M[p],M[c]; d=-d
        d*=M[c][c]
        for i in range(c+1,n):
            f=M[i][c]/M[c][c]
            if f: M[i]=[a-f*b for a,b in zip(M[i],M[c])]
    return d
for k in range(3,8):
    N=1<<k; n=N//4
    M=[[comb(N//2+i,N//4+j) for j in range(n)] for i in range(n)]
    d=abs(det(M)); lg=(log2(d.numerator>>max(0,d.numerator.bit_length()-60))+max(0,d.numerator.bit_length()-60)-log2(d.denominator)) if d else float('-inf')
    print(f"  N={N}: log2 |minor| = {lg:.1f}; divided by N^2: {lg/N/N:.4f}; (N/2) log2 N = {N*k//2}")
print("E. spin matrix K = Sym^(N-1)[[1,1],[1,-1]] in the basis x^s y^(N-1-s)")
for k in (2,3,4,5):
    N=1<<k; n=N-1
    K=[]
    for u in range(N):
        row=[]
        for s in range(N):
            # coefficient of x^u y^(n-u) in (x+y)^s (x-y)^(n-s)
            row.append(sum(comb(s,a)*comb(n-s,u-a)*(-1)**(n-s-(u-a)) for a in range(0,u+1) if 0<=u-a<=n-s and a<=s))
        K.append(row)
    K2=[[sum(K[a][j]*K[j][b] for j in range(N)) for b in range(N)] for a in range(N)]
    isref=all(K2[a][b]==(2**n if a==b else 0) for a in range(N) for b in range(N))
    H=[[(-1)**ones(s&t) for t in range(N)] for s in range(N)]
    odd=all(x%2 for r in K for x in r)
    # rank mod 2 of (|K| pattern difference): (K - J)/2 mod 2 against (H - J)/2 mod 2
    def rank2(M):
        rows=[sum((x&1)<<j for j,x in enumerate(r)) for r in M]; r=0
        for bit in range(len(M[0])):
            p=next((i for i in range(r,len(rows)) if rows[i]>>bit&1),None)
            if p is None: continue
            rows[r],rows[p]=rows[p],rows[r]
            for i in range(len(rows)):
                if i!=r and rows[i]>>bit&1: rows[i]^=rows[r]
            r+=1
        return r
    rk=rank2([[(x-1)//2 for x in r] for r in K]); rh=rank2([[(x-1)//2 for x in r] for r in H])
    print(f"  N={N}: K^2 = 2^(N-1) I: {isref}; all entries odd: {odd}; largest entry {max(abs(x) for r in K for x in r)}; rank mod 2 of (K-J)/2: {rk}; of (H-J)/2: {rh}")
