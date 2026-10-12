# i-hatch: two flags at k=5 (32 points), |y| modulo 4, exhaustive up to the symmetry of permuting the 5 bits:
# first flag's smallest subspace {0,w} with w one representative per Hamming weight. Stops at the time limit and says how far it got.
import sys, time
sys.path.insert(0, "waves/wave-01/i-hatch")
pc = lambda x: bin(x).count("1")
k = 5; n = 32
def flags(k):
    n = 1 << k; out = set()
    def rec(chain):
        W = chain[-1]
        if len(W) == n: out.add(tuple(chain)); return
        seen = set()
        for v in range(1, n):
            if v in W: continue
            W2 = frozenset(W | {w ^ v for w in W})
            if W2 in seen: continue
            seen.add(W2); rec(chain + [W2])
    rec([frozenset([0])]); return [list(c) for c in out]
def level(chain):
    return [next(j for j, W in enumerate(chain) if y in W) for y in range(n)]
t0 = time.time(); FL = flags(k); LV = [level(c) for c in FL]
W4 = [pc(y) % 4 for y in range(n)]
first = [i for i in range(len(FL)) if min(FL[i][1] - {0}) in (1, 3, 7, 15, 31)]
print("flags: %d ; first flags after symmetry: %d ; built in %.0f s" % (len(FL), len(first), time.time() - t0)); sys.stdout.flush()
order = sorted(range(n), key=lambda y: -pc(y))
def cyc_ok(LA, LB):
    val = {}; adj = {}
    for y in range(n):
        a, b, w = ("A", LA[y]), ("B", LB[y]), W4[y]
        adj.setdefault(a, []).append((b, w)); adj.setdefault(b, []).append((a, w))
    for s in adj:
        if s in val: continue
        val[s] = 0; st = [s]
        while st:
            u = st.pop()
            for (v, w) in adj[u]:
                want = (w - val[u]) % 4
                if v not in val: val[v] = want; st.append(v)
                elif val[v] != want: return False
    return True
hits = []; done = 0; LIMIT = float(sys.argv[1])
for ia in first:
    LA = LV[ia]; keyA = [LA[y] * 8 for y in order]; wts = [W4[y] for y in order]
    for ib in range(len(FL)):
        LB = LV[ib]; seen = {}; ok = True
        for idx in range(n):
            key = keyA[idx] + LB[order[idx]]
            w = seen.get(key)
            if w is None: seen[key] = wts[idx]
            elif w != wts[idx]: ok = False; break
        if ok and cyc_ok(LA, LB): hits.append((ia, ib))
    done += 1
    if time.time() - t0 > LIMIT: break
print("first flags done: %d of %d ; pairs tested: %d ; solutions: %d ; %.0f s" % (done, len(first), done * len(FL), len(hits), time.time() - t0))
for (ia, ib) in hits[:4]:
    print("  ", [sorted(W) for W in FL[ia][1:-1]], "|", [sorted(W) for W in FL[ib][1:-1]])
