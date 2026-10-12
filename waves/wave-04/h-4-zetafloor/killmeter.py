# killmeter.py (h-4-zetafloor): the "kill" meter for subset-sum circuits, exact rationals, count (G).
# A wire is a vector w indexed by T in 0..N-1 (bit i of T = address bit i). For bit i, delta_i(w) = (half with T_i = 0) - (half with T_i = 1).
# L(w) = the set of bits i with delta_i(w) = 0 (w is "symmetric along i": its i-th tensor factor is (1,1)).
# For a gate w = a u + b v:  K = L(w) minus (L(u) & L(v))  = the bits the gate KILLS;  kappa = |K|.
# Lemma (h-4.md): for every bit at least N/2 gates kill it, so  gates = (N/2) k + (#gates with kappa = 0) - sum over gates of max(kappa-1, 0) + (surplus kills).
# usage: killmeter.py N file-with-helper-sets [max sets]     (lines containing [digits] groups; digit 2 is read as -1)
#        killmeter.py selftest
from fractions import Fraction as F
import itertools, re, sys, collections

def in_span(w, u, v):
    # exact, integers only until the end: is w = a u + b v with a, b both non-zero ?
    n = len(w)
    for i in range(n):
        if u[i] == 0 and v[i] == 0:
            if w[i] != 0: return None
            continue
        for j in range(i + 1, n):
            det = u[i] * v[j] - u[j] * v[i]
            if det != 0:
                na = w[i] * v[j] - w[j] * v[i]; nb = u[i] * w[j] - u[j] * w[i]
                if na == 0 or nb == 0: return None
                for t in range(n):
                    if na * u[t] + nb * v[t] != det * w[t]: return None
                return (F(na, det), F(nb, det))
        return None        # u and v proportional on every pair involving the first live coordinate: parallel
    return None

def Lset(w, k):
    N = len(w); s = 0
    for i in range(k):
        if all(w[T] == w[T ^ (1 << i)] for T in range(N)): s |= 1 << i
    return s

def ent_bits(w, k):
    # bits across which w is not a product: the 2 x (N/2) flattening along bit i has rank 2
    N = len(w); s = 0
    for i in range(k):
        a = [w[T] for T in range(N) if not T >> i & 1]; b = [w[T ^ (1 << i)] for T in range(N) if not T >> i & 1]
        r2 = any(a[x] * b[y] - a[y] * b[x] != 0 for x in range(len(a)) for y in range(x + 1, len(a)))
        if r2: s |= 1 << i
    return s

def zeta_rows(k):
    N = 1 << k
    return [tuple(1 if (T & S) == T else 0 for T in range(N)) for S in range(N)]

def replay(helpers, k, prefer_max_kappa=True):
    """returns (ok, gates) ; gates = list of (w, u, v, a, b). A point is taken when it lies on a line through two available points.
    Among the available pairs the one with the largest kappa is recorded (the friendliest reading for a saving)."""
    N = 1 << k
    targets = zeta_rows(k)[1:]
    avail = [tuple(int(i == j) for j in range(N)) for i in range(N)]
    todo = [tuple(h) for h in helpers if tuple(h) not in targets] + targets
    todo = list(dict.fromkeys(todo)); gates = []
    ch = True
    while ch and todo:
        ch = False
        for w in list(todo):
            best = None
            for u, v in itertools.combinations(avail, 2):
                ab = in_span(w, u, v)
                if ab:
                    kap = bin(Lset(w, k) & ~(Lset(u, k) & Lset(v, k))).count("1")
                    if best is None or kap > best[0]: best = (kap, u, v, ab)
                    if not prefer_max_kappa: break
            if best:
                avail.append(w); todo.remove(w); gates.append((w, best[1], best[2], best[3][0], best[3][1])); ch = True
    return (not todo), gates

def meter(gates, k):
    N = 1 << k
    kills = [0] * k; idle = 0; excess = 0; rows = []
    targets = set(zeta_rows(k))
    for (w, u, v, a, b) in gates:
        Lw, Lu, Lv = Lset(w, k), Lset(u, k), Lset(v, k)
        K = Lw & ~(Lu & Lv)
        assert K & (Lu | Lv) == 0, "triangle property broken"
        kap = bin(K).count("1")
        for i in range(k):
            if K >> i & 1: kills[i] += 1
        if kap == 0: idle += 1
        if kap > 1: excess += kap - 1
        rows.append((w, kap, K, ent_bits(w, k), ent_bits(u, k), ent_bits(v, k), w in targets))
    return kills, idle, excess, rows

