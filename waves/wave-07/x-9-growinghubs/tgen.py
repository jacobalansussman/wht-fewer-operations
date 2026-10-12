#!/usr/bin/env python3
"""x-9-growinghubs/tgen.py  -- the mixed-hub family of e2-0 with a FREE hub coefficient per level.  Count (G).
Exact arithmetic over the Gaussian rationals Q(i) (pairs of Fractions).
A *product wire* on a node (block of m = 2^j consecutive inputs) is  (1,s_1) x ... x (1,s_j): slope s_b on address bit b.
Slope 0 = 'only the first half', INF = 'only the second half'.  Characters are slopes +1/-1 on every bit.
Hub of a node for the lower tuple v (j-2 slopes):  M = (v,+1 on L) + t * (v,-1 on R).
Output (v,p,r) with p = +1 or -1 is ONE gate from M and the witness (v,s) on R (p=+1) or on L (p=-1), s = (r+t)/(r-t).
t for a node = -e * z * tau_j  (e = +1 for a left child or the top, -1 for a right child; z = top slope of v; tau_j free).
tau_j = 1 for all j is e2-0's family.  A second output of the same (v,p) is made by a textbook step from the first and the hub part.
Wires are deduplicated by their vector up to scale, so any coincidence 'the witness is a wire already held' is used automatically.
usage: tgen.py k spec     spec: comma list of tau for levels 2..k (last repeated), each 'a' or 'a+bi' or 'a/b' ; or 'pow2' ; or 'orbit:a'"""
import sys
from fractions import Fraction as F
class G:
    __slots__ = ('a', 'b')
    def __init__(s, a=0, b=0): s.a = F(a); s.b = F(b)
    def __add__(s, o): return G(s.a + o.a, s.b + o.b)
    def __sub__(s, o): return G(s.a - o.a, s.b - o.b)
    def __neg__(s): return G(-s.a, -s.b)
    def __mul__(s, o): return G(s.a * o.a - s.b * o.b, s.a * o.b + s.b * o.a)
    def __truediv__(s, o):
        d = o.a * o.a + o.b * o.b
        return G((s.a * o.a + s.b * o.b) / d, (s.b * o.a - s.a * o.b) / d)
    def __eq__(s, o): return isinstance(o, G) and s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def __bool__(s): return bool(s.a) or bool(s.b)
    def __repr__(s): return str(s.a) if not s.b else '(%s%+si)' % (s.a, s.b)
ZERO, ONE, MONE, I = G(0), G(1), G(-1), G(0, 1)
INF = 'inf'
def parse(x):
    x = x.strip()
    if x.endswith('i'):
        body = x[:-1]
        if body in ('', '+'): return G(0, 1)
        if body == '-': return G(0, -1)
        for pos in range(len(body) - 1, 0, -1):
            if body[pos] in '+-':
                im = body[pos:]; im = im + '1' if im in '+-' else im
                return G(F(body[:pos]), F(im))
        return G(0, F(body))
    return G(F(x))
k = int(sys.argv[1]); N = 1 << k; spec = sys.argv[2]
def cay(t): return (ONE + t) / (ONE - t)
if spec == 'pow2': taus = {j: G(2 ** j) for j in range(2, k + 1)}
elif spec == 'powN': taus = {j: G(2 ** (2 ** (j - 1))) for j in range(2, k + 1)}
elif spec.startswith('orbit:'):
    t = parse(spec[6:]); orb = [t]
    for _ in range(3): orb.append(cay(orb[-1]))
    taus = {j: orb[(j - 2) % 4] for j in range(2, k + 1)}
else:
    lst = [parse(x) for x in spec.split(',')]
    taus = {j: lst[min(j - 2, len(lst) - 1)] for j in range(2, k + 1)}
vec = {}; byvec = {}; prog = []; memo = {}; first = {}; hubs = {}; cnt = [0]; kinds = {}
def norm(v):
    for x in v:
        if x: return tuple(y / x for y in v)
for i in range(N):
    v = tuple(ONE if i == j else ZERO for j in range(N)); vec[('x', i)] = v; byvec[norm(v)] = ('x', i)
def prodvec(lo, m, tup):
    v = [ZERO] * N; j = len(tup)
    for pos in range(m):
        c = ONE; dead = False
        for b in range(j):
            bit = (pos >> b) & 1; s = tup[b]
            if s is INF:
                if not bit: dead = True; break
            elif bit: c = c * s
        if not dead: v[lo + pos] = c
    return tuple(v)
def solve2(u, v, p):
    for i in range(N):
        for j in range(i + 1, N):
            det = u[i] * v[j] - u[j] * v[i]
            if det:
                a = (p[i] * v[j] - p[j] * v[i]) / det; b = (u[i] * p[j] - u[j] * p[i]) / det
                return (a, b) if all(a * u[t] + b * v[t] == p[t] for t in range(N)) else None
    return None
