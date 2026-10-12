# d-3-mod4, experiment 1.  The 54 two-flag identities at 16 points: print, classify, find the rule.
# A flag = chain 0 < W_1 < ... < W_4 = F_2^4 of frequency subspaces; level(y) = first j with y in W_j.
# Identity: h_A(level_A(y)) + h_B(level_B(y)) = |y|   exactly, or only modulo 4.
# All arithmetic is exact (integers; "exact" test done by rational elimination with Fraction).
import itertools, sys
from fractions import Fraction
k = 4; n = 16
pc = lambda x: bin(x).count("1")
def flags(k):
    n = 1 << k; out = set()
    def rec(chain):
        W = chain[-1]
        if len(W) == n: out.add(tuple(chain)); return
        seen = set()
        for v in range(1, n):
            if v in W: continue
            W2 = frozenset(W | {w ^ v for w in W})
            if W2 in seen: continue
            seen.add(W2); rec(chain + [W2])
    rec([frozenset([0])])
    return sorted(out, key=lambda c: [sorted(W) for W in c])
def level(chain):
    return tuple(next(j for j, W in enumerate(chain) if y in W) for y in range(n))
def solve_mod4(LA, LB):
    # returns (hA, hB) as dicts level -> value mod 4 with hA[0] = 0, or None ; also number of components
    val = {}; adj = {}
    for y in range(n):
        a, b, w = ("A", LA[y]), ("B", LB[y]), pc(y) % 4
        adj.setdefault(a, []).append((b, w)); adj.setdefault(b, []).append((a, w))
    comps = 0
    for s in sorted(adj):
        if s in val: continue
        comps += 1; val[s] = 0; st = [s]
        while st:
            u = st.pop()
            for (v, w) in adj[u]:
                want = (w - val[u]) % 4
                if v not in val: val[v] = want; st.append(v)
                elif val[v] != want: return None
    return val, comps
def exact_ok(LA, LB):
    cols = []
    for L in (LA, LB):
        for j in range(1, k + 1): cols.append([Fraction(1 if L[y] == j else 0) for y in range(n)])
    rows = [[c[y] for c in cols] + [Fraction(pc(y))] for y in range(n)]
    m = len(cols); r = 0
    for c in range(m):
        p = next((i for i in range(r, n) if rows[i][c] != 0), None)
        if p is None: continue
        rows[r], rows[p] = rows[p], rows[r]
        rows[r] = [a / rows[r][c] for a in rows[r]]
        for i in range(n):
            if i != r and rows[i][c] != 0:
                f = rows[i][c]; rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        r += 1
    return all(rows[i][m] == 0 for i in range(r, n))

FL = flags(k); LV = [level(c) for c in FL]
sol = []
for i in range(len(FL)):
    for j in range(i + 1, len(FL)):
        s = solve_mod4(LV[i], LV[j])
        if s is not None: sol.append((i, j, s[0], s[1], exact_ok(LV[i], LV[j])))
print("flags:", len(FL), " two-flag identities modulo 4:", len(sol), " exact:", sum(1 for s in sol if s[4]), " only modulo 4:", sum(1 for s in sol if not s[4]))

# linear maps of F_2^4 as tuples of images of e0..e3
def apply(A, y):
    r = 0
    for b in range(k):
        if y >> b & 1: r ^= A[b]
    return r
GL = []
for A in itertools.product(range(1, n), repeat=k):
    img = {apply(A, y) for y in range(n)}
    if len(img) == n: GL.append(A)
Oq = [A for A in GL if all(pc(apply(A, y)) % 4 == pc(y) % 4 for y in range(n))]
Om = [A for A in GL if all(pc(apply(A, y)) % 4 == (-pc(y)) % 4 for y in range(n))]
Odot = [A for A in GL if all(pc(apply(A, x) & apply(A, y)) % 2 == pc(x & y) % 2 for x in range(n) for y in range(n))]
print("GL(4,2):", len(GL), " keep the dot product:", len(Odot), " keep |y| mod 4:", len(Oq), " send |y| to -|y| mod 4:", len(Om))
print("  maps that send |y| to -|y| mod 4, as images of e0..e3:", [[format(v, "04b") for v in A] for A in Om[:3]], "...")
T1 = tuple((n - 1) ^ (1 << b) for b in range(k))          # y -> y + (|y| mod 2) * 1111
print("  T1: y -> y + (parity of y)*1111 is one of them:", T1 in Om)

def mapflag(A, chain): return tuple(frozenset(apply(A, y) for y in W) for W in chain)
idx = {c: i for i, c in enumerate(FL)}
def mappair(A, i, j):
    a, b = idx[mapflag(A, FL[i])], idx[mapflag(A, FL[j])]
    return (min(a, b), max(a, b))
S = {(i, j): e for (i, j, _, _, e) in sol}
ex = {p for p, e in S.items() if e}; m4 = {p for p, e in S.items() if not e}
imgT = {mappair(T1, i, j) for (i, j) in ex}
print("RULE TEST: T1(exact identities) == identities that hold only modulo 4 :", imgT == m4)
# orbits
def orbits(pairs, group):
    left = set(pairs); orbs = []
    while left:
        p = next(iter(left)); o = {mappair(A, *p) for A in group}
        orbs.append(o); left -= o
    return orbs
perm = [A for A in Oq if all(pc(v) == 1 for v in A)]
print("orbits of the 54 under coordinate permutations (%d maps):" % len(perm), sorted(len(o) for o in orbits(S, perm)))
print("orbits of the 54 under the maps keeping |y| mod 4 up to sign (%d maps):" % (len(Oq) + len(Om)), sorted(len(o) for o in orbits(S, Oq + Om)))
print("orbits of the 27 exact under permutations:", sorted(len(o) for o in orbits(ex, perm)), " of the 27 mod-4-only:", sorted(len(o) for o in orbits(m4, perm)))

def show(i, j, val, comps, e):
    hA = [val.get(("A", l)) for l in range(k + 1)]; hB = [val.get(("B", l)) for l in range(k + 1)]
    fa = [sorted(W) for W in FL[i][1:-1]]; fb = [sorted(W) for W in FL[j][1:-1]]
    usedA = [l for l in range(2, k + 1) if hA[l] != hA[l - 1]]; usedB = [l for l in range(2, k + 1) if hB[l] != hB[l - 1]]
    return "%s  A=%s hA=%s | B=%s hB=%s | comps=%d" % ("EXACT" if e else "MOD4 ", fa, hA, fb, hB, comps)
print("\nall 54 (h normalised with hA[0]=0; level 0 is y=0 alone):")
for s in sorted(sol, key=lambda s: (s[4], s[0], s[1])): print(" ", show(*s))
# profile table: which (hA, hB) vectors occur
from collections import Counter
prof = Counter()
for (i, j, val, comps, e) in sol:
    hA = tuple(val.get(("A", l)) for l in range(k + 1)); hB = tuple(val.get(("B", l)) for l in range(k + 1))
    prof[(e, tuple(sorted([hA, hB])))] += 1
print("\nprofiles (exact?, sorted pair of h vectors) -> count:")
for key, c in sorted(prof.items(), key=str): print("  ", key, c)
