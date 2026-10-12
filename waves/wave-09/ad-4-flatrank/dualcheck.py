#!/usr/bin/env python3
"""dualcheck.py [ad-4-flatrank]  Lemma B of ad-4.md on examples, in whole numbers.
For each decomposition g = sum c_j f_j (candidates of fr, re-solved exactly): transform every f_j and g (the +-1 transform on K bits);
check that each transform is a multiple of a signed flat of dimension K - d_j; that the transform of g is +-2^(K/2) times a bent quadratic
sign pattern; then take two flats that are not points with directions v_i in V_i, v_j in V_j, B(v_i, v_j) = 1, restrict the transformed
identity to W' = {y : v_i.y = v_i.b_i + 1, v_j.y = v_j.b_j + 1} (b = the flat's own sign vector) and check: both transforms vanish on W',
the survivors add up to the transform of g on W', and that restriction is bent on K - 2 bits.
Also: the totally singular subspaces of K/2 bits at K = 6 and the largest family meeting pairwise in 0."""
import sys, itertools
from fractions import Fraction
sys.path.insert(0, ".")
def wt(x): return bin(x).count("1")
def quad(z, K): return sum(((z >> i) & 1) & ((z >> (i + 1)) & 1) for i in range(0, K, 2)) & 1
def Bf(a, b, K): return quad(a ^ b, K) ^ quad(a, K) ^ quad(b, K)
def wht(v):
    v = list(v); n = len(v); h = 1
    while h < n:
        for i in range(0, n, 2 * h):
            for j in range(i, i + h):
                a, b = v[j], v[j + h]; v[j], v[j + h] = a + b, a - b
        h *= 2
    return v
def is_flat(mask_pts, N):
    a = mask_pts[0]; V = {p ^ a for p in mask_pts}
    return all((x ^ y) in V for x in V for y in V) and (len(V) & (len(V) - 1)) == 0
def bent(vals):    # vals: +-1 on 2^n points indexed 0..2^n-1 (any affine labelling); bent iff all transform values have the same size
    t = wht(vals); return len({abs(x) for x in t}) == 1
def solve(vecs, g):
    n = len(g); r = len(vecs)
    rows = [[Fraction(vecs[j][z]) for j in range(r)] + [Fraction(g[z])] for z in range(n)]; rk = 0; piv = []
    for c in range(r):
        p = next((i for i in range(rk, n) if rows[i][c] != 0), None)
        if p is None: continue
        rows[rk], rows[p] = rows[p], rows[rk]; inv = 1 / rows[rk][c]; rows[rk] = [v * inv for v in rows[rk]]
        for i in range(n):
            if i != rk and rows[i][c] != 0:
                f = rows[i][c]; rows[i] = [a - f * b for a, b in zip(rows[i], rows[rk])]
        piv.append(c); rk += 1
    assert all(rw[-1] == 0 for rw in rows[rk:]); coef = [Fraction(0)] * r
    for i, c in enumerate(piv): coef[c] = rows[i][-1]
    return coef
tot = ok = 0; survs = {}
for fn in sys.argv[1:]:
    for line in open(fn):
        if not line.startswith("CANDIDATE"): continue
        head = line.split("(")[0].split(); r = int(head[1].split("=")[1]); K = int(head[2].split("=")[1]); N = 1 << K
        g = [(-1) ** quad(z, K) for z in range(N)]; gh = wht(g)
        assert len({abs(x) for x in gh}) == 1 and abs(gh[0]) == 1 << (K // 2)
        vecs = []; info = []
        for t in line.split("):")[1].split():
            sup, neg = (int(x, 16) for x in t.split(":")); pts = [z for z in range(N) if (sup >> z) & 1]
            vec = [0 if not (sup >> z) & 1 else (-1 if (neg >> z) & 1 else 1) for z in range(N)]; vecs.append(vec)
            a = pts[0]; V = sorted(p ^ a for p in pts)
            th = wht(vec); spts = [y for y in range(N) if th[y]]
            assert is_flat(spts, N) and len(spts) * len(pts) == N and len({abs(x) for x in th if x}) == 1      # transform = multiple of a signed flat, dimension K - d
            # sign vector b of the flat: any point of the transform's support
            info.append((V, spts[0], th))
        coef = solve(vecs, g)
        assert all(sum(coef[j] * info[j][2][y] for j in range(r)) == gh[y] for y in range(N))                 # the transformed identity
        done = False
        for i in range(r):
            for j in range(i + 1, r):
                if done or len(info[i][0]) == 1 or len(info[j][0]) == 1: continue
                for vi in info[i][0]:
                    for vj in info[j][0]:
                        if done or not Bf(vi, vj, K): continue
                        ci = (wt(vi & info[i][1]) & 1) ^ 1; cj = (wt(vj & info[j][1]) & 1) ^ 1
                        W = [y for y in range(N) if (wt(vi & y) & 1) == ci and (wt(vj & y) & 1) == cj]
                        assert all(info[i][2][y] == 0 and info[j][2][y] == 0 for y in W)                      # both killed
                        s = sum(1 for (V, b, th) in info if any(th[y] for y in W))
                        # bent on W: label W by an affine frame
                        w0 = W[0]; dirs = sorted(y ^ w0 for y in W); basis = []
                        span = {0}
                        for d in dirs:
                            if d not in span: basis.append(d); span |= {x ^ d for x in span}
                        lab = []
                        for idx in range(len(W)):
                            y = w0
                            for bi, bv in enumerate(basis):
                                if (idx >> bi) & 1: y ^= bv
                            lab.append(gh[y] // abs(gh[y]))
                        assert bent(lab)
                        survs[(K, r, s)] = survs.get((K, r, s), 0) + 1; done = True
        tot += 1; ok += done
print("Lemma B on examples: %d decompositions, %d with a pair of non-point flats whose directions are not perpendicular; in each: every transform is a multiple of a signed flat of the complementary dimension, the transformed identity holds, both flats vanish on W', and the transform of g on W' is bent on K - 2 bits" % (tot, ok))
for (K, r, s), n in sorted(survs.items()): print("   K=%d, %d flats: %d survive the projection (first pair found) in %d cases" % (K, r, s, n))
# totally singular 3-subspaces at K = 6
K = 6; N = 64; sing = [z for z in range(1, N) if quad(z, K) == 0]
subs = set()
for a, b, c in itertools.combinations(sing, 3):
    S = {0, a, b, c, a ^ b, a ^ c, b ^ c, a ^ b ^ c}
    if len(S) == 8 and all(quad(z, K) == 0 for z in S): subs.add(frozenset(S))
subs = list(subs)
disj = [(i, j) for i in range(len(subs)) for j in range(i + 1, len(subs)) if len(subs[i] & subs[j]) == 1]
tri = sum(1 for (i, j) in disj for l in range(j + 1, len(subs)) if len(subs[i] & subs[l]) == 1 and len(subs[j] & subs[l]) == 1)
print("K=6: %d singular non-zero points, %d totally singular subspaces of 3 bits, %d pairs meeting in 0 only, %d triples pairwise meeting in 0 only (a spread would need 5)" % (len(sing), len(subs), len(disj), tri))
