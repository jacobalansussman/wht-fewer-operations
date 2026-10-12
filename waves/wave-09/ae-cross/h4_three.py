# Hybrid 4: three helpers per output. (a) correctness of "degree 3 with three helper classes per point", exact fractions, k = 5, 6.
# (b) the necessary condition for h helpers: Hall's condition on sets of fewer than 2^(d+1) outputs; for two helpers it is the girth.
from fractions import Fraction
from itertools import combinations
def pc(x): return bin(x).count("1")
def rref_rank(rows):
    M=[[Fraction(v) for v in r] for r in rows]; rk=0
    if not M: return 0
    for c in range(len(M[0])):
        piv=None
        for r in range(rk,len(M)):
            if M[r][c]!=0: piv=r;break
        if piv is None: continue
        M[rk],M[piv]=M[piv],M[rk]
        for r in range(rk+1,len(M)):
            if M[r][c]!=0:
                f=M[r][c]/M[rk][c]; M[r]=[a-f*b for a,b in zip(M[r],M[rk])]
        rk+=1
    return rk
def test(k,parts,deg):
    N=1<<k
    cols=[]; ncls=0
    for p in parts:
        lab={}
        for x in range(N): lab.setdefault(p(x),[]).append(x)
        ncls+=len(lab)
        for key,pts in lab.items():
            v=[0]*N
            for x in pts: v[x]=1
            cols.append(v)
    # work with transposed matrices: rank of the class indicators, and rank after adding the monomials
    r0=rref_rank(cols)
    out={}
    for d in range(0,deg+2):
        mons=[[1 if x&S==S else 0 for x in range(N)] for S in range(N) if pc(S)==d]
        out[d]=(rref_rank(cols+mons)==r0)
    return ncls,r0,out
# bits: x = (a, s, rest): bit0 = a (outer selector), bit1 = s (inner selector), bits 2.. = rest
def P1(x): return ('y',x>>1)                                   # forgets a: one class per y
def P2(x): return ('a',x&1,x>>2)                               # for each a: forgets the inner selector s
def P3(x):
    a=x&1; s=x>>1&1; rest=x>>2
    return ('b',a,s,(rest>>1) if s else (rest&1))              # aa-cross's family on y: s=1 forgets bit 2, s=0 keeps only bit 2
for k in (5,6):
    ncls,r0,out=test(k,[P1,P2,P3],3)
    print("k",k,"three helpers: classes",ncls,"of N =",1<<k,"rank",r0,"| every monomial of degree d is a sum of three helper functions:",out)
    ncls,r0,out=test(k,[lambda x:('q',x>>1), P3 if False else (lambda x:('r',x&1, (x>>2) if (x>>1&1) else (x>>1&3)))],2)
# (b) smallest dependent set of outputs (rows) for two helpers against three helpers on the same number of classes, k = 6, random labelled classes
import random
def min_dep(k,h,V,seed,cap=7):
    random.seed(seed); N=1<<k
    rows=[tuple(sorted(random.sample(range(V),h))) for _ in range(N)]
    # smallest set S of rows touching fewer than |S| classes (a forced dependency whatever the weights)
    for s in range(1,cap+1):
        for S in combinations(range(N),s):
            if len(set(c for i in S for c in rows[i]))<s: return s
    return ">%d"%cap
for h in (2,3):
    print("k 6, V = 32 classes, h =",h,": smallest set of outputs with fewer classes than outputs (5 random drawings):",[min_dep(6,h,32,sd,5) for sd in range(5)])
