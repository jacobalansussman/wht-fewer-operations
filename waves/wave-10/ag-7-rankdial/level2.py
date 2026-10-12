# level2.py k d enumfile [cap] : mechanical check of the three facts of the SECOND STEP (ag-7.md section 5) in the
# cleanest regime, full rank (no relation among outputs at all), on every minimum circuit and every way of deriving
# ALL its wires (one gate for each output and each helper, acyclic).  Two-element field.
# H+ as in private.py; a GROUP is a connected component of H+ (z's component included; an isolated wire is alone).
# For a helper gate w = a + b:
#   INTERNAL  : a and b both in w's group                      claim (1): at most one such gate in each group
#   OWN+OUT   : exactly one operand, m, in w's group; the other, x, is a non-output wire outside it
#                                                              claim (2): no wire is such an x twice
#                                                              claim (3): no group holds two such x
#   an operand that is an output, the other in w's own group   claim (4): never
import sys
from itertools import combinations, product
k=int(sys.argv[1]); d=int(sys.argv[2]); fn=sys.argv[3]; cap=int(sys.argv[4]) if len(sys.argv)>4 else 3000
sets=[]
for j in range(d+1):
    for c in combinations(range(k),j): sets.append(sum(1<<i for i in c))
ncol=len(sets)+len(sets)%2
def idmask(x): return sum(1<<i for i in range(ncol) if (x>>(ncol-1-i))&1)
N=1<<k
outs=[sum(1<<i for i,s in enumerate(sets) if (s&y)==s) for y in range(N)]
inputs=[1<<i for i in range(len(sets))]
Out=set(outs); tg=[t for t in outs if t not in inputs]
sols=set()
for line in open(fn):
    if line.startswith('SOL'): sols.add(frozenset(idmask(int(x)) for x in line.split()[1:]))
nd=0; v1=v2=v3=v4=0; capped=0; cnt_int=0; cnt_own=0; cnt_pair=0; cnt_pair_iso=0; maxgroups=0; xin=0; xiso=0
for S in sols:
    wires=set(inputs)|Out|set(S); made=tg+sorted(S)
    reps={o:[(u,o^u) for u in wires if u<(o^u) and (o^u) in wires] for o in made}
    n=0
    for choice in product(*[reps[o] for o in made]):
        gate=dict(zip(made,choice))
        have=set(inputs); todo=set(made); ch=True
        while ch and todo:
            ch=False
            for w in list(todo):
                if gate[w][0] in have and gate[w][1] in have: have.add(w); todo.discard(w); ch=True
        if todo: continue
        n+=1
        if n>cap: capped+=1; break
        nd+=1
        # H+ and its components
        par={}
        def find(x):
            while par.setdefault(x,x)!=x:
                par[x]=par[par[x]]; x=par[x]
            return x
        for o in tg:
            u,v=gate[o]; iu=u in Out; iv=v in Out
            if iu and iv: raise SystemExit("kind c gate")
            a,b=('z',(v if iu else u)) if (iu or iv) else (u,v)
            par[find(a)]=find(b)
        W=wires-Out
        grp={w:find(w) for w in W}
        size={}
        for w in W: size[grp[w]]=size.get(grp[w],0)+1
        zg=find('z')
        maxgroups=max(maxgroups,len(set(grp.values())))
        internal={}; xs={}
        for w in S:
            a,b=gate[w]; g=grp[w]
            ina = a in W and grp[a]==g; inb = b in W and grp[b]==g
            if ina and inb: internal[g]=internal.get(g,0)+1; cnt_int+=1
            elif ina or inb:
                x=b if ina else a
                if x in Out: v4+=1
                else: xs.setdefault(x,[]).append(w); cnt_own+=1
            elif size[g]==1 and g!=zg: cnt_pair_iso+=1
            else: cnt_pair+=1
        if any(c>1 for c in internal.values()): v1+=1
        if any(len(l)>1 for l in xs.values()): v2+=1
        gx={}
        for x in xs:
            gx[grp[x]]=gx.get(grp[x],0)+1
            if size[grp[x]]==1 and grp[x]!=zg: xiso+=1
            else: xin+=1
        # an isolated wire is a group of one: only groups with an edge count for claim (3)
        if any(c>1 for c in gx.values()): v3+=1
print(f"k={k} d={d}: {len(sols)} minimum circuits, {nd} complete derivations ({capped} circuits cut off at {cap} derivations each)")
print(f"  helper gates by shape, summed: internal {cnt_int}, own group + outside wire {cnt_own}, both operands outside the group: {cnt_pair} for wires that sit in a group with an edge, {cnt_pair_iso} for isolated wires")
print(f"  the outside wire x of an 'own group + outside' gate is isolated {xiso} times, sits in a group with an edge {xin} times")
print(f"  derivations that break claim (1): {v1}; claim (2): {v2}; claim (3): {v3}; gates that break claim (4): {v4}")
print(f"  most groups (isolated wires included) in one derivation: {maxgroups}")
