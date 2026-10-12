# d-6-excess: the zero-excess ("Gray") lemma, checked against brute force, then used on products.
# Gate model: w = a*u + b*v, any coefficients, scalings free.  excess = gates - (inputs-1) - (outputs-1).
# LEMMA (derived): m sign rows (entries +-1, full support, pairwise not proportional) on n inputs have excess 0
#   iff for some root row r (normalised to all ones by free input signs) and some binary tree on the n inputs,
#   every other row is reached from an earlier row y by negating y on a block S (a tree node or one input)
#   on which y is constant.
# Part 1: compare the lemma with exhaustive search (engine of i-play/n4.py) for every set of 2..4 sign rows, n = 3, 4.
# Part 2: verify explicit circuits exactly (Gray family; H2 x G3 in 13 gates).
# Part 3: decide excess 0 by the lemma for products of zero-excess bricks on 6 wires.
import sys, itertools
from fractions import Fraction
sys.path.insert(0, "waves/wave-01/i-play")
import n4

def canon(v):
    return v if v[0] > 0 else tuple(-a for a in v)

def trees(leaves):
    """all binary trees on a labelled leaf set, each as the frozenset of its node leaf-sets (root and leaves excluded)"""
    leaves = tuple(leaves)
    if len(leaves) == 1:
        yield frozenset(); return
    first, rest = leaves[0], leaves[1:]
    for k in range(0, len(rest)):
        for comp in itertools.combinations(rest, k):
            left = (first,) + comp
            right = tuple(x for x in rest if x not in comp)
            if not right: continue
            for tl in trees(left):
                for tr in trees(right):
                    nodes = set(tl) | set(tr)
                    if len(left) > 1: nodes.add(frozenset(left))
                    if len(right) > 1: nodes.add(frozenset(right))
                    yield frozenset(nodes)

def gray_zero(rows, n, treelist=None):
    rows = [canon(tuple(r)) for r in rows]
    if treelist is None: treelist = list(trees(range(n)))
    for r in rows:
        tg = set(canon(tuple(a*b for a, b in zip(t, r))) for t in rows)
        one = tuple([1]*n)
        for tr in treelist:
            blocks = [tuple(sorted(s)) for s in tr] + [(i,) for i in range(n)]
            reached = {one}; frontier = [one]
            while frontier:
                y = frontier.pop()
                for S in blocks:
                    if len(set(y[i] for i in S)) != 1: continue
                    z = list(y)
                    for i in S: z[i] = -z[i]
                    z = canon(tuple(z))
                    if z in tg and z not in reached:
                        reached.add(z); frontier.append(z)
            if len(reached) == len(tg): return True
    return False

def brute_zero(rows, n):
    n4.H4 = [tuple(r) for r in rows]
    depth = (n - 1) + (len(rows) - 1)
    sols, targets = n4.search(n, list(range(len(rows))), depth, False)
    return bool(sols)

def run_circuit(n, gates):
    vals = [tuple(Fraction(1 if i == j else 0) for i in range(n)) for j in range(n)]
    for (i, a, j, b) in gates:
        vals.append(tuple(a*x + b*y for x, y in zip(vals[i], vals[j])))
    return vals

def prop(u, v):
    k = None
    for a, b in zip(u, v):
        if (a == 0) != (b == 0): return False
        if a != 0:
            q = Fraction(a) / Fraction(b)
            if k is None: k = q
            elif q != k: return False
    return True

print("PART 1: lemma against exhaustive search (excess-0 depth only)")
for n in (3, 4):
    pats = [(1,) + p for p in itertools.product((1, -1), repeat=n-1)]
    tl = list(trees(range(n)))
    agree = dis = 0; yes = {}
    for m in (2, 3, 4):
        for rows in itertools.combinations(pats, m):
            g = gray_zero(rows, n, tl); b = brute_zero(rows, n)
            if g == b: agree += 1
            else:
                dis += 1; print("  DISAGREE n=%d rows=%s lemma=%s brute=%s" % (n, rows, g, b))
            if g: yes[m] = yes.get(m, 0) + 1
    print("  n=%d trees=%d: sets tested %d, agree %d, disagree %d; zero-excess sets by m: %s" % (n, len(tl), agree+dis, agree, dis, sorted(yes.items())))

