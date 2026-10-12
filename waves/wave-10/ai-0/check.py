#!/usr/bin/env python3
"""check.py [ai-0]  Critic's own code for ag-0's "tower of lamps" (degree 3 at all cube points with two helpers).
Nothing is imported from ag-0 or ad-6.  Whole numbers only (numpy int64, values stay tiny; python ints for counts).

Address x = a | (y << t): a = t selector bits (the colour), y = m bits.  Tower with Lr real colours and atoms of s bits:
level 0 = one atom (bits 0..s-1); level j = one atom per value of all bits below it.  Colour c < Lr forgets, at y, the
level-c atom whose index is the value of all lower bits.  Colours >= Lr forget nothing.  'extra' = free bits on top.

modes:
  good  Lr s t extra dmax      : my own test "every monomial of degree <= d is U[P1 class] + V[P2 class]" (BFS, exact)
  build Lr s t extra           : build the circuit gate by gate from MY closed formula for the helpers, replay on every
                                 unit input (each wire carries its exact linear form), count gates (G)
"""
import sys, itertools, time
import numpy as np

def levels(Lr, s):
    offs = []; m = 0
    for j in range(Lr):
        offs.append(m); m += s * (1 if j == 0 else (1 << m))
    return offs, m

class Tower:
    def __init__(self, Lr, s, t, extra):
        self.Lr, self.s, self.t = Lr, s, t
        self.offs, self.mt = levels(Lr, s)
        self.m = self.mt + extra; self.k = t + self.m; self.N = 1 << self.k
        assert Lr <= (1 << t)
        self.lev = [None] * self.m                       # level of a y bit (None = free bit)
        self.iota = [None] * self.m                      # the value of the lower bits at which this bit's atom is active
        for j in range(Lr):
            width = s * (1 if j == 0 else (1 << self.offs[j]))
            for b in range(self.offs[j], self.offs[j] + width):
                self.lev[b] = j; self.iota[b] = (b - self.offs[j]) // s
    def active(self, c, y):
        """mask of the atom colour c forgets at y (0 for a colour that forgets nothing)"""
        if c >= self.Lr: return 0
        off = self.offs[c]
        idx = y & ((1 << off) - 1)
        return ((1 << self.s) - 1) << (off + self.s * idx)

def mons(k, d):
    return [sum(1 << i for i in S) for j in range(d + 1) for S in itertools.combinations(range(k), j)]

def good(T, d):
    """exact: is every monomial of degree <= d a sum U[P1(x)] + V[P2(x)] ?  BFS over the graph classes/points."""
    k, N, t = T.k, T.N, T.t; M = np.array(mons(k, d), dtype=np.int64); D = len(M)
    am = (1 << t) - 1
    def phi(x): return ((x & M) == M).astype(np.int64)
    c1 = {}; c2 = {}; l2 = [None] * N
    for x in range(N):
        a = x & am; y = x >> t
        c1.setdefault(y, []).append(x)
        l2[x] = (a, y & ~T.active(a, y)); c2.setdefault(l2[x], []).append(x)
    U = {}; V = {}; comps = 0
    for root in c1:
        if root in U: continue
        comps += 1; U[root] = np.zeros(D, dtype=np.int64); todo = [(1, root)]
        while todo:
            side, c = todo.pop()
            if side == 1:
                u = U[c]
                for x in c1[c]:
                    val = phi(x) - u; v = l2[x]
                    if v in V:
                        if not np.array_equal(V[v], val): return False, len(c1) + len(c2), None
                    else: V[v] = val; todo.append((2, v))
            else:
                v = V[c]
                for x in c2[c]:
                    val = phi(x) - v; u = x >> t
                    if u in U:
                        if not np.array_equal(U[u], val): return False, len(c1) + len(c2), None
                    else: U[u] = val; todo.append((1, u))
    return True, len(c1) + len(c2), comps

# ----------------------------------------------------------------------------------------------------------- circuit
class W:
    __slots__ = ("v",)
    def __init__(self, v): self.v = v

