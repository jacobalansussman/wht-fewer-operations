# layer1.py: exact replay over Q of the sum/difference tree for layer 1 at any k (count G): 2(k-1) gates,
# and of the d-7 layer-2 circuit at k = 4 (10 gates). Checks that the outputs are: the all-ones form, forms U^(i-w) g with g in the
# head space (killed by 'remove one element'), and that they are independent.
from fractions import Fraction as Fr
import itertools
def rank(rows):
    A=[[Fr(x) for x in r] for r in rows]; r=0
    for c in range(len(A[0])):
        piv=next((i for i in range(r,len(A)) if A[i][c]!=0),None)
        if piv is None: continue
        A[r],A[piv]=A[piv],A[r]
        for i in range(len(A)):
            if i!=r and A[i][c]!=0:
                f=A[i][c]/A[r][c]; A[i]=[x-f*y for x,y in zip(A[i],A[r])]
        r+=1
    return r
for k in range(2,10):
    vals=[[1 if j==i else 0 for j in range(k)] for i in range(k)]; gates=0; outs=[]; level=vals
    while len(level)>1:
        nxt=[]
        for a in range(0,len(level)-1,2):
            u,v=level[a],level[a+1]; s=[x+y for x,y in zip(u,v)]
            nu=sum(1 for x in u if x); nv=sum(1 for x in v if x)
            d=[nv*x-nu*y for x,y in zip(u,v)]            # sum-zero: one gate a*u + b*v
            gates+=2; outs.append(d); nxt.append(s)
        if len(level)%2: nxt.append(level[-1])
        level=nxt
    outs.append(level[0])
    ok=all(sum(d)==0 for d in outs[:-1]) and outs[-1]==[1]*k and rank(outs)==k
    print("layer 1, k=%d: sum/difference tree, %d gates = 2(k-1) = %d, outputs correct and independent: %s" % (k,gates,2*(k-1),ok))
# layer 2 at k = 4: wires = pairs
pairs=list(itertools.combinations(range(4),2)); ix={P:n for n,P in enumerate(pairs)}
e=lambda P:[1 if ix[P]==n else 0 for n in range(6)]
add=lambda u,v,a=1,b=1:[a*x+b*y for x,y in zip(u,v)]
comp=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
S=[add(e(a),e(b)) for a,b in comp]; Dd=[add(e(a),e(b),1,-1) for a,b in comp]      # 6 gates; the three differences are outputs (type w=1)
t=add(S[0],S[1]); s=add(t,S[2])                                                    # 2 gates; s output (w=0)
h1=add(S[0],S[1],1,-1); h2=add(t,S[2],1,-2)                                        # 2 gates; outputs (w=2)
outs=[s]+Dd+[h1,h2]
def Dn(f):   # remove one element: pairs -> singletons
    return [sum(f[ix[P]] for P in pairs if i in P) for i in range(4)]
print("layer 2, k=4: 10 gates (3 sums, 3 differences, 2 for the total, 2 heads). rank %d; heads killed by D: %s; differences = U g with g sum-zero: %s" % (
    rank(outs), [Dn(h1),Dn(h2)], [Dn(d) for d in Dd]))
