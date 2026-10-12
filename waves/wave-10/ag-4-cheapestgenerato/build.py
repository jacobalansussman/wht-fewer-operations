# ag-4: build the best known generator of the half-rate space S_k (split on one bit, ends free), replay it exactly
# (whole numbers), and sort its gates by how many hidden wires they touch (the count used by the floor lemma).
import sys
from math import comb
def pc(x): return bin(x).count("1")
class C:
    def __init__(s): s.nin = 0; s.wires = []; s.gates = []   # wire = dict input -> coefficient ; gate = (out, u, v)
    def inp(s):
        s.wires.append({s.nin: 1}); s.nin += 1; return len(s.wires) - 1
    def gate(s, u, a, v, b):
        w = {}
        for i, c in s.wires[u].items(): w[i] = w.get(i, 0) + a * c
        for i, c in s.wires[v].items(): w[i] = w.get(i, 0) + b * c
        s.wires.append({i: c for i, c in w.items() if c}); s.gates.append((len(s.wires) - 1, u, v)); return len(s.wires) - 1
def gen(c, r, k):
    N = 1 << k
    if r <= 0:
        w = c.inp(); return [w] * N                       # degree 0: every output is a copy of one input
    if r >= k: return [c.inp() for _ in range(N)]         # every function: outputs are the inputs
    if r == 1:                                            # values at 0 and at the unit points are the inputs: N - 2 gates
        val = {0: c.inp()}
        for i in range(k): val[1 << i] = c.inp()
        d = {i: c.gate(val[1 << i], 1, val[0], -1) for i in range(1, k)}
        for x in range(1, N):
            if pc(x) >= 2:
                hi = x.bit_length() - 1; val[x] = c.gate(val[x ^ (1 << hi)], 1, d[hi], 1)
        return [val[x] for x in range(N)]
    if r == k - 1:                                        # one relation, sum of (-1)^weight f = 0: N - 2 gates
        val = {x: c.inp() for x in range(N - 1)}
        acc = c.gate(val[0], (-1) ** pc(0), val[1], (-1) ** pc(1))
        for x in range(2, N - 1): acc = c.gate(acc, 1, val[x], (-1) ** pc(x))
        # acc = sum over x < N-1 of sign(x) f(x) ; f(N-1) = -sign(N-1) * acc : a scaling, free ; the last gate above IS the output up to sign
        val[N - 1] = acc; c.scale = getattr(c, "scale", {}); c.scale[acc] = -(-1) ** pc(N - 1)
        return [val[x] for x in range(N)]
    u = gen(c, r, k - 1); v = gen(c, r - 1, k - 1)
    return u + [c.gate(u[y], getattr(c, "scale", {}).get(u[y], 1), v[y], getattr(c, "scale", {}).get(v[y], 1)) for y in range(N // 2)]
def rank_mod(rows, p=1000003):
    rows = [list(r) for r in rows]; rk = 0; ncol = len(rows[0])
    for col in range(ncol):
        piv = next((i for i in range(rk, len(rows)) if rows[i][col] % p), None)
        if piv is None: continue
        rows[rk], rows[piv] = rows[piv], rows[rk]; inv = pow(rows[rk][col], -1, p)
        rows[rk] = [(x * inv) % p for x in rows[rk]]
        for i in range(len(rows)):
            if i != rk and rows[i][col] % p:
                f = rows[i][col]; rows[i] = [(x - f * y) % p for x, y in zip(rows[i], rows[rk])]
        rk += 1
    return rk
for k in (3, 5, 7, 9):
    r = (k - 1) // 2; N = 1 << k
    c = C(); out = gen(c, r, k); sc = getattr(c, "scale", {})
    A = [[sc.get(w, 1) * c.wires[w].get(i, 0) for i in range(c.nin)] for w in out]
    orth = all(sum(A[y][i] * (-1) ** pc(x & y) for y in range(N)) == 0 for x in range(N) if pc(x) > r for i in range(c.nin)) if k <= 7 else "skipped"
    rk = rank_mod(A) if k <= 7 else "skipped"
    outs = set(out); hidden = set(range(len(c.wires))) - outs
    t = [0, 0, 0, 0]
    for g in c.gates: t[sum(1 for w in set(g) if w in hidden)] += 1
    print("k", k, "N", N, "inputs", c.nin, "gates", len(c.gates), "| outputs orthogonal to every character of weight > k/2:", orth,
          "| rank (mod 1000003):", rk, "| distinct output wires", len(outs), "hidden wires", len(hidden),
          "| gates touching 0,1,2,3 hidden wires:", t, "| lemma: N <= 2*t1 + t2:", N, "<=", 2 * t[1] + t[2], "and t1 <= hidden:", t[1] <= len(hidden))
