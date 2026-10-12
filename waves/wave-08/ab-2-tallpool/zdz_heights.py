# zdz_heights.py : heights of the wires of the second pass of H = Z D Z^T, as PRIMITIVE wires (common factor removed).
# Z = subset sums (output at S = sum of inputs at subsets of S), D = diagonal (-2)^|T|.  Exact whole numbers.
# (a) tensor order: the second pass sums one address bit at a time.  (b) level order: the partial sum over |T| <= j.
import math, itertools
def prim_height(v):
    g=0
    for x in v: g=math.gcd(g,abs(x))
    return (max(abs(x) for x in v)//g, g) if g else (0,0)
for k in (3,4,5,6):
    N=1<<k
    # rows of D Z^T : row T = (-2)^|T| * indicator(x contains T)
    W=[[((-2)**bin(T).count('1')) if (x&T)==T else 0 for x in range(N)] for T in range(N)]
    tall=0; total=0; maxfac=1; gates=0; kinds={}
    for b in range(k):
        newW=[r[:] for r in W]
        for S in range(N):
            if S>>b&1:
                u=W[S]; v=W[S^(1<<b)]
                newW[S]=[u[i]+v[i] for i in range(N)]; gates+=1
                hu,gu=prim_height(u); hv,gv=prim_height(v); hw,gw=prim_height(newW[S])
                r=(gu//math.gcd(gu,gv), gv//math.gcd(gu,gv)); kinds[tuple(sorted(r))]=kinds.get(tuple(sorted(r)),0)+1
        W=newW
        for r in W:
            h,g=prim_height(r); total+=1; maxfac=max(maxfac,g)
            if h>1: tall+=1
    ok=all(W[S][x]==(-1)**bin(S&x).count('1') for S in range(N) for x in range(N))
    # level order
    lv_h=[]
    for j in range(k+1):
        hmax=0
        for S in range(N):
            r=[sum(((-2)**bin(T).count('1')) for T in range(N) if (T&S)==T and (T&x)==T and bin(T).count('1')<=j) for x in range(N)]
            hmax=max(hmax,prim_height(r)[0])
        lv_h.append(hmax)
    print('N=%d: second pass in tensor order: %d gates, gives H: %s; wires %d, of height above 1 as primitive wires: %d; largest common factor %d; gate kinds between the primitive wires (|a|,|b|): %s; level order, largest height of the partial sum over levels <= j, j=0..k: %s'%(N,gates,ok,total,tall,maxfac,sorted(kinds.items()),lv_h))
