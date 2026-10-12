# witt.py (ab-7): is the transform at 2^k points a (twisted) convolution for the SECOND addition on addresses,
# "multiply the power series 1 + a_1 x + ... + a_k x^k modulo 2 and modulo x^(k+1)"?   k = 3..6.
# Rows are labelled by the series u itself (address = its coefficients). Columns are labelled through a map w: group -> addresses
# with  w(uv) = (transpose-inverse of 'multiply by u') w(v) + w(u)  (so that every group element is a symmetry of H up to signs),
# w one-to-one. All such w are enumerated through their values on the generators 1 + x^j, j odd. For each w and each twist
# (a sign when the subtraction wraps around a cyclic factor) the question "are there signs r, s and a kernel c with
# H[row u][column v] = r(u) s(v) c(u^-1 v) x twist" is a linear system modulo 2, solved exactly.
import sys, itertools
def run(k):
    N=1<<k
    def mulser(a,b):   # a,b: bitmasks of coefficients x^1..x^k (bit i-1 = coeff of x^i), series 1+a, 1+b; returns (1+a)(1+b)-1
        r=a^b
        for i in range(k):
            if a>>i&1:
                for j in range(k):
                    if b>>j&1 and i+j+2<=k: r^=1<<(i+j+1)
        return r
    gens=[1<<(j-1) for j in range(1,k+1,2)]
    def order(g):
        o=1; c=g
        while c: c=mulser(c,g); o+=1
        return o
    ords=[order(g) for g in gens]
    # coordinates
    coords={}; 
    for e in itertools.product(*[range(o) for o in ords]):
        u=0
        for g,ee in zip(gens,e):
            for _ in range(ee): u=mulser(u,g)
        coords[e]=u
    assert len(set(coords.values()))==N, "generators not independent"
    elem=list(coords.items())   # (exponents, series)
    # linear part of 'multiply by 1+g' on addresses: a -> a*(1+g) = a + a*g (without the shift)
    def Lmat(g):   # columns: image of basis vector x^(i+1)
        cols=[]
        for i in range(k):
            a=1<<i; cols.append(mulser(a,g)^g)   # (1+a)(1+g)-1 = a + g + a g ; remove g
        return cols
    def apply(cols,v):
        r=0
        for i in range(k):
            if v>>i&1: r^=cols[i]
        return r
    def transpose(cols): return [sum(((cols[j]>>i)&1)<<j for j in range(k)) for i in range(k)]
    def inverse(cols):
        # brute force: unipotent of 2-power order, inverse = power
        cur=cols; prev=None
        ident=[1<<i for i in range(k)]
        P=cols
        while True:
            Q=[apply(cols,c) for c in P]   # cols o P
            if Q==ident: return P
            P=Q
    LiT=[transpose(inverse(Lmat(g))) if Lmat(g)!=[1<<i for i in range(k)] else [1<<i for i in range(k)] for g in gens]
    ng=len(gens); found=0; tested=0; report=None
    cand=[]
    for j in range(ng):
        cj=[]
        for x in range(N):
            acc=0; cur=x
            for _ in range(ords[j]): acc^=cur; cur=apply(LiT[j],cur)
            if not acc: cj.append(x)
        cand.append(cj)
    def tuples(prefix):
        j=len(prefix)
        if j==ng: yield tuple(prefix); return
        for x in cand[j]:
            if all(apply(LiT[i],x)^prefix[i]==apply(LiT[j],prefix[i])^x for i in range(j)):
                yield from tuples(prefix+[x])
    for ws in tuples([]):
        if FIRST and found: break
        w={}
        for e,u in elem:
            y=0
            for j in reversed(range(ng)):
                for _ in range(e[j]): y=apply(LiT[j],y)^ws[j]
            w[e]=y
        if len(set(w.values()))!=N: continue
        tested+=1
        # system for each twist
        E=[e for e,_ in elem]; pos={e:i for i,e in enumerate(E)}
        for tw in itertools.product((0,1),repeat=ng):
            if FIRST and found: break
            rows=[]
            for e,u in elem:
                for f in E:
                    d=tuple((b-a)%o for a,b,o in zip(e,f,ords))
                    wrap=sum(t for a,b,t in zip(e,f,tw) if b<a)&1
                    m=bin(u&w[f]).count("1")&1
                    # unknowns: rho(e) [0..N), sig(f) [N..2N), kap(d) [2N..3N), constant bit at 3N
                    rows.append((1<<pos[e])|(1<<(N+pos[f]))|(1<<(2*N+pos[d]))|(((m^wrap)&1)<<(3*N)))
            # eliminate
            piv={}; cons=True
            for r in rows:
                while r:
                    hb=(r&((1<<(3*N))-1))
                    if hb==0:
                        cons=False if r>>(3*N)&1 else cons; break
                    b=hb.bit_length()-1
                    if b in piv: r^=piv[b]
                    else: piv[b]=r; break
                if not cons: break
            if cons:
                found+=1
                if report is None: report=(ws,tw)
    names=" x ".join(f"Z/{o}" for o in ords)
    print(f"k={k} N={N}: group {names}; one-to-one column labellings w tried: {tested}; (w, twist) pairs for which H is a twisted convolution up to signs: {found}{' (stopped at the first)' if FIRST else ''}"+(f"; first: w on generators {[format(x,'0%db'%k) for x in report[0]]}, twist {report[1]}" if report else "")); sys.stdout.flush()
FIRST=('first' in sys.argv)
for k in (int(a) for a in sys.argv[1:] if a!='first'): run(k)
