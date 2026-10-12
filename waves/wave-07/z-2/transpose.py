# z-2: the transposition rule in count (G), checked by my own code, exact arithmetic (fractions / Gaussian whole numbers).
# Count (G): a gate is a*u + b*v, scalings free.  Rule: a program with g gates for an m x n matrix M (no zero row or column,
# every output a gate, outputs distinct gates) turns into a program with g + m - n gates for the transpose of M.
import random, sys, re
from fractions import Fraction
random.seed(11)

def run(n, gates, outs):
    # gates: list of (a, u, b, v); wires 0..n-1 inputs, n.. gates.  returns the matrix rows of outs
    w = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for (a, u, b, v) in gates:
        w.append([a * p + b * q for p, q in zip(w[u], w[v])])
    return [w[o] for o in outs]

def transpose(n, gates, outs):
    """Reverse every edge.  Node with out-edges e_1..e_d (to consumers c_i with weights w_i) becomes the sum of
    w_i * (value of c_i in the reversed program): d - 1 gates, plus one more if the node is itself an output."""
    W = n + len(gates)
    cons = [[] for _ in range(W)]
    for gi, (a, u, b, v) in enumerate(gates):
        cons[u].append((a, n + gi)); cons[v].append((b, n + gi))
    m = len(outs)
    # new inputs: one per output, in order; an output node that is also consumed adds its own input
    newg = []; val = {}        # val[node] = (scale, new wire index): reversed value of node = scale * wire
    own = {}
    for j, o in enumerate(outs): own.setdefault(o, []).append(j)
    for node in range(W - 1, -1, -1):
        terms = [(Fraction(1), j) for j in own.get(node, [])]
        for (wgt, c) in cons[node]:
            if c in val:
                s, idx = val[c]; terms.append((wgt * s, idx))
        terms = [t for t in terms if t[0] != 0]
        if not terms: continue
        if len(terms) == 1:
            val[node] = terms[0]; continue
        (s0, i0) = terms[0]
        cur = None
        for (s1, i1) in terms[1:]:
            if cur is None: newg.append((s0, i0, s1, i1))
            else: newg.append((Fraction(1), cur, s1, i1))
            cur = m + len(newg) - 1
        val[node] = (Fraction(1), cur)
    # outputs of the reversed program: the n old inputs
    rows = []
    w = [[Fraction(int(i == j)) for j in range(m)] for i in range(m)]
    for (a, u, b, v) in newg:
        w.append([a * p + b * q for p, q in zip(w[u], w[v])])
    for i in range(n):
        s, idx = val[i]
        rows.append([s * e for e in w[idx]])
    return newg, rows

print("== random programs: g gates for an m x n matrix; the reversed program, its gate count, its matrix ==")
allok = True; stats = {}
for trial in range(400):
    n = random.randint(2, 7); g = random.randint(n, 22)
    gates = []
    for i in range(g):
        u = random.randrange(n + i); v = random.randrange(n + i)
        if u == v: v = (v + 1) % (n + i) if n + i > 1 else v
        gates.append((Fraction(random.choice([-3, -2, -1, 1, 2, 3])), u, Fraction(random.choice([-3, -2, -1, 1, 2, 3])), v))
    used = set()
    for (a, u, b, v) in gates: used |= {u, v}
    sinks = [n + i for i in range(g) if (n + i) not in used]
    extra = random.sample(range(n, n + g), k=random.randint(0, 2))
    outs = list(dict.fromkeys(sinks + extra))
    if not all(i in used for i in range(n)): continue
    M = run(n, gates, outs)
    if any(all(e == 0 for e in r) for r in M) or any(all(r[j] == 0 for r in M) for j in range(n)): continue
    newg, MT = transpose(n, gates, outs)
    m = len(outs)
    good = all(MT[i][j] == M[j][i] for i in range(n) for j in range(m))
    d = len(newg) - (g + m - n)
    stats[d] = stats.get(d, 0) + 1
    allok &= good
