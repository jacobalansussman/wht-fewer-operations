# ag-4: least gates (G) over ALL generators of the space of polynomials of degree <= 1 at the 2^k cube points, modulo p.
# Reformulation used (derived in ag-4.md): a generator circuit with n inputs and G gates is a set of n + G points of the
# projective space of dimension n - 1 that CONTAINS the N "cube points" (1, y) and can be built from n of its points by
# adding, one at a time, a point on the line through two points already present. h = G - (N - n) points are not cube
# points ("hidden wires"). So: for every set W of h extra points, is cube + W buildable from n of its points?
# Exhaustive over W modulo p. usage: rig.py p k h [all]
import sys, itertools
p = int(sys.argv[1]); k = int(sys.argv[2]); h = int(sys.argv[3]); showall = len(sys.argv) > 4
n = k + 1; N = 1 << k
def canon(v):
    for c in v:
        if c % p:
            inv = pow(c, -1, p); return tuple((x * inv) % p for x in v)
    return None
cube = [tuple([1] + [(y >> i) & 1 for i in range(k)]) for y in range(N)]
cubeset = {c: i for i, c in enumerate(cube)}
allpts = set()
for v in itertools.product(range(p), repeat=n):
    c = canon(v)
    if c: allpts.add(c)
others = sorted(allpts - set(cube))
# sanity: no three cube points on a line (needs p odd)
bad = 0
for a, b in itertools.combinations(cube, 2):
    for t in range(1, p):
        c = canon(tuple((a[i] + t * b[i]) % p for i in range(n)))
        if c in cubeset and c != a and c != b: bad += 1
print("p", p, "k", k, "N", N, "n", n, "points of the projective space", len(allpts), "| collinear cube triples:", bad)
def chords(w):   # pairs of cube points whose line passes through w
    res = set()
    for a in cube:
        for t in range(1, p):
            c = canon(tuple((a[i] + t * w[i]) % p for i in range(n)))
            if c in cubeset and c != a:
                res.add(frozenset((cubeset[a], cubeset[c])))
    return [tuple(sorted(s)) for s in res]
ch = {w: chords(w) for w in others}
print("largest number of cube chords through one extra point:", max(len(v) for v in ch.values()),
      "| extra points with at least 2 chords:", sum(1 for v in ch.values() if len(v) >= 2))
def buildable(W):
    # points: 0..N-1 cube, N..N+h-1 hidden. triples = collinear triples.
    P = N + len(W); G = P - n
    tr = []
    for j, w in enumerate(W):
        for (a, b) in ch[w]: tr.append((a, b, N + j))
    for j1, j2 in itertools.combinations(range(len(W)), 2):
        w1, w2 = W[j1], W[j2]
        for t in range(1, p):
            c = canon(tuple((w1[i] + t * w2[i]) % p for i in range(n)))
            if c in cubeset: tr.append((cubeset[c], N + j1, N + j2))
            else:
                for j3 in range(len(W)):
                    if j3 > j2 and W[j3] == c: tr.append((N + j1, N + j2, N + j3))
    if len(tr) < G: return None
    on = set()
    for t3 in tr: on.update(t3)
    forced = [x for x in range(P) if x not in on]      # on no line: must be inputs
    if len(forced) > n: return None
    rest = [x for x in range(P) if x in on]
    for extra in itertools.combinations(rest, n - len(forced)):
        have = set(forced) | set(extra); order = []
        changed = True
        while changed and len(have) < P:
            changed = False
            for t3 in tr:
                inn = [x for x in t3 if x in have]
                if len(inn) == 2:
                    new = [x for x in t3 if x not in have][0]
                    have.add(new); order.append((new, tuple(inn))); changed = True
        if len(have) == P: return (sorted(set(forced) | set(extra)), order)
    return None
found = 0; tried = 0
for W in itertools.combinations(others, h):
    tried += 1
    r = buildable(W)
    if r:
        found += 1
        if found <= 2 or showall:
            print("YES with", N - n + h, "gates: hidden points", W, "| inputs", r[0], "| gates (new, from):", r[1])
print("h =", h, "gates =", N - n + h, ": sets of hidden points tried", tried, "| buildable:", found)
