#!/usr/bin/env python3
"""c-0 klass.py: my own check of k-cross's attached claim: "the same 19-gate circuit computes the cube (triple Kronecker
product) of ANY 2x2 kernel, up to a scaling of each output; it is an identity of the class".  Count (G).
Part A: parse k-cross/class19.txt and replay each listed circuit exactly (Fractions).
Part B: the general claim.  The WIRING is fixed (taken from the file's first block: which two wires each gate reads).  For a
kernel K the centre c is forced by the outputs y2 and y3 (each differs from the centre in two inputs only).  Given c, every
other coefficient and every output scaling enters LINEARLY:  y_j = c + sum over the steps on its path of coef * partner,
and y_j = s_j * (row of K cubed).  I solve that linear system exactly for many kernels; solvable with all s_j nonzero = the
circuit exists for that kernel."""
import re, ast, sys, random
from fractions import Fraction as F

SRC = "waves/wave-03/k-cross/class19.txt"

def kron3(K):
    return [[K[(r >> 2) & 1][(c >> 2) & 1] * K[(r >> 1) & 1][(c >> 1) & 1] * K[r & 1][c & 1] for c in range(8)] for r in range(8)]

def blocks(path):
    out = []; cur = None
    for line in open(path):
        line = line.rstrip("\n")
        if line.startswith("# kernel"):
            K = [F(t) for t in re.search(r"\[\[(-?\d+),(-?\d+)\],\[(-?\d+),(-?\d+)\]\]", line).groups()]
            lists = re.findall(r"\[(\d(?:, \d){7})\]", line)
            cur = {"K": [[K[0], K[1]], [K[2], K[3]]], "sig": [int(t) for t in lists[0].split(",")], "pi": [int(t) for t in lists[1].split(",")], "gates": [], "head": line}
            out.append(cur)
        elif line.startswith("# a ="):
            cur["a"] = [F(t) for t in ast.literal_eval(line.split("=", 1)[1].strip())]
        elif "=" in line and not line.startswith("#"):
            name, rhs = [s.strip() for s in line.split("=")]
            m = re.fullmatch(r"(-?[\d/]+) \* (\w+) \+ (-?[\d/]+) \* (\w+)", rhs); assert m, line
            cur["gates"].append((name, F(m.group(1)), m.group(2), F(m.group(3)), m.group(4)))
    return out

B = blocks(SRC)
print("Part A: the", len(B), "listed circuits, replayed exactly")
for b in B:
    K3 = kron3(b["K"]); w = {"x%d" % i: [F(int(c == b["sig"][i])) for c in range(8)] for i in range(8)}   # x_i = kernel column sig[i]
    for (name, a, u, bb, v) in b["gates"]:
        assert name not in w; w[name] = [a * p + bb * q for p, q in zip(w[u], w[v])]
    ok = all([b["a"][j] * e for e in w["y%d" % j]] == K3[b["pi"][j]] for j in range(8))
    print("  kernel %s: %d gates; a_j * y_j = row pi[j] of K (x) K (x) K for all j: %s" % ([[str(e) for e in r] for r in b["K"]], len(b["gates"]), ok))

# ---------------------------------------------------------------- Part B
WIRE = [(n, u, v) for (n, _a, u, _b, v) in B[0]["gates"]]       # the wiring only
SIG, PI = B[0]["sig"], B[0]["pi"]
assert all(b["sig"] == SIG and b["pi"] == PI and [(n, u, v) for (n, _a, u, _b, v) in b["gates"]] == WIRE for b in B)
TREE = {"g1": (0, 7), "g2": (1, 6), "g3": (2, 5), "g4": (3, 4), "g5": (0, 7, 1, 6), "g6": (2, 5, 3, 4)}
assert WIRE[:7] == [("g1", "x0", "x7"), ("g2", "x1", "x6"), ("g3", "x2", "x5"), ("g4", "x3", "x4"), ("g5", "g1", "g2"), ("g6", "g3", "g4"), ("g7", "g5", "g6")]
WALK = WIRE[7:]                                                # (name, previous full wire, partner)

def solve(rows, ncol):
    """exact Gaussian elimination of an augmented system rows = [coeffs..., rhs]; returns a solution or None"""
    rows = [r[:] for r in rows]; piv = []; r0 = 0
    for c in range(ncol):
        p = next((i for i in range(r0, len(rows)) if rows[i][c] != 0), None)
        if p is None: continue
        rows[r0], rows[p] = rows[p], rows[r0]; inv = 1 / rows[r0][c]; rows[r0] = [e * inv for e in rows[r0]]
        for i in range(len(rows)):
            if i != r0 and rows[i][c] != 0:
                f = rows[i][c]; rows[i] = [a - f * b for a, b in zip(rows[i], rows[r0])]
        piv.append(c); r0 += 1
    if any(r[ncol] != 0 for r in rows[r0:]): return None
    sol = [F(0)] * ncol
    for i, c in enumerate(piv): sol[c] = rows[i][ncol]
    return sol

