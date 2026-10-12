# ad-2: the cut read as a DECORATED circuit.  TWO-ELEMENT FIELD, count (G).
# Cut 2n points along one bit: lower inputs x', upper x''.  Class searched: circuits whose mixed part has exactly f(n) gates
# between mixed wires (M2) and exactly n injections (M3)  ("extra = 0").  Then (see ad-2.md, section 2):
#   - the M2 gates are a minimum circuit C'' for Z on the upper inputs; every wire of C'' exists in VERSIONS (same upper
#     part, different lower part), a new version costs one injection of a pure wire;
#   - a consumer slot of a wire = a gate of C'' that uses it, or its being an output; the slots of a wire are grouped into
#     classes by the version they use; each class k with non-zero offset d_k has a transfer vector tau_k (which outputs its
#     lower part reaches, modulo 2);  sum_k tau_k (x) d_k = Z, so with n classes the tau are a basis and the d_k are FORCED;
#   - a cancelling gate (delivery) is the sum of two versions of one wire: it hands over the difference of their offsets;
#     it beats a pure gate only when the path between the two versions has 3 or more injections.
# For each structure with a wire of >= 3 classes: least pure gates (the tool free8 with the injected wires as extra targets
# and the deliveries as free forms costing one gate each).  A saving in the cut needs pure gates <= f(n) - 1.
import sys, itertools, subprocess, os, collections
here=os.path.dirname(os.path.abspath(__file__))
n=int(sys.argv[1]); src=sys.argv[2]; LIMIT=int(sys.argv[3]) if len(sys.argv)>3 else 10**9; CAP=int(sys.argv[4]) if len(sys.argv)>4 else 10**9
FN={4:4,8:12}[n]
Zrow=[sum(1<<t for t in range(n) if (t&S)==t) for S in range(n)]
def derivations(forms):
    """all acyclic ways to derive every form in `forms` (a set of n-bit masks) from inputs and the other forms"""
    forms=sorted(forms); wires=[1<<j for j in range(n)]+forms
    opts=[]
    for f in forms:
        o=[(u,v) for u,v in itertools.combinations(wires,2) if u^v==f and u!=f and v!=f]
        if not o: return
        opts.append(o)
    for choice in itertools.product(*opts):
        par=dict(zip(forms,choice)); done=set(1<<j for j in range(n)); order=[]; ch=True
        while ch:
            ch=False
            for f in forms:
                if f not in done and par[f][0] in done and par[f][1] in done: done.add(f); order.append(f); ch=True
        if len(order)==len(forms): yield [(f,par[f]) for f in order]
def circuits():
    if src=='yates':
        forms=set()
        v=[1<<j for j in range(n)]
        b=1
        while b<n:
            for S in range(n):
                if S&b: v[S]=v[S]^v[S^b]; forms.add(v[S])
            b<<=1
        # in-place Yates: the stored wire for S after each stage
        yield from derivations(forms)
    elif src=='all4':
        tg=[z for z in Zrow if bin(z).count('1')>1]
        allf=[w for w in range(1,1<<n) if bin(w).count('1')>1 and w not in tg]
        for k in range(0,FN-len(tg)+1):
            for extra in itertools.combinations(allf,k):
                if len(tg)+k==FN: yield from derivations(set(tg)|set(extra))
    else:
        tg=[z for z in Zrow if bin(z).count('1')>1]
        for l in open(src):
            if 'example' not in l: continue
            inter=[sum(1<<i for i,c in enumerate(tok.strip('[]')) if c=='1') for tok in l.split(':')[1].split()]
            yield from derivations(set(tg)|set(inter))
def transfers(circ):
    sig={}; wires=[1<<j for j in range(n)]+[f for f,_ in circ]
    users=collections.defaultdict(list)
    for f,(u,v) in circ: users[u].append(f); users[v].append(f)
    for w in reversed(wires):
        s=0
        if w in Zrow: s^=1<<Zrow.index(w)
        for g in users[w]: s^=sig[g]
        sig[w]=s
    slots={}
    for w in wires:
        sl=[('gate',g,sig[g]) for g in users[w]]
        if w in Zrow: sl.append(('out',Zrow.index(w),1<<Zrow.index(w)))
        slots[w]=sl
    return wires,sig,slots
