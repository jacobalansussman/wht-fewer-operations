#!/usr/bin/env python3
"""Machine check (sample) of the step behind 'count (G) >= 2N-1' at N = 8 and 16.
Hold: the N inputs, the first output y = all ones, and its N-2 tree helpers (y restricted to the leaf set of each subtree).
Claim: closing under 'an output that lies on a line through two held points' never yields more than 2 outputs in all.
Exact integer arithmetic (3x3 minors)."""
import sys, random
from itertools import combinations
k = int(sys.argv[1]); trials = int(sys.argv[2]); N = 1 << k
rng = random.Random(7)
Y = [tuple((-1) ** bin(w & x).count('1') for x in range(N)) for w in range(N)]
def on_line(p, u, v):
    # p in span(u, v): every 3x3 minor of the 3 x N matrix vanishes; test via elimination on integers
    rows = [list(u), list(v), list(p)]
    r = 0
    for c in range(N):
        piv = next((i for i in range(r, 3) if rows[i][c] != 0), None)
        if piv is None: continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(r + 1, 3):
            if rows[i][c] != 0:
                a, b = rows[r][c], rows[i][c]
                rows[i] = [a * y - b * x for x, y in zip(rows[r], rows[i])]
        r += 1
        if r == 3: return False
    return True
def run(sets):
    pts = [tuple(int(i == x) for i in range(N)) for x in range(N)]
    pts += [tuple(1 if i in S else 0 for i in range(N)) for S in sets]
    got = [0]
    pts.append(Y[0])
    changed = True
    while changed:
        changed = False
        for w in range(1, N):
            if w in got: continue
            if any(on_line(Y[w], u, v) for u, v in combinations(pts, 2)):
                got.append(w); pts.append(Y[w]); changed = True
    return len(got)
def random_tree(parts):
    parts = [frozenset(p) for p in parts]; inner = []
    while len(parts) > 1:
        a, b = rng.sample(range(len(parts)), 2)
        m = parts[a] | parts[b]
        parts = [p for i, p in enumerate(parts) if i not in (a, b)] + [m]
        if len(m) < N: inner.append(m)
    return inner
hist = {}
for t in range(trials):
    n = run(random_tree([[x] for x in range(N)]))
    hist[n] = hist.get(n, 0) + 1
print(f"N={N} random trees {trials}: outputs reached (first output included) -> count", sorted(hist.items()))
hist = {}
for t in range(trials):
    w = rng.randrange(1, N)
    D = [x for x in range(N) if Y[w][x] == -1]; Dc = [x for x in range(N) if Y[w][x] == 1]
    a = random_tree_part = None
    def sub(S):
        parts = [frozenset([x]) for x in S]; inner = []
        while len(parts) > 1:
            i, j = rng.sample(range(len(parts)), 2)
            m = parts[i] | parts[j]
            parts = [p for q, p in enumerate(parts) if q not in (i, j)] + [m]
            inner.append(m)
        return inner
    n = run(sub(D) + sub(Dc))
    hist[n] = hist.get(n, 0) + 1
print(f"N={N} trees whose root splits along a half D of some output, {trials}:", sorted(hist.items()))
