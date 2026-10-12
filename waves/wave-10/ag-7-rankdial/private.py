# private.py k d enumfile : mechanical check of the PRIVATE-WIRE LEMMA (ag-7.md section 3) on every minimum circuit
# enumerated by enum2 (two-element field).  Out = the N output forms; W = the wires that are not outputs.
# For a derivation (one gate u+v for every non-input output):
#   type c: u, v both outputs           -> claimed impossible when the shortest relation among outputs has > 3 terms
#   type a: one operand an output       -> the other operand (in W) is the LABEL; claimed: labels are distinct
#   type b: u, v both in W              -> an edge {u, v}
# Graph H+: vertices W and one extra vertex z; an edge {u,v} for each type b output, an edge {z,label} for each type a.
# Claim: H+ has no cycle shorter than (shortest relation among the outputs) - 2; no cycle at all if there is no relation.
import sys
from itertools import combinations, product
k=int(sys.argv[1]); d=int(sys.argv[2]); fn=sys.argv[3]
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
def girth(edges):
    adj={}
    for a,b in edges: adj.setdefault(a,[]).append(b); adj.setdefault(b,[]).append(a)
    best=10**9
    for s in adj:
        dist={s:0}; par={s:None}; q=[s]
        for x in q:
            for y in adj[x]:
                if y not in dist: dist[y]=dist[x]+1; par[y]=x; q.append(y)
                elif par[x]!=y: best=min(best,dist[x]+dist[y]+1)
    return best
ncirc=0; nder=0; typec=0; replabel=0; mingirth=10**9; ga=0; gb=0; hist={}
for S in sols:
    ncirc+=1
    wires=set(inputs)|Out|set(S); W=wires-Out
    reps={o:[(u,o^u) for u in wires if u<(o^u) and (o^u) in wires] for o in tg}
    for choice in product(*[reps[o] for o in tg]):
        # is there an order in which everything can be built with these gates for the outputs?
        have=set(inputs); todo=set(tg)|set(S); ch=True; gate=dict(zip(tg,choice))
        while ch and todo:
            ch=False
            for w in list(todo):
                if w in gate: ok = gate[w][0] in have and gate[w][1] in have
                else: ok = any((w^a) in have for a in have)
                if ok: have.add(w); todo.discard(w); ch=True
        if todo: continue
        nder+=1; edges=[]; labels=[]
        for o,(u,v) in gate.items():
            iu=u in Out; iv=v in Out
            if iu and iv: typec+=1
            elif iu or iv: lab=v if iu else u; labels.append(lab); edges.append(('z',lab)); ga+=1
            else: edges.append((u,v)); gb+=1
        if len(set(labels))<len(labels): replabel+=1
        if len(set(map(frozenset,edges)))<len(edges): replabel+=1
        g=girth(edges); mingirth=min(mingirth,g); hist[g]=hist.get(g,0)+1
print(f"k={k} d={d}: {ncirc} minimum circuits, {nder} derivations of their outputs")
print(f"  type c gates (two outputs added): {typec};  derivations with a repeated label or edge: {replabel}")
print(f"  type a outputs {ga}, type b outputs {gb} (summed over derivations)")
print("  shortest cycle of H+ over all derivations:", "none (always a forest)" if mingirth>=10**9 else mingirth, " histogram:", {('forest' if g>=10**9 else g):c for g,c in sorted(hist.items())})
