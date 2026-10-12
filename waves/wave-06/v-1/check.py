#!/usr/bin/env python3
# v-1: independent checks of the four "one line through the cube" proofs (u-0, u-1, u-2, u-6).
# Whole numbers and exact fractions only, except where a logarithm is printed (marked "float").
# Usage: check.py exh | bricks | adv | bounds | files
import sys, math, random, re
from fractions import Fraction
from itertools import permutations
from math import comb
try:
    import numpy as np
except ImportError:
    np = None

def zmat(k):
    N = 1 << k
    s = np.arange(N)
    return ((s[None, :] & ~s[:, None]) == 0).astype(np.int8)   # [S, T] = 1 iff T inside S

def picture(Z, rows, cols):
    N = len(rows)
    A = np.zeros((N + 1, N + 1), dtype=np.int16)
    A[:N, :N] = Z[np.ix_(rows, cols)]
    return A

def corners(A):
    M = A[:-1, :-1] - A[1:, :-1] - A[:-1, 1:] + A[1:, 1:]
    return int(np.count_nonzero(M))

def gray(k):
    return [i ^ (i >> 1) for i in range(1 << k)]

def pc(x):
    return bin(x).count("1")

# ---------------------------------------------------------------- exhaustive minima
def exh4():
    Z = zmat(2); best = 99; cnt = 0
    for r in permutations(range(4)):
        for c in permutations(range(4)):
            v = corners(picture(Z, list(r), list(c)))
            if v < best: best, cnt = v, 1
            elif v == best: cnt += 1
    print("4 points: least corners", best, "optimal pairs", cnt)

def exh8():
    Z = zmat(3)
    P = np.array(list(permutations(range(8))), dtype=np.int64)
    n = len(P)
    A = np.zeros((n, 9, 9), dtype=np.int8)
    A[:, :8, :8] = Z[:, P].transpose(1, 0, 2)
    E = A[:, :, :8] - A[:, :, 1:]
    W = np.count_nonzero(E[:, :, None, :] - E[:, None, :, :], axis=3).astype(np.int16)
    INF = 10000
    f = np.full((256, 8, n), INF, dtype=np.int16)
    g = np.zeros((256, 8, n), dtype=np.int32)
    for i in range(8):
        f[1 << i, i] = 0; g[1 << i, i] = 1
    for mask in range(1, 256):
        for last in range(8):
            if not (mask >> last) & 1: continue
            fl = f[mask, last]; gl = g[mask, last]
            for nx in range(8):
                if (mask >> nx) & 1: continue
                nm = mask | (1 << nx)
                cand = fl + W[:, last, nx]
                cur = f[nm, nx]
                g[nm, nx] = np.where(cand < cur, gl, np.where(cand == cur, g[nm, nx] + gl, g[nm, nx]))
                f[nm, nx] = np.minimum(cur, cand)
    tot = np.full(n, INF, dtype=np.int32); num = np.zeros(n, dtype=np.int64)
    for last in range(8):
        cand = f[255, last].astype(np.int32) + W[:, last, 8]
        num = np.where(cand < tot, g[255, last], np.where(cand == tot, num + g[255, last], num))
        tot = np.minimum(tot, cand)
    m = int(tot.min())
    print("8 points: least corners", m, "optimal pairs", int(num[tot == m].sum()), "input orders reaching it", int((tot == m).sum()))
    vals, cts = np.unique(tot, return_counts=True)
    print("8 points: histogram of best count per input order", dict(zip(vals.tolist(), cts.tolist())))

# ---------------------------------------------------------------- the bricks of the proofs
def runlen_left(B):
    # B: (n, N) values; left[a,b] = length of the maximal constant stretch ending at b, 0 where B is 0
    n, N = B.shape
    L = np.zeros((n, N), dtype=np.int32)
    L[:, 0] = (B[:, 0] != 0)
    for b in range(1, N):
        same = (B[:, b] == B[:, b - 1])
        L[:, b] = np.where(B[:, b] != 0, np.where(same, L[:, b - 1] + 1, 1), 0)
    return L

