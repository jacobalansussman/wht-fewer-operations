#!/usr/bin/env python3
"""e-4-passes / anneal4.py   Gaussian integers held in two int64 arrays (real, imaginary): exact.

E = D * (S_r H S_c) * D^T  with S_r, S_c free diagonal matrices of FOURTH ROOTS OF UNITY (a pass coefficient
+-1 or +-i is the same as such a phase), D = plain difference in a free row order / column order.
Counts non-zeros N of E.  Gate count (G): pass + E entry by entry + pass = N + d - 2.
usage: anneal4.py d iters seed
"""
import sys, random
import numpy as np

def expo(d):
    a = np.arange(d); x = a[:, None] & a[None, :]; pc = np.zeros((d, d), dtype=np.int64)
    while x.any():
        pc += x & 1; x >>= 1
    return 2 * (pc & 1)          # exponent of i

RE = np.array([1, 0, -1, 0], dtype=np.int64); IM = np.array([0, 1, 0, -1], dtype=np.int64)

def emat(K, pi, sig, er, ec):
    k = (K[np.ix_(pi, sig)] + er[:, None] + ec[None, :]) & 3
    out = []
    for T in (RE, IM):
        M = T[k]
        M[1:] = M[1:] - M[:-1]
        M[:, 1:] = M[:, 1:] - M[:, :-1]
        out.append(M)
    return out

def nnz(K, pi, sig, er, ec):
    a, b = emat(K, pi, sig, er, ec)
    return int(np.count_nonzero(a | b)) if False else int(np.count_nonzero((a != 0) | (b != 0)))

def run(d, iters, seed):
    rng = random.Random(seed); K = expo(d)
    g = [i ^ (i >> 1) for i in range(d)]
    pi = np.array(g); sig = np.array(g)
    er = np.array([rng.randrange(4) for _ in range(d)]); ec = np.array([rng.randrange(4) for _ in range(d)])
    cur = nnz(K, pi, sig, er, ec); best = (cur, pi.copy(), sig.copy(), er.copy(), ec.copy())
    T0, T1 = 2.0, 0.15
    for it in range(iters):
        T = T0 * (T1 / T0) ** (it / iters)
        which = rng.random()
        arr, ph = (pi, er) if rng.random() < 0.5 else (sig, ec)
        i, j = sorted(rng.sample(range(d), 2))
        if which < 0.4:
            arr[i], arr[j] = arr[j], arr[i]; ph[i], ph[j] = ph[j], ph[i]; undo = (0, arr, ph, i, j, 0)
        elif which < 0.7:
            arr[i:j + 1] = arr[i:j + 1][::-1].copy(); ph[i:j + 1] = ph[i:j + 1][::-1].copy(); undo = (1, arr, ph, i, j, 0)
        else:
            old = int(ph[i]); ph[i] = (old + rng.randrange(1, 4)) & 3; undo = (2, arr, ph, i, j, old)
        new = nnz(K, pi, sig, er, ec)
        if new <= cur or rng.random() < np.exp((cur - new) / T):
            cur = new
            if cur < best[0]: best = (cur, pi.copy(), sig.copy(), er.copy(), ec.copy())
        else:
            kind, arr, ph, i, j, old = undo
            if kind == 0:
                arr[i], arr[j] = arr[j], arr[i]; ph[i], ph[j] = ph[j], ph[i]
            elif kind == 1:
                arr[i:j + 1] = arr[i:j + 1][::-1].copy(); ph[i:j + 1] = ph[i:j + 1][::-1].copy()
            else:
                ph[i] = old
    n, pi, sig, er, ec = best
    m = d.bit_length() - 1
    print(f"d={d} fourth-root phases seed={seed} iters={iters}: best non-zeros {n}  (d*m-1 = {d*m-1})  gates (G) {n + d - 2}  textbook {d*m}  best known (G) {7*d*m//8 if m % 2 == 0 else '22 at d=8'}")
    print("  row order", pi.tolist(), "phase exponents", er.tolist())
    print("  col order", sig.tolist(), "phase exponents", ec.tolist())
    a, b = emat(K, pi, sig, er, ec)
    print("  non-zeros per row", np.count_nonzero((a != 0) | (b != 0), axis=1).tolist(), " rows using i:", int(np.count_nonzero(np.any(b != 0, axis=1))))
    if d <= 16:
        for r in range(d):
            print("    ", " ".join((f"{int(a[r][c])}{int(b[r][c]):+d}i" if b[r][c] else f"{int(a[r][c])}").rjust(6) for c in range(d)))

if __name__ == "__main__":
    run(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
