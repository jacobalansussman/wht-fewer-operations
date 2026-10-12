# e-6-shifts: the collapser.
# A program for the 16-point Walsh-Hadamard transform is a list of gates  w = a*u + b*v  (exact Gaussian rationals).
# An "embedding" writes 4 unknowns x_0..x_3 into the 16 inputs (fan-out, zeros, free scalings).
# Collapse: every wire becomes a linear form in x; forms equal up to a scalar are ONE node; a gate whose result is
# proportional to one of its arguments (or is zero) costs nothing; then find the fewest nodes that still derive the
# four wanted outputs (rows of H4).
#   strict : a node may only be derived the way some gate of the big program derived it
#   pool   : a node may be derived from ANY two available nodes that span it (the big program only suggests helpers)
# Count (G): one gate = any a*u + b*v, scalings free.  All arithmetic exact (Fractions); no floating point.
import sys, itertools
from fractions import Fraction as Fr

class G:
    __slots__ = ("a", "b")
    def __init__(s, a=0, b=0): s.a = Fr(a); s.b = Fr(b)
    def __add__(s, o): return G(s.a + o.a, s.b + o.b)
    def __sub__(s, o): return G(s.a - o.a, s.b - o.b)
    def __mul__(s, o): return G(s.a * o.a - s.b * o.b, s.a * o.b + s.b * o.a)
    def __neg__(s): return G(-s.a, -s.b)
    def inv(s):
        d = s.a * s.a + s.b * s.b; return G(s.a / d, -s.b / d)
    def z(s): return s.a == 0 and s.b == 0
    def key(s): return (s.a, s.b)
    def __repr__(s):
        if s.b == 0: return str(s.a)
        if s.a == 0: return "%si" % s.b
        return "(%s%+si)" % (s.a, s.b)
ONE = G(1); ZERO = G(0); I = G(0, 1)
def gi(k):  # i^k
    return [G(1), G(0, 1), G(-1), G(0, -1)][k % 4]
pc = lambda x: bin(x).count("1")

class Prog:
    def __init__(s, n):
        s.n = n; s.gates = []; s.out = {}
    def gate(s, a, u, b, v):
        s.gates.append((a if isinstance(a, G) else G(a), u, b if isinstance(b, G) else G(b), v)); return s.n + len(s.gates) - 1
    def scale(s, a, u):
        s.gates.append((a if isinstance(a, G) else G(a), u, None, None)); return s.n + len(s.gates) - 1
    def ngates(s): return sum(1 for g in s.gates if g[3] is not None)

def evaluate(prog, inputs):
    vals = [list(v) for v in inputs]
    for (a, u, b, v) in prog.gates:
        if v is None: vals.append([a * t for t in vals[u]])
        else: vals.append([a * t + b * w for t, w in zip(vals[u], vals[v])])
    return vals
def nkey(v):
    for t in v:
        if not t.z():
            iv = t.inv(); return tuple((w * iv).key() for w in v)
    return None
def unit(n, j): return [ONE if i == j else ZERO for i in range(n)]

def Hrow(k, w): return [G(1 - 2 * (pc(w & s) & 1)) for s in range(1 << k)]

def verify16(prog):
    vals = evaluate(prog, [unit(16, j) for j in range(16)])
    for P in range(16):
        if nkey(vals[prog.out[P]]) != nkey(Hrow(4, P)): return False
    return True

# ---------- span tests in exact Gaussian rationals ----------
def rank_le2(f, g, h):
    # is f in span(g, h) for independent g, h (vectors of G)?  eliminate exactly
    rows = [list(g), list(h), list(f)]
    n = len(f); r = 0
    for c in range(n):
        p = next((i for i in range(r, 3) if not rows[i][c].z()), None)
        if p is None: continue
        rows[r], rows[p] = rows[p], rows[r]
        iv = rows[r][c].inv()
        for i in range(3):
            if i != r and not rows[i][c].z():
                m = rows[i][c] * iv
                rows[i] = [x - m * y for x, y in zip(rows[i], rows[r])]
        r += 1
        if r == 3: return False
    return True

