# Count (O) at 4 points, exhaustive.  A gate is u+v or u-v (cost 1) or c*u (cost 1).
# Fact used [derived in e-5.md]: count (G) minimum for H4 is 7, and a count-(O) program with S scalings and A
# additions gives a count-(G) program with A gates.  So a count-(O) program of total cost 7 has A = 7, S = 0:
# seven additions/subtractions and nothing else.  Such a program has integer wires, so the search is finite.
# Wires are kept up to sign (u-v and v-u are both free; -(u+v) is "u+v up to sign"; see e-5.md for why this loses nothing
# when outputs are wanted up to sign or scale).
# Three conventions for the target, all tested on every reachable wire set:
#   exact : 4 wires equal to +-(row of H4)
#   debt  : 4 wires equal to c_r * (row r of H4), any non-zero integers c_r
#   both  : 4 wires w_r with w_r[j] = c_r * H4[r][j] * d_j, any non-zero c_r, d_j  (inputs and outputs rescaled)
import sys, itertools
H4 = [(1,1,1,1),(1,-1,1,-1),(1,1,-1,-1),(1,-1,-1,1)]
def norm(v):
    for a in v:
        if a != 0:
            return v if a > 0 else tuple(-b for b in v)
    return None
def full(v): return all(v)
def ratio_class(v):
    # for full-support v: the vector v up to scale, as a canonical rational direction
    from math import gcd
    g = 0
    for a in v: g = gcd(g, abs(a))
    return norm(tuple(a//g for a in v))
ROWDIR = {ratio_class(r): i for i, r in enumerate(H4)}
def test_exact(ws):
    return sum(1 for r in H4 if norm(r) in ws) == 4
def test_debt(ws):
    got = set()
    for w in ws:
        if full(w):
            k = ROWDIR.get(ratio_class(w))
            if k is not None: got.add(k)
    return len(got) == 4
def compatible(u, v):
    # full-support u, v: v_j/u_j must be +-t with two plus and two minus  (then they can be two rows of H4*D)
    from fractions import Fraction
    q = [Fraction(b, a) for a, b in zip(u, v)]
    t = abs(q[0])
    if any(abs(x) != t for x in q): return False
    return sum(1 for x in q if x > 0) == 2
def test_both(ws):
    fs = [w for w in ws if full(w)]
    if len(fs) < 4: return None
    for quad in itertools.combinations(fs, 4):
        if all(compatible(a, b) for a, b in itertools.combinations(quad, 2)):
            return quad
    return None
def maxclique(fs):
    # size of the largest pairwise-compatible family among full-support wires (small sets: brute force)
    best = 1 if fs else 0
    for k in (4, 3, 2):
        if len(fs) >= k:
            for c in itertools.combinations(fs, k):
                if all(compatible(a, b) for a, b in itertools.combinations(c, 2)):
                    return k
    return best
def run(depth):
    inputs = frozenset(tuple(1 if i == j else 0 for i in range(4)) for j in range(4))
    seen = set(); hits = {"exact": [], "debt": [], "both": []}
    nodes = [0]
    def dfs(ws, left, hist):
        nodes[0] += 1
        fs = [w for w in ws if full(w)]
        mc = maxclique(fs)
        if mc + left < 4: return
        if mc == 4:
            if test_exact(ws): hits["exact"].append(hist)
            if test_debt(ws): hits["debt"].append(hist)
            q = test_both(ws)
            if q: hits["both"].append((hist, q))
        if left == 0: return
        key = (ws, left)
        if key in seen: return
        seen.add(key)
        wl = sorted(ws)
        for u, v in itertools.combinations(wl, 2):
            for s in (1, -1):
                w = norm(tuple(a + s*b for a, b in zip(u, v)))
                if w is None or w in ws: continue
                dfs(ws | {w}, left - 1, hist + ((u, '+' if s == 1 else '-', v, w),))
    dfs(inputs, depth, ())
    return hits, nodes[0]
if __name__ == "__main__":
    for d in (int(a) for a in sys.argv[1:]):
        hits, n = run(d)
        print("additions/subtractions only, at most", d, "gates; nodes", n)
        for k in ("exact", "debt", "both"):
            print("  convention", k, ": programs found", len(hits[k]))
            if hits[k]:
                ex = hits[k][0]
                print("    example:", ex)
        sys.stdout.flush()
