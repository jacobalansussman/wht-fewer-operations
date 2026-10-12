#!/usr/bin/env python3
"""recount.py -- a second reader of the circuit text files, written separately.
Does not import slp.py, gen.py, fam.py or gen_rtl.py.
For each file: number of adders (lines with two terms), depth in adder levels,
adder bits = sum over adders of the exact signed width of the result when the
inputs are signed W-bit numbers (range -2^(W-1) .. 2^(W-1)-1), found from the
coefficient vector of every value.  Also checks every output yJ against row J
of the Walsh-Hadamard matrix (dense, exact integers) and counts subtractions.
"""
import re, sys, json

def parse_term(s):
    s = s.strip()
    sign = 1
    if s.startswith('-'):
        sign = -1; s = s[1:].strip()
    if '*' in s:
        c, n = s.split('*'); c = int(c.strip()); n = n.strip()
    else:
        c, n = 1, s
    return sign * c, n

def read(path):
    lines = []
    for raw in open(path):
        t = raw.split('#')[0].strip()
        if not t: continue
        name, rhs = t.split('=')
        name = name.strip(); rhs = rhs.strip()
        # split on top-level + or - that is not the leading sign
        m = re.match(r'^(-?\s*[^+-]+?)\s*([+-])\s*(.+)$', rhs)
        if m:
            a = parse_term(m.group(1)); b = parse_term(m.group(3))
            if m.group(2) == '-': b = (-b[0], b[1])
            lines.append((name, [a, b]))
        else:
            lines.append((name, [parse_term(rhs)]))
    return lines

def width(vec, W):
    lo, hi = -(1 << (W-1)), (1 << (W-1)) - 1
    pos = sum(c for c in vec if c > 0); neg = sum(c for c in vec if c < 0)
    mx = pos*hi + neg*lo; mn = pos*lo + neg*hi
    b = 1
    while not (-(1 << (b-1)) <= mn and mx <= (1 << (b-1)) - 1): b += 1
    return b

def analyse(path, widths=(9, 12)):
    lines = read(path)
    N = 1 + max(int(n[1:]) for _, ts in lines for _, n in ts if re.fullmatch(r'x\d+', n))
    vec = {}; lev = {}
    for i in range(N):
        v = [0] * N; v[i] = 1
        vec['x%d' % i] = v; lev['x%d' % i] = 0
    adders = 0; subs = 0; negsum = 0; nonpow2 = 0; depth = 0
    bits = {W: 0 for W in widths}
    for name, ts in lines:
        assert name not in vec, name
        v = [0] * N
        for c, n in ts:
            u = vec[n]
            v = [a + c * b for a, b in zip(v, u)]
        vec[name] = v
        for c, _ in ts:
            if abs(c) not in (1, 2, 4, 8): nonpow2 += 1
        if len(ts) == 2:
            adders += 1
            lev[name] = 1 + max(lev[n] for _, n in ts)
            depth = max(depth, lev[name])
            s = [c < 0 for c, _ in ts]
            if all(s): negsum += 1
            elif any(s): subs += 1
            for W in widths: bits[W] += width(v, W)
        else:
            lev[name] = lev[ts[0][1]]
    # outputs
    k = N.bit_length() - 1
    ok = True
    for J in range(N):
        row = [(-1) ** bin(J & i).count('1') for i in range(N)]
        if 'y%d' % J not in vec or vec['y%d' % J] != row: ok = False
    outw = {W: max(width(vec['y%d' % J], W) for J in range(N)) for W in widths}
    return dict(N=N, adders=adders, depth=depth, bits=bits, subs=subs, negsum=negsum,
                nonpow2=nonpow2, outputs_ok=ok, outw=outw)

if __name__ == '__main__':
    base = sys.argv[1]
    out = {}
    for N in (16, 32, 64, 128, 256):
        for d in ('textbook', 'cfl1994', 'family'):
            r = analyse('%s/%d_%s.txt' % (base, N, d))
            out['%d_%s' % (N, d)] = r
            print('%4d %-9s adders %5d depth %3d bits(W=9) %6d bits(W=12) %6d subtractions %5d (%.1f%%) negsum %d nonpow2 %d out width %d/%d outputs_ok %s'
                  % (N, d, r['adders'], r['depth'], r['bits'][9], r['bits'][12], r['subs'],
                     100.0*r['subs']/r['adders'], r['negsum'], r['nonpow2'], r['outw'][9], r['outw'][12], r['outputs_ok']))
    json.dump(out, open('recount.json', 'w'), indent=1, default=int)
