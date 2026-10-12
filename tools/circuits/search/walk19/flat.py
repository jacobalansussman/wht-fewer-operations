#!/usr/bin/env python3
"""g-1 flat.py: hubs.  For a wire v and an output y_j (a character), the cheapest partner has support
a_j(v) = min over scalars c of #{x : v(x) != c * chi_j(x)}   (then y_j = (v - u)/c with u supported on those places).
Checks, exact (Gaussian integers as pairs):
 (1) hub theorem: for every v and every two outputs i != j, a_i + a_j >= N/2.
     Run on all vectors with entries 0, 1, -1 at 4 and 8 points and on all vectors with entries 1, i, -1, -i at 4 and 8 points.
 (2) census of the forms flat on both sides with entries in 1, i, -1, -i at 8 points (all |H v|^2 equal to 8):
     how many, and the list of partner supports to the 8 outputs.
 (3) the same for sign vectors at 16 points that are flat on both sides (bent functions), by their partner supports.
"""
import itertools, sys
def wht_c(v):
    v = list(v); n = len(v); h = 1
    while h < n:
        for i in range(0, n, 2 * h):
            for j in range(i, i + h):
                a, b = v[j], v[j + h]; v[j], v[j + h] = (a[0] + b[0], a[1] + b[1]), (a[0] - b[0], a[1] - b[1])
        h *= 2
    return v
U = [(1, 0), (0, 1), (-1, 0), (0, -1)]
def mulc(a, b): return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])
def partners(v, N):
    """a_j for every character j: N - (largest number of places where v = c * chi_j, over all scalars c)"""
    out = []
    for j in range(N):
        cnt = {}
        for x in range(N):
            if v[x] == (0, 0): continue
            # c = v(x) / chi_j(x) = v(x) * chi_j(x)
            s = -1 if bin(j & x).count("1") & 1 else 1
            c = (v[x][0] * s, v[x][1] * s); cnt[c] = cnt.get(c, 0) + 1
        out.append(N - max(cnt.values()))
    return out

for k in (2, 3):
    N = 1 << k
    for name, alphabet, lead in (("entries 0, 1, -1", [(0, 0), (1, 0), (-1, 0)], None), ("entries 1, i, -1, -i", U, (1, 0))):
        worst = 10 ** 9; tot = 0; flat = 0; caps = {}; arg = None
        for v in itertools.product(alphabet, repeat=N):
            if all(x == (0, 0) for x in v): continue
            if lead and v[0] != lead: continue
            tot += 1; a = sorted(partners(v, N))
            if a[0] + a[1] < worst: worst = a[0] + a[1]; arg = v
            if lead:
                w = wht_c(v)
                if all(x[0] * x[0] + x[1] * x[1] == N for x in w): flat += 1; caps[tuple(a)] = caps.get(tuple(a), 0) + 1
        print("N = %d, %s: %d vectors; least a_i + a_j over all vectors and pairs of outputs = %d (theorem: >= N/2 = %d)" % (N, name, tot, worst, N // 2))
        if lead: print("   flat on both sides: %d; sorted partner supports to the %d outputs: %s" % (flat, N, sorted(caps.items())))
if len(sys.argv) > 1:
    # sign vectors at 16 points, flat on both sides (bent), first entry +1
    N = 16; flat = 0; caps = {}
    for bits in range(1 << 15):
        v = [(1, 0)] + [((-1 if bits >> t & 1 else 1), 0) for t in range(15)]
        w = wht_c(v)
        if all(x[0] * x[0] == 16 for x in w):
            flat += 1; a = tuple(sorted(partners(v, N))); caps[a] = caps.get(a, 0) + 1
    print("N = 16, sign vectors flat on both sides (first entry +1): %d; sorted partner supports to the 16 outputs: %s" % (flat, sorted(caps.items())))
