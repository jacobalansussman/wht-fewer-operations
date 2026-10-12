# e-6-shifts: the shift array with a window.  v0 = sqrt(N)*delta_0 + (all ones) satisfies H v0 = sqrt(N) v0.
# G[c][d] = sum_s v0(s xor c) * (-1)^(d.s) * x(s)   ("windowed transform": row c of the shift array of v0, times x, transformed)
# Claims, exact integers, N = 4, 16, 64 (sqrt(N) = 2, 4, 8):
#   (1) G[c][d] = sqrt(N) * (-1)^(c.d) * x(c) + (Hx)(d)
#   (2) the same array built from Hx in place of x is sqrt(N) * G transposed: on these N^2 numbers the transform is a relabelling
#   (3) more windows of the same kind: for a subgroup A, v_A = sqrt(|A-perp|) * 1_A + sqrt(|A|) * 1_(A-perp) when both roots are integers
pc = lambda x: bin(x).count("1")
for k in (2, 4, 6):
    N = 1 << k; r = 1 << (k // 2)
    H = [[1 - 2 * (pc(a & b) & 1) for b in range(N)] for a in range(N)]
    v0 = [r * (1 if s == 0 else 0) + 1 for s in range(N)]
    eig = [sum(H[w][s] * v0[s] for s in range(N)) for w in range(N)] == [r * t for t in v0]
    def gabor(x, v): return [[sum(v[s ^ c] * H[d][s] * x[s] for s in range(N)) for d in range(N)] for c in range(N)]
    ok1 = ok2 = True
    for j in range(N):
        x = [1 if s == j else 0 for s in range(N)]; hx = [H[w][j] for w in range(N)]
        G = gabor(x, v0); Gh = gabor(hx, v0)
        ok1 &= all(G[c][d] == r * H[c][d] * x[c] + hx[d] for c in range(N) for d in range(N))
        ok2 &= all(Gh[c][d] == r * G[d][c] for c in range(N) for d in range(N))
    # (3) A = span of the first k/2 unit addresses (|A| = |A-perp| = sqrt N): v_A = 1_A + 1_Aperp
    A = [s for s in range(N) if s < r]; Ap = [s for s in range(N) if all(pc(s & a) % 2 == 0 for a in A)]
    vA = [(1 if s in A else 0) + (1 if s in Ap else 0) for s in range(N)]
    eigA = [sum(H[w][s] * vA[s] for s in range(N)) for w in range(N)] == [r * t for t in vA]
    ok3 = True
    for j in range(N):
        x = [1 if s == j else 0 for s in range(N)]; hx = [H[w][j] for w in range(N)]
        G = gabor(x, vA); Gh = gabor(hx, vA)
        ok3 &= all(Gh[c][d] == r * H[c][d] * G[d][c] for c in range(N) for d in range(N))
    print("N=%2d  H v0 = sqrt(N) v0: %s   (1) G = sqrt(N)*sign*x(c) + Hx(d): %s   (2) transform acts on G as transpose: %s   (3) two-bump window (support %d) is an eigenvector: %s, transform acts as signed transpose: %s" % (N, eig, ok1, ok2, sum(1 for t in vA if t), eigA, ok3))
