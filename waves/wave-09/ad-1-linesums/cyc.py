#!/usr/bin/env python3
"""cyc.py k [ad-1-linesums]  The cyclic form of the line sums (d-1): the N - 1 lines that miss the origin are the cyclic
shifts of one set D of q logarithms.  As an operator this is multiplication by D(t) = sum of t^d in Q[t]/(t^(N-1) - 1).
QUESTION: can D(t) be a product of a FEW sparse factors (two or three terms, rational coefficients of any size) and their
inverses?  Each such factor is one pass of 1 or 2 gates per point, so O(1) factors would be a linear R.
METHOD (exact): the 2-adic valuation of D and of every candidate factor at every prime above 2 of the field of (N-1)-th
roots of unity.  Computed in the Galois ring Z/2^s[t]/(h): tau = t^(2^(k(s-1))) is the Teichmuller root of unity, and the
valuation at the prime number a is the largest power of 2 dividing the value at tau^a.  Whole numbers modulo 2^s only."""
import sys, math, itertools
import numpy as np
k = int(sys.argv[1]); j = k // 2; q = 1 << j; N = 1 << k; n = N - 1; s = 8; MOD = 1 << s
PRIM = {4: [1, 1, 0, 0], 6: [1, 1, 0, 0, 0, 0], 8: [1, 0, 1, 1, 1, 0, 0, 0]}[k]      # low coefficients of the primitive polynomial
hbits = sum(b << i for i, b in enumerate(PRIM)) | (1 << k)
def gf_mul(a, b):
    r = 0
    while b:
        if b & 1: r ^= a
        b >>= 1; a <<= 1
        if a >> k: a ^= hbits
    return r
th = [1]
for i in range(1, n): th.append(gf_mul(th[-1], 2))
assert len(set(th)) == n, "not primitive"
def gf_pow(a, e):
    r = 1
    while e:
        if e & 1: r = gf_mul(r, a)
        a = gf_mul(a, a); e >>= 1
    return r
D = [d for d in range(n) if th[d] ^ gf_pow(th[d], q) == 1]
print("N =", N, " q =", q, " D =", D if k <= 6 else "(%d logarithms)" % len(D))
assert len(D) == q
def gr_mul(a, b):
    r = [0] * (2 * k - 1)
    for i in range(k):
        if a[i]:
            for l in range(k): r[i + l] += a[i] * b[l]
    for d in range(2 * k - 2, k - 1, -1):
        c = r[d]
        if c:
            r[d] = 0
            for i in range(k): r[d - k + i] -= c * PRIM[i]
    return [v % MOD for v in r[:k]]
tau = [0, 1] + [0] * (k - 2)
for _ in range(k * (s - 1)): tau = gr_mul(tau, tau)
pw = [[1] + [0] * (k - 1)]
for i in range(1, n): pw.append(gr_mul(pw[-1], tau))
assert gr_mul(pw[-1], tau) == pw[0] and [v % 2 for v in tau] == [0, 1] + [0] * (k - 2)
PW = np.array(pw, dtype=np.int64)
def val_arr(A):
    """2-adic valuation (capped at s) of each element of the Galois ring in array A[..., k]"""
    A = A % MOD
    v = np.full(A.shape[:-1], s, dtype=np.int64)
    for l in range(s - 1, -1, -1):
        v = np.where((A % (1 << (l + 1)) != 0).any(axis=-1) & ((A % (1 << l)) == 0).all(axis=-1), l, v)
    return v
def val(x):
    return int(val_arr(np.array(x, dtype=np.int64)[None, :])[0])
# cyclotomic cosets (one prime above 2 of the component d = n / gcd(a, n) for each coset)
seen = set(); reps = []
for a in range(n):
    if a in seen: continue
    c = set(); b = a
    while b not in c: c.add(b); b = (2 * b) % n
    seen |= c; reps.append(a)
Dv = {}
for a in reps:
    Dv[a] = val(PW[[(a * d) % n for d in D]].sum(axis=0))
def dig(x): return bin(x).count("1")
def stick(a, sg):
    b = (sg * a) % n
    return dig(b) - (dig(b % (q - 1)) if b % (q - 1) else j)
for sg in (1, -1):
    match = all(Dv[a] == stick(a, sg) for a in reps if a)
    print("valuation of D at the prime a equals  digits(b) - digits(b mod (q-1))  [or - j when q-1 divides b], b = %+d * a, on every prime:" % sg, match)
print("sum of the valuations over all N - 1 roots of unity:", sum(Dv[a] * len({(a * 2 ** i) % n for i in range(k)}) for a in reps), " (N-1) j / 2 =", n * j / 2)
comp = {}
for a in reps:
    d = n // math.gcd(a, n) if a else 1
    comp.setdefault(d, []).append(Dv[a])
print("component (order of the root of unity) : valuations of D at its primes")
for d in sorted(comp):
    kind = "trivial" if d == 1 else ("radius only" if (q - 1) % d == 0 else ("angle only" if (q + 1) % d == 0 else "MIXED"))
    vs = sorted(comp[d]); print("   %4d %-11s primes %3d  valuations %s  spread %d" % (d, kind, len(vs), dict((x, vs.count(x)) for x in sorted(set(vs))), vs[-1] - vs[0]))
