#!/usr/bin/env python3
"""ladder.py -- ab-3 convolution-ladder.  Exact whole numbers / Fractions only.  Count (G): a gate is any a*u + b*v,
scalings free; a wire that is a scalar multiple of an existing wire is the same wire (no gate).
Parts: (1) identities; (2) circuits BUILT and REPLAYED exactly for families of weight-only convolutions; (3) the grid."""
import sys, itertools
from fractions import Fraction
from math import comb, gcd
from functools import reduce

def pop(x): return bin(x).count("1")

# ---------- exact matrices ----------
def conv_matrix(k, qw):            # qw[j] = value of q on weight j
    N = 1 << k
    return [[qw[pop(x ^ y)] for x in range(N)] for y in range(N)]
def kraw(k, j, w):                 # Krawtchouk: eigenvalue of "sum over distance exactly j" on Fourier weight w
    return sum((-1) ** i * comb(w, i) * comb(k - w, j - i) for i in range(j + 1))
def spectrum(k, qw): return [sum(qw[j] * kraw(k, j, w) for j in range(k + 1)) for w in range(k + 1)]
def q_from_spectrum(k, s):         # q(j) = (1/N) sum_w s(w) K_w(j)
    N = 1 << k
    return [Fraction(sum(s[w] * kraw(k, w, j) for w in range(k + 1)), N) for j in range(k + 1)]