print("reversed program computes the transpose in every case:", allok, "; (gates of reversed) - (g + m - n):", sorted(stats.items()))
print("   (a negative difference means the reversed program is SHORTER: a cancellation made some gate of the original useless)")

print("== the 19-gate 8-point circuit reversed ==")
txt = open('waves/wave-03/g-1-tightwires/h8_19gates.txt').read().splitlines()
names = {f'x{i}': i for i in range(8)}; gates = []
for line in txt:
    line = line.split('#')[0].strip()
    if not line: continue
    lhs, rhs = [s.strip() for s in line.split('=')]
    toks = rhs.replace('-', ' - ').replace('+', ' + ').split()
    terms = []; sign = 1
    for t in toks:
        if t == '+': sign = 1
        elif t == '-': sign = -1
        else:
            if '*' in t: c, nm = t.split('*'); c = int(c)
            else: c, nm = 1, t
            terms.append((Fraction(sign * c), names[nm])); sign = 1
    (a, u), (b, v) = terms
    names[lhs] = 8 + len(gates); gates.append((a, u, b, v))
outs = [names[f'y{j}'] for j in range(8)]
M = run(8, gates, outs)
H = [[1 - 2 * (bin(j & x).count('1') & 1) for x in range(8)] for j in range(8)]
print("original:", len(gates), "gates; computes H exactly:", M == H)
newg, MT = transpose(8, gates, outs)
print("reversed:", len(newg), "gates; computes H^T = H exactly:", MT == H)

print("== hybrid 1: H(x,y) = i^|x| * (-i)^|x+y| * i^|y| for EVERY k (Gaussian; no need for k even) ==")
for k in range(1, 9):
    N = 1 << k; wt = [bin(x).count('1') for x in range(N)]
    ok = all(((wt[x] + wt[y] - wt[x ^ y]) % 4) == 2 * (bin(x & y).count('1') & 1) for x in range(N) for y in range(N))
    print(f"k={k}: {ok}", end='; ')
print()

print("== hybrid 2: V = (sum and difference on exchanged pairs)(half transform); V H' V^T diagonal; H' = N V^T diag^-1 V ==")
def matmul(A, B):
    Bt = list(zip(*B)); return [[sum(a * b for a, b in zip(r, c)) for c in Bt] for r in A]
for h in (1, 2, 3, 4):
    k = 2 * h; N = 1 << k; s = 1 << h
    dot = lambda x, y: bin(x & y).count('1') & 1
    # address = (a, b) -> a * s + b ; H'((a,b),(a',b')) = (-1)^(a.b' + b.a')
    Hp = [[1 - 2 * (dot(x >> h, y & (s - 1)) ^ dot(x & (s - 1), y >> h)) for y in range(N)] for x in range(N)]
    F = [[(1 - 2 * dot(x >> h, y >> h)) if (x & (s - 1)) == (y & (s - 1)) else 0 for y in range(N)] for x in range(N)]
    B = [[0] * N for _ in range(N)]; pair_gates = 0
    for a in range(s):
        for b in range(s):
            x = a * s + b; y = b * s + a
            if a == b: B[x][x] = 1
            elif a < b:
                B[x][x] = 1; B[x][y] = 1; B[y][x] = 1; B[y][y] = -1; pair_gates += 2
    V = matmul(B, F)
    VT = [list(r) for r in zip(*V)]
    Dg = matmul(matmul(V, Hp), VT)
    diag = all(Dg[i][j] == 0 for i in range(N) for j in range(N) if i != j)
    vals = sorted(set(Dg[i][i] for i in range(N)))
    if N <= 64:
        R = matmul([[Fraction(N * VT[i][j], Dg[j][j]) for j in range(N)] for i in range(N)], V)
        back = all(R[i][j] == Hp[i][j] for i in range(N) for j in range(N))
    else:
        back = 'not run at this size'
    print(f"N={N}: diagonal: {diag}, values {vals}; H' = N V^T diag^-1 V: {back}; pair gates {pair_gates} = N - sqrt N = {N - s}")
