# d-6-excess, second run.
# (a) which sets of 3 or 4 sign rows on 4 inputs are NOT zero-excess (lemma, already checked against brute force)
# (b) n = 5: among all sets of 5 sign rows on 5 inputs with zero excess, the largest |det| (Hadamard bound 5^(5/2) = 55.9; max for +-1 is 48)
# (c) growth law if a fraction 1/rho of the excess survives when N copies run together:  f(2k) = 2 + (2/rho) f(k), f = excess per point
import sys, itertools
from fractions import Fraction
sys.path.insert(0, "waves/wave-01/d-6-excess")
sys.argv = [sys.argv[0]]
import importlib.util
src = open("waves/wave-01/d-6-excess/gray.py").read().split('print("PART 1')[0]
ns = {}
exec(compile(src, "gray_head", "exec"), ns)
gray_zero, trees, canon = ns["gray_zero"], ns["trees"], ns["canon"]

def det(M):
    M = [[Fraction(x) for x in r] for r in M]; n = len(M); d = Fraction(1)
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None: return 0
        if p != c: M[c], M[p] = M[p], M[c]; d = -d
        d *= M[c][c]
        for r in range(c+1, n):
            f = M[r][c] / M[c][c]
            for k in range(c, n): M[r][k] -= f * M[c][k]
    return int(d)
def dist(u, v): return sum(1 for a, b in zip(u, v) if a != b)

print("(a) n = 4")
pats = [(1,) + p for p in itertools.product((1, -1), repeat=3)]
tl = list(trees(range(4)))
for m in (3, 4):
    bad = [rows for rows in itertools.combinations(pats, m) if not gray_zero(rows, 4, tl)]
    print("  m=%d: %d sets pay excess" % (m, len(bad)))
    for rows in bad:
        ds = sorted(min(dist(u, v), 4 - dist(u, v)) for u, v in itertools.combinations(rows, 2))
        print("    rows", rows, "pairwise distances (up to sign)", ds, "det" if m == 4 else "", det(rows) if m == 4 else "")
good4 = [rows for rows in itertools.combinations(pats, 4) if gray_zero(rows, 4, tl)]
print("  zero-excess 4-row sets: %d; |det| histogram %s" % (len(good4), sorted((d, sum(1 for r in good4 if abs(det(r)) == d)) for d in set(abs(det(r)) for r in good4))))
# pairs of orthogonal rows inside zero-excess sets
mx = max(sum(1 for u, v in itertools.combinations(r, 2) if dist(u, v) == 2) for r in good4)
print("  most orthogonal pairs in a zero-excess 4-row set: %d of 6" % mx)

print("(b) n = 5")
pats = [(1,) + p for p in itertools.product((1, -1), repeat=4)]
tl = list(trees(range(5)))
hist = {}; cnt = 0; tot = 0
for rows in itertools.combinations(pats, 5):
    d = abs(det(rows))
    if d == 0: continue
    tot += 1
    z = gray_zero(rows, 5, tl)
    hist.setdefault(d, [0, 0])[0] += 1
    if z: hist[d][1] += 1
print("  full-rank 5-row sets: %d.  |det| : (sets, zero-excess sets) %s" % (tot, sorted(hist.items())))

print("(c) excess per point f(2k) = 2(1 - 1/N)^2 + (2/rho) f(k), N = 2^k, from f(2) = 1/4 (the 7-gate brick)")
for rho in (1, Fraction(3, 2), 2, 3, 4):
    f = Fraction(1, 4); k = 2; line = []
    while k <= 1024:
        line.append("k=%d: %.3f" % (k, float(f)))
        N = 2**k
        f = 2*(1 - Fraction(1, N))**2 + Fraction(2)/rho * f; k *= 2
    print("  rho=%s  " % rho + "  ".join(line))
