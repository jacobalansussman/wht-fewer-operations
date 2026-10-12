#!/usr/bin/env python3
# e-0-ring / roots.py : how many "primes" can ONE three-term letter of the cyclic ring touch?
# A letter a0 + a1 t^a + a2 t^b (odd integer coefficients) has positive 2-adic valuation at the prime j only if
# 1 + x^a + x^b = 0 at x = theta^j in the field with N = 2^k elements.  Exact count of such j, for every (a, b) up to the
# free relabellings j -> u j (so a runs over the divisors of n only).  Counts both all j and the j coprime to n.
import sys
from math import gcd
PRIM = {4: 0b10011, 5: 0b100101, 6: 0b1000011, 7: 0b10000011, 8: 0b100011101, 9: 0b1000010001, 10: 0b10000001001,
        11: 0b100000000101, 12: 0b1000001010011}

def run(k):
    p = PRIM[k]; n = (1 << k) - 1
    pw = [1]
    for _ in range(n - 1):
        v = pw[-1] << 1
        if v >> k: v ^= p
        pw.append(v)
    assert len(set(pw)) == n
    lg = {v: i for i, v in enumerate(pw)}
    Z = [None] + [lg[pw[m] ^ 1] for m in range(1, n)]          # 1 + theta^m = theta^Z[m]
    phi = sum(1 for j in range(1, n) if gcd(j, n) == 1)
    best = []
    for a in [d for d in range(1, n) if n % d == 0]:
        cnt = [0] * n; cntp = [0] * n
        for j in range(1, n):
            m = (j * a) % n
            if m == 0: continue
            z = Z[m]; g = gcd(j, n)
            if z % g: continue
            j1 = j // g; n1 = n // g
            b0 = (z // g) * pow(j1, -1, n1) % n1
            for r in range(g):
                b = b0 + r * n1
                cnt[b] += 1
                if g == 1: cntp[b] += 1
        for b in range(1, n):
            if b != a and cnt[b]:
                best.append((cntp[b], cnt[b], a, b))
    best.sort(reverse=True)
    print("k=%d n=%d phi(n)=%d   sqrt(N)=%.1f" % (k, n, phi, 2 ** (k / 2)))
    print("   largest numbers of primitive j (and of all j) on which 1 + x^a + x^b vanishes:")
    shown = 0; last = None
    for cp, c, a, b in best:
        if (cp, c) == last: continue
        last = (cp, c)
        # subfield type: a and b both multiples of e = n/(2^k' - 1) for a proper divisor k' of k
        typ = ""
        for kk in range(1, k):
            if k % kk == 0:
                e = n // ((1 << kk) - 1)
                if a % e == 0 and b % e == 0: typ = "subfield F_%d letter (a function of j mod %d)" % (1 << kk, (1 << kk) - 1); break
        print("     %5d primitive (%.4f of them), %5d in all:  a=%d b=%d  %s" % (cp, cp / phi, c, a, b, typ))
        shown += 1
        if shown >= 8: break
    gen = [x for x in best if not any(k % kk == 0 and x[2] % (n // ((1 << kk) - 1)) == 0 and x[3] % (n // ((1 << kk) - 1)) == 0 for kk in range(1, k))]
    if gen:
        cp, c, a, b = gen[0]
        print("   best letter NOT of subfield type: %d primitive j of %d (fraction %.5f; 2^(-k/2) = %.5f), a=%d b=%d" % (cp, phi, cp / phi, 2 ** (-k / 2), a, b))
    tot = sum(x[0] for x in best)
    print("   average over all (a,b): %.3f primitive j per letter" % (tot / max(1, len(best))), flush=True)

for k in [int(x) for x in sys.argv[1:]]:
    run(k)
