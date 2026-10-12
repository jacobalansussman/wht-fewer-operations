#!/usr/bin/env python3
# e-0-ring / hd_exact.py : the product formula EXACTLY, in (Z[w])[t]/(t^n - 1), w a primitive cube root of unity (w^2 = -1 - w).
#     M(t) * M(w t) * M(w^2 t) = N * ( -J3 + 4 K(t^3) )
# M = sum of c[m] t^m, c[m] = (-1)^Trace(theta^m);  "M(w t)" has coefficients c[m] w^m (a twist by the cubic character);
# J3 = sum of t^(3u);  K = sum of t^(3u) over u mod n/3 with Trace to the field with 4 elements of theta^u equal to 0.
PRIM = {4: 0b10011, 6: 0b1000011, 8: 0b100011101}
def wmul(a, b):                                   # (a0 + a1 w)(b0 + b1 w), w^2 = -1 - w
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0] - a[1] * b[1])
W = [(1, 0), (0, 1), (-1, -1)]
for k in (4, 6, 8):
    p = PRIM[k]; n = (1 << k) - 1; N = 1 << k; pw = [1]
    for _ in range(n - 1):
        v = pw[-1] << 1
        if v >> k: v ^= p
        pw.append(v)
    lg = {v: i for i, v in enumerate(pw)}
    def mul(a, b): return 0 if a == 0 or b == 0 else pw[(lg[a] + lg[b]) % n]
    def trace(v, steps, power):
        s = 0; w = v
        for _ in range(steps):
            s ^= w
            for _ in range(power): w = mul(w, w)
        return s
    c = [1 - 2 * trace(v, k, 1) for v in pw]
    def pmul(A, B):
        out = [(0, 0)] * n; out = [list(x) for x in out]
        for i, a in enumerate(A):
            if a == (0, 0): continue
            for j, b in enumerate(B):
                x = wmul(a, b); o = out[(i + j) % n]; o[0] += x[0]; o[1] += x[1]
        return [tuple(x) for x in out]
    M = [[(c[m] * W[(a * m) % 3][0], c[m] * W[(a * m) % 3][1]) for m in range(n)] for a in range(3)]
    lhs = pmul(pmul(M[0], M[1]), M[2])
    rhs = [(0, 0)] * n
    Kset = [u for u in range(n // 3) if trace(pw[u], k // 2, 2) == 0]
    for u in range(n // 3):
        rhs[3 * u] = (N * (-1 + 4 * (u in Kset)), 0)
    print("k=%d N=%d: M(t) M(wt) M(w^2 t) == N(-J3 + 4K(t^3)) exactly: %s ;  K has %d of %d points: %s"
          % (k, N, lhs == rhs, len(Kset), n // 3, Kset if len(Kset) < 12 else "..."), flush=True)
