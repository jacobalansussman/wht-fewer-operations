# chain.py (critic b-2): what the counting chain of Lemma 4 forces at rho = 3/4 and 1/2, with e-7's cap |T|^2/N and with my sharper cap.
from fractions import Fraction as Fr
def chain_bound(N, m, dminus, improved):
    r = m - dminus; best = (0, 0)
    def cap(T):
        c = Fr(T * T, N)
        if improved: c = min(c, dminus - (N - T) + Fr((N - T) ** 2, N))
        return c
    for t in range(max(r, 0) + 1, m + 1):
        T = next(T for T in range(0, N + 1) if cap(T) >= t - r)
        b = -(-m * T // t)
        if b > best[0]: best = (b, t)
    return best
for N in (16, 64, 256, 1024, 4096):
    s = int(N ** 0.5)
    for lab, m, dm in (("rho=3/4, identity", 3 * N // 4, N // 2), ("rho=1/2, identity", N // 2, N // 2), ("rho=1/2, best relabelling", N // 2, (N - s) // 2), ("rho=5/8, identity", 5 * N // 8, N // 2)):
        a = chain_bound(N, m, dm, False); b = chain_bound(N, m, dm, True)
        print(f"N={N:5d} {lab:26s}: nnz(A)/N >= {a[0]/N:.3f} (e-7's cap)   >= {b[0]/N:.3f} (sharper cap)")