def partial_partitions(q):
    """all sets of disjoint non-empty blocks of range(q) (the rest of the slots keep offset 0)"""
    res=[]
    def rec(i,blocks):
        if i==q: res.append([tuple(b) for b in blocks]); return
        rec(i+1,blocks)
        for b in blocks: b.append(i); rec(i+1,blocks); b.pop()
        blocks.append([i]); rec(i+1,blocks); blocks.pop()
    rec(0,[]); return res
PP={q:partial_partitions(q) for q in range(0,8)}
def insert(basis,v):
    for b in basis: v=min(v,v^b)
    return v
def solve(taus):
    """offsets d_k with sum_k tau_k(S) d_k = Zrow[S] for all S (tau a basis)"""
    rows=[[sum(((taus[k]>>S)&1)<<k for k in range(n)), Zrow[S]] for S in range(n)]
    for c in range(n):
        piv=next(r for r in range(c,n) if (rows[r][0]>>c)&1); rows[c],rows[piv]=rows[piv],rows[c]
        for r in range(n):
            if r!=c and (rows[r][0]>>c)&1: rows[r][0]^=rows[c][0]; rows[r][1]^=rows[c][1]
    return [rows[k][1] for k in range(n)]
def trees(m):
    """spanning trees on points 0..m (0 = the root version), as edge lists"""
    pts=list(range(m+1)); allE=list(itertools.combinations(pts,2)); out=[]
    for E in itertools.combinations(allE,m):
        comp=list(range(m+1))
        def find(a):
            while comp[a]!=a: a=comp[a]
            return a
        ok=True
        for a,b in E:
            ra,rb=find(a),find(b)
            if ra==rb: ok=False; break
            comp[ra]=rb
        if ok: out.append(E)
    return out
TREES={m:trees(m) for m in range(1,6)}
def pathlen(E,m,a,b):
    adj=collections.defaultdict(list)
    for u,v in E: adj[u].append(v); adj[v].append(u)
    dist={a:0}; st=[a]
    while st:
        u=st.pop()
        for v in adj[u]:
            if v not in dist: dist[v]=dist[u]+1; st.append(v)
    return dist[b]
