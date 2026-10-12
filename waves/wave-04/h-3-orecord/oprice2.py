#!/usr/bin/env python3
"""h-3-orecord / oprice2.py.  Price in count (O) the 19-gate circuits that g-1's annealer ended on (sa8_known0..3.out list the
wires of each circuit in order of derivation).  For every wire all ways to write it as a*u + b*v from earlier wires with
|a|, |b| in {1, 2} are found (exact integers); up to CAP combinations of these choices are priced with the rule of oprice.py
(price = gates + extra scale copies), for output scale 1/2 (e = -1), 1 (e = 0, H x itself) and 2 (e = +1, an 'up' unit).
Branch and bound with candidates restricted to scales already demanded of the wire or of one of its inputs, and a node limit.
The restriction is NOT proved complete (a later consumer of an input could ask for a scale not yet demanded), so the prices
printed are upper bounds for the rule; 'searches complete' only means the restricted search finished."""
import sys, re, itertools, math
sys.setrecursionlimit(10000)
CAP = 24; LIMIT = 300000
def read(path):
    ws = []
    for l in open(path):
        m = re.match(r'\s+(help|OUT)\s+\((\d+),(\d+)\)\s+\[(.*)\]', l)
        if m: ws.append((m.group(1).strip(), tuple(int(z) for z in m.group(4).split(','))))
    return ws
def options(ws):
    N = 8; held = [tuple(1 if i == j else 0 for j in range(N)) for i in range(N)]; names = ['x%d' % i for i in range(N)]
    opts = []
    for idx, (kind, w) in enumerate(ws):
        o = []
        for (i, u), (j, v) in itertools.combinations(list(enumerate(held)), 2):
            for a in (1, -1, 2, -2):
                for b in (1, -1, 2, -2):
                    for sgn in (1, -1):
                        if all(a * p + b * q == sgn * r for p, q, r in zip(u, v, w)):
                            o.append((a * sgn, names[i], b * sgn, names[j]))
        # keep one per unordered (|a|,u,|b|,v)
        seen = {}; 
        for (a, u, b, v) in o: seen.setdefault((abs(a), u, abs(b), v), (a, u, b, v))
        opts.append(list(seen.values())); held.append(w); names.append(('y' if kind == 'OUT' else 'g') + str(idx))
    return opts, names[8:]
def price(gates, inputs, outputs, eout):
    order = list(reversed(gates)); D = {g[0]: set() for g in gates}
    for x in inputs: D[x] = set()
    for y in outputs: D[y].add(eout)
    best = [10 ** 9]; nodes = [0]
    def lb(i): return sum(max(1, len(D[order[j][0]])) for j in range(i, len(order))) + sum(len(D[x] - {0}) for x in inputs)
    def go(i, cost):
        nodes[0] += 1
        if nodes[0] > LIMIT or cost + lb(i) >= best[0]: return
        if i == len(order): best[0] = cost + sum(len(D[x] - {0}) for x in inputs); return
        t, a, u, b, v = order[i]
        if not D[t]: go(i + 1, cost); return
        la = int(math.log2(abs(a))); lbb = int(math.log2(abs(b)))
        cands = sorted(D[t]) + sorted({e - la for e in D[u]} | {e - lbb for e in D[v]} - D[t])
        if u in inputs: cands += [e for e in [0 - la] if e not in cands]
        if v in inputs: cands += [e for e in [0 - lbb] if e not in cands]
        for e0 in cands:
            c = len(D[t] | {e0}); au = (e0 + la) not in D[u]
            if au: D[u].add(e0 + la)
            av = (e0 + lbb) not in D[v]
            if av: D[v].add(e0 + lbb)
            go(i + 1, cost + c)
            if av: D[v].discard(e0 + lbb)
            if au: D[u].discard(e0 + la)
    go(0, 0); return best[0], nodes[0] <= LIMIT
for path in sys.argv[1:]:
    ws = read(path); opts, names = options(ws)
    nopt = [len(o) for o in opts]; total = 1
    for n in nopt: total *= max(n, 1)
    print('%s: %d wires after the inputs (%d gates); ways to write each wire as one gate: %s; combinations %d, priced %d' % (path.split('/')[-1], len(ws), len(ws), nopt, total, min(total, CAP)), flush=True)
    if 0 in nopt: print('   a wire has no one-gate form with coefficients 1, 2: skipped'); continue
    outs = [names[i] for i, (k, w) in enumerate(ws) if k == 'OUT']; inputs = ['x%d' % i for i in range(8)]
    res = {-1: (99, True), 0: (99, True), 1: (99, True)}; cnt = 0
    for combo in itertools.product(*opts):
        cnt += 1
        if cnt > CAP: break
        gates = [(names[i], g[0], g[1], g[2], g[3]) for i, g in enumerate(combo)]
        for e in (-1, 0, 1):
            p, done = price(gates, inputs, outs, e)
            if p < res[e][0]: res[e] = (p, done)
    for e, lab in ((-1, 'H x / 2'), (0, 'H x itself'), (1, '2 * H x (up unit)')):
        print('   best price (O) for %-18s: %d  [%s]' % (lab, res[e][0], 'searches complete' if res[e][1] else 'a search hit its node limit: upper bound'), flush=True)
