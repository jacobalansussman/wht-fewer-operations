# tensor.py (e-7-halftouch): exact check of the doubling rule.
# If H_N0 = S0 + A0 * H_(N0/2) * B0 then, for every M = 2^j,
#     H_(M*N0) = (H_M (x) S0) + (I_M (x) A0) * H_(M*N0/2) * (I_M (x) B0)
# so one half-length child still suffices, A and B keep their sparsity, and the remainder has M^2 * nnz(S0) entries.
import sys
from fractions import Fraction as Fr
from replay2 import load, child, Hm, mul
def kron(X, Y): return [[a * b for a in rx for b in ry] for rx in X for ry in Y]
def eye(n): return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
hd, N0, mode, m, A0, B0 = load(sys.argv[1]); assert mode == 0
H0 = Hm(N0); M0 = mul(mul(A0, Hm(N0 // 2)), B0); S0 = [[H0[x][y] - M0[x][y] for y in range(N0)] for x in range(N0)]
nz = lambda X: sum(1 for r in X for v in r if v != 0)
print("base:", sys.argv[1], "N0 =", N0, "nnz(S0) =", nz(S0), "rows of S0 that are not zero:", sum(1 for r in S0 if any(v != 0 for v in r)))
for M in [2, 4]:
    N = M * N0
    A = kron(eye(M), A0); B = kron(eye(M), B0); S = kron(Hm(M), S0)
    L = mul(mul(A, Hm(N // 2)), B); H = Hm(N)
    ok = all(H[x][y] == S[x][y] + L[x][y] for x in range(N) for y in range(N))
    print(f"N = {N}: identity exact: {ok}; nnz(S) = {nz(S)} = {Fr(nz(S), N)} * N = {float(Fr(nz(S), N*N)):.4f} * N^2; max per row of A {max(sum(1 for v in r if v != 0) for r in A)}, per column of B {max(sum(1 for v in c if v != 0) for c in zip(*B))}; textbook split has N^2/4 = {N*N//4}")
    if len(sys.argv) > 2:      # write the tensored solution as a starting point for altmin.c
        with open(f"{sys.argv[2]}{N}.txt", "w") as f:
            f.write(f"k {N.bit_length()-1} N {N} mode 0 m {N//2} a 3 b 3 freediag 0 best_nnz {nz(S)} tensored\nA\n")
            for r in A: f.write(" ".join(str(float(v)) for v in r) + "\n")
            f.write("B\n")
            for r in B: f.write(" ".join(str(float(v)) for v in r) + "\n")
