# u-7-quotient, run E: Q gates inside the optimal 8-point SUBSET-SUM circuits of d-0 / h-4 (12 gates, Yates' count).
# Input: h-4-zetafloor/z8_p3_full.local.out (2,772 sets of 5 helper wires found modulo 3; digit 2 read as -1).
# For each set that replays exactly over the integers: the 20 wires (8 inputs, 5 helpers, 7 outputs other than x0), every way a wire
# is a*u + b*v of two others (exact integer test), the kind of that gate by classes (class = support, all entries are 0,+1,-1):
#   J three different supports, S result has the support of one parent, Q parents share a support and the result has another, E all equal.
# Then, over all orders in which the 12 wires can be made (subset dynamic programme), the LEAST number of Q gates.
import sys, re, itertools
sys.path.insert(0, sys.argv[1] + '/h-4-zetafloor')
import killmeter as km
k = 3; N = 8
sets = km.parse_sets(sys.argv[1] + '/h-4-zetafloor/z8_p3_full.local.out')
targets = km.zeta_rows(k)[1:]
inputs = [tuple(int(i == j) for j in range(N)) for i in range(N)]
limit = int(sys.argv[2]) if len(sys.argv) > 2 else len(sets)
hist = {}; nrep = 0; examples = {}; kinds_tot = {}
for idx, hs in enumerate(sets[:limit]):
    helpers = [tuple(h) for h in hs if len(h) == N]
    if len(helpers) != 5: continue
    made = list(dict.fromkeys([h for h in helpers if h not in targets] + targets))
    if len(made) != 12: continue
    allw = inputs + made
    sup = [sum(1 << x for x in range(N) if w[x]) for w in allw]
    births = [[] for _ in made]          # for made wire t: list of (mask of made-parents needed, isQ)
    for t, w in enumerate(made):
        for i in range(len(allw)):
            for j in range(i):
                if i == 8 + t or j == 8 + t: continue
                # cheap filter: support of w inside union of supports
                if sup[8 + t] & ~(sup[i] | sup[j]): continue
                if km.in_span(w, allw[i], allw[j]):
                    need = (1 << (i - 8) if i >= 8 else 0) | (1 << (j - 8) if j >= 8 else 0)
                    cu, cv, cw = sup[i], sup[j], sup[8 + t]
                    kind = 'E' if cu == cv == cw else 'Q' if cu == cv else 'S' if cw in (cu, cv) else 'J'
                    births[t].append((need, kind))
    INF = 99; best = {0: 0}
    full = (1 << 12) - 1
    for mask in range(full + 1):
        if mask not in best: continue
        c = best[mask]
        for t in range(12):
            if mask >> t & 1: continue
            cost = None
            for need, kind in births[t]:
                if need & ~mask: continue
                q = 1 if kind in ('Q', 'E') else 0
                cost = q if cost is None else min(cost, q)
                if cost == 0: break
            if cost is None: continue
            nm = mask | 1 << t
            if best.get(nm, INF) > c + cost: best[nm] = c + cost
    if full not in best: continue
    nrep += 1; q = best[full]; hist[q] = hist.get(q, 0) + 1
    if q not in examples: examples[q] = (idx, helpers)
    nq = sum(1 for t in range(12) if any(kd == 'Q' for _, kd in births[t]))
    kinds_tot[nq] = kinds_tot.get(nq, 0) + 1
print('sets read %d, replay exactly with 12 gates: %d' % (min(limit, len(sets)), nrep))
print('least number of Q (or E) gates over all orders and parent choices: %s' % sorted(hist.items()))
print('circuits by number of wires that CAN be read as born by a Q gate (some parent pair with one support): %s' % sorted(kinds_tot.items()))
for q, (idx, helpers) in sorted(examples.items()):
    print('example with least Q = %d: set %d helpers %s' % (q, idx, [''.join('%2d' % x for x in h) for h in helpers]))
