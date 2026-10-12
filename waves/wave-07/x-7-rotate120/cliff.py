# x-7-rotate120 / cliff.py : census of the "stabilizer" mirrors of R = D H / sqrt(N) at 4, 16 (all) and 64 points (sample).
# A stabilizer (Clifford) matrix sends every Pauli matrix X^a Z^b to another one, up to sign, under U P U^-1; it is described
# by a 2k x 2k matrix of bits (its action on the labels (a, b)).  Its rows all have the same number 2^j of non-zeros, where
# j = rank of the a-parts of the images of the Z-type labels.  Up to free maps (signs, relabellings) it is N / 2^j copies
# of the 2^j-point transform.
# Mirrors: bit matrices t with t^2 = 1 and t M t = M^-1, M the bit matrix of R.  For each: (j of S, j of S R, j of S R^2).
# Exact: the bit matrices of R and D are computed from the actual integer matrices at 4 and 16 points.
import sys, random, collections, itertools
def pop(v): return bin(v).count('1')
def build(n):
    k = 2 * n; N = 1 << k
    Q = lambda x: sum(((x >> (2 * i)) & 1) * ((x >> (2 * i + 1)) & 1) for i in range(n)) & 1
    sw = lambda x: sum((((x >> (2 * i)) & 1) << (2 * i + 1)) | (((x >> (2 * i + 1)) & 1) << (2 * i)) for i in range(n))
    H = [[(-1) ** pop(x & sw(y)) for y in range(N)] for x in range(N)]
    D = [(-1) ** Q(x) for x in range(N)]
    return k, N, H, D
def mul(A, B):
    Bt = list(zip(*B)); return [[sum(a * b for a, b in zip(r, c)) for c in Bt] for r in A]
def pauli(k, a, b):
    N = 1 << k
    return [[((-1) ** pop(b & y)) if x == (y ^ a) else 0 for y in range(N)] for x in range(N)]
def identify(k, Mx, scale):
    # Mx = +- scale * X^a Z^b ; return label a | b<<k
    N = 1 << k
    a = next(y for y in range(N) if Mx[0][y])          # row 0 non-zero at column y = 0 ^ a
    s0 = Mx[a][0]                                       # entry (x = a, y = 0) = sign * (-1)^(b.0) = sign
    assert abs(s0) == scale
    b = 0
    for i in range(k):
        y = 1 << i
        e = Mx[y ^ a][y]
        assert abs(e) == scale
        if e != s0: b |= 1 << i
    P = pauli(k, a, b); sg = s0 // scale
    assert all(Mx[x][y] == sg * scale * P[x][y] for x in range(N) for y in range(N)), 'not a Pauli'
    return a | (b << k)
def bitmat_of(k, U, Uinv, scale):
    # images of X_0..X_{k-1}, Z_0..Z_{k-1} under P -> U P Uinv ; U Uinv = scale * identity
    out = []
    for i in range(2 * k):
        a = (1 << i) if i < k else 0; b = (1 << (i - k)) if i >= k else 0
        out.append(identify(k, mul(mul(U, pauli(k, a, b)), Uinv), scale))
    return tuple(out)
def app(t, v):
    r = 0; i = 0
    while v:
        if v & 1: r ^= t[i]
        v >>= 1; i += 1
    return r
def comp(s, t): return tuple(app(s, x) for x in t)        # s after t
def ident(k): return tuple(1 << i for i in range(2 * k))
def inv(t, k):
    # brute inverse by Gaussian elimination over bits
    n = 2 * k; rows = [(t[i], 1 << i) for i in range(n)]   # image, source
    res = [0] * n
    rows = list(rows)
    for c in range(n):
        p = next(i for i in range(c, n) if (rows[i][0] >> c) & 1)
        rows[c], rows[p] = rows[p], rows[c]
        for i in range(n):
            if i != c and (rows[i][0] >> c) & 1: rows[i] = (rows[i][0] ^ rows[c][0], rows[i][1] ^ rows[c][1])
    # now rows[c] = (e_c, source combo) : t(source) = e_c
    return tuple(rows[c][1] for c in range(n))
def rk(vs):
    vs = list(vs); r = 0
    for c in range(64):
        p = next((i for i in range(r, len(vs)) if (vs[i] >> c) & 1), None)
        if p is None: continue
        vs[r], vs[p] = vs[p], vs[r]
        for i in range(len(vs)):
            if i != r and (vs[i] >> c) & 1: vs[i] ^= vs[r]
        r += 1
    return r
def jrank(t, k):
    mask = (1 << k) - 1
    return rk([t[i] & mask for i in range(k, 2 * k)])
def omega(u, v, k):
    mask = (1 << k) - 1
    return (pop((u & mask) & (v >> k)) + pop((u >> k) & (v & mask))) & 1
def direct_sum(t, k, copies):
    # label layout: X bits 0..K-1, Z bits K..2K-1 with K = k*copies ; block c uses X bits c*k.., Z bits K + c*k..
    K = k * copies; out = [0] * (2 * K); mask = (1 << k) - 1
    for c in range(copies):
        for i in range(2 * k):
            img = t[i]; a = img & mask; b = img >> k
            src = (c * k + i) if i < k else (K + c * k + (i - k))
            out[src] = (a << (c * k)) | (b << (K + c * k))
    return tuple(out)
