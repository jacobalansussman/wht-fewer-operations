# n-1: independent census of the non-tight wires that lie on two tight lines (h-8 Lemmas 2, 3, 4), exact integers.
# usage: census.py k all|reps
#  all  : the first wire u of the first line runs over every tight wire (full count, as h-8's gen1.py claims)
#  reps : u runs over one tight wire per level (enough up to the symmetries: affine maps of the addresses and
#         multiplication by a character carry any tight wire of level d to the indicator of a fixed d-dim subspace,
#         and keep s, s', tightness and lines)
import sys, numpy as np
from collections import defaultdict, Counter

def subspaces(k):
    N = 1 << k
    seen = {frozenset([0])}
    frontier = [frozenset([0])]
    while frontier:
        nf = []
        for V in frontier:
            for x in range(1, N):
                if x not in V:
                    Wn = frozenset(V | {v ^ x for v in V})
                    if Wn not in seen:
                        seen.add(Wn)
                        nf.append(Wn)
        frontier = nf
    return seen

def tight_wires(k):
    N = 1 << k
    out = {}
    for V in subspaces(k):
        d = len(V).bit_length() - 1
        done = set()
        for a in range(N):
            c = frozenset(a ^ v for v in V)
            if c in done:
                continue
            done.add(c)
            for m in range(N):
                vec = [0] * N
                for x in c:
                    vec[x] = 1 - 2 * (bin(m & x).count("1") & 1)
                f = next(v for v in vec if v)
                if f < 0:
                    vec = [-v for v in vec]
                out[tuple(vec)] = d
    return out

