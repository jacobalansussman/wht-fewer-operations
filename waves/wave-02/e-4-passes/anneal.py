#!/usr/bin/env python3
"""e-4-passes / anneal.py   integer arithmetic (numpy int64, entries stay below 2^(2k+1)).

E = (difference in a row order)^k  *  S_r H S_c  *  (difference in a column order)^k transposed,
with H[a][x] = (-1)^popcount(a&x), S_r, S_c free signs (a coefficient -1 in a pass is the same as a sign), and the
row order pi, column order sig free.  Counts the non-zero entries N of E.  Gate count (G) of
"k passes, then E applied entry by entry, then k passes" is  N - d + 2k(d-1).
usage: anneal.py d k iters seed      ('orders' as first argument prints the three named orders at d=16)
"""
import sys, random
import numpy as np

def had(d):
    a = np.arange(d)
    pc = np.zeros((d, d), dtype=np.int64)
    x = a[:, None] & a[None, :]
    while x.any():
        pc += x & 1; x >>= 1
    return 1 - 2 * (pc & 1)

def diffs(M, k):
    E = M.copy()
    for _ in range(k):
        E[1:] = E[1:] - E[:-1]
    for _ in range(k):
        E[:, 1:] = E[:, 1:] - E[:, :-1]
    return E

def nnz(H, pi, sig, sr, sc, k):
    M = H[np.ix_(pi, sig)] * sr[:, None] * sc[None, :]
    return int(np.count_nonzero(diffs(M, k)))

def gray(d): return [i ^ (i >> 1) for i in range(d)]

def named():
    d = 16; H = had(d)
    ones = np.ones(d, dtype=np.int64)
    plain = list(range(d)); g = gray(d)
    # field-logarithm order in GF(16) = GF(2)[t]/(t^4+t+1): 0, 1, t, t^2, ...
    fl = [0]; x = 1
    for _ in range(15):
        fl.append(x); x <<= 1
        if x & 16: x ^= 0b10011
    # trace-form matrix: T[a][x] = (-1)^Tr(a*x)
    def mul(a, b):
        r = 0
        while b:
            if b & 1: r ^= a
            a <<= 1
            if a & 16: a ^= 0b10011
            b >>= 1
        return r
    def tr(a):
        s = 0; y = a
        for _ in range(4):
            s ^= y; y = mul(y, y)
        return s & 1
    T = np.array([[1 - 2 * tr(mul(a, x)) for x in range(d)] for a in range(d)], dtype=np.int64)
    rev = [int(format(i, "04b")[::-1], 2) for i in range(d)]
    grev = [rev[v] for v in g]
    for name, M, pi, sig in (("plain / plain", H, plain, plain), ("Gray / Gray", H, g, g),
                             ("Gray / bit-reversed Gray", H, g, grev), ("plain / bit-reversed", H, plain, rev),
                             ("field-log / field-log (trace form)", T, fl, fl)):
        for k in (1, 2):
            n = nnz(M, np.array(pi), np.array(sig), ones, ones, k)
            print(f"  d=16 {name:38s} differences applied {k}x each side: non-zeros {n:4d} of 256   gates (G) {n - d + 2*k*(d-1)}")

def anneal(d, k, iters, seed):
    rng = random.Random(seed); H = had(d)
    pi = np.array(gray(d)); sig = np.array(gray(d))
    sr = np.ones(d, dtype=np.int64); sc = np.ones(d, dtype=np.int64)
    cur = nnz(H, pi, sig, sr, sc, k); best = (cur, pi.copy(), sig.copy(), sr.copy(), sc.copy())
    T0, T1 = 2.0, 0.15
    for it in range(iters):
        T = T0 * (T1 / T0) ** (it / iters)
        which = rng.random()
        arr = pi if rng.random() < 0.5 else sig
        sg = sr if arr is pi else sc
        i, j = sorted(rng.sample(range(d), 2))
        if which < 0.45:
            arr[i], arr[j] = arr[j], arr[i]; sg[i], sg[j] = sg[j], sg[i]
            undo = ("swap", arr, sg, i, j)
        elif which < 0.85:
            arr[i:j + 1] = arr[i:j + 1][::-1].copy(); sg[i:j + 1] = sg[i:j + 1][::-1].copy()
            undo = ("rev", arr, sg, i, j)
        else:
            sg[i] = -sg[i]; undo = ("sign", arr, sg, i, j)
        new = nnz(H, pi, sig, sr, sc, k)
        if new <= cur or rng.random() < np.exp((cur - new) / T):
            cur = new
            if cur < best[0]: best = (cur, pi.copy(), sig.copy(), sr.copy(), sc.copy())
        else:
            kind, arr, sg, i, j = undo
            if kind == "swap":
                arr[i], arr[j] = arr[j], arr[i]; sg[i], sg[j] = sg[j], sg[i]
            elif kind == "rev":
                arr[i:j + 1] = arr[i:j + 1][::-1].copy(); sg[i:j + 1] = sg[i:j + 1][::-1].copy()
            else:
                sg[i] = -sg[i]
    n, pi, sig, sr, sc = best
    m = d.bit_length() - 1
    print(f"d={d} k={k} seed={seed} iters={iters}: best non-zeros {n}   (d*m - 1 = {d*m-1}, d*m = {d*m})   gates (G) {n - d + 2*k*(d-1)}  textbook {d*m}")
    print("  row order", pi.tolist(), "signs", sr.tolist())
    print("  col order", sig.tolist(), "signs", sc.tolist())
    E = diffs(H[np.ix_(pi, sig)] * sr[:, None] * sc[None, :], k)
    print("  non-zeros per row", np.count_nonzero(E, axis=1).tolist(), " max |entry|", int(np.abs(E).max()))
    if d <= 16:
        for r in E.tolist(): print("    ", r)

if __name__ == "__main__":
    if sys.argv[1] == "orders": named()
    else: anneal(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