def collapse(prog, E, wanted_rows, maxh_strict=4, maxh_pool=3, want_sets=False):
    N = len(E[0])
    vals = evaluate(prog, E)
    ids = {}; vecs = []
    def cid(v):
        k = nkey(v)
        if k is None: return None
        if k not in ids: ids[k] = len(vecs); vecs.append([G(a, b) for (a, b) in k])
        return ids[k]
    inp = [cid(unit(N, j)) for j in range(N)]
    want = [cid(r) for r in wanted_rows]
    wid = [cid(v) for v in vals]
    deriv = {}
    for gi_, (a, u, b, v) in enumerate(prog.gates):
        if v is None: continue
        o = wid[prog.n + gi_]; cu = wid[u]; cv = wid[v]
        if o is None or cu is None or cv is None or a.z() or b.z(): continue
        if cu == cv or o == cu or o == cv: continue
        deriv.setdefault(o, set()).add((min(cu, cv), max(cu, cv)))
    # are the wanted classes produced at all?
    produced = set(wid) - {None}
    ok = all(w in produced for w in want)
    m = len(vecs)
    base = set(inp)
    wantset = [w for w in want if w not in base]
    cand = [c for c in range(m) if c not in base and c not in wantset and c in produced]
    res = {"classes": m, "produced_ok": ok, "live_gates": sum(len(v) for v in deriv.values())}
    # strict search
    def closure_strict(nodes):
        avail = set(base); todo = set(nodes); ch = True
        while ch and todo:
            ch = False
            for f in list(todo):
                for (g, h) in deriv.get(f, ()):
                    if g in avail and h in avail:
                        avail.add(f); todo.discard(f); ch = True; break
        return not todo
    scand = [c for c in cand if c in deriv]
    res["strict"] = None; res["strict_sets"] = []
    for sz in range(0, maxh_strict + 1):
        found = []
        for hs in itertools.combinations(scand, sz):
            if closure_strict(list(hs) + wantset):
                found.append(hs)
                if not want_sets: break
        if found:
            res["strict"] = len(wantset) + sz; res["strict_sets"] = found; break
    # pool search
    memo = {}
    def inspan(f, g, h):
        k = (f, g, h)
        if k not in memo: memo[k] = rank_le2(vecs[f], vecs[g], vecs[h])
        return memo[k]
    def closure_pool(nodes):
        avail = list(base); todo = list(nodes); ch = True
        while ch and todo:
            ch = False
            for f in list(todo):
                hit = False
                for i in range(len(avail)):
                    for j in range(i + 1, len(avail)):
                        if inspan(f, avail[i], avail[j]): hit = True; break
                    if hit: break
                if hit: avail.append(f); todo.remove(f); ch = True
        return not todo
    res["pool"] = None; res["pool_sets"] = []
    if maxh_pool is not None:
        for sz in range(0, maxh_pool + 1):
            found = []
            for hs in itertools.combinations(cand, sz):
                if closure_pool(list(hs) + wantset):
                    found.append(hs)
                    if not want_sets: break
            if found:
                res["pool"] = len(wantset) + sz; res["pool_sets"] = found; break
    res["vecs"] = vecs; res["cand"] = cand; res["want"] = wantset
    return res

def show(v):
    return "(" + ",".join(repr(t) for t in v) + ")"

# ---------- embeddings of 4 unknowns into 16 inputs ----------
def subspaces2():
    out = set()
    for a in range(1, 16):
        for b in range(a + 1, 16):
            out.add(frozenset([0, a, b, a ^ b]))
    return sorted(sorted(s) for s in out)
def perp(K):
    return [P for P in range(16) if all(pc(P & k) % 2 == 0 for k in K)]
def basis2(S):
    nz = [s for s in S if s]; return nz[0], nz[1]
