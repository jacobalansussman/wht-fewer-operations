# ai-2: own check of the class ledger at 8 points.  Kernel (1, t; t, 1): entries t^(Hamming distance).  Exact (fractions).
# Wires of the 19-gate wiring as monomial vectors (exponents read from ag-6's t = 3 listing, where every entry is a power of 3);
# every gate is then SOLVED as c*w = a*u + b*v with polynomials a, b, c (identity in t checked on every coordinate).
from fractions import Fraction as F
import itertools, random, math
def trim(p):
    while p and p[-1] == 0: p.pop()
    return p
def add(p, q): return trim([(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(max(len(p), len(q)))])
def neg(p): return [-c for c in p]
def mul(p, q):
    if not p or not q: return []
    r = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q): r[i + j] += a * b
    return trim(r)
def divmod_(p, q):
    p = list(p); out = [F(0)] * max(1, len(p) - len(q) + 1)
    while len(p) >= len(q) and p:
        f = p[-1] / q[-1]; s = len(p) - len(q); out[s] = f
        for i, b in enumerate(q): p[s + i] -= f * b
        trim(p)
    return trim(out), p
def gcd(p, q):
    p, q = list(p), list(q)
    while q: p, q = q, divmod_(p, q)[1]
    return [c / p[-1] for c in p] if p else []
def mono(e): return [F(0)] * e + [F(1)]
E = {"g1": (1,None,None,None,None,None,None,0), "g2": (None,1,None,None,None,None,0,None), "g3": (None,None,0,None,None,1,None,None),
     "g4": (None,None,None,0,1,None,None,None), "g5": (1,2,None,None,None,None,1,0), "g6": (None,None,1,0,1,2,None,None),
     "g7": (1,2,2,1,2,3,1,0), "g8": (0,1,1,0,1,2,0,1), "g9": (1,2,2,1,2,1,1,0), "g10": (0,1,1,0,1,2,2,1), "g11": (1,2,2,1,0,1,1,0),
     "y7": (0,1,1,2,3,2,2,1), "y1": (1,2,0,1,2,1,3,2), "y6": (2,1,3,2,1,2,0,1), "y0": (3,2,2,1,0,1,1,2), "y2": (1,0,2,1,2,3,1,2),
     "y4": (2,1,1,0,1,2,2,3), "y3": (1,2,2,3,2,1,1,0), "y5": (2,3,1,2,1,0,2,1)}
wiring = [("g1","x0","x7"),("g2","x1","x6"),("g3","x2","x5"),("g4","x3","x4"),("g5","g1","g2"),("g6","g3","g4"),("g7","g5","g6"),
          ("g8","g7","x7"),("g9","g7","x5"),("g10","g8","x6"),("g11","g9","x4"),("y7","g10","g4"),("y3","g9","x3"),("y5","y3","g5"),
          ("y1","g10","g3"),("y6","g11","g2"),("y2","g8","x1"),("y4","y2","g6"),("y0","g11","g1")]
W = {f"x{i}": [mono(0) if j == i else [] for j in range(8)] for i in range(8)}
for nm, ex in E.items(): W[nm] = [mono(e) if e is not None else [] for e in ex]
def solve(u, v, w):
    for i in range(8):
        for j in range(i + 1, 8):
            d = add(mul(u[i], v[j]), neg(mul(u[j], v[i])))
            if d:
                a = add(mul(w[i], v[j]), neg(mul(w[j], v[i]))); b = add(mul(u[i], w[j]), neg(mul(u[j], w[i])))
                g = gcd(gcd(a, b), d)
                a, b, c = divmod_(a, g)[0], divmod_(b, g)[0], divmod_(d, g)[0]
                if all(mul(c, w[x]) == add(mul(a, u[x]), mul(b, v[x])) for x in range(8)): return a, b, c
                return None
    return None
def show(p): return "(" + " + ".join(f"{c}*t^{i}" for i, c in enumerate(p) if c) + ")"
tot = 0; hist = {}; gates = []
for nm, u, v in wiring:
    s = solve(W[u], W[v], W[nm])
    if s is None: print("gate", nm, "is NOT a combination of", u, v); continue
    a, b, c = s; wt = max(len(a), len(b)) - len(c); tot += max(0, wt); hist[wt] = hist.get(wt, 0) + 1; gates.append((nm, u, v, wt))
    print(f"  {nm:4s} = ({show(a)}*{u} + {show(b)}*{v}) / {show(c)}   weight {wt}")
# outputs: rows t^(distance) of the kernel power, up to one relabelling of the 8 addresses
ys = [tuple(E[f"y{j}"]) for j in range(8)]; target = {tuple(bin(x ^ j).count("1") for x in range(8)) for j in range(8)}
perm = next((p for p in itertools.permutations(range(8)) if {tuple(y[p[x]] for x in range(8)) for y in ys} == target), None)
print(f"the 8 outputs are the rows t^(distance) after the relabelling {perm}: {perm is not None}")
print(f"19 gates as an identity in t: weights {dict(sorted(hist.items()))}; sum of positive weights {tot}; the determinant (1 - t^2)^12 has degree 24")
# the inequality of the proof, minor by minor: deg M_w <= weight + max(deg M_u, deg M_v), on sampled 8 x 8 minors (t = 10^12, exact)
T = 10 ** 12
def ev(p): return sum(int(c) * T ** i for i, c in enumerate(p))
def det(M):
    M = [r[:] for r in M]; n = len(M); sign = 1; prev = 1
    for i in range(n):
        p = next((r for r in range(i, n) if M[r][i]), None)
        if p is None: return 0
        if p != i: M[i], M[p] = M[p], M[i]; sign = -sign
        for r in range(i + 1, n):
            for c in range(i + 1, n): M[r][c] = (M[r][c] * M[i][i] - M[r][i] * M[i][c]) // prev
        prev = M[i][i]
    return sign * M[n - 1][n - 1]
def deg(d): return None if d == 0 else round(math.log(abs(d)) / math.log(T))
N_ = {k: [ev(p) for p in v] for k, v in W.items()}; names = [f"x{i}" for i in range(8)]; random.seed(5); bad = 0; tested = 0; tight = 0
for nm, u, v, wt in gates:
    for _ in range(250):
        others = random.sample(names, 7)
        dw = deg(det([N_[nm]] + [N_[o] for o in others]))
        if dw is None: continue
        du = deg(det([N_[u]] + [N_[o] for o in others])); dv = deg(det([N_[v]] + [N_[o] for o in others]))
        m = max(x for x in (du, dv) if x is not None); tested += 1
        if dw > wt + m: bad += 1
        if dw == wt + m: tight += 1
    names.append(nm)
print(f"sampled 8 x 8 minors through the new wire: {tested} non-zero; 'degree rises by at most the weight' violated {bad} times; attained {tight} times")
print("degree of the determinant of the 8 outputs:", deg(det([N_[f'y{j}'] for j in range(8)])))
