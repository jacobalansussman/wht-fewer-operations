# ag-5: replay of the saved families, from the files alone. Whole numbers only (fraction-free elimination).
# For each file: are the three lists partitions of the cube; classes; rank of the incidence matrix; is every monomial of
# degree <= d in its column space (missing = 0); the same for d+1; and the necessary condition of ae-cross as a program:
# the smallest set of outputs that touches fewer classes than it has outputs (exact up to sets of 7).
import ast, sys
from balanced import exact_rank, incid, missing, pc
def hall_small(parts,N,cap):
    rows=[[] for _ in range(N)]
    for i,P in enumerate(parts):
        for j,C in enumerate(P):
            for y in C: rows[y].append((i,j))
    nb={}
    for y in range(N):
        for c in rows[y]: nb.setdefault(c,[]).append(y)
    def rec(S,cls,y0,size_cap):
        if len(cls)<len(S): return True
        if len(S)>=size_cap: return False
        cand=set()
        for c in cls:
            for y in nb[c]:
                if y>y0 and y not in S: cand.add(y)
        for y in sorted(cand):
            new=[c for c in rows[y] if c not in cls]
            if len(cls)+len(new)-len(S)-1 > size_cap-len(S)-1: continue
            S.add(y)
            for c in new: cls.add(c)
            if rec(S,cls,y0,size_cap): return True
            S.discard(y)
            for c in new: cls.discard(c)
        return False
    for size in range(2,cap+1):
        for y0 in range(N):
            if rec({y0},set(rows[y0]),y0,size): return size
    return None
for fn,k,d in (("best_k5_d3_29classes.txt",5,3),("best_k6_d4_61classes.txt",6,4),("k6_d4_62classes.txt",6,4),("best_k7_d5_125classes.txt",7,5)):
    parts=ast.literal_eval(open(fn).read()); N=1<<k
    ok=all(sorted(y for C in P for y in C)==list(range(N)) for P in parts)
    V=sum(len(P) for P in parts)
    r0,m0=missing(parts,k,d); r1,m1=missing(parts,k,d+1)
    D=sum(1 for S in range(N) if pc(S)<=d); h=len(parts)
    lb=-(-(D+h-2)*h*2**d//(h*2**d-1))
    print(fn,"| k",k,"d",d,"helpers",h,"| partitions of the cube:",ok,"| classes",V,"of N",N,"sizes",[len(P) for P in parts],
          "| rank",r0,"| missing at degree d:",m0,"| at d+1:",m1,"| dim RM(d)",D,"rank bound",D+h-1,"ag-5 bound",lb,
          "| class sizes",sorted(set(len(C) for P in parts for C in P)),"| 4-classes that are affine flats (XOR = 0):",sum(1 for P in parts for C in P if len(C)==4 and C[0]^C[1]^C[2]^C[3]==0),"of",sum(1 for P in parts for C in P if len(C)==4),"| pairs along one bit:",sum(1 for P in parts for C in P if len(C)==2 and pc(C[0]^C[1])==1),"of",sum(1 for P in parts for C in P if len(C)==2),"| smallest Hall violator up to 7:",hall_small(parts,N,7))
# the lemma V_h,d(k) <= N/2 + V_(2h-2),d-1(k-1), smallest correctness test: h = 3, d = 3, k = 5 from four partitions of the
# 4-cube good for degree 2 (forget bit 0, forget bit 1, forget bit 2, one class)
k=5; N=32
def cl(f):
    D={}
    for x in range(N): D.setdefault(f(x),[]).append(x)
    return list(D.values())
P1=cl(lambda x:x>>1)
P2=cl(lambda x:(x&1, ((x>>1)&~1) if x&1==0 else ((x>>1)&~4)))
P3=cl(lambda x:(x&1, ((x>>1)&~2) if x&1==0 else 0))
parts=[P1,P2,P3]
print("lemma test (forget a; four partitions of the 4-cube good for degree 2 spread on the two halves): classes",sum(len(P) for P in parts),"degree 3 (rank, missing):",missing(parts,k,3),"degree 4:",missing(parts,k,4))
