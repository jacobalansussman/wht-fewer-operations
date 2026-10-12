#!/usr/bin/env python3
# i-wild, experiment C: "only one output is wanted, then two: how does the cost grow?"  N=16, exact integers.
# Heuristic UPPER bounds on additions/subtractions by greedy pair sharing (Paar style, signed, random tie breaks).
# Also checks, exactly, that the twisted transform is the grading of the Walsh basis by weight mod 4.
import random, itertools
from fractions import Fraction as F
k=4; N=16
wt=lambda v: bin(v).count('1')
H=[[(-1)**(wt(v&w)&1) for w in range(N)] for v in range(N)]
def paar(rows,tries=40,seed=1):
    rnd=random.Random(seed); best=None
    for _ in range(tries):
        T=[{j:c for j,c in enumerate(r) if c} for r in rows]; nsig=len(rows[0]); adds=0
        while True:
            cnt={}
            for t in T:
                ks=sorted(t)
                for a,b in itertools.combinations(ks,2):
                    key=(a,b,t[a]*t[b]); cnt[key]=cnt.get(key,0)+1
            if not cnt: break
            m=max(cnt.values()); a,b,s=rnd.choice([key for key,c in cnt.items() if c==m])
            c=nsig; nsig+=1; adds+=1
            for t in T:
                if a in t and b in t and t[a]*t[b]==s:
                    t[c]=t[a]; del t[a]; del t[b]
        if best is None or adds<best: best=adds
    return best
print("full H16, greedy:",paar(H),"(textbook 64)")
order_sub=list(range(N))                       # fills subspaces 1,2,4,8,16
order_wt=sorted(range(N),key=lambda v:(wt(v),v))  # fills Hamming balls
rnd=random.Random(7); order_rand=list(range(N)); rnd.shuffle(order_rand)
print("j  subspace-order  weight-order  random-order   (greedy upper bounds on add/sub for the first j outputs)")
for j in range(1,N+1):
    print("%2d  %6d %12d %12d"%(j,paar([H[v] for v in order_sub[:j]]),paar([H[v] for v in order_wt[:j]]),paar([H[v] for v in order_rand[:j]])))
# grading check, Gaussian rationals as pairs
def cmul(a,b): return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])
def cpow(a,n):
    r=(F(1),F(0))
    for _ in range(n): r=cmul(r,a)
    return r
mi=(F(0),F(-1)); ii=(F(0),F(1))
K=[[cpow(mi,wt(v^w)) for w in range(N)] for v in range(N)]         # K_{-i}: entries (-i)^distance
# E_j = (1/N) sum_{|s|=j} chi_s chi_s^T ;  claim K = (1-i)^k sum_j i^j E_j
c=cpow((F(1),F(-1)),k); ok=True
for v in range(N):
    for w in range(N):
        tot=(F(0),F(0))
        for s in range(N):
            e=F(H[s][v]*H[s][w],N); z=cmul(c,cpow(ii,wt(s))); tot=(tot[0]+z[0]*e,tot[1]+z[1]*e)
        ok&=(tot==K[v][w])
print("K_{-i} = (1-i)^k * sum_j i^j E_j  (weight mod 4 grading):",ok)
# H = D K D / stuff: (-1)^{v.w} = i^{|v|+|w|} (-i)^{d(v,w)}
ok2=all(cmul(cmul(cpow(ii,wt(v)),cpow(ii,wt(w))),K[v][w])==(F(H[v][w]),F(0)) for v in range(N) for w in range(N))
print("H = D K_{-i} D with D = diag(i^weight):",ok2)
# antipode = (-1)^weight grading
J=[[1 if v^w==N-1 else 0 for w in range(N)] for v in range(N)]
ok3=all(sum(F(H[s][v]*H[s][w],N)*(-1)**wt(s) for s in range(N))==J[v][w] for v in range(N) for w in range(N))
print("antipode J = sum_j (-1)^j E_j (weight mod 2 grading is a free relabelling):",ok3)
