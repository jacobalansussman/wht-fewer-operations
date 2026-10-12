# af-2: the 8-gate wiring on kernels with a zero entry: which have a working placement? Exact fractions.
import random, importlib.util, io, contextlib
from fractions import Fraction as Fr
from itertools import permutations
src=open("check.py").read()
start=src.index("def feasible"); end=src.index("tested=[")
exec(src[start:end])
random.seed(5); tally={}
for _ in range(4000):
    K=[Fr(random.randint(-4,4),random.randint(1,3)) for _ in range(4)]
    p,q,r,s=K
    if p*s-q*r==0: continue
    R=rows(*K); n=sum(feasible(R[a],R[b],R[c],R[d]) for a,b,c,d in permutations(range(4)))
    key=("p=0" if p==0 else "p!=0", "r=0" if r==0 else "r!=0", "ps+qr=0" if p*s+q*r==0 else "ps+qr!=0")
    tally.setdefault(key,{}); tally[key][n]=tally[key].get(n,0)+1
for k in sorted(tally): print(k,"-> number of working placements : count of kernels",tally[k])
