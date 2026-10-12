# cuts.py k d enumfile : every minimum circuit (as a set of wires) of "degree <= d at 2^k points" over the two-element
# field, read from enum2's SOL lines, sorted in each of its k cuts into pure and mixed wires.
# A wire is a set of inputs (bit mask over the columns of rows.py).  Cut along address bit t: an input (a set S of bits)
# is UPPER if S contains t.  upper part of a wire = its upper inputs.  PURE = upper part empty.
# For each upper part b: versions(b) = the wires (inputs included) with that upper part.  bus length of b = versions - 1
# (in ad-2's lemma: the number of injections on b).  "new upper parts" = upper parts that are not a single upper input.
import sys
from itertools import combinations
from collections import Counter
k=int(sys.argv[1]); d=int(sys.argv[2]); fn=sys.argv[3]
sets=[]
for j in range(d+1):
    for c in combinations(range(k),j): sets.append(sum(1<<i for i in c))
ncol=len(sets)+len(sets)%2
def idmask(x):   # enum2 id -> mask over columns (column i <-> bit ncol-1-i of the id)
    return sum(1<<i for i in range(ncol) if (x>>(ncol-1-i))&1)
N=1<<k
targets=[sum(1<<i for i,s in enumerate(sets) if (s&y)==s) for y in range(N)]
inputs=[1<<i for i in range(len(sets))]
tg=[t for t in targets if t not in inputs]
sols=set()
for line in open(fn):
    if line.startswith('SOL'):
        sols.add(frozenset(idmask(int(x)) for x in line.split()[1:]))
print(f"k={k} d={d}: {len(sols)} different minimum circuits (sets of helper wires); gates = {len(tg)} outputs + {len(next(iter(sols)))} helpers")
tab=Counter(); fan=Counter(); busmax=Counter()
for S in sols:
    wires=set(inputs)|set(tg)|set(S); gates=set(tg)|set(S)
    # fan-out: how many OUTPUTS can read each helper (output = helper + another wire)
    best=0
    for h in S:
        r=sum(1 for t in tg if (t^h) in wires)
        best=max(best,r)
    fan[best]+=1
    for t in range(k):
        up=sum(1<<i for i,s in enumerate(sets) if (s>>t)&1)
        mixed=[w for w in gates if w&up]; pure=[w for w in gates if not w&up]
        ver=Counter()
        for w in wires:
            if w&up: ver[w&up]+=1
        upin=set(i for i in inputs if i&up)
        newup=[b for b in ver if b not in upin]
        longest=max(v-1 for v in ver.values())
        # pure gates that are the sum of two versions of one upper part (possible deliveries)
        mixedall=[w for w in wires if w&up]
        byup={}
        for w in mixedall: byup.setdefault(w&up,[]).append(w)
        deliv=set()
        for b,lst in byup.items():
            for x,y in combinations(lst,2):
                if (x^y) in pure: deliv.add(x^y)
        tab[(len(newup),len(mixed)-len(newup),len(pure),longest,len(deliv))]+=1
        busmax[longest]+=1
print("cuts sorted by (new upper parts, extra versions = injections, pure gates, longest bus, pure gates that can be a delivery): count")
for key in sorted(tab): print("  ",key,tab[key])
print("longest bus over cuts:",dict(sorted(busmax.items())))
print("largest number of outputs that read one helper, per circuit:",dict(sorted(fan.items())))
