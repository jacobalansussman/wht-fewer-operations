#!/usr/bin/env python3
"""n-0 build.py: my own builder of the 'windows of 3' programs, written from g-1's listing of the 8-point unit
(g-1.md section 0), not from orec.py.  Differences from h-3's builder on purpose: leftover address bits are done
FIRST (textbook butterflies on the low bits), windows of three on the higher bits, wire names differ.

usage: build.py <k> <outfile> [exact]      (N = 2^k; 'exact' adds the N final multiplications by 2^m)
       build.py random <k>                 (no file: build in memory, run on one random integer vector in exact
                                            integers scaled by 2^m, compare ALL outputs with a plain butterfly
                                            transform and 200 random outputs with the defining sum)
"""
import sys, random
from fractions import Fraction

def unit(x, tag):
    """8 wire names -> (lines, 8 output names), outputs = H_8 x / 2 in Sylvester order.  20 operations."""
    g = lambda n: f"{tag}{n}"
    L = [
        (g("g1"), "+", x[0], x[7]), (g("g2"), "+", x[1], x[6]), (g("g3"), "-", x[2], x[5]), (g("g4"), "-", x[3], x[4]),
        (g("g5"), "-", g("g1"), g("g2")), (g("g6"), "+", g("g3"), g("g4")),
        (g("g7"), "-", g("g5"), g("g6")),
        (g("h"), "*", "1/2", g("g7")),
        (g("a8"), "-", g("h"), x[7]), (g("a9"), "-", g("h"), x[5]),
        (g("a10"), "+", g("a8"), x[6]), (g("a11"), "-", g("a9"), x[4]),
        (g("y7"), "+", g("a10"), g("g4")), (g("y1"), "+", g("a10"), g("g3")),
        (g("y6"), "+", g("a11"), g("g2")), (g("y0"), "-", g("g1"), g("a11")),
        (g("y2"), "+", g("a8"), x[1]), (g("y3"), "+", g("a9"), x[3]),
        (g("y4"), "+", g("y2"), g("g6")), (g("y5"), "-", g("g5"), g("y3")),
    ]
    return L, [g(f"y{j}") for j in range(8)]

def build(k, exact):
    N = 1 << k
    r, m = k % 3, k // 3
    cur = [f"x{i}" for i in range(N)]
    L = []
    for b in range(r):                                   # leftover bits first: textbook butterflies
        nxt = list(cur)
        for i in range(N):
            if not (i >> b) & 1:
                j = i | (1 << b)
                L.append((f"b{b}_{i}", "+", cur[i], cur[j])); nxt[i] = f"b{b}_{i}"
                L.append((f"b{b}_{j}", "-", cur[i], cur[j])); nxt[j] = f"b{b}_{j}"
        cur = nxt
    for w in range(m):                                   # windows of three on bits r+3w .. r+3w+2
        s = r + 3 * w
        nxt = list(cur)
        for base in range(N):
            if (base >> s) & 7:
                continue
            pos = [base | (t << s) for t in range(8)]
            lines, out = unit([cur[p] for p in pos], f"w{w}_{base}_")
            L += lines
            for t in range(8):
                nxt[pos[t]] = out[t]
        cur = nxt
    if exact and m:
        L += [(f"z{i}", "*", str(1 << m), cur[i]) for i in range(N)]
        cur = [f"z{i}" for i in range(N)]
    return L, cur, m

if __name__ != "__main__":
    pass
elif sys.argv[1] == "random":
    k = int(sys.argv[2]); N = 1 << k
    L, outs, m = build(k, True)
    rng = random.Random(1011 + k)
    x = [rng.randint(-10**6, 10**6) for _ in range(N)]
    val = {f"x{i}": x[i] << m for i in range(N)}          # scaled by 2^m so that every halving must be exact
    kinds = {"+": 0, "-": 0, "*": 0}
    for name, op, a, b in L:
        kinds[op] += 1
        if op == "+": val[name] = val[a] + val[b]
        elif op == "-": val[name] = val[a] - val[b]
        else:
            c = Fraction(a); t = val[b] * c.numerator
            assert t % c.denominator == 0, "halving not exact"
            val[name] = t // c.denominator
    y = list(x)                                           # plain butterflies, my own loop
    h = 1
    while h < N:
        for i in range(0, N, 2 * h):
            for j in range(i, i + h):
                y[j], y[j + h] = y[j] + y[j + h], y[j] - y[j + h]
        h *= 2
    ok_all = all(val[outs[j]] == y[j] << m for j in range(N))
    ok_def = True
    for j in rng.sample(range(N), min(N, 200)):
        s = 0
        for i in range(N):
            s += -x[i] if bin(i & j).count("1") & 1 else x[i]
        ok_def &= (val[outs[j]] == s << m)
    print(f"k={k} N={N} operations={len(L)} (+ {kinds['+']}, - {kinds['-']}, * {kinds['*']}) textbook={N*k} "
          f"formula N(2.5*floor(k/3) + k mod 3) + N = {N*(5*(k//3))//2 + N*(k%3) + N} "
          f"ratio to N log2 N = {len(L)/(N*k):.4f}; one random vector: all outputs equal butterflies: {ok_all}; "
          f"200 outputs equal the defining sum: {ok_def}", flush=True)
else:
    k = int(sys.argv[1]); exact = len(sys.argv) > 3
    L, outs, m = build(k, exact)
    with open(sys.argv[2], "w") as f:
        f.write(f"# n-0 build.py, k={k}, {'exact H x' if exact else 'H x / 2^%d' % m}, {len(L)} operations\n")
        for name, op, a, b in L:
            f.write(f"{name} = {a} {op} {b}\n")
        f.write("# OUT " + " ".join(outs) + "\n")
    print(f"wrote {sys.argv[2]}: {len(L)} operations")
