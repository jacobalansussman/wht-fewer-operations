# e2-1-dictionary / tiling.py : a splitting A + V of the 6-bit addresses, |A| = |V| = 8, neither set periodic (exact, tiny).
import itertools
e=[1<<i for i in range(6)]   # e[0]=e1 ... e[5]=e6
def span(gs):
    S={0}
    for g in gs: S|={s^g for s in S}
    return S
V=sorted(span([e[3],e[4]]) | {e[5]^x for x in span([e[3]^e[0], e[4]^e[1]])})
A=sorted({e[3],e[3]^e[0]} | {e[1],e[1]^e[0]} | {e[2]^e[4],e[2]^e[1]^e[4]} | {e[2]^e[0],e[2]^e[0]^e[1]})
sums=sorted(a^v for a in A for v in V)
print("A =",A); print("V =",V)
print("every address a+v exactly once:",sums==list(range(64)))
def periods(S): return [g for g in range(1,64) if {s^g for s in S}==set(S)]
print("periods of A:",periods(A)," periods of V:",periods(V))
def rank(vs):
    b=[]
    for v in vs:
        for x in b: v=min(v,v^x)
        if v: b.append(v)
    return len(b)
print("dimension of the affine span: A",rank([a^A[0] for a in A])," V",rank([v^V[0] for v in V]))
def par(x): return bin(x).count("1")&1
for name,S in (("A",A),("V",V)):
    rows=set()
    for y in range(64):
        r=tuple((-1)**par(y&s) for s in S)
        if r[0]<0: r=tuple(-t for t in r)
        rows.add(r)
    # rank over Q of the distinct rows is at most 8; count them
    print(f"distinct rows up to sign of H restricted to the columns in {name}: {len(rows)} (a subgroup of order 8 would give 8)")
# how many (y-class) pairs: the output y needs row_A(y) (x) row_V(y); count distinct pairs
pairs={(tuple((-1)**par(y&s) for s in A),tuple((-1)**par(y&s) for s in V)) for y in range(64)}
print("distinct (row on A, row on V) pairs:",len(pairs))
# exhaustive small census: are ALL tilings of 5-bit addresses by |A|=4,|V|=8 periodic in one factor?  (Hajos property of Z_2^5, from memory)  -- sampled check only
import random
random.seed(1)
def is_tiling(A,V,n): return len({a^v for a in A for v in V})==len(A)*len(V)==1<<n
cnt=0; nonper=0
for _ in range(200000):
    A4=[0]+random.sample(range(1,32),3)
    # complete greedily to a tiling: V must be a transversal-like set; brute force is too slow, so test only translates structure: skip
    break
