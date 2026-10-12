# u-7-quotient, run A: exact integer arithmetic only (ranks by fraction-free elimination on small integer vectors).
# 1. parallelograms among outputs (the reason for m-cross's circularity), 8 to 64 points
# 2. the partner bound: a vector with entries 0,+1,-1 on a set D that is +-(an output) on D for m outputs has m <= N / 2^dim(affine span of D)
# 3. 8 points, every vector q with entries 0,+1,-1 (= every quotient of two parents congruent to one output modulo 4):
#    how many outputs is it one gate from, partner taken in a stock (any coefficients: a rank test)
import sys, re, itertools
from fractions import Fraction as F
def had(N): return [[(-1)**bin(y & x).count('1') for x in range(N)] for y in range(N)]
def rank(rows):
    rows = [list(r) for r in rows]; rk = 0; n = len(rows[0])
    for c in range(n):
        p = next((i for i in range(rk, len(rows)) if rows[i][c] != 0), None)
        if p is None: continue
        rows[rk], rows[p] = rows[p], rows[rk]
        for i in range(rk + 1, len(rows)):
            if rows[i][c] != 0:
                a, b = rows[rk][c], rows[i][c]
                rows[i] = [a * y - b * x for x, y in zip(rows[rk], rows[i])]
        rk += 1
        if rk == len(rows): break
    return rk
def parse(path):
    gates = []
    for line in open(path, errors='replace'):
        line = line.split('#')[0].strip()
        if '=' not in line: continue
        name, rhs = line.split('=', 1); name = name.strip(); rhs = rhs.replace(' ', '')
        m = re.fullmatch(r'([+-]?[\d/]*)\*?([A-Za-z_]\w*)(\+-|\+|-)([\d/]*)\*?([A-Za-z_]\w*)', rhs)
        def coef(s): return F(1) if s in ('', '+') else F(-1) if s == '-' else F(s)
        gates.append((name, coef(m.group(1)), m.group(2), coef(m.group(4)) * (-1 if '-' in m.group(3) else 1), m.group(5)))
    return gates
def wires(path, N):
    W = {'x%d' % i: [F(int(i == j)) for j in range(N)] for i in range(N)}
    for (name, a, u, b, v) in parse(path): W[name] = [a * p + b * q for p, q in zip(W[u], W[v])]
    return W
def norm(v):   # sign-normalise an integer vector
    v = tuple(int(t) for t in v); l = next((t for t in v if t), 0)
    return v if l >= 0 else tuple(-t for t in v)
base = sys.argv[1]
print('1. parallelograms among outputs: pairs {a,b} != {c,d} with h_a - h_b = +-(h_c - h_d)')
for N in (8, 16, 32, 64):
    H = had(N); seen = {}; par = 0
    for a in range(N):
        for b in range(a + 1, N):
            d = norm([H[a][x] - H[b][x] for x in range(N)])
            if d in seen: par += 1
            seen[d] = (a, b)
    print('  N=%d: pairs %d, coincidences %d' % (N, N * (N - 1) // 2, par))
print('2. partner bound at 8 points, all 3280 vectors with entries 0,+-1 up to sign')
N = 8; H = had(N); tab = {}; viol = 0; eq = 0
def dimaff(D):
    D = list(D); x0 = D[0]; basis = []
    for x in D[1:]:
        v = x ^ x0
        for b in basis: v = min(v, v ^ b)
        if v: basis.append(v)
    return len(basis)
forms = []
for q in itertools.product((0, 1, -1), repeat=N):
    if not any(q) or norm(q) != q: continue
    forms.append(q)
    D = [x for x in range(N) if q[x]]
    served = [y for y in range(N) if len({q[x] * H[y][x] for x in D}) == 1]
    m = len(served); da = dimaff(D)
    if m > N // 2**da: viol += 1
    if m * len(D) == N: eq += 1
    key = (len(D), m); tab[key] = tab.get(key, 0) + 1
print('  violations of m <= N/2^dimaff: %d ; forms with m*|D| = N: %d' % (viol, eq))
print('  (|D|, outputs it is a restriction of): count ', sorted(tab.items()))
print('3. 8 points: outputs one gate from q (rank test h in span(q, s)), s in a stock')
W19 = wires(base + '/g-1-tightwires/h8_19gates.txt', 8)
names = list(W19)
for y in range(8): assert norm(W19['y%d' % y]) == norm(H[y]), y
stocks = {'inputs+g1..g7 (tree and centre, 15 wires)': ['x%d' % i for i in range(8)] + ['g%d' % i for i in range(1, 8)],
          'all non-output wires of the 19 (19 wires)': [n for n in names if not n.startswith('y')]}
for label, st in stocks.items():
    S = [[int(t) for t in W19[n]] for n in st]; Sset = {norm(s) for s in S}
    dist = {}; best = []
    for q in forms:
        if q in Sset: continue
        cnt = 0; who = []
        for y in range(N):
            for i, s in enumerate(S):
                if rank([q, H[y], s]) == 2:
                    cnt += 1; who.append((y, st[i])); break
        key = (sum(1 for t in q if t), cnt); dist[key] = dist.get(key, 0) + 1
        best.append((cnt, q, who))
    best.sort(reverse=True)
    print('  stock = %s' % label)
    print('    (support size of q, outputs one gate away): count ', sorted(dist.items()))
    for cnt, q, who in best[:6]: print('    best: serves %d  q=%s  with %s' % (cnt, q, who))
    # same question for sign vectors only, split by whether q is one gate from the stock itself
    one = 0; tot = 0; mx1 = 0
    for cnt, q, who in best:
        if all(q):
            tot += 1
            made = any(rank([q, S[i], S[j]]) == 2 for i in range(len(S)) for j in range(i))
            if made: one += 1; mx1 = max(mx1, cnt)
    print('    sign vectors not in stock: %d ; of them one gate from the stock: %d ; most outputs served by one of those: %d' % (tot, one, mx1))
