# torus.py (ab-7): is the 16-point transform a CONVOLUTION on a group with a long cycle?
# For every abelian group G of order 16 and every function c: G -> {+1,-1} with c(0) = +1, test whether the matrix
# M[g][h] = c(g - h) is a Hadamard matrix (rows orthogonal), and if so whether it is the transform H up to free signs and
# relabellings of rows and columns. Test used for the last point: scale rows and columns so that row 0 and column 0 are +1;
# the matrix is then Sylvester's (the transform) exactly when its 16 rows are closed under entrywise product
# (closed => the rows are 16 distinct homomorphisms of an elementary abelian 2-group structure on the columns => character table).
# Exhaustive: 2^15 functions per group. Whole numbers only.
import itertools, sys
def groups():
    return {"Z16":[16],"Z8xZ2":[8,2],"Z4xZ4":[4,4],"Z4xZ2xZ2":[4,2,2],"Z2^4":[2,2,2,2]}
for name,shape in groups().items():
    els=list(itertools.product(*[range(m) for m in shape])); idx={e:i for i,e in enumerate(els)}
    N=len(els)
    sub=[[idx[tuple((a-b)%m for a,b,m in zip(g,h,shape))] for h in els] for g in els]   # index of g - h
    add=[[idx[tuple((a+b)%m for a,b,m in zip(g,h,shape))] for h in els] for g in els]
    nh=0; nsyl=0; example=None; changes=set()
    for bits in range(1<<(N-1)):
        c=[1]+[1-2*((bits>>i)&1) for i in range(N-1)]
        ok=True
        for d in range(1,N):
            if sum(c[g]*c[add[g][d]] for g in range(N))!=0: ok=False;break
        if not ok: continue
        nh+=1
        M=[[c[sub[g][h]] for h in range(N)] for g in range(N)]
        M=[[M[g][h]*M[0][h] for h in range(N)] for g in range(N)]
        M=[[M[g][h]*M[g][0] for h in range(N)] for g in range(N)]
        rows=set(tuple(r) for r in M)
        closed=len(rows)==N and all(tuple(a*b for a,b in zip(r,s)) in rows for r in rows for s in rows)
        if closed:
            nsyl+=1
            if example is None: example=c
    print(f"{name}: functions with c(0)=+1 whose convolution matrix is Hadamard: {nh}; of these equal to the transform up to signs and relabellings: {nsyl}")
    if example:
        print("   one such kernel c, listed over the group elements", "x".join(map(str,shape)), "in dictionary order:", "".join("+" if v>0 else "-" for v in example))
    sys.stdout.flush()
