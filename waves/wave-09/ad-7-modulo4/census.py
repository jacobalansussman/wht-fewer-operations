#!/usr/bin/env python3
"""census.py [ad-7]  The night's best exact circuits for the transform, read as 2-adic objects.  Count (G).
For each circuit (e2-0-pieces/slp_N.txt, 7 / 20 / 52 / 128 / 304 gates at 4 to 64 points; g-1's 19 gates at 8 points):
 1. replay over the whole numbers; check the outputs are the N rows of H up to sign;
 2. are all wires primitive (entries with no common factor 2) and all coefficients whole numbers (no division by 2)?
    classify each gate a*u + b*v by the powers of 2 in (a, b);
 3. reduce the circuit modulo 2^j: a gate whose value equals an earlier wire up to an odd factor is dropped, then gates no
    output depends on are dropped.  What is left is a circuit for H modulo 2^j: an UPPER bound on the least count modulo 2^j
    (outputs up to odd factors).  This shows in which binary digit the gates of the circuit do their work."""
import re, sys
from fractions import Fraction
from collections import Counter
D = "waves/wave-09/"
def v2(c):
    c = Fraction(c)
    if c == 0: return 99
    n, d, v = c.numerator, c.denominator, 0
    while n % 2 == 0: n //= 2; v += 1
    while d % 2 == 0: d //= 2; v -= 1
    return v
def parse(path):
    gates = []
    for line in open(path):
        line = line.split('#')[0].strip()
        if '=' not in line: continue
        name, rhs = [s.strip() for s in line.split('=')]
        rhs = rhs.replace(' ', '')
        terms = re.findall(r'([+-]?)(?:(\d+(?:/\d+)?)\*)?([A-Za-z_]\w*)', rhs)
        assert len(terms) == 2, (line, terms)
        tt = []
        for sg, co, nm in terms:
            c = Fraction(co) if co else Fraction(1)
            if sg == '-': c = -c
            tt.append((c, nm))
        gates.append((name, tt[0][0], tt[0][1], tt[1][0], tt[1][1]))
    return gates
def parse_slp(path):
    gates = []
    for line in open(path):
        line = line.split('#')[0].strip()
        m = re.match(r'(\w+) = (-?[\d/]+) \* (\w+) \+ (-?[\d/]+) \* (\w+)', line)
        if m: gates.append((m.group(1), Fraction(m.group(2)), m.group(3), Fraction(m.group(4)), m.group(5)))
    return gates
def canon_mod(vec, M):
    best = None
    for u in range(1, M, 2):
        t = tuple((u * c) % M for c in vec)
        if best is None or t < best: best = t
    return best
def census(label, gates, N):
    k = N.bit_length() - 1
    val = {'x%d' % i: [int(i == j) for j in range(N)] for i in range(N)}
    kinds = Counter(); nonprim = 0; nonint = 0
    for name, a, u, b, v in gates:
        w = [a * p + b * q for p, q in zip(val[u], val[v])]
        val[name] = w
        if any(Fraction(c).denominator != 1 for c in w) or all(Fraction(c).numerator % 2 == 0 for c in w): nonprim += 1
        if v2(a) < 0 or v2(b) < 0: nonint += 1
        kinds[tuple(sorted((min(v2(a), 9), min(v2(b), 9))))] += 1
    H = {tuple((-1) ** bin(x & y).count('1') for x in range(N)) for y in range(N)}
    outs = [n for n in val if tuple(val[n]) in H or tuple(-c for c in val[n]) in H]
    rows = {tuple(val[n]) if tuple(val[n]) in H else tuple(-c for c in val[n]) for n in outs}
    print("%s : N=%d, %d gates ; outputs found (rows of H up to sign): %d of %d ; wires not primitive: %d ; gates with a division by 2: %d" % (label, N, len(gates), len(rows), N, nonprim, nonint))
    print("     gates by the powers of 2 in their two coefficients (0 = odd): " + ", ".join("(2^%d, 2^%d) x%d" % (p, q, c) for (p, q), c in sorted(kinds.items())))
    res = []
    for j in range(1, k + 3):
        M = 2 ** j
        rep = {}            # canonical value -> representative name
        alias = {}          # name -> representative name
        par = {}
        vm = {}
        for i in range(N):
            nm = 'x%d' % i; vm[nm] = tuple(val[nm]); rep[canon_mod(vm[nm], M)] = nm; alias[nm] = nm
        for name, a, u, b, v in gates:
            am = int(a) % M; bm = int(b) % M           # coefficients are whole numbers in all files (checked above)
            w = tuple((am * p + bm * q) % M for p, q in zip(vm[alias[u]], vm[alias[v]]))
            # value taken from the true wire, so that the reduction is the reduction of the exact circuit
            w = tuple(int(c) % M for c in val[name])
            cw = canon_mod(w, M)
            if cw in rep: alias[name] = rep[cw]
            else: rep[cw] = name; alias[name] = name; vm[name] = w; par[name] = (u, v)
        live = set(); stack = [alias[n] for n in outs]
        while stack:
            n = stack.pop()
            if n in live or n.startswith('x'): continue
            live.add(n); u, v = par[n]; stack += [alias[u], alias[v]]
        res.append(len(live))
    print("     gates left modulo 2, 4, 8, ... : " + " ".join(map(str, res)))
    return res
if __name__ == "__main__":
    for N in (4, 8, 16, 32, 64):
        census("e2-0 family", parse_slp(D + "e2-0-pieces/slp_%d.txt" % N), N)
    census("g-1 19 gates", parse(D + "g-1-tightwires/h8_19gates.txt"), 8)
    print("for comparison, x-1's route [read]: modulo 4: 7, 18, 41, 88, 183 at 4 to 64 points; modulo 8: 23, 57, 130, 282 at 8 to 64; modulo 16: 63, 152, 346 at 16 to 64")
