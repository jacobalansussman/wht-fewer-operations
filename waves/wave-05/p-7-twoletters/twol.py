# p-7-twoletters: products of two "letters" (sums of tree rectangles), count (G).
# A letter X (rows R, columns C) = sum over s of mu_s * (ar * 1_{A_s}) (cc * 1_{B_s})^T, A_s a node of a tree on the rows,
# B_s a node of a tree on the columns, ar and cc scalings. H = L1 L2, L2: inputs -> m middle wires, L1: middle -> outputs.
# The search for the numbers is a float integer programme (HiGHS): CANDIDATES ONLY. Every candidate is turned into a gate
# list by emit() and replayed with exact fractions on the basis vectors by replay(); only that count is reported as [ran].
import numpy as np, sys, time, random
from fractions import Fraction as Fr
from scipy.optimize import milp, LinearConstraint, Bounds
import scipy.sparse as sp

def Hmat(N): return np.array([[(-1) ** bin(a & x).count('1') for x in range(N)] for a in range(N)], dtype=float)

# ---------- trees: list of nodes; node = (tuple of leaves, child1 index or -1, child2 index or -1); leaves first
def tree_from_merges(n, merges):
    nodes = [((i,), -1, -1) for i in range(n)]
    for (p, q) in merges:
        nodes.append((tuple(sorted(nodes[p][0] + nodes[q][0])), p, q))
    return nodes
def random_tree(n, rng):
    live = list(range(n)); merges = []; nxt = n
    while len(live) > 1:
        p, q = rng.sample(live, 2); live.remove(p); live.remove(q); merges.append((p, q)); live.append(nxt); nxt += 1
    return tree_from_merges(n, merges)
def tree_from_sets(n, sets):
    # sets: list of tuples (internal nodes), must be laminar and binary; builds the node list
    sets = sorted(set(tuple(sorted(s)) for s in sets), key=len)
    nodes = [((i,), -1, -1) for i in range(n)]; idx = {(i,): i for i in range(n)}
    for s in sets:
        if len(s) == 1: continue
        # maximal already-built nodes inside s
        inside = [t for t in idx if set(t) <= set(s)]
        maxi = [t for t in inside if not any(set(t) < set(u) for u in inside)]
        while len(maxi) > 2:   # merge extra pieces greedily to stay binary
            a, b = maxi[0], maxi[1]; u = tuple(sorted(a + b)); nodes.append((u, idx[a], idx[b])); idx[u] = len(nodes) - 1
            maxi = [u] + maxi[2:]
        a, b = maxi; nodes.append((s, idx[a], idx[b])); idx[s] = len(nodes) - 1
    return nodes
def chain_tree(N, flag):
    # nodes = cosets of the subgroups of the flag (list of generators, cumulative), then the whole set
    sets = []; gens = []
    for g in flag:
        gens.append(g); V = {0}
        for h in gens: V |= {v ^ h for v in V}
        seen = set()
        for x in range(N):
            if x in seen: continue
            cs = tuple(sorted(x ^ v for v in V)); seen |= set(cs); sets.append(cs)
    sets.append(tuple(range(N)))
    return tree_from_sets(N, sets)
def ancestors(nodes):
    par = [-1] * len(nodes)
    for i, (s, a, b) in enumerate(nodes):
        if a >= 0: par[a] = i; par[b] = i
    anc = []
    for i in range(len(nodes)):
        l = []; j = par[i]
        while j >= 0: l.append(j); j = par[j]
        anc.append(l)
    return par, anc

