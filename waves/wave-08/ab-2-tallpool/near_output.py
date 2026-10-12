# near_output.py : checks for section 4(b) of ab-2.md.
# (1) For a full sign vector y on n points and a FORM v: every primitive wire u = (a y + b v)/g of height exactly 2 is, up to
#     sign, "y with a set Z of entries set to 0 and a set D doubled" (so u_i is 0, y_i or 2 y_i).  Exhaustive, n = 4, 5, |a|,|b| <= 8.
# (2) At 8 points: for four rows of H whose labels add up to zero, p = (y_a + y_b + y_c - y_d)/2 is a full sign vector and
#     differs from y_a, y_b, y_c, -y_d on four disjoint pairs of points.
import itertools, math
def prim(v):
    g=0
    for x in v: g=math.gcd(g,abs(x))
    return tuple(x//g for x in v) if g else None
for n in (4,5):
    bad=0; seen=0
    y=tuple([1]*n)        # by symmetry (signs of the inputs) one y is enough
    for v in itertools.product((-1,0,1),repeat=n):
        if not any(v): continue
        for a in range(-8,9):
            for b in range(-8,9):
                if a==0 or b==0: continue
                u=prim(tuple(a*y[i]+b*v[i] for i in range(n)))
                if u is None or max(abs(x) for x in u)!=2: continue
                seen+=1
                ok=any(all(s*u[i] in (0,y[i],2*y[i]) for i in range(n)) for s in (1,-1))
                if not ok: bad+=1
    print('n=%d: wires of height 2 on a line through y and a form: %d checked, %d not of the shape "zeros and doubles"'%(n,seen,bad))
N=8
def row(j): return tuple((-1)**bin(j&x).count('1') for x in range(N))
cnt=0; good=0
for a,b,c in itertools.combinations(range(N),3):
    d=a^b^c
    if d in (a,b,c): continue
    ya,yb,yc,yd=row(a),row(b),row(c),row(d)
    p=tuple((ya[i]+yb[i]+yc[i]-yd[i]) for i in range(N))
    cnt+=1
    if all(abs(x)==2 for x in p):
        p=tuple(x//2 for x in p)
        sets=[frozenset(i for i in range(N) if p[i]!=t[i]) for t in (ya,yb,yc,tuple(-x for x in yd))]
        if all(len(s)==2 for s in sets) and len(frozenset().union(*sets))==8: good+=1
print('8 points: triples of rows with their fourth: %d; p is a full sign vector two entries away from all four, on four disjoint pairs: %d'%(cnt,good))