class Ckt:
    """count (G): one gate = a*u + b*v with u, v two wires that are not zero.  Scaling one wire is free."""
    def __init__(self, replay): self.gates = 0; self.replay = replay; self.by = {}
    def comb(self, terms, what):
        """terms: list of (integer coefficient, wire or None).  n live terms cost n - 1 gates."""
        live = [(c, w) for c, w in terms if w is not None and c != 0]
        # cancel exact repeats of one wire (u - u): no gate, no wire
        acc = {}
        for c, w in live: acc[id(w)] = (acc.get(id(w), (0, w))[0] + c, w)
        live = [(c, w) for c, w in acc.values() if c != 0]
        if not live: return None
        if len(live) == 1 and live[0][0] == 1: return live[0][1]
        self.gates += len(live) - 1; self.by[what] = self.by.get(what, 0) + len(live) - 1
        if not self.replay: return W(None)
        v = live[0][0] * live[0][1].v
        for c, w in live[1:]: v = v + c * w.v
        return W(v)

def eval_poly(C, coef, vars_, deg, what):
    """textbook: values of a polynomial (dict mask -> wire) of degree <= deg at all points of the cube on vars_.
    returns a list indexed by the compact index over vars_.  f = g + x_v h: one gate per point with x_v = 1."""
    if not vars_:
        return [coef.get(0)]
    if all(w is None for w in coef.values()):
        return [None] * (1 << len(vars_))
    v = vars_[-1]; bit = 1 << v
    g = {mk: w for mk, w in coef.items() if not mk & bit}
    h = {mk ^ bit: w for mk, w in coef.items() if mk & bit}
    vg = eval_poly(C, g, vars_[:-1], deg, what)
    vh = eval_poly(C, h, vars_[:-1], deg - 1, what) if h else [None] * len(vg)
    return vg + [C.comb([(1, a), (1, b)], what) for a, b in zip(vg, vh)]

def build(T, replay=True):
    Lr, s, t, m, k, N = T.Lr, T.s, T.t, T.m, T.k, T.N
    M = mons(k, 3); D = len(M); pos = {mk: i for i, mk in enumerate(M)}
    C = Ckt(replay); T.checked = 0
    eye = np.eye(D, dtype=np.int64) if replay else None
    inp = {mk: W(eye[i] if replay else None) for mk, i in pos.items()}     # one input per monomial of (a, y)
    am = (1 << t) - 1
    ymons = [mk for mk in mons(m, 3)]                                       # masks over y bits
    # c0(y): the part without selector bits, a cubic in y.  Q_c(y): the rest at selector value c, a quadratic in y.
    c0 = {S: inp[S << t] for S in ymons}
    Q = []
    for c in range(1 << t):
        subs = [sa for sa in range(1, 1 << t) if sa & ~c == 0]
        q = {}
        for S in ymons:
            dS = bin(S).count("1")
            if dS > 2: continue
            w = C.comb([(1, inp[sa | (S << t)]) for sa in subs if bin(sa).count("1") + dS <= 3], "coefficients")
            if w is not None: q[S] = w
        Q.append(q)
    INF = 10 ** 9
    lev = [INF if l is None else l for l in T.lev]
    # MY FORMULA for the P1 helper A = c0 + A', A' a quadratic in y:
    #   coefficient of y_p y_q : the one of Q_c, c = the lower of the two levels (0 if both bits are free)
    #   coefficient of y_q, q at level l in the atom that is active at "lower bits = iota":
    #        Q_l[q] + sum over lower bits p set in iota of ( Q_l[p q] - Q_lev(p)[p q] )
    Ap = {}
    for p in range(m):
        for q in range(p + 1, m):
            c = min(lev[p], lev[q])
            if c < INF and (1 << p | 1 << q) in Q[c]: Ap[1 << p | 1 << q] = Q[c][1 << p | 1 << q]
    for q in range(m):
        l = lev[q]
        if l == INF: continue
        terms = [(1, Q[l].get(1 << q))]
        io = T.iota[q] if l > 0 else 0
        for p in range(T.offs[l]):
            if io >> p & 1:
                terms.append((1, Q[l].get(1 << p | 1 << q))); terms.append((-1, Q[lev[p]].get(1 << p | 1 << q)))
        w = C.comb(terms, "coefficients")
        if w is not None: Ap[1 << q] = w
    Acoef = {}
    for S in ymons:
        w = C.comb([(1, c0.get(S)), (1, Ap.get(S))], "coefficients")
        if w is not None: Acoef[S] = w
    A = eval_poly(C, Acoef, list(range(m)), 3, "helper A (cubic at the P1 classes)")
    # P2 helpers: E_c = Q_c - A', a quadratic in y that must not depend on the active atom of colour c
    B = {}
    for c in range(1 << t):
        E = {}
        for S in ymons:
            if bin(S).count("1") > 2: continue
            w = C.comb([(1, Q[c].get(S)), (-1, Ap.get(S))], "coefficients")
            if w is not None: E[S] = w
        if c >= Lr:
            vals = eval_poly(C, E, list(range(m)), 2, "helper B, colours that forget nothing")
            for y in range(1 << m): B[(c, y)] = vals[y]
            continue
        off = T.offs[c]
        for io in range(1 << off):
            act = ((1 << s) - 1) << (off + s * io)
            free = [b for b in range(off, m) if not act >> b & 1]
            low = [p for p in range(off) if io >> p & 1]
            R = {}
            for S, w in E.items():                      # restrict E_c to "lower bits = io"
                lo = S & ((1 << off) - 1); hi = S ^ lo
                if any(not io >> p & 1 for p in range(off) if lo >> p & 1): continue
                R.setdefault(hi, []).append((1, w))
            Rw = {}
            for hi, terms in R.items():
                if hi & act:
                    # THE CHECK OF THE HELPER CLAIM in this piece: a coefficient that contains a bit of the active atom
                    # must be zero as a linear form in the inputs.  Formed on a scratch counter: it is not a gate.
                    if replay:
                        w = Ckt(True).comb(terms, "scratch"); T.checked += 1
                        assert w is None or not w.v.any(), ("active atom survives", c, io, hi)
                    continue
                w = C.comb(terms, "coefficients per piece")
                if w is not None: Rw[hi] = w
            vals = eval_poly(C, Rw, free, 2, "helper B (quadratic on each piece)")
            for z in range(1 << len(free)):
                y = io
                for j, b in enumerate(free):
                    if z >> j & 1: y |= 1 << b
                B[(c, y)] = vals[z]
    # outputs
    bad = 0
    for x in range(N):
        a = x & am; y = x >> t
        o = C.comb([(1, A[y]), (1, B[(a, y & ~T.active(a, y))])], "outputs")
        if replay:
            want = np.fromiter(((x & mk) == mk for mk in M), dtype=np.int64, count=D)
            if o is None or not np.array_equal(o.v, want): bad += 1
    return C, D, bad

