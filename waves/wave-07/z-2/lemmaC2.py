# z-2: the "forced step" of x-4 lemma C, case e = +1, exhaustive over SIGN-valued p, q, pure Python (no numpy here).
# Condition: for all x, y with x + y outside {0, m1, m2, m1+m2}:  p(x) = chi(y)  or  q(y) = psi(x),
# chi(y) = (-1)^(m1.y), psi(x) = (-1)^(x.m2); p invariant under x -> x + m1, q under y -> y + m2.
# Search: choose q class by class; each choice FIXES p on a set; prune when p is asked to be +1 and -1 at one point.
# Every pair m1, m2 with m1.m2 = 0 (m1 = m2 included), plain labelling (dot product), 16 and 32 points.
import sys
def dot(x, y): return bin(x & y).count('1') & 1

def solve(k, m1, m2):
    N = 1 << k
    excl = {0, m1, m2, m1 ^ m2}
    yreps = [y for y in range(N) if y < (y ^ m2)]
    S = {}
    for y in yreps:
        for s in (0, 1):                       # s = 1: q(y) = -1
            m = 0
            for yy in (y, y ^ m2):
                for x in range(N):
                    if (x ^ yy) in excl: continue
                    if dot(x, m2) != s: m |= (1 << x) | (1 << (x ^ m1))
            S[(y, s)] = m
    total = 0; sols = []
    def rec(i, A, B, q):
        nonlocal total
        if A & B: return
        if i == len(yreps):
            free = (N - bin(A | B).count('1')) // 2
            total += 1 << free
            if len(sols) < 50: sols.append((A, B, tuple(q)))
            return
        y = yreps[i]
        for s in (0, 1):
            if dot(m1, y): rec(i + 1, A, B | S[(y, s)], q + [s])      # chi(y) = -1: p = -1 on the set
            else:          rec(i + 1, A | S[(y, s)], B, q + [s])      # chi(y) = +1: p = +1 on the set
    rec(0, 0, 0, [])
    return total, sols

for k in (3, 4, 5, 6):
    N = 1 << k
    hist = {}; npairs = 0; notpred = 0
    pairs = [(m1, m2) for m1 in range(1, N) for m2 in range(1, N) if dot(m1, m2) == 0]
    if k == 6:
        # 64 points: a sample of pairs (every 23rd), to push one size beyond the 450 pairs of x-4
        pairs = pairs[::23]
    for (m1, m2) in pairs:
        npairs += 1
        n, sols = solve(k, m1, m2)
        hist[(n, m1 == m2)] = hist.get((n, m1 == m2), 0) + 1
        psi = sum(1 << x for x in range(N) if dot(x, m2))
        full = (1 << N) - 1
        # predicted: p = eta psi, that is (A, B) = (complement of psi-set, psi-set) or the reverse
        got = {(A, B) for (A, B, q) in sols}
        if got != {(full ^ psi, psi), (psi, full ^ psi)}: notpred += 1
    print(f"N={N}: {npairs} pairs m1, m2 with m1.m2 = 0;  (solutions, m1 == m2) -> pairs: {sorted(hist.items())};"
          f"  pairs whose solutions are NOT exactly p = +psi and p = -psi: {notpred}", flush=True)
