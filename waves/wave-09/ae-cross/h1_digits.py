# Hybrid 1: a binary digit of the transform is a degree. Exact integers.
from itertools import combinations
from math import comb
from fractions import Fraction
def pc(x): return bin(x).count("1")
def rank_mod_p(M,p=1000003):
    M=[r[:] for r in M]; rk=0; rows=len(M); cols=len(M[0])
    for c in range(cols):
        piv=None
        for r in range(rk,rows):
            if M[r][c]%p: piv=r;break
        if piv is None: continue
        M[rk],M[piv]=M[piv],M[rk]; inv=pow(M[rk][c],p-2,p)
        M[rk]=[(v*inv)%p for v in M[rk]]
        for r in range(rows):
            if r!=rk and M[r][c]%p:
                f=M[r][c]; M[r]=[(a-f*b)%p for a,b in zip(M[r],M[rk])]
        rk+=1
    return rk
for k in (2,3,4,5,6):
    N=1<<k
    H=[[(-1)**pc(x&y) for x in range(N)] for y in range(N)]
    E=[[[comb(pc(x&y),j) for x in range(N)] for y in range(N)] for j in range(k+1)]
    # exact identity H = sum_j (-2)^j E_j
    ok=all(H[y][x]==sum((-2)**j*E[j][y][x] for j in range(k+1)) for y in range(N) for x in range(N))
    # truncation: H = sum_{j<=d} (-2)^j E_j modulo 2^(d+1)
    tr=[all((H[y][x]-sum((-2)**j*E[j][y][x] for j in range(d+1)))%(1<<(d+1))==0 for y in range(N) for x in range(N)) for d in range(k+1)]
    rk=[rank_mod_p(E[j]) for j in range(k+1)] if k<=5 else None
    print("k",k,"H = sum (-2)^j E_j:",ok,"| truncation mod 2^(d+1) for d=0..k:",all(tr),"| rank E_j (mod 1000003):",rk,"binomials",[comb(k,j) for j in range(k+1)])
    # digit j at output y = sum over J subset y, |J|=j of sigma_J (superset sums): check on a unit-free random integer input
    import random
    random.seed(k); inp=[random.randint(-9,9) for _ in range(N)]
    sig={J:sum(inp[x] for x in range(N) if x&J==J) for J in range(N)}
    ok2=all(sum(E[j][y][x]*inp[x] for x in range(N))==sum(sig[J] for J in range(N) if pc(J)==j and J&y==J) for j in range(k+1) for y in range(N))
    print("   digit j at y = sum of the superset sums sigma_J over J inside y, |J|=j:",ok2)
# where the mass is: share of the N coefficients sigma_J in the middle band |j-k/2|<=c sqrt(k)
from math import sqrt
for k in (16,64,256,1024):
    tot=1<<k
    for c in (0.5,1,1.5):
        lo=int(k/2-c*sqrt(k)); hi=int(k/2+c*sqrt(k))
        band=sum(comb(k,j) for j in range(lo,hi+1))
        print("k",k,"c",c,"levels",hi-lo+1,"share of coefficients %.4f"%(band/tot))
# Plotkin/Yates ladder: E(d,k) = E(d,k-1)+E(d-1,k-1)+2^(k-1); bases E(0,k)=0 and (a) E(1,k)=N-... plain, (b) E(2,k)=N*(1+1.5*log2(k)/k) [ad-6's reported excess, as a what-if]
from functools import lru_cache
from math import log2
import sys
sys.setrecursionlimit(100000)
def ladder(base2):
    @lru_cache(None)
    def E(d,k):
        if d<=0 or k==0: return Fraction(0)
        if d>=k: return Fraction(k*(1<<k),2)
        if base2 and d==2 and k>=6: return Fraction(1<<k)*Fraction(int(1000*(1+1.5*log2(k)/k)),1000)
        return E(d,k-1)+E(d-1,k-1)+Fraction(1<<(k-1))
    return E
for k in (16,32,64):
    A=ladder(False); B=ladder(True)
    for d in (2,3,4,k//4,k//2):
        print("ladder k",k,"degree<=",d,"gates per point: Yates-type %.3f"%float(A(d,k)/(1<<k)),"| with ad-6's degree-2 base (what-if) %.3f"%float(B(d,k)/(1<<k)))
# the 8-gate circuit at 4 points with only 3 repeats
a,b,c,d=(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)
def lin(p,u,q,v): return tuple(p*x+q*y for x,y in zip(u,v))
g=[lin(1,a,1,b),lin(1,c,1,d)]; g.append(lin(1,g[0],1,g[1])); g.append(lin(1,b,1,d)); g.append(lin(1,g[2],-2,g[3])); g.append(lin(1,g[2],-2,g[1])); g.append(lin(1,b,1,c)); g.append(lin(1,g[2],-2,g[6]))
outs=[g[2],g[4],g[5],g[7]]
H4=[tuple((-1)**pc(x&y) for x in range(4)) for y in range(4)]
print("8 gates:",g); print("outputs are the four rows of H_4:",sorted(outs)==sorted(H4))
res=[tuple(v%2 for v in w) for w in [a,b,c,d]+g]; seen=set(res[:4]); rep=0
for r in res[4:]:
    if r in seen: rep+=1
    seen.add(r)
print("repeats modulo 2:",rep,"(ad-7's guess asked for at least (N/2) log2 N = 4); gates 8 against the least 7")