def bricks(k, Z, rows, cols, lemma3=True):
    N = 1 << k
    rows = list(rows); cols = list(cols)
    A = picture(Z, rows, cols)
    D = (A[:N, :] - A[1:, :]).astype(np.int8)            # D[a, b], b = 0..N, last column 0
    nz = np.count_nonzero(D[:, :N] != D[:, 1:], axis=1)   # non-zeros of row a of M
    out = {"corners": int(nz.sum())}
    assert out["corners"] == corners(A)
    Dn = D[:, :N]
    left = runlen_left(Dn)
    right = runlen_left(Dn[:, ::-1])[:, ::-1]
    starts = (Dn != 0) & np.concatenate([np.ones((N, 1), bool), Dn[:, 1:] != Dn[:, :-1]], axis=1)
    R = int(starts.sum()); out["runs"] = R
    assert out["corners"] >= R, "corners >= runs fails"
    c = np.count_nonzero(Dn, axis=0)                      # c(T) per input position
    S = (left + right - (Dn != 0)).sum(axis=0)            # total length of runs through T
    # u-2 step 1: j * (left part of the j-th longest-left run through T) <= 2N
    j = np.arange(1, N + 1)[:, None]
    r1 = max(int((np.sort(left, axis=0)[::-1] * j).max()), int((np.sort(right, axis=0)[::-1] * j).max()))
    out["u2_step1 max j*len/(2N)"] = Fraction(r1, 2 * N)
    assert r1 <= 2 * N, "u-2 step 1 fails"
    rs = max(float(S[b]) / (4 * N * (1 + math.log(c[b]))) for b in range(N) if c[b] > 0)   # float
    out["u2 S/(4N(1+ln c)) max (float)"] = round(rs, 4)
    assert rs <= 1 + 1e-12
    # u-2 step 2: R >= sum c^2 / S (exact)
    lb = sum(Fraction(int(c[b]) ** 2, int(S[b])) for b in range(N) if c[b] > 0)
    out["u2 sum c^2/S"] = float(lb)
    assert R >= lb, "u-2 step 2 fails"
    # u-2 step 3: V_j >= (j/k) C(k,j) (2^(k-j) - 1/2);   100 * sum c^2 >= 5^k
    sz = np.array([pc(t) for t in cols])
    for jj in range(1, k + 1):
        Vj = int(c[sz == jj].sum())
        assert 2 * k * Vj >= jj * comb(k, jj) * (2 ** (k - jj + 1) - 1), ("u-2 step 3 fails", jj)
    sc2 = int((c.astype(np.int64) ** 2).sum()); V = int(c.sum())
    out["V/3^k"] = round(V / 3 ** k, 4); out["sum c^2/5^k"] = round(sc2 / 5 ** k, 4)
    assert 2 * V >= 3 ** k - N // 2
    assert 100 * sc2 >= 5 ** k
    out["u2 final R*400(1+lnN)/(5/2)^k (float)"] = round(R * 400 * (1 + math.log(N)) / 2.5 ** k, 2)
    assert R * 400 * (1 + math.log(N)) >= 2.5 ** k
    # ---------------- u-1
    Zc = Z[:, cols]                                       # Zc[S, b]
    tops = []; others = []
    for a in range(N):
        if a == N - 1: tops.append(rows[a]); others.append(-1)
        else:
            s, t = rows[a], rows[a + 1]
            if pc(s) >= pc(t): tops.append(s); others.append(t)
            else: tops.append(t); others.append(s)
    Zt = Zc[tops]; Zo = np.array([Zc[o] if o >= 0 else np.zeros(N, np.int8) for o in others])
    Rp = (Zt == 1) & (Zo == 0)
    st = Rp & np.concatenate([np.ones((N, 1), bool), ~Rp[:, :-1]], axis=1)
    runsRp = st.sum(axis=1)
    assert (nz >= runsRp).all(), "non-zeros >= runs of R+ fails"
    ts = np.array([pc(t) for t in tops])
    assert (Rp.sum(axis=1) >= 2 ** np.maximum(ts - 1, 0)).all() or (ts == 0).any()
    for a in range(N):
        if ts[a] >= 1: assert int(Rp[a].sum()) >= 2 ** (ts[a] - 1), "|R+| >= 2^(s-1) fails"
    one = int((nz == 1).sum()); out["single-non-zero steps"] = one
    assert one <= 2 * k + 1, "u-1 lemma 1 fails"
    pos = {t: b for b, t in enumerate(cols)}
    rid = np.cumsum(st, axis=1)
    mem = np.zeros(N, dtype=np.int64)
    for a in range(N):
        b = pos[tops[a]]
        assert Rp[a, b]
        mem += (Rp[a] & (rid[a] == rid[a, b]))
    out["top runs through one input, max"] = int(mem.max())
    assert mem.max() <= 4 * (k + 1), "u-1 lemma 2 fails"
    if lemma3:
        worst = Fraction(0)
        for s in range(1, k + 1):
            rr = sorted(int(x) for x in runsRp[ts == s])
            if not rr: continue
            for r in sorted(set(rr)):
                cnt = sum(1 for x in rr if x <= r)
                l = Fraction(2 ** (s - 1), r)
                for L in range(1, int(l) + 1):
                    lam = (L - 1).bit_length()
                    cap = 2 * (N - L + 1) * comb(k - lam, s - lam)
                    lhs = cnt * (l - L + 1)
                    assert lhs <= cap, ("u-1 lemma 3 fails", s, r, L, cnt)
                    worst = max(worst, lhs / cap)
        out["u1 lemma3 max lhs/cap"] = round(float(worst), 4)
    # ---------------- u-0
    lb1 = runlen_left(Zc).max(axis=1)                     # longest block of inputs inside each output S
    for a in range(N):
        s = rows[a]; t = rows[a + 1] if a < N - 1 else -1
        for x, y in ((s, t), (t, s)):
            if x < 0: continue
            if y >= 0 and (x & ~y) == 0: continue          # x inside y: lemma does not apply to x
            assert int(lb1[x]) * int(nz[a]) >= 2 ** max(pc(x) - 1, 0), "u-0 block lemma fails"
    worst = Fraction(0)
    for jl in range(1, k + 1):
        blk = sorted(int(lb1[s]) for s in range(N) if pc(s) == jl)
        for L in range(1, 2 ** jl + 1):
            cnt = sum(1 for x in blk if x >= L)
            if cnt == 0: break
            for t in range(1, jl + 1):
                ov = 2 ** (jl - t)
                if L <= ov: continue
                Vt = sum(comb(jl, i) * comb(k - jl, i) for i in range(t))
                cap = Fraction(N - L, L - ov) + 1
                assert cnt <= cap * Vt, ("u-0 packing fails", jl, L, t, cnt)
                worst = max(worst, Fraction(cnt) / (cap * Vt))
    out["u0 packing max cnt/(P V)"] = round(float(worst), 4)
    return out

