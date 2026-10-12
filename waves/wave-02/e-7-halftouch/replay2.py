# replay2.py (e-7-halftouch): exact replay of an altmin.c output. The coefficients come back as doubles; they are turned into
# fractions (limit_denominator) and S = H - A C B is recomputed with exact rational arithmetic. The count printed is exact
# for the rational matrices shown, whatever the doubles were.
import sys
from fractions import Fraction as Fr
def par(x): return bin(x).count("1") & 1
def Hm(n): return [[-1 if par(i & j) else 1 for j in range(n)] for i in range(n)]
def child(N, mode):
    if mode == 8: return [[1 if i == j else 0 for j in range(N//2)] for i in range(N//2)]
    sizes = {0:[N//2], 1:[N//2]*2, 2:[N//4]*2, 3:[N//2,N//4], 4:[N//4]*3, 5:[N//4]*4, 6:[N//4], 7:[N//8]*7}[mode]
    m = sum(sizes); C = [[0]*m for _ in range(m)]; o = 0
    for s in sizes:
        h = Hm(s)
        for i in range(s):
            for j in range(s): C[o+i][o+j] = h[i][j]
        o += s
    return C
def mul(X, Y):
    Yt = list(zip(*Y)); return [[sum(a*b for a, b in zip(r, c) if a != 0 and b != 0) for c in Yt] for r in X]
def rank(M):
    M = [list(map(Fr, r)) for r in M]; r = 0
    for c in range(len(M[0])):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        for i in range(r+1, len(M)):
            if M[i][c] != 0:
                f = M[i][c] / M[r][c]; M[i] = [a - f*b for a, b in zip(M[i], M[r])]
        r += 1
    return r
def load(fn):
    L = open(fn).read().split("\n"); hd = L[0].split(); N = int(hd[3]); mode = int(hd[5]); m = int(hd[7])
    ia = L.index("A"); ib = L.index("B")
    cv = lambda v: Fr(float(v)).limit_denominator(100000) if abs(float(v)) > 1e-9 else Fr(0)
    A = [[cv(v) for v in L[ia+1+x].split()] for x in range(N)]
    B = [[cv(v) for v in L[ib+1+j].split()] for j in range(m)]
    return hd, N, mode, m, A, B
def fmt(v): return "." if v == 0 else str(v)
def show(X, name):
    print(name)
    for r in X: print("  " + " ".join(f"{fmt(v):>5}" for v in r))
if __name__ == "__main__":
    hd, N, mode, m, A, B = load(sys.argv[1])
    C = child(N, mode); H = Hm(N)
    M = mul(mul(A, C), B)
    S = [[H[x][y] - M[x][y] for y in range(N)] for x in range(N)]
    nz = lambda X: sum(1 for r in X for v in r if v != 0)
    print("file", sys.argv[1], "| claimed", hd[hd.index("best_nnz")+1], "| N", N, "mode", mode, "m", m, "| EXACT nnz(S) =", nz(S), "| nnz(A) =", nz(A), "nnz(B) =", nz(B), "| rank S =", rank(S), "rank(H-S) =", rank(M))
    print("  max per row of A", max(sum(1 for v in r if v != 0) for r in A), "per col of A", max(sum(1 for v in c if v != 0) for c in zip(*A)),
          "| per row of B", max(sum(1 for v in r if v != 0) for r in B), "per col of B", max(sum(1 for v in c if v != 0) for c in zip(*B)))
    print("  S per row:", [sum(1 for v in r if v != 0) for r in S], " per column:", [sum(1 for v in c if v != 0) for c in zip(*S)])
    print("  values in S:", sorted(set(v for r in S for v in r if v != 0)), " values in A:", sorted(set(v for r in A for v in r if v != 0)), " values in B:", sorted(set(v for r in B for v in r if v != 0)))
    # gate count (G): a row with t non-zeros costs t-1 gates when computed alone; S adds one gate per non-zero entry
    gB = sum(max(0, sum(1 for v in r if v != 0) - 1) for r in B); gA = sum(max(0, sum(1 for v in r if v != 0) - 1) for r in A)
    used = sum(1 for r in B if any(v != 0 for v in r))
    print("  naive gate count (G), no sharing: B", gB, "+ A", gA, "+ S", nz(S), "=", gB + gA + nz(S), "plus the child calls; child inputs actually used:", used, "of", m)
    if N <= 16 and "-q" not in sys.argv:
        show(A, "A"); show(B, "B"); show(S, "S = H - A C B")
