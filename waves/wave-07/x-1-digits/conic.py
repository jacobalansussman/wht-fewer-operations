# x-1-digits/conic.py   count (G): a gate is a*u + b*v with ANY rational a, b; scalings free.  Exact whole numbers.
# (1) A polynomial of degree 2, a + b t + c t^2, at the N points t = 0..N-1.  Finite differences: 2(N-1) gates.
#     Here: N + 1 gates.  Two helper wires h_s = b + s c (s = N-1 and s = N); then p(s - n) = p(n) + (s - 2n) * h_s :
#     ONE helper serves every pair of points symmetric about s/2, each time with a different coefficient.
# (2) Why the cube refuses: the same helper serves two outputs only if they are two of THREE evaluation points on one line,
#     and the cube has no three points on a line.  Checked: for k <= 5, over all pairs of cube points, the helper direction
#     ev_x - ev_x' (degree <= 2 monomials) is different for every pair (projectively).
from fractions import Fraction as F
from math import gcd
def line(N):
    gates = 0
    def gate(a, u, b, v):
        nonlocal gates; gates += 1; return tuple(a * p + b * q for p, q in zip(u, v))
    A, B, C = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    h = {s: gate(1, B, s, C) for s in (N - 1, N)}
    val = {0: A}; n = 0; s = N - 1; maxc = 0
    while len(val) < N:
        m = s - n
        if 0 <= m < N and m not in val:
            val[m] = gate(1, val[n], s - 2 * n, h[s]); maxc = max(maxc, abs(s - 2 * n))
        n = m; s = (2 * N - 1) - s
    ok = all(val[t] == (1, t, t * t) for t in range(N))
    return gates, ok, maxc
print("(1) degree 2 on N points in a row")
for N in (4, 8, 16, 64, 256, 1024, 4096):
    g, ok, mc = line(N); print(f"  N={N:5d}: {g:5d} gates (G) ; all N values exact: {ok} ; finite differences {2 * (N - 1)} ; largest coefficient used {mc}")
print("(2) the cube: helper directions of all pairs")
pc = lambda v: bin(v).count("1")
for k in (2, 3, 4, 5):
    N = 1 << k; mon = [U for U in range(N) if pc(U) <= 2]
    ev = [tuple(int(U & x == U) for U in mon) for x in range(N)]
    seen = set(); clash = 0
    for x in range(N):
        for y in range(x):
            d = [p - q for p, q in zip(ev[x], ev[y])]
            g = 0
            for t in d: g = gcd(g, abs(t))
            lead = next(t for t in d if t); sgn = 1 if lead > 0 else -1
            key = tuple(sgn * t // g for t in d)
            clash += key in seen; seen.add(key)
    print(f"  k={k}: {N * (N - 1) // 2} pairs, {len(seen)} different helper directions, pairs sharing one: {clash}")
