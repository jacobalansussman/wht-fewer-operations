#!/usr/bin/env python3
"""g-1 flipwalk.py: the 'one merge tree + flip walk' model read off the 19-gate circuit.  Count (G).  Exact integers.
Design: a sign vector F0 on N = 2^k points and a chain of subgroups V_1 < V_2 < ... < V_(k-1) of the addresses.
Circuit: (1) build F0 by merging: pairs (cosets of V_1), quads (cosets of V_2), ... : N - 1 gates; every node A of this
tree leaves behind the wire F0 restricted to A.  (2) walk: from a held full-support sign vector v make v with the signs on A
flipped, v - 2 (v restricted to A): ONE gate if A is a single point (the partner is an input) or A is a tree node on which v
equals +-F0 (the partner is the tree's wire).  Outputs = the N characters, up to sign.
In 'difference' coordinates D = {x : v(x) != F0(x)} (D and its complement are the same wire): a step toggles a point, or
toggles a tree node A lying entirely inside or entirely outside D.  Gates = N - 1 + (edges of a tree in this graph that
contains the empty set and the N target sets).  That is a Steiner tree problem; here: the shortest-path heuristic (upper bounds)
with random tie-breaking, over many designs.  The best design is turned into an explicit circuit and replayed exactly.
usage: flipwalk.py k seconds seed [quad|any]
"""
import sys, time, random, itertools
import numpy as np

def chi(j, x): return -1 if bin(j & x).count("1") & 1 else 1

def nodes_of(k, flag):
    N = 1 << k; out = []; V = [0]
    for d in flag:
        V = V + [x ^ d for x in V]; seen = set()
        for c in range(N):
            m = 0
            for x in V: m |= 1 << (x ^ c)
            if m not in seen: seen.add(m); out.append(m)
    return out                       # proper nodes of sizes 2, 4, ..., N/2

def steiner(k, F0, flag, rng, tries=2):
    N = 1 << k; FULL = (1 << N) - 1
    canon = lambda D: D ^ FULL if D & 1 else D
    nodes = nodes_of(k, flag); pts = [1 << p for p in range(N)]
    targets = sorted({canon(sum(1 << x for x in range(N) if chi(j, x) != F0[x])) for j in range(N)})
    best = None
    allm = np.arange(1 << N, dtype=np.int64)
    for _ in range(tries):
        intree = np.zeros(1 << N, dtype=bool); intree[0] = True; edges = []          # edges: (child D, parent D, moved set)
        todo = set(t for t in targets if t != 0)
        while todo:
            dist = np.full(1 << N, -1, dtype=np.int32); par = np.full(1 << N, -1, dtype=np.int64); mv = np.zeros(1 << N, dtype=np.int64)
            front = np.nonzero(intree)[0]; dist[front] = 0; hit = None; d = 0
            moves = pts + nodes;
            while hit is None and len(front):
                d += 1; newf = []
                order = list(range(len(moves))); rng.shuffle(order)
                for mi in order:
                    A = moves[mi]
                    if mi < N: src = front
                    else:
                        a = front & A; src = front[(a == 0) | (a == A)]
                    nb = src ^ A; nb = np.where(nb & 1, nb ^ FULL, nb)
                    new = dist[nb] < 0
                    nbn = nb[new]; srcn = src[new]
                    # keep first occurrence
                    u, idx = np.unique(nbn, return_index=True)
                    dist[u] = d; par[u] = srcn[idx]; mv[u] = A; newf.append(u)
                front = np.concatenate(newf) if newf else np.array([], dtype=np.int64)
                reached = [t for t in todo if dist[t] >= 0]
                if reached: hit = rng.choice(reached)
            if hit is None: return None
            v = hit
            while not intree[v]:
                edges.append((int(v), int(par[v]), int(mv[v]))); intree[v] = True; v = int(par[v])
            todo = {t for t in todo if not intree[t]}
        if best is None or len(edges) < len(best): best = edges
    return best, targets

