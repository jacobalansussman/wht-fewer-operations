#!/usr/bin/env python3
"""c-0 verify.py: my own replay of g-1's claims.  Nothing imported from g-1's programs; only the text file
h8_19gates.txt is read (and parsed with my own parser).

Count (G): a gate is any a*u + b*v, scalings free.
Count (O): OpenAI's circuit model, R/OAI/Computability/FourierCircuit/Core.lean:
    Gate = add i j | sub i j | scale c i ; each gate costs 1 ; the wire list is  inputs (n of them), then the constant 0,
    then one new wire per gate ; outputs NAME wires (no charge for permutations or fan-out) ; the circuit must compute
    the matrix itself (Circuit.Computes: C.eval x = A.mulVec x), not a multiple of it.
Here the programs are built as explicit lists of such gates and evaluated with exactly that semantics.
"""
import re, sys
from fractions import Fraction as F

SRC = "waves/wave-03/g-1-tightwires/h8_19gates.txt"

def chi(j, x): return -1 if bin(j & x).count("1") & 1 else 1

# ---------------------------------------------------------------- (G) parse and replay the published text file
def parse_G(path):
    gates = []
    term = re.compile(r"\s*([+-]?)\s*(?:(\d+)\s*\*\s*)?([a-z]\d+)")
    for line in open(path):
        line = line.split("#")[0].strip()
        if not line: continue
        name, rhs = [s.strip() for s in line.split("=")]
        ts = term.findall(rhs)
        assert len(ts) == 2, line
        (s1, c1, u), (s2, c2, v) = ts
        a = (-1 if s1 == "-" else 1) * int(c1 or 1); b = (-1 if s2 == "-" else 1) * int(c2 or 1)
        gates.append((name, a, u, b, v))
    return gates

G = parse_G(SRC)
w = {"x%d" % i: [int(i == j) for j in range(8)] for i in range(8)}
for (name, a, u, b, v) in G:
    assert name not in w and u in w and v in w
    w[name] = [a * p + b * q for p, q in zip(w[u], w[v])]
okG = all(w["y%d" % j] == [chi(j, x) for x in range(8)] for j in range(8))
print("[G] 8 points: %d gates, every output y_j equals row j of H_8 exactly (factor 1): %s" % (len(G), okG))
alph = sorted({abs(e) for (n, *_r) in G for e in w[n]})
print("[G] entries of all 19 wires in the inputs: absolute values", alph, "; coefficients used:", sorted({abs(c) for (_n, a, _u, b, _v) in G for c in (a, b)}))

# ---------------------------------------------------------------- (O) the brick, written by me from the (G) circuit:
# halve the centre once (h = g7/2); then every "w -/+ 2*p" of the (G) circuit becomes "w/2 -/+ p".
# wires: 0..7 inputs, 8 = the constant 0 of the Lean model, 9.. = gates.  ("add", i, j) / ("sub", i, j) / ("scale", c, i)
def brick_O():
    names = {"x%d" % i: i for i in range(8)}; prog = []
    def emit(name, g):
        prog.append(g); names[name] = 8 + len(prog)
    for (name, a, u, b, v) in G[:7]:                       # the merge tree, coefficients +-1
        assert a == 1 and abs(b) == 1
        emit(name, ("add" if b == 1 else "sub", names[u], names[v]))
    emit("h7", ("scale", F(1, 2), names["g7"]))
    half = {"g7": "h7"}                                    # half[w] = name of the wire holding w/2
    for (name, a, u, b, v) in G[7:]:
        assert abs(a) == 1 and abs(b) == 2 and u in half
        if a == 1: emit("h" + name, ("add" if b == 2 else "sub", names[half[u]], names[v]))
        else:
            assert b == 2; emit("h" + name, ("sub", names[v], names[half[u]]))
        half[name] = "h" + name
    outs = [names["hy%d" % j] for j in range(8)]
    return prog, outs

BR, BOUT = brick_O()

def run_lean(n, prog, outs, x):
    """Program.eval of Core.lean: v = inputs, then 0, then one value per gate."""
    v = list(x) + [0]
    for g in prog:
        if g[0] == "add": v.append(v[g[1]] + v[g[2]])
        elif g[0] == "sub": v.append(v[g[1]] - v[g[2]])
        else: v.append(g[1] * v[g[2]])
    return [v[o] for o in outs]

cols = [run_lean(8, BR, BOUT, [F(int(i == j)) for i in range(8)]) for j in range(8)]   # cols[j] = image of e_j
okO = all(cols[x][j] == F(chi(j, x), 2) for j in range(8) for x in range(8))
print("[O] 8 points: %d gates (%d add/sub, %d scale); computes exactly H_8 / 2: %s" % (
    len(BR), sum(g[0] != "scale" for g in BR), sum(g[0] == "scale" for g in BR), okO))

