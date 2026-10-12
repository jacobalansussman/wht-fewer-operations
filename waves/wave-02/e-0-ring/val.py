#!/usr/bin/env python3
# e-0-ring / val.py : the 2-adic picture of the cyclic ring Z[t]/(t^n - 1), n = 2^k - 1.
# Exact.  For each "prime" j (j = 1..n-1 up to doubling) the valuation v_j(f) of a ring element f is the power of 2
# dividing f(tau^j), tau the Teichmueller lift of the field generator theta in Z_2[x]/(g), computed modulo 2^PREC.
# Norms on each piece (divisor d of n) are exact integer determinants (Bareiss).
import sys
from itertools import combinations
from math import gcd
PREC = 48
MOD = 1 << PREC
PRIM = {3: 0b1011, 4: 0b10011, 5: 0b100101, 6: 0b1000011, 7: 0b10000011, 8: 0b100011101}


def field(k):
    p = PRIM[k]; n = (1 << k) - 1
    pw = [1]
    for _ in range(n - 1):
        v = pw[-1] << 1
        if v >> k: v ^= p
        pw.append(v)
    assert len(set(pw)) == n
    def tr(v):                                   # absolute trace of field element v (bit vector)
        s = 0; w = v
        for _ in range(k):
            s ^= w
            # square w
            r = 0
            for b in range(k):
                if w >> b & 1:
                    e = pw[(2 * b) % n]
                    r ^= e
            w = r
        assert s in (0, 1)
        return s
    return p, n, pw, [tr(v) for v in pw]


def graeffe(g):                                  # g: coefficient list low..high, monic.  returns h with h(x^2) = +-g(x)g(-x)
    k = len(g) - 1
    gm = [c if i % 2 == 0 else -c for i, c in enumerate(g)]
    prod = [0] * (2 * k + 1)
    for i, a in enumerate(g):
        for j, b in enumerate(gm):
            prod[i + j] += a * b
    h = prod[0::2]
    if h[-1] < 0: h = [-c for c in h]
    return [c % MOD for c in h]


def teich(k):
    p = PRIM[k]
    g = [(p >> i) & 1 for i in range(k + 1)]
    for _ in range(PREC + 2):
        g = graeffe(g)
    assert g[-1] == 1
    return g


def xpowers(g, n):
    k = len(g) - 1
    out = [[1] + [0] * (k - 1)]
    for _ in range(n - 1):
        a = out[-1]
        top = a[-1]
        b = [0] + a[:-1]
        if top:
            b = [(b[i] - top * g[i]) % MOD for i in range(k)]
        out.append(b)
    # check x^n = 1
    a = out[-1]; top = a[-1]; b = [0] + a[:-1]
    b = [(b[i] - top * g[i]) % MOD for i in range(k)]
    assert b == [1] + [0] * (k - 1), "Teichmueller polynomial does not divide x^n - 1"
    return out


def v2(c):
    if c % MOD == 0: return PREC
    c %= MOD
    return (c & -c).bit_length() - 1


def val(f, j, XP, n):                            # f: dict exponent -> integer coefficient
    k = len(XP[0])
    acc = [0] * k
    for e, a in f.items():
        row = XP[(j * e) % n]
        for i in range(k): acc[i] = (acc[i] + a * row[i]) % MOD
    return min(v2(c) for c in acc)


def cyclo(d):
    # integer coefficients of the d-th cyclotomic polynomial, low..high
    def pdiv(a, b):
        a = a[:]; q = [0] * (len(a) - len(b) + 1)
        for i in range(len(a) - len(b), -1, -1):
            q[i] = a[i + len(b) - 1] // b[-1]
            for j, c in enumerate(b): a[i + j] -= q[i] * c
        assert not any(a)
        return q
    p = [-1] + [0] * (d - 1) + [1]
    for e in range(1, d):
        if d % e == 0: p = pdiv(p, cyclo(e))
    return p


def norm_on_piece(f, d, n):                      # exact norm of f(zeta_d) to the rationals: det of multiplication by f on Z[x]/Phi_d
    Phi = cyclo(d); m = len(Phi) - 1
    def red(vec):                                # reduce polynomial (list) modulo Phi
        vec = vec[:]
        for i in range(len(vec) - 1, m - 1, -1):
            c = vec[i]
            if c:
                for j in range(m + 1): vec[i - m + j] -= c * Phi[j]
        return vec[:m] + [0] * (m - len(vec[:m]))
    base = [0] * d
    for e, a in f.items(): base[e % d] += a
    M = []
    for s in range(m):
        vec = [0] * (d + m)
        for e in range(d): vec[e + s] += base[e]
        M.append(red(vec))
    # Bareiss
    A = [r[:] for r in M]; sign = 1; prev = 1
    for i in range(m):
        if A[i][i] == 0:
            sw = next((r for r in range(i + 1, m) if A[r][i] != 0), None)
            if sw is None: return 0
            A[i], A[sw] = A[sw], A[i]; sign = -sign
        for r in range(i + 1, m):
            for c in range(i + 1, m):
                A[r][c] = (A[r][c] * A[i][i] - A[r][i] * A[i][c]) // prev
        prev = A[i][i]
    return sign * A[m - 1][m - 1]


