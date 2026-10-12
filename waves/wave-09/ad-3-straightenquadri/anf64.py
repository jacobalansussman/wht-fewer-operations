#!/usr/bin/env python3
"""anf64.py [ad-3]  Print the polynomial (modulo 2, in the bits y0..y5) of each set along the 5-exchange path of k6_S60.out,
and the flats used, as lists of affine conditions.  Exact."""
def anf(m):
    a = [(m >> y) & 1 for y in range(64)]
    for b in range(6):
        for y in range(64):
            if y >> b & 1: a[y] ^= a[y ^ (1 << b)]
    terms = ["".join("y%d" % i for i in range(6) if y >> i & 1) or "1" for y in range(64) if a[y]]
    return " + ".join(sorted(terms, key=lambda t: (len(t), t)))
def flat_desc(m):
    pts = [y for y in range(64) if m >> y & 1]
    conds = []
    for a in range(1, 64):
        vals = set(bin(a & y).count("1") & 1 for y in pts)
        if len(vals) == 1: conds.append(("+".join("y%d" % i for i in range(6) if a >> i & 1), vals.pop()))
    # keep an independent subset
    basis = []; out = []
    for (s, v), a in zip(conds, [a for a in range(1, 64) if len(set(bin(a & y).count("1") & 1 for y in pts)) == 1]):
        x = a
        for b in basis: x = min(x, x ^ b)
        if x: basis.append(x); out.append("%s=%d" % (s, v))
    return ", ".join(out)
path = [(None, None, 0x5555555555555500), (1, 0x0303030303030303, 0x5656565656565600), (9, 0xc0c030300c0c0303, 0x969666665a5a5401),
        (2, 0x0055005500000000, 0x96c366335a5a5401), (4, 0x0000000000550000, 0x96c366335a0f5401), (8, 0x0000000000000101, 0x96c366335a0f5500)]
for u, T, g in path:
    if u is not None: print("exchange u=%d on the flat {%s}  (%d points)" % (u, flat_desc(T), bin(T).count("1")))
    print("   pattern: %s" % anf(g))
