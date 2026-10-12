# af-2: own checks of ad-4's pair-kill theorem and of ae-cross's 8-gate circuit. Exact integers / fractions only.
import sys, random
from fractions import Fraction as Fr
from itertools import permutations, combinations
def pc(x): return bin(x).count("1")
print("== A. the dichotomy, exhaustively over ALL subspaces (k = 2, 4, 6)")
def subspaces(k):
    N=1<<k; seen={1}; frontier=[1]
    while frontier:
        nxt=[]
        for m in frontier:
            els=[z for z in range(N) if m>>z&1]
            for v in range(1,N):
                if m>>v&1: continue
                m2=m
                for z in els: m2|=1<<(z^v)
                if m2 not in seen: seen.add(m2); nxt.append(m2)
        frontier=nxt
    return sorted(seen)
def Jmap(v,k):   # polar form of z1 z2 + z3 z4 + ... : B(u,v) = parity(u & J v), J swaps the two bits of each pair
    w=0
    for i in range(0,k,2):
        if v>>i&1: w|=1<<(i+1)
        if v>>(i+1)&1: w|=1<<i
    return w
for k in (2,4,6):
    N=1<<k; full=(1<<N)-1
    hyp=[sum(1<<u for u in range(N) if pc(u&Jmap(v,k))%2==0) for v in range(N)]   # hyp[v] = all u with B(u,v)=0
    def perp(m):
        r=full
        for v in range(N):
            if m>>v&1: r&=hyp[v]
        return r
    subs=subspaces(k); U=[perp(m) for m in subs]; UU=[perp(u) for u in U]; VV=U  # perp of V is U; perp of U is UU
    assert all(UU[i]==subs[i] for i in range(len(subs)))                          # double perp = itself (B non-degenerate)
    n=len(subs); point=1; safe_pairs=0; bad=0; nb=[[] for _ in range(n)]
    for i in range(n):
        Vi,Ui=subs[i],U[i]
        for j in range(i,n):
            Vj,Uj=subs[j],U[j]
            # Lemma A applies: both non-characters and U_i not perpendicular to U_j   (computed directly: U_i inside perp(U_j))
            A=(Vi!=full and Vj!=full and (Ui & ~UU[j] & full)!=0)
            # Lemma B applies: both non-points and V_i not perpendicular to V_j
            B=(Vi!=point and Vj!=point and (Vi & ~U[j] & full)!=0)
            safe=not A and not B
            if safe:
                safe_pairs+=1; nb[i].append(j)
                if j!=i: nb[j].append(i)
            if safe!=(Vj==Ui): bad+=1
    tri=0; tri_bad=0; lag=sum(1 for i in range(n) if subs[i]==U[i])
    for i in range(n):
        for j in nb[i]:
            for l in nb[i]:
                if l in nb[j]:
                    tri+=1
                    if not (subs[i]==subs[j]==subs[l]==U[i]): tri_bad+=1
    print(f"k={k}: {n} subspaces; pairs (with repeats) that neither lemma can kill: {safe_pairs}; pairs where 'unkillable' differs from 'V_j = perp V_i': {bad}; "
          f"ordered triples pairwise unkillable: {tri}, of which not 'three copies of one Lagrangian': {tri_bad}; Lagrangians {lag}")
print("== B. Lemma A: every restriction to W = {B(u1,z)=c1, B(u2,z)=c2}, B(u1,u2)=1, is bent quadratic on k-2 bits (k = 4, 6, 8)")
def q(z,k): return sum((z>>i&1)&(z>>(i+1)&1) for i in range(0,k,2))%2
def Bf(u,v,k): return pc(u&Jmap(v,k))%2
def wht(f):
    f=f[:]; n=len(f); h=1
    while h<n:
        for s in range(0,n,2*h):
            for t in range(s,s+h): f[t],f[t+h]=f[t]+f[t+h],f[t]-f[t+h]
        h*=2
    return f