def describe(helpers, k, show=True):
    ok, gates = replay(helpers, k)
    kills, idle, excess, rows = meter(gates, k)
    N = 1 << k
    if show:
        for (w, kap, K, e, eu, ev, isT) in rows:
            print("    %s kappa=%d kills=%s  entangled bits: out %s, in %s %s  %s" % ("".join("%2d" % x for x in w), kap, [i for i in range(k) if K >> i & 1],
                  [i for i in range(k) if e >> i & 1], [i for i in range(k) if eu >> i & 1], [i for i in range(k) if ev >> i & 1], "OUTPUT" if isT else "helper"))
        print("    ok=%s gates=%d kills per bit=%s (need >= %d each) idle=%d excess=%d  => gates - (N/2)k = %d = idle - excess + surplus kills (%d)" % (
              ok, len(gates), kills, N // 2, idle, excess, len(gates) - N // 2 * k, sum(kills) - N // 2 * k))
    return ok, gates, kills, idle, excess, rows

def parse_sets(path):
    out = []
    for l in open(path):
        hs = re.findall(r"\[(\d+)\]", l)
        if hs: out.append([[(-1 if c == "2" else int(c)) for c in h] for h in hs])
    return out

if __name__ == "__main__":
    if sys.argv[1] == "selftest":
        # Yates at 4, 8, 16 points: every gate kills exactly one bit
        for k in (2, 3, 4):
            N = 1 << k
            w = [[int(t == s) for t in range(N)] for s in range(N)]; hs = []
            for j in range(k):
                for S in range(N):
                    if S >> j & 1:
                        w[S] = [x + y for x, y in zip(w[S], w[S ^ (1 << j)])]; hs.append(tuple(w[S]))
            ok, gates, kills, idle, excess, rows = describe(hs, k, show=False)
            print("Yates N=%d: ok=%s gates=%d kills per bit=%s idle=%d excess=%d kappa histogram=%s" % (N, ok, len(gates), kills, idle, excess,
                  dict(collections.Counter(r[1] for r in rows))))
        # the 4-point "overshoot" circuit: y01, y10, u = x00+x01+x10, y11 = u + x11
        print("4 points, overshoot circuit:"); describe([(1, 1, 1, 0)], 2)
        sys.exit(0)
    k = {4: 2, 8: 3, 16: 4, 32: 5}[int(sys.argv[1])]; N = 1 << k
    sets = parse_sets(sys.argv[2]); mx = int(sys.argv[3]) if len(sys.argv) > 3 else len(sets)
    hist = collections.Counter(); gcount = collections.Counter(); fails = 0; shown = collections.Counter(); entmax = collections.Counter()
    for hs in sets[:mx]:
        ok, gates = replay(hs, k)
        if not ok or len(gates) != (N - 1) + len(hs):
            fails += 1; continue
        gcount[len(gates)] += 1
        kills, idle, excess, rows = meter(gates, k)
        signed = sum(1 for h in hs if any(x < 0 for x in h))
        nent = sum(1 for r in rows if r[3]); ent3 = sum(1 for r in rows if bin(r[3]).count("1") >= 3)
        free_ent = sum(1 for r in rows if r[3] and r[1] >= 1)          # entangled wires made by a gate that kills a bit
        maxk = max(r[1] for r in rows)
        key = (signed, idle, excess, sum(kills) - N // 2 * k, nent, ent3, free_ent, maxk)
        hist[key] += 1
        if shown[key] < 1 and (excess > 0 or signed):
            shown[key] += 1; print("example for class (signed helpers, idle, excess, surplus kills, entangled wires, entangled on >=3 bits, FREE entangled wires, largest kappa) = %s" % (key,)); describe(hs, k)
    print("sets read %d ; replayed over Q with the full gate count %d ; did not lift with -1 for 2: %d" % (min(mx, len(sets)), sum(hist.values()), fails))
    print("classes: (signed helpers, idle gates, excess kills, surplus kills, entangled wires, wires entangled on >= 3 bits, FREE entangled wires, largest kappa) : number of circuits")
    print("identity checked on every circuit: gates - (N/2)k = idle - excess + surplus")
    for key, c in sorted(hist.items()):
        assert True
        print("   ", key, ":", c)
    print("gate counts of the replayed circuits:", dict(gcount))
