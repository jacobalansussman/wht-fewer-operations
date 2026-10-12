#!/usr/bin/env python3
"""mir.py (p-2-mirror64class).  Exact (fractions / integers).
For a 2x2 kernel k with b*c != 0:  R = (k (x) k) P / det  with P the signed, scaled swap of k-cross hybrid 3;  R*R = I.
Mirror matrix  M_m = I - R^(x)m  (= twice the projection onto the mirror).  N = 4^m.
Read-side points = columns of M_m, write-side points = rows of M_m, both up to scale.  M_m[i][j] = 0  <=>  write point i is
perpendicular to read point j.
usage: mir.py struct            structure tables for several kernels, m = 1, 2, 3
       mir.py search16 a b c d  reduced-model search (g-0's model) at 16 points, both sides, then the three-box count
"""
import sys, itertools
from fractions import Fraction as Fr
from math import gcd

def kron(A, B): return [[a*b for a in ra for b in rb] for ra in A for rb in B]
def matmul(A, B): return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def rank(M):
    M = [[Fr(v) for v in r] for r in M]; r = 0
    if not M or not M[0]: return 0
    for c in range(len(M[0])):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        for i in range(r+1, len(M)):
            if M[i][c] != 0:
                f = M[i][c]/M[r][c]; M[i] = [a - f*b for a, b in zip(M[i], M[r])]
        r += 1
    return r
def R4(k):
    a, b, c, d = [Fr(x) for x in (k[0][0], k[0][1], k[1][0], k[1][1])]; det = a*d - b*c
    P = [[Fr(0)]*4 for _ in range(4)]; P[1][1] = Fr(1); P[2][2] = Fr(1); P[0][3] = -b/c; P[3][0] = -c/b
    KP = matmul(kron([[a,b],[c,d]], [[a,b],[c,d]]), P)
    return [[x/det for x in r] for r in KP]
