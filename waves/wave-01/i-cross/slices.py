# i-cross hybrid 3, general q: structure of the symmetric and antisymmetric squares of the q-point transform in slice coordinates.
# Inputs: unordered pairs {x,y} grouped by m = x^y; outputs: unordered pairs {u,v} grouped by w = u^v. Exact integers.
# Claim checked: every block (w, m) is zero or has rank one; the non-zero blocks are those with w.m = 0 (symmetric, and all blocks with
# m = 0 or w = 0) or w.m = 1 (antisymmetric); and on each slice the row factors are a full set of mutually orthogonal sign vectors closed
# under entrywise product up to sign (so: a transform of the slice's size). Then the two-layer program costs what the report says.
import sys
def par(a): return bin(a).count("1")&1
for a in (2,3,4):
    q=1<<a; h=lambda x,y: -1 if par(x&y) else 1
    for sgn,name in ((1,"symmetric"),(-1,"antisymmetric")):
        sl={}
        for x in range(q):
            for y in range(x,q):
                if x==y and sgn<0: continue
                sl.setdefault(x^y,[]).append((x,y))
        ok_zero=ok_rank=ok_had=True; nblocks=0
        for m,ins in sl.items():
            factors=[]
            for w,outs in sl.items():
                B=[[ (h(u,x)*h(y,v) + (sgn*h(u,y)*h(x,v) if x!=y else 0)) for (x,y) in ins] for (u,v) in outs]
                nz=any(e for r in B for e in r)
                expect = (m==0 or w==0 or par(m&w)==0) if sgn>0 else (par(m&w)==1)
                ok_zero&=(nz==expect)
                if nz:
                    nblocks+=1
                    r0=next(r for r in B if any(r))
                    ok_rank&=all(r[i]*r0[j]==r[j]*r0[i] for r in B for i in range(len(r0)) for j in range(len(r0)))
                    g=abs(next(e for e in r0 if e)); f=tuple(e//g for e in r0)
                    ok_rank&=all(abs(e)==g for e in r0)
                    factors.append(f)
            n=len(ins)
            norm=lambda f: f if f[0]>0 else tuple(-e for e in f)
            S=set(norm(f) for f in factors)
            ok_had&=(len(S)==n) and all(sum(p*q2 for p,q2 in zip(f,g2))==(n if f==g2 else 0) for f in S for g2 in S)
            ok_had&=all(norm(tuple(p*q2*r for p,q2,r in zip(f,g2,next(iter(S))))) in S for f in S for g2 in S)
        T=lambda n: n*(n.bit_length()-1)                # textbook gates of an n-point transform (2 gates per butterfly)
        cost = 2*T(q)+2*(q-1)*T(q//2) if sgn>0 else 2*(q-1)*T(q//2)
        print("q=%2d %-13s: slices %2d, non-zero blocks %3d, zero pattern as claimed: %s, every block rank one with flat factor: %s, slice factors form a transform of the slice: %s, two-layer cost at textbook prices %d" % (q,name,len(sl),nblocks,ok_zero,ok_rank,ok_had,cost))
    print("      total with split and merge: %d   textbook for %d points: %d" % (2*(q*q-q)+2*T(q)+4*(q-1)*T(q//2), q*q, T(q*q)))
