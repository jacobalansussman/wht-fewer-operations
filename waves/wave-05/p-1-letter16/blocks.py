# p-1-letter16: the 2 x 2 blocks (row pair of the row tree) x (column pair of the column tree) of M = diag(r) H diag(c), dual chains.
# Each block of H has rank one, so each block of M is one of four kinds:
#   flat (all four equal), vertical (columns opposite, rows equal: one column of the block is -1), horizontal, checker (diagonal).
# Claim tested here: for EVERY pair of sign vectors,  #flat = #checker.   Exact (whole numbers).  Random signs + named designs.
import random, json, sys
def par(a): return bin(a).count('1') & 1
def census(N, v, w, r, c):
    # row pairs {y, y^v}, column pairs {x, x^w}, v.w = 0
    cnt = {'flat': 0, 'vertical': 0, 'horizontal': 0, 'checker': 0}
    for y in range(N):
        if y > y ^ v: continue
        for x in range(N):
            if x > x ^ w: continue
            m = [[r[a] * c[b] * (-1) ** par(a & b) for b in (x, x ^ w)] for a in (y, y ^ v)]
            roweq = m[0][0] == m[1][0]; coleq = m[0][0] == m[0][1]
            assert m[0][0] * m[1][1] == m[0][1] * m[1][0]
            cnt['flat' if roweq and coleq else 'vertical' if roweq else 'horizontal' if coleq else 'checker'] += 1
    return cnt
random.seed(5); bad = 0; seen = {}
for N, v, w in ((8, 6, 7), (16, 1, 8), (32, 1, 16), (64, 1, 32)):
    for t in range(4000 if N <= 16 else 300):
        r = [random.choice([1, -1]) for _ in range(N)]; c = [random.choice([1, -1]) for _ in range(N)]
        k = census(N, v, w, r, c); bad += k['flat'] != k['checker'] or k['vertical'] != k['horizontal']
        seen.setdefault(N, set()).add(k['checker'])
    print("N", N, " random sign pairs: violations of #flat = #checker and #vertical = #horizontal:", bad, "  values of #checker seen: min", min(seen[N]), "max", max(seen[N]), " blocks in all:", N * N // 4)
named = {
 '45-design (rank-2 forms)': ([(-1) ** (y & 1) if y < 8 else 1 for y in range(16)], [1 if x % 2 == 0 else (-1) ** (x >> 3 & 1) for x in range(16)]),
 'bent x0x1+x2x3 with its transform': None,
 'all ones': ([1] * 16, [1] * 16),
}
c = [(-1) ** ((x & 1) * (x >> 1 & 1) ^ (x >> 2 & 1) * (x >> 3 & 1)) for x in range(16)]
a = [sum((-1) ** par(y & x) * c[x] for x in range(16)) // 4 for y in range(16)]
named['bent x0x1+x2x3 with its transform'] = (a, c)
for nm, (r, c) in named.items(): print(" ", nm, census(16, 1, 8, r, c))
r8 = [1, 1, 1, 1, 1, -1, -1, 1]; c8 = [1, 1, 1, -1, 1, -1, 1, 1]
print("  8 points, the 13-design", census(8, 6, 7, r8, c8))
