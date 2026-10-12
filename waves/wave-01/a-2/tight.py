#!/usr/bin/env python3
"""a-2: exact checks of "tight wires tie" (i-cross W3).  Pure Python, integers and Fractions only.

A wire is a non-zero linear form a.x in the N = 2^k inputs, taken up to a scalar.  s = number of non-zero entries of a,
s' = number of non-zero entries of H a (the same form written in the outputs y = H x is (H a / N).y).  Tight: s s' = N.

  python3 tight.py ds k          Donoho-Stark at N = 2^k, all support pairs (k = 2, 3): s s' >= N, equality = character on a coset
  python3 tight.py triples k M   all dependent triples of tight wires; M = full (every u) or reduced (one u per level)
  python3 tight.py bfs4          least number of gates for the 4-point transform: tight wires only, and all wires with entries 0, +1, -1
  python3 tight.py rand k T      T random tight-only circuits at N = 2^k, pruned; least size seen
  python3 tight.py slack         the rise and the slack of every gate in the textbook and in the 7-gate-brick circuits; random triples
"""
import sys, random, itertools
from fractions import Fraction
from math import log2


def pc(x):
    return bin(x).count("1")


def had(k):
    N = 1 << k
    return [[1 - 2 * (pc(x & y) & 1) for y in range(N)] for x in range(N)]


def wht(v):
    v = list(v)
    n = len(v)
    h = 1
    while h < n:
        for i in range(0, n, 2 * h):
            for j in range(i, i + h):
                a, b = v[j], v[j + h]
                v[j], v[j + h] = a + b, a - b
        h *= 2
    return v


def subspaces(k):
    N = 1 << k
    seen = {frozenset([0])}
    frontier = [frozenset([0])]
    while frontier:
        new = []
        for V in frontier:
            for g in range(1, N):
                if g not in V:
                    W = frozenset(V | {v ^ g for v in V})
                    if W not in seen:
                        seen.add(W)
                        new.append(W)
        frontier = new
    return seen


def norm(S, Ng):
    """support mask, mask of negative entries; sign fixed so that the lowest entry is +."""
    low = S & -S
    if Ng & low:
        Ng = S & ~Ng
    return (S, Ng)


def tight_wires(k):
    """dict (S, Ng) -> level d, built from the DEFINITION 'a character on a coset of a subgroup'."""
    N = 1 << k
    out = {}
    for V in subspaces(k):
        Vl = sorted(V)
        d = len(Vl).bit_length() - 1
        pats = set()
        for w in range(N):
            pats.add(tuple(pc(w & x) & 1 for x in Vl))
        assert len(pats) == len(Vl)
        reps = sorted({min(c ^ x for x in Vl) for c in range(N)})
        for c in reps:
            S = 0
            for x in Vl:
                S |= 1 << (c ^ x)
            for p in pats:
                Ng = 0
                for x, b in zip(Vl, p):
                    if b:
                        Ng |= 1 << (c ^ x)
                out[norm(S, Ng)] = d
    return out


def vec(w, N):
    S, Ng = w
    return [0 if not (S >> i) & 1 else (-1 if (Ng >> i) & 1 else 1) for i in range(N)]


def from_vec(v):
    """integer vector -> (S, Ng) if all non-zero entries have one absolute value, else None."""
    m = 0
    S = Ng = 0
    for i, x in enumerate(v):
        if x:
            ax = x if x > 0 else -x
            if m == 0:
                m = ax
            elif ax != m:
                return None
            S |= 1 << i
            if x < 0:
                Ng |= 1 << i
    if S == 0:
        return None
    return norm(S, Ng)


RATIOS = [(1, 1), (1, -1), (1, 2), (1, -2), (2, 1), (2, -1)]
# complete for entries 0, +1, -1: p u + q v takes the values +-p, +-q, +-(p+q), +-(p-q); all non-zero ones of one
# absolute value forces q/p in {1, -1, 2, -2, 1/2, -1/2} (derived in a-2.md, section 2).


