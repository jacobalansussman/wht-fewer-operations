# lemma_own.py [b-1]  exact rationals.  My own check of the two steps of the clique lemma's proof.
# Model: R arrays, the first W live.  Word = g_0 D_1 g_1 ... D_k g_k ; D_i = sign change of array l_i, switched on when the hidden form selects block i.
# Step 1 (identity, any word):  live(word_A) = live(G) - 2 U_A (1 + 2 C_A)^(-1) W_A^T   for every subset A of blocks.
# Step 2 (tight sets): build words in which a chosen W-subset A gives live part -1 by SOLVING for the last constant, with scratch arrays
#   and generic (non-commuting, non-diagonal) constants in between; check w_i.u_i = 1 and w_i.u_j = 0 (i after j) on A.
import random, itertools
from fractions import Fraction as F
random.seed(11)
def mm(A,B): return [[sum(a*b for a,b in zip(r,c)) for c in zip(*B)] for r in A]
def I(n): return [[F(i==j) for j in range(n)] for i in range(n)]
def inv(A):
    n=len(A); M=[r[:]+e for r,e in zip(A,I(n))]
    for c in range(n):
        p=[r for r in range(c,n) if M[r][c]!=0]
        if not p: return None
        M[c],M[p[0]]=M[p[0]],M[c]; x=M[c][c]; M[c]=[v/x for v in M[c]]
        for r in range(n):
            if r!=c and M[r][c]!=0: f=M[r][c]; M[r]=[a-f*b for a,b in zip(M[r],M[c])]
    return [r[n:] for r in M]
def rnd(n):
    while True:
        A=[[F(random.randint(-3,3)) for _ in range(n)] for _ in range(n)]
        if inv(A): return A
def word(g,l,A,R):
    P=I(R)
    for i in range(len(g)):
        P=mm(P,g[i])
        if i<len(l) and i in A: P=[[-v if c==l[i] else v for c,v in enumerate(r)] for r in P]
    return P
def uwc(g,l,R,W):
    k=len(l); pre=[I(R)]
    for x in g: pre.append(mm(pre[-1],x))           # pre[i+1] = g_0..g_i
    suf=[I(R)]
    for x in reversed(g): suf.append(mm(x,suf[-1]))  # suf[j] = product of the last j constants
    U=[[pre[i+1][a][l[i]] for a in range(W)] for i in range(k)]
    Wt=[[suf[k-i][l[i]][b] for b in range(W)] for i in range(k)]
    def between(i,j):
        P=I(R)
        for x in g[i+1:j+1]: P=mm(P,x)
        return P[l[i]][l[j]]
    C=[[between(i,j) if i<j else F(0) for j in range(k)] for i in range(k)]
    return U,Wt,C,pre[-1]
cases=bad=0
for trial in range(60):
    R=random.choice([2,3,4,5]); W=random.randint(1,R); k=random.randint(1,7)
    g=[rnd(R) for _ in range(k+1)]; l=[random.randrange(R) for _ in range(k)]
    U,Wt,C,G=uwc(g,l,R,W)
    for r in range(k+1):
        for A in itertools.combinations(range(k),r):
            live=[row[:W] for row in word(g,l,set(A),R)[:W]]
            if A:
                Mi=inv([[F(a==b)+2*C[i][j] for b,j in enumerate(A)] for a,i in enumerate(A)])
                corr=mm(mm([[U[i][a] for i in A] for a in range(W)],Mi),[Wt[i] for i in A])
            else: corr=[[F(0)]*W for _ in range(W)]
            pred=[[G[a][b]-2*corr[a][b] for b in range(W)] for a in range(W)]
            cases+=1; bad+=(pred!=live)
print("step 1: identity checked on %d (word, subset) cases with scratch arrays; wrong in %d"%(cases,bad))
# Step 2: words with live(G)=1 and a tight subset A (|A| = W) giving live part -1, constants generic.
built=viol=0
for trial in range(4000):
    W=random.choice([2,3]); S=random.choice([0,1,2]); R=W+S; k=W
    g=[rnd(R) for _ in range(k)]; l=[random.randrange(R) for _ in range(k)]
    # choose the last constant g_k so that BOTH live(G) = 1 and live(word with all blocks on) = -1 : 2*W*W linear conditions on R*R unknowns (row space)
    X=word(g+[I(R)],l,set(),R); Y=word(g+[I(R)],l,set(range(k)),R)
    # need (X gk)[:W,:W] = 1 and (Y gk)[:W,:W] = -1 ; unknown first W columns of gk, column by column: [X_live; Y_live] c_b = [e_b; -e_b]
    rows=[X[a] for a in range(W)]+[Y[a] for a in range(W)]
    if 2*W>R:  # overdetermined unless rows are dependent: skip unless consistent
        pass
    # solve by least structure: pick R unknowns, Gaussian elimination per column
    def solve(Arows,b):
        n=len(Arows[0]); M=[r[:]+[v] for r,v in zip(Arows,b)]; piv=[]; r0=0
        for c in range(n):
            p=[r for r in range(r0,len(M)) if M[r][c]!=0]
            if not p: continue
            M[r0],M[p[0]]=M[p[0]],M[r0]; x=M[r0][c]; M[r0]=[v/x for v in M[r0]]
            for r in range(len(M)):
                if r!=r0 and M[r][c]!=0: f=M[r][c]; M[r]=[a-f*bb for a,bb in zip(M[r],M[r0])]
            piv.append(c); r0+=1
        if any(all(v==0 for v in M[r][:-1]) and M[r][-1]!=0 for r in range(len(M))): return None
        x=[F(random.randint(-2,2)) for _ in range(n)]          # free unknowns random
        for r,c in enumerate(piv): x[c]=M[r][-1]-sum(M[r][j]*x[j] for j in range(n) if j!=c and j not in piv)
        return x
    cols=[]
    for b in range(W):
        c=solve(rows,[F(a==b) for a in range(W)]+[-F(a==b) for a in range(W)])
        if c is None: break
        cols.append(c)
    if len(cols)<W: continue
    gk=[[cols[b][r] if b<W else F(random.randint(-2,2)) for b in range(R)] for r in range(R)]
    gg=g+[gk]
    if [r[:W] for r in word(gg,l,set(),R)[:W]]!=I(W): continue
    if [r[:W] for r in word(gg,l,set(range(k)),R)[:W]]!=[[-v for v in r] for r in I(W)]: continue
    built+=1
    U,Wt,C,G=uwc(gg,l,R,W)
    for i in range(k):
        for j in range(k):
            d=sum(Wt[i][t]*U[j][t] for t in range(W))
            if (i==j and d!=1) or (i>j and d!=0) or (i<j and d!=2*C[i][j]): viol+=1
print("step 2: %d words built with a tight set (live part +1 with all signs off, -1 with W signs on; generic constants, 0 to 2 scratch arrays); pattern w_i.u_j = [i=j] + 2c_ij (i<j), 0 (i>j) violated in %d entries"%(built,viol))