def gate(target, n1, n2, kind):
    nk = norm(target)
    if nk in byvec: return byvec[nk]                      # coincidence: already held
    s = solve2(vec[n1], vec[n2], target)
    assert s is not None and s[0] and s[1], ('gate failed', kind, n1, n2)
    cnt[0] += 1; nm = (kind, cnt[0]); vec[nm] = target; byvec[nk] = nm; prog.append((nm, s[0], n1, s[1], n2))
    kinds[kind] = kinds.get(kind, 0) + 1; return nm
def tcoef(lo, m, v, e):
    j = m.bit_length() - 1
    z = v[-1] if (v and v[-1] in (ONE, MONE)) else ONE
    return -(ONE if e > 0 else MONE) * z * taus[j]
def need(lo, m, tup, e=1):
    """wire for the product (tup) on node [lo, lo+m); e = +1 if the node is a left child or the top, -1 if a right child"""
    j = len(tup)
    if j == 0: return ('x', lo)
    top = tup[-1]
    if top is INF: return need(lo + m // 2, m // 2, tup[:-1], -1)
    if top == ZERO: return need(lo, m // 2, tup[:-1], 1)
    key = (lo, m, tup)
    if key in memo: return memo[key]
    target = prodvec(lo, m, tup); nk = norm(target)
    if nk in byvec: memo[key] = byvec[nk]; return byvec[nk]
    h = m // 2
    if j == 1: w = gate(target, ('x', lo), ('x', lo + 1), 'pair')
    else:
        v = tup[:-2]; p = tup[-2]; r = top
        if p in (ONE, MONE):
            ck = (lo, m, v, p)
            if ck in first:                               # textbook step from the first output of this (v,p) and the hub part
                part = need(lo, h, v + (ONE,), 1) if p == ONE else need(lo + h, h, v + (MONE,), -1)
                w = gate(target, first[ck], part, 'step')
            else:
                hk = (lo, m, v)
                if hk not in hubs:
                    A = need(lo, h, v + (ONE,), 1); B = need(lo + h, h, v + (MONE,), -1); t = tcoef(lo, m, v, e)
                    hubs[hk] = (gate(tuple(x + t * y for x, y in zip(vec[A], vec[B])), A, B, 'hub'), t)
                M, t = hubs[hk]
                s = INF if r == t else (r + t) / (r - t)
                wit = need(lo + h, h, v + (s,), -1) if p == ONE else need(lo, h, v + (s,), 1)
                w = gate(target, M, wit, 'out'); first[ck] = w
        else:
            a = need(lo, h, tup[:-1], 1); b = need(lo + h, h, tup[:-1], -1); w = gate(target, a, b, 'join')
    memo[key] = w; return w
import itertools
outs = []
for tup in itertools.product((ONE, MONE), repeat=k):
    if tup[-1] == ONE: outs.append(need(0, N, tup))
for tup in itertools.product((ONE, MONE), repeat=k):
    if tup[-1] == MONE: outs.append(need(0, N, tup))
# exact replay from scratch
val = {('x', i): [ONE if i == j else ZERO for j in range(N)] for i in range(N)}
for nm, a, u, b, w in prog: val[nm] = [a * s + b * t for s, t in zip(val[u], val[w])]
rows = set()
for o in outs:
    t = val[o]
    assert all(x in (ONE, MONE) for x in t)
    rows.add(tuple(1 if x == ONE else -1 for x in t))
def par(w, x): return -1 if bin(w & x).count('1') & 1 else 1
ok = rows == {tuple(par(w, x) for x in range(N)) for w in range(N)}
import math
big = max(max(abs(c.a), abs(c.b)) for _, a, _, b, _ in prog for c in (a, b))
# volume ledger: sum of log2(|a|+|b|) with the gate scaled so that the smaller coefficient is 1 (real case only, rough)
print('N %d spec %s gates %d  rate gates/(N log2 N) = %.4f  family %d textbook %d  all %d rows of H exact: %s  kinds %s  largest coefficient %s'
      % (N, spec, len(prog), len(prog) / (N * k), 3 * N * k // 4 + N // 4, N * k, N, ok, dict(sorted(kinds.items())), big))
if len(sys.argv) > 3:
    with open(sys.argv[3], 'w') as f:
        f.write('# count (G), %d points, %d gates, hub coefficients tau = %s ; name = a*u + b*v\n' % (N, len(prog), spec))
        for nm, a, u, b, w in prog: f.write('%s%d = %r * %s%d + %r * %s%d\n' % (nm[0], nm[1], a, u[0], u[1], b, w[0], w[1]))
