# x-1-digits/slices.py   count (G): a gate is a*u + b*v, scalings free.  Whole numbers only, every circuit replayed on all N x N entries.
# H = sum_j (-2)^j B_j ,  B_j(y,x) = C(|y&x|, j) = sum over sets U of j bits of [U in y][U in x].
# A "window" [lo,hi] of digits = the levels lo..hi of  Z D Z^T.  The circuit: Yates in (superset sums z_U), diagonal, Yates out,
# each pass TRIMMED to the states that some level of the window can still use.
import sys
from math import comb
pc = lambda v: bin(v).count("1")
def window(k, lo, hi, replay=True, q=-2):   # q = s - 1 ; q = -2 is the transform
    N = 1 << k; gates_in = gates_out = 0
    # in-pass: state s after stage i: bits <= i of s are a prefix of U, bits > i are a suffix of x.
    f = {x: ([int(t == x) for t in range(N)] if replay else None) for x in range(N) if pc(x) >= lo}
    for i in range(k):
        low = (1 << (i + 1)) - 1; g = {}
        for s0 in range(N):
            if s0 >> i & 1: continue
            s1 = s0 | 1 << i; wu = pc(s0 & low); wx = pc(s0 >> (i + 1))
            if wu <= hi and wu + wx >= lo:
                a, b = f[s0], f[s1]; gates_in += 1
                g[s0] = [p + q for p, q in zip(a, b)] if replay else None
            if wu + 1 <= hi and wu + 1 + wx >= lo: g[s1] = f[s1]
        f = g
    assert set(f) == {U for U in range(N) if lo <= pc(U) <= hi}
    # diagonal (free), then out-pass: state s after stage i: bits <= i are a prefix of y, bits > i a suffix of U.
    h = {U: ([q ** pc(U) * t for t in f[U]] if replay else None) for U in f}
    for i in range(k):
        g = {}
        for s0 in range(N):
            if s0 >> i & 1: continue
            s1 = s0 | 1 << i; a = h.get(s0, 0); b = h.get(s1, 0)
            if a != 0: g[s0] = a
            if a != 0 and b != 0:
                gates_out += 1; g[s1] = [p + q for p, q in zip(a, b)] if replay else None
            elif a != 0: g[s1] = a
            elif b != 0: g[s1] = b
        h = g
    return gates_in, gates_out, h
def target(k, lo, hi):
    N = 1 << k
    return [[sum((-2) ** j * comb(pc(y & x), j) for j in range(lo, hi + 1)) for x in range(N)] for y in range(N)]
if __name__ == "__main__":
    print("A. two starting facts")
    for k in (3, 4, 5, 6):
        N = 1 << k; ok1 = True
        for j in range(k + 1):
            W = [[int(U & x == U) for x in range(N)] for U in range(N) if pc(U) == j]
            ok1 &= all(sum(r[y] * r[x] for r in W) == comb(pc(y & x), j) for y in range(N) for x in range(N))
        print(f"  k={k}: B_j = W_j^T W_j for every j: {ok1}")
    for k in (8, 16, 32, 64, 128, 256):
        N = 1 << k
        # pairs (y,x) with exactly m common ones: C(k,m) 3^(k-m)
        tail = 0; jstar = None
        for j in range(k, -1, -1):
            tail += comb(k, j) * 3 ** (k - j)
            if tail >= N: jstar = j; break
        print(f"  k={k}: pairs with at least j common ones number fewer than N as long as j > {jstar}  (j/k = {jstar / k:.3f})")
    print("B. bottom window [0,d]: a circuit congruent to H modulo 2^(d+1); gates in + out; replayed on all entries")
    print("   k   N   d   in  out  total  total/N   congruent mod 2^(d+1)   equal to H   extra gates for this digit")
    for k in range(2, 9):
        N = 1 << k; H = [[(-1) ** pc(y & x) for x in range(N)] for y in range(N)]; prev = None
        for d in range(0, k + 1):
            gi, go, out = window(k, 0, d)
            T = target(k, 0, d)
            assert all(out[y] == T[y] for y in range(N))
            cong = all((out[y][x] - H[y][x]) % (1 << (d + 1)) == 0 for y in range(N) for x in range(N))
            eq = all(out[y] == H[y] for y in range(N))
            tot = gi + go
            print(f"  {k:2d} {N:4d} {d:2d} {gi:5d} {go:5d} {tot:5d}  {tot / N:6.3f}   {cong}   {eq}   {'' if prev is None else tot - prev}")
            prev = tot
    print("C. top window [j,k]: the digits from the top; gates in + out; replayed (equals H minus the bottom window [0,j-1])")
    print("   k   N   j   in  out  total  total/N   inputs read   outputs touched")
    for k in range(2, 9):
        N = 1 << k
        for j in range(k, -1, -1):
            gi, go, out = window(k, j, k)
            T = target(k, j, k)
            assert all((out.get(y) or [0] * N) == T[y] for y in range(N))
            heavy = sum(1 for x in range(N) if pc(x) >= j)
            print(f"  {k:2d} {N:4d} {j:2d} {gi:5d} {go:5d} {gi + go:5d}  {(gi + go) / N:6.3f}   {heavy:4d}   {heavy:4d}")
    print("D. the same counts without replay, larger k: cost of digit j alone = cost[0,j] - cost[0,j-1], per point")
    for k in (10, 12, 14, 16):
        N = 1 << k; prev = 0; row = []
        for d in range(0, k + 1):
            gi, go, _ = window(k, 0, d, replay=False); row.append((gi + go - prev) / N); prev = gi + go
        print(f"  k={k}: total {prev} = {prev / N:.3f} N (N log2 N = {N * k}); per digit j=0..k: " + " ".join(f"{t:.2f}" for t in row))