proc=subprocess.Popen([os.path.join(here,'free8'),str(n),'list'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True,bufsize=1)
proc.stdout.readline()
cache={}
def pure(free,targets):
    key=(tuple(sorted(free)),tuple(sorted(targets)))
    if key not in cache:
        proc.stdin.write(' '.join(map(str,key[0] or (0,)))+' T '+' '.join(map(str,key[1]))+'\n'); proc.stdin.flush()
        cache[key]=int(proc.stdout.readline().split(':')[1])
    return cache[key]
name=lambda w:'+'.join("x'%d"%i for i in range(n) if (w>>i)&1) or '0'
S1={}; S2={}
if n==8:
    for l in open(os.path.join(here,'single8.txt')):
        if l[0]!='#': w_,g_=map(int,l.split()); S1[w_]=12-g_
    import glob
    for f_ in glob.glob(os.path.join(here,'p[ABC][12].txt')):
        for l in open(f_):
            if l[0]!='#': a_,b_,g_=map(int,l.split()); S2[(a_,b_)]=12-g_
else:
    for w_ in range(1,1<<n):
        if bin(w_).count('1')>1: S1[w_]=FN-pure([w_],[])
    for a_,b_ in itertools.combinations(sorted(S1),2): S2[(a_,b_)]=FN-pure([a_,b_],[])
TOT=(1<<n)-1; BASE9=pure([TOT],[]); G9=set(1<<j for j in range(n))
if os.environ.get('MODE')=='d4':
    for g_ in range(1,1<<n):
        if bin(g_).count('1')>1 and g_!=TOT and pure([TOT],[g_])==BASE9: G9.add(g_)
    print('f(Z | total free) =',BASE9,'; forms that are free in some optimal circuit given the total (inputs included):',len(G9),flush=True)
stats=collections.Counter(); best=None; hist=collections.Counter(); ncirc=0; shown=0
maxq=collections.Counter()
for circ in circuits():
    ncirc+=1
    if ncirc>LIMIT: break
    if ncirc<=int(os.environ.get('START','0')): continue
    wires,sig,slots=transfers(circ)
    # rank of the slot transfers of each wire = the longest bus without an idle injection
    for w in wires:
        bs=[]
        for _,_,s in slots[w]:
            r=insert(bs,s)
            if r: bs.append(r)
        maxq[len(bs)]+=1
    wl=sorted(wires,key=lambda w:-len(slots[w]))
    cap=[0]*(len(wl)+1)
    for i in range(len(wl)-1,-1,-1): cap[i]=cap[i+1]+len(slots[wl[i]])
    def rec(i,basis,classes,big):
        if len(classes)==n:
            if big: yield list(classes)
            return
        if i==len(wl) or len(classes)+cap[i]<n: return
        w=wl[i]; sl=slots[w]
        for blocks in PP[len(sl)]:
            if len(classes)+len(blocks)>n: continue
            nb=list(basis); ok=True; add=[]
            for b in blocks:
                t=0
                for j in b: t^=sl[j][2]
                r=insert(nb,t)
                if not r: ok=False; break
                nb.append(r); add.append((w,b,t))
            if not ok: continue
            yield from rec(i+1,nb,classes+add,big or len(blocks)>=3 or os.environ.get('MODE')=='d4')
    for classes in rec(0,[],[],False):
        stats['structures with n independent classes and a wire with >= 3 classes']+=1
        if stats['structures with n independent classes and a wire with >= 3 classes']%20000==0: print('...',dict(stats),dict(hist),len(cache),file=sys.stderr,flush=True)
        if os.environ.get('MODE')=='count':
            stats['largest number of classes on one wire = %d'%max(collections.Counter(w for w,_,_ in classes).values())]+=1
            continue
        d=solve([t for _,_,t in classes])
        if os.environ.get('MODE')=='d4':
            # ONE IDLE INJECTION: a new version v of some wire, used by no gate, hung on version k by the pure wire
            # e = v + offset_k; the cancelling gate adds v and version l and must give the lower total:
            # e = total + offset_k + offset_l.  Pure part = 1 + f(Z and all 9 injected wires | total free); it equals
            # 1 + f(Z | total) exactly when every injected wire is free in one optimal circuit given the total.
            byw=collections.defaultdict(list)
            for (w,b,t),dk in zip(classes,d): byw[w].append(dk)
            good=[]; allpts=[]
            for w,ds in byw.items():
                pts=[0]+ds; allpts.append(pts)
                good.append([E for E in TREES[len(ds)] if all((pts[a_]^pts[b_]) in G9 for a_,b_ in E)])
            bad=[i for i,g in enumerate(good) if not g]
            if len(bad)>=2: continue
            stats['structures in which at most one wire lacks a tree of wires free given the total']+=1
            for i in (bad if bad else range(len(good))):
                pts=allpts[i]; m1=len(pts)
                cands=set(p_^g_ for p_ in pts for g_ in G9)-set(pts)
                for v in cands:
                    P2=pts+[v]
                    # is the total a difference of two versions at all?
                    if not any(P2[a_]^P2[b_]==TOT for a_,b_ in itertools.combinations(range(m1+1),2)): continue
                    for E in TREES[m1]:
                        if not all((P2[a_]^P2[b_]) in G9 for a_,b_ in E): continue
                        stats['(structure, wire, idle version, tree) with every injected wire free given the total and the total a difference of two versions']+=1
                        others=[[ [allpts[j][a_]^allpts[j][b_] for a_,b_ in E2] for E2 in good[j]] for j in range(len(good)) if j!=i]
                        for combo in itertools.product(*others):
                            inj=set(P2[a_]^P2[b_] for a_,b_ in E)
                            for ed in combo: inj.update(ed)
                            P=1+pure([TOT],[x for x in inj if bin(x).count('1')>1])
                            hist[P]+=1
                            if P==BASE9+1 and shown<4:
                                shown+=1; print('FOUND: pure gates',P,'= 1 + f(Z | total); injected',[name(x) for x in sorted(inj)],'idle version offset',name(v),'\n   classes',[(format(w,'0%db'%n)[::-1],b,format(t,'0%db'%n)[::-1],name(dk)) for (w,b,t),dk in zip(classes,d)],'\n   C\'\'',[(format(f,'0%db'%n)[::-1],format(u,'0%db'%n)[::-1],format(v_,'0%db'%n)[::-1]) for f,(u,v_) in circ],flush=True)
            continue
        byw=collections.defaultdict(list)
        for (w,b,t),dk in zip(classes,d): byw[w].append(dk)
        # per wire with >= 3 classes: every spanning tree on its versions; USEFUL deliveries = pairs of versions whose tree
        # path has >= 3 injections (a path of 2 costs one gate either way).  Census filter first (no search):
        # a set D of deliveries pays only if s(D) >= |D| + 1, s = what D saves the lower half when given free.
        per=[]; fixed=[]
        for w,ds in byw.items():
            pts=[0]+ds; m=len(ds)
            if m<3:
                # no useful delivery; the cheapest tree is found by the search below among all trees
                per.append([([pts[a]^pts[b] for a,b in E],[]) for E in TREES[m]]); continue
            o=[]
            for E in TREES[m]:
                dl=[pts[a]^pts[b] for a,b in itertools.combinations(range(m+1),2) if (a,b) not in E and pathlen(E,m,a,b)>=3]
                o.append(([pts[a]^pts[b] for a,b in E],dl))
            per.append(o)
        found=None
        for combo in itertools.product(*per):
            dl=sorted(set(x for _,dd in combo for x in dd))
            if not dl: continue
            edges=[e for ed,_ in combo for e in ed]; inj=[e for e in edges if bin(e).count('1')>1]
            for k in range(1,len(dl)+1):
                for sub in itertools.combinations(dl,k):
                    if k==1 and S1.get(sub[0],0)<2: continue
                    if k==2 and S2.get((min(sub),max(sub)),0)<3: continue
                    stats['(tree, delivery set) pairs that pass the census filter']+=1
                    P=k+pure(list(sub),inj)
                    if found is None or P<found[0]: found=(P,edges,sub)
        if found is None: hist['no delivery set passes the census filter: pure >= %d'%FN]+=1; continue
        bestP=found
        hist[bestP[0]]+=1
        if best is None or bestP[0]<best[0][0]: best=(bestP,circ,classes,d)
        if bestP[0]<=FN-1 and shown<5:
            shown+=1; print('SAVING candidate: pure gates',bestP[0],'injected',[name(e) for e in bestP[1]],'deliveries',[name(x) for x in bestP[2]],'circuit',circ,flush=True)
print('n = %d (cut of %d points), source %s: derivations (C\'\', one per way of deriving each wire) = %d'%(n,2*n,src,min(ncirc,LIMIT)))
print('wires by rank of their slot transfers (longest bus without an idle injection) -> count:',dict(sorted(maxq.items())))
for k,v in stats.items(): print(k,':',v)
print('least pure gates over these structures -> count (the lower half alone costs %d; a saving needs <= %d):'%(FN,FN-1),dict(sorted(hist.items(),key=str)))
if best:
    (P,edges,sub),circ,classes,d=best
    print('one best structure: pure gates',P,'; injected wires',[name(e) for e in edges],'; deliveries used',[name(x) for x in sub])
    print('   C\'\' =',[(format(f,'0%db'%n)[::-1],format(u,'0%db'%n)[::-1],format(v,'0%db'%n)[::-1]) for f,(u,v) in circ])
    print('   classes (wire, slots, tau) and forced offsets:',[(format(w,'0%db'%n)[::-1],b,format(t,'0%db'%n)[::-1],name(dk)) for (w,b,t),dk in zip(classes,d)])
