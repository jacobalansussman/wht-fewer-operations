# i-hatch: "flag multipliers".  A flag is a chain of subspaces W_0=0 < W_1 < ... < W_k = Z_2^k of frequencies.
# An operator whose spectrum g(y) depends only on the level of y in ONE flag (level = first W_j containing y) is a
# Haar-type multiplier: about 2n gates, whatever k is.  The transform's spectrum is (-i)^|y| (|y| = Hamming weight).
# Question: how few flags r give  sum_m h_m(level_m(y)) = |y|  (exactly: then every noise operator; or modulo 4: the transform)?
# Textbook = k flags (one hyperplane each).  Exact rank tests modulo P = 2^61-1 (0/1 matrices with at most 17 columns of
# length at most 64: every minor is far below P, so ranks modulo P are the rational ranks).
import sys, random, itertools, time
P = (1 << 61) - 1
pc = lambda x: bin(x).count("1")

def flags(k):
    n = 1 << k
    out = set()
    def rec(chain):
        W = chain[-1]
        if len(W) == n:
            out.add(tuple(chain)); return
        seen = set()
        for v in range(1, n):
            if v in W: continue
            W2 = frozenset(W | {w ^ v for w in W})
            if W2 in seen: continue
            seen.add(W2); rec(chain + [W2])
    rec([frozenset([0])])
    return [list(c) for c in out]
def randflag(k):
    n = 1 << k; W = {0}; chain = [frozenset(W)]
    while len(W) < n:
        v = random.choice([x for x in range(n) if x not in W])
        W = W | {w ^ v for w in W}; chain.append(frozenset(W))
    return chain
def level(chain, n):
    L = [0] * n
    for y in range(n):
        L[y] = next(j for j, W in enumerate(chain) if y in W)
    return L
def in_span(vecs, t):
    rows = [list(v) for v in vecs] + [list(t)]
    m = len(rows[0]); piv = []
    for idx, r in enumerate(rows):
        for (pcol, pr) in piv:
            if r[pcol]:
                f = r[pcol]
                r[:] = [(a - f * b) % P for a, b in zip(r, pr)]
        c = next((j for j in range(m) if r[j]), None)
        if idx == len(rows) - 1: return c is None
        if c is not None:
            inv = pow(r[c], P - 2, P); r[:] = [a * inv % P for a in r]; piv.append((c, r))
def exact_ok(Ls, k):
    n = 1 << k
    vecs = [[1] * n]
    for L in Ls:
        for j in range(k): vecs.append([1 if L[y] <= j else 0 for y in range(n)])
    return in_span(vecs, [pc(y) for y in range(n)])
def mod4_ok_pair(LA, LB, k):
    # h_A(LA[y]) + h_B(LB[y]) = |y| mod 4, real-valued h allowed: consistency around cycles of the bipartite level graph
    n = 1 << k; val = {}
    adj = {}
    for y in range(n):
        a, b, w = ("A", LA[y]), ("B", LB[y]), pc(y) % 4
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

random.seed(11); t0 = time.time()
for k in (2, 3, 4):
    n = 1 << k; FL = flags(k); LV = [level(c, n) for c in FL]
    print("k=%d: %d flags" % (k, len(FL)))
    one = [i for i in range(len(FL)) if exact_ok([LV[i]], k)]
    print("  one flag, exact |y|: %d solutions" % len(one), (" e.g. W_1=%s" % sorted(FL[one[0]][1])) if one else "")
    if k >= 3:
        ex = []; m4 = []
        for i in range(len(FL)):
            for j in range(i + 1, len(FL)):
                if mod4_ok_pair(LV[i], LV[j], k):
                    m4.append((i, j))
                    if exact_ok([LV[i], LV[j]], k): ex.append((i, j))
                elif k == 3 and exact_ok([LV[i], LV[j]], k): ex.append((i, j))
        print("  two flags: |y| modulo 4 (the transform): %d pairs of %d ; of these exact |y|: %d" % (len(m4), len(FL) * (len(FL) - 1) // 2, len(ex)))
        for (i, j) in (m4[:2]):
            print("     e.g.", [sorted(W) for W in FL[i][1:-1]], "and", [sorted(W) for W in FL[j][1:-1]])
    sys.stdout.flush()
# exact version with two flags at k=4, all pairs (slower): only if modulo-4 found nothing above we still want to know
k = 4; n = 16; FL = flags(k); LV = [level(c, n) for c in FL]
cnt = 0; tried = 0
for i in range(len(FL)):
    for j in range(i + 1, len(FL)):
        tried += 1
        if exact_ok([LV[i], LV[j]], k): cnt += 1
    if time.time() - t0 > 120: break
print("k=4 two flags, exact |y|: %d solutions among %d pairs tried" % (cnt, tried)); sys.stdout.flush()
# three flags at k=5 and k=6 (textbook-with-pairs needs 3): do TWO flags ever suffice at k=5?  random pairs, modulo 4
for k, trials in ((5, 60000), (6, 30000)):
    n = 1 << k; hit = 0; ex = None
    for _ in range(trials):
        A, B = randflag(k), randflag(k)
        if mod4_ok_pair(level(A, n), level(B, n), k): hit += 1; ex = (A, B)
        if time.time() - t0 > 200 + 40 * (k - 5): break
    print("k=%d two random flags, |y| modulo 4: %d hits in %d trials" % (k, hit, _ + 1))
    if ex: print("   e.g.", [sorted(W) for W in ex[0][1:3]], [sorted(W) for W in ex[1][1:3]])
    sys.stdout.flush()