def replay(k, F0, flag, edges):
    """explicit circuit from a design and a flip tree; exact; returns (gates, ok)"""
    N = 1 << k; FULL = (1 << N) - 1; gates = 0
    vec = lambda mask, base: [base[x] if mask >> x & 1 else 0 for x in range(N)]
    held = {}                                     # mask -> F0 restricted to it
    for p in range(N): held[1 << p] = vec(1 << p, F0)       # an input times a sign: free (scalings are free)
    V = [0]
    for d in list(flag) + [None]:
        if d is None:
            # top merge: the two cosets of V_(k-1)
            cos = sorted({sum(1 << (x ^ c) for x in V) for c in range(N)})
        else:
            cos = None
        Vn = V + [x ^ d for x in V] if d is not None else None
        if d is not None:
            seen = set()
            for c in range(N):
                lo = sum(1 << (x ^ c) for x in V); hi = sum(1 << (x ^ c ^ d) for x in V); m = lo | hi
                if m in seen: continue
                seen.add(m); a, b = held[lo], held[hi]; held[m] = [x + y for x, y in zip(a, b)]; gates += 1
                assert held[m] == vec(m, F0)
            V = Vn
        else:
            a, b = held[cos[0]], held[cos[1]]; held[FULL] = [x + y for x, y in zip(a, b)]; gates += 1
            assert held[FULL] == list(F0)
    full = {0: list(F0)}                           # difference set (canonical) -> held full vector
    canon = lambda D: D ^ FULL if D & 1 else D
    pending = list(edges); progress = True
    while pending and progress:
        progress = False; rest = []
        for (child, parent, A) in pending:
            if parent not in full: rest.append((child, parent, A)); continue
            v = full[parent]; part = [v[x] if A >> x & 1 else 0 for x in range(N)]
            base = held[A]
            assert part == base or part == [-x for x in base], "partner is not a held wire"
            w = [x - 2 * y for x, y in zip(v, part)]; gates += 1          # one gate: v - 2 * (+-held wire)
            D = canon(sum(1 << x for x in range(N) if w[x] != F0[x]))
            if D != child:                       # the same wire up to sign
                D2 = canon(sum(1 << x for x in range(N) if -w[x] != F0[x])); assert D2 == child or D == child
            full[child] = w; progress = True
        pending = rest
    assert not pending
    have = set()
    for w in full.values(): have.add(tuple(w)); have.add(tuple(-x for x in w))
    ok = all(tuple(chi(j, x) for x in range(N)) in have for j in range(N))
    return gates, ok

def flags(k):
    N = 1 << k; out = []
    def rec(V, fl):
        if len(fl) == k - 1: out.append(tuple(fl)); return
        seen = set()
        for d in range(1, N):
            if d in V: continue
            W = frozenset(V | {x ^ d for x in V})
            if W in seen: continue
            seen.add(W); rec(W, fl + [d])
    rec(frozenset([0]), []); return out

if __name__ == "__main__":
    k, secs, seed = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]); kind = sys.argv[4] if len(sys.argv) > 4 else "any"
    N = 1 << k; rng = random.Random(seed); t0 = time.time(); fl = flags(k); best = None; hist = {}; nd = 0
    print("N = %d: %d chains of subgroups; designs sampled at random (%s sign vectors); count (G)" % (N, len(fl), kind), flush=True)
    # the design of the 19-gate circuit, first, as a check of this program (k = 3)
    fixed = []
    if k == 3: fixed.append(([1, -1, -1, -1, 1, 1, -1, 1], (7, 1)))
    while time.time() - t0 < secs:
        if fixed: F0, flag = fixed.pop()
        else:
            flag = rng.choice(fl)
            if kind == "quad":
                # (-1)^(quadratic form): random upper-triangular form
                pairs = [(a, b) for a in range(k) for b in range(a + 1, k)]; co = [rng.random() < 0.5 for _ in pairs]
                F0 = [(-1) ** sum(c and (x >> a & 1) and (x >> b & 1) for c, (a, b) in zip(co, pairs)) for x in range(N)]
            else:
                F0 = [1] + [rng.choice((1, -1)) for _ in range(N - 1)]
        r = steiner(k, F0, flag, rng)
        if r is None: continue
        edges, targets = r; nd += 1; g = N - 1 + len(edges); hist[g] = hist.get(g, 0) + 1
        if best is None or g < best[0]:
            gates, ok = replay(k, F0, flag, edges)
            best = (g, F0, flag, edges); print("   t=%.0fs design %d: %d gates (replayed exactly: %d gates, all %d characters present: %s)  F0 = %s  chain = %s" % (time.time() - t0, nd, g, gates, N, ok, F0, flag), flush=True)
    print("N = %d: %d designs; gates found (count: designs): %s" % (N, nd, sorted(hist.items())))
    g, F0, flag, edges = best
    print("best: %d gates = %d (merge tree) + %d (flip steps); textbook %d; F0 = %s; chain = %s" % (g, N - 1, len(edges), N * k, F0, flag))
    print("flip steps (new difference set <- old difference set, toggled set):")
    for (c, p, A) in edges[::-1]: print("   %s <- %s  toggling %s" % (format(c, "0%db" % N), format(p, "0%db" % N), format(A, "0%db" % N)))
