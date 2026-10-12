# Exact census of the cheapest linear circuits for sub-rectangles of the 4-point Walsh-Hadamard matrix.
# Gate: w = a*u + b*v, scalings free (vectors are kept up to a scalar: primitive integer vector, first non-zero positive).
# A gate that makes a wanted output may use ANY rational a, b (test: output in span(u, v), exact integer minors).
# A gate that makes a helper uses u + c*v with c in RATIOS (the only restriction of this search).
import sys, itertools
from math import gcd
RATIOS = [(1,1),(1,-1),(1,2),(1,-2),(2,1),(2,-1),(1,3),(1,-3),(3,1),(3,-1)]
H4 = [(1,1,1,1),(1,-1,1,-1),(1,1,-1,-1),(1,-1,-1,1)]
def norm(v):
    g = 0
    for a in v: g = gcd(g, abs(a))
    if g == 0: return None
    v = tuple(a//g for a in v)
    for a in v:
        if a != 0:
            if a < 0: v = tuple(-b for b in v)
            break
    return v
def inspan(u, v, t):
    n = len(u)
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                d = (u[i]*(v[j]*t[k]-v[k]*t[j]) - u[j]*(v[i]*t[k]-v[k]*t[i]) + u[k]*(v[i]*t[j]-v[j]*t[i]))
                if d: return False
    return True
def search(ncols, rows, depth, collect):
    inputs = [tuple(1 if i == j else 0 for i in range(ncols)) for j in range(ncols)]
    targets = set()
    for r in rows:
        t = norm(H4[r][:ncols])
        targets.add(t)
    targets -= set(inputs)
    seen = set(); sols = set()
    def dfs(base, missing, left):
        if not missing:
            sols.add(frozenset(base) - set(inputs)); return
        if left < len(missing): return
        key = (frozenset(base), left)
        if key in seen: return
        seen.add(key)
        bl = list(base)
        for t in missing:
            ok = False
            for u, v in itertools.combinations(bl, 2):
                if inspan(u, v, t) if ncols >= 3 else True:
                    ok = True; break
            if ok:
                dfs(base | {t}, missing - {t}, left - 1)
                if sols and not collect: return
        if left > len(missing):
            for u, v in itertools.combinations(bl, 2):
                for a, b in RATIOS:
                    w = norm(tuple(a*x + b*y for x, y in zip(u, v)))
                    if w is None or w in base or w in missing: continue
                    dfs(base | {w}, missing, left - 1)
                    if sols and not collect: return
    dfs(frozenset(inputs), frozenset(targets), depth)
    return sols, targets
if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "full":
        for d in (6, 7):
            sols, targets = search(4, [0,1,2,3], d, True)
            print("H4 full, gates", d, ": distinct gate sets", len(sols))
            if sols:
                kinds = {}
                for s in sols:
                    helpers = tuple(sorted(tuple(sorted(sum(1 for a in v if a) for v in s - targets))))
                    kinds.setdefault(helpers, []).append(s)
                for k, lst in sorted(kinds.items()):
                    print("  helper supports", k, ":", len(lst), "sets; example helpers", sorted(lst[0] - targets))
    else:
        print("cheapest gate count for (live inputs = first a columns) x (wanted rows): exact within the helper-ratio set")
        for a in (1,2,3,4):
            for m in range(1, 5):
                for rows in itertools.combinations(range(4), m):
                    best = None
                    for d in range(0, 8):
                        sols, targets = search(a, rows, d, False)
                        if sols: best = d; break
                    print("a=%d rows=%s distinct targets=%d min gates=%s" % (a, rows, len(targets), best))