def wht(M):
    M = np.array(M, dtype=np.int64)
    n = M.shape[-1]
    h = 1
    while h < n:
        M = M.reshape(M.shape[:-1] + (n // (2 * h), 2, h))
        a = M[..., 0, :].copy(); b = M[..., 1, :].copy()
        M[..., 0, :] = a + b; M[..., 1, :] = a - b
        M = M.reshape(M.shape[:-3] + (n,))
        h *= 2
    return M

def canon(R):
    """rows of R (non-zero) -> primitive rows with first non-zero positive, and the signed scalar"""
    g = np.gcd.reduce(np.abs(R), axis=1)
    C = R // g[:, None]
    idx = (C != 0).argmax(axis=1)
    sg = np.sign(C[np.arange(C.shape[0]), idx])
    C = C * sg[:, None]
    return C, g * sg

def main():
    k = int(sys.argv[1]); mode = sys.argv[2]
    N = 1 << k
    tw = tight_wires(k)
    keys = sorted(tw)
    P = np.array(keys, dtype=np.int64)
    lev = np.array([tw[t] for t in keys])
    M = len(keys)
    tightset = set(keys)
    print("k =", k, " N =", N, " tight wires:", M, " by level:", dict(sorted(Counter(lev.tolist()).items())))
    if mode == "all":
        firsts = list(range(M))
    else:
        firsts = []
        for d in range(k + 1):
            vec = tuple(1 if x < (1 << d) else 0 for x in range(N))
            firsts.append(keys.index(vec))
    found = {}        # canonical non-tight h -> True
    wide_violation = 0
    npairs = 0
    for iu in firsts:
        u = P[iu]
        for iv in range(M):
            if iv == iu:
                continue
            if mode == "all" and iv < iu:
                continue
            v = P[iv]
            npairs += 1
            # pivot coordinates with a non-zero 2x2 minor
            i = int(np.nonzero(u)[0][0])
            minors = u[i] * v - u * v[i]
            nz = np.nonzero(minors)[0]
            j = int(nz[0])
            D = int(minors[j])
            A = P[:, i] * v[j] - P[:, j] * v[i]
            B = u[i] * P[:, j] - u[j] * P[:, i]
            R = D * P - np.outer(A, u) - np.outer(B, v)
            nzr = R.any(axis=1)
            online = np.nonzero(~nzr)[0]
            span_uv = int(lev[online].max() - lev[online].min())
            rows = np.nonzero(nzr)[0]
            C, sc = canon(R[rows])
            groups = defaultdict(list)
            for t in range(len(rows)):
                groups[C[t].tobytes()].append(t)
            for g in groups.values():
                if len(g) < 2:
                    continue
                for x in range(len(g)):
                    for y in range(x + 1, len(g)):
                        p = P[rows[g[x]]]; w = P[rows[g[y]]]
                        h = sc[g[y]] * p - sc[g[x]] * w
                        gg = int(np.gcd.reduce(np.abs(h)))
                        h = h // gg
                        f = int(h[np.nonzero(h)[0][0]])
                        if f < 0:
                            h = -h
                        th = tuple(int(z) for z in h)
                        if th in tightset:
                            continue
                        found[th] = True
    print("pairs (u, v) scanned:", npairs, "  distinct non-tight wires on two tight lines:", len(found))
    # every tight line through each such wire
    classes = defaultdict(lambda: [0, Counter(), Counter(), Counter(), Counter()])
    maxratio = 0
    worst = None
    lemma3_fail = 0
    lemma2_fail = 0
    hub_fail = 0
    H = np.array(list(found.keys()), dtype=np.int64)
    if len(H):
        S1 = (H != 0).sum(axis=1)
        S2 = (wht(H) != 0).sum(axis=1)
    for n in range(len(H)):
        h = H[n]
        s, s2 = int(S1[n]), int(S2[n])
        i = int(np.nonzero(h)[0][0])
        R = h[i] * P - np.outer(P[:, i], h)
        C, sc = canon(R)
        groups = defaultdict(list)
        for t in range(M):
            groups[C[t].tobytes()].append(t)
        lines = [g for g in groups.values() if len(g) >= 2]
        spans = []
        near = Counter()
        for g in lines:
            ls = [int(lev[t]) for t in g]
            b, c = min(ls), max(ls)
            spans.append(c - b)
            for l in ls:
                near[l] += 1
            if c - b >= 2:
                # h-8 Lemma 2 windows
                if not ((1 << c) - (1 << b) <= s <= (1 << c) + (1 << b)):
                    lemma2_fail += 1
                if not (N * ((1 << (c - b)) - 1) <= s2 * (1 << c) <= N * ((1 << (c - b)) + 1)):
                    lemma2_fail += 1
        widest = max(spans)
        n2 = sum(1 for x in spans if x == 2)
        if widest > 2 or 16 * s * s2 > 100 * N:
            lemma3_fail += 1
        if n2 > 4 or (n2 >= 2 and s * s2 != 4 * N):
            hub_fail += 1
        if s * s2 > maxratio * N:
            maxratio = s * s2 / N
            worst = tuple(int(z) for z in h)
        cl = classes[(s, s2)]
        cl[0] += 1
        cl[1][len(lines)] += 1
        cl[2][widest] += 1
        cl[3][n2] += 1
        cl[4][tuple(near[l] for l in range(k + 1))] += 1
    print("largest s*s'/N:", maxratio, " at", worst)
    print("h-8 Lemma 2 window failures:", lemma2_fail)
    print("h-8 Lemma 3 failures (a line spanning 3 or more levels, or s*s' > 6.25 N):", lemma3_fail)
    print("hub theorem failures (more than 4 two-level lines, or 2 or more such lines on a wire with s*s' != 4N):", hub_fail)
    print("classes (s, s') : count ; number of tight lines ; widest line ; number of two-level lines ; tight neighbours by level")
    for key in sorted(classes):
        cl = classes[key]
        print("  ", key, ":", cl[0], "; lines", dict(cl[1]), "; widest", dict(cl[2]), "; two-level lines", dict(cl[3]),
              "; neighbours", dict(cl[4].most_common(3)))

main()