def show(tag, o):
    print(tag, "| " + "; ".join("%s=%s" % (a, (float(b) if isinstance(b, Fraction) else b)) for a, b in o.items()), flush=True)

def run_bricks():
    rnd = random.Random(20261011)
    for k in range(2, 10):
        N = 1 << k; Z = zmat(k)
        g = gray(k); cnt = list(range(N))
        show("k=%d gray/gray" % k, bricks(k, Z, g, g))
        show("k=%d count/count" % k, bricks(k, Z, cnt, cnt))
        show("k=%d gray/count" % k, bricks(k, Z, g, cnt))
        nrand = {2: 300, 3: 300, 4: 200, 5: 100, 6: 40, 7: 20, 8: 6, 9: 3}[k]
        agg = {}
        for _ in range(nrand):
            r = cnt[:]; c = cnt[:]; rnd.shuffle(r); rnd.shuffle(c)
            o = bricks(k, Z, r, c)
            for a, b in o.items(): agg[a] = max(agg.get(a, b), b)
        show("k=%d random x%d (max of each)" % (k, nrand), agg)
    Z = zmat(4)
    o = bricks(4, Z, [11, 9, 8, 10, 14, 2, 6, 7, 3, 1, 5, 13, 12, 4, 0, 15], [4, 6, 14, 12, 8, 13, 9, 1, 5, 7, 3, 2, 10, 11, 15, 0])
    show("u-0's 16-point picture", o)

def run_files():
    base = "waves/wave-06/u-0-cornerssearch/"
    for fn in ("r32.out", "r64_first.out", "t128.out"):
        txt = open(base + fn).read()
        r = re.search(r"rows \[([0-9, ]+)\]", txt); c = re.search(r"cols \[([0-9, ]+)\]", txt)
        rows = [int(x) for x in r.group(1).split(",")]; cols = [int(x) for x in c.group(1).split(",")]
        k = len(rows).bit_length() - 1
        assert sorted(rows) == list(range(1 << k)) and sorted(cols) == list(range(1 << k))
        show(fn, bricks(k, zmat(k), rows, cols))

def run_adv():
    # hill-climb AGAINST the lemmas: try to push each ratio above 1
    rnd = random.Random(7)
    for k in (3, 4, 5):
        N = 1 << k; Z = zmat(k)
        for key in ("u2_step1 max j*len/(2N)", "u1 lemma3 max lhs/cap", "single-non-zero steps", "top runs through one input, max", "u0 packing max cnt/(P V)", "u2 S/(4N(1+ln c)) max (float)"):
            best = None
            for rest in range(3):
                r = list(range(N)); c = list(range(N)); rnd.shuffle(r); rnd.shuffle(c)
                cur = bricks(k, Z, r, c)[key]
                for it in range({3: 1500, 4: 700, 5: 250}[k]):
                    which = r if rnd.random() < 0.5 else c
                    i, j2 = rnd.randrange(N), rnd.randrange(N)
                    which[i], which[j2] = which[j2], which[i]
                    v = bricks(k, Z, r, c)[key]
                    if v >= cur: cur = v
                    else: which[i], which[j2] = which[j2], which[i]
                best = cur if best is None else max(best, cur)
            print("k=%d adversarial max of [%s] = %s   (limit: %s)" % (k, key, float(best) if isinstance(best, Fraction) else best,
                  {"single-non-zero steps": 2 * k + 1, "top runs through one input, max": 4 * (k + 1)}.get(key, 1)), flush=True)