def emb_pullback(K):
    # x lives on the 4 cosets of K (fan-out: every coset member carries the same x); answer sits on K-perp
    P1, P2 = basis2(perp(K))
    E = [unit(4, (pc(P1 & p) & 1) + 2 * (pc(P2 & p) & 1)) for p in range(16)]
    outs = {0: 0, P1: 1, P2: 2, P1 ^ P2: 3}     # position -> row of H4
    return E, outs
def emb_sparse(K):
    # x sits on the 4 points of K, zero elsewhere; every output is a row of H4
    k1, k2 = basis2(K)
    pos = {0: 0, k1: 1, k2: 2, k1 ^ k2: 3}
    E = [unit(4, pos[p]) if p in pos else [ZERO] * 4 for p in range(16)]
    outs = {P: (pc(P & k1) & 1) + 2 * (pc(P & k2) & 1) for P in range(16)}
    return E, outs

# ---------- 16-point programs ----------
def textbook(order=(1, 2, 4, 8)):
    p = Prog(16); w = list(range(16))
    for bit in order:
        for q in range(16):
            if q & bit: continue
            a, b = w[q], w[q | bit]
            w[q] = p.gate(1, a, 1, b); w[q | bit] = p.gate(1, a, -1, b)
    p.out = {P: w[P] for P in range(16)}; return p

def h4_seven(p, x, variant=0):
    # 7 gates: T = -x0 + x1 + x2 + x3 (3 gates), then T + 2x0, -T + 2x2, -T + 2x1, -T + 2x3
    if variant == 0:
        g1 = p.gate(-1, x[0], 1, x[1]); g2 = p.gate(1, x[2], 1, x[3]); T = p.gate(1, g1, 1, g2)
    elif variant == 1:
        g1 = p.gate(-1, x[0], 1, x[2]); g2 = p.gate(1, x[1], 1, x[3]); T = p.gate(1, g1, 1, g2)
    elif variant == 2:
        g1 = p.gate(1, x[1], 1, x[2]); g2 = p.gate(1, g1, 1, x[3]); T = p.gate(-1, x[0], 1, g2)
    else:
        g1 = p.gate(-1, x[0], 1, x[3]); g2 = p.gate(1, x[1], 1, x[2]); T = p.gate(1, g1, 1, g2)
    return [p.gate(1, T, 2, x[0]), p.gate(-1, T, 2, x[2]), p.gate(-1, T, 2, x[1]), p.gate(-1, T, 2, x[3])]
def h4_text(p, x):
    a = p.gate(1, x[0], 1, x[1]); b = p.gate(1, x[0], -1, x[1]); c = p.gate(1, x[2], 1, x[3]); d = p.gate(1, x[2], -1, x[3])
    return [p.gate(1, a, 1, c), p.gate(1, b, 1, d), p.gate(1, a, -1, c), p.gate(1, b, -1, d)]
def twopass(rowvariants=(0, 0, 0, 0), colvariants=(0, 0, 0, 0)):
    # index p = a + 4*b ; first pass over a for each b, second over b for each a
    p = Prog(16); w = list(range(16))
    for b in range(4):
        o = h4_seven(p, [w[a + 4 * b] for a in range(4)], rowvariants[b])
        for a in range(4): w[a + 4 * b] = o[a]
    for a in range(4):
        o = h4_seven(p, [w[a + 4 * b] for b in range(4)], colvariants[a])
        for b in range(4): w[a + 4 * b] = o[b]
    p.out = {P: w[P] for P in range(16)}; return p

def find_j2i():
    # H4[w][s] = d1[w] * B[perm[w]][s] * d2[s]  with B = J - 2I
    H = [[1 - 2 * (pc(w & s) & 1) for s in range(4)] for w in range(4)]
    B = [[(-1 if i == j else 1) for j in range(4)] for i in range(4)]
    for perm in itertools.permutations(range(4)):
        for d2 in itertools.product((1, -1), repeat=4):
            ok = True; d1 = []
            for w in range(4):
                r = [B[perm[w]][s] * d2[s] for s in range(4)]
                if r == H[w]: d1.append(1)
                elif [-t for t in r] == H[w]: d1.append(-1)
                else: ok = False; break
            if ok: return perm, d1, list(d2)
