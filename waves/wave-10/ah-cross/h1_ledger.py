# Hybrid 1: the class ledger. Kernel (1,1;1,tau), 4 points, target rows tau^(common ones). Exact (fractions, whole numbers).
# Wires are kept as primitive polynomial vectors (common polynomial factor removed). A gate w' = (a u' + b v')/c has
# weight max(deg a, deg b) - deg c. Tested: after each gate the largest degree of a minor of the matrix of all wires
# rises by at most max(0, weight); the 4x4 minor on the outputs has degree N k / 2 = 4.
# Degrees of minors are read by evaluating at tau = 10^9 (coefficients here are far below 10^9).
from fractions import Fraction as F
import itertools, math
N = 4; T = 10**9
def trim(p):
    p = list(p)
    while p and p[-1] == 0: p.pop()
    return p
def add(p, q):
    n = max(len(p), len(q)); return trim([(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(n)])
def mul(p, q):
    if not p or not q: return []
    r = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q): r[i + j] += a * b
    return trim(r)
def mod(p, q):
    p = list(p)
    while len(p) >= len(q) and p:
        f = p[-1] / q[-1]; s = len(p) - len(q)
        for i, b in enumerate(q): p[s + i] -= f * b
        p = trim(p)
    return p
def gcd(p, q):
    while q: p, q = q, mod(p, q)
    return [c / p[-1] for c in p] if p else []
def ev(p): return sum(c * T ** i for i, c in enumerate(p))
def deg(p): return len(p) - 1
def content(v):
    g = []
    for p in v: g = gcd(g, p) if g else ([c / p[-1] for c in p] if p else [])
    return g
def det(M):
    n = len(M)
    if n == 1: return M[0][0]
    return sum((-1) ** j * M[0][j] * det([r[:j] + r[j + 1:] for r in M[1:]]) for j in range(n) if M[0][j])
def fdeg(d): return round((math.log(abs(d.numerator)) - math.log(d.denominator)) / math.log(T))
def maxdeg(rows):
    best = 0
    for m in range(1, N + 1):
        for R in itertools.combinations(range(len(rows)), m):
            for C in itertools.combinations(range(N), m):
                d = det([[rows[r][c] for c in C] for r in R])
                if d: best = max(best, fdeg(d))
    return best
def run(name, gates, outs):
    raw = {'x%d' % i: [[F(1)] if j == i else [] for j in range(N)] for i in range(N)}
    cd = {w: 0 for w in raw}                     # degree of the content of each raw wire
    prim = lambda w: [F(ev(p)) / F(ev(content(raw[w]))) for p in raw[w]]
    rows = [prim('x%d' % i) for i in range(N)]
    delta = 0; tot = 0; pos = 0; ws = []; ok = True
    for (g, a, u, b, v) in gates:
        raw[g] = [add(mul(a, raw[u][j]), mul(b, raw[v][j])) for j in range(N)]
        cd[g] = deg(content(raw[g]))
        w = max(deg(a) + cd[u], deg(b) + cd[v]) - cd[g]
        rows.append(prim(g)); nd = maxdeg(rows)
        if nd > delta + max(0, w): ok = False
        delta = nd; tot += max(0, w); pos += (w > 0); ws.append(w)
    tgt = all(raw[outs[y]] == [[F(0)] * bin(x & y).count('1') + [F(1)] for x in range(N)] for y in range(N))
    D = det([prim(outs[y]) for y in range(N)])
    print(f"{name}: gates {len(gates)}; computes the target: {tgt}; weights {ws}; sum of positive weights {tot}; "
          f"gates of positive weight {pos}; largest minor degree at the end {delta}; degree of the output determinant {fdeg(D)}; "
          f"'a minor rises by at most the weight' held at every gate: {ok}")
one = [F(1)]; t = [F(0), F(1)]; m1 = [F(-1)]; omt = [F(1), F(-1)]; tmo = [F(-1), F(1)]
run("textbook", [('p0',one,'x0',one,'x1'),('p1',one,'x0',t,'x1'),('p2',one,'x2',one,'x3'),('p3',one,'x2',t,'x3'),
     ('y0',one,'p0',one,'p2'),('y2',one,'p0',t,'p2'),('y1',one,'p1',one,'p3'),('y3',one,'p1',t,'p3')], ['y0','y1','y2','y3'])
run("seven gates (ag-6's wiring, general tau)", [('a',one,'x0',one,'x1'),('b',one,'x2',one,'x3'),('y0',one,'a',one,'b'),
     ('y2',one,'a',t,'b'),('h',omt,'x0',t,'y0'),('y1',one,'h',omt,'x2'),('y3',one,'h',mul(t,tmo),'x3')], ['y0','y1','y2','y3'])
run("eight gates (ae-cross / ag-8)", [('g1',one,'x0',t,'x1'),('g2',one,'x2',t,'x3'),('g3',one,'g1',one,'g2'),('g4',one,'x1',one,'x3'),
     ('g5',one,'g3',omt,'g4'),('g6',one,'g3',tmo,'g2'),('g7',one,'x1',m1,'x2'),('g8',one,'g3',omt,'g7')], ['g5','g3','g8','g6'])
run("nine gates, one gate of weight 2 (mine)", [('a',one,'x0',one,'x1'),('b',one,'x2',one,'x3'),('y0',one,'a',one,'b'),
     ('c',one,'x1',one,'x3'),('y1',one,'y0',tmo,'c'),('y2',one,'y0',tmo,'b'),('q',one,'y1',one,'y2'),('q2',one,'q',m1,'y0'),
     ('y3',one,'q2',mul(tmo,tmo),'x3')], ['y0','y1','y2','y3'])
