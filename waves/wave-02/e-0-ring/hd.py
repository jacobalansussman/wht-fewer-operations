#!/usr/bin/env python3
# e-0-ring / hd.py : the Hasse-Davenport product formula read in the ring, k even (so 3 divides n = 2^k - 1).
# g(j) = sum over m of c[m] zeta^(j m), c[m] = (-1)^Trace(theta^m): the eigenvalue of the transform's element M at the exponent j.
# Claim: g(j) g(j + n/3) g(j + 2n/3) = N g(3j) for every j.   Floating point (double precision), error printed.
# Second claim (exact, integers): the element with eigenvalues g(3j) has coefficient c[u] + c[u+n/3] + c[u+2n/3] at t^(3u)
# and that number is -1 + 4*[Trace to the field with 4 elements of theta^u is 0].
import cmath, math
PRIM = {4: 0b10011, 6: 0b1000011, 8: 0b100011101, 10: 0b10000001001}
for k in (4, 6, 8, 10):
    p = PRIM[k]; n = (1 << k) - 1; N = 1 << k; pw = [1]
    for _ in range(n - 1):
        v = pw[-1] << 1
        if v >> k: v ^= p
        pw.append(v)
    lg = {v: i for i, v in enumerate(pw)}
    def mul(a, b): return 0 if a == 0 or b == 0 else pw[(lg[a] + lg[b]) % n]
    def trace(v, steps, power):               # sum of v^(power^i), i < steps
        s = 0; w = v
        for _ in range(steps):
            s ^= w
            for _ in range(power): w = mul(w, w)
        return s
    c = [1 - 2 * trace(v, k, 1) for v in pw]
    z = [cmath.exp(2j * math.pi * i / n) for i in range(n)]
    g = [sum(c[m] * z[(j * m) % n] for m in range(n)) for j in range(n)]
    err = max(abs(g[j] * g[(j + n // 3) % n] * g[(j + 2 * n // 3) % n] - N * g[(3 * j) % n]) for j in range(n))
    ok = all(c[u] + c[(u + n // 3) % n] + c[(u + 2 * n // 3) % n] == (-1 + 4 * (trace(pw[u], k // 2, 2) == 0)) for u in range(n))
    print("k=%d n=%d: largest |g(j) g(j+n/3) g(j+2n/3) - N g(3j)| over all j = %.2e (the terms have size %.0f);  coefficient identity exact: %s"
          % (k, n, err, N ** 1.5, ok), flush=True)
