#!/usr/bin/env python3
# i-wild, experiment A and B: "half of the outputs determine the other half".
# H16 = 4(I - 2P), P projector on the (-4)-eigenspace E (dim 8).  For an information set T of E,
# p = P x is known from p_T, and p_rest = Gamma_T p_T.  So  y_rest = 4 x_rest - Gamma_T (4 x_T - y_T).
# A: over all 8-subsets T: nnz(Gamma_T).   B: same for the bent form G = D_f H P_B D_f (eigenspace dim 6).
# Exact rational arithmetic (fractions).
import sys, itertools
from fractions import Fraction as F
k=4; N=16
def dot(a,b): return bin(a&b).count('1')&1
H=[[(-1)**dot(v,w) for w in range(N)] for v in range(N)]
def nullspace(M):
    M=[[F(x) for x in r] for r in M]; n=len(M[0]); piv=[]; r=0
    for c in range(n):
        p=next((i for i in range(r,len(M)) if M[i][c]!=0),None)
        if p is None: continue
        M[r],M[p]=M[p],M[r]; inv=1/M[r][c]; M[r]=[x*inv for x in M[r]]
        for i in range(len(M)):
            if i!=r and M[i][c]!=0:
                f=M[i][c]; M[i]=[a-f*b for a,b in zip(M[i],M[r])]
        piv.append(c); r+=1
    free=[c for c in range(n) if c not in piv]; out=[]
    for fc in free:
        v=[F(0)]*n; v[fc]=F(1)
        for i,pc in enumerate(piv): v[pc]=-M[i][fc]
        out.append(v)
    return out
def systematic(Bas,T):
    d=len(Bas); M=[r[:] for r in Bas]
    for j,c in enumerate(T):
        p=next((i for i in range(j,d) if M[i][c]!=0),None)
        if p is None: return None
        M[j],M[p]=M[p],M[j]; inv=1/M[j][c]; M[j]=[x*inv for x in M[j]]
        for i in range(d):
            if i!=j and M[i][c]!=0:
                f=M[i][c]; M[i]=[a-f*b for a,b in zip(M[i],M[j])]
    return M
def affdim(T):
    t0=T[0]; vs=[t^t0 for t in T[1:]]; basis=[]
    for v in vs:
        for b in basis: v=min(v,v^b)
        if v: basis.append(v)
    return len(basis)
def scan(name,Mat,lam):
    E=nullspace([[Mat[i][j]-(lam if i==j else 0) for j in range(N)] for i in range(N)])
    d=len(E); print(name,"eigenvalue",lam,"eigenspace dim",d)
    hist={}; best=None; bestT=[]; ninfo=0
    for T in itertools.combinations(range(N),d):
        S=systematic(E,T)
        if S is None: continue
        ninfo+=1
        nz=sum(1 for r in S for x in r if x!=0)-d
        hist[nz]=hist.get(nz,0)+1
        if best is None or nz<best: best=nz; bestT=[(T,S)]
        elif nz==best: bestT.append((T,S))
    print(" information sets:",ninfo,"of",sum(1 for _ in itertools.combinations(range(N),d)))
    print(" nnz(Gamma_T) histogram:",sorted(hist.items()))
    print(" min nnz(Gamma_T) =",best,"attained by",len(bestT),"sets; affine-span dims of those T:",
          sorted({affdim(T) for T,_ in bestT}))
    vals=sorted({str(x) for T,S in bestT for r in S for x in r})
    print(" entry values in best Gamma:",vals)
    T,S=bestT[0]; print(" example T =",[format(t,'04b') for t in T])
    for r in S: print("   "," ".join("%2s"%("." if x==0 else ("+" if x==1 else ("-" if x==-1 else str(x)))) for x in r))
    # hyperplane / subspace information sets
    for T,S in bestT[:0]: pass
    sub=[(T,sum(1 for r in systematic(E,T) for x in r if x!=0)-d) for T in itertools.combinations(range(N),d)
         if affdim(T)<=3 and systematic(E,T) is not None]
    print(" T inside an affine 3-space: count",len(sub),"nnz values",sorted({n for _,n in sub}))
    return E,bestT
print("== A: Sylvester H16, eigenvalue -4")
EA,bestA=scan("H16",H,-4)
# bent form
def f(v): return ((v&1)&((v>>1)&1))^(((v>>2)&1)&((v>>3)&1))
G=[[(-1)**f(v^w) for w in range(N)] for v in range(N)]
assert all(G[i][j]==G[j][i] for i in range(N) for j in range(N))
assert all(sum(G[i][t]*G[j][t] for t in range(N))==(16 if i==j else 0) for i in range(N) for j in range(N))
def Bm(w): b=[(w>>i)&1 for i in range(4)]; b=[b[1],b[0],b[3],b[2]]; return sum(b[i]<<i for i in range(4))
# check G = D_f H P_B D_f : G[v][w] = (-1)^f(v) * H[v][B w] * (-1)^f(w)
assert all(G[v][w]==(-1)**f(v)*H[v][Bm(w)]*(-1)**f(w) for v in range(N) for w in range(N))
print("== B: bent form G = D_f H P_B D_f (same matrix up to free signed relabelling), trace",sum(G[i][i] for i in range(N)))
EB,bestB=scan("G16",G,-4)
import pickle
pickle.dump((bestA[:50],bestB[:200]),open(sys.argv[1],"wb"))