def rook(tree=False):
    perm, d1, d2 = find_j2i()
    p = Prog(16)
    x = [[p.scale(d2[a] * d2[b], a + 4 * b) for b in range(4)] for a in range(4)]   # x[a][b]
    def chain(ws):
        if tree:
            return p.gate(1, p.gate(1, ws[0], 1, ws[1]), 1, p.gate(1, ws[2], 1, ws[3]))
        s = p.gate(1, ws[0], 1, ws[1]); s = p.gate(1, s, 1, ws[2]); return p.gate(1, s, 1, ws[3])
    r = [chain([x[a][b] for b in range(4)]) for a in range(4)]
    c = [chain([x[a][b] for a in range(4)]) for b in range(4)]
    t = chain(r)
    m = [p.gate(1, t, -2, r[a]) for a in range(4)]
    o = [[p.gate(1, p.gate(1, m[a], -2, c[b]), 4, x[a][b]) for b in range(4)] for a in range(4)]
    for w1 in range(4):
        for w2 in range(4):
            p.out[w1 + 4 * w2] = p.scale(d1[w1] * d1[w2], o[perm[w1]][perm[w2]])
    return p

def clebsch(pairing=0):
    S = [1, 2, 4, 8, 15]
    q = lambda s: 1 if (s == 0 or s in S) else 0
    # q(y+z) = q(y) + q(z) + B(y,z) ; B(y, z) = y . (Bm z)
    def Bf(y, z): return (q(y ^ z) + q(y) + q(z) + 1) % 2
    # find the linear map Bm with Bf(y,z) = parity(y & Bm(z))
    Bm = {}
    for z in range(16):
        Bm[z] = next(t for t in range(16) if all(Bf(y, z) == (pc(y & t) & 1) for y in range(16)))
    Binv = {v: k for k, v in Bm.items()}
    assert len(Binv) == 16
    p = Prog(16)
    # H16[y][z'] = (-1)^q(y) * M[y][z] * (-1)^q(z), z = Binv[z']
    inm = [None] * 16
    for zp in range(16):
        z = Binv[zp]; inm[z] = p.scale(1 - 2 * q(z), zp)
    def tree(ws):
        while len(ws) > 1:
            ws = [p.gate(1, ws[i], 1, ws[i + 1]) for i in range(0, len(ws) - 1, 2)] + ([ws[-1]] if len(ws) % 2 else [])
        return ws[0]
    T = tree(list(inm))
    pairs = [[(0, 15), (1, 2), (4, 8)], [(0, 15), (1, 4), (2, 8)], [(0, 15), (1, 8), (2, 4)], [(0, 1), (2, 4), (8, 15)]][pairing]
    cache = {}
    def pr(a, b):
        k = (min(a, b), max(a, b))
        if k not in cache: cache[k] = p.gate(1, inm[a], 1, inm[b])
        return cache[k]
    for y in range(16):
        ws = [pr(y ^ a, y ^ b) for (a, b) in pairs]
        nsum = p.gate(1, p.gate(1, ws[0], 1, ws[1]), 1, ws[2])
        o = p.gate(1, T, -2, nsum)
        p.out[y] = p.scale(1 - 2 * q(y), o)
    return p

# ---------- flag multipliers ----------
def flags(k):
    n = 1 << k; out = set()
    def rec(chain):
        W = chain[-1]
        if len(W) == n: out.add(tuple(chain)); return
        seen = set()
        for v in range(1, n):
            if v in W: continue
            W2 = frozenset(W | {w ^ v for w in W})
            if W2 in seen: continue
            seen.add(W2); rec(chain + [W2])
    rec([frozenset([0])])
    return sorted([sorted(W) for W in c] for c in out)
def level(chain, n):
    return [next(j for j, W in enumerate(chain) if y in W) for y in range(n)]
