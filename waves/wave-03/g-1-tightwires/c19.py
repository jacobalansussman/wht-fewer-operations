#!/usr/bin/env python3
"""g-1 c19.py: the 19-gate circuit for the 8-point Walsh-Hadamard transform, replayed exactly.  Stand-alone (no imports of
tonight's other programs).  Integers and Fractions only.
Count (G): a gate is any a*u + b*v; scalings free.  Count (O): every addition/subtraction costs 1, every multiplication by a
constant costs 1.
 (1) count (G), 8 points: 19 gates; the outputs are EXACTLY the 8 rows of the Sylvester matrix H_8 (no sign or scale left over).
 (2) count (O), 8 points: the same circuit with the hub halved once computes H_8 x / 2 with 19 additions/subtractions and
     ONE halving = 20 operations.  (H_8 itself this way: 28, worse than the textbook's 24.)
 (3) count (G), 16 and 64 points: tensor products.  16 = 8 x 2: two copies + 8 butterflies = 54.  64 = 8 x 8: 16 copies = 304.
     Checked: the computed matrix is the Sylvester matrix up to the order of its rows.
 (4) count (O), 512 points: three layers of the 20-operation brick give H_512 x / 8 in 3 * 64 * 20 = 3840 operations; one
     multiplication by 8 per output gives H_512 x exactly in 4352, against the textbook's 4608.  Replayed here at 64 points
     (H_64 x / 4 in 320 operations; with the 64 final multiplications 384, a tie with the textbook) and at 512 points.
"""
from fractions import Fraction as F
import itertools

# the circuit: (name, a, u, b, v) meaning name = a*u + b*v
C19 = [("g1", 1, "x0", 1, "x7"), ("g2", 1, "x1", 1, "x6"), ("g3", 1, "x2", -1, "x5"), ("g4", 1, "x3", -1, "x4"),
       ("g5", 1, "g1", -1, "g2"), ("g6", 1, "g3", 1, "g4"), ("g7", 1, "g5", -1, "g6"),
       ("g8", 1, "g7", -2, "x7"), ("g9", 1, "g7", -2, "x5"), ("g10", 1, "g8", 2, "x6"), ("g11", 1, "g9", -2, "x4"),
       ("y7", 1, "g10", 2, "g4"), ("y3", 1, "g9", 2, "x3"), ("y5", -1, "y3", 2, "g5"), ("y1", 1, "g10", 2, "g3"),
       ("y6", 1, "g11", 2, "g2"), ("y2", 1, "g8", 2, "x1"), ("y4", 1, "y2", 2, "g6"), ("y0", -1, "g11", 2, "g1")]
# the same in count (O): h = (g5 - g6)/2 is one subtraction and one halving; every later line is one addition or subtraction
O20 = [("g1", "x0", "+", "x7"), ("g2", "x1", "+", "x6"), ("g3", "x2", "-", "x5"), ("g4", "x3", "-", "x4"),
       ("g5", "g1", "-", "g2"), ("g6", "g3", "+", "g4"), ("t", "g5", "-", "g6"), ("h", "t", "half", None),
       ("a8", "h", "-", "x7"), ("a9", "h", "-", "x5"), ("a10", "a8", "+", "x6"), ("a11", "a9", "-", "x4"),
       ("y7", "a10", "+", "g4"), ("y3", "a9", "+", "x3"), ("y5", "g5", "-", "y3"), ("y1", "a10", "+", "g3"),
       ("y6", "a11", "+", "g2"), ("y2", "a8", "+", "x1"), ("y4", "y2", "+", "g6"), ("y0", "g1", "-", "a11")]

def chi(j, x): return -1 if bin(j & x).count("1") & 1 else 1

def run_G(inputs):
    """inputs: list of 8 vectors (forms); returns (outputs y0..y7 as forms, number of gates)"""
    w = {"x%d" % i: inputs[i] for i in range(8)}; gates = 0
    for (name, a, u, b, v) in C19:
        w[name] = [a * p + b * q for p, q in zip(w[u], w[v])]; gates += 1
    return [w["y%d" % j] for j in range(8)], gates

def run_O(inputs):
    w = {"x%d" % i: inputs[i] for i in range(8)}; ops = 0
    for (name, u, op, v) in O20:
        if op == "+": w[name] = [p + q for p, q in zip(w[u], w[v])]
        elif op == "-": w[name] = [p - q for p, q in zip(w[u], w[v])]
        else: w[name] = [p / 2 for p in w[u]]
        ops += 1
    return [w["y%d" % j] for j in range(8)], ops

def unit(n): return [[F(int(i == j)) for i in range(n)] for j in range(n)]

# (1)
out, gates = run_G(unit(8))
ok = all(out[j] == [chi(j, x) for x in range(8)] for j in range(8))
print("(1) count (G), 8 points: %d gates; output j is exactly row j of H_8 for every j: %s   (textbook 24, best known before 22)" % (gates, ok))
# (2)
out, ops = run_O(unit(8))
ok = all(out[j] == [F(chi(j, x), 2) for x in range(8)] for j in range(8))
print("(2) count (O), 8 points: %d operations (19 additions/subtractions, 1 halving); output j is exactly row j of H_8 / 2: %s" % (ops, ok))

def tensor(k, plan, mode):
    """apply bricks along groups of address bits; plan = list of group sizes (3 = the 8-point brick, 1 = a butterfly)"""
    n = 1 << k; cur = unit(n); count = 0; pos = 0
    for part in plan:
        blk = list(range(pos, pos + part)); pos += part; rest = [d for d in range(k) if d not in blk]
        for base in itertools.product((0, 1), repeat=len(rest)):
            addr0 = sum(bit << d for bit, d in zip(base, rest))
            idx = [addr0 + sum(((t >> q) & 1) << d for q, d in enumerate(blk)) for t in range(1 << part)]
            if part == 3:
                o, c = (run_G if mode == "G" else run_O)([cur[i] for i in idx]); count += c
                for t, i in enumerate(idx): cur[i] = o[t]
            else:
                a, b = cur[idx[0]], cur[idx[1]]; cur[idx[0]] = [p + q for p, q in zip(a, b)]; cur[idx[1]] = [p - q for p, q in zip(a, b)]; count += 2
    return cur, count

for k, plan in ((4, (3, 1)), (6, (3, 3))):
    n = 1 << k; M, c = tensor(k, plan, "G")
    ok = all(M[j] == [chi(j, x) for x in range(n)] for j in range(n))
    print("(3) count (G), %d points, plan %s: %d gates; the computed matrix is exactly H_%d: %s   (textbook %d, bricks of 4: %d)" % (n, "x".join(str(1 << p) for p in plan), c, n, ok, n * k, n * k * 7 // 8))
for k, plan in ((6, (3, 3)), (9, (3, 3, 3))):
    n = 1 << k; M, c = tensor(k, plan, "O"); s = 1 << (k // 3)
    ok = all(M[j] == [F(chi(j, x), s) for x in range(n)] for j in range(n))
    print("(4) count (O), %d points: %d operations give exactly H_%d / %d: %s; with one multiplication by %d per output: %d operations for H_%d itself (textbook %d)" % (n, c, n, s, ok, s, c + n, n, n * k))
