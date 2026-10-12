# torus2.py (ab-7): the same question as torus.py, now with TWISTED kernels.
# A convolution kernel c on a group G that is "H up to free scalings" need not be +-1: it may be (root of unity)^(position) x (+-1).
# Equivalent whole-number form: M[g][h] = eps(g - h) * product over the twisted directions j of (-1)^[g_j < h_j]
# ("negacyclic" in direction j). Twist (0,...,0) is torus.py's case. For every abelian group of order 8 and 16, every twist,
# and every eps with eps(0) = +1: is M a Hadamard matrix, and is it the transform up to signs and relabellings
# (test: after scaling row 0 and column 0 to +1 the rows are closed under entrywise product)?
import itertools, sys
def run(name,shape):
    els=list(itertools.product(*[range(m) for m in shape])); idx={e:i for i,e in enumerate(els)}; N=len(els)
    sub=[[idx[tuple((a-b)%m for a,b,m in zip(g,h,shape))] for h in els] for g in els]
    for tw in itertools.product((0,1),repeat=len(shape)):
        sg=[[(-1)**sum(t for a,b,t in zip(g,h,tw) if a<b) for h in els] for g in els]
        nh=0;nsyl=0;ex=None
        for bits in range(1<<(N-1)):
            e=[1]+[1-2*((bits>>i)&1) for i in range(N-1)]
            r0=[e[sub[0][h]]*sg[0][h] for h in range(N)]
            ok=True
            for g in range(1,N):
                sgg=sg[g]; sbg=sub[g]
                if sum(r0[h]*e[sbg[h]]*sgg[h] for h in range(N))!=0: ok=False;break
            if not ok: continue
            M=[[e[sub[g][h]]*sg[g][h] for h in range(N)] for g in range(N)]
            if any(sum(a*b for a,b in zip(M[g],M[g2])) for g in range(N) for g2 in range(g)): continue
            nh+=1
            M=[[M[g][h]*M[0][h] for h in range(N)] for g in range(N)]
            M=[[M[g][h]*M[g][0] for h in range(N)] for g in range(N)]
            rows=set(tuple(r) for r in M)
            if len(rows)==N and all(tuple(a*b for a,b in zip(r,s)) in rows for r in rows for s in rows):
                nsyl+=1
                if ex is None: ex=e
        print(f"{name} twist {tw}: Hadamard {nh}; the transform {nsyl}"+("; example eps "+"".join("+" if v>0 else "-" for v in ex) if ex else "")); sys.stdout.flush()
for name,shape in (("Z8",[8]),("Z4xZ2",[4,2]),("Z2^3",[2,2,2]),("Z16",[16]),("Z8xZ2",[8,2]),("Z4xZ4",[4,4])):
    run(name,shape)
