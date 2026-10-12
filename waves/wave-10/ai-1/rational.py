# rational.py : the passage to the rationals (count G: a gate is a*u + b*v, scalings free).
# Part 1 (exact, Fractions): the two-element statement "no cycle shorter than delta - 2" is FALSE over the rationals
#   at the smallest size.  8 points, degree 2 (delta = 8, so the claim would be: no cycle shorter than 6).
#   Take the outputs o1 = out(a,b), o2 = out(a,c), o3 = out(b,c) and the wires
#   w1 = (o1 + o2 - o3)/2, w2 = (o1 - o2 + o3)/2, w3 = (-o1 + o2 + o3)/2.   Then o1 = w1 + w2, o2 = w1 + w3,
#   o3 = w2 + w3: a triangle of non-output wires carrying three outputs, and no relation among outputs follows.
# Part 2 (floating point, a table, not a proof): the bound my own derivation gives over the rationals (ai-1.md section 4):
#   every connected piece with at most T = 2^d - 1 edges has at most as many edges as vertices, hence
#   N - 1 <= (1 + eps)(V + 1),   eps <= 4/T + ((V+1)/2)^(1/(r-1)) / 2 - 1/2,   r = floor((floor(T/4) + 1)/2),
#   compared with the two-element field (exact table in moore_exact.out).
from fractions import Fraction as Fr
from itertools import combinations
from math import comb
k, d = 3, 2
sets = [frozenset(c) for j in range(d + 1) for c in combinations(range(k), j)]
def out(y): return tuple(Fr(1) if s <= y else Fr(0) for s in sets)
outs = {frozenset(y): out(frozenset(y)) for j in range(k + 1) for y in combinations(range(k), j)}
def comb_(*terms):
    v = [Fr(0)] * len(sets)
    for c, x in terms: v = [a + Fr(c) * b for a, b in zip(v, x)]
    return tuple(v)
def proportional(x, y):
    r = None
    for a, b in zip(x, y):
        if (a == 0) != (b == 0): return False
        if a != 0:
            if r is None: r = a / b
            elif a / b != r: return False
    return True
o1, o2, o3 = outs[frozenset((0, 1))], outs[frozenset((0, 2))], outs[frozenset((1, 2))]
h = Fr(1, 2)
w1 = comb_((h, o1), (h, o2), (-h, o3)); w2 = comb_((h, o1), (-h, o2), (h, o3)); w3 = comb_((-h, o1), (h, o2), (h, o3))
assert comb_((1, w1), (1, w2)) == o1 and comb_((1, w1), (1, w3)) == o2 and comb_((1, w2), (1, w3)) == o3
for w in (w1, w2, w3): assert not any(proportional(w, o) for o in outs.values())
print("part 1 [exact]: 8 points, degree 2, rationals: three wires that are not multiples of outputs carry the outputs")
print("   out(a,b) = w1 + w2, out(a,c) = w1 + w3, out(b,c) = w2 + w3: a cycle of length 3, where the two-element lemma allows none shorter than 6.")
print("   w1 =", [str(x) for x in w1])
print("part 2 [floating point]: gates / N at least, rank ignored below 1e-3 N")
print("k     d    two-element field: 1 + 1/(1+eps2)   rationals (my derivation): 1 + 1/(1+epsQ)   epsQ")
for kk in (32, 64, 128, 256):
    for dd in (6, 8, 9, 10, 11, 12, 14, 16):
        if dd >= kk / 2: continue
        R = sum(comb(kk, j) for j in range(dd + 1))
        if R > 2 ** kk / 1000: continue
        T = 2 ** dd - 1
        r = (T // 4 + 1) // 2
        lnv = (kk - 1) * 0.6931471805599453
        import math
        epsQ = 4 / T + (math.exp(lnv / (r - 1)) - 1) / 2 if r > 1 else float('inf')
        eps2 = (math.exp(lnv / (2 ** dd - 2)) - 1) / 2
        print(f"{kk:<5d} {dd:<4d} {1 + 1 / (1 + eps2):<36.4f} {1 + 1 / (1 + epsQ):<44.4f} {epsQ:.4f}")
    print()
