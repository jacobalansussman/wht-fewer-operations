#!/usr/bin/env python3
"""af-0/own.py  My own builder of the 'selector and atoms' circuit for a polynomial of degree <= 2 on the cube, written
from the identity q(a, y) = A(y) + B_a(y outside atom a) and nothing else; imports nothing of ad-6.
It writes an explicit program: wires 0..D-1 are the coefficients; a gate is (i, si, j, sj) = si*wire_i + sj*wire_j with
si, sj = +-1 (count (G); also one operation in count (O) when both signs are +, or one is -).
Then (1) replays the program on every unit input with whole numbers (exact, a proof), (2) counts the helper classes
that the last layer reads, (3) checks a count-only formula against the built programs, (4) pushes the formula far.
usage: own.py kbuild kexact kcount"""
import sys, math
from itertools import combinations
from functools import lru_cache
from fractions import Fraction
TMAX = 16
PC = [bin(i).count('1') for i in range(1 << TMAX)]
PRE = [0]
for i in range(1 << TMAX): PRE.append(PRE[-1] + PC[i])
def sizes2(m, t):
    g = 1 << t; lo = m // g; r = m % g; return lo, r          # atoms 0..r-1 have lo+1 bits, the others lo bits
def step_count(k, t, sub):
    g = 1 << t; m = k - t; lo, r = sizes2(m, t); N = 1 << k
    lina = lo * t * (g >> 1) + PRE[r]
    ca = sum(math.comb(t, w) * max(0, w + w * (w - 1) // 2 - 1) for w in range(t + 1))
    coef = m * (t * (g >> 1) - g + 1)
    sz0 = lo + (1 if r > 0 else 0)
    aff = r * (1 << (m - lo - 1)) + (g - r) * (1 << (m - lo)) - g - (m - sz0)
    return sub(m) + lina + ca + coef + aff + N - (1 << sz0)
BEST = {0: (0, 0), 1: (1, 0), 2: (4, 0)}
def fill(K):
    for k in range(3, K + 1):
        if k in BEST: continue
        BEST[k] = min((step_count(k, t, lambda m: BEST[m][0]), t) for t in range(1, min(k - 1, TMAX) + 1))
class Prog:
    def __init__(s, D): s.D = D; s.gates = []
    def add(s, u, v):                       # u, v are (wire, sign) or None (= zero)
        if v is None: return u
        if u is None: return v
        if u[1] == -1 and v[1] == -1:          # -(u + v): do the plain addition and carry the sign forward (free in both counts)
            s.gates.append((u[0], 1, v[0], 1)); return (s.D + len(s.gates) - 1, -1)
        s.gates.append((u[0], u[1], v[0], v[1])); return (s.D + len(s.gates) - 1, 1)
neg = lambda u: None if u is None else (u[0], -u[1])
def affine(P, c, coefs):                    # all values of c + sum of chosen coefs, by doubling
    vals = {0: c}
    for p, w in coefs:
        vals.update({mk | (1 << p): P.add(v, w) for mk, v in list(vals.items())})
    return vals
def quad(P, c, lin, Q, bits, stats):
    k = len(bits); qq = lambda p, q: Q[(p, q)] if p < q else Q[(q, p)]
    if k <= 2:
        vals = {0: c}
        for j, p in enumerate(bits):
            new = {}
            for mk, v in list(vals.items()):
                w = P.add(v, lin[p])
                for q in bits[:j]:
                    if mk >> q & 1: w = P.add(w, qq(q, p))
                new[mk | (1 << p)] = w
            vals.update(new)
        return vals
    t = BEST[k][1]; g = 1 << t; sel = bits[:t]; Y = bits[t:]; m = k - t
    atom = {p: j % g for j, p in enumerate(Y)}
    linA = {}
    for p in Y:
        w = lin[p]
        for i in range(t):
            if atom[p] >> i & 1: w = P.add(w, qq(sel[i], p))
        linA[p] = w
    A = quad(P, c, linA, Q, Y, None)
    out = {}; nB = 0
    for a in range(g):
        S = [sel[i] for i in range(t) if a >> i & 1]; ca = None
        for p in S: ca = P.add(ca, lin[p])
        for p, q in combinations(S, 2): ca = P.add(ca, qq(p, q))
        coefs = []
        for p in Y:
            b = atom[p]
            if b == a: continue
            w = None
            for i in range(t):
                ai, bi = a >> i & 1, b >> i & 1
                if ai != bi: w = P.add(w, qq(sel[i], p) if ai else neg(qq(sel[i], p)))
            coefs.append((p, w))
        B = affine(P, ca, coefs); nB += len(B)
        am = sum(1 << p for p in S); keep = sum(1 << p for p in Y if atom[p] != a)
        for ym, wa in A.items(): out[am | ym] = P.add(wa, B[ym & keep])
    if stats is not None: stats.update(t=t, classes=len(A) + nB)
    return out
def build(k):
    pairs = list(combinations(range(k), 2)); D = 1 + k + len(pairs); P = Prog(D); st = {}
    out = quad(P, (0, 1), {p: (1 + p, 1) for p in range(k)}, {pq: (1 + k + i, 1) for i, pq in enumerate(pairs)}, list(range(k)), st)
    return P, out, pairs, st
def replay(P, out, k, pairs, c, lin, qd):
    w = [c] + [lin[p] for p in range(k)] + [qd[pq] for pq in pairs]
    for (i, si, j, sj) in P.gates: w.append(si * w[i] + sj * w[j])
    for x in range(1 << k):
        S = [i for i in range(k) if x >> i & 1]
        if out[x][1] * w[out[x][0]] != c + sum(lin[p] for p in S) + sum(qd[pq] for pq in combinations(S, 2)): return False
    return True
if __name__ == "__main__":
    kbuild, kexact, kcount = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    fill(max(kbuild, kcount))
    import random; rnd = random.Random(20261011)
    print("== my builder: k, N, t, helper classes read by the last layer, gates (G), gates/N, formula agrees, replay")
    for k in range(3, kbuild + 1):
        P, out, pairs, st = build(k); N = 1 << k; D = P.D; g = len(P.gates)
        assert all(i < D + n and j < D + n for n, (i, si, j, sj) in enumerate(P.gates))      # a gate reads only earlier wires
        ok = True
        if k <= kexact:
            how = "every unit input (%d), exact" % D
            for u in range(D):
                c = 1 if u == 0 else 0; lin = {p: 1 if u == 1 + p else 0 for p in range(k)}
                qd = {pq: 1 if u == 1 + k + i else 0 for i, pq in enumerate(pairs)}
                ok = ok and replay(P, out, k, pairs, c, lin, qd)
        else:
            how = "2 draws of whole numbers below 10^9"
            for _ in range(2):
                c = rnd.randrange(-10**9, 10**9); lin = {p: rnd.randrange(-10**9, 10**9) for p in range(k)}
                qd = {pq: rnd.randrange(-10**9, 10**9) for pq in pairs}
                ok = ok and replay(P, out, k, pairs, c, lin, qd)
        negout = sum(1 for x in range(N) if out[x][1] != 1); both = sum(1 for (i, si, j, sj) in P.gates if si == -1 and sj == -1)
        subs = sum(1 for (i, si, j, sj) in P.gates if si != sj); distinct = len(set(out[x][0] for x in range(N)))
        print("k=%2d N=%7d t=%d classes=%7d (%.4f N) gates=%8d = %.4f N [adds %d, subtractions %d, gates -u-v %d, outputs needing a sign flip %d, distinct output wires %d]  formula %s  replay %s [%s]" % (
            k, N, st['t'], st['classes'], st['classes'] / N, g, g / N, g - subs - both, subs, both, negout, distinct, "same" if g == BEST[k][0] else "DIFFERS (%d)" % BEST[k][0], "PASS" if ok else "FAIL", how), flush=True)
    print("== count-only formula (checked above against every built program): k, best t, (gates - N)/N, that times k/log2(k)")
    ks = [k for k in (8, 16, 20, 24, 32, 48, 64, 100, 128, 200, 256, 400, 512, 800, 1024, 1600, 2048, 3000, 4096, 6000, 8192, 12000, 16384, 32768, 65536) if k <= kcount]
    for k in ks:
        gts, t = BEST[k]; N = 1 << k; ex = Fraction(gts - N, N); f = float(ex)
        print("k=%6d t=%2d excess/N=%.6f  times k/log2 k = %.4f   2^-t = %.6f" % (k, t, f, f * k / math.log2(k), 2.0 ** -t), flush=True)
