# census_check.py (h-4-zetafloor): totals of census8.out recomputed, and the census repeated with the OTHER recording rule
# (for each wire the available pair with the SMALLEST kappa), to see which readings depend on the rule.
import re, sys, itertools, collections
sys.path.insert(0, ".")
from killmeter import parse_sets, in_span, Lset, ent_bits, zeta_rows, meter
tot = collections.Counter()
for l in open("census8.out"):
    m = re.match(r"\s+\((\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+)\) : (\d+)", l)
    if m:
        s, idle, exc, sur, nent, e3, free, maxk, c = map(int, m.groups())
        tot["all"] += c; tot["signed"] += c * (s > 0); tot["yates-like"] += c * (nent == 0 and exc == 0)
        tot["idle=excess,surplus=0"] += c * (idle == exc and sur == 0); tot["excess>idle"] += c * (exc > idle)
        tot["free entangled wire"] += c * (free > 0); tot["a gate with kappa 3"] += c * (maxk == 3)
print("largest-kappa rule:", dict(tot))
def replay_min(helpers, k):
    N = 1 << k; targets = zeta_rows(k)[1:]
    avail = [tuple(int(i == j) for j in range(N)) for i in range(N)]
    todo = list(dict.fromkeys([tuple(h) for h in helpers if tuple(h) not in targets] + targets)); gates = []; ch = True
    while ch and todo:
        ch = False
        for w in list(todo):
            best = None
            for u, v in itertools.combinations(avail, 2):
                ab = in_span(w, u, v)
                if ab:
                    kap = bin(Lset(w, k) & ~(Lset(u, k) & Lset(v, k))).count("1")
                    if best is None or kap < best[0]: best = (kap, u, v, ab)
            if best: avail.append(w); todo.remove(w); gates.append((w, best[1], best[2], best[3][0], best[3][1])); ch = True
    return (not todo), gates
tot2 = collections.Counter(); cls = collections.Counter()
for hs in parse_sets("z8_p3_full.local.out"):
    ok, gates = replay_min(hs, 3)
    if not ok or len(gates) != 12: continue
    kills, idle, excess, rows = meter(gates, 3); sur = sum(kills) - 12
    free = sum(1 for r in rows if r[3] and r[1] >= 1); tri = sum(1 for r in rows if r[3] and r[4] and r[5] and r[1] >= 1 and len({r[3], r[4], r[5]}) == 3)
    tot2["all"] += 1; tot2["idle=excess,surplus=0"] += (idle == excess and sur == 0); tot2["excess>idle"] += excess > idle
    tot2["free entangled wire"] += free > 0; tot2["a gate with kappa 3"] += max(r[1] for r in rows) == 3
    tot2["a gate with two entangled inputs, an entangled output, three different entanglement sets, kappa>=1"] += tri > 0
    cls[(idle, excess, sur)] += 1
print("smallest-kappa rule:", dict(tot2))
print("smallest-kappa rule, (idle, excess, surplus) :", dict(sorted(cls.items())))
