# a-1: independent check of i-cross Hybrid 3 ("squares"). Own code, exact integer / rational arithmetic only.
# Model: a gate is a*u + b*v of two earlier values, any rational a, b; scalings of inputs and outputs are free; cost = gates.
import sys, itertools
from fractions import Fraction as Fr

def par(a): return bin(a).count("1") & 1
def sgn(a): return -1 if par(a) else 1

class Circ:
    def __init__(s, n): s.n = n; s.g = 0
    def inp(s, i): v = [0]*s.n; v[i] = 1; return v
    def gate(s, a, u, b, v): s.g += 1; return [a*x + b*y for x, y in zip(u, v)]

def wht(c, f, brick):
    """f: list of 2^d forms; returns out[e] = sum_x (-1)^(e.x) f[x], exactly. brick: use the 7-gate 4-point block on pairs of bits."""
    f = list(f); n = len(f); d = n.bit_length() - 1; i = 0
    while i < d:
        if brick and i + 1 < d:
            bi, bj = 1 << i, 1 << (i + 1)
            for e in range(n):
                if e & (bi | bj): continue
                x0, x1, x2, x3 = f[e], f[e | bi], f[e | bj], f[e | bi | bj]
                w1 = c.gate(1, x0, 1, x1); w2 = c.gate(1, x2, 1, x3)
                y0 = c.gate(1, w1, 1, w2); y2 = c.gate(1, w1, -1, w2)
                w3 = c.gate(2, x0, -1, y0); y3 = c.gate(1, w3, 2, x3); y1 = c.gate(1, w3, 2, x2)
                f[e], f[e | bi], f[e | bj], f[e | bi | bj] = y0, y1, y2, y3
            i += 2
        else:
            b = 1 << i
            for e in range(n):
                if e & b: continue
                u, v = f[e], f[e | b]
                f[e], f[e | b] = c.gate(1, u, 1, v), c.gate(1, u, -1, v)
            i += 1
    return f

def low(m): return (m & -m).bit_length() - 1
def squeeze(x, p):            # drop bit p of x
    return (x & ((1 << p) - 1)) | ((x >> (p + 1)) << p)
def spread(e, p):             # inverse of squeeze, bit p = 0
    return (e & ((1 << p) - 1)) | ((e >> p) << (p + 1))