def run_bounds():
    # u-2: exact sum against 5^k/100, and where the bound passes N, 3N, Yates
    okmin = None
    for k in range(1, 301):
        s = sum(Fraction(j * j, k * k) * comb(k, j) * (Fraction(2 ** (k - j)) - Fraction(1, 2)) ** 2 for j in range(1, k + 1))
        ratio = s / Fraction(5 ** k)
        okmin = ratio if okmin is None else min(okmin, ratio)
        assert 100 * s >= 5 ** k, k
    print("u-2: exact sum_j (j/k)^2 C(k,j)(2^(k-j)-1/2)^2 >= 5^k/100 for k = 1..300; least ratio to 5^k:", float(okmin), "(limit 1/25 =", 0.04, ")")
    marks = {}
    for k in range(2, 200):
        N = 2 ** k
        lb = 2.5 ** k / (400 * (1 + math.log(N)))
        for name, thr in (("N", N), ("3N", 3 * N), ("Yates (N/2)k+1", N * k / 2 + 1)):
            if name not in marks and lb > thr: marks[name] = k
    print("u-2 bound (5/2)^k/(400(1+ln N)) first exceeds:", marks, " (float)")
    for k in (16, 32, 64, 100, 101):
        print("  k=%d  u-2 bound / N = %.4g" % (k, 2.5 ** k / (400 * (1 + math.log(2.0 ** k))) / 2.0 ** k))
    # u-1: explicit window bound, my own optimisation (threshold size s0, r runs)
    def B(k, s, r):
        N = 2 ** k; l = Fraction(2 ** (s - 1), r); best = 2 * comb(k, s)
        Lmax = int(l)
        cand = set(x for x in (1, Lmax, Lmax // 2, Lmax // 2 + 1, 1 << max(Lmax.bit_length() - 2, 0), 1 << max(Lmax.bit_length() - 3, 0)) if 1 <= x <= Lmax)
        for L in cand:
            if L < 1: continue
            lam = (L - 1).bit_length()
            v = Fraction(2 * (N - L + 1) * comb(k - lam, s - lam)) / (l - L + 1)
            best = min(best, int(v))
        return best
    print("u-1 window bound, my optimisation: corners >= (r+1) * (steps with top size >= s0  -  those allowed <= r runs)")
    for k in (16, 19, 20, 24, 32, 40, 48, 64, 96, 128):
        N = 2 ** k; bestv = 0; arg = None
        for s0 in range(max(2, k // 2 - 4), min(k, k // 2 + 24) + 1, 1 if k <= 48 else 2):
            nl = sum(comb(k, s) for s in range(s0, k + 1))
            r = 1
            while r <= 2 ** (s0 - 1):
                few = sum(B(k, s, r) for s in range(s0, k + 1))
                v = (r + 1) * (nl - few) + (N - nl)      # the other steps cost at least 1 each
                if v > bestv: bestv, arg = v, (s0, r)
                r *= 2
        print("  k=%d  bound/N = %.4g at (s0, r) = %s ;  Yates/N = %.4g" % (k, bestv / N, arg, k / 2))
    # exponent of u-1's method: at sizes s = sigma k, runs 2^(alpha k)
    def h(x): return 0.0 if x <= 0 or x >= 1 else -x * math.log2(x) - (1 - x) * math.log2(1 - x)
    def alpha_star(sig):
        lo, hi = 0.0, 1.0
        f = lambda a: 1 + a - sig + (1 - sig + a) * h(a / (1 - sig + a)) - h(sig)
        if f(1e-9) >= 0: return 0.0
        for _ in range(80):
            mid = (lo + hi) / 2
            if f(mid) < 0: lo = mid
            else: hi = mid
        return lo
    print("u-1 method, exponent h(sigma) + alpha*(sigma) (float):")
    bestx = (0, 0, 0)
    for i in range(500, 1000):
        sig = i / 1000; a = alpha_star(sig); x = h(sig) + a
        if x > bestx[0]: bestx = (x, sig, a)
    print("  at sigma = 1/2: alpha* = %.4f, exponent %.4f;  best over sigma: exponent %.4f at sigma = %.3f (alpha* = %.4f)" % (alpha_star(0.5), 1 + alpha_star(0.5), bestx[0], bestx[1], bestx[2]))
    print("  u-2 exponent log2(5/2) = %.4f ; upper bound log2 3 = %.4f" % (math.log2(2.5), math.log2(3)))

if __name__ == "__main__":
    what = sys.argv[1]
    if what == "exh": exh4(); exh8()
    elif what == "bricks": run_bricks()
    elif what == "files": run_files()
    elif what == "adv": run_adv()
    elif what == "bounds": run_bounds()
