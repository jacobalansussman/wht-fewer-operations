# i-represent: small exact checks. All values are dyadic Gaussian rationals with tiny exponents,
# so Python complex/float arithmetic is exact here; integer parts use Python ints.
import itertools, math
from math import comb, log2
def wt(v): return bin(v).count("1")
def Hm(k):
    N=1<<k; return [[(-1)**wt(y&z) for z in range(N)] for y in range(N)]
def mul(A,B):
    n=len(A); m=len(B[0]); l=len(B)
    return [[sum(A[i][t]*B[t][j] for t in range(l)) for j in range(m)] for i in range(n)]

print("== 1. H_4 in 7 gates (gate = a*u+b*v) and H_4 as ONE diffusion I - J/2")
H4=Hm(2); ok=True
for x in itertools.product([1,2,5,11,-7,3],repeat=4):
    x0,x1,x2,x3=x
    g1=x1+x2; g2=g1+x3; g3=x0+g2; g4=x0-g2; g5=g4+2*x2; g6=g4+2*x1; g7=g4+2*x3
    want=[sum(H4[r][c]*x[c] for c in range(4)) for r in range(4)]
    ok&= ([g3,g5,g6,g7]==want)
print("   7-gate circuit equals H_4 on 1296 integer inputs:",ok)
G=[[ (1 if i==j else 0)-0.5 for j in range(4)] for i in range(4)]
GG=mul(G,G); print("   G=I-J/2: entries",sorted(set(v for r in G for v in r)),"G*G=I:",all(abs(GG[i][j]-(i==j))==0 for i in range(4) for j in range(4)))
for d in (8,16):
    for c in (2,d/2):
        F=[[(1 if i==j else 0)-c/d for j in range(d)] for i in range(d)]
        print("   I-(%g/%d)J on %d points: entry set"%(c,d,d),sorted(set(v for r in F for v in r)),"eigs: 1 (x%d),"%(d-1),1-c)

print("== 2. C^{(x)k} = R*Q, R on antipodal pairs, Q real, flat, depends on distance mod 4")
for k in (4,6):
    N=1<<k; al=(1+1j)/2
    C=[[al**k*(-1j)**wt(y^z) for z in range(N)] for y in range(N)]
    full=N-1
    Rinv=[[((1-1j)/2 if y==z else 0)+((1+1j)/2 if y==(z^full) else 0) for z in range(N)] for y in range(N)]
    Q=mul(Rinv,C)
    real=all(q.imag==0 for r in Q for q in r)
    byd={}
    for y in range(N):
        for z in range(N): byd.setdefault(wt(y^z),set()).add(Q[y][z].real*2**(k/2))
    Q2=mul(Q,Q); refl=all(abs(Q2[i][j]-(i==j))<1e-12 for i in range(N) for j in range(N))
    tr=sum(Q[i][i].real for i in range(N))
    print("   k=%d: Q real:%s  Q^2=I:%s  trace=%g  sqrt(N)*Q by distance:"%(k,real,refl,tr),{d:sorted(s) for d,s in sorted(byd.items())})

print("== 3. Type II code (extended Hamming [8,4,4]): kernel (-i)^d on coset x coset blocks has rank 1")
gens=[0b11110000,0b11001100,0b10101010,0b11111111]
code=set([0])
for g in gens: code|={c^g for c in code}
code=sorted(code); print("   code size",len(code),"weights",sorted(set(wt(c) for c in code)))
reps=[]; seen=set()
for v in range(256):
    if v not in seen:
        reps.append(v); seen|={v^c for c in code}
pw=[1,-1j,-1,1j]
bad=0
for y in reps:
    for z in reps:
        B=[[pw[wt(y^c^z^c2)%4] for c2 in code] for c in code]
        for a in range(16):
            for b in range(16):
                if B[a][b]*B[0][0]!=B[a][0]*B[0][b]: bad+=1
print("   cosets:",len(reps)," blocks:",len(reps)**2," rank-1 violations:",bad)
# contrast: a self-dual code that is NOT doubly even: i2 (+) i2 (+) i2 (+) i2 (repetition pairs)
code2=set([0])
for g in [0b11000000,0b00110000,0b00001100,0b00000011]: code2|={c^g for c in code2}
code2=sorted(code2); B=[[pw[wt(c^c2)%4] for c2 in code2] for c in code2]
bad2=sum(1 for a in range(16) for b in range(16) if B[a][b]*B[0][0]!=B[a][0]*B[0][b])
print("   singly-even self-dual code (pairs): rank-1 violations in the 0-block:",bad2)

print("== 4. Schur-Weyl: H^{(x)k} is a direct sum of Krawtchouk blocks of size k-2j+1, multiplicity C(k,j)-C(k,j-1)")
for k in (4,16,64,256):
    N=2**k; tot=0; a2=0; alog=0; med=0
    for j in range(k//2+1):
        f=comb(k,j)-(comb(k,j-1) if j else 0); b=k-2*j+1
        tot+=f*b; a2+=f*b*b; alog+=f*b*(log2(b) if b>1 else 0)
    assert tot==N
    print("   k=%4d: dense-block work per point = %.2f ; fast-block work per point (log2 b) = %.2f ; textbook = %d"%(k,a2/N,alog/N,k))

print("== 5. entropy of one column after one diffusion I-(c/|D|)J, per addition spent")
for r in (1,2,3,4,5):
    d=2**r
    for c in (2,):
        p0=(1-c/d)**2; p1=(c/d)**2
        ent=(-p0*log2(p0) if p0>0 else 0)-(d-1)*p1*log2(p1)
        cost=(d-1)/d+1
        print("   |D|=%2d c=2: entropy %.3f bits, adds per point %.3f, bits per add %.3f"%(d,ent,cost,ent/cost))
print("   textbook butterfly: 1 bit, 1 add per point, 1.000")