def mod4_solve(LA, LB, k):
    n = 1 << k; val = {}; adj = {}
    for y in range(n):
        a, b, w = ("A", LA[y]), ("B", LB[y]), pc(y) % 4
        adj.setdefault(a, []).append((b, w)); adj.setdefault(b, []).append((a, w))
    for s in sorted(adj):
        if s in val: continue
        val[s] = 0; st = [s]
        while st:
            u = st.pop()
            for (v, w) in adj[u]:
                want = (w - val[u]) % 4
                if v not in val: val[v] = want; st.append(v)
                elif val[v] != want: return None
    return val
def flag_mult(p, win, chain, c):
    # operator with spectrum c[level(y)], c a list of G of length k+1; win = 16 wire ids; returns 16 wire ids
    k = len(chain) - 1; n = 1 << k
    V = [[v for v in range(n) if all(pc(v & y) % 2 == 0 for y in W)] for W in chain]   # V_j = W_j-perp, shrinking
    rep = [[min(z ^ v for v in V[j]) for z in range(n)] for j in range(k + 1)]
    S = [None] * (k + 1)
    S[k] = {z: win[z] for z in range(n)}
    for j in range(k - 1, -1, -1):
        S[j] = {}
        for r in sorted(set(rep[j])):
            kids = sorted(set(rep[j + 1][z] for z in range(n) if rep[j][z] == r))
            S[j][r] = p.gate(1, S[j + 1][kids[0]], 1, S[j + 1][kids[1]])
    gam = [(c[j] - (c[j + 1] if j < k else ZERO)) * G(Fr(1, len(V[j]))) for j in range(k + 1)]
    R = {rep[0][0]: p.scale(gam[0], S[0][rep[0][0]])}
    for j in range(1, k + 1):
        R2 = {}
        for r in sorted(set(rep[j])):
            R2[r] = p.gate(1, R[rep[j - 1][r]], gam[j], S[j][r])
        R = R2
    return [R[z] for z in range(n)]
def twoflag(chA, chB, first="B"):
    LA, LB = level(chA, 16), level(chB, 16)
    val = mod4_solve(LA, LB, 4)
    if val is None: return None
    cA = [gi(val.get(("A", j), 0)) for j in range(5)]; cB = [gi(val.get(("B", j), 0)) for j in range(5)]
    p = Prog(16)
    w = [p.scale(gi(pc(z)), z) for z in range(16)]
    if first == "B":
        w = flag_mult(p, w, chB, cB); w = flag_mult(p, w, chA, cA)
    else:
        w = flag_mult(p, w, chA, cA); w = flag_mult(p, w, chB, cB)
    p.out = {y: p.scale(gi(pc(y)), w[y]) for y in range(16)}
    return p

H4rows = [Hrow(2, w) for w in range(4)]
def run_one(name, prog, embs, verbose=True, want_sets=False):
    ok = verify16(prog)
    line = "%-34s gates(G)=%3d  computes H16: %s" % (name, prog.ngates(), ok)
    out = []
    for (ename, E, outs) in embs:
        # check the embedding: the wanted outputs really are the rows of H4
        vals = evaluate(prog, E)
        good = all(nkey(vals[prog.out[P]]) == nkey(H4rows[w]) for P, w in outs.items())
        r = collapse(prog, E, H4rows, want_sets=want_sets)
        out.append((ename, good, r))
    return line, out

