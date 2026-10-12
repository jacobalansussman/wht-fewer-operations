#!/usr/bin/env python3
"""af-0/trace.py  Replay of ad-6's circuit (circuit2.eval2, THEIR builder, untouched) from the coefficients, with MY tracer.
Every input I hand to their builder is an object W carrying the exact linear form of that wire in the
D = 1 + k + k(k-1)/2 coefficients.  The only inputs are the D unit forms (one per coefficient).  Their builder can only
combine objects through W.__add__ (one gate, count (G)), W.__neg__ and W.__rmul__ by +-1 (a scaling, free in (G));
adding a plain number to a wire raises.  So every wire is built from the coefficients alone, the gate count is mine,
and 'output x == the form [1, x, x(x)x]' is a proof for every input, not a test on samples.
How a form is stored (no numpy on this machine): one whole number, sum_j coef_j * BASE^j, BASE = 2^SH.  Each wire also
carries 'bound' = the number of leaves of its formula, so |coef_j| <= bound; every gate asserts bound < BASE/4.  Two
whole numbers whose digits are all below BASE/2 in size are equal only if all digits are equal, so the comparison with
the expected form is exact.
usage: trace.py kmin kmax [SH]"""
import sys, time
from itertools import combinations
sys.path.insert(0, 'waves/wave-09/ad-6-twohelpers')
import circuit2
ST = {}; SH = 16
class W:
    __slots__ = ('v', 'b', 'kind')
    def __init__(s, v, b, kind): s.v = v; s.b = b; s.kind = kind
    def __add__(s, o):
        if not isinstance(o, W): raise TypeError("a wire was added to something that is not a wire")
        b = s.b + o.b
        if b >= ST['lim']: raise OverflowError("bound")
        if b > ST['maxb']: ST['maxb'] = b
        ST['gates'] += 1
        if o.kind == 'neg' or s.kind == 'neg': ST['minus'] += 1
        return W(s.v + o.v, b, 'gate')
    def __neg__(s): ST['negs'] += 1; return W(-s.v, s.b, 'neg')
    def __rmul__(s, c):
        if c == 1: return s
        if c == -1: return W(-s.v, s.b, 'neg')
        raise TypeError
def trace(k):
    pairs = list(combinations(range(k), 2)); D = 1 + k + len(pairs); N = 1 << k
    idx = {pq: 1 + k + i for i, pq in enumerate(pairs)}
    unit = lambda j: W(1 << (SH * j), 1, 'input')
    ST.update(gates=0, minus=0, negs=0, maxb=0, lim=(1 << SH) // 4)
    c = unit(0); lin = {p: unit(1 + p) for p in range(k)}; quad = {pq: unit(idx[pq]) for pq in pairs}
    circuit2.G = 0
    out = circuit2.eval2(c, lin, quad, list(range(k)))
    theirs = circuit2.G
    assert len(out) == N and set(out) == set(range(N))
    exp = [0] * N; exp[0] = 1; bad = 0; ungated = 0
    for x in range(1, N):
        h = x.bit_length() - 1; r = x ^ (1 << h); e = exp[r] + (1 << (SH * (1 + h)))
        p = 0
        while r:
            if r & 1: e += 1 << (SH * idx[(p, h)])
            r >>= 1; p += 1
        exp[x] = e
    for x in range(N):
        w = out[x]
        if not isinstance(w, W) or w.v != exp[x]: bad += 1
        elif w.kind != 'gate': ungated += 1
    return D, N, ST['gates'], theirs, ST['minus'], ST['negs'], ST['maxb'], bad, ungated
if __name__ == "__main__":
    kmin, kmax = int(sys.argv[1]), int(sys.argv[2])
    if len(sys.argv) > 3: SH = int(sys.argv[3])
    print("k | N | inputs D | gates (G) counted by my tracer | their counter | gates/N | gates that subtract | free negations | largest leaf count of a wire (limit %d) | outputs whose form is wrong | outputs that are no gate" % ((1 << SH) // 4))
    for k in range(kmin, kmax + 1):
        t0 = time.time(); D, N, g, th, gm, ng, mx, bad, ung = trace(k)
        print("k=%2d N=%7d D=%3d gates=%8d theirs=%8d %s gates/N=%.4f minus=%d negs=%d maxleaves=%d wrong=%d ungated=%d  %s  (%.1fs)" % (
            k, N, D, g, th, "same" if g == th else "DIFFER", g / N, gm, ng, mx, bad, ung, "EXACT PASS" if bad == 0 else "FAIL", time.time() - t0), flush=True)
