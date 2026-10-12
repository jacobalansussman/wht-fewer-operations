# u-7-quotient, run D: exact integers.
# D1. the ladder: for j = 1, 2, 3 the wires congruent to a combination of outputs modulo 2^j.
#     claim: { (H c) / 2^j mod 2 : c integer, H c == 0 mod 2^j } is the Reed-Muller code of degree j (dimension 1 + k + ... + C(k, j)).
#     computed from the Hermite-style reduction of the row lattice of H over the integers modulo 2^(j+1).
# D2. 'all quotients of held full wires are distinct' on more circuits.
import sys, itertools, math
exec(open(sys.argv[1] + '/u-7-quotient/qa.py').read().split("base = sys.argv[1]")[0])
base = sys.argv[1]
def f2rank(vecs):
    basis = []
    for v in vecs:
        for b in basis: v = min(v, v ^ b)
        if v: basis.append(v)
    return basis
for N in (8, 16):
    k = N.bit_length() - 1; H = had(N)
    # lattice basis in echelon form over Z (integer row reduction), then read the diagonal valuations
    rows = [list(r) for r in H]; ech = []
    for c in range(N):
        while True:
            nz = [r for r in rows if r[c] != 0]
            if len(nz) <= 1: break
            nz.sort(key=lambda r: abs(r[c])); p = nz[0]
            for r in nz[1:]:
                q = r[c] // p[c]
                for t in range(N): r[t] -= q * p[t]
        nz = [r for r in rows if r[c] != 0]
        if nz: ech.append(nz[0]); rows.remove(nz[0])
    assert len(ech) == N
    # L_j = (lattice intersect 2^j Z^N) / 2^j mod 2, by brute force over the lattice modulo 2^(j+1): generate with the echelon basis
    for j in (0, 1, 2, 3):
        if j > k: continue
        M = 2 ** (j + 1)
        # lattice mod M as a set is too large in general; instead use the Reed-Muller side: check both inclusions by dimension.
        # inclusion RM(j) inside L_j: indicator of every codimension-j coordinate subcube = 2^-j * sum of 2^j outputs (checked exactly)
        ok = True; gens = []
        for bits in itertools.combinations(range(k), j):
            ys = [sum(1 << b for b in sub) for r in range(j + 1) for sub in itertools.combinations(bits, r)]
            s = [sum(H[y][x] for y in ys) for x in range(N)]
            ok &= all(t % 2**j == 0 for t in s)
            gens.append(sum(1 << x for x in range(N) if (s[x] // 2**j) % 2))
        dim_rm = len(f2rank(gens))
        # upper bound on dim L_j from the elementary divisors: number of divisors 2^i with i <= j
        # elementary divisors by Smith form through gcds of the echelon is not direct; use the known determinant structure:
        # count them exactly by rank of H modulo 2^(i) ... rank over Z/2 of (basis of lattice /2^i)-part: do Smith by brute force
        print('  N=%d j=%d: indicators of the C(k,j)=%d coordinate subcubes of codimension j are 2^-j * (sum of 2^j outputs): %s ; span of those for this j alone: %d' % (N, j, math.comb(k, j), ok, dim_rm))
    # Smith normal form by repeated gcd elimination (small N)
    A = [list(r) for r in H]; div = []
    n = N; t = 0
    while t < n:
        piv = None
        for i in range(t, n):
            for jj in range(t, n):
                if A[i][jj] != 0 and (piv is None or abs(A[i][jj]) < abs(A[piv[0]][piv[1]])): piv = (i, jj)
        if piv is None: break
        A[t], A[piv[0]] = A[piv[0]], A[t]
        for r in A: r[t], r[piv[1]] = r[piv[1]], r[t]
        again = True
        while again:
            again = False
            for i in range(t + 1, n):
                if A[i][t] != 0:
                    q = A[i][t] // A[t][t]
                    for c in range(t, n): A[i][c] -= q * A[t][c]
                    if A[i][t] != 0:
                        A[t], A[i] = A[i], A[t]; again = True
            for c in range(t + 1, n):
                if A[t][c] != 0:
                    q = A[t][c] // A[t][t]
                    for i in range(t, n): A[i][c] -= q * A[i][t]
                    if A[t][c] != 0:
                        for r in A: r[t], r[c] = r[c], r[t]
                        again = True
        div.append(abs(A[t][t])); t += 1
    from collections import Counter
    print('  N=%d diagonal after integer row and column reduction (2^j: how many): %s ; binomials %s' % (N, sorted(Counter(div).items()), [math.comb(k, j) for j in range(k + 1)]))
print('D2. more circuits: are all quotients (f-f\')/2, (f+f\')/2 of held full wires distinct?')
import glob, os
for path, N in ((base + '/h-8-provethewrongthi/h8_21_three_hubs.txt', 8), (base + '/h-0-onepergate/h16_54gates_tensor.txt', 16),
                (base + '/e2-0-pieces/slp_64.txt', 64), (base + '/h-6-classhub/brick_m1.txt', 4)):
    try:
        W = wires(path, N)
    except Exception as e:
        print('  %s: could not parse (%s)' % (os.path.basename(path), type(e).__name__)); continue
    H = had(N); Hn = {norm(r) for r in H}; held = {}
    for n_, w in W.items():
        if all(t.denominator == 1 for t in w): held.setdefault(norm(w), n_)
    full = [v for v in held if all(abs(t) == 1 for t in v)]
    nout = sum(1 for v in full if v in Hn)
    quo = {}
    for i in range(len(full)):
        for j in range(i):
            f, g = full[i], full[j]
            for q in (norm([(a - b) // 2 for a, b in zip(f, g)]), norm([(a + b) // 2 for a, b in zip(f, g)])):
                quo[q] = quo.get(q, 0) + 1
    print('  %s: N=%d gates=%d full wires=%d (outputs among them %d) quotients %d distinct %d ; most pairs for one quotient %d' % (
        os.path.basename(path), N, len(W) - N, len(full), nout, len(full) * (len(full) - 1), len(quo), max(quo.values())))