if __name__ == "__main__":
    mode = sys.argv[1]
    Ks = subspaces2()
    DIAG = [0, 5, 10, 15]
    if mode == "basic":
        embs = [("shift(diag)",) + emb_pullback(DIAG), ("sparse(diag)",) + emb_sparse(DIAG)]
        progs = [("textbook 1,2,4,8", textbook()), ("textbook 1,4,2,8", textbook((1, 4, 2, 8))),
                 ("two-pass 7x7 (56)", twopass()), ("two-pass mixed variants", twopass((0, 1, 2, 3), (3, 2, 1, 0))),
                 ("rook chain (63)", rook(False)), ("rook tree (63)", rook(True))] + \
                [("clebsch pairing %d" % i, clebsch(i)) for i in range(4)]
        for name, pg in progs:
            line, out = run_one(name, pg, embs, want_sets=True)
            print(line)
            for (ename, good, r) in out:
                print("    %-14s embedding ok=%s classes=%2d strict=%s (%d sets) pool=%s (%d sets)" % (
                    ename, good, r["classes"], r["strict"], len(r["strict_sets"]), r["pool"], len(r["pool_sets"])))
                for hs in r["strict_sets"][:3]:
                    print("        strict helpers:", " ".join(show(r["vecs"][h]) for h in hs))
            sys.stdout.flush()
    if mode == "allK":
        # every 2-dimensional subgroup K, both embeddings, on the non-product programs
        progs = [("textbook", textbook()), ("two-pass 7x7", twopass()), ("rook chain", rook(False)), ("rook tree", rook(True))] + \
                [("clebsch %d" % i, clebsch(i)) for i in range(4)]
        for name, pg in progs:
            print(name, "gates", pg.ngates(), "ok", verify16(pg)); hist = {}
            for K in Ks:
                for kind, f in (("pull", emb_pullback), ("sparse", emb_sparse)):
                    E, outs = f(K)
                    r = collapse(pg, E, H4rows, maxh_strict=4, maxh_pool=3)
                    hist.setdefault((kind, r["strict"], r["pool"]), []).append((K, r["classes"]))
            for k in sorted(hist, key=str):
                print("   %-6s strict=%s pool=%s : %d subgroups, classes %s, e.g. K=%s" % (
                    k[0], k[1], k[2], len(hist[k]), sorted(set(c for _, c in hist[k])), hist[k][0][0]))
            sys.stdout.flush()
    if mode == "flags":
        FL = flags(4); LV = [level(c, 16) for c in FL]
        pairs = [(i, j) for i in range(len(FL)) for j in range(i + 1, len(FL)) if mod4_solve(LV[i], LV[j], 4) is not None]
        print("two-flag pairs modulo 4:", len(pairs))
        which = sys.argv[2] if len(sys.argv) > 2 else "diag"
        tot = {}
        for (i, j) in pairs:
            for first in ("B", "A"):
                pg = twoflag(FL[i], FL[j], first)
                ok = verify16(pg)
                if which == "diag":
                    Elist = [("pull", DIAG), ("sparse", DIAG)]
                else:
                    Elist = [(kind, K) for K in Ks for kind in ("pull", "sparse")]
                best = {}
                for kind, K in Elist:
                    E, outs = (emb_pullback if kind == "pull" else emb_sparse)(K)
                    r = collapse(pg, E, H4rows, maxh_strict=4, maxh_pool=3)
                    key = (kind, r["strict"], r["pool"])
                    best.setdefault(key, []).append((K, r["classes"]))
                    tot[key] = tot.get(key, 0) + 1
                    if r["strict"] is not None and r["strict"] <= 7:
                        print("   STRICT<=7:", i, j, first, kind, K, r["strict"], [show(r["vecs"][h]) for h in r["strict_sets"][0]])
                    if r["pool"] is not None and r["pool"] <= 7:
                        hs = r["pool_sets"][0]
                        cx = any(any(t.b != 0 for t in r["vecs"][h]) for h in hs)
                        if cx or r["pool"] < 7:
                            print("   POOL %d complex=%s:" % (r["pool"], cx), i, j, first, kind, K, [show(r["vecs"][h]) for h in hs])
                print("pair %3d %3d first=%s gates=%d H16 ok=%s :" % (i, j, first, pg.ngates(), ok),
                      "; ".join("%s strict=%s pool=%s x%d (classes %s)" % (k[0], k[1], k[2], len(v), sorted(set(c for _, c in v))) for k, v in sorted(best.items(), key=str)))
                sys.stdout.flush()
        print("TOTAL", sorted(tot.items(), key=str))
