# r-1: one size further (N = 64, halves of n = 32 points). L(32) cannot be enumerated (2^31 sign vectors), so:
#   lower bound, derived:  L(2n) >= 4 L(n) - 2n   (checked here on the exact values at n = 2, 4, 8, 16)
#   upper bound, by search: descent on the two halves c0, c1, objective = sum over the 32 characters of min(t'(c0 chi), t'(c1 chi)).
# Whole numbers, doubled units (node of two or more points = 2, single point = 1).
import numpy as np, sys, time, random
random.seed(11); rng = np.random.default_rng(11)
def tbatch(Fm):                       # Fm: (M, n) entries +1/-1 ; returns doubled t' for each row
    n = Fm.shape[1]
    def rec(lo, hi):
        if hi - lo == 1:
            s = Fm[:, lo]; return {o: (s != o).astype(np.int32) for o in (0, 1, -1)}
        mid = (lo + hi) // 2; A = rec(lo, mid); B = rec(mid, hi)
        S = {o: A[o] + B[o] for o in (0, 1, -1)}
        return {off: np.minimum.reduce([S[o] + (0 if o == off else 2) for o in (0, 1, -1)]) for off in (0, 1, -1)}
    return rec(0, n)[0]
def chars(n): return np.array([[(-1) ** bin(a & x).count('1') for x in range(n)] for a in range(n)], dtype=np.int8)
def prof(c, CH): return tbatch(c[None, :] * CH)
def exactL(n):                        # exhaustive, returns doubled L and one optimal pair
    CH = chars(n); idx = np.arange(1 << n)
    allc = (1 - 2 * ((idx[:, None] >> np.arange(n)[None, :]) & 1)).astype(np.int8)
    T = tbatch(allc)
    chim = np.array([sum(1 << x for x in range(n) if CH[a, x] < 0) for a in range(n)])
    P = T[idx[:, None] ^ chim[None, :]]
    U, first = np.unique(P, axis=0, return_index=True)
    best = (10 ** 9, 0, 0)
    for i in range(len(U)):
        s = np.minimum(U[i][None, :], U).sum(axis=1); j = int(s.argmin())
        if s[j] < best[0]: best = (int(s[j]), int(first[i]), int(first[j]))
    return best[0], allc[best[1]].copy(), allc[best[2]].copy()
ex = {}
for n in (2, 4, 8, 16):
    ex[n] = exactL(n); print("exact: n =", n, " L =", ex[n][0] / 2, " c0 =", ''.join('+-'[int(v < 0)] for v in ex[n][1]), " c1 =", ''.join('+-'[int(v < 0)] for v in ex[n][2]))
for n in (2, 4, 8):
    print("  check L(2n) >= 4 L(n) - 2n :", ex[2 * n][0] / 2, ">=", 4 * ex[n][0] / 2 - 2 * n, ex[2 * n][0] >= 4 * ex[n][0] - 4 * n)
sys.stdout.flush()
n = 32; CH = chars(n)
def obj(c0, c1): return int(np.minimum(prof(c0, CH), prof(c1, CH)).sum())
def descend(c0, c1, tmax):
    cur = obj(c0, c1); t0 = time.time(); side = 0
    eye = 1 - 2 * np.eye(n, dtype=np.int8)
    while time.time() - t0 < tmax:
        P0 = prof(c0, CH); P1 = prof(c1, CH)
        N0 = tbatch(((c0[None, :] * eye)[:, None, :] * CH[None, :, :]).reshape(n * n, n)).reshape(n, n)
        N1 = tbatch(((c1[None, :] * eye)[:, None, :] * CH[None, :, :]).reshape(n * n, n)).reshape(n, n)
        s0 = np.minimum(N0, P1[None, :]).sum(axis=1); s1 = np.minimum(N1, P0[None, :]).sum(axis=1)
        alls = np.concatenate([s0, s1]); m = int(alls.min())
        if m > cur or (m == cur and side >= 30): break
        side = side + 1 if m == cur else 0
        i = int(rng.choice(np.flatnonzero(alls == m)))
        if i < n: c0 = c0 * eye[i]
        else: c1 = c1 * eye[i - n]
        cur = m
    return cur, c0, c1
best = (10 ** 9, None, None); a0, a1 = ex[16][1], ex[16][2]
def lifts(c):
    return [np.concatenate([c, c]), np.concatenate([c, -c]), np.repeat(c, 2), (np.repeat(c, 2) * np.tile([1, -1], 16)).astype(np.int8)]
seeds = [(u, v) for u in lifts(a0) + lifts(a1) for v in lifts(a0) + lifts(a1)]
T0 = time.time()
for u, v in seeds:
    r = descend(u.astype(np.int8), v.astype(np.int8), 6)
    if r[0] < best[0]: best = r; print("  seed descent: L(32) <=", best[0] / 2, " at", int(time.time() - T0), "s"); sys.stdout.flush()
    if time.time() - T0 > 200: break
while time.time() - T0 < 330:
    u = rng.choice(np.array([1, -1], dtype=np.int8), n); v = rng.choice(np.array([1, -1], dtype=np.int8), n)
    r = descend(u, v, 8)
    if r[0] < best[0]: best = r; print("  random descent: L(32) <=", best[0] / 2, " at", int(time.time() - T0), "s"); sys.stdout.flush()
print("upper bound found: L(32) <=", best[0] / 2, " c0 =", ''.join('+-'[int(v < 0)] for v in best[1]), " c1 =", ''.join('+-'[int(v < 0)] for v in best[2]))
print("derived lower bound: L(32) >= 4 L(16) - 32 =", 4 * ex[16][0] / 2 - 32)
print("so at N = 64 the floor 2 L(32) lies between", 2 * (4 * ex[16][0] // 2 - 32), "and", best[0])
