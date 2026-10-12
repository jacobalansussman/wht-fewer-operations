# u-7-quotient, run B: exact integers.  On the 19 and on the staircase (8 to 32 points):
#  full wires = held wires with all entries +1/-1 (outputs and hubs).  Every pair gives two Q gates: (f-f')/2 and (f+f')/2,
#  the wire f on the set where they differ / agree.
#  B1. how many of these quotients are new wires (not held up to sign), by support size
#  B2. translation classes: differences f-f' that occur for two or more pairs of held full wires; is the quotient already held?
#  B3. for every NEW quotient q: the outputs h with h in span(q, s) for a held non-output wire s (any coefficients)
#  B4. parents modulo 4: for full wires f1,f2,f3 the sum f1+f2+f3 == -f1*f2*f3 (mod 4), entries 1 and 3; how many triples of
#      non-output full wires (hubs) have a product that is an output or a held hub
import sys, re, itertools
from fractions import Fraction as F
exec(open(sys.argv[1] + '/u-7-quotient/qa.py').read().split("base = sys.argv[1]")[0])
base = sys.argv[1]
def plane(q, h, s):     # is rank(q,h,s) <= 2 ?  rows of the 3-column matrix repeat a lot: take distinct rows first
    rows = list(set(zip(q, h, s)))
    return rank(rows) <= 2
for label, path, N in (('the 19', base + '/g-1-tightwires/h8_19gates.txt', 8), ('staircase 8', base + '/e2-0-pieces/slp_8.txt', 8),
                       ('staircase 16', base + '/e2-0-pieces/slp_16.txt', 16), ('staircase 32', base + '/e2-0-pieces/slp_32.txt', 32)):
    W = wires(path, N); H = had(N); Hn = {norm(r): y for y, r in enumerate(H)}
    held = {}
    for n, w in W.items():
        assert all(t.denominator == 1 for t in w); held.setdefault(norm(w), n)
    full = [v for v in held if all(abs(t) == 1 for t in v)]
    hubs = [v for v in full if v not in Hn]
    assert len([v for v in full if v in Hn]) == N
    stock = [v for v in held if v not in Hn]
    print('%s: N=%d gates=%d held wires=%d full wires=%d (hubs %d)' % (label, N, len(W) - N, len(held), len(full), len(hubs)))
    quo = {}; diffs = {}
    for i in range(len(full)):
        for j in range(i):
            f, g = full[i], full[j]
            d = norm([(a - b) // 2 for a, b in zip(f, g)]); s = norm([(a + b) // 2 for a, b in zip(f, g)])
            for q in (d, s):
                quo.setdefault(q, []).append((held[f], held[g]))
    new = [q for q in quo if q not in held]
    bysz = {}
    for q in new: z = sum(1 for t in q if t); bysz[z] = bysz.get(z, 0) + 1
    print('  B1 quotients of pairs of full wires: %d distinct, %d already held, %d new; new by support size %s' % (len(quo), len(quo) - len(new), len(new), sorted(bysz.items())))
    multi = [(q, p) for q, p in quo.items() if len(p) >= 2]
    mh = sum(1 for q, p in multi if q in held)
    print('  B2 quotients made by 2 or more pairs: %d (held %d, not held %d); largest number of pairs for one quotient: held %d, not held %d' % (
        len(multi), mh, len(multi) - mh, max([len(p) for q, p in multi if q in held] or [0]), max([len(p) for q, p in multi if q not in held] or [0])))
    dist = {}; best = (0, None)
    for q in new:
        cnt = 0
        for y in range(N):
            if any(plane(q, H[y], s) for s in stock): cnt += 1
        dist[cnt] = dist.get(cnt, 0) + 1
        if cnt > best[0]: best = (cnt, q, quo[q][:2])
    print('  B3 new quotients by number of outputs one gate away (partner any held non-output wire, any coefficients): %s' % sorted(dist.items()))
    print('     best:', best)
    # the same for multi-pair quotients that are not held: number of pairs = number of shifts it could serve between held full wires
    if N <= 16:
        t_out = 0; t_hub = 0; t_all = 0
        fullset = set(full)
        for a, b, c in itertools.combinations(hubs, 3):
            t_all += 1
            p = norm([x * y * z for x, y, z in zip(a, b, c)])
            if p in Hn: t_out += 1
            elif p in fullset: t_hub += 1
        print('  B4 triples of hubs: %d ; product is an output: %d ; product is a held hub: %d' % (t_all, t_out, t_hub))
        t2 = 0; t2o = 0
        for a, b, c in itertools.combinations(full, 3):
            p = norm([x * y * z for x, y, z in zip(a, b, c)])
            if p in fullset: t2 += 1
            if p in Hn: t2o += 1
        print('     triples of full wires: %d ; product held: %d ; product an output: %d (of them all three outputs: %d)' % (
            len(full) * (len(full) - 1) * (len(full) - 2) // 6, t2, t2o, N * (N - 1) * (N - 2) // 6))