def circuit_for(K):
    """returns (ok, reason).  Unknowns: 12 walk coefficients, 8 output scalings s_j."""
    K3 = kron3(K); T = {j: [K3[PI[j]][SIG[i]] for i in range(8)] for j in range(8)}   # target of y_j over circuit inputs
    # the centre: y2 = c + (x7) + (x1) ; y3 = c + (x5) + (x3)
    if any(e == 0 for e in T[2]) or any(e == 0 for e in T[3]): return False, "zero entry"
    c = T[2][:]; lam = T[2][0] / T[3][0]
    if any(T[2][i] != lam * T[3][i] for i in (0, 2, 4, 6)): return False, "rows of y2, y3 not proportional off their flips"
    c[1] = lam * T[3][1]; c[7] = lam * T[3][7]
    def partner(p):
        if p[0] == "x": return [F(int(i == int(p[1:]))) for i in range(8)]
        return [c[i] if i in TREE[p] else F(0) for i in range(8)]
    path = {"g7": []}
    for t, (name, prev, p) in enumerate(WALK): path[name] = path[prev] + [(t, p)]
    ncol = 12 + 8; rows = []
    for j in range(8):
        for i in range(8):
            r = [F(0)] * (ncol + 1)
            for (t, p) in path["y%d" % j]: r[t] += partner(p)[i]
            r[12 + j] = -T[j][i]; r[ncol] = -c[i]
            rows.append(r)
    sol = solve(rows, ncol)
    if sol is None: return False, "no solution"
    if any(sol[12 + j] == 0 for j in range(8)): return False, "an output scaling is zero"
    # replay the solved circuit from scratch
    w = {"x%d" % i: [F(int(k == i)) for k in range(8)] for i in range(8)}
    w["g1"] = [c[0] * a + c[7] * b for a, b in zip(w["x0"], w["x7"])]; w["g2"] = [c[1] * a + c[6] * b for a, b in zip(w["x1"], w["x6"])]
    w["g3"] = [c[2] * a + c[5] * b for a, b in zip(w["x2"], w["x5"])]; w["g4"] = [c[3] * a + c[4] * b for a, b in zip(w["x3"], w["x4"])]
    for n, u, v in WIRE[4:7]: w[n] = [a + b for a, b in zip(w[u], w[v])]
    for t, (n, u, v) in enumerate(WALK): w[n] = [a + sol[t] * b for a, b in zip(w[u], w[v])]
    ok = all(w["y%d" % j] == [sol[12 + j] * e for e in T[j]] for j in range(8))
    return ok, "replayed" if ok else "replay failed"

print("Part B: the fixed wiring, coefficients solved by me, kernel by kernel")
named = {"[[1,1],[1,-1]] transform": [[1, 1], [1, -1]], "[[1,1],[1,0]] subset sums (a zero entry)": [[1, 1], [1, 0]], "[[1,1],[0,1]] (a zero entry)": [[1, 1], [0, 1]],
         "[[1,1],[1,1]] rank one": [[1, 1], [1, 1]], "[[1,2],[3,4]]": [[1, 2], [3, 4]], "[[1,2],[2,4]] rank one": [[1, 2], [2, 4]], "[[1,1],[1,2]]": [[1, 1], [1, 2]],
         "[[1,1],[-1,1]]": [[1, 1], [-1, 1]]}
for nm, K in named.items():
    print("  %-45s %s" % (nm, circuit_for([[F(e) for e in r] for r in K])))
random.seed(20261011); good = 0; bad = []; ratios = set()
for _ in range(300):
    K = [[F(random.choice([-1, 1]) * random.randint(1, 40), random.randint(1, 7)) for _ in range(2)] for _ in range(2)]
    ok, why = circuit_for(K); ratios.add(K[0][0] * K[1][1] / (K[0][1] * K[1][0]))
    if ok: good += 1
    else: bad.append((K, why))
print("  300 random kernels with nonzero rational entries: circuit exists and replays for %d ; distinct values of the cross ratio ad/(bc): %d ; failures: %s" % (good, len(ratios), bad[:3]))
