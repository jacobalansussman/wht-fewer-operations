# lemmas2.py (h-4-zetafloor): two more hand statements of h-4.md checked exactly (integers).
#  TRI: the "triangle gate": three hubs on the three pairs of three bits, one gate, which kills one bit and whose output is entangled.
#  CUBE: in "point coordinates" (a wire w = sum c_T x_T is read as the function p -> sum_T c_T prod_{i in T} (-p_i) on the cube {0,1}^k)
#        bit i is in L(w)  <=>  w vanishes on the facet p_i = 1 ; inputs are (signed) indicators of up-sets, outputs are indicators of
#        the sub-cubes {p_S = 0} ; a gate kills the set K <=> its two inputs are proportional on the union of the facets p_i = 1, i in K.
import itertools, random, sys
sys.path.insert(0, ".")
from killmeter import Lset, ent_bits, zeta_rows
def vec(k, terms):          # terms: list of (coef, {bit: 'e'|'f'|'j'}) ; e = (1,0), f = (0,1), j = (1,1)
    N = 1 << k; out = [0] * N
    fac = {'e': (1, 0), 'f': (0, 1), 'j': (1, 1)}
    for c, d in terms:
        for T in range(N):
            v = c
            for i in range(k): v *= fac[d[i]][T >> i & 1]
            out[T] += v
    return out
k = 3
p1 = vec(k, [(1, {0: 'j', 1: 'e', 2: 'e'}), (-1, {0: 'j', 1: 'f', 2: 'f'})])        # j on bit 0, (ee - ff) on bits 1,2
q1 = vec(k, [(1, {1: 'j', 0: 'e', 2: 'f'}), (-1, {1: 'j', 0: 'f', 2: 'e'})])        # j on bit 1, (ef - fe) on bits 0,2
w = vec(k, [(1, {2: 'j', 0: 'e', 1: 'e'}), (-1, {2: 'j', 0: 'f', 1: 'f'})])         # j on bit 2, (ee - ff) on bits 0,1
bits = lambda s: [i for i in range(k) if s >> i & 1]
print("TRI: p + q == w :", [a + b for a, b in zip(p1, q1)] == w)
for name, v in (("p", p1), ("q", q1), ("w", w)): print("   %s = %s  symmetric bits %s  entangled bits %s" % (name, v, bits(Lset(v, k)), bits(ent_bits(v, k))))
K = Lset(w, k) & ~(Lset(p1, k) & Lset(q1, k)); print("   kills", bits(K), "=> kappa", len(bits(K)), "with an entangled output: a hub born by a useful gate from hubs of two other types")
def cube(wv, k):
    N = 1 << k; out = []
    for p in range(N):
        s = 0
        for T in range(N):
            if T & p == T: s += wv[T] * (-1) ** bin(T).count("1")
        out.append(s)
    return out
random.seed(7); bad = 0; tested = 0
for k in (2, 3, 4):
    N = 1 << k
    Z = zeta_rows(k)
    okout = all(cube(Z[S], k) == [1 if p & S == 0 else 0 for p in range(N)] for S in range(N))
    okin = all(cube([int(t == T) for t in range(N)], k) == [(-1) ** bin(T).count("1") if p & T == T else 0 for p in range(N)] for T in range(N))
    for trial in range(3000):
        base = [random.choice([-2, -1, 0, 0, 1, 1, 2]) for _ in range(N)]
        # make it symmetric in a random set of bits so that L is not always empty
        for i in range(k):
            if random.random() < 0.4:
                base = [base[T & ~(1 << i)] for T in range(N)]
        if not any(base): continue
        f = cube(base, k); L = Lset(base, k)
        Lc = sum(1 << i for i in range(k) if all(f[p] == 0 for p in range(N) if p >> i & 1))
        tested += 1; bad += (L != Lc)
    print("CUBE k=%d: outputs are indicators of {p_S = 0}: %s ; inputs are signed indicators of up-sets: %s" % (k, okout, okin))
print("CUBE: L(w) = facets on which the function vanishes: %d wires tested, %d mismatches" % (tested, bad))
print("CUBE: the 4-point hub (1,1,1,0) as a function on the square (p = 00, 10, 01, 11):", cube([1, 1, 1, 0], 2), " = delta_00 - delta_11")
