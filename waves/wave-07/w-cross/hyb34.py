# w-cross hybrids 3 and 4, exact whole numbers.
import itertools, sys, time
from fractions import Fraction
def pop(x): return bin(x).count("1")

print("== HYBRID 3: ports are the subspaces P with P and P-perp meeting only in 0 ==")
def span(vs):
    S={0}
    for v in vs: S|={s^v for s in S}
    return frozenset(S)
for h in (2,3,4,5,6):
    out=[]
    for r in (1,2,3):
        if r>h-1: continue
        subs=set()
        for vs in itertools.combinations(range(1,1<<h),r):
            S=span(vs)
            if len(S)==1<<r: subs.add(S)
        good=0; coord=0
        for S in subs:
            # radical: elements of S orthogonal to all of S
            rad=[s for s in S if all(pop(s&t)%2==0 for t in S)]
            if len(rad)==1: good+=1
        out.append(f"dim {r}: {good} of {len(subs)} subspaces")
    print(f"h={h}: "+"; ".join(out))
# the split itself at h=3 along p=111: H_8 = (butterfly along p) x (transform on p-perp), as an exact identity of entries
h=3; p=7
perp=[x for x in range(8) if pop(x&p)%2==0]
ok=True
for x in range(8):
    for y in range(8):
        # write x = a*p + u, y = b*p + v with u, v in p-perp
        a=pop(x&p)%2; u=x^(p if a else 0); b=pop(y&p)%2; v=y^(p if b else 0)
        assert u in perp and v in perp
        lhs=1-2*(pop(x&y)%2); rhs=(1-2*(a&b))*(1-2*(pop(u&v)%2))
        ok&=(lhs==rhs)
print("h=3, p=111: H(x,y) = (-1)^(ab) * (-1)^(u.v) with x = a p + u, y = b p + v, u, v even words:", ok)

print()
print("== HYBRID 4: the whole-number diagonalising bases are Z times the automorphisms of the form D ==")
def run(k, ent, maxnz, depth, tlimit):
    N=1<<k
    Z=[[1 if (t&s)==t else 0 for t in range(N)] for s in range(N)]   # Z[s][t] = [t subset of s]
    D=[(-2)**pop(t) for t in range(N)]
    Hm=[[1-2*(pop(x&y)%2) for y in range(N)] for x in range(N)]
    # check Z D Z^T = H
    assert all(sum(Z[x][t]*D[t]*Z[y][t] for t in range(N))==Hm[x][y] for x in range(N) for y in range(N))
    # roots: v with few non-zeros, n = v D v != 0, reflection integral: n | 2 D_t v_t for all t
    roots=[]
    for nz in range(1,maxnz+1):
        for supp in itertools.combinations(range(N),nz):
            for vals in itertools.product([e for e in range(-ent,ent+1) if e!=0],repeat=nz):
                if vals[0]<0: continue
                n=sum(D[t]*a*a for t,a in zip(supp,vals))
                if n==0: continue
                if all((2*D[t]*a)%n==0 for t,a in zip(supp,vals)):
                    from math import gcd
                    g=0
                    for a in vals: g=gcd(g,abs(a))
                    if g==1: roots.append((supp,vals,n))
    def reflect_rows(A,root):
        supp,vals,n=root
        # A -> A * R, R = I - (2/n) D v v^T ... acting on the right so that (A R) D (A R)^T = A D A^T
        # R must satisfy R D R^T = D : R = I - (2/n) v v^T D   (x -> x - 2 (v.Dx)/n v as a column map); use its transpose action on rows
        out=[]
        for row in A:
            c=sum(row[t]*a for t,a in zip(supp,vals))          # row . v
            new=list(row)
            for t in range(N):
                pass
            # row * (I - (2/n) v (D v)^T) = row - (2/n)(row.v) (D v)^T
            for t,a in zip(supp,vals):
                new[t]=row[t]-(2*c*D[t]*a)//n
            out.append(new)
        return out
    def okA(A):
        return all(sum(A[x][t]*D[t]*A[y][t] for t in range(N))==Hm[x][y] for x in range(N) for y in range(N))
    def key(A):
        # up to sign of columns
        cols=list(zip(*A)); nc=[]
        for c in cols:
            f=next((e for e in c if e!=0),1)
            nc.append(tuple(e if f>0 else -e for e in c))
        return tuple(nc)
    def nnz(A): return sum(1 for r in A for e in r if e!=0)
    def hgt(A): return max(abs(e) for r in A for e in r)
    seen={key(Z):Z}; frontier=[Z]; t0=time.time()
    hist={}
    for d in range(1,depth+1):
        nxt=[]
        for A in frontier:
            for root in roots:
                Bm=reflect_rows(A,root)
                kk=key(Bm)
                if kk in seen: continue
                if hgt(Bm)>ent+1: continue
                seen[kk]=Bm; nxt.append(Bm)
            if time.time()-t0>tlimit: break
        frontier=nxt
        if time.time()-t0>tlimit: print("  (time limit; depth",d,"incomplete)"); break
    allok=all(okA(A) for A in list(seen.values())[:2000])
    for A in seen.values():
        hist[nnz(A)]=hist.get(nnz(A),0)+1
    best=min(seen.values(),key=nnz)
    print(f"k={k} N={N}: roots with <= {maxnz} non-zeros and entries <= {ent}: {len(roots)}; bases A = Z*O reached within {depth} reflections: {len(seen)}"
          f"; all satisfy A D A^T = H (first 2000 checked): {allok}")
    print("  non-zeros of Z:",nnz(Z)," histogram of non-zeros (count):",sorted(hist.items())[:12])
    print("  sparsest basis found, rows:",[tuple(r) for r in best])
    return seen
s4=run(2,2,3,4,20)
# does x-8's alternating basis occur?  rows (0,0,0,1),(0,0,1,-1),(0,1,-1,1),(1,-1,0,1), diagonal (1,2,-2,-4) up to order
s8=run(3,2,2,2,150)
