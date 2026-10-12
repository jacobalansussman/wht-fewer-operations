# ab-4-zcut/zreturn.py : how many optimal 12-gate circuits for Z at 8 points lie in the class of ab-4.md section 3b
# ("no return"): for a cube tree (an order of the address bits), NO gate w = a*u + b*v has a wire that vanishes on the
# on-half X1 of a node X, is non-zero on its off-half X0, and has a parent that is non-zero on X1.
# For each circuit (a set of 12 wires) and each of the 6 trees: is there a valid derivation (each wire from two wires already
# made or inputs) that uses only parent pairs allowed by the rule at every node?  Also: cancellation-free derivation
# (some parent pair with both coefficients of the same sign for every gate; wires scaled to have a positive first entry).
# Count (G). Exact.
import sys, re, itertools
from fractions import Fraction as F
exec(open('zmeter.py').read().split('def projections')[0])
def lift(d, p): return tuple((x if x <= p // 2 else x - p) for x in d)
def coef(w, u, v):
    for i in range(N):
        for j in range(i + 1, N):
            d = u[i] * v[j] - u[j] * v[i]
            if d:
                a = F(w[i] * v[j] - w[j] * v[i], d); b = F(u[i] * w[j] - u[j] * w[i], d)
                return (a, b) if all(a * u[t] + b * v[t] == w[t] for t in range(N)) else None
    return None
def nodes(order):
    res = []
    def rec(X, d):
        if len(X) == 1: return
        b = order[d]; X0 = [x for x in X if not x >> b & 1]; X1 = [x for x in X if x >> b & 1]
        res.append((X0, X1)); rec(X0, d + 1); rec(X1, d + 1)
    rec(list(range(N)), 0); return res
TREES = {o: nodes(o) for o in itertools.permutations(range(3))}
def ok_pair(w, u, v, nds):
    for X0, X1 in nds:
        if not any(w[i] for i in X1) and any(w[i] for i in X0) and (any(u[i] for i in X1) or any(v[i] for i in X1)): return False
    return True
def derivable(G, allowed):
    made = 0; ch = True
    while ch:
        ch = False
        for g in range(G):
            if not made >> g & 1 and any(m & made == m for m in allowed[g]): made |= 1 << g; ch = True
    return made == (1 << G) - 1
p = int(sys.argv[1]); tot = 0; hist = {}; cf = 0; cf_in = 0; ex = {}
for line in open(sys.argv[2]):
    if 'example' not in line: continue
    hs = [lift([int(ch) for ch in h], p) for h in re.findall(r'\[(\d+)\]', line)]
    wires = list(hs) + list(targets); allp = inputs + wires; G = 12
    pairs = [[] for _ in range(G)]
    for g, w in enumerate(wires):
        for i, j in itertools.combinations(range(len(allp)), 2):
            if i - N == g or j - N == g: continue
            ab = coef(w, allp[i], allp[j])
            if ab is None or ab[0] == 0 or ab[1] == 0: continue
            m = (1 << (i - N) if i >= N else 0) | (1 << (j - N) if j >= N else 0)
            pairs[g].append((m, allp[i], allp[j], ab))
    if not derivable(G, [[q[0] for q in pairs[g]] for g in range(G)]): continue
    tot += 1
    good = 0
    for o, nds in TREES.items():
        if derivable(G, [[q[0] for q in pairs[g] if ok_pair(wires[g], q[1], q[2], nds)] for g in range(G)]): good += 1
    hist[good] = hist.get(good, 0) + 1; ex.setdefault(good, hs)
    # cancellation-free: every wire has entries of one sign, and a derivation with coefficients of the same sign as needed
    def pos(v): return all(t >= 0 for t in v) or all(t <= 0 for t in v)
    def sgn(v): return 1 if next(t for t in v if t) > 0 else -1
    if all(pos(w) for w in wires):
        c = derivable(G, [[q[0] for q in pairs[g] if q[3][0] * sgn(q[1]) * sgn(wires[g]) > 0 and q[3][1] * sgn(q[2]) * sgn(wires[g]) > 0] for g in range(G)])
        if c:
            cf += 1
            if good == 6: cf_in += 1
print('p=%d: %d circuits' % (p, tot))
print('number of trees (of 6) for which the circuit has a derivation with no return : circuits')
for k in sorted(hist): print('   %d : %d   e.g. %s' % (k, hist[k], [''.join('%d' % x if x >= 0 else 'm' for x in h) for h in ex[k]]))
print('circuits with a cancellation-free derivation: %d; of these, no return in all 6 trees: %d' % (cf, cf_in))