top = [a for a in reps if a and math.gcd(a, n) == 1]
w = tuple(Dv[a] for a in top)
print("top component: %d primes, target valuations" % len(top), w)
# ---------- every rational trinomial 1 + c1 t^e + c2 t^f, c1 and c2 odd (all classes modulo 8) ----------
A = np.array(reps, dtype=np.int64); odd = (1, 3, 5, 7)
maxv = 0; hi = []; pats = {}; cnt_ge2 = 0; cube_only = True; best_zero = (0, None)
for e in range(1, n):
    fs = np.arange(e + 1, n, dtype=np.int64)
    if len(fs) == 0: continue
    Ae = PW[(A * e) % n]                                  # reps x k
    Af = PW[(A[None, :] * fs[:, None]) % n]               # f x reps x k
    for c1 in odd:
        for c2 in odd:
            X = PW[0][None, None, :] + c1 * Ae[None, :, :] + c2 * Af
            v = val_arr(X)                                # f x reps
            m = int(v.max())
            if m >= 2:
                idx = np.argwhere(v >= 2)
                for fi, ai in idx:
                    f = int(fs[fi]); a = int(A[ai]); cnt_ge2 += 1
                    cube = (3 * a * e) % n == 0 and (3 * a * f) % n == 0
                    cube_only &= cube
                    if len(hi) < 6: hi.append((e, f, c1, c2, a, int(v[fi, ai]), cube))
            maxv = max(maxv, m)
            if c1 == 1 and c2 == 1:
                z = (v >= 1); exact = (v >= 2)
                for fi in range(len(fs)):
                    row = z[fi]
                    p = tuple(int(row[reps.index(a)]) for a in top) if k <= 6 else None
                    if p is not None and any(p) and not any(exact[fi][reps.index(a)] for a in top): pats.setdefault(p, (e, int(fs[fi])))
                if k > 6:
                    ti = [reps.index(a) for a in top]
                    sub = z[:, ti]; subx = exact[:, ti]
                    for fi in range(len(fs)):
                        if sub[fi].any() and not subx[fi].any(): pats.setdefault(tuple(int(b) for b in sub[fi]), (e, int(fs[fi])))
print("trinomials 1 + c1 t^e + c2 t^f, all e < f, c1 and c2 in every odd class modulo 8:")
print("   largest valuation at any prime:", maxv, "(8 = the cap = exactly zero)  cases with valuation >= 2:", cnt_ge2,
      "  all of them at primes where t^e and t^f are cube roots of unity:", cube_only)
print("   examples (e, f, c1, c2, prime a, valuation, cube-root case):", hi[:3])
print("   distinct zero patterns on the top component (trinomials that are exactly zero there are left out):", len(pats))
sizes = sorted(set(sum(p) for p in pats)); print("   number of top primes one trinomial vanishes at, values seen:", sizes, "of", len(top))
if len(pats) <= 40:
    for p, ef in sorted(pats.items(), key=lambda t: (sum(t[0]), t[0])): print("      pattern", p, " e.g. 1 + t^%d + t^%d" % ef)
print("   total valuation of D on the top component (in primes):", sum(w), "  so at least", -(-sum(w) // max(sizes)), "trinomials by count and", max(w) - min(w), "by spread")
# least number of signed patterns whose sum is w + constant
S1 = set()
for p in pats: S1.add(p); S1.add(tuple(-x for x in p))
levels = [{tuple([0] * len(top))}, S1]
LIM = 3000000
while len(levels) < 5:
    nxt = set()
    for u in levels[-1]:
        for v2 in S1:
            nxt.add(tuple(a + b for a, b in zip(u, v2)))
        if len(nxt) > LIM: break
    if len(nxt) > LIM: break
    levels.append(nxt)
print("   reachable sums with 0..%d signed patterns:" % (len(levels) - 1), [len(L) for L in levels])
found = None
for m in range(0, 2 * (len(levels) - 1) + 1):
    a_ = min(m, len(levels) - 1); b_ = m - a_
    if b_ > len(levels) - 1: break
    for c in range(-m, m + 1):
        t = tuple(x + c for x in w)
        small, big = (levels[b_], levels[a_]) if len(levels[b_]) <= len(levels[a_]) else (levels[a_], levels[b_])
        for u in small:
            if tuple(x - y for x, y in zip(t, u)) in big: found = (m, c); break
        if found: break
    if found: break
print("   LEAST number of trinomial factors (inverses allowed, a power of 2 free) with D's valuations on the top component:",
      ("%d (scalar shift %d)" % found) if found else "more than %d" % (2 * (len(levels) - 1)))
# ---------- four-term factors, optional ----------
if len(sys.argv) > 2 and sys.argv[2] == '4':
    ti = [reps.index(a) for a in top]; At = A[ti]
    best_tot = 0; best = None; hist = {}; cl = (1, 3, 5, 7)
    for e in range(1, n):
        Ae = PW[(At * e) % n]
        for f in range(e + 1, n):
            gs = np.arange(f + 1, n, dtype=np.int64)
            if len(gs) == 0: continue
            Af = PW[(At * f) % n]; Ag = PW[(At[None, :] * gs[:, None]) % n]
            for c1 in cl:
                for c2 in cl:
                    base = PW[0][None, :] + c1 * Ae + c2 * Af
                    for c3 in cl:
                        v = val_arr(base[None, :, :] + c3 * Ag)       # g x top
                        v = np.where((v >= s).any(axis=1)[:, None], 0, v)   # exactly zero somewhere: not a usable factor
                        tot = v.sum(axis=1); mx = int(v.max())
                        hist[mx] = hist.get(mx, 0) + 1
                        gi = int(tot.argmax())
                        if int(tot[gi]) > best_tot: best_tot = int(tot[gi]); best = (e, f, int(gs[gi]), c1, c2, c3, tuple(int(x) for x in v[gi]))
    print("four-term factors 1 + c1 t^e + c2 t^f + c3 t^g (3 gates per point), odd classes modulo 8, exact zeros left out:")
    print("   largest valuation at a top prime, by number of (e, f, coefficient) cases:", dict(sorted(hist.items())))
    print("   largest total valuation on the top component by one factor:", best_tot, " example", best, " (D itself:", sum(w), "with", q - 1, "gates per point)")
