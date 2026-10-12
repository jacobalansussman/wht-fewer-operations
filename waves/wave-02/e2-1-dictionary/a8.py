# e2-1-dictionary / a8.py : 8 points, exact. Every dictionary sigma (all 8! bijections G -> Z_2^3), groups D4 and Q8.
# Bridge up to free column scalings: B'[y][row] = sum_g H[y][sigma(g)] * conj(F[row][g])   (so that B . F . P_sigma = H with B = B' . diag(d/8)).
# Entries are Gaussian integers, held exactly as pairs of Python ints.
import itertools, sys
from collections import Counter, defaultdict
def cm(a,b): return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])
def cadd(a,b): return (a[0]+b[0], a[1]+b[1])
def mm(A,B): return [[ (lambda s: s)(tuple(map(sum, zip(*[cm(A[i][k],B[k][j]) for k in range(2)])))) for j in range(2)] for i in range(2)]
ONE=(1,0); ZERO=(0,0); I=(0,1); MI=(0,-1); M1=(-1,0)
def mpow(M,e):
    R=[[ONE,ZERO],[ZERO,ONE]]
    for _ in range(e): R=mm(R,M)
    return R
def group(name):
    if name=="D4": r=[[ZERO,M1],[ONE,ZERO]]; s=[[ONE,ZERO],[ZERO,M1]]
    else:          r=[[I,ZERO],[ZERO,MI]];  s=[[ZERO,M1],[ONE,ZERO]]
    els=[(a,b) for b in range(2) for a in range(4)]           # g = r^a s^b, index 4*b+a
    rows=[]
    for ea in (1,-1):
        for eb in (1,-1):
            rows.append([((ea**a)*(eb**b),0) for (a,b) in els])
    big=[mm(mpow(r,a),mpow(s,b)) for (a,b) in els]
    for i in range(2):
        for j in range(2):
            rows.append([big[g][i][j] for g in range(8)])
    return rows
Hm=[[(-1)**bin(y&x).count("1") for x in range(8)] for y in range(8)]
P=1000033  # prime, 1 mod 4? check below; used only to make a projective key for a row
assert P%4==1
im=next(t for t in range(2,P) if t*t%P==P-1)
def key_row(row):
    v=[(a+im*b)%P for (a,b) in row]
    f=next((t for t in v if t),None)
    if f is None: return None
    inv=pow(f,P-2,P)
    return tuple(t*inv%P for t in v)
def blocks(B):
    par=list(range(16))
    def f(a):
        while par[a]!=a: par[a]=par[par[a]]; a=par[a]
        return a
    for i in range(8):
        for j in range(8):
            if B[i][j]!=ZERO: par[f(i)]=f(8+j)
    c=Counter(f(i) for i in range(8))
    return tuple(sorted(c.values()))
for name in ("D4","Q8"):
    F=group(name)
    Fc=[[ (a,-b) for (a,b) in row] for row in F]
    classes={}
    stats=Counter()
    for sig in itertools.permutations(range(8)):
        if sig[0]!=0: continue            # translations of the address side are free: fix sigma(identity)=0  (5040 left)
        B=[[ZERO]*8 for _ in range(8)]
        for y in range(8):
            hy=Hm[y]
            for rw in range(8):
                sa=sb=0
                fr=Fc[rw]
                for g in range(8):
                    a,b=fr[g]
                    if hy[sig[g]]>0: sa+=a; sb+=b
                    else: sa-=a; sb-=b
                B[y][rw]=(sa,sb)
        nz=sum(1 for y in range(8) for c in range(8) if B[y][c]!=ZERO)
        rowsup=tuple(sorted(sum(1 for c in range(8) if B[y][c]!=ZERO) for y in range(8)))
        k=frozenset(key_row(B[y]) for y in range(8))
        stats[(nz,blocks(B),rowsup)]+=1
        if k not in classes: classes[k]=(sig,B,nz,blocks(B),rowsup)
    print("==",name,": dictionaries with sigma(e)=0:",sum(stats.values())," distinct bridges up to row order/scale:",len(classes))
    for (nz,bl,rs),c in sorted(stats.items()):
        print("  nonzeros",nz," blocks",bl," row supports",rs," count",c)
    # write representatives per (nz, blocks, rowsup, sorted column supports) coarse class
    coarse={}
    for k,(sig,B,nz,bl,rs) in classes.items():
        cs=tuple(sorted(sum(1 for y in range(8) if B[y][c]!=ZERO) for c in range(8)))
        coarse.setdefault((nz,bl,rs,cs),[]).append((sig,B))
    print("  coarse classes (nonzeros, blocks, row supports, column supports):",len(coarse))
    import json
    out={}
    for idx,(ck,lst) in enumerate(sorted(coarse.items())):
        print("   class",idx,ck," bridges:",len(lst))
        out[idx]={"key":str(ck),"n":len(lst),"reps":[{"sigma":list(s),"B":[[list(e) for e in row] for row in B]} for (s,B) in lst]}
    json.dump(out,open(f"a8_{name}_classes.json","w"))
