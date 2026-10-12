#!/usr/bin/env python3
"""tower2.py -- exact integers.  The transform in the form Hk = (J - 2I) tensor ... tensor (J - 2I)  (J = 4x4 all ones),
which is the N-point Walsh-Hadamard matrix after relabelling and sign changes (free in count G).  Points are words x in {0..3}^k.
Checks: (1) Hk Hk^T = N I and entry = (-1)^(number of coordinates where x and y agree);
(2) the peel tower: centre = all ones; E = (J - Hk)/2 is the 0/1 matrix 'x and y agree in an odd number of coordinates';
    row weight, pairwise overlap, rank of E, rank of the pieces peeled (sums over flats), row weight left after each peel;
(3) Parseval drain law: for a set L, sum over outputs x of (2|L & E_x| - |L|)^2 = N |L|;
(4) ranks of Hk - s I and Hk + s I (s = sqrt N), and the Gram matrix of the rows of Hk + s I;
(5) 16 points: 29 stored numbers built by 31 gates, every output a combination of 3 (replayed gate by gate)."""
from fractions import Fraction as F
from itertools import product
import random
def rank(M):
    M=[[F(x) for x in r] for r in M]; r=0
    for c in range(len(M[0])):
        p=next((i for i in range(r,len(M)) if M[i][c]!=0),None)
        if p is None: continue
        M[r],M[p]=M[p],M[r]
        for i in range(r+1,len(M)):
            if M[i][c]!=0:
                f=M[i][c]/M[r][c]; M[i]=[a-f*b for a,b in zip(M[i],M[r])]
        r+=1
    return r
for k in (1,2,3):
    W=list(product(range(4),repeat=k)); N=len(W); s=2**k
    agree=lambda x,y: sum(a==b for a,b in zip(x,y))
    H=[[(-1)**agree(x,y) for y in W] for x in W]
    assert all(sum(a*b for a,b in zip(H[i],H[j]))==(N if i==j else 0) for i in range(N) for j in range(N))
    E=[[(1-h)//2 for h in r] for r in H]
    wts=set(sum(r) for r in E); ov=set(sum(a*b for a,b in zip(E[i],E[j])) for i in range(N) for j in range(i))
    print('N',N,': row weight of E',wts,'| overlap of two rows',ov,'| rank E',rank(E))
    # peel by levels: flats fixing a set A of coordinates of x; level j = |A|.  H_x = sum over A of (-2)^|A| * (sum of inputs agreeing with x on A)
    def flatrow(x,A): return [int(all(x[i]==y[i] for i in A)) for y in W]
    from itertools import combinations
    resid=[[h for h in r] for r in H]; forms=[]
    for j in range(0,k+1):
        level=[]
        for A in combinations(range(k),j):
            seen=set()
            for x in W:
                key=tuple(x[i] for i in A)
                if key in seen: continue
                seen.add(key); level.append(flatrow(x,A))
            for xi,x in enumerate(W):
                fr=flatrow(x,A); resid[xi]=[a-(-2)**j*b for a,b in zip(resid[xi],fr)]
        forms+=level
        print('   after peeling level',j,'(%d forms, rank of all forms so far %d): row weight left'%(len(level),rank(forms)),set(sum(1 for v in r if v) for r in resid))
    rnd=random.Random(1)
    for trial in range(5):
        L=rnd.sample(range(N),rnd.randint(1,N)); tot=sum((2*sum(E[x][y] for y in L)-len(L))**2 for x in range(N)); assert tot==N*len(L)
    print('   Parseval drain law sum_x (2|L & E_x| - |L|)^2 = N|L|: holds on 5 random sets')
    I=lambda i,j:int(i==j)
    Mm=[[H[i][j]-s*I(i,j) for j in range(N)] for i in range(N)]; Mp=[[H[i][j]+s*I(i,j) for j in range(N)] for i in range(N)]
    print('   rank(H - %d I) ='%s,rank(Mm),'| rank(H + %d I) ='%s,rank(Mp),'| (N - sqrt N)/2 =',(N-s)//2,'(N + sqrt N)/2 =',(N+s)//2)
# (5) 16 points: stored numbers and gates
W=list(product(range(4),repeat=2)); idx={w:i for i,w in enumerate(W)}; N=16
H=[[(-1)**sum(a==b for a,b in zip(x,y)) for y in W] for x in W]
vec=[[int(i==j) for j in range(N)] for i in range(N)]; gates=0
def g(a,u,b,v):
    global gates; gates+=1; return [a*p+b*q for p,q in zip(u,v)]
R=[]; C=[]
for i in range(4):
    t=g(1,vec[idx[(i,0)]],1,vec[idx[(i,1)]]); t=g(1,t,1,vec[idx[(i,2)]]); R.append(g(1,t,1,vec[idx[(i,3)]]))
for j in range(4):
    t=g(1,vec[idx[(0,j)]],1,vec[idx[(1,j)]]); t=g(1,t,1,vec[idx[(2,j)]]); C.append(g(1,t,1,vec[idx[(3,j)]]))
T=g(1,g(1,g(1,R[0],1,R[1]),1,R[2]),1,R[3])
Pm=[g(1,T,-2,R[i]) for i in range(4)]
stored=16+4+4+1+4+ (2*4+2*4+2)   # inputs, R, C, T, P and the partial sums passed through
ok=all([p-2*c+4*v for p,c,v in zip(Pm[i],C[j],vec[idx[(i,j)]])]==H[idx[(i,j)]] for i in range(4) for j in range(4))
print('16 points: gates so far',gates,'| forms that the read-out uses: 16 inputs + 4 column sums + 4 "total minus twice a row sum" = 24 (29 with the row sums and the total; 47 with every partial sum) | every output = P_i - 2 C_j + 4 x_ij:',ok,'| finishing costs 2 gates per output: total',gates+32)