# ---------------------------------------------------------------- tensor products as explicit OAI programs
def build(k, plan, final_scale=True):
    """plan: list of 3 (my 20-gate brick) and 1 (a butterfly: one add, one sub).  Returns (n, prog, outs, halvings)."""
    n = 1 << k; cur = list(range(n)); prog = []; pos = 0; m = 0
    def emit(g):
        prog.append(g); return n + len(prog)
    for part in plan:
        blk = list(range(pos, pos + part)); pos += part; rest = [d for d in range(k) if d not in blk]
        for base in range(1 << len(rest)):
            addr0 = sum(((base >> q) & 1) << d for q, d in enumerate(rest))
            idx = [addr0 + sum(((t >> q) & 1) << d for q, d in enumerate(blk)) for t in range(1 << part)]
            if part == 3:
                loc = [cur[i] for i in idx] + [None]       # local wire table of the brick
                for g in BR:
                    if g[0] == "scale": loc.append(emit(("scale", g[1], loc[g[2]])))
                    else: loc.append(emit((g[0], loc[g[1]], loc[g[2]])))
                for t, i in enumerate(idx): cur[i] = loc[BOUT[t]]
            else:
                a, b = cur[idx[0]], cur[idx[1]]
                cur[idx[0]] = emit(("add", a, b)); cur[idx[1]] = emit(("sub", a, b))
        if part == 3: m += 1
    if final_scale and m:
        cur = [emit(("scale", 1 << m, c)) for c in cur]
    return n, prog, cur, m

def check_fraction(k, plan):
    """exact, Fractions, all unit vectors, the final multiplications RUN as gates"""
    n, prog, outs, m = build(k, plan)
    ok = True
    for j in range(n):
        y = run_lean(n, prog, outs, [F(int(i == j)) for i in range(n)])
        ok &= all(y[r] == chi(r, j) for r in range(n))
    return n, len(prog), m, ok

def check_numpy(k, plan):
    """exact in integers: evaluate on 2^m * identity (so every halving must divide exactly; asserted), compare with 2^m * H_n.
    Linear, so this is the same statement as on the identity.  Wires are freed after their last use."""
    import numpy as np
    n, prog, outs, m = build(k, plan)
    last = {}
    for t, g in enumerate(prog):
        for i in (g[1:] if g[0] != "scale" else g[2:]): last[i] = t
    for o in outs: last[o] = len(prog)
    I = (np.eye(n, dtype=np.int32) << m)
    v = {i: I[i].copy() for i in range(n)}; peak = 0
    for t, g in enumerate(prog):
        if g[0] == "add": r = v[g[1]] + v[g[2]]
        elif g[0] == "sub": r = v[g[1]] - v[g[2]]
        else:
            c = g[1]
            if isinstance(c, F) and c.denominator != 1:
                assert c == F(1, 2); a = v[g[2]]; assert not (a & 1).any(); r = a >> 1
            else: r = v[g[2]] * int(c)
        assert np.abs(r).max() < 2 ** 30
        v[n + 1 + t] = r
        for i in (g[1:] if g[0] != "scale" else g[2:]):
            if last.get(i) == t and i in v: del v[i]
    idx = np.arange(n)
    # H_n by rows: row r, column x = chi(r, x)
    H = np.ones((n, n), dtype=np.int32)
    pc = np.array([bin(a).count("1") & 1 for a in range(n)], dtype=np.int32)
    H = 1 - 2 * pc[(idx[:, None] & idx[None, :])]
    # v[outs[r]] is the form "output r" as a row over the inputs (we evaluated the rows of the identity as inputs:
    # wire value on input e_j at position j)  -> vector over j
    ok = all((v[outs[r]] == (H[r] << m)).all() for r in range(n))
    return n, len(prog), m, ok

if __name__ == "__main__":
    for k, plan in ((6, (3, 3)), (9, (3, 3, 3))):
        n, c, m, ok = check_fraction(k, plan)
        print("[O] %d points, plan %s, final multiplications by %d RUN: %d gates, computes exactly H_%d: %s ; textbook %d ; formula (5/6) n log2 n + n = %s" % (
            n, plan, 1 << m, c, n, ok, n * k, F(5, 6) * n * k + n))
    big = [(9, (3, 3, 3)), (10, (3, 3, 3, 1)), (12, (3, 3, 3, 3))] if len(sys.argv) > 1 else []
    for k, plan in big:
        n, c, m, ok = check_numpy(k, plan)
        mm = sum(p == 3 for p in plan)
        print("[O] %d points, plan %s (integers, numpy): %d gates, computes exactly H_%d: %s ; textbook %d ; 20*(n/8)*m + 2*(n/2)*(k-3m) + n = %d" % (
            n, plan, c, n, ok, n * k, 20 * (n // 8) * mm + n * (k - 3 * mm) + n))
