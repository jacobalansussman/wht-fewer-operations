# z-2: is the 19-gate 8-point circuit inside x-9's class in ANY linear coordinate system (168 of them)?
# Class (x-9 section 5): (i) product wires on the nodes of one chain of halvings; (ii) hubs = (a product on L) + t (a product on R)
# with the same lower tuple.  At 8 points: a wire on a 2-point node is a product; a wire on a 4-point node is a product or a hub;
# a wire on the whole cube is a product if the 2x2x2 array has rank one, a hub if the flattening (top, middle | low) has rank one.
import itertools, re
from fractions import Fraction
txt = open('waves/wave-03/g-1-tightwires/h8_19gates.txt').read().splitlines()
names = {f'x{i}': [int(i == j) for j in range(8)] for i in range(8)}; order = []; defs = {}
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
            terms.append((sign * c, nm)); sign = 1
    (a, u), (b, v) = terms
    names[lhs] = [a * p + b * q for p, q in zip(names[u], names[v])]; order.append(lhs); defs[lhs] = (u, v)
H = [[1 - 2 * (bin(j & x).count('1') & 1) for x in range(8)] for j in range(8)]
assert all(names[f'y{j}'] == H[j] for j in range(8)) and len(order) == 19
print("replayed: 19 gates, all 8 outputs exact")

def rank2(rows):
    rows = [[Fraction(v) for v in r] for r in rows]; rk = 0
    for c in range(len(rows[0])):
        p = next((i for i in range(rk, len(rows)) if rows[i][c] != 0), None)
        if p is None: continue
        rows[rk], rows[p] = rows[p], rows[rk]
        for i in range(rk + 1, len(rows)):
            if rows[i][c] != 0:
                f = rows[i][c] / rows[rk][c]; rows[i] = [x - f * y for x, y in zip(rows[i], rows[rk])]
        rk += 1
        if rk == len(rows): break
    return rk

def classify(w, b):
    # coordinates c = (c1, c2, c3) -> address c1 b1 + c2 b2 + c3 b3 ; c1 is the lowest bit of the chain
    arr = {}
    for c in itertools.product((0, 1), repeat=3):
        x = (b[0] if c[0] else 0) ^ (b[1] if c[1] else 0) ^ (b[2] if c[2] else 0)
        arr[c] = w[x]
    supp = [c for c in arr if arr[c] != 0]
    if len({(c[1], c[2]) for c in supp}) == 1: return 'P1'          # on a 2-point node
    if len({c[2] for c in supp}) == 1:
        c3 = supp[0][2]
        m = [[arr[(c1, c2, c3)] for c1 in (0, 1)] for c2 in (0, 1)]
        return 'P2' if rank2(m) == 1 else 'H2'
    f_low = [[arr[(c1, c2, c3)] for c1 in (0, 1)] for c2 in (0, 1) for c3 in (0, 1)]          # (c2, c3 | c1)
    f_mid = [[arr[(c1, c2, c3)] for c2 in (0, 1)] for c1 in (0, 1) for c3 in (0, 1)]
    f_top = [[arr[(c1, c2, c3)] for c3 in (0, 1)] for c1 in (0, 1) for c2 in (0, 1)]
    if rank2(f_low) == 1 and rank2(f_mid) == 1 and rank2(f_top) == 1: return 'P3'
    # hub: L part and R part each a product on its half, same lower slope
    L = [[arr[(c1, c2, 0)] for c1 in (0, 1)] for c2 in (0, 1)]; R = [[arr[(c1, c2, 1)] for c1 in (0, 1)] for c2 in (0, 1)]
    if rank2(L) == 1 and rank2(R) == 1:
        return 'H3' if rank2(f_low) == 1 else 'H3x'                 # H3x: two products with DIFFERENT lower tuples (a hatch)
    return 'X'

best = None; tally = {}
bases = [(b1, b2, b3) for b1 in range(1, 8) for b2 in range(1, 8) for b3 in range(1, 8)
         if b2 != b1 and b3 not in (b1, b2, b1 ^ b2)]
print("coordinate systems:", len(bases))
for b in bases:
    cls = {g: classify(names[g], b) for g in order}
    out = [g for g in order if cls[g] in ('X', 'H3x')]
    key = len(out); tally[key] = tally.get(key, 0) + 1
    if best is None or key < best[0]: best = (key, b, cls)
print("number of the 19 wires OUTSIDE the class (X = neither; H3x = two-piece hub with different lower tuples) -> coordinate systems:",
      sorted(tally.items()))
k, b, cls = best
print("best coordinate system", b, ":", k, "wires outside")
for g in order: print(f"  {g:4s} {cls[g]:4s} {names[g]}  = f({defs[g][0]}, {defs[g][1]})")
print("class floor at 8 points (x-9 section 5): (3/4)*8*3 + 8/4 =", 3 * 8 * 3 // 4 + 2, "; this circuit: 19")
