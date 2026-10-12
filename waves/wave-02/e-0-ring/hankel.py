#!/usr/bin/env python3
# e-0-ring / hankel.py : the Hankel matrix of one period of the +-1 maximal-length sequence, c[m] = (-1)^Trace(theta^(m+shift)).
# A[i][j] = c[i+j], 0 <= i,j < h = 2^(k-1): uses each of the n = 2^k - 1 entries of one period.
# Rank modulo two large primes (numpy int64).  Full rank mod p  =>  full rank over the rationals (exact).
# Deficient mod both primes => deficient over the rationals, candidate (the chance of a false alarm is about 1/p each).
# Question: is the lost rank at k = 6 structural (n has a repeated prime factor) or does it depend on the starting point?
import sys, time
import numpy as np
P1, P2 = 2147483647, 2147483629

def prim_polys(k):
    # all primitive polynomials of degree k over F_2, as bit masks
    n = (1 << k) - 1; out = []
    for p in range((1 << k) | 1, 1 << (k + 1), 2):
        v = 1; ok = True
        for m in range(1, n):
            v <<= 1
            if v >> k: v ^= p
            if v == 1: ok = False; break
        if ok:
            v <<= 1
            if v >> k: v ^= p
            if v == 1: out.append(p)
    return out

def seq(k, p):
    n = (1 << k) - 1
    pw = [1]
    for _ in range(n - 1):
        v = pw[-1] << 1
        if v >> k: v ^= p
        pw.append(v)
    # trace via the linear functional: Trace(theta^m) computed from the recurrence: use dual basis trick = brute force
    assert len(set(pw)) == n, 'polynomial is not primitive'
    idx = {v: i for i, v in enumerate(pw)}
    def mul(a, b):
        if a == 0 or b == 0: return 0
        return pw[(idx[a] + idx[b]) % n]
    tr = []
    for v in pw:
        s = 0; w = v
        for _ in range(k):
            s ^= w; w = mul(w, w)
        tr.append(s)
    assert set(tr) <= {0, 1} and sum(tr) == (n + 1) // 2
    return np.array([1 - 2 * t for t in tr], dtype=np.int64)

def rank_mod(A, p):
    A = A % p; m = A.shape[0]; r = 0
    for c in range(m):
        col = A[r:, c]
        nz = np.nonzero(col)[0]
        if len(nz) == 0: continue
        piv = r + nz[0]
        if piv != r: A[[r, piv]] = A[[piv, r]]
        inv = pow(int(A[r, c]), p - 2, p)
        A[r] = (A[r] * inv) % p
        rows = np.nonzero(A[r + 1:, c])[0] + r + 1
        if len(rows):
            A[rows, c:] = (A[rows, c:] - np.outer(A[rows, c], A[r, c:])) % p
        r += 1
        if r == m: break
    return r

def hank(c, shift):
    n = len(c); h = (n + 1) // 2
    i = np.arange(h)
    return c[(i[:, None] + i[None, :] + shift) % n]

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "shifts":                       # every primitive polynomial and every starting point
        for k in range(3, int(sys.argv[2]) + 1):
            n = (1 << k) - 1; h = (n + 1) // 2
            pp = prim_polys(k)
            tot = {}
            t0 = time.time()
            for p in pp:
                c = seq(k, p)
                defs = []
                for s in range(n):
                    r = rank_mod(hank(c, s), P1)
                    if r < h: defs.append((s, h - r))
                tot[bin(p)] = defs
            nd = sum(len(v) for v in tot.values())
            print("k=%d n=%d size %d: %d primitive polynomials x %d starting points; singular Hankel matrices (mod P1): %d of %d  [%.0fs]"
                  % (k, n, h, len(pp), n, nd, len(pp) * n, time.time() - t0), flush=True)
            for p, v in tot.items():
                if v: print("    poly %s: (start, lost rank) %s" % (p, v[:40]), flush=True)
    elif mode == "scan":                       # one polynomial, every starting point in a range, one prime
        k = int(sys.argv[2]); lo, hi, step = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
        p = prim_polys(k)[int(sys.argv[6]) if len(sys.argv) > 6 else 0]
        c = seq(k, p); n = len(c); h = (n + 1) // 2; defs = []; t0 = time.time(); cnt = 0
        for s in range(lo, hi, step):
            r = rank_mod(hank(c, s), P1); cnt += 1
            if r < h: defs.append((s, h - r))
        print("k=%d n=%d poly %s: %d starting points scanned (%d..%d step %d); singular (mod P1): %d  %s  [%.0fs]"
              % (k, n, bin(p), cnt, lo, hi, step, len(defs), defs[:60], time.time() - t0), flush=True)
    else:                                      # one polynomial, a few starting points, two primes
        k = int(sys.argv[2]); shifts = [int(x) for x in sys.argv[3:]] or [0]
        pp = prim_polys(k) if k <= 10 else None
        p = pp[0] if pp else {12: 0b1000001010011, 11: 0b100000000101}[k]
        c = seq(k, p); n = len(c); h = (n + 1) // 2
        for s in shifts:
            t0 = time.time()
            r1 = rank_mod(hank(c, s), P1); r2 = rank_mod(hank(c, s), P2)
            print("k=%d n=%d poly %s start %d: rank %d (mod P1), %d (mod P2) of %d  [%.0fs]" % (k, n, bin(p), s, r1, r2, h, time.time() - t0), flush=True)
