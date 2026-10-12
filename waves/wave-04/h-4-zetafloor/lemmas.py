# lemmas.py (h-4-zetafloor): brute-force checks of the hand lemmas of h-4.md, exact rationals.
#  P1: two product wires in, product wire out  => the gate kills at most one bit.
#  P2: two product wires in, entangled wire out => the gate kills no bit.
#  P4: a hub M (x) R (entangled on one pair of bits) and a product partner give a product: exactly one such gate kills two bits.
#  HUB: the 4-point hub of subset sums is (1,1,1,0); its three consumers; and the same count for the kernel [[1,1],[1,tau]].
from fractions import Fraction as F
import itertools, sys
sys.path.insert(0, ".")
from killmeter import Lset, ent_bits

def kron(*vs):
    out = [1]
    for v in vs: out = [a * b for b in v for a in out]     # first factor = bit 0 (fastest index)
    return out

vals = [-2, -1, 0, 1, 2, 3]
pts = []                                                   # projective points of the line with small entries
for a in vals:
    for b in vals:
        if (a, b) != (0, 0) and not any((a * q[1] - b * q[0]) == 0 for q in pts): pts.append((a, b))
print("2-vectors used as tensor factors:", len(pts), pts)
for k in (2, 3):
    prods = [kron(*c) for c in itertools.product(pts, repeat=k)]
    coef = [F(1), F(-1), F(2), F(-2), F(1, 2), F(-1, 2), F(3), F(-3), F(1, 3)]
    n1 = n2 = worst1 = worst2 = 0
    import random; random.seed(1)
    pairs = list(itertools.combinations(range(len(prods)), 2))
    if len(pairs) > 60000: pairs = random.sample(pairs, 60000)
    for i, j in pairs:
        u, v = prods[i], prods[j]; Lu, Lv = Lset(u, k), Lset(v, k)
        for c in coef:
            w = [x + c * y for x, y in zip(u, v)]
            if not any(w): continue
            K = Lset(w, k) & ~(Lu & Lv); kap = bin(K).count("1")
            if ent_bits(w, k): n2 += 1; worst2 = max(worst2, kap)
            else: n1 += 1; worst1 = max(worst1, kap)
    print("k=%d: gates with two product inputs: product output %d, largest kappa %d (P1 says <= 1); entangled output %d, largest kappa %d (P2 says 0)" % (k, n1, worst1, n2, worst2))

# P4: hubs M on 2 bits (all 2x2 integer matrices of rank 2 with entries in -2..2), partners = all product wires x (x) y, coefficient solved exactly
cnt = {}
ms = [m for m in itertools.product(range(-2, 3), repeat=4) if m[0] * m[3] - m[1] * m[2] != 0]
for m in ms:
    M = list(m)                      # positions 00, 10, 01, 11 with bit 0 fastest: M[T0 + 2*T1]
    dk = 0
    for x in pts:
        for y in pts:
            v = kron(x, y)
            # w = M - t v must have rank one: det(M - t v) = det M - t * (cofactor form) is linear in t
            d0 = M[0] * M[3] - M[1] * M[2]; d1 = (M[0] - v[0]) * (M[3] - v[3]) - (M[1] - v[1]) * (M[2] - v[2])
            lin = d1 - d0                                 # det(M - t v) = d0 + t * lin   (det v = 0)
            if lin == 0: continue
            t = F(-d0) / lin
            w = [a - t * b for a, b in zip(M, v)]
            assert w[0] * w[3] - w[1] * w[2] == 0
            K = Lset(w, 2) & ~(Lset(M, 2) & Lset(v, 2))
            if bin(K).count("1") == 2: dk += 1
    cnt[dk] = cnt.get(dk, 0) + 1
print("P4: number of double-kill consumers per hub, over %d hubs with entries -2..2 and the %d partners per axis: %s  (the proof says exactly one partner direction, when it lies in the list)" % (len(ms), len(pts), cnt))

# HUB for subset sums at 4 points
e, f, j = (1, 0), (0, 1), (1, 1)
M = [1, 1, 1, 0]
def sub(a, b, c=1): return [x - c * y for x, y in zip(a, b)]
print("subset sums, hub M = x00+x10+x01 =", M)
print("  M - e(x)f =", sub(M, kron(e, f)), " = j(x)e ?", sub(M, kron(e, f)) == kron(j, e), "| bits: e on bit 0, f on bit 1")
print("  M - f(x)e =", sub(M, kron(f, e)), " = e(x)j ?", sub(M, kron(f, e)) == kron(e, j))
print("  M + f(x)f =", sub(M, kron(f, f), -1), " = j(x)j ?", sub(M, kron(f, f), -1) == kron(j, j))
print("  so hub (2 gates) + 3 consumers = 5 gates against Yates's 4; kills: 1 + 1 + 2 = 4, idle 2, excess 1")
# the same for the kernel [[1,1],[1,tau]]: outputs (1,1)(x)(1,1), (1,1)(x)(1,tau), (1,tau)(x)(1,1), (1,tau)(x)(1,tau); hub u = (1,1,1,tau)
def rank(rows):
    rows = [list(map(F, r)) for r in rows]; rk = 0
    for c in range(len(rows[0])):
        p = next((r for r in range(rk, len(rows)) if rows[r][c] != 0), None)
        if p is None: continue
        rows[rk], rows[p] = rows[p], rows[rk]
        for r in range(len(rows)):
            if r != rk and rows[r][c] != 0:
                q = rows[r][c] / rows[rk][c]; rows[r] = [x - q * y for x, y in zip(rows[r], rows[rk])]
        rk += 1
    return rk
units = [kron(e, e), kron(f, e), kron(e, f), kron(f, f)]
for tau in (F(-1), F(2), F(1, 3), F(7), F(0)):
    a, b = (1, 1), (1, tau)
    u = [1, 1, 1, tau]
    outs = [kron(a, a), kron(b, a), kron(a, b), kron(b, b)]
    ok = [sum(1 for q in units if rank([u, q, r]) == 2) for r in outs]
    print("  kernel [[1,1],[1,tau]], tau=%s: number of inputs q with (output, hub, q) on one line, per output: %s" % (tau, ok))
print("  (tau = 0: the kernel [[1,1],[1,0]] is subset sums with the two inputs of each bit swapped; the output (1,0)(x)(1,0) is then an input, so only three consumers remain: hub 2 gates + 3 = 5 against 4)")
