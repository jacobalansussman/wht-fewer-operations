# bc4.py: exact minimum circuits with BOUNDED INTEGER coefficients for the second power of a 2x2 kernel, 4 points.
# A gate is a*u + b*v with a, b in the allowed set C (u = v allowed: a doubling). Outputs must be the rows EXACTLY (up to sign).
# Extra values (helpers) are allowed. Every target needs its own gate, and taking a target the moment it is one gate away
# never costs more, so the search is over sets of helpers: gates = 4 + helpers.  Exhaustive for the coefficient set given.
import sys, itertools
def kron(A, B): return [[x*y for x in ra for y in rb] for ra in A for rb in B]
def norm(v):
    for x in v:
        if x: return v if x > 0 else tuple(-y for y in v)
    return None
def run(K, C, maxh, bound):
    T = [norm(tuple(r)) for r in kron(K, K)]
    n = 4; inputs = [tuple(int(i == j) for j in range(n)) for i in range(n)]
    Cp = sorted({(a, b) for a in C for b in C})
    def cands(av):
        out = set()
        L = list(av)
        for i in range(len(L)):
            for j in range(i, len(L)):
                u, v = L[i], L[j]
                for a, b in Cp:
                    w = tuple(a*x + b*y for x, y in zip(u, v))
                    w = norm(w)
                    if w is not None and w not in av and max(map(abs, w)) <= bound: out.add(w)
        return out
    def close(av):
        av = set(av); ch = True
        while ch:
            ch = False
            miss = [t for t in T if t not in av]
            if not miss: break
            cs = cands(av)
            for t in miss:
                if t in cs: av.add(t); ch = True
        return frozenset(av)
    start = close(inputs)
    level = {start}
    for h in range(maxh + 1):
        done = [s for s in level if all(t in s for t in T)]
        print("  helpers %d (gates %d): states %d, solved %d" % (h, 4 + h, len(level), len(done)), flush=True)
        if done:
            s = done[0]; print("   one solution, helper values:", sorted(set(s) - set(inputs) - set(T))); return 4 + h
        nxt = set()
        for s in level:
            for w in cands(s): nxt.add(close(s | {w}))
        level = nxt
    return None
for name, K in [("K=[[1,1],[1,2]]", [[1,1],[1,2]]), ("[[2,1],[1,1]]", [[2,1],[1,1]]), ("H=[[1,1],[1,-1]]", [[1,1],[1,-1]])]:
    for cname, C in [("+1,-1", (1, -1)), ("+-1,+-2", (1, -1, 2, -2))]:
        maxh = int(sys.argv[1]) if len(sys.argv) > 1 else 3
        print(name, "coefficients", cname, flush=True)
        r = run(K, C, maxh if cname == "+1,-1" else min(maxh, 3), 12)
        print("  MINIMUM gates:", r if r else "> %d" % (4 + (maxh if cname == "+1,-1" else min(maxh,3))))
