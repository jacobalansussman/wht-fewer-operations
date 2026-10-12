# x-5-weightedz / bcost.py : the price of the change of basis B (count G: a gate is any a*u + b*v, scalings free).
# Exact whole numbers and fractions only.
#  A. two explicit Jordan bases of U ("add one element"), as integer matrices whose COLUMNS are the basis vectors (this is B^-1):
#       web   : matched pairs carry e_a - e_b, unmatched positions carry the sum of all j-subsets (d-0, i-cross schur.py)
#       tower : built one coordinate at a time (the only basis adapted to the tower, up to scalings):
#               long  string  L'_j     = L_j (x) e0 + L_(j-1) (x) e1            j = 0..d+1
#               short string  F_(j-1)  = j L_j (x) e0 - (d-j+1) L_(j-1) (x) e1  j = 1..d
#     Check for both: Z * column(string, j) = sum over m >= j of C(m, j) * column(string, m)   (Pascal blocks), and rank N.
#  B. gates of the tower basis counted from its construction: one stage per coordinate, every full 2 x 2 block is 2 gates.
#  C. greedy elimination (Gauss-Jordan, pivot of least (row count - 1)(column count - 1)), one gate per entry removed, on both.
#     Control on a matrix with a known answer: Z itself (exact minimum 12 at 8 points, Yates (N/2) k).
#  D. the pairing tree (couple halves): gates if every weight block of size m of a coupling is priced as dense, m(m-1).
import sys
from fractions import Fraction as Fr
from math import comb, log2

def zeta(v, k):
    v = v[:]
    for j in range(k):
        h = 1 << j
        for x in range(len(v)):
            if x & h: v[x] += v[x ^ h]
    return v

def web(k):
    N = 1 << k; groups = {}
    for x in range(N):
        st = []; pr = []
        for pos in range(k):
            if (x >> pos) & 1: st.append(pos)
            elif st: pr.append((st.pop(), pos))
        groups.setdefault(tuple(sorted(pr)), None)
    strings = []
    for M in groups:
        matched = set(p for pq in M for p in pq); free = [p for p in range(k) if p not in matched]; u = len(free)
        pv = {0: 1}
        for (a, b) in M:
            nv = {}
            for idx, c in pv.items():
                nv[idx | (1 << a)] = nv.get(idx | (1 << a), 0) + c; nv[idx | (1 << b)] = nv.get(idx | (1 << b), 0) - c
            pv = nv
        s = []
        for i in range(u + 1):
            v = [0] * N
            for t in range(1 << u):
                if bin(t).count("1") != i: continue
                add = sum(1 << free[q] for q in range(u) if (t >> q) & 1)
                for idx, c in pv.items(): v[idx | add] += c
            s.append(v)
        strings.append(s)
    return strings

def tower(k):
    # returns strings (lists of integer vectors), the gate count of the construction, and the largest coefficient used
    strings = [[[1, 0], [0, 1]]]        # one coordinate: e0, e1 = U e0
    gates = 0; big = 1; per_stage = []
    for i in range(2, k + 1):
        n = 1 << (i - 1); new = []; g = 0
        for s in strings:
            d = len(s) - 1
            Lg = []
            for j in range(d + 2):
                v = [0] * (2 * n)
                if j <= d:
                    for x in range(n): v[x] = s[j][x]
                if j >= 1:
                    for x in range(n): v[n + x] = s[j - 1][x]
                Lg.append(v)
            new.append(Lg)
            if d >= 1:
                Sh = []
                for j in range(1, d + 1):
                    v = [0] * (2 * n)
                    for x in range(n):
                        v[x] = j * s[j][x]; v[n + x] = -(d - j + 1) * s[j - 1][x]
                    Sh.append(v)
                    big = max(big, j, d - j + 1)
                new.append(Sh)
            g += 2 * d                      # d full 2 x 2 blocks [[1, 1], [j, -(d-j+1)]], two gates each; the two ends are copies
        strings = new
        per_stage.append((i, g))
        gates = gates * 2 + g               # the earlier stages run on both halves of the new coordinate
    return strings, gates, big, per_stage

def check(strings, k):
    N = 1 << k
    cols = [v for s in strings for v in s]
    assert len(cols) == N
    ok = True
    for s in strings:
        d = len(s) - 1
        for j in range(d + 1):
            z = zeta(s[j], k)
            want = [0] * N
            for m in range(j, d + 1):
                c = comb(m, j)
                for x in range(N):
                    if s[m][x]: want[x] += c * s[m][x]
            ok &= (z == want)
    # rank over a large prime (non-zero determinant modulo p implies non-zero over the rationals)
    p = 2147483629; A = [[cols[c][r] % p for c in range(N)] for r in range(N)]; r = 0
    for c in range(N):
        piv = next((i for i in range(r, N) if A[i][c]), None)
        if piv is None: continue
        A[r], A[piv] = A[piv], A[r]; inv = pow(A[r][c], p - 2, p); Ar = A[r]
        for i in range(r + 1, N):
            f = A[i][c]
            if f:
                f = f * inv % p; A[i] = [(x - f * y) % p for x, y in zip(A[i], Ar)]
        r += 1
    return ok, r