# ---------- one letter by integer programme. Solve Left * X * Right = T with X a letter over (TR, ar, TC, cc).
def solve_letter(TR, ar, TC, cc, Left, Right, T, Mb=4.0, tl=20.0, allow=None, mode='nor'):
    nr, nc = len(ar), len(cc)
    rvecs = []; cvecs = []
    for (s, _, _) in TR:
        v = np.zeros(nr); v[list(s)] = ar[list(s)]; rvecs.append(Left @ v if Left is not None else v)
    for (s, _, _) in TC:
        v = np.zeros(nc); v[list(s)] = cc[list(s)]; cvecs.append(v @ Right if Right is not None else v)
    pairs = [(i, j) for i in range(len(TR)) for j in range(len(TC)) if (allow is None or allow(TR[i][0], TC[j][0]))]
    pairs = [(i, j) for (i, j) in pairs if np.any(rvecs[i]) and np.any(cvecs[j])]
    n = len(pairs)
    A = np.array([np.outer(rvecs[i], cvecs[j]).ravel() for (i, j) in pairs]).T
    b = T.ravel()
    intC = [j for j in range(len(TC)) if TC[j][1] >= 0]; ci = {j: t for t, j in enumerate(intC)}
    nR = len(TR); parR, ancR = ancestors(TR)
    # variables: mu (n) | z (n) | comp (len intC) | used (nR) | root (nR)
    o_z, o_c, o_u, o_r = n, 2 * n, 2 * n + len(intC), 2 * n + len(intC) + nR
    nv = o_r + nR
    rows = []; lo = []; hi = []
    def add(coefs, l, h): rows.append(coefs); lo.append(l); hi.append(h)
    Asp = sp.csr_matrix(A)
    cons = [LinearConstraint(sp.hstack([Asp, sp.csr_matrix((A.shape[0], nv - n))]), b, b)]
    for s in range(n):
        add({s: 1.0, o_z + s: -Mb}, -np.inf, 0.0); add({s: -1.0, o_z + s: -Mb}, -np.inf, 0.0)
        i, j = pairs[s]
        if j in ci: add({o_z + s: 1.0, o_c + ci[j]: -1.0}, -np.inf, 0.0)
        add({o_z + s: 1.0, o_u + i: -1.0}, -np.inf, 0.0)
    for j in intC:
        for ch in (TC[j][1], TC[j][2]):
            if ch in ci: add({o_c + ci[j]: 1.0, o_c + ci[ch]: -1.0}, -np.inf, 0.0)
    byrow = {}
    for s, (i, j) in enumerate(pairs): byrow.setdefault(i, []).append(s)
    for i in range(nR):
        d = {o_u + i: 1.0}
        for s in byrow.get(i, []): d[o_z + s] = -1.0
        add(d, -np.inf, 0.0)
        add({o_r + i: 1.0, o_u + i: -1.0}, -np.inf, 0.0)
        for a in ancR[i]: add({o_r + i: 1.0, o_u + a: 1.0}, -np.inf, 1.0)
    rr = []; cc_ = []; vv = []
    for t, d in enumerate(rows):
        for k_, v in d.items(): rr.append(t); cc_.append(k_); vv.append(v)
    cons.append(LinearConstraint(sp.csr_matrix((vv, (rr, cc_)), shape=(len(rows), nv)), np.array(lo), np.array(hi)))
    c = np.zeros(nv); c[o_z:o_z + n] = 1.0
    if mode != 'tau': c[o_c:o_c + len(intC)] = 1.0
    if mode == 'full': c[o_r:] = -1.0
    integ = np.ones(nv); integ[:n] = 0
    lb = np.zeros(nv); ub = np.ones(nv); lb[:n] = -Mb; ub[:n] = Mb
    r = milp(c, constraints=cons, integrality=integ, bounds=Bounds(lb, ub), options={'time_limit': tl})
    if r.x is None: return None
    rect = [(pairs[s][0], pairs[s][1], Fr(float(r.x[s])).limit_denominator(64)) for s in range(n) if abs(r.x[s]) > 1e-6]
    return dict(cost=int(round(r.fun)), rect=rect, status=r.status, bound=getattr(r, 'mip_dual_bound', None))

# ---------- exact gate list from a letter. handles: (scale Fraction, wire id or None for zero)
class Prog:
    def __init__(self, n_in):
        self.vec = [[Fr(int(i == j)) for j in range(n_in)] for i in range(n_in)]; self.gates = []; self.n_in = n_in
    def gate(self, a, u, b, v):
        self.gates.append((a, u, b, v)); self.vec.append([a * p + b * q for p, q in zip(self.vec[u], self.vec[v])])
        return len(self.vec) - 1
    def add(self, h1, h2):   # handles
        if h1 is None: return h2
        if h2 is None: return h1
        return (Fr(1), self.gate(h1[0], h1[1], h2[0], h2[1]))
def emit(prog, TR, ar, TC, cc, rect, inh):
    form = {}
    def cform(j):
        if j in form: return form[j]
        s, a, b = TC[j]
        if a < 0:
            h = inh[s[0]]; form[j] = None if h is None else (h[0] * Fr(cc[s[0]]).limit_denominator(64), h[1])
        else: form[j] = prog.add(cform(a), cform(b))
        return form[j]
    val = {}
    for (i, j, mu) in rect:
        f = cform(j)
        if f is None: continue
        val.setdefault(i, []).append((mu * f[0], f[1]))
    par, anc = ancestors(TR); stream = {}
    def st(i):
        if i in stream: return stream[i]
        h = st(par[i]) if par[i] >= 0 else None
        for t in val.get(i, []): h = prog.add(h, t)
        stream[i] = h; return h
    out = []
    for i in range(len(ar)):
        h = st(i); out.append(None if h is None else (h[0] * Fr(ar[i]).limit_denominator(64), h[1]))
    return out
def replay(N, L2d, L1d):
    # L2d = (TR (wires), ar, TC (inputs), cc, rect), L1d = (TR (outputs), ar, TC (wires), cc, rect); returns gates, ok, scales
    prog = Prog(N); inh = [(Fr(1), i) for i in range(N)]
    mid = emit(prog, *L2d, inh); g2 = len(prog.gates)
    out = emit(prog, *L1d, mid)
    ok = True; scales = []
    for y in range(N):
        if out[y] is None: ok = False; continue
        v = [out[y][0] * t for t in prog.vec[out[y][1]]]
        tgt = [(-1) ** bin(y & x).count('1') for x in range(N)]
        if v != tgt: ok = False
        scales.append(out[y][0])
    return len(prog.gates), g2, ok, prog, mid
def letter_matrix(TR, ar, TC, cc, rect):
    X = np.zeros((len(ar), len(cc)))
    for (i, j, mu) in rect:
        X[np.ix_(list(TR[i][0]), list(TC[j][0]))] += float(mu) * np.outer(ar[list(TR[i][0])], cc[list(TC[j][0])])
    return X
def wires_matrix(prog, mid, N):
    return np.array([[0.0] * N if h is None else [float(h[0] * t) for t in prog.vec[h[1]]] for h in mid])