def comb(u, v, p, q):
    """p u + q v for u, v with entries 0, +1, -1 given as (S, Ng); returns (S, Ng) normalised if flat, else None."""
    Su, Nu = u
    Sv, Nv = v
    Pu, Pv = Su & ~Nu, Sv & ~Nv
    Zu, Zv = ~Su, ~Sv
    mag = 0
    S = Ng = 0
    for mu, cu in ((Pu, 1), (Nu, -1), (Zu, 0)):
        for mv, cv in ((Pv, 1), (Nv, -1), (Zv, 0)):
            val = p * cu + q * cv
            if val == 0:
                continue
            m = mu & mv
            if cu == 0 and cv == 0:
                continue
            if m == 0:
                continue
            a = val if val > 0 else -val
            if mag == 0:
                mag = a
            elif a != mag:
                return None
            S |= m
            if val < 0:
                Ng |= m
    if S == 0:
        return None
    return norm(S, Ng)


def rank_frac(rows, ncols):
    """rank and one kernel vector (if the kernel is a line) of an integer matrix, exact."""
    M = [[Fraction(x) for x in r] for r in rows]
    piv = []
    r = 0
    for c in range(ncols):
        p = None
        for i in range(r, len(M)):
            if M[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        inv = 1 / M[r][c]
        M[r] = [x * inv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        piv.append(c)
        r += 1
    free = [c for c in range(ncols) if c not in piv]
    ker = None
    if len(free) == 1:
        f = free[0]
        ker = [Fraction(0)] * ncols
        ker[f] = Fraction(1)
        for i, c in enumerate(piv):
            ker[c] = -M[i][f]
    return r, ker


def cmd_ds(k):
    N = 1 << k
    H = had(k)
    tw = tight_wires(k)
    print("N = %d: tight wires by definition: %d (N times the number of subgroups = %d)" % (N, len(tw), N * len(subspaces(k))))
    # every tight wire really has s s' = N
    for w, d in tw.items():
        v = vec(w, N)
        s = sum(1 for x in v if x)
        s2 = sum(1 for x in wht(v) if x)
        assert s == 1 << d and s * s2 == N, (w, s, s2)
    print("  each has s = 2^level and s s' = N: yes")
    pts = list(range(N))
    below = eq_zero = eq_one = 0
    found = set()
    for s in range(1, N + 1):
        tmax = N // s
        for S in itertools.combinations(pts, s):
            for t in range(1, tmax + 1):
                for T in itertools.combinations(pts, t):
                    Tc = [y for y in pts if y not in T]
                    rows = [[H[y][x] for x in S] for y in Tc]
                    r, ker = rank_frac(rows, s)
                    dim = s - r
                    if s * t < N:
                        assert dim == 0, ("uncertainty fails", S, T)
                        below += 1
                    else:
                        assert dim <= 1, ("two tight forms on one support pair", S, T)
                        if dim == 0:
                            eq_zero += 1
                        else:
                            eq_one += 1
                            full = [Fraction(0)] * N
                            for x, c in zip(S, ker):
                                full[x] = c
                            assert all(c != 0 for c in ker)
                            den = 1
                            for c in full:
                                den = den * c.denominator // __import__("math").gcd(den, c.denominator)
                            w = from_vec([int(c * den) for c in full])
                            assert w is not None and w in tw, ("tight form that is not a coset character", S, T, ker)
                            found.add(w)
    print("  support pairs with |S||T| < N: %d, all with no non-zero form (so s s' >= N)" % below)
    print("  support pairs with |S||T| = N: %d empty, %d carrying exactly one form up to a scalar" % (eq_zero, eq_one))
    print("  the forms found are exactly the coset characters: %s (%d)" % (found == set(tw), len(found)))


def reps(k, tw):
    """one tight wire per level: the plain sum over the points 0 .. 2^d - 1."""
    out = []
    for d in range(k + 1):
        w = norm((1 << (1 << d)) - 1, 0)
        assert tw[w] == d
        out.append(w)
    return out


def triples(k, mode, tw=None, want_lines=False):
    N = 1 << k
    if tw is None:
        tw = tight_wires(k)
    wires = list(tw)
    us = wires if mode == "full" else reps(k, tw)
    counts = {}
    lines = {}
    bad = 0
    for u in us:
        du = tw[u]
        for v in wires:
            if v == u:
                continue
            for p, q in RATIOS:
                w = comb(u, v, p, q)
                if w is None or w == u or w == v:
                    continue
                dw = tw.get(w)
                if dw is None:
                    continue
                key = (du, tw[v], dw)
                counts[key] = counts.get(key, 0) + 1
                lv = sorted(key)
                if lv[2] - lv[0] > 1:
                    bad += 1
                if want_lines:
                    lines.setdefault((u, v), set()).add(w)
    return tw, counts, bad, lines


def cmd_triples(k, mode):
    N = 1 << k
    tw, counts, bad, _ = triples(k, mode)
    nl = {}
    for d in tw.values():
        nl[d] = nl.get(d, 0) + 1
    print("N = %d, %s: %d tight wires, by level %s" % (N, mode, len(tw), [nl[d] for d in range(k + 1)]))
    print("  ordered (u, v, w) with w = p u + q v tight, w not parallel to u or v, by levels (level u, level v, level w): count")
    shapes = {}
    for key in sorted(counts):
        du, dv, dw = key
        shape = (dv - du, dw - du)
        shapes[shape] = shapes.get(shape, 0) + counts[key]
        print("   %s: %d" % (key, counts[key]))
    print("  shapes (level v - level u, level w - level u): %s" % sorted(shapes.items()))
    print("  triples whose levels differ by more than 1: %d" % bad)
    if mode == "full":
        # the reduced run must agree after multiplying by the orbit sizes
        tw2, c2, bad2, _ = triples(k, "reduced", tw)
        ok = all(counts.get(key, 0) == c2.get(key, 0) * nl[key[0]] for key in set(counts) | set(c2))
        print("  full count = (number of wires of level u) x (count for the one representative), every row: %s" % ok)


def brute_triples(k):
    """independent path: integer vectors, no bit masks, the definition of a gate."""
    N = 1 << k
    tw = tight_wires(k)
    V = {w: vec(w, N) for w in tw}
    wires = list(tw)
    bad = 0
    n = 0
    for i, u in enumerate(wires):
        for v in wires[i + 1:]:
            a, b = V[u], V[v]
            for p, q in RATIOS:
                w = from_vec([p * x + q * y for x, y in zip(a, b)])
                if w is None or w == u or w == v or w not in tw:
                    continue
                n += 1
                lv = sorted((tw[u], tw[v], tw[w]))
                if lv[2] - lv[0] > 1:
                    bad += 1
                assert comb(u, v, p, q) == w
    print("N = %d, brute (integer vectors): %d dependent (unordered pair, third) found, %d with levels more than 1 apart" % (N, n, bad))


def cmd_bfs4():
    k, N = 2, 4
    H = had(k)
    tw = tight_wires(k)
    # (a) tight wires only
    for name, alphabet in (("tight wires only (20 wires)", list(tw)),
                           ("every wire with entries 0, +1, -1 (40 wires)", None)):
        if alphabet is None:
            alphabet = sorted({from_vec(v) for v in itertools.product((0, 1, -1), repeat=N) if any(v)})
        idx = {w: i for i, w in enumerate(alphabet)}
        n = len(alphabet)
        third = [[0] * n for _ in range(n)]
        for i, u in enumerate(alphabet):
            for j, v in enumerate(alphabet):
                if i == j:
                    continue
                for p, q in RATIOS:
                    w = comb(u, v, p, q)
                    if w is not None and w != u and w != v and w in idx:
                        third[i][j] |= 1 << idx[w]
        start = 0
        for i in range(N):
            start |= 1 << idx[norm(1 << i, 0)]
        target = 0
        for y in range(N):
            target |= 1 << idx[from_vec(H[y])]
        level = {start}
        g = 0
        while True:
            hit = [s for s in level if s & target == target]
            if hit:
                break
            nxt = set()
            for s in level:
                mem = [i for i in range(n) if (s >> i) & 1]
                reach = 0
                for a in range(len(mem)):
                    ta = third[mem[a]]
                    for b in range(a + 1, len(mem)):
                        reach |= ta[mem[b]]
                reach &= ~s
                missing = pc(target & ~s)
                while reach:
                    low = reach & -reach
                    reach ^= low
                    nxt.add(s | low)
            level = nxt
            g += 1
            print("   %s: after %d gates %d sets of wires" % (name, g, len(level)), flush=True)
        print("  %s: least number of gates = %d; %d different sets of wires reach it" % (name, g, len(hit)))
        if len(alphabet) == 40:
            nont = {}
            alltight = 0
            for s in hit:
                ws = [alphabet[i] for i in range(n) if (s >> i) & 1]
                nt = [w for w in ws if w not in tw]
                if not nt:
                    alltight += 1
                for w in nt:
                    v = tuple(vec(w, N))
                    nont[v] = nont.get(v, 0) + 1
            print("  of these, sets with no non-tight wire: %d" % alltight)
            byflat = {}
            for s in hit:
                ws = [vec(alphabet[i], N) for i in range(n) if (s >> i) & 1]
                c = sum(1 for v in ws if supp(v) * supp(wht(v)) == N * N)
                c3 = sum(1 for v in ws if supp(v) * supp(wht(v)) not in (N, N * N))
                byflat[(c, c3)] = byflat.get((c, c3), 0) + 1
            print("  sets by (number of wires with s s' = N^2, number of other non-tight wires): %s" % sorted(byflat.items()))
            for v, c in sorted(nont.items()):
                s = sum(1 for x in v if x)
                s2 = sum(1 for x in wht(v) if x)
                print("   non-tight wire %s  s = %d, s' = %d, s s' = %d: in %d of the sets" % (v, s, s2, s * s2, c))


def cmd_rand(k, trials):
    N = 1 << k
    H = had(k)
    tw, counts, bad, lines = triples(k, "full", want_lines=True)
    wires = list(tw)
    idx = {w: i for i, w in enumerate(wires)}
    n = len(wires)
    third = {}
    for (u, v), ws in lines.items():
        third[(idx[u], idx[v])] = [idx[w] for w in ws]
    lev = [tw[w] for w in wires]
    inputs = [idx[norm(1 << i, 0)] for i in range(N)]
    outputs = [idx[from_vec(H[y])] for y in range(N)]
    rng = random.Random(20261010)
    best = None
    hist = {}
    for t in range(trials):
        have = set(inputs)
        parent = {}
        order = list(inputs)
        bias = rng.choice((1.0, 2.0, 4.0, 8.0))
        while not all(o in have for o in outputs):
            cand = {}
            # sample pairs instead of listing all of them
            for _ in range(40):
                a, b = rng.sample(order, 2)
                for w in third.get((a, b), ()):
                    if w not in have:
                        cand[w] = (a, b)
            if not cand:
                continue
            ws = list(cand)
            wts = [bias ** lev[w] for w in ws]
            w = rng.choices(ws, wts)[0]
            have.add(w)
            order.append(w)
            parent[w] = cand[w]
        need = set()
        stack = list(outputs)
        while stack:
            w = stack.pop()
            if w in need or w not in parent:
                continue
            need.add(w)
            stack.extend(parent[w])
        g = len(need)
        hist[g] = hist.get(g, 0) + 1
        if best is None or g < best:
            best = g
    print("N = %d: %d random tight-only circuits, pruned to the wires the outputs use" % (N, trials))
    print("  least number of gates seen: %d   (N log2 N = %d)" % (best, N * k))
    print("  sizes seen (size: how often), smallest ten: %s" % sorted(hist.items())[:10])


def supp(v):
    return sum(1 for x in v if x)


def gate_table(name, k, wires_in_order, gates):
    """wires_in_order: list of integer vectors (inputs first); gates: list of (out index, in1, in2)."""
    N = 1 << k
    s = [supp(v) for v in wires_in_order]
    s2 = [supp(wht(v)) for v in wires_in_order]
    nont = sum(1 for i in range(N, len(wires_in_order)) if s[i] * s2[i] != N)
    rise = 0.0
    bound = 0.0
    for o, a, b in gates:
        r = log2(s[o]) - log2(min(s[a], s[b]))
        if r > 0:
            rise += r
        P = max(s[i] * s2[i] for i in (o, a, b))
        assert s[o] * N <= (N + 2 * P) * min(s[a], s[b])
        bound += log2(1 + 2 * P / N)
    print("  %-28s N = %4d  gates = %5d  N log2 N = %5d  non-tight wires = %4d  sum of rises = %8.2f  sum of log2(1 + 2 P/N) = %8.2f"
          % (name, N, len(gates), N * k, nont, rise, bound))


def textbook(k):
    N = 1 << k
    W = [[1 if i == j else 0 for j in range(N)] for i in range(N)]
    cur = list(range(N))
    gates = []
    for b in range(k):
        bit = 1 << b
        for x in range(N):
            if x & bit:
                continue
            u, v = cur[x], cur[x | bit]
            W.append([p + q for p, q in zip(W[u], W[v])])
            gates.append((len(W) - 1, u, v))
            a = len(W) - 1
            W.append([p - q for p, q in zip(W[u], W[v])])
            gates.append((len(W) - 1, u, v))
            cur[x], cur[x | bit] = a, len(W) - 1
    assert [W[cur[x]] for x in range(N)] == had(k)
    return W, gates


def bricks(k):
    """the 4-point transform in 7 gates (helper h = x0 - x1 - x2 - x3, each output = +-h + 2 x_i), on bit pairs."""
    assert k % 2 == 0
    N = 1 << k
    W = [[1 if i == j else 0 for j in range(N)] for i in range(N)]
    cur = list(range(N))
    gates = []

    def add(u, v, p, q):
        W.append([p * a + q * b for a, b in zip(W[u], W[v])])
        gates.append((len(W) - 1, u, v))
        return len(W) - 1

    for b in range(0, k, 2):
        b0, b1 = 1 << b, 1 << (b + 1)
        for x in range(N):
            if x & (b0 | b1):
                continue
            i0, i1, i2, i3 = cur[x], cur[x | b0], cur[x | b1], cur[x | b0 | b1]
            t1 = add(i0, i1, 1, -1)
            t2 = add(i2, i3, 1, 1)
            h = add(t1, t2, 1, -1)              # x0 - x1 - x2 - x3
            y0 = add(h, i0, -1, 2)              # x0 + x1 + x2 + x3
            y1 = add(h, i2, 1, 2)               # x0 - x1 + x2 - x3
            y2 = add(h, i1, 1, 2)               # x0 + x1 - x2 - x3
            y3 = add(h, i3, 1, 2)               # x0 - x1 - x2 + x3
            cur[x], cur[x | b0], cur[x | b1], cur[x | b0 | b1] = y0, y1, y2, y3
    assert [W[cur[x]] for x in range(N)] == had(k), "brick circuit does not compute the transform"
    return W, gates


def cmd_slack():
    print("gate by gate: rise = log2 s(out) - log2 min s(in), counted when positive; P = largest s s' among the gate's three wires")
    for k in (1, 2, 3, 4, 5, 6, 7, 8):
        W, g = textbook(k)
        gate_table("textbook", k, W, g)
    for k in (2, 4, 6, 8):
        W, g = bricks(k)
        gate_table("7-gate bricks on bit pairs", k, W, g)
    rng = random.Random(7)
    for k in (3, 4, 5):
        N = 1 << k
        n = 0
        worst = 0.0
        while n < 20000:
            dens = rng.choice((0.15, 0.3, 0.6, 1.0))
            u = [rng.choice((-2, -1, 1, 2, 3)) if rng.random() < dens else 0 for _ in range(N)]
            v = [rng.choice((-2, -1, 1, 2, 3)) if rng.random() < dens else 0 for _ in range(N)]
            if rng.random() < 0.5:                      # make cancellations likely
                for i in range(N):
                    if rng.random() < 0.5:
                        v[i] = u[i]
            p, q = rng.choice((1, -1, 2, -2, 3)), rng.choice((1, -1, 2, -2, 3))
            w = [p * a + q * b for a, b in zip(u, v)]
            if not any(u) or not any(v) or not any(w):
                continue
            # parallel pairs are not gates
            if all(u[i] * v[j] == u[j] * v[i] for i in range(N) for j in range(i)):
                continue
            n += 1
            for (o, a, b) in ((w, u, v), (u, v, w), (v, u, w)):
                so, sa, sb = supp(o), supp(a), supp(b)
                P = max(supp(z) * supp(wht(z)) for z in (o, a, b))
                assert P >= N
                assert so * N <= (N + 2 * P) * min(sa, sb), (u, v, w)
                worst = max(worst, so * N / ((N + 2 * P) * min(sa, sb)))
        print("  N = %d: 20000 random dependent triples (60000 gate readings): s(out) <= (1 + 2P/N) min s(in) always; largest ratio of the two sides %.3f" % (N, worst))


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "ds":
        cmd_ds(int(sys.argv[2]))
    elif c == "triples":
        cmd_triples(int(sys.argv[2]), sys.argv[3])
    elif c == "brute":
        brute_triples(int(sys.argv[2]))
    elif c == "bfs4":
        cmd_bfs4()
    elif c == "rand":
        cmd_rand(int(sys.argv[2]), int(sys.argv[3]))
    elif c == "slack":
        cmd_slack()
