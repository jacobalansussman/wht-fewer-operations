# lift22.py: the 16-point analysis map B^-1 in 22 gates (count G), replayed over the rationals.
# head basis at w = 1:  g1 = x3 - x4, g2 = x2 - x4, g3 = x1 - x2 - x3 + x4  (coordinates 1..4);  w = 2: any basis of the head space.
import itertools, subprocess, sys
from fractions import Fraction as Fr
MC = "waves/wave-01/d-0-zeta/mincirc"
k = 4; G1 = [(0, 0, 1, -1), (0, 1, 0, -1), (1, -1, -1, 1)]
pairs = list(itertools.combinations(range(4), 2)); n = 6
def online(t, u, v):      # is t = a*u + b*v ?
    for i, j in itertools.combinations(range(len(t)), 2):
        det = u[i] * v[j] - u[j] * v[i]
        if det != 0:
            a = (t[i] * v[j] - t[j] * v[i]) / det; b = (u[i] * t[j] - u[j] * t[i]) / det
            return all(a * x + b * y == z for x, y, z in zip(u, v, t))
    return False
def prop(u, v): return all(u[i] * v[j] == u[j] * v[i] for i in range(len(u)) for j in range(len(u)))
# ---- layer 1 (and layer 3, the same forms on complements up to sign): 6 gates
x = [[Fr(int(i == j)) for j in range(4)] for i in range(4)]
add = lambda u, v, a=1, b=1: [a * p + b * q for p, q in zip(u, v)]
g1 = add(x[2], x[3], 1, -1); g2 = add(x[1], x[3], 1, -1)
h = add(x[0], x[1], 1, -1)                 # helper x1 - x2
g3 = add(h, g1, 1, -1)                     # x1 - x2 - x3 + x4
# total: s = x1+x2+x3+x4.  helper t = x1 + x2 ... try all single helpers on a line through two available values
avail = x + [g1, g2, h, g3]; s = [Fr(1)] * 4; found = None
print("layer 1: g1,g2,g3 with one helper (x1 - x2): 4 gates so far; is the total then one gate away?", any(online(s, u, v) for u, v in itertools.combinations(avail, 2)))
# honest search for layer 1 with exactly 2 helpers from small coefficients
best = None
C = [Fr(a, b) for a in (1, -1, 2, -2, 3, -3) for b in (1, 2, 3)]
T1 = [[Fr(c) for c in g] for g in G1] + [s]
def closure(av, targets):
    av = list(av); got = 0; left = list(targets); ch = True
    while ch:
        ch = False
        for t in list(left):
            if any(prop(t, a) for a in av) or any(online(t, u, v) for u, v in itertools.combinations(av, 2)):
                av.append(t); left.remove(t); got += 1; ch = True
    return av, left
for (i, j) in itertools.combinations(range(4), 2):
    for c in C:
        h1 = add(x[i], x[j], 1, c); av1, left1 = closure(x + [h1], T1)
        for u, v in itertools.combinations(av1, 2):
            for c2 in C:
                h2 = add(u, v, 1, c2); av2, left2 = closure(av1 + [h2], left1)
                if not left2 and best is None: best = (i, j, c, h1, h2)
print("layer 1 over Q with 2 helpers (6 gates):", "YES helpers %s and %s" % ([str(a) for a in best[3]], [str(a) for a in best[4]]) if best else "not found in the pool")
# ---- layer 2: targets s, U g1, U g2, U g3 fixed; two independent forms of the head space (killed by 'remove one element')
def Ug(g): return [Fr(g[a] + g[b]) for (a, b) in pairs]
def Dn(f): return [sum(f[n_] for n_, P in enumerate(pairs) if i in P) for i in range(4)]
T2 = [[Fr(1)] * 6] + [Ug(g) for g in G1]
print("layer 2 fixed targets:", [[str(a) for a in t] for t in T2])
e = [[Fr(int(i == j)) for j in range(6)] for i in range(6)]
def headrank(av):
    hs = [a for a in av if any(a) and not any(Dn(a))]
    # rank of the head forms found (space has dimension 2)
    r = 0
    for a, b in itertools.combinations(hs, 2):
        if not prop(a, b): r = 2
    return max(r, 1 if hs else 0), hs
# get the modulo-5 circuit from mincirc and lift it: helpers ('inter') get every lift of their coefficient from a small pool
rows5 = [[int(a) % 5 for a in t] for t in T2]
H2 = [[1, 0, 0, 0, 0, 1], [0, 1, 0, 0, 1, 0], [0, 0, 1, 1, 0, 0]]   # complementary pair sums; head space = sum-zero combinations
hA = [1, -1, 0, 0, -1, 1]; hB = [1, 1, -2, -2, 1, 1]
assert not any(Dn(hA)) and not any(Dn(hB))
out = None
for ca, cb in itertools.product(range(5), repeat=2):
    for da, db in itertools.product(range(5), repeat=2):
        r1 = [(ca * a + cb * b) % 5 for a, b in zip(hA, hB)]; r2 = [(da * a + db * b) % 5 for a, b in zip(hA, hB)]
        if not any(r1) or not any(r2) or (ca * db - cb * da) % 5 == 0: continue
        open("rows22.txt", "w").write("\n".join(" ".join(map(str, r)) for r in rows5 + [r1, r2]) + "\n")
        o = subprocess.run([MC, "5", "6", "4", "rows22.txt"], capture_output=True, text=True).stdout
        if "YES" in o: out = o; break
    if out: break
print(out)
