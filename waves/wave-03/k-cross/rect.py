# k-cross: fewest constant rectangles over two hierarchies summing to a sign-rescaled transform.
# Solver output is FLOATING POINT (HiGHS): candidates only; anything interesting must be replayed exactly.
import numpy as np, itertools, sys, time, random
from scipy.optimize import linprog, milp, LinearConstraint, Bounds
from scipy.sparse import csr_matrix

def Hm(k):
    N = 1 << k
    return np.array([[(-1)**bin(a & x).count('1') for x in range(N)] for a in range(N)], dtype=float)

def dictionary(rownodes, colnodes, N):
    cols = []
    for nu in rownodes:
        for mu in colnodes:
            M = np.zeros((N, N)); M[np.ix_(list(nu), list(mu))] = 1.0
            cols.append(M.ravel())
    return np.array(cols).T

def l1(A, b):
    n = A.shape[1]
    res = linprog(np.ones(2*n), A_eq=np.hstack([A, -A]), b_eq=b, bounds=(0, None), method='highs')
    if res.status != 0: return None, None
    p = res.x[:n] - res.x[n:]
    return int((np.abs(p) > 1e-7).sum()), p

def l0(A, b, M=16.0, tl=240):
    n = A.shape[1]
    c = np.concatenate([np.zeros(n), np.ones(n)])
    I = np.eye(n)
    cons = [LinearConstraint(np.hstack([A, np.zeros_like(A)]), b, b),
            LinearConstraint(np.hstack([I, -M*I]), -np.inf, 0), LinearConstraint(np.hstack([-I, -M*I]), -np.inf, 0)]
    res = milp(c, constraints=cons, integrality=np.concatenate([np.zeros(n), np.ones(n)]),
               bounds=Bounds(np.concatenate([-M*np.ones(n), np.zeros(n)]), np.concatenate([M*np.ones(n), np.ones(n)])),
               options={'time_limit': tl})
    return res

print("== 8 points, g-1's design ==")
H8 = Hm(3)
astar = np.array([-1,1,1,1,1,-1,1,1.]); c = np.array([1,-1,-1,-1,1,1,-1,1.])
Hp = H8 * np.outer(astar, c)
rown = [tuple(range(8)), (1,2,4,7), (0,3,5,6), (1,7), (2,4), (0,6), (3,5)] + [(i,) for i in range(8)]
coln = [tuple(range(8)), (0,1,6,7), (2,3,4,5), (0,7), (1,6), (2,5), (3,4)] + [(i,) for i in range(8)]
A = dictionary(rown, coln, 8)
print(" entries -1 in the rescaled transform:", int((Hp < 0).sum()), "of 64;  dictionary", A.shape)
n1, p = l1(A, Hp.ravel()); print(" least sum of |constants| solution uses", n1, "rectangles")
for M in (4.0, 64.0, 1024.0):
    t0 = time.time(); r = l0(A, Hp.ravel(), M=M, tl=150)
    print(" fewest rectangles with constants bounded by", M, ":", None if r.x is None else round(r.fun), " solver status", r.status, r.message, " (%.0f s)" % (time.time() - t0))
    if r.x is not None:
        pp = r.x[:A.shape[1]]; nz = [(rown[i // 15], coln[i % 15], round(pp[i], 6)) for i in range(225) if abs(pp[i]) > 1e-7]
        print("   ", nz)
    sys.stdout.flush()

print("== 16 points: bent centre, its dual on the output side, dual chains; least-|constants| solutions (upper bounds only) ==")
k = 4; N = 16; H16 = Hm(4)
vecs = list(range(1, 16))
def span(gens):
    S = {0}
    for g in gens: S |= {s ^ g for s in S}
    return S
def perp(S): return {x for x in range(16) if all(bin(x & s).count('1') % 2 == 0 for s in S)}
def cosets(S):
    seen = set(); out = []
    for x in range(16):
        if x in seen: continue
        cs = tuple(sorted(x ^ s for s in S)); seen |= set(cs); out.append(cs)
    return out
flags = []
for v1 in vecs:
    for v2 in vecs:
        if v2 in span([v1]): continue
        for v3 in vecs:
            if v3 in span([v1, v2]): continue
            f = (frozenset(span([v1])), frozenset(span([v1, v2])), frozenset(span([v1, v2, v3])))
            if f not in flags: flags.append(f)
print(" flags:", len(flags))
# bent quadratic sign vectors: Q(x) = sum_{i<j} q_ij x_i x_j + linear + const, with non-degenerate polar form
bents = []
pairs = [(i, j) for i in range(4) for j in range(i+1, 4)]
for qm in range(64):
    B = np.zeros((4, 4), dtype=int)
    for t, (i, j) in enumerate(pairs):
        if qm >> t & 1: B[i, j] = B[j, i] = 1
    if round(np.linalg.det(B)) % 2 == 0: continue
    for lin in range(16):
        s = np.array([(-1)**((sum(B[i, j] * (x >> i & 1) * (x >> j & 1) for (i, j) in pairs) + bin(x & lin).count('1')) % 2) for x in range(16)], dtype=float)
        bents.append(s)
print(" bent quadratic centres (up to sign):", len(bents))
random.seed(5); best = (10**9, None); hist = {}; t0 = time.time(); done = 0
combos = [(b, f) for b in range(len(bents)) for f in range(len(flags))]
random.shuffle(combos)
for (bi, fi) in combos:
    if time.time() - t0 > 780: break
    cc = bents[bi]; a = H16 @ cc / 4.0
    V1, V2, V3 = flags[fi]
    rown = [tuple(range(16))] + cosets(V3) + cosets(V2) + cosets(V1) + [(i,) for i in range(16)]
    U1, U2, U3 = perp(V3), perp(V2), perp(V1)
    coln = [tuple(range(16))] + cosets(U3) + cosets(U2) + cosets(U1) + [(i,) for i in range(16)]
    A = dictionary(rown, coln, 16)
    n1, p = l1(A, (H16 * np.outer(a, cc)).ravel()); done += 1
    if n1 is None: continue
    hist[n1] = hist.get(n1, 0) + 1
    if n1 < best[0]:
        best = (n1, (bi, fi)); print("  new best: rectangles", n1, " -> gates N - 2 + tau =", 14 + n1, " centre", cc.astype(int).tolist(), " flag", [sorted(v) for v in flags[fi]], " max |constant| %.3f" % np.abs(p).max()); sys.stdout.flush()
print(" designs tried:", done, " histogram of rectangle counts:", sorted(hist.items()))
print(" best upper bound from this sweep: tau(16) <=", best[0], ", gates", 14 + best[0], "(known: 52)")