def stage(c, q, sym0, symm, altm, brick, cnt):
    """One half of the middle. sym0[x] (x in 0..q-1), symm[m][e], altm[m][e] (m != 0, e in 0..q/2-1, rep x = spread(e, low(m))).
    Returns C[w][m] for all w, m: the block numbers. cnt collects gates of (sym part, alt part)."""
    C = [[None]*q for _ in range(q)]
    g0 = c.g
    t = wht(c, sym0, brick)
    for w in range(q): C[w][0] = t[w]
    for m in range(1, q):
        p = low(m)
        t = wht(c, symm[m], brick)
        for e in range(q // 2):
            w = spread(e, p)
            if par(w & m): w |= 1 << p          # make w.m = 0
            C[w][m] = t[e]
    cnt[0] += c.g - g0; g0 = c.g
    for m in range(1, q):
        p = low(m)
        t = wht(c, altm[m], brick)
        for e in range(q // 2):
            w = spread(e, p)
            if not par(w & m): w |= 1 << p      # make w.m = 1
            C[w][m] = t[e]
    cnt[1] += c.g - g0
    return C

def full(q, brick, verbose=True):
    """The whole q^2-point transform by the route: split, stage, (one number per block), stage, merge. Gate-by-gate replay."""
    N = q*q; c = Circ(N); F = [[c.inp(x*q + y) for y in range(q)] for x in range(q)]
    cnt_split = cnt_merge = 0; cs = [0, 0]
    g0 = c.g
    sym0 = [F[x][x] for x in range(q)]
    symm = {}; altm = {}
    for m in range(1, q):
        p = low(m); S = []; A = []
        for e in range(q // 2):
            x = spread(e, p); y = x ^ m
            S.append(c.gate(1, F[x][y], 1, F[y][x])); A.append(c.gate(1, F[x][y], -1, F[y][x]))
        symm[m] = S; altm[m] = A
    cnt_split = c.g - g0
    C = stage(c, q, sym0, symm, altm, brick, cs)
    # exact check of the block numbers: C[w][m] = sum_x (-1)^(w.x) F[x][x+m]
    for w in range(q):
        for m in range(q):
            want = [0]*N
            for x in range(q): want[x*q + (x ^ m)] = sgn(w & x)
            assert C[w][m] == want, ("block number", w, m)
    # second half: roles of (w, m) exchanged: for output-slice w, the numbers C[w][m] over m with w.m = 0 (sym) or 1 (alt)
    sym0 = [C[0][m] for m in range(q)]
    symw = {}; altw = {}
    for w in range(1, q):
        p = low(w); S = []; A = []
        for e in range(q // 2):
            m = spread(e, p)
            m0 = m | (1 << p) if par(m & w) else m          # m0.w = 0
            m1 = m if par(m & w) else m | (1 << p)          # m1.w = 1
            S.append(C[w][m0]); A.append(C[w][m1])
        symw[w] = S; altw[w] = A
    D = stage(c, q, sym0, symw, altw, brick, cs)      # D[v][w]
    g0 = c.g
    G = [[None]*q for _ in range(q)]
    for v in range(q): G[v][v] = D[v][0]
    for w in range(1, q):
        p = low(w)
        for e in range(q // 2):
            v = spread(e, p)
            So = D[v if not par(v & w) else v | (1 << p)][w]        # index with v'.w = 0, agrees with v off bit p
            Ao = D[v | (1 << p) if not par(v & w) else v][w]        # index with v'.w = 1
            a = c.gate(1, So, 1, Ao); b = c.gate(1, So, -1, Ao)
            # one of a, b is G[v^w][v], the other G[v][v^w]; decide by exact comparison below
            G[v ^ w][v], G[v][v ^ w] = a, b
    cnt_merge = c.g - g0
    # exact check against the Walsh-Hadamard matrix (free scaling per output; a swap inside a merged pair is a relabelling)
    ok = True; scales = set()
    def prop(form, u, v):
        k = None
        for x in range(q):
            for y in range(q):
                t = form[x*q + y] * sgn(u & x) * sgn(v & y)
                if k is None: k = t
                if t != k or t == 0: return None
        return k
    for u in range(q):
        for v in range(q):
            k = prop(G[u][v], u, v)
            if k is None:
                k = prop(G[u][v], v, u)       # the pair came out in the other order
                if k is None: ok = False
            scales.add(k)
    T = lambda n: 0 if n == 1 else (n*(n.bit_length()-1) if not brick else
                 (7*(n.bit_length()-1)*n//8 if (n.bit_length()-1) % 2 == 0 else 7*(n.bit_length()-2)*n//8 + n))
    formula = 2*(q*q - q) + 2*T(q) + 4*(q - 1)*T(q // 2)
    if verbose:
        print("q=%3d points=%5d brick=%d: gates=%6d = split %d + sym middle %d + alt middle %d + merge %d ; formula %d ; all %d outputs proportional to rows of H: %s ; output scales %s ; textbook %d ; brick-direct %d"
              % (q, N, brick, c.g, cnt_split, cs[0], cs[1], cnt_merge, formula, N, ok, sorted(scales), N*(N.bit_length()-1), 7*N*(N.bit_length()-1)//8))
    assert ok and c.g == formula
    return c.g

# ---------- the two squares as matrices, from the definition (2 x 2 minors and permanents of H) ----------
def squares(q):
    H = [[sgn(x & y) for y in range(q)] for x in range(q)]
    pairs = [(i, j) for i in range(q) for j in range(i + 1, q)]
    symc = [(i, i) for i in range(q)] + pairs
    A2 = [[H[a][i]*H[b][j] - H[a][j]*H[b][i] for (i, j) in pairs] for (a, b) in pairs]            # second compound matrix
    S2 = [[(H[a][i]*H[b][j] + H[a][j]*H[b][i]) if i != j else H[a][i]*H[b][i] for (i, j) in symc] for (a, b) in symc]
    return H, pairs, symc, A2, S2
def mm(A, B): return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]

def middle_alone(q, which, brick):
    """The middle of one square as a circuit on its own coordinates; compared with the matrix from the definition."""
    H, pairs, symc, A2, S2 = squares(q)
    coords = symc if which == "sym" else pairs
    M = S2 if which == "sym" else A2
    idx = {p: i for i, p in enumerate(coords)}
    c = Circ(len(coords)); zero = [0]*len(coords)
    sym0 = [c.inp(idx[(x, x)]) if which == "sym" else zero for x in range(q)]
    symm = {}; altm = {}
    for m in range(1, q):
        p = low(m); L = []
        for e in range(q // 2):
            x = spread(e, p); y = x ^ m
            v = c.inp(idx[(min(x, y), max(x, y))])
            if which == "alt" and x > y: v = [-t for t in v]         # free sign
            L.append(v)
        symm[m] = L if which == "sym" else None; altm[m] = L if which == "alt" else None
    # run only the relevant half-stages
    def half(s0, sm, am):
        C = {}
        if which == "sym":
            t = wht(c, s0, brick)
            for w in range(q): C[(w, 0)] = t[w]
        for m in range(1, q):
            p = low(m); t = wht(c, sm[m] if which == "sym" else am[m], brick)
            for e in range(q // 2):
                w = spread(e, p)
                if par(w & m) != (which == "alt"): w |= 1 << p
                C[(w, m)] = t[e]
        return C
    C = half(sym0, symm, altm)
    s0 = [C[(0, m)] for m in range(q)] if which == "sym" else None
    sw = {}
    for w in range(1, q):
        p = low(w); L = []
        for e in range(q // 2):
            m = spread(e, p)
            if par(m & w) != (which == "alt"): m |= 1 << p
            L.append(C[(w, m)])
        sw[w] = L
    D = half(s0, sw, sw)
    outs = list(D.values())
    def propto(o, r):
        k = [(x, y) for x, y in zip(o, r) if x or y]
        return bool(k) and all(x*k[0][1] == y*k[0][0] for x, y in k) and k[0][1] != 0 and k[0][0] != 0
    hit = [sum(1 for o in outs if propto(o, r)) for r in M]
    return c.g, all(h == 1 for h in hit), len(outs)

if __name__ == "__main__":
    q = 4
    H, pairs, symc, A2, S2 = squares(q)
    theirs_a = [[int(t) for t in l.split()] for l in open("../i-cross/rows_alt4.txt")]
    theirs_s = [[int(t) for t in l.split()] for l in open("../i-cross/rows_sym4.txt")]
    print("A2 (2 x 2 minors of H4) / 2 equals rows_alt4.txt:", [[v//2 for v in r] for r in A2] == theirs_a, "; entries:", sorted(set(v for r in A2 for v in r)))
    print("S2 (induced / permanent matrix) equals rows_sym4.txt:", S2 == theirs_s)
    I = lambda n, s: [[s*(i == j) for j in range(n)] for i in range(n)]
    print("A2^2 = 16 I:", mm(A2, A2) == I(6, 16), "; S2^2 = 16 I:", mm(S2, S2) == I(10, 16))
    # octahedron: support = complete tripartite K(2,2,2) after matching column slices to row slices
    sl = lambda pr: pr[0] ^ pr[1]
    supp_ok = all((A2[r][c] != 0) == (par(sl(pairs[r]) & sl(pairs[c])) == 1) for r in range(6) for c in range(6))
    print("A2 non-zero exactly when (u+v).(x+y) = 1:", supp_ok, "; row slice w misses column slice", {w: [m for m in (1, 2, 3) if not par(w & m)] for w in (1, 2, 3)})
    for which in ("alt", "sym"):
        for brick in (0, 1):
            g, ok, no = middle_alone(4, which, brick)
            print("middle alone q=4 %s brick=%d: %d gates, %d outputs, each row of the matrix produced exactly once (up to scale): %s" % (which, brick, g, no, ok))
    for which in ("alt", "sym"):
        for qq in (8, 16):
            g, ok, no = middle_alone(qq, which, 0)
            print("middle alone q=%d %s textbook slices: %d gates, %d outputs, rows produced: %s" % (qq, which, g, no, ok))
    for qq in (2, 4, 8, 16, 32):
        for brick in (0, 1):
            full(qq, brick)
    # Krawtchouk form: Lambda^2(H2 x H2) = Sym^2(H2) x Lambda^2(H2) + Lambda^2(H2) x Sym^2(H2) = -2 (K + K)
    # basis change: keep pairs (0,1),(2,3),(0,2),(1,3); replace (0,3),(1,2) by their sum and difference
    P = [[0]*6 for _ in range(6)]   # columns = new basis vectors in the pair basis
    ip = {p: i for i, p in enumerate(pairs)}
    newb = [{(0, 1): 1}, {(0, 3): 1, (1, 2): 1}, {(2, 3): 1}, {(0, 2): 1}, {(0, 3): 1, (1, 2): -1}, {(1, 3): 1}]
    for j, b in enumerate(newb):
        for pr, v in b.items(): P[ip[pr]][j] = v
    # solve P X = A2 P  exactly
    def solve(P, B):
        n = len(P); M = [[Fr(x) for x in P[i]] + [Fr(x) for x in B[i]] for i in range(n)]
        for col in range(n):
            piv = next(r for r in range(col, n) if M[r][col] != 0); M[col], M[piv] = M[piv], M[col]
            M[col] = [x / M[col][col] for x in M[col]]
            for r in range(n):
                if r != col and M[r][col] != 0: M[r] = [x - M[r][col]*y for x, y in zip(M[r], M[col])]
        return [row[n:] for row in M]
    X = solve(P, mm(A2, P))
    print("Lambda^2(H4) in the basis {01, 03+12, 23 | 02, 03-12, 13}:")
    for r in X: print("   ", [int(v) if v.denominator == 1 else str(v) for v in r])
