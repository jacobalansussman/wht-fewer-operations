# replay.py (e-7-halftouch): exact replay of an anneal.c output. Reads the file, rebuilds C, recomputes S = H - A C B
# with Fractions, prints the count of non-zero entries, the matrices and the pattern of S.
import sys
from fractions import Fraction as Fr
def par(x): return bin(x).count("1") & 1
def Hm(n): return [[-1 if par(i & j) else 1 for j in range(n)] for i in range(n)]
def child(N, mode):
    def blk(sizes):
        m = sum(sizes); C = [[0]*m for _ in range(m)]; o = 0
        for s in sizes:
            h = Hm(s)
            for i in range(s):
                for j in range(s): C[o+i][o+j] = h[i][j]
            o += s
        return C
    return blk({0:[N//2], 1:[N//2,N//2], 2:[N//4,N//4], 3:[N//2,N//4], 4:[N//4]*3}[mode])
def mul(X, Y): return [[sum(a*b for a, b in zip(r, c)) for c in zip(*Y)] for r in X]
def load(fn):
    L = open(fn).read().split("\n"); hd = L[0].split(); N = int(hd[3]); mode = int(hd[5]); m = int(hd[7])
    ia = L.index("A"); ib = L.index("B")
    A = [[Fr(int(v), 2) for v in L[ia+1+x].split()] for x in range(N)]
    B = [[Fr(int(v), 2) for v in L[ib+1+j].split()] for j in range(m)]
    return N, mode, m, A, B
def fmt(v): return "." if v == 0 else str(v)
def show(X, name):
    print(name)
    for r in X: print("  " + " ".join(f"{fmt(v):>4}" for v in r))
if __name__ == "__main__":
    N, mode, m, A, B = load(sys.argv[1])
    C = child(N, mode); H = Hm(N)
    M = mul(mul(A, C), B)
    S = [[H[x][y] - M[x][y] for y in range(N)] for x in range(N)]
    nnz = sum(1 for r in S for v in r if v != 0)
    print("N", N, "mode", mode, "m", m, "EXACT nnz(S) =", nnz, " nnz(A) =", sum(1 for r in A for v in r if v != 0), " nnz(B) =", sum(1 for r in B for v in r if v != 0))
    print("max non-zeros: row of A", max(sum(1 for v in r if v != 0) for r in A), "col of A", max(sum(1 for v in c if v != 0) for c in zip(*A)),
          "row of B", max(sum(1 for v in r if v != 0) for r in B), "col of B", max(sum(1 for v in c if v != 0) for c in zip(*B)))
    print("non-zeros of S per row:", [sum(1 for v in r if v != 0) for r in S], " per column:", [sum(1 for v in c if v != 0) for c in zip(*S)])
    if N <= 16 and "-q" not in sys.argv:
        show(A, "A"); show(B, "B"); show(S, "S = H - A C B")
