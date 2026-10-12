#!/usr/bin/env python3
# j-cross / meters.py : three meters from other reports, read on e2-0's programs (independent parser, exact Fractions).
#  (1) e2-3: clean / cancelling gates and cancellation depth D; compare saving with (N/4)*D.
#  (2) a-2: s = non-zeros of a wire in the inputs, s' = non-zeros in the outputs; tight means s*s' = N; sum of log2(1+2P/N).
#  (3) j-cross lemma: over how many address bits is a wire entangled (flattening of rank 2 on that bit).
#  (4) count (O) files: replay, count operations by kind, check outputs = rows of H / d.
import sys, re, math
from fractions import Fraction as F
import os
D = os.environ.get('E20', 'waves/wave-02/e2-0-pieces/')
def wht(v):
    v = list(v); n = len(v); h = 1
    while h < n:
        for i in range(0, n, 2 * h):
            for j in range(i, i + h):
                a, b = v[j], v[j + h]; v[j], v[j + h] = a + b, a - b
        h *= 2
    return v
def entangled_bits(v, k):
    n = len(v); out = []
    for b in range(k):
        lo = [v[i] for i in range(n) if not (i >> b) & 1]; hi = [v[i | (1 << b)] for i in range(n) if not (i >> b) & 1]
        # rank of the 2 x n/2 matrix [lo; hi]
        r2 = False
        piv = next((j for j in range(len(lo)) if lo[j] != 0 or hi[j] != 0), None)
        for j in range(len(lo)):
            if lo[piv] * hi[j] - hi[piv] * lo[j] != 0: r2 = True; break
        if r2: out.append(b)
    return out
def gfile(N):
    k = N.bit_length() - 1
    val = {'x%d' % i: tuple(F(int(i == j)) for j in range(N)) for i in range(N)}
    cdep = {'x%d' % i: 0 for i in range(N)}
    gates = []; clean = canc = 0
    for line in open(D + 'slp_%d.txt' % N):
        line = line.split('#')[0].strip()
        if not line: continue
        m = re.fullmatch(r'(\w+) = (\S+) \* (\w+) \+ (\S+) \* (\w+)', line); assert m, line
        t, a, u, b, v = m.groups(); assert t not in val
        val[t] = tuple(F(a) * p + F(b) * q for p, q in zip(val[u], val[v]))
        ov = any(p != 0 and q != 0 for p, q in zip(val[u], val[v]))
        if ov: canc += 1
        else: clean += 1
        cdep[t] = max(cdep[u], cdep[v]) + (1 if ov else 0)
        gates.append((t, u, v, F(a), F(b)))
    rows = {tuple(F((-1) ** bin(w & x).count('1')) for x in range(N)): w for w in range(N)}
    outs = [t for t in val if val[t] in rows]
    assert len({rows[val[t]] for t in outs}) == N, 'not all rows of H present'
    Dmax = max(cdep[t] for t in outs); Dmin = min(cdep[t] for t in outs)
    def P(t):
        s = sum(1 for z in val[t] if z != 0); s2 = sum(1 for z in wht(val[t]) if z != 0); return s * s2
    Pw = {t: P(t) for t in val}
    nont = [t for (t, _, _, _, _) in gates if Pw[t] != N]
    slack = sum(math.log2(1 + 2 * max(Pw[t], Pw[u], Pw[v]) / N) for (t, u, v, _, _) in gates)
    ent = {t: entangled_bits(val[t], k) for (t, _, _, _, _) in gates}
    hist = {}
    for t in ent: hist[len(ent[t])] = hist.get(len(ent[t]), 0) + 1
    coefs = sorted({abs(c) for g in gates for c in g[3:]})
    sav = N * k - len(gates)
    print('G N=%d gates=%d clean=%d cancelling=%d | outputs at cancellation depth %d..%d | saving=%d, (N/4)*Dmax=%d, (N/4)*(k-1)=%d'
          % (N, len(gates), clean, canc, Dmin, Dmax, sav, N // 4 * Dmax, N // 4 * (k - 1)))
    print('   wires not tight: %d of %d; values of s*s\'/N among them: %s' % (len(nont), len(gates), sorted({Pw[t] // N if Pw[t] % N == 0 else F(Pw[t], N) for t in nont})))
    print('   a-2 slack sum = %.2f against N log2 N = %d' % (slack, N * k))
    print('   wires by number of entangled address bits:', dict(sorted(hist.items())), '| |coefficients| used:', [str(c) for c in coefs])
    if N <= 16:
        for t in ent:
            if len(ent[t]) >= 2: print('     ', t, 'entangled on bits', ent[t], 's*s\'/N =', F(Pw[t], N))
def ofile(N):
    val = {'x%d' % i: tuple(F(int(i == j)) for j in range(N)) for i in range(N)}
    n = {'+': 0, '-': 0, '*': 0}; consts = {}
    for line in open(D + 'oslp_%d.txt' % N):
        line = line.split('#')[0].strip()
        if not line: continue
        m = re.fullmatch(r'(\w+) = (\S+) ([+\-*]) (\S+)', line); assert m, line
        t, a, op, b = m.groups(); assert t not in val
        if op == '*': val[t] = tuple(F(a) * z for z in val[b]); consts[a] = consts.get(a, 0) + 1
        elif op == '+': val[t] = tuple(p + q for p, q in zip(val[a], val[b]))
        else: val[t] = tuple(p - q for p, q in zip(val[a], val[b]))
        n[op] += 1
    k = N.bit_length() - 1; sc = F(1, 2 ** (k // 2))
    want = {tuple(sc * (-1) ** bin(w & x).count('1') for x in range(N)) for w in range(N)}
    got = {val[t] for t in val if t[0] == 'y'}
    ok = (got == want) and sum(1 for t in val if t[0] == 'y') == N
    tot = sum(n.values())
    print('O N=%d operations=%d %s constants=%s | outputs are exactly the rows of H/%d: %s | textbook for H: %d | bits per operation N log2 N / ops = %.4f'
          % (N, tot, n, consts, 2 ** (k // 2), ok, N * k, N * k / tot))
for N in (4, 8, 16, 32, 64): gfile(N)
for N in (4, 16, 64): ofile(N)