def mirror(k, m):
    R = R4(k); M = R
    for _ in range(m-1): M = kron(M, R)
    n = len(M)
    assert all(sum(M[i][t]*M[t][j] for t in range(n)) == (1 if i == j else 0) for i in range(0, n, max(1, n//8)) for j in range(n)), "R^m not an involution"
    return [[(1 if i == j else 0) - M[i][j] for j in range(n)] for i in range(n)]
def prim(v):
    """primitive integer vector, first non-zero positive; None for zero"""
    den = 1
    for x in v:
        x = Fr(x); den = den*x.denominator//gcd(den, x.denominator)
    w = [int(Fr(x)*den) for x in v]; g = 0
    for x in w: g = gcd(g, abs(x))
    if g == 0: return None
    s = next(x for x in w if x != 0); s = 1 if s > 0 else -1
    return tuple(s*x//g for x in w)
def points(vecs):
    """distinct projective points among vecs; returns (list of points, index map vec->point or -1)"""
    pts = []; idx = {}; mp = []
    for v in vecs:
        p = prim(v)
        if p is None: mp.append(-1); continue
        if p not in idx: idx[p] = len(pts); pts.append(p)
        mp.append(idx[p])
    return pts, mp

def struct(name, k, ms=(1, 2, 3)):
    for m in ms:
        M = mirror(k, m); n = len(M)
        cols = [[M[i][j] for i in range(n)] for j in range(n)]; rows = M
        cp, cm = points(cols); rp, rm = points(rows)
        nz = sum(1 for r in M for x in r if x != 0)
        Np = sum(1 for t in cm if t >= 0); Npp = sum(1 for t in rm if t >= 0)
        r = rank(M) if n <= 64 else -1
        perp = sum(1 for i in range(n) for j in range(n) if rm[i] >= 0 and cm[j] >= 0 and M[i][j] == 0)
        D, Dp = len(cp), len(rp)
        floor_read = Np + D - 2*r; floor_write = Dp - r
        print("%-22s N=%3d rank r=%2d  non-zeros %4d  | non-zero columns N'=%2d distinct read points D=%2d | non-zero rows N''=%2d distinct write points D'=%2d"
              % (name, n, r, nz, Np, D, Npp, Dp))
        print("%-22s        perpendicular (write i, read j) pairs among non-zero ones: %d of %d   floors: read %d  write %d  final adds %d  => route >= %d ; textbook of the route's matrix: see report"
              % ("", perp, Np*Npp, floor_read, floor_write, Npp, floor_read + floor_write + Npp))
        sys.stdout.flush()

def nullvec(vs):
    """one non-zero rational combination of the vectors vs that vanishes, if the nullspace is 1-dimensional; else None"""
    n = len(vs); L = len(vs[0])
    A = [[Fr(vs[j][i]) for j in range(n)] for i in range(L)]   # L x n
    piv = []; r = 0
    for c in range(n):
        p = next((i for i in range(r, L) if A[i][c] != 0), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]; f = A[r][c]; A[r] = [x/f for x in A[r]]
        for i in range(L):
            if i != r and A[i][c] != 0:
                f = A[i][c]; A[i] = [x - f*y for x, y in zip(A[i], A[r])]
        piv.append(c); r += 1
    free = [c for c in range(n) if c not in piv]
    if len(free) != 1: return None
    z = [Fr(0)]*n; z[free[0]] = Fr(1)
    for i, c in enumerate(piv): z[c] = -A[i][free[0]]
    return z

def reduced(T, r, label, maxx=5, deep=True):
    """g-0's reduced model.  T: distinct target points (tuples).  Returns (x_min, list of (X, B) solutions for x_min) with
    helpers from the pool = points on at least two secants (lines through two targets)."""
    nT = len(T)
    trip_T = [c for c in itertools.combinations(range(nT), 3) if rank([T[i] for i in c]) == 2]
    print("  [%s] targets %d in dimension %d; collinear triples of targets: %d" % (label, nT, r, len(trip_T)))
    quads = [q for q in itertools.combinations(range(nT), 4) if rank([T[i] for i in q]) == 3
             and all(rank([T[i] for i in t]) == 3 for t in itertools.combinations(q, 3))]
    print("  [%s] four targets in a plane, no three on a line (4-term relations): %d" % (label, len(quads)))
    pool = {}
    for q in quads:
        a, b, c, d = q
        for (p1, p2) in (((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c))):
            z = nullvec([T[p1[0]], T[p1[1]], T[p2[0]], T[p2[1]]])
            if z is None: continue
            v = prim([z[0]*x + z[1]*y for x, y in zip(T[p1[0]], T[p1[1]])])
            if v is None or v in T: continue
            pool.setdefault(v, set()).update([p1, p2])
    P = sorted(pool)
    hist = {}
    for v in P: hist[len(pool[v])] = hist.get(len(pool[v]), 0) + 1
    print("  [%s] pool (points on at least two secants): %d ; by number of secants through them: %s" % (label, len(P), sorted(hist.items())))
    W = list(T) + P; nW = len(W)
    trips = [c for c in itertools.combinations(range(nW), 3) if rank([W[i] for i in c]) == 2]
    print("  [%s] collinear triples in targets + pool: %d" % (label, len(trips)))
    tmask = [sum(1 << i for i in c) for c in trips]
    full_T = (1 << nT) - 1
    def closure(S, allowed):
        ch = True
        while ch:
            ch = False
            for tm in tm_allowed:
                if tm & S and bin(tm & S).count('1') == 2:
                    S |= tm; ch = True
        return S
    for x in range(0, maxx+1):
        sols = []; nX = 0
        for X in itertools.combinations(range(nT, nW), x):
            nX += 1
            allowed = full_T | sum(1 << i for i in X)
            tm_allowed = [tm for tm in tmask if tm & allowed == tm]
            if len(tm_allowed) < nT + x - r: continue
            cov = 0
            for tm in tm_allowed: cov |= tm
            must = [i for i in range(nW) if allowed >> i & 1 and not cov >> i & 1]
            if len(must) > r: continue
            rest = [i for i in range(nW) if allowed >> i & 1 and cov >> i & 1]
            for Bc in itertools.combinations(rest, r - len(must)):
                S = sum(1 << i for i in must) | sum(1 << i for i in Bc)
                if closure(S, allowed) == allowed:
                    sols.append((X, tuple(must) + Bc))
        print("  [%s] x = %d: helper sets tried %d; (helper set, start set) pairs that generate everything: %d" % (label, x, nX, len(sols)))
        sys.stdout.flush()
        if sols: return x, sols, W, pool
    return None, [], W, pool

def search16(k):
    M = mirror(k, 2); n = 16; r = rank(M)
    cols = [[M[i][j] for i in range(n)] for j in range(n)]
    cp, cm = points(cols); rp, rm = points(M)
    Np = sum(1 for t in cm if t >= 0); Npp = sum(1 for t in rm if t >= 0)
    print("kernel", k, " N = 16, r =", r, " N' =", Np, " D =", len(cp), " N'' =", Npp, " D' =", len(rp))
    print(" read points (columns of the mirror matrix), which inputs carry them:")
    for t, p in enumerate(cp): print("   c%-2d" % t, p, " inputs", [j for j in range(n) if cm[j] == t])
    print(" zero columns (inputs the mirror never reads):", [j for j in range(n) if cm[j] < 0])
    print(" write points (rows), which outputs carry them:")
    for t, p in enumerate(rp): print("   e%-2d" % t, p, " outputs", [i for i in range(n) if rm[i] == t])
    print(" zero rows (outputs equal to their input):", [i for i in range(n) if rm[i] < 0])
    # perpendicularity table between distinct write points (rows) and distinct read points (columns)
    repc = [next(j for j in range(n) if cm[j] == t) for t in range(len(cp))]
    repr_ = [next(i for i in range(n) if rm[i] == t) for t in range(len(rp))]
    print(" table: write point e_s against read point c_t; '.' = perpendicular")
    for s in range(len(rp)):
        print("   e%-2d " % s + " ".join("." if M[repr_[s]][repc[t]] == 0 else "x" for t in range(len(cp))))
    xr, solr, Wr, poolr = reduced(cp, r, "read")
    xw, solw, Ww, poolw = reduced(rp, r, "write")
    if xr is None or xw is None: print(" no solution within the pool"); return
    read_cost = Np + len(cp) - 2*r + xr; write_cost = len(rp) - r + xw
    print(" READ: least helpers x = %d  => forward gates N' + D - 2r + x = %d (floor %d)" % (xr, read_cost, Np + len(cp) - 2*r))
    print(" WRITE: least helpers x' = %d => gates D' - r + x' = %d (floor %d)" % (xw, write_cost, len(rp) - r))
    # the middle: for read start set B and write start set B', the r x r table of e_b' . c_b.
    # a point of W is a rational vector in the column space (read) / row space (write); its pairing with the other side:
    # read point v = M z (z any preimage), write point u = y M; pairing = y M z / 2 = u . z / 2.  Compute through a preimage.
    def preimage_cols(v):   # solve M z = v
        z = solve(M, v); return z
    def solve(A, v):
        nA = len(A); aug = [[Fr(x) for x in A[i]] + [Fr(v[i])] for i in range(nA)]
        piv = []; rr = 0
        for c in range(nA):
            p = next((i for i in range(rr, nA) if aug[i][c] != 0), None)
            if p is None: continue
            aug[rr], aug[p] = aug[p], aug[rr]; f = aug[rr][c]; aug[rr] = [x/f for x in aug[rr]]
            for i in range(nA):
                if i != rr and aug[i][c] != 0:
                    f = aug[i][c]; aug[i] = [x - f*y for x, y in zip(aug[i], aug[rr])]
            piv.append(c); rr += 1
        assert all(aug[i][nA] == 0 for i in range(rr, nA)), "not in the space"
        z = [Fr(0)]*nA
        for i, c in enumerate(piv): z[c] = aug[i][nA]
        return z
    zr = [preimage_cols(v) for v in Wr]
    def pair(s, t): return sum(Fr(Ww[s][j])*zr[t][j] for j in range(n))
    best = None; hist = {}
    import random; random.seed(5)
    sr = solr if len(solr) <= 400 else random.sample(solr, 400)
    sw = solw if len(solw) <= 400 else random.sample(solw, 400)
    tab = {}
    for (X, B) in sr:
        for (Xp, Bp) in sw:
            nnz_rows = 0; nnz = 0
            for s in Bp:
                c = 0
                for t in B:
                    key = (s, t)
                    if key not in tab: tab[key] = pair(s, t) != 0
                    c += tab[key]
                nnz += c; nnz_rows += (c >= 2)
            hist[nnz_rows] = hist.get(nnz_rows, 0) + 1
            if best is None or (nnz_rows, nnz) < best[0]: best = ((nnz_rows, nnz), X, B, Xp, Bp)
    print(" MIDDLE over %d x %d (read, write) solution pairs: rows of the middle table with two or more non-zeros (each costs at least one gate), histogram: %s" % (len(sr), len(sw), sorted(hist.items())))
    (lo, nnz), X, B, Xp, Bp = best
    print(" best pair: middle has %d rows with >= 2 non-zeros, %d non-zeros in all (cost between %d and %d)" % (lo, nnz, lo, nnz - r))
    print("   read helpers", [Wr[i] for i in X]); print("   read start", [("c%d" % i if i < len(cp) else Wr[i]) for i in B])
    print("   write helpers", [Ww[i] for i in Xp]); print("   write start", [("e%d" % i if i < len(rp) else Ww[i]) for i in Bp])
    print(" THREE-BOX TOTAL at 16 points: final adds %d + read %d + middle >= %d + write %d = >= %d   (floor of the route %d)"
          % (Npp, read_cost, lo, write_cost, Npp + read_cost + lo + write_cost, Npp + Np + len(cp) - 2*r + len(rp) - r))

if __name__ == "__main__":
    if sys.argv[1] == "struct":
        for name, k in [("zeta [[1,1],[1,0]]", [[1,1],[1,0]]), ("mirror image [[0,1],[1,1]]", [[0,1],[1,1]]), ("[[1,1],[1,2]]", [[1,1],[1,2]]),
                        ("transform [[1,1],[1,-1]]", [[1,1],[1,-1]]), ("[[1,2],[3,4]]", [[1,2],[3,4]])]:
            struct(name, k)
    elif sys.argv[1] == "search16":
        a, b, c, d = map(int, sys.argv[2:6]); search16([[a, b], [c, d]])
