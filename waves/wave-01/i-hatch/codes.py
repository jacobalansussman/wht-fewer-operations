# i-hatch: indicators of self-dual codes are eigenvectors of the plain +-1 transform with exactly sqrt(N) non-zeros (integers, exact).
pc = lambda x: bin(x).count("1")
def span(gens):
    S = {0}
    for g in gens: S |= {s ^ g for s in S}
    return S
def wht_at(support, y):            # (H 1_C)(y) = sum over c in C of (-1)^(c.y)
    return sum(-1 if pc(c & y) & 1 else 1 for c in support)
tests = {
  "diagonal of two 2-bit columns {(u,u)}, N=16": (4, [0b0101, 0b1010]),
  "diagonal of two 3-bit columns, N=64": (6, [0b001001, 0b010010, 0b100100]),
  "extended Hamming [8,4] (the code under E8), N=256": (8, [0b11110000, 0b11001100, 0b10101010, 0b11111111]),
}
for name, (k, gens) in tests.items():
    C = span(gens); N = 1 << k
    ok = all(wht_at(C, y) == (len(C) if y in C else 0) for y in range(N))
    print("%-52s |C|=%3d  sqrt(N)=%3d  H 1_C == sqrt(N) 1_C : %s" % (name, len(C), int(N ** 0.5), ok and len(C) ** 2 == N))
# a self-orthogonal code C of dimension j (C inside its dual): functions on C_dual / C are carried to themselves, as a transform of size N/4^j
k = 6; C = span([0b110000, 0b001100]); Cd = {y for y in range(64) if all(pc(y & c) % 2 == 0 for c in C)}
reps = sorted({min(y ^ c for c in C) for y in Cd})
img = {r: [wht_at({r ^ c for c in C}, y) for y in range(64)] for r in reps}
inv = all(all(v[y] == 0 for y in range(64) if y not in Cd) and all(v[y] == v[y ^ c] for y in Cd for c in C) for v in img.values())
print("k=6, C of dimension 2: the %d-dimensional space of functions on C_dual/C is invariant: %s (acts there as 4 x the 4-point transform)" % (len(reps), inv))