print("PART 2: explicit circuits, exact")
for n in range(3, 8):
    gates = []; idx = n
    prev = 0
    for i in range(1, n):
        gates.append((prev, 1, i, 1)); prev = idx; idx += 1
    sign = [1]*n; cur = prev; seen = {tuple(sign)}
    code = [0]
    for b in range(n-1):
        code = code + [c ^ (1 << b) for c in reversed(code)]
    for a, b in zip(code, code[1:]):
        bit = (a ^ b).bit_length()            # coordinate 1..n-1
        gates.append((cur, 1, bit, -2*sign[bit])); sign[bit] = -sign[bit]; cur = idx; idx += 1
        seen.add(tuple(sign))
    vals = run_circuit(n, gates)
    outs = set(canon(tuple(int(x) for x in v)) for v in vals[n+n-2:])
    ok = outs == set((1,) + p for p in itertools.product((1, -1), repeat=n-1))
    print("  all %d sign patterns of %d inputs: gates %d = (n-1) + (2^(n-1)-1) = %d, correct %s" % (2**(n-1), n, len(gates), n-1+2**(n-1)-1, ok))
# H2 x G3 on inputs a0 a1 a2 b0 b1 b2 (0..5); G3 rows g1=(1,1,1) g2=(1,1,-1) g3=(-1,1,-1): a 3x3 zero-excess matrix (4 gates)
G3 = [(1,1,1),(1,1,-1),(-1,1,-1)]
gates = [(0,1,1,1),(3,1,4,1),(6,1,2,1),(8,1,7,1),(9,1,5,-1),(10,1,5,2),(10,1,2,-2),(10,1,7,-2),(10,1,6,-2),
         (0,1,3,1),(12,1,15,-2),(0,1,3,-1),(14,1,17,2)]
vals = run_circuit(6, gates)
want = [g + g for g in G3] + [g + tuple(-x for x in g) for g in G3]
found = [any(prop(v, w) for v in vals[6:]) for w in want]
det = G3[0][0]*(G3[1][1]*G3[2][2]-G3[1][2]*G3[2][1]) - G3[0][1]*(G3[1][0]*G3[2][2]-G3[1][2]*G3[2][0]) + G3[0][2]*(G3[1][0]*G3[2][1]-G3[1][1]*G3[2][0])
print("  G3 det", det, "; G3 zero excess by lemma:", gray_zero(G3, 3))
print("  H2 x G3: gates", len(gates), "rows found", found, "; product rule 2*4 + 3*2 = 14; baseline 5 + 5 = 10")

print("PART 3: is the excess of a product ever 0?  (lemma, 945 trees on 6 wires)")
tl6 = list(trees(range(6)))
H2 = [(1,1),(1,-1)]
R = [(1,1,1),(1,-1,1),(1,1,-1),(1,-1,-1)]       # 3 inputs, 4 outputs, zero excess (5 gates)
def kron(A, B): return [tuple(a*b for a in ra for b in rb) for ra in A for rb in B]
for name, A, B in (("H2 x G3", H2, G3), ("G3 x H2", G3, H2), ("H2 x R", H2, R), ("R x H2", R, H2), ("2 rows of H2xG3", [H2[0]], G3)):
    P = kron(A, B)
    print("  %-16s rows %d inputs %d: zero excess %s" % (name, len(P), len(P[0]), gray_zero(P, 6, tl6)))
# largest zero-excess subfamily of the 8 x 6 product R x H2 and of H2 x G3
for name, P in (("R x H2", kron(R, H2)), ("H2 x G3", kron(H2, G3))):
    best = 0
    for m in range(len(P), 1, -1):
        hit = None
        for rows in itertools.combinations(P, m):
            if gray_zero(rows, 6, tl6): hit = rows; break
        if hit: best = m; break
    print("  %-8s: largest zero-excess row set has %d of %d rows" % (name, best, len(P)))
