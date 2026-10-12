#!/usr/bin/env python3
# e-0-ring / unit16.py : N = 16.  On the 8-dimensional mixed piece (the 15th roots of unity) write the trace-one mask as
#     mask = (rational) * (+- t^s) * f1 * f2 * product over a of (1 - t^a)^(e_a),
# f1, f2 three-term letters that carry the prime above 2, e_a in -2..2 (a denominator is an inverse of a two-term element).
# Search with floating logarithms, then every hit is VERIFIED EXACTLY in Z[x]/Phi_15 (integer polynomial arithmetic).
import cmath, math, itertools
from fractions import Fraction as F
n = 15
PHI = [1, -1, 0, 1, -1, 1, 0, -1, 1]             # Phi_15, low..high
def red(v):
    v = list(v) + [0] * 40
    for i in range(len(v) - 1, 7, -1):
        c = v[i]
        if c:
            for j in range(9): v[i - 8 + j] -= c * PHI[j]
    return v[:8]
def pmul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b): out[i + j] += x * y
    return red(out)
def elt(d):
    v = [0] * 15
    for e, c in d.items(): v[e % 15] += c
    return red(v)
def ppow(a, e):
    r = elt({0: 1})
    for _ in range(e): r = pmul(r, a)
    return r
# field with 16 elements, x^4 + x + 1
pw = [1]
for _ in range(14):
    v = pw[-1] << 1
    if v >> 4: v ^= 0b10011
    pw.append(v)
def tr(v):
    s = 0; w = v
    for _ in range(4):
        s ^= w; r = 0
        for b in range(4):
            if w >> b & 1: r ^= pw[(2 * b) % 15]
        w = r
    return s
mask = {m: 1 for m in range(15) if tr(pw[m])}
print("trace-one mask at 16 points:", sorted(mask))
z = cmath.exp(2j * math.pi / 15)
def ev(d, j): return sum(c * z ** ((j * e) % 15) for e, c in d.items())
J = [1, 2, 4, 7]                                  # the primitive j up to complex conjugation
def lv(d): return [math.log(abs(ev(d, j))) for j in J]
def centre(v):
    m = sum(v) / len(v); return [x - m for x in v]
two = {a: centre(lv({0: 1, a: -1})) for a in range(1, 8)}
table = {}
for es in itertools.product(range(-2, 3), repeat=7):
    v = [sum(e * two[a][i] for a, e in zip(range(1, 8), es)) for i in range(4)]
    key = tuple(round(x, 6) for x in v)
    cost = sum(abs(e) for e in es)
    if key not in table or cost < table[key][0]: table[key] = (cost, es)
three = []
for (a, b) in ((1, 4), (2, 8)):
    for s1 in (1, -1):
        for s2 in (1, -1): three.append({0: 1, a: s1, b: s2})
tm = centre(lv(mask))
hits = []
for f1, f2 in itertools.combinations_with_replacement(three, 2):
    l1, l2 = lv(f1), lv(f2)
    want = centre([tm[i] - l1[i] - l2[i] for i in range(4)])
    for dx in itertools.product((-1e-6, 0, 1e-6), repeat=4):
        key = tuple(round(want[i] + dx[i], 6) for i in range(4))
        if key in table:
            hits.append((table[key][0], table[key][1], f1, f2)); break
hits.sort(key=lambda h: h[0])
print("%d of %d pairs (f1, f2) pass the absolute-value test with exponents in -2..2" % (len(hits), 36))
def show(d): return " ".join("%+d*t^%d" % (c, e) for e, c in sorted(d.items()))
good = 0
for cost, es, f1, f2 in hits:
    # exact check: mask * prod_{e<0} (1 - t^a)^(-e)  ==  c * (+- t^s) * f1 * f2 * prod_{e>0} (1 - t^a)^e   in Z[x]/Phi_15
    lhs = elt(mask); rhs = pmul(elt(f1), elt(f2))
    for a, e in zip(range(1, 8), es):
        u = elt({0: 1, a: -1})
        if e > 0: rhs = pmul(rhs, ppow(u, e))
        if e < 0: lhs = pmul(lhs, ppow(u, -e))
    found = None
    for s in range(15):
        r2 = pmul(rhs, elt({s: 1}))
        i0 = next(i for i in range(8) if r2[i])
        c = F(lhs[i0], r2[i0])
        if c != 0 and all(F(lhs[i]) == c * r2[i] for i in range(8)): found = (s, c); break
    if found:
        good += 1
        num = [(a, e) for a, e in zip(range(1, 8), es) if e > 0]; den = [(a, -e) for a, e in zip(range(1, 8), es) if e < 0]
        if good <= 12:
            print("EXACT on the mixed piece:  mask = (%s) * t^%d * (%s) * (%s) * prod(1 - t^a)^e,  numerators %s denominators %s   [%d two-term letters]"
                  % (found[1], found[0], show(f1), show(f2), num, den, cost))
print("exact identities found: %d (of %d candidates)" % (good, len(hits)))
