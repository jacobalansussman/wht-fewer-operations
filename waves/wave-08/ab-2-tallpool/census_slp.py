# census_slp.py : the census of census.py on the (3/4) N log2 N family of e2-0-pieces (files slp_N.txt, one gate per line
# "name = a * u + b * v").  Exact whole numbers.  Checks first that the program holds every row of H up to scale.
import sys, re, math, itertools
def prim(v):
    g=0
    for x in v: g=math.gcd(g,abs(x))
    if not g: return None
    s=next(x for x in v if x); s=1 if s>0 else -1
    return tuple(s*x//g for x in v)
for fn in sys.argv[1:]:
    val={}; order=[]
    for line in open(fn):
        line=line.split('#')[0].strip()
        if not line: continue
        m=re.match(r'(\w+)\s*=\s*(-?\d+)\s*\*\s*(\w+)\s*\+\s*(-?\d+)\s*\*\s*(\w+)',line)
        if not m: print('unparsed:',line); continue
        nm,a,u,b,v=m.group(1),int(m.group(2)),m.group(3),int(m.group(4)),m.group(5)
        order.append((nm,a,u,b,v))
    names=set(n for n,_,_,_,_ in order); xs=sorted({t for _,_,u,_,v in order for t in (u,v) if t not in names},key=lambda t:int(t[1:]))
    N=len(xs)
    for i,x in enumerate(xs): val[x]=tuple(1 if i==j else 0 for j in range(N))
    for nm,a,u,b,v in order: val[nm]=tuple(a*p+b*q for p,q in zip(val[u],val[v]))
    wires=list(dict.fromkeys(prim(val[k]) for k in val))
    rows={prim(tuple((-1)**bin(j&x).count('1') for x in range(N))) for j in range(N)}
    ok=rows<=set(wires)
    tallw=sum(1 for w in wires if max(abs(x) for x in w)>=2)
    cnt={}; cf={}
    for u,v in itertools.combinations(wires,2):
        for sg in (1,-1):
            d=prim(tuple(a+sg*b for a,b in zip(u,v)))
            if not d: continue
            if max(abs(x) for x in d)>=2: cnt[d]=cnt.get(d,0)+1
            else: cf[d]=cf.get(d,0)+1
    rep=sum(1 for k in cnt.values() if k>=2); mx=max(cnt.values()) if cnt else 0
    mf={}
    for k in cf.values(): mf[k]=mf.get(k,0)+1
    print('%s: N=%d, %d gates, all rows of H held: %s; tall wires in the circuit: %d; tall sums or differences: %d, occurring twice or more: %d (most pairs %d); form sums or differences by number of pairs: %s'%(fn.split('/')[-1],N,len(order),ok,tallw,len(cnt),rep,mx,sorted(mf.items())))
    if rep:
        best=sorted(((k,d) for d,k in cnt.items() if k>=2),key=lambda t:(-t[0],sum(1 for x in t[1] if x)))[:3]
        for k,d in best: print('    tall %s (support %d, height %d) connects %d pairs'%(d,sum(1 for x in d if x),max(abs(x) for x in d),k))
