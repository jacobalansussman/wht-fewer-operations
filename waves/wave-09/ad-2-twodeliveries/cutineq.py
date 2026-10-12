# ad-2: check of the cut inequality on every minimum circuit at 8 points, TWO-ELEMENT FIELD, count (G).
# For each of the 6,960 derivations of ab-4's 2,802 minimum 12-gate circuits and each of the 3 cuts: classify the gates
# (M2: two mixed operands, mixed result; M3: injection; pure; cancelling), and when M2 = f(4) = 4 check
#     12  >=  2 f(4) + sum over upper forms b of min(number of injections onto b, 2).
import sys, os, collections
sys.argv=[sys.argv[0],'8',os.path.join(os.path.dirname(os.path.abspath(__file__)),'z8_sets.txt')]
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'deco.py')).read().split("proc=subprocess.Popen")[0])
tab=collections.Counter(); bad=0; cases=0; canc=collections.Counter()
for circ in circuits():
    for c in range(3):
        U=sum(1<<i for i in range(8) if (i>>c)&1)
        m2=0; r=collections.Counter(); pc=0; pint=0
        for f,(u,v) in circ:
            mf,mu,mv=bool(f&U),bool(u&U),bool(v&U)
            if mf and mu and mv: m2+=1
            elif mf: r[f&U]+=1
            elif mu: pc+=1
            else: pint+=1
        cases+=1
        bound=2*4+sum(min(x,2) for x in r.values())
        tab[(m2,sum(r.values()),pint,pc,tuple(sorted(r.values(),reverse=True)),bound if m2==4 else None)]+=1
        if m2==4 and bound>12: bad+=1
print('(derivation, cut) cases:',cases,'; violations of the inequality among cases with M2 = 4:',bad)
print('(M2 gates, injections, pure gates, cancelling gates, injections per upper wire, the bound 8 + sum of min(r,2)) -> cases')
for k,v in sorted(tab.items(),key=lambda t:-t[1]): print('  ',k,v)
