# replay.py : exact replay of every SAVE line of tallmin.  For each: rebuild a circuit (every wire = a*u + b*v of two earlier
# wires, whole numbers), check that every target is reached, print the gates with their kinds (|a|,|b|)/g, the heights, the
# index of the target lattice (gcd of the largest minors) and its odd part.  Count (G).
import sys, re, itertools, math
from fractions import Fraction
def prim(v):
    g=0
    for x in v: g=math.gcd(g,abs(x))
    if g==0: return None
    s=next(x for x in v if x); s=1 if s>0 else -1
    return tuple(s*x//g for x in v)
def comb(u,v,w):
    n=len(u)
    for i in range(n):
        for j in range(i+1,n):
            D=u[i]*v[j]-u[j]*v[i]
            if D:
                a=w[i]*v[j]-w[j]*v[i]; b=u[i]*w[j]-u[j]*w[i]
                if all(D*w[l]==a*u[l]+b*v[l] for l in range(n)):
                    g=math.gcd(math.gcd(abs(a),abs(b)),abs(D)); return a//g,b//g,D//g
                return None
    return None
def minors_gcd(M):
    n=len(M[0]); m=len(M); g=0
    def det(A):
        A=[[Fraction(x) for x in r] for r in A]; k=len(A); d=Fraction(1)
        for i in range(k):
            p=next((r for r in range(i,k) if A[r][i]!=0),None)
            if p is None: return 0
            if p!=i: A[i],A[p]=A[p],A[i]; d=-d
            d*=A[i][i]
            for r in range(i+1,k):
                f=A[r][i]/A[i][i]; A[r]=[x-f*y for x,y in zip(A[r],A[i])]
        return int(d)
    r=min(m,n)
    best=0
    for rows in itertools.combinations(range(m),r):
        for cols in itertools.combinations(range(n),r):
            d=abs(det([[M[i][j] for j in cols] for i in rows])); g=math.gcd(g,d); best=max(best,d)
    return g,best
kinds_all={}; nsave=0; pure2=0
for line in open(sys.argv[1]):
    if not line.startswith('SAVE'): continue
    nsave+=1
    a,b=line.split('forms:'); fpart,tpart=b.split('| tall:')
    T=[tuple(int(x) for x in s.split(',')) for s in re.findall(r'\(([-\d,]+)\)',a)]
    Hh=[tuple(int(x) for x in s.split(',')) for s in re.findall(r'\(([-\d,]+)\)',tpart)]
    n=len(T[0]); wires=[tuple(1 if i==j else 0 for j in range(n)) for i in range(n)]; names=['x%d'%(i+1) for i in range(n)]
    todo=[('p%d'%(i+1),h) for i,h in enumerate(Hh)]+[('t%d'%(i+1),t) for i,t in enumerate(T)]
    out=[]; ok=True; kinds=[]
    while todo:
        prog=False
        for nm,w in list(todo):
            hit=None
            for i in range(len(wires)):
                for j in range(i+1,len(wires)):
                    c=comb(wires[i],wires[j],w)
                    if c: hit=(i,j,c); break
                if hit: break
            if hit:
                i,j,(a_,b_,g_)=hit; out.append('%s = (%d*%s + %d*%s)/%d = %s'%(nm,a_,names[i],b_,names[j],g_,w)); kinds.append((min(abs(a_),abs(b_)),max(abs(a_),abs(b_)),abs(g_)))
                wires.append(w); names.append(nm); todo.remove((nm,w)); prog=True; break
        if not prog: ok=False; break
    g,best=minors_gcd(T); odd=g
    while odd and odd%2==0: odd//=2
    big=max(max(abs(x) for x in h) for h in Hh)
    odd_coeff=any((k[0]*k[1]) % 2==1 and max(k[0],k[1])>1 or (k[1] not in (1,2,4,8)) for k in kinds)
    if not odd_coeff: pure2+=1
    for k in kinds: kinds_all[k]=kinds_all.get(k,0)+1
    print('SAVE #%d replay %s: %d gates (forms need %d); targets %s; tallest helper %d; lattice index %d (odd part %d), largest minor %d; coefficient other than 1,2,4: %s'%(nsave,'OK' if ok else 'FAILED',len(out),len(out)+1,T,big,g,odd,best,odd_coeff))
    if len(sys.argv)>2:
        for l in out: print('    '+l)
print('# SAVE lines',nsave,' with only coefficients 1,2,4,8:',pure2,' gate kinds (small,large,divisor):count',sorted(kinds_all.items()))
