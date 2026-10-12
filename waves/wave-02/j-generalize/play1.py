# j-generalize play 1: the numbers axis.  Exact integer arithmetic (Python ints).
# (a) H = Z D Z^T, T_t = Z D_t Z^T for every t;  (b) H mod 2^b = sum_{j<b} (-2)^j Z_j Z_j^T;
# (c) a program for H mod 2^b with its gate count (G): gate = one a*u+b*v, scalings free;
# (d) the count recursion for large k.
import sys, random
from fractions import Fraction
from functools import lru_cache
from math import comb

def popc(a): return bin(a).count("1")

def Hmat(k):
    N = 1 << k
    return [[(-1) ** popc(x & y) for y in range(N)] for x in range(N)]

def Zmat(k):
    N = 1 << k
    return [[1 if (x & S) == S else 0 for S in range(N)] for x in range(N)]   # Z[x][S] = [S inside x]

def mul(A, B):
    n, m, p = len(A), len(B), len(B[0])
    return [[sum(A[i][l] * B[l][j] for l in range(m)) for j in range(p)] for i in range(n)]

def tr(A): return [list(r) for r in zip(*A)]

def rank_q(A):
    A = [[Fraction(v) for v in r] for r in A]
    r = 0
    for c in range(len(A[0])):
        p = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c] / A[r][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        r += 1
    return r

print("== (a),(b): identities, k = 1..6")
for k in range(1, 7):
    N = 1 << k
    H, Z = Hmat(k), Zmat(k)
    ok = True
    for t in (-1, 3, -5, 7):
        D = [[(t - 1) ** popc(S) if S == T else 0 for T in range(N)] for S in range(N)]
        T_t = [[t ** popc(x & y) for y in range(N)] for x in range(N)]
        ok &= mul(mul(Z, D), tr(Z)) == T_t
    # truncations
    line = []
    for b in range(1, k + 2):
        Hb = [[sum((-2) ** j * comb(popc(x & y), j) for j in range(b)) for y in range(N)] for x in range(N)]
        cong = all((Hb[x][y] - H[x][y]) % (1 << b) == 0 for x in range(N) for y in range(N))
        rk = rank_q(Hb) if k <= 5 else -1
        line.append((b, cong, rk, sum(comb(k, j) for j in range(b))))
    print(f"k={k}: T_t = Z D_t Z^T for t=-1,3,-5,7: {ok};  (b, H_b==H mod 2^b, rank_Q(H_b), sum_j<b C(k,j)):", line)

# (c) the program.  analysis: superset sums f(S) = sum_{x contains S} x[x] for |S| < b.
gates = 0
def analysis(x, k, b):
    """returns dict S -> sum over addresses containing S, for |S| < b (S as bitmask over k bits)"""
    global gates
    if b <= 0: return {}
    if k == 0: return {0: x[0]}
    h = 1 << (k - 1)
    x0, x1 = x[:h], x[h:]
    g = [u + v for u, v in zip(x0, x1)]; gates += h
    out = dict(analysis(g, k - 1, b))
    for S, v in analysis(x1, k - 1, b - 1).items():
        out[S | h] = v
    return out

def synth(c, k, b):
    """out[a] = sum_{S inside a, |S|<b} c[S]"""
    global gates
    if b <= 0: return None                       # identically zero, nothing to add
    if k == 0: return [c.get(0, 0)]
    h = 1 << (k - 1)
    lo = synth({S: v for S, v in c.items() if not S & h}, k - 1, b)
    hi = synth({S ^ h: v for S, v in c.items() if S & h}, k - 1, b - 1)
    if hi is None:
        return lo + lo                           # fan-out, no gate
    if b - 1 == 1:
        top = [u + hi[0] for u in lo]; gates += h   # hi is a constant table
    else:
        top = [u + v for u, v in zip(lo, hi)]; gates += h
    return lo + top

print("== (c): program for H mod 2^b, checked on random integer data, gate count (G)")
random.seed(7)
for k in (6, 8, 10):
    N = 1 << k
    x = [random.randrange(-10**6, 10**6) for _ in range(N)]
    # exact transform by the textbook
    y = x[:]
    for i in range(k):
        s = 1 << i
        for a in range(N):
            if not a & s:
                u, v = y[a], y[a | s]; y[a], y[a | s] = u + v, u - v
    row = []
    for b in range(1, k + 2):
        gates = 0
        f = analysis(x, k, b)
        c = {S: (-2) ** popc(S) * v for S, v in f.items()}       # diagonal layer: free scalings in (G)
        out = synth(c, k, b)
        good = all((o - t) % (1 << b) == 0 for o, t in zip(out, y))
        exact = out == y
        row.append(f"b={b}:{gates / N:.2f}{'ok' if good else 'BAD'}{'=' if exact else ''}")
    print(f"k={k} N={N} gates/N by b (ok = right mod 2^b, '=' = exactly H x; textbook = {k}):", " ".join(row))

# (d) counts for large k
@lru_cache(None)
def An(k, b):
    if b <= 0 or k == 0: return 0
    return (1 << (k - 1)) + An(k - 1, b) + An(k - 1, b - 1)
@lru_cache(None)
def Sy(k, b):
    if b <= 0 or k == 0: return 0
    return Sy(k - 1, b) + Sy(k - 1, b - 1) + ((1 << (k - 1)) if b - 1 >= 1 else 0)
sys.setrecursionlimit(10000)
print("== (d): gates per point of the mod-2^b program, analysis+synthesis")
for k in (24, 48, 96):
    N = 1 << k
    print(f"k={k}:", " ".join(f"b={b}:{(An(k, b) + Sy(k, b)) / N:.2f}" for b in (1, 2, 3, 4, 6, 8, k // 4, k // 2, 3 * k // 4, k + 1)))