def greedy(rows):
    # rows: list of dicts column -> Fraction. Gauss-Jordan; returns (row operations, largest |numerator| or |denominator| of a multiplier)
    N = len(rows)
    rows = [dict(r) for r in rows]
    colrows = {}
    for i, r in enumerate(rows):
        for c in r: colrows.setdefault(c, set()).add(i)
    freeR = set(range(N)); freeC = set(colrows)
    ops = 0; big = 1
    while freeR:
        best = None
        for i in freeR:
            ri = rows[i]; rc = len(ri) - 1
            for c in ri:
                if c in freeC:
                    sc = (rc * (len(colrows[c]) - 1), len(colrows[c]))
                    if best is None or sc < best[0]: best = (sc, i, c)
                    if sc[0] == 0: break
            if best is not None and best[0][0] == 0: break
        if best is None: raise SystemExit("singular")
        _, p, c = best
        rp = rows[p]; pv = rp[c]
        for i in list(colrows[c]):
            if i == p: continue
            f = rows[i][c] / pv
            big = max(big, abs(f.numerator), abs(f.denominator))
            ri = rows[i]
            for cc, val in rp.items():
                nv = ri.get(cc, 0) - f * val
                if nv == 0:
                    if cc in ri: del ri[cc]; colrows[cc].discard(i)
                else:
                    if cc not in ri: colrows[cc].add(i)
                    ri[cc] = nv
            ops += 1
        freeR.discard(p); freeC.discard(c)
    return ops, big

def as_rows(strings, N):
    cols = [v for s in strings for v in s]
    rows = [dict() for _ in range(N)]
    for c, v in enumerate(cols):
        for x in range(N):
            if v[x]: rows[x][c] = Fr(v[x])
    return rows

def tree_dense(K):
    # pairing tree on k = 2^i coordinates. mult[d] = number of strings of length d+1. Coupling V_a (x) V_b: weight blocks of size
    # m = number of (i, j) with i + j = w; priced dense: m(m-1) gates (LU count). Returns per-point cost for k = 1, 2, 4, ...
    mult = {1: 1}; t = Fr(0); out = []; k = 1
    while k < K:
        c = 0; new = {}
        for a, ma in mult.items():
            for b, mb in mult.items():
                g = 0
                for w in range(a + b + 1):
                    m = min(w, a, b, a + b - w) + 1
                    g += m * (m - 1)
                c += ma * mb * g
                for d in range(abs(a - b), a + b + 1, 2): new[d] = new.get(d, 0) + ma * mb
        k *= 2; N = 1 << k
        t = 2 * t + Fr(c, N)
        mult = new
        out.append((k, float(t), float(Fr(c, N))))
    return out

kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 8
print("== A, B, C: gates of the change of basis (count G) ==")
print("  k    N | tower: gates  /N    /(N k)  largest coeff | greedy on tower: ops /N  mult | greedy on web: ops /N  mult | nonzeros/N web, tower | checks")
for k in range(2, kmax + 1):
    N = 1 << k
    W = web(k); T, g, big, per = tower(k)
    okW, rW = check(W, k) if k <= 8 else (None, None)
    okT, rT = check(T, k) if k <= 8 else (None, None)
    gT = greedy(as_rows(T, N)) if k <= 8 else (None, None)
    gW = greedy(as_rows(W, N)) if k <= 8 else (None, None)
    nzW = sum(1 for s in W for v in s for x in v if x); nzT = sum(1 for s in T for v in s for x in v if x)
    print("  %d %4d | %6d %6.3f %6.3f %4d | %s | %s | %.2f %.2f | Pascal web %s rank %s, tower %s rank %s" % (
        k, N, g, g / N, g / (N * k), big,
        "%6d %6.3f %s" % (gT[0], gT[0] / N, gT[1]) if gT[0] is not None else "-",
        "%6d %6.3f %s" % (gW[0], gW[0] / N, gW[1]) if gW[0] is not None else "-",
        nzW / N, nzT / N, okW, rW, okT, rT))
    sys.stdout.flush()
print("== control for the greedy counter: Z itself (known: 4, 12 at 4, 8 points; Yates (N/2) k) ==")
for k in range(2, 9):
    N = 1 << k
    rows = [{c: Fr(1) for c in range(N) if c & r == c} for r in range(N)]
    o, b = greedy(rows)
    print("  k=%d N=%d greedy ops on Z: %d  (Yates %d)" % (k, N, o, k * N // 2))
print("== B, larger k from the multiplicities alone: tower gates / N ==")
mult = {1: 1}; tot = Fr(0)
for i in range(2, 1025):
    g = sum(m * 2 * d for d, m in mult.items())
    new = {}
    for d, m in mult.items():
        new[d + 1] = new.get(d + 1, 0) + m
        if d >= 1: new[d - 1] = new.get(d - 1, 0) + m
    mult = new
    tot = tot + Fr(g, 1 << i)
    if i in (4, 6, 8, 12, 16, 32, 64, 128, 256, 512, 1024):
        print("  k=%4d  tower gates/N = %9.3f   /k = %.4f   k - gates/N = %.3f  sqrt(k) = %.2f" % (i, float(tot), float(tot) / i, i - float(tot), i ** 0.5))
print("== D. pairing tree, every weight block priced dense m(m-1): per point t(k) = 2 t(k/2) + c(k) ==")
for k, t, c in tree_dense(64):
    print("  k=%3d  t = %8.3f  t/k = %.4f   top coupling c(k) = %.3f   c/sqrt(k) = %.3f" % (k, t, t / k, c, c / k ** 0.5))
