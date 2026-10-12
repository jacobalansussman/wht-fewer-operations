# ag-2: the relation rule tested on REAL circuits.  TWO-ELEMENT FIELD, count (G).
# Every derivation of every minimum 12-gate circuit for Z at 8 points (ab-4's list), each of its 3 cuts (lower half 4 points,
# f(4) = 4).  Injected wires E = the pure operands of the injections; delivered forms w = results of the cancelling gates;
# L(w) = number of terms of w in E (unique when E is independent; otherwise the least and the most over the expansions).
# Prediction (purification): pure gates + sum over deliveries of (L - 1) >= f(4) = 4, so with 5 M2 gates, 4 injections,
# 2 pure gates and 1 cancelling gate the delivered form must have L >= 3.
import sys, os, collections, itertools
A=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','ad-2-twodeliveries')
sys.argv=[sys.argv[0],'8',os.path.join(A,'z8_sets.txt')]
exec(open(os.path.join(A,'deco.py')).read().split("proc=subprocess.Popen")[0])
tab=collections.Counter(); bad=0; cases=0; notspan=0
for circ in circuits():
    for c in range(3):
        U=sum(1<<i for i in range(8) if (i>>c)&1)
        m2=0; E=[]; W=[]; pint=0
        for f,(u,v) in circ:
            mf,mu,mv=bool(f&U),bool(u&U),bool(v&U)
            if mf and mu and mv: m2+=1
            elif mf: E.append(v if mu else u)
            elif mu: W.append(f)
            else: pint+=1
        cases+=1
        Ls=[]
        for w in W:
            ws=[bin(mask).count('1') for mask in range(1<<len(E)) if (lambda m: __import__('functools').reduce(lambda x,i: x^E[i] if (m>>i)&1 else x, range(len(E)), 0))(mask)==w]
            if not ws: notspan+=1; Ls.append(None)
            else: Ls.append((min(ws),max(ws)))
        rk=len(set()) ; basis=[]
        for e in E:
            x=e
            for b in basis: x=min(x,x^b)
            if x: basis.append(x)
        indep=(len(basis)==len(E))
        if all(l is not None for l in Ls):
            lhs=pint+sum(l[1]-1 for l in Ls)
            if lhs<4: bad+=1
        tab[(m2,len(E),pint,len(W),indep,tuple(sorted(Ls,key=str)))]+=1
print('TWO-ELEMENT FIELD. (derivation, cut) cases:',cases,'; delivered forms outside the span of the injected wires:',notspan,'; violations of  pure + sum (L - 1) >= 4 :',bad)
print('(M2 gates, injections, pure gates, cancelling gates, injected wires independent?, (least L, most L) of each delivered form) -> cases')
for k,v in sorted(tab.items(),key=lambda t:-t[1]): print('  ',k,v)