# ---- exact bit matrices at 4 and 16 points
bm = {}
for n in (1, 2):
    k, N, H, D = build(n)
    Dm = [[D[x] if x == y else 0 for y in range(N)] for x in range(N)]
    DH = mul(Dm, H); HD = mul(H, Dm)            # R = DH / sqrtN, R^-1 = HD / sqrtN ; DH * HD = N
    M = bitmat_of(k, DH, HD, N); tD = bitmat_of(k, Dm, Dm, 1); tH = bitmat_of(k, H, H, N)
    bm[n] = (M, tD, tH)
    assert comp(M, comp(M, M)) == ident(k) and comp(tD, tD) == ident(k) and comp(comp(tD, M), tD) == comp(M, M)
    assert all(app(M, v) != v for v in range(1, 1 << (2 * k))), 'M has a fixed label'
    print('N=%d: bit matrix of R has order 3, no fixed label; D inverts it; j(D)=%d j(H)=%d j(D R^2)=%d' % (N, jrank(tD, k), jrank(comp(tD, M), k), jrank(comp(tD, comp(M, M)), k)))
assert bm[2][0] == direct_sum(bm[1][0], 2, 2) and bm[2][1] == direct_sum(bm[1][1], 2, 2), 'tensor layout'
print('16-point bit matrices = two copies of the 4-point ones (same layout): True')
def census(n, sample=None, seed=1):
    k = 2 * n
    M = direct_sum(bm[1][0], 2, n); tD = direct_sum(bm[1][1], 2, n)
    M2 = comp(M, M); I = ident(k)
    # generators of the maps commuting with M: M on the plane {v, Mv}, identity on its complement (v with omega(v, Mv) = 1)
    def refl(v):
        Mv = app(M, v); assert omega(v, Mv, k) == 1
        img = []
        for i in range(2 * k):
            x = 1 << i
            p = (v if omega(x, Mv, k) else 0) ^ (Mv if omega(x, v, k) else 0)   # projection of x on the plane
            img.append(x ^ p ^ app(M, p))
        t = tuple(img); assert comp(t, M) == comp(M, t) and comp(t, comp(t, t)) == I
        return t
    good = [v for v in range(1, 1 << (2 * k)) if omega(v, app(M, v), k) == 1]
    rnd = random.Random(seed)
    if sample is None:
        gens = [refl(v) for v in rnd.sample(good, min(len(good), 8))]
        seen = {I}; frontier = [I]
        while frontier:
            nf = []
            for g in frontier:
                for h in gens:
                    x = comp(h, g)
                    if x not in seen: seen.add(x); nf.append(x)
            frontier = nf
        if k == 2:   # the reflections of order 3 generate only half of the group at 4 points: take all 4 x 4 bit matrices instead
            seen = set()
            for t in itertools.product(range(1, 16), repeat=4):
                if all(omega(t[i], t[j], k) == omega(1 << i, 1 << j, k) for i in range(4) for j in range(4)) and comp(t, M) == comp(M, t): seen.add(tuple(t))
        print('N=%d: maps commuting with R found: %d  (the unitary group of dimension %d over the field of 4 elements has %d)' % (1 << k, len(seen), k, {2: 18, 4: 77760}.get(k, -1)))
        mirrors = [comp(tD, c) for c in seen if comp(comp(tD, c), comp(tD, c)) == I]
        conj = set(comp(comp(c, tD), inv(c, k)) for c in seen)
        print('  stabilizer mirrors (as bit matrices): %d ; of these conjugate to D: %d' % (len(mirrors), len(conj & set(mirrors))))
    else:
        gens = [refl(v) for v in rnd.sample(good, 12)]
        mirrors = []
        for _ in range(sample):
            c = I
            for _ in range(rnd.randint(4, 40)): c = comp(rnd.choice(gens), c)
            mirrors.append(comp(comp(c, tD), inv(c, k)))
        print('N=%d: %d random conjugates of D by maps commuting with R (%d distinct)' % (1 << k, sample, len(set(mirrors))))
        mirrors = list(set(mirrors))
    tri = collections.Counter(); bad = 0
    for t in mirrors:
        js = (jrank(t, k), jrank(comp(t, M), k), jrank(comp(t, M2), k))
        s = tuple(sorted(js)); tri[s] += 1
        if s[0] + s[1] < k: bad += 1
    print('  triples (j of S, S R, S R^2) sorted : count ; each mirror is N/2^j copies of the 2^j-point transform up to free maps')
    for s in sorted(tri): print('   %s : %d   least pair sum %d (k = %d)   textbook price of the best pair = N * %d' % (s, tri[s], s[0] + s[1], k, s[0] + s[1]))
    print('  pairs violating j1 + j2 >= k : %d' % bad)
census(1); census(2)
if len(sys.argv) > 1: census(3, sample=int(sys.argv[1]))
