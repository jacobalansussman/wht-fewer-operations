# j-generalize play 2: the group axis and the data axis.
# Entries here are 0, +-1, +-i or small integer multiples: complex doubles hold them exactly for parts A, C, D.
# Part B (cyclic groups of order 16, 32) uses roots of unity in floating point: marked as such.
import numpy as np, itertools, cmath
from math import comb

def H(k):
    M = np.array([[1.0]])
    for _ in range(k): M = np.kron(M, np.array([[1, 1], [1, -1]]))
    return M

def comps(B, tol=1e-9):
    """sizes of the connected blocks of B (rows and columns joined by non-zero entries)"""
    n = B.shape[0]; par = list(range(2 * n))
    def f(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for i in range(n):
        for j in range(n):
            if abs(B[i, j]) > tol: par[f(i)] = f(n + j)
    c = {}
    for i in range(n): c[f(i)] = c.get(f(i), 0) + 1
    return sorted(c.values())

print("== A. Z_4 against Z_2 x Z_2 (exact)")
F4 = np.array([[1j ** (a * b) for b in range(4)] for a in range(4)])
B4 = F4 @ H(2) / 4                      # bridge: F4 = B4 . H4
print("bridge F4.H4^-1 =\n", np.round(B4, 3))
print("blocks:", comps(B4), " non-zeros:", int((abs(B4) > 1e-9).sum()))
R = np.array([[1 + 1j, 1 - 1j], [1 - 1j, 1 + 1j]]) / 2
print("2x2 block squared = swap:", np.allclose(R @ R, [[0, 1], [1, 0]]))
for m in (2, 3, 4):
    Bm = B4
    for _ in range(m - 1): Bm = np.kron(Bm, B4)
    n = 4 ** m
    cs = comps(Bm)
    fixed = cs.count(1)
    cost = sum(s * np.log2(s) for s in cs)          # 2x2 mixes: (size/2)*log2(size) of them, 2 gates each
    print(f"m={m}: n={n}, untouched points {fixed} (= 2^m), block sizes {sorted(set(cs))}, "
          f"gates (G) {cost:.0f} = {cost / n:.3f} per point; transform itself {2 * m} per point")

print("== B. cyclic group of order 2^k against Z_2^k (floating point)")
for k in (3, 4, 5):
    n = 1 << k
    F = np.array([[cmath.exp(2j * cmath.pi * a * b / n) for b in range(n)] for a in range(n)])
    Br = F @ H(k) / n
    print(f"k={k}: blocks of F_n.H_n^-1 with both in natural order: {comps(Br, 1e-7)}")

print("== C. the five groups of order 8 against Z_2^3 (exact)")
def ft(elems_rep):
    """rows: one per matrix entry of each irreducible representation, scaled by sqrt(d)"""
    rows = []
    for reps, d in elems_rep:
        for i in range(d):
            for j in range(d):
                rows.append([np.sqrt(d) * reps[g][i][j] for g in range(8)])
    return np.array(rows)
# address g = 4*b + a, a in Z_4 (rotation r^a), b the reflection/second generator. chain <r^2> < <r> < G.
I2 = np.eye(2); r = np.array([[1j, 0], [0, -1j]]); s_d = np.array([[0, 1], [1, 0]]); s_q = np.array([[0, -1], [1, 0]])
def group(sm):
    lin = []
    for ea, eb in itertools.product((1, -1), repeat=2):
        lin.append(([[[ea ** a * eb ** b]] for b in range(2) for a in range(4)], 1))
    big = [np.linalg.matrix_power(r, a) @ np.linalg.matrix_power(sm, b) for b in range(2) for a in range(4)]
    return ft(lin + [(big, 2)])
# relabel so that the cosets of <r^2> are the pairs differing in the lowest bit: a = 2*lo + mid ... use address bits (b, a mod 2, a div 2)
perm = [4 * b + (2 * hi + lo) for b in range(2) for lo in range(2) for hi in range(2)]
for name, sm in (("D4", s_d), ("Q8", s_q)):
    F = group(sm)[:, perm]
    print(name, "unitary up to 8:", np.allclose(F @ F.conj().T, 8 * np.eye(8)),
          " blocks of F_G.H_8^-1:", comps(F @ H(3) / 8), " non-zeros:", int((abs(F @ H(3) / 8) > 1e-9).sum()))

print("== D. counts")
for k in (8, 16, 24, 32):
    n = 1 << k
    m = (k - 1) // 2
    # extraspecial group of order 2^(2m+1): half the mass in one representation of dimension 2^m
    print(f"k={k}: layers per point: Z_2^k {k};  extraspecial 2^(1+{2*m}) (order 2^{2*m+1}): {(2*m + 1) - m / 2:.1f} of {2*m+1};"
          f"  Heisenberg over GF(2^{k//3}) (order 2^{3*(k//3)}): about {2 * (k // 3)};"
          f"  floor of the chain method k/2 = {k / 2}")
print("tensor-train form: butterflies needed to transform all cores, per n:")
for k in (8, 16, 24):
    chi = [min(1 << i, 1 << (k - i)) for i in range(k + 1)]
    print(f"  k={k}: {sum(chi[i] * chi[i + 1] for i in range(k)) / (1 << k):.3f}")