for k in (4,6,8):
    N=1<<k; cnt=0; okc=0
    pairs=[(u1,u2) for u1 in range(1,N) for u2 in range(1,N) if Bf(u1,u2,k)==1]
    if k==8: random.seed(8); pairs=random.sample(pairs,150)
    for (u1,u2) in pairs:
        P=[z for z in range(N) if Bf(u1,z,k)==0 and Bf(u2,z,k)==0]
        # basis of P
        basis=[]; span={0}
        for z in P:
            if z not in span: basis.append(z); span|={s^z for s in span}
        assert len(basis)==k-2
        for c in range(4):
            w0=next(z for z in range(N) if Bf(u1,z,k)==(c&1) and Bf(u2,z,k)==(c>>1))
            f=[]
            for t in range(1<<(k-2)):
                z=w0
                for i,b in enumerate(basis):
                    if t>>i&1: z^=b
                f.append(1-2*q(z,k))
            sp=wht(f); bent=all(abs(v)==1<<((k-2)//2) for v in sp)
            # quadratic: all third derivatives vanish (check on basis directions suffices for a polynomial of the cube)
            ex=[(1-v)//2 for v in f]; quad=True; m=1<<(k-2)
            for a,b2,c2 in combinations(range(k-2),3):
                A,Bb,C=1<<a,1<<b2,1<<c2
                for t in range(m):
                    s=0
                    for sub in range(8):
                        tt=t^(A if sub&1 else 0)^(Bb if sub&2 else 0)^(C if sub&4 else 0); s^=ex[tt]
                    if s: quad=False;break
                if not quad: break
            cnt+=1; okc+=bent and quad
    print(f"k={k}: {len(pairs)} pairs (u1,u2){' (random sample)' if k==8 else ' (all)'} x 4 constants = {cnt} restrictions; bent and quadratic on k-2 bits: {okc}")
print("== C. Lemma B: the transform of a signed flat is a multiple of a signed flat of complementary dimension, direction = ordinary perpendicular (k=4 all 1072; k=6 sample)")
for k,sample in ((4,None),(6,4000)):
    N=1<<k; subs=subspaces(k); random.seed(k); tot=0; ok=0
    jobs=[(m,a,b) for m in subs for a in range(N) for b in range(N)] if sample is None else [(random.choice(subs),random.randrange(N),random.randrange(N)) for _ in range(sample)]
    for (m,a,b) in jobs:
        f=[(1-2*(pc(b&z)%2)) if m>>(z^a)&1 else 0 for z in range(N)]
        F=wht(f); supp=[y for y in range(N) if F[y]]; d=pc(m).bit_length()-1 if False else (bin(m).count("1")).bit_length()-1
        # support must be b + (ordinary perpendicular of V), values +-|V| with a linear sign
        Vels=[z for z in range(N) if m>>z&1]
        perp_ord={y for y in range(N) if all(pc(y&v)%2==0 for v in Vels)}
        good=(set(supp)=={b^y for y in perp_ord}) and all(abs(F[y])==len(Vels) for y in supp)
        if good:
            y0=supp[0]
            good=all(F[y]*F[y0]==len(Vels)**2*(1-2*(pc(a&(y^y0))%2)) for y in supp)
        tot+=1; ok+=good
    print(f"k={k}: {tot} signed flats tested, {ok} transform to a signed flat on b + V^perp with sign (-1)^(a.y)")
for k in (2,4,6,8):
    N=1<<k; g=[1-2*q(z,k) for z in range(N)]; G=wht(g)
    print(f"k={k}: transform of g is 2^(k/2) times a bent quadratic sign pattern:",all(abs(v)==1<<(k//2) for v in G))
print("== D. upper bounds: 4 unsigned flats at 16 points; 11 unsigned flats at 256 points (own search for the eight matrices)")
g4=[1-2*q(z,4) for z in range(16)]
print("16 points: g = 1 - 2[z1z2=11] - 2[z3z4=11] + 4[z=1111]:",all(g4[z]==1-2*((z&3)==3)-2*((z>>2)==3)+4*(z==15) for z in range(16)))
def matvec(S,x): # S as list of 4 row masks
    return sum(((pc(S[i]&x)&1)<<i) for i in range(4))
alts=[]
for bits in range(64):
    idx=0; M=[0]*4
    for i in range(4):
        for j in range(i+1,4):
            if bits>>idx&1: M[i]|=1<<j; M[j]|=1<<i
            idx+=1
    alts.append(tuple(M))
def inv(M): return len({matvec(M,x) for x in range(16)})==16
def diff(A,B): return tuple(a^b for a,b in zip(A,B))
def grow(cl,cands):
    if len(cl)==8: return cl
    for i,c in enumerate(cands):
        r=grow(cl+[c],[d for d in cands[i+1:] if inv(diff(c,d))])
        if r: return r
    return None
zero=alts[0]; K8=grow([zero],[m for m in alts[1:] if inv(m)])
ok=True
for x in range(16):
    for y in range(16):
        val=-1+2*(x==0)+2*sum(1 for S in K8 if matvec(S,x)==y)-16*(x==0 and y==0)
        ok&=(val==1-2*(pc(x&y)%2))
print("256 points: alternating matrices",len(alts),", invertible",sum(inv(m) for m in alts),"; set of 8 with invertible differences found:",K8 is not None,"; identity -1 + 2[x=0] + 2 sum[y=Sx] - 16[x=y=0] = (-1)^(x.y) on all 256 entries:",ok)
print("== E. the step to the doubled class, and where it stops")
H4=[[1-2*(pc(x&y)%2) for x in range(4)] for y in range(4)]
print("H_4(x,y) on the 4 bits (x1,x2,y1,y2) is -1 exactly where x1 y1 + x2 y2 = 1 (the quadric on 4 bits, pairs (x1,y1),(x2,y2)):",all(H4[y][x]==1-2*(((x&1)&(y&1))^((x>>1)&(y>>1))) for x in range(4) for y in range(4)))
a=[1,1,1,-1]
M=[[a[y]*H4[y][x]*a[x] for x in range(4)] for y in range(4)]
P=[[1 if M[y][x]==-1 else 0 for x in range(4)] for y in range(4)]
print("a H_4 a with a = (+,+,+,-):",M,"; = J - 2 P with P a permutation matrix:",all(sum(r)==1 for r in P) and all(sum(P[y][x] for y in range(4))==1 for x in range(4)),"-> 2 flats, below the bound 2 log2 N = 4 that holds for H_4 itself (exhaustive run exh4)")
print("== F. claim (i): the 8-gate circuit, its repeats; then the same idea at every size")
e=[tuple(1 if i==j else 0 for j in range(4)) for i in range(4)]
def lin(p,u,qq,v): return tuple(p*x+qq*y for x,y in zip(u,v))
g1=lin(1,e[0],1,e[1]); g2=lin(1,e[2],1,e[3]); g3=lin(1,g1,1,g2); g4=lin(1,e[1],1,e[3]); g5=lin(1,g3,-2,g4); g6=lin(1,g3,-2,g2); g7=lin(1,e[1],1,e[2]); g8=lin(1,g3,-2,g7)
gates=[g1,g2,g3,g4,g5,g6,g7,g8]
def repeats(inputs,gates):
    seen={tuple(v%2 for v in w) for w in inputs}; rep=0
    for w in gates:
        r=tuple(v%2 for v in w)
        if r in seen: rep+=1
        seen.add(r)
    return rep
print("outputs g3,g5,g6,g8 =",[g3,g5,g6,g8],"are the rows of H_4:",sorted([g3,g5,g6,g8])==sorted(tuple(r) for r in H4),"; gates 8 ; repeats modulo 2:",repeats(e,gates),"; (N/2) log2 N = 4")
def family(k):
    N=1<<k; inputs=[tuple(1 if i==j else 0 for j in range(N)) for i in range(N)]; gates=[]
    def add(u,v,cu=1,cv=1):
        w=tuple(cu*x+cv*y for x,y in zip(u,v)); gates.append(w); return w
    def rec(lo,kk,needQ):
        # block of inputs lo .. lo+2^kk-1 ; returns total S, and dicts P[y], Q[y] (y != 0): sums of the inputs with x.y odd / even
        if kk==0: return inputs[lo],{}, {}
        h=1<<(kk-1)
        S0,P0,Q0=rec(lo,kk-1,True); S1,P1,Q1=rec(lo+h,kk-1,True)
        S=add(S0,S1); P={}; Q={}
        P[h]=S1; Q[h]=S0
        for y in range(1,h):
            P[y]=add(P0[y],P1[y]); P[y|h]=add(P0[y],Q1[y])
            if needQ: Q[y]=add(Q0[y],Q1[y]); Q[y|h]=add(Q0[y],P1[y])
        return S,P,Q
    S,P,Q=rec(0,k,False); nadd=len(gates)
    outs={0:S}
    for y in range(1,N): outs[y]=add(S,P[y],1,-2)
    ok=all(outs[y][x]==1-2*(pc(x&y)%2) for x in range(N) for y in range(N))
    return N,len(gates),nadd,repeats(inputs,gates),ok
for k in range(2,8):
    N,ng,nadd,rep,ok=family(k)
    print(f"N={N}: outputs = H exactly: {ok}; gates {ng} (adding gates {nadd}, then {N-1} gates u - 2v); coefficients +1, -2 only, no halving; repeats modulo 2: {rep} = N-1; ad-7's guess (N/2) log2 N = {N//2*k}; textbook gates {N*k}")
print("== G. claim (ii): is the 8-gate wiring an identity of the class of 2 x 2 kernels?  ALL 24 ways of putting the four rows on the four output gates")
def feasible(T3,T5,T6,T8):
    ab=(0,1); cd=(2,3)
    z=lambda v,idx: all(v[i]==0 for i in idx)
    def prop(w,u):   # exists x with w = x u
        if all(x==0 for x in u): return all(x==0 for x in w)
        i=next(i for i,x in enumerate(u) if x!=0); x=Fr(w[i])/Fr(u[i])
        return all(Fr(w[j])==x*u[j] for j in range(len(u)))
    # g3 = T3 always reachable (g1 on a,b ; g2 on c,d). g6 in span(g3,g2):
    if not z(T3,ab) and not z(T3,cd):
        ok6=prop([T6[0],T6[1]],[T3[0],T3[1]]) and prop([T6[2],T6[3]],[T3[2],T3[3]])     # g2 forced = T3 on c,d
    elif z(T3,cd): ok6=prop([T6[0],T6[1]],[T3[0],T3[1]])                               # g2 free on c,d
    else: ok6=prop(list(T6),list(T3))                                                  # g3 lives on c,d: g2 parallel to g3
    ok5=prop([T5[0],T5[2]],[T3[0],T3[2]])     # T5 - x T3 supported on b,d
    ok8=prop([T8[0],T8[3]],[T3[0],T3[3]])     # T8 - x T3 supported on b,c
    return ok5 and ok6 and ok8
names=["K1xK1","K1xK2","K2xK1","K2xK2"]
def rows(p,qq,r,s):
    K=[(p,qq),(r,s)]
    return [tuple(K[i][x]*K[j][y] for x in range(2) for y in range(2)) for i in range(2) for j in range(2)]
tested=[(1,1,1,-1),(1,2,3,-6),(2,3,5,Fr(-15,2)),(1,2,3,5),(1,1,1,-2),(2,1,1,3),(1,1,0,1),(1,0,1,1),(1,1,1,0),(0,1,1,1)]
for K in tested:
    R=rows(*K); good=[]
    for perm in permutations(range(4)):
        if feasible(R[perm[0]],R[perm[1]],R[perm[2]],R[perm[3]]): good.append("g3=%s g5=%s g6=%s g8=%s"%tuple(names[i] for i in perm))
    p,qq,r,s=K
    print("kernel",tuple(str(x) for x in K),"p s + q r =",p*s+qq*r,"| placements that work:",len(good),good)
# explicit coefficients, valid for every kernel: g3 carries the MIXED row K1 x K2
random.seed(2); cnt=0; okc=0
kern=[(1,2,3,5),(1,1,1,-2),(2,1,1,3),(1,1,1,-1)]+[tuple(Fr(random.randint(-9,9),random.randint(1,5)) for _ in range(4)) for _ in range(500)]
for (p,qq,r,s) in kern:
    if p==0 or qq==0 or r==0 or p*s-qq*r==0: continue
    a,b,c,d=[tuple(Fr(int(i==j)) for j in range(4)) for i in range(4)]
    L=lambda x,u,y,v: tuple(x*m+y*n for m,n in zip(u,v))
    w1=L(p*r,a,p*s,b); w2=L(qq*r,c,qq*s,d); w3=L(1,w1,1,w2); w4=L(p,b,qq,d); w5=L(Fr(p)/r,w3,Fr(qq*r-p*s)/r,w4)
    w6=L(Fr(r)/p,w3,Fr(s)/qq-Fr(r)/p,w2); w7=L(1,b,-1,c); w8=L(1,w3,qq*r-p*s,w7)
    R=rows(p,qq,r,s); cnt+=1; okc+=(w5==R[0] and w3==R[1] and w8==R[2] and w6==R[3])
print(f"explicit coefficients (g1 = pr a + ps b, g2 = qr c + qs d, g3 = g1 + g2, g4 = p b + q d, g5 = (p/r) g3 + ((qr-ps)/r) g4, g6 = (r/p) g3 + (s/q - r/p) g2, g7 = b - c, g8 = g3 + (qr-ps) g7): {cnt} kernels with p, q, r non-zero and non-zero determinant; outputs exactly K1xK1, K1xK2, K2xK1, K2xK2 on g5, g3, g8, g6: {okc}")
