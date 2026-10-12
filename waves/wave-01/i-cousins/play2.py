# i-cousins play 2: (a) the 7-gate 4-point transform over Q, checked; (b) no 6-gate circuit over GF(7), GF(11), GF(13);
# (c) randomized greedy upper bounds at n=8 over GF(7) for zeta, Hadamard, generic.
import sys, itertools, random, time
from fractions import Fraction as F
# (a)
def run(x):
    a,b,c,d=x
    w1=a+b; w2=c+d; y0=w1+w2; y2=w1-w2; w3=2*a-y0; y3=w3+2*d; y1=w3+2*c      # 7 gates, scalings by 2 free
    return [y0,y1,y2,y3]
Hm=[[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]]
ok=all(run([F(int(i==j)) for i in range(4)])==[F(Hm[r][j]) for r in range(4)] for j in range(4))
print("(a) 7-gate circuit computes H(x)H over Q on the 4 unit vectors:",ok)
def kron(A,B): return [[(x*y) for x in ra for y in rb] for ra in A for rb in B]
H=[[1,1],[1,-1]]; L=[[1,0],[1,1]]
def setup(p,n):
    def norm(v):
        for x in v:
            if x%p:
                inv=pow(x,p-2,p); return tuple((y*inv)%p for y in v)
    return norm
def has_circuit(Mat,p,m):          # is there a circuit with (non-input targets)+m gates, n=4
    n=4; norm=setup(p,n)
    T={norm(tuple(x%p for x in r)) for r in Mat}
    inp={norm(tuple(1 if j==i else 0 for j in range(n))) for i in range(n)}
    def onl(t,u,v):                # t in span(u,v)?
        for a in range(p):
            w=norm(tuple((x+a*y)%p for x,y in zip(u,v)))
            if w==t: return True
        return t==v
    def clo(R):
        R=set(R); ch=True
        while ch:
            ch=False
            for t in T-R:
                Rl=list(R)
                if any(onl(t,Rl[i],Rl[j]) for i in range(len(Rl)) for j in range(i)): R.add(t); ch=True
        return frozenset(R)
    front={clo(inp)}
    if any(T<=R for R in front): return True
    for step in range(m):
        nf=set()
        for R in front:
            Rl=sorted(R)
            for i in range(len(Rl)):
                for j in range(i):
                    for a in range(1,p):
                        w=norm(tuple((x+a*y)%p for x,y in zip(Rl[i],Rl[j])))
                        if w in R: continue
                        R2=clo(R|{w})
                        if T<=R2: return True
                        nf.add(R2)
        front=nf
    return False
for p in (7,11,13):
    print("(b) GF(%d): H(x)H with 6 gates (2 intermediates)? %s ; zeta(x)zeta with 3 gates? %s"%(p,has_circuit(kron(H,H),p,2),has_circuit(kron(L,L),p,0))); sys.stdout.flush()
# (c) greedy at n=8 over GF(7)
p=7; n=8; norm=setup(p,n)
def greedy(Mat,rng,limit):
    T={norm(tuple(x%p for x in r)) for r in Mat}
    R=[norm(tuple(1 if j==i else 0 for j in range(n))) for i in range(n)]; Rs=set(R); gates=0
    todo=set(T)-Rs
    while todo:
        if gates>=limit: return None
        # points on lines (t,r): one gate from there to t
        near={}
        for t in todo:
            for r in R:
                for a in range(p):
                    w=norm(tuple((x+a*y)%p for x,y in zip(t,r)))
                    if w is not None: near.setdefault(w,set()).add(t)
        done=[t for t in todo if any((w in Rs) and w!=t for w in [x for x in near if t in near[x]])]
        direct=[t for t in todo if any(t in near.get(r,()) and r!=t for r in R)]
        if direct:
            t=rng.choice(direct); R.append(t); Rs.add(t); todo.discard(t); gates+=1; continue
        best=[];bs=-1
        for i in range(len(R)):
            for j in range(i):
                for a in range(1,p):
                    w=norm(tuple((x+a*y)%p for x,y in zip(R[i],R[j])))
                    if w in Rs: continue
                    s=len(near.get(w,()))
                    if s>bs: bs=s; best=[w]
                    elif s==bs: best.append(w)
        w=rng.choice(best); R.append(w); Rs.add(w); gates+=1
    return gates
G=[[1,1],[1,2]]
t0=time.time()
for name,M2,tb in [("zeta",L,12),("Hadamard",H,24),("generic tau=2",G,24)]:
    Mat=kron(M2,kron(M2,M2)); rng=random.Random(1); best=None; tries=0; t1=time.time()
    while time.time()-t1<45:
        g=greedy(Mat,rng,(best or 40)); tries+=1
        if g is not None and (best is None or g<best): best=g
    print("(c) n=8 GF(7) greedy best gates %-14s : %s  (textbook %d, %d tries)"%(name,best,tb,tries)); sys.stdout.flush()