def factor(x):
    x = abs(x); out = []
    if x == 0: return "0"
    p = 2
    while p * p <= x and p < 2000000:
        e = 0
        while x % p == 0: x //= p; e += 1
        if e: out.append("%d^%d" % (p, e) if e > 1 else "%d" % p)
        p += 1 if p == 2 else 2
    if x > 1: out.append(str(x))
    return "*".join(out) if out else "1"


def orbits(n):
    seen = set(); reps = []
    for j in range(1, n):
        if j in seen: continue
        o = set(); x = j
        while x not in o: o.add(x); x = (2 * x) % n
        seen |= o; reps.append(min(o))
    return reps


def digsum(j): return bin(j).count("1")


def main(k, maxterms_list=True):
    p, n, pw, tr = field(k)
    g = teich(k); XP = xpowers(g, n)
    reps = orbits(n)
    mask = {m: 1 for m in range(n) if tr[m] == 1}
    divs = [d for d in range(2, n + 1) if n % d == 0]
    print("== k=%d N=%d n=%d  primitive polynomial %s  trace-one set has %d terms" % (k, 1 << k, n, bin(p), len(mask)))
    print("primes (orbits of doubling) reps:", reps)
    print("  piece of each rep (order of zeta^j):", [n // gcd(j, n) for j in reps])
    print("  digit sums s(j):                   ", [digsum(j) for j in reps])
    vm = [val(mask, j, XP, n) for j in reps]
    print("  valuation of the mask at j:        ", vm)
    print("  k-1-s(j):                          ", [k - 1 - digsum(j) for j in reps], " s(j)-1:", [digsum(j) - 1 for j in reps])
    print("  norm of mask on each piece:", {d: factor(norm_on_piece(mask, d, n)) for d in divs})
    # letters
    print("-- two-term letters 1 + c t^a (integer c): valuations at the reps, norms per piece")
    for c in (1, -1, 2, -2, 3, -3):
        tot = 0
        for a in range(1, n):
            f = {0: 1, a: c}
            vs = [val(f, j, XP, n) for j in reps]
            # where zeta^(ja) = 1 the element is the scalar 1 + c: subtract that constant
            vs2 = [v - (v2(1 + c) if (j * a) % n == 0 else 0) for v, j in zip(vs, reps)]
            tot += sum(abs(x) for x in vs2)
        print("   c=%+d: sum over all a and all primes of |valuation beyond the scalar| = %d" % (c, tot))
    print("-- three-term letters s0 + s1 t^a + s2 t^b, signs +-1, a<b, up to shift: those that vanish mod 2 somewhere")
    seen = set(); rows = []
    for a, b in combinations(range(1, n), 2):
        key = min(tuple(sorted(((0 - s) % n, (a - s) % n, (b - s) % n))) for s in (0, a, b))
        if key in seen: continue
        seen.add(key)
        for s1 in (1, -1):
            for s2 in (1, -1):
                f = {0: 1, a: s1, b: s2}
                vs = [val(f, j, XP, n) for j in reps]
                if any(vs):
                    nm = {d: norm_on_piece(f, d, n) for d in divs}
                    rows.append((a, b, s1, s2, vs, nm))
    print("   %d shift classes of supports; %d signed letters with some positive valuation" % (len(seen), len(rows)))
    pure = 0
    for a, b, s1, s2, vs, nm in rows:
        odd = all((abs(x) & (abs(x) - 1)) == 0 and x != 0 for x in nm.values())
        if odd: pure += 1
        if maxterms_list or odd:
            print("   1 %s t^%d %s t^%d  val %s  norms %s%s" % ("+" if s1 > 0 else "-", a, "+" if s2 > 0 else "-", b, vs,
                  {d: factor(x) for d, x in nm.items()}, "   <-- PURE power of 2 on every piece" if odd else ""))
    print("   letters whose norm is a pure power of 2 on every non-trivial piece: %d of %d" % (pure, len(rows)))
    # how many primes can one support hit
    hit = {}
    for a, b, s1, s2, vs, nm in rows:
        if s1 == 1 and s2 == 1:
            c = sum(1 for v in vs if v > 0); hit[c] = hit.get(c, 0) + 1
    print("   (all-plus trinomials) number of primes hit -> how many trinomial classes:", dict(sorted(hit.items())), "of", len(reps), "primes")


if __name__ == "__main__":
    k = int(sys.argv[1])
    main(k, maxterms_list=(len(sys.argv) > 2 and sys.argv[2] == "all"))
