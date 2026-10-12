# p-1-letter16: EXACT replay of a rectangle list (whole numbers and fractions only).
# input: a file with lines starting "JSON {...}" as printed by rf.py / rr.py.  For each: (1) the rectangles' row sets are nodes of the
# row tree, column sets nodes of the column tree, both families laminar; (2) sum of rectangles == diag(r) H diag(c) exactly;
# (3) builds the circuit (merge tree on inputs, sparse middle, merge tree on outputs backwards), counts its gates (G: a gate is a*u+b*v)
# and replays it on the N basis vectors: every output must be exactly the row of H.
import sys, json
from fractions import Fraction as F
def par(a): return bin(a).count('1') & 1
def run(d):
    N = d['N']; H = [[(-1) ** par(a & x) for x in range(N)] for a in range(N)]
    r = [F(str(v)) for v in d['r']]; c = [F(str(v)) for v in d['c']]
    rown = [tuple(s) for s in d['rown']]; coln = [tuple(s) for s in d['coln']]
    for fam in (rown, coln):
        assert len(fam) == 2 * N - 1 and len(set(fam)) == 2 * N - 1
        for a in fam:
            for b in fam:
                A, B = set(a), set(b); assert not (A & B) or A <= B or B <= A
    rects = [(tuple(a), tuple(b), F(str(v)).limit_denominator(10 ** 6)) for a, b, v in d['rects']]
    assert len(set((a, b) for a, b, v in rects)) == len(rects)
    S = [[F(0)] * N for _ in range(N)]
    for a, b, v in rects:
        assert a in rown and b in coln and v != 0
        for y in a:
            for x in b: S[y][x] += v
    ok = all(S[y][x] == r[y] * H[y][x] * c[x] for y in range(N) for x in range(N))
    tau = len(rects)
    # circuit.  wires are exact vectors of length N (coefficients of the inputs)
    gates = 0
    def lin(a, u, b, v): return [a * p + b * q for p, q in zip(u, v)]
    unit = lambda x: [F(int(i == x)) for i in range(N)]
    form = {}
    def child(fam, s):   # the two children of node s in a laminar family
        sub = [t for t in fam if set(t) < set(s)]; mx = [t for t in sub if not any(set(t) < set(u) for u in sub)]; assert len(mx) == 2; return mx
    def getform(b):
        nonlocal gates
        if b in form: return form[b]
        if len(b) == 1: form[b] = [v * c[b[0]] for v in unit(b[0])]   # scaling of an input: free in count (G)
        else:
            l, rr = child(coln, b); u = getform(l); v = getform(rr); form[b] = lin(F(1), u, F(1), v); gates += 1
        return form[b]
    own = {}
    for a, b, v in rects: own.setdefault(a, []).append((v, b))
    out = [None] * N
    def down(a, cum):    # cum: wire holding the sum of the ancestors' own values (None = zero)
        nonlocal gates
        cur = cum
        for v, b in own.get(a, []):
            f = getform(b)
            if cur is None: cur = [v * p for p in f]            # a scaling, free
            else: cur = lin(F(1), cur, v, f); gates += 1
        if len(a) == 1: out[a[0]] = cur; return
        for ch in child(rown, a): down(ch, cur)
    down(tuple(range(N)), None)
    good = all(out[y] is not None and [r[y] * t for t in out[y]] == [F(h) * (r[y] * r[y]) for h in H[y]] for y in range(N))
    mx = max(abs(v) for a, b, v in rects)
    shapes = {}
    for a, b, v in rects: shapes[(len(a), len(b), str(v))] = shapes.get((len(a), len(b), str(v)), 0) + 1
    print("design", d.get('design'), d.get('tag', ''), " N", N, " tau", tau, " matrix identity exact:", ok, " circuit gates (G):", gates, " N-2+tau:", N - 2 + tau,
          " circuit computes r(y)^2 * row y of H for every y:", good, " largest |number|:", mx)
    print("   scalings r:", [str(v) for v in r], " c:", [str(v) for v in c])
    print("   shapes (rows, columns, number): count ", sorted(shapes.items()))
for fn in sys.argv[1:]:
    for line in open(fn):
        if line.startswith("JSON "): run(json.loads(line[5:]))
