#!/usr/bin/env python3
"""h-3-orecord / oprice.py.  The exact count-(O) price of a GIVEN count-(G) circuit, keeping its wires and its gates.
A wire w (its integer vector fixed by the file) may be held at several scales 2^e; each held copy of a non-input wire costs ONE
operation (either the gate itself, run on copies of its inputs at the right scales, or a multiplication of another copy by a
constant); each copy of an input at a scale other than 1 costs one.  Gate w = a*u + b*v run at scale e needs u at e + log2|a|
and v at e + log2|b|.  So  price = gates + (number of extra copies).  Branch and bound over the scale at which each gate is run,
in reverse program order; exact when the search finishes inside the node limit.
Modes: 'exact' = outputs at scale 1 (H x itself); 'scaled' = all outputs at one common scale, the best one."""
import sys, re, math
sys.setrecursionlimit(10000)
def parse(path):
    gates = []; inputs = set(); names = []
    for l in open(path):
        l = l.split('#')[0].strip()
        if not l: continue
        t, rhs = l.split('=')
        t = t.strip(); r = rhs.replace(' ', '').replace('+-', '-')
        m = re.fullmatch(r'([+-]?)(\d*)\*?([a-z]\w*)([+-])(\d*)\*?([a-z]\w*)', r); assert m, l
        s1, c1, u, s2, c2, v = m.groups()
        a = (-1 if s1 == '-' else 1) * int(c1 or 1); b = (-1 if s2 == '-' else 1) * int(c2 or 1)
        gates.append((t, a, u, b, v)); names.append(t)
    made = set(names)
    for (t, a, u, b, v) in gates:
        for z in (u, v):
            if z not in made: inputs.add(z)
    return gates, inputs
def vectors(gates, inputs):
    xs = sorted(inputs, key=lambda s: int(s[1:])); N = len(xs)
    val = {x: [1 if i == j else 0 for j in range(N)] for i, x in enumerate(xs)}
    for (t, a, u, b, v) in gates: val[t] = [a * p + b * q for p, q in zip(val[u], val[v])]
    return N, val
def price(gates, inputs, outputs, eout, limit=4000000):
    order = [g for g in reversed(gates)]
    D = {g[0]: set() for g in gates}
    for x in inputs: D[x] = set()
    for y in outputs: D[y].add(eout)
    best = [10 ** 9, None]; nodes = [0]
    def lb(i):
        s = 0
        for j in range(i, len(order)): s += max(1, len(D[order[j][0]])) if D[order[j][0]] or True else 0
        for x in inputs: s += len(D[x] - {0})
        return s
    choice = {}
    def go(i, cost):
        nodes[0] += 1
        if nodes[0] > limit: return
        if cost + lb(i) >= best[0]: return
        if i == len(order):
            best[0] = cost + sum(len(D[x] - {0}) for x in inputs); best[1] = dict(choice); return
        t, a, u, b, v = order[i]
        if not D[t]: go(i + 1, cost); return          # unused wire: not needed at all (does not happen in these files)
        la = int(math.log2(abs(a))); lbb = int(math.log2(abs(b)))
        cands = sorted(D[t]) + [e for e in range(-4, 5) if e not in D[t]]
        for e0 in cands:
            c = len(D[t] | {e0})
            addu = (e0 + la) not in D[u]; 
            if addu: D[u].add(e0 + la)
            addv = (e0 + lbb) not in D[v]
            if addv: D[v].add(e0 + lbb)
            choice[t] = e0
            go(i + 1, cost + c)
            if addv: D[v].discard(e0 + lbb)
            if addu: D[u].discard(e0 + la)
    go(0, 0)
    return best[0], best[1], nodes[0], nodes[0] <= limit
if __name__ == '__main__':
    for path in sys.argv[1:]:
        gates, inputs = parse(path); N, val = vectors(gates, inputs)
        k = N.bit_length() - 1
        rows = {tuple((-1) ** bin(j & x).count('1') for x in range(N)): j for j in range(N)}
        outputs = [t for (t, a, u, b, v) in gates if tuple(val[t]) in rows]
        assert len({rows[tuple(val[t])] for t in outputs}) == N, 'not all rows present'
        coefs = sorted({(abs(a), abs(b)) for (t, a, u, b, v) in gates}); neg = sum(1 for g in gates if g[1] < 0 and g[3] < 0)
        print('%s: N=%d, %d gates (G), every output exactly a row of H [replayed]; |coefficients| used %s; gates of the form -u-v: %d' % (path.split('/')[-1], N, len(gates), coefs, neg))
        pe, ch, nd, done = price(gates, inputs, outputs, 0)
        print('   exact H x        : price (O) = %d = %d gates + %d extra copies   [%s, %d nodes]   textbook %d' % (pe, len(gates), pe - len(gates), 'search complete' if done else 'NODE LIMIT: upper bound only', nd, N * k))
        res = []
        for e in range(-4, 3):
            p, ch, nd, done = price(gates, inputs, outputs, e)
            res.append((p, e, done, ch))
        p, e, done, ch = min(res, key=lambda r: r[0])
        print('   common scale free: price (O) = %d = %d gates + %d extra copies at output scale 2^%d   [%s]   all scales tried: %s' % (p, len(gates), p - len(gates), e, 'search complete' if all(r[2] for r in res) else 'NODE LIMIT somewhere: upper bound only', [(r[1], r[0]) for r in res]), flush=True)
