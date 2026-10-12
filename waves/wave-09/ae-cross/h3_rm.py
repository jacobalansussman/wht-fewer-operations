# Hybrid 3: the transform is, within a constant factor and O(N), the encoder of the half-rate "low degree" code. Exact integers.
from math import comb
def pc(x): return bin(x).count("1")
for k in (3,5,7):
    N=1<<k; full=N-1
    low=[S for S in range(N) if pc(S)<=k//2]; high=[S for S in range(N) if pc(S)>k//2]
    Z=lambda T,S: 1 if S&T==S else 0
    # (1) Z_high[T,S] = Z_LL[S^c, T^c] : the block "all outputs from high inputs" is the transpose of "low outputs from low inputs", relabelled
    ok1=all(Z(T,S)==(Z(full^S,full^T) if pc(full^T)<=k//2 else 0) for T in range(N) for S in high)
    # and rows T of weight < that of S are zero, so the block is supported on high outputs only
    ok1b=all(Z(T,S)==0 for T in low for S in high)
    # (2) the low block is the evaluation of all polynomials of degree <= k//2 at all cube points: column space = span of characters of weight <= k//2
    #     check: every column Z[.,S], S low, is orthogonal to every character of weight > k//2
    ok2=all(sum(Z(T,S)*(-1)**pc(T&y) for T in range(N))==0 for S in low for y in high)
    print("k",k,"N",N,"low inputs",len(low),"| high block = transposed low-low block, relabelled:",ok1 and ok1b,"| low block spans exactly the characters of weight <= k/2:",ok2)
# systematic encoder of the affine code (degree <= 1) : N - 2 gates against N - 1 in the monomial basis, replayed at k = 3..6
for k in (3,4,5,6):
    N=1<<k
    import random; random.seed(k)
    c=[random.randint(-9,9) for _ in range(k+1)]
    f=lambda x: c[0]+sum(c[i+1] for i in range(k) if x>>i&1)
    val={0:f(0)}; gates=0
    for i in range(k): val[1<<i]=f(1<<i)            # the k+1 inputs are the values at 0 and at the unit points
    u=[val[1<<i]-val[0] for i in range(k)]; gates+=k-1  # differences; the last one is never needed if the lowest set bit is used below
    for x in range(1,N):
        if pc(x)>=2:
            hi=x.bit_length()-1
            val[x]=val[x^(1<<hi)]+ (val[1<<hi]-val[0]); gates+=1
    print("affine code, k",k,": systematic encoder correct:",all(val[x]==f(x) for x in range(N)),"gates",gates,"(N - 2); floor N - (k+1) =",N-k-1)