# ---------- a straight-line program builder with exact replay ----------
class SLP:
    def __init__(self, N):
        self.N = N; self.vec = []; self.key = {}; self.gates = 0; self.prog = []
        for i in range(N):
            v = [0] * N; v[i] = 1; self._add(tuple(v))
    @staticmethod
    def norm(v):
        g = 0
        for a in v:
            a = Fraction(a)
        den = reduce(lambda a, b: a * b // gcd(a, b), [Fraction(a).denominator for a in v], 1)
        iv = [int(Fraction(a) * den) for a in v]
        g = reduce(gcd, [abs(a) for a in iv], 0)
        if g == 0: return None
        iv = [a // g for a in iv]
        for a in iv:
            if a != 0:
                if a < 0: iv = [-b for b in iv]
                break
        return tuple(iv)
    def _add(self, v):
        self.vec.append(v); self.key[v] = len(self.vec) - 1; return len(self.vec) - 1
    def gate(self, u, a, v, b):    # wire a*u + b*v ; returns wire id (existing one if proportional to an existing wire)
        w = self.norm([Fraction(a) * x + Fraction(b) * y for x, y in zip(self.vec[u], self.vec[v])])
        if w is None: raise ValueError("zero wire")
        if w in self.key: return self.key[w]
        self.gates += 1; self.prog.append((u, a, v, b)); return self._add(w)
    def gate2(self, u, a, v, b):
        raw = [Fraction(a) * x + Fraction(b) * y for x, y in zip(self.vec[u], self.vec[v])]
        w = self.gate(u, a, v, b)
        i = next(i for i, x in enumerate(raw) if x != 0)
        return w, raw[i] / self.vec[w][i]
    def check(self, outs, M):      # every row of M proportional to the wire named
        for o, row in zip(outs, M):
            if self.norm(row) != self.vec[o]: return False
        return True

# ---------- family 1: spectrum supported on Fourier weights <= d  (x-1's "lightest outputs", both ways) ----------
def analysis(S, wires, d):
    """all Fourier coefficients of degree <= d of the function held by `wires` (len 2^j). dict: frozenset(bits)->wire"""
    n = len(wires)
    if n == 1: return {frozenset(): wires[0]}
    if d == 0:
        acc = wires[:]
        while len(acc) > 1:
            acc = [S.gate(acc[i], 1, acc[i + 1], 1) for i in range(0, len(acc), 2)]
        return {frozenset(): acc[0]}
    h = n // 2; bit = n.bit_length() - 2
    s = [S.gate(wires[i], 1, wires[i + h], 1) for i in range(h)]
    res = dict(analysis(S, s, d))
    df = [S.gate(wires[i], 1, wires[i + h], -1) for i in range(h)]
    for m, w in analysis(S, df, d - 1).items(): res[m | {bit}] = w
    return res
def synthesis(S, coef, j, d, scale):
    """wires for g(y) = sum_m scale(m)*c_m*chi_m(y) over the j low bits; coef: frozenset->(wire, Fraction multiplier)"""
    if j == 0: return [coef[frozenset()]]
    if d == 0 or all(len(m) == 0 for m in coef): return [coef[frozenset()]] * (1 << j)
    bit = j - 1
    c0 = {m: w for m, w in coef.items() if bit not in m}
    c1 = {m - {bit}: w for m, w in coef.items() if bit in m}
    g0 = synthesis(S, c0, j - 1, d, scale); g1 = synthesis(S, c1, j - 1, d - 1, scale)
    out = [None] * (1 << j)
    for y in range(1 << (j - 1)):
        (u, a), (v, b) = g0[y], g1[y]
        out[y] = S.gate2(u, a, v, b); out[y | (1 << bit)] = S.gate2(u, a, v, -b)
    return out
def lowpass_circuit(k, d, sw=None, plus_identity=0):
    """convolution with spectrum sw[w] on weights w<=d, 0 above (default: 1), plus plus_identity * I"""
    N = 1 << k; S = SLP(N)
    co = analysis(S, list(range(N)), d)
    if sw is None: sw = [1] * (d + 1)
    coef = {m: (w, Fraction(sw[len(m)])) for m, w in co.items() if sw[len(m)] != 0}
    # the analysis wires are primitive whole-number vectors proportional to the characters; record the true multiplier
    for m in list(coef):
        w, mult = coef[m]; v = S.vec[w]
        chi0 = 1                                   # character value at address 0 is +1; v[0] is +1 after normalisation
        coef[m] = (w, mult * Fraction(1, v[0]))
    outs = synthesis(S, coef, k, d, None)
    g_an = S.gates
    ids = []
    for y in range(N):
        w, a = outs[y]
        if plus_identity: w = S.gate(w, a, y, Fraction(plus_identity) * N)
        ids.append(w)
    s_full = [(sw[w] if w <= d else 0) + plus_identity for w in range(k + 1)]
    M = conv_matrix(k, q_from_spectrum(k, s_full))
    return S.gates, S.check(ids, M)

# ---------- adding-only greedy (Paar) for 0/1 matrices, replayed ----------
def paar(M):
    N = len(M[0]); S = SLP(N)
    rows = [set(j for j in range(N) if r[j]) for r in M]
    while True:
        cnt = {}
        for r in rows:
            if len(r) < 2: continue
            lr = sorted(r)
            for a in range(len(lr)):
                for b in range(a + 1, len(lr)):
                    cnt[(lr[a], lr[b])] = cnt.get((lr[a], lr[b]), 0) + 1
        if not cnt: break
        (a, b), c = max(cnt.items(), key=lambda t: (t[1], -t[0][0], -t[0][1]))
        w = S.gate(a, 1, b, 1)
        for r in rows:
            if a in r and b in r: r.discard(a); r.discard(b); r.add(w)
    outs = [next(iter(r)) for r in rows]
    return S.gates, S.check(outs, M)

# ---------- neighbour sums by pairing bits (x-5's hand count), replayed ----------
def nbr_pairing(k):
    N = 1 << k; S = SLP(N); parts = []
    for i in range(0, k - 1, 2):
        parts.append([S.gate(y ^ (1 << i), 1, y ^ (1 << (i + 1)), 1) for y in range(N)])
    if k % 2: parts.append([y ^ (1 << (k - 1)) for y in range(N)])
    outs = parts[0]
    for p in parts[1:]: outs = [S.gate(u, 1, v, 1) for u, v in zip(outs, p)]
    return S.gates, S.check(outs, conv_matrix(k, [1 if j == 1 else 0 for j in range(k + 1)]))

if __name__ == "__main__":
    part = sys.argv[1]
    if part == "ident":
        print("== identities (whole numbers) ==")
        for k in range(2, 9):
            N = 1 << k
            qH = [1 - 2 * (comb(j, 2) & 1) for j in range(k + 1)]
            sH = spectrum(k, qH)
            print(f"k={k}: H's own q by weight {qH}; spectrum by weight {sH}")
        # (a) for even k: C_q = diag(q) H Pi diag(q)  (hyb.py checked it); spectrum = 2^(k/2) * (+-1 by weight mod 4)
        for k in (2, 4, 6, 8):
            qH = [1 - 2 * (comb(j, 2) & 1) for j in range(k + 1)]; sH = spectrum(k, qH); r = 1 << (k // 2)
            neg = sorted(set(w % 4 for w in range(k + 1) if sH[w] == -r)); pos = sorted(set(w % 4 for w in range(k + 1) if sH[w] == r))
            print(f"k={k}: spectrum/2^(k/2) = -1 exactly on weights congruent to {neg} mod 4, +1 on {pos}; two-valued: {set(abs(v) for v in sH)=={r}}")
        # (b) twist and reversal are free: spectrum (-1)^w s(w)  <->  q(k-j) (antipodal relabelling);  s(k-w) <-> (-1)^j q(j)
        for k in (3, 4, 5):
            import random
            random.seed(k); q = [random.randint(-3, 3) for _ in range(k + 1)]
            s = spectrum(k, q)
            s_rev = spectrum(k, q[::-1]); s_tw = spectrum(k, [(-1) ** j * q[j] for j in range(k + 1)])
            print(f"k={k}: q reversed -> spectrum (-1)^w s(w): {s_rev == [(-1)**w * s[w] for w in range(k+1)]};"
                  f"  q times (-1)^j -> spectrum s(k-w): {s_tw == s[::-1]}")
        # (c) tensor power t^weight is the class member with s = t^-2, up to free diagonal scalings
        for k in (2, 3, 4):
            for t in (2, 3, Fraction(1, 2), -3):
                N = 1 << k; t = Fraction(t)
                A = conv_matrix(k, [t ** j for j in range(k + 1)])
                ok = all(A[y][x] == t ** pop(x) * t ** pop(y) * (1 / t ** 2) ** pop(x & y) for x in range(N) for y in range(N))
                print(f"k={k} t={t}: t^distance == t^|x| t^|y| (t^-2)^|x&y| : {ok};  spectrum by weight {spectrum(k, [t**j for j in range(k+1)])}")
        # (d) weights mod 2 filter is the antipodal pairing; weights mod 4 filter is H
        for k in (2, 3, 4, 5, 6):
            s = [1 if w % 2 == 0 else 0 for w in range(k + 1)]
            print(f"k={k}: spectrum [w even] has q by weight {q_from_spectrum(k, s)}")
        for k in (4, 6, 8):
            for R in ((0, 1), (0,), (1,), (2,), (3,)):
                s = [1 if w % 4 in R else 0 for w in range(k + 1)]
                print(f"k={k}: spectrum [w mod 4 in {R}] has q by weight {[str(v) for v in q_from_spectrum(k, s)]}")
        for k in (3, 6, 9):
            s = [1 if w % 3 == 0 else 0 for w in range(k + 1)]
            print(f"k={k}: spectrum [w mod 3 == 0] has N*q by weight {[str(v*(1<<k)) for v in q_from_spectrum(k, s)]}")
    if part == "lowpass":
        print("== family: spectrum 1 on weights <= d, 0 above (lightest outputs there and back); circuits built and replayed ==")
        K = int(sys.argv[2])
        print("gates (G); 'per point' = gates / N")
        for k in range(2, K + 1):
            line = []
            for d in range(0, k + 1):
                g, ok = lowpass_circuit(k, d)
                line.append(f"d={d}:{g}({g/(1<<k):.2f}){'ok' if ok else 'BAD'}")
            print(f"k={k} N={1<<k}: " + "  ".join(line), flush=True)
    if part == "grid":
        K = [int(a) for a in sys.argv[2:]]
        TG = {2: 7, 3: 19, 4: 52, 5: 128, 6: 304}
        for k in K:
            N = 1 << k
            print(f"== grid at k={k}, N={N} points.  best known transform (G) [read]: {TG.get(k)} gates; route 'via transform' = 2T+N = {2*TG[k]+N} ==")
            for j in range(0, k + 1):
                q = [1 if i == j else 0 for i in range(k + 1)]
                g, ok = paar(conv_matrix(k, q))
                print(f"  sphere j={j}: spectrum {spectrum(k, q)}  adding-only greedy {g} gates ({g/N:.3f}/pt) replay {'ok' if ok else 'BAD'}", flush=True)
            for j in range(0, k + 1):
                q = [1 if i <= j else 0 for i in range(k + 1)]
                g, ok = paar(conv_matrix(k, q))
                print(f"  ball  j={j}: spectrum {spectrum(k, q)}  adding-only greedy {g} gates ({g/N:.3f}/pt) replay {'ok' if ok else 'BAD'}", flush=True)
            g, ok = nbr_pairing(k)
            print(f"  neighbour sums by pairing: {g} gates ({g/N:.3f}/pt) replay {'ok' if ok else 'BAD'}; formula (3/4)k-1 = {0.75*k-1:.3f} (even k)")
            for d in range(0, k + 1):
                g, ok = lowpass_circuit(k, d)
                s = [1 if w <= d else 0 for w in range(k + 1)]
                print(f"  low-pass d={d}: N*q by weight {[str(v*N) for v in q_from_spectrum(k, s)]}  built {g} gates ({g/N:.3f}/pt) replay {'ok' if ok else 'BAD'}", flush=True)