def T3(f):   # exact textbook counts for a generic polynomial of degree 1, 2, 3 on f bits (same recursion as eval_poly)
    t1 = t2 = t3 = 0
    for j in range(1, f + 1):
        t3 = t3 + t2 + (1 << (j - 1)); t2 = t2 + t1 + (1 << (j - 1)); t1 = t1 + (1 << (j - 1)) - (1 if j == 1 else 0) + (1 if j == 1 else 0)
    return t1, t2, t3

if __name__ == "__main__":
    mode = sys.argv[1]; Lr, s, t, extra = map(int, sys.argv[2:6])
    T = Tower(Lr, s, t, extra); t0 = time.time()
    P1 = 1 << T.m
    P2 = sum((1 << T.m) >> (s if c < Lr else 0) for c in range(1 << t))
    head = "tower: %d real colours of %d, atoms of %d bits, %d extra bits: y has %d bits, k = %d, N = %d, classes %d = %.4f N" % (
        Lr, 1 << t, s, extra, T.m, T.k, T.N, P1 + P2, (P1 + P2) / T.N)
    if mode == "good":
        dmax = int(sys.argv[6])
        print(head, flush=True)
        for d in range(2, dmax + 1):
            g = good(T, d)
            print("   degree <= %d : good %s  classes counted %d  components %s   (%.0f s)" % (d, g[0], g[1], g[2], time.time() - t0), flush=True)
    elif mode in ("build", "count"):
        C, D, bad = build(T, replay=(mode == "build"))
        print(head)
        print("   coefficients containing a bit of the forgotten atom, formed and found to be the zero form: %d" % T.checked)
        print("   inputs %d ; gates (G) %d = %.4f N ; %s" % (D, C.gates, C.gates / T.N,
              ("outputs wrong on some unit input: %d of %d" % (bad, T.N)) if mode == "build" else "count only, nothing replayed"))
        for kk, vv in sorted(C.by.items(), key=lambda z: -z[1]): print("      %-45s %8d = %.4f N" % (kk, vv, vv / T.N))
        print("   textbook for degree 3 on k bits (same recursion): %d = %.4f N   (%.0f s)" % (T3(T.k)[2], T3(T.k)[2] / T.N, time.time() - t0), flush=True)
