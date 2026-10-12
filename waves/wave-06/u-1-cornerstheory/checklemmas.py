# u-1: direct checks of the three lemmas on real pictures (the best found at 16, 32, 64 points; all 168 optimal 8-point pairs; random orders).
import re, ast, random, sys
from math import comb
from lib import *
def load(fn):
    txt = open(fn).read().split('BEST')[-1]
    rows = ast.literal_eval(re.search(r'rows (\[[^\]]*\])', txt).group(1)); cols = ast.literal_eval(re.search(r'cols (\[[^\]]*\])', txt).group(1)); return rows, cols
def runs_of(flags):
    out = []; start = None
    for i, f in enumerate(flags + [False]):
        if f and start is None: start = i
        if not f and start is not None: out.append((start, i - 1)); start = None
    return out
def check(rows, cols, name, verbose=True):
    N = len(rows); k = N.bit_length() - 1; pos = {T: b for b, T in enumerate(cols)}
    c, M = corners(rows, cols); ok = True
    # Lemma 1: rows of M with a single non-zero number at most 2k+1
    single = sum(1 for r in M if sum(1 for v in r if v) == 1); ok &= single <= 2 * k + 1
    # per step: top (the larger endpoint not inside the other), R+ = inputs inside the top and not inside the other, its runs
    thru = [0] * N; rplus = []; bysize = {}
    for a in range(N):
        S = rows[a]; Sp = rows[a + 1] if a + 1 < N else None
        if Sp is not None and bin(Sp).count('1') > bin(S).count('1'): S, Sp = Sp, S
        flags = [((S & T) == T) and not (Sp is not None and (Sp & T) == T) for T in cols]
        rr = runs_of(flags); nz = sum(1 for v in M[a] if v)
        ok &= nz >= len(rr)                                    # non-zeros of the step >= runs of R+
        ok &= 2 * sum(flags) >= (1 << bin(S).count('1'))     # |R+| >= 2^(s-1)
        for (u, v) in rr:
            if u <= pos[S] <= v:
                for b in range(u, v + 1): thru[b] += 1          # the top component (the run that holds the input with the top's own address)
        rplus.append((bin(S).count('1'), S, rr)); bysize.setdefault(bin(S).count('1'), []).append((len(rr), nz))
    ok &= max(thru) <= 4 * (k + 1)                              # Lemma 2
    # Lemma 3 (window count): for every window length L and top size s: pairs (step, window inside a run of R+) <= 2 (N-L+1) comb(k-lam, s-lam)
    worst = 0.0
    for L in range(1, N + 1):
        lam = (L - 1).bit_length(); cnt = {}
        for s, S, rr in rplus:
            cnt[s] = cnt.get(s, 0) + sum(max(0, v - u + 1 - L + 1) for u, v in rr)
        for s, n in cnt.items():
            cap = 2 * (N - L + 1) * (comb(k - lam, s - lam) if lam <= s else 0)
            if n > cap: ok = False
            if cap: worst = max(worst, n / cap)
    if verbose:
        print(f"{name}: N={N} corners={c}; single-non-zero steps {single} (<= {2*k+1}); most top components through one input {max(thru)} (<= {4*(k+1)}); window count at most {worst:.2f} of its cap; all lemma checks pass: {ok}")
        for s in sorted(bysize): print(f"     top size {s}: {len(bysize[s])} steps; runs of R+ {sorted(x for x, _ in bysize[s])}; non-zeros {sorted(y for _, y in bysize[s])}")
    return ok
Q = 'waves/wave-05/q-cross/'
for fn in ('cat3_8.out', 'cat3_16.out', 'cat3g_32.out', 'cat3g_64.out'):
    r, c = load(Q + fn); check(r, c, fn)
allok = True; n = 0
for line in open('opt8.txt'):
    p = line.split('|'); allok &= check(list(map(int, p[1].split())), list(map(int, p[2].split())), '', False); n += 1
print("all", n, "optimal 8-point pairs pass the three lemma checks:", allok)
random.seed(1); allok = True; n = 0
for k in (2, 3, 4, 5, 6, 7):
    for t in range(60 if k < 7 else 10):
        r = list(range(1 << k)); c = list(range(1 << k)); random.shuffle(r); random.shuffle(c)
        if t % 3 == 0: r.sort(key=lambda x: x ^ (x >> 1)); 
        if t % 3 == 1: c.sort(key=lambda x: (bin(x).count('1'), x))
        allok &= check(r, c, '', False); n += 1
print("random and half-regular orders,", n, "pictures at 4 to 128 points pass:", allok)
