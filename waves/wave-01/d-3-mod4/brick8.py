# d-3-mod4, experiment 3.  The new brick seen at 64 points, checked as operators at 8 points (exact Gaussian integers).
#  (1) on three bits:  |y| = 2*[y not all equal] + 3*[|y| odd]   modulo 4   (false for the exact weight)
#  (2) hence  8*K_8 = (1-i)^3 * A * B  with  K_8[x][x'] = (-i)^dist(x,x'),
#      A = 4*(2E - I),  E = average over the points of the same parity (a reflection: Grover's diffusion on two 4-point classes)
#      B = (1-i) I + (1+i) P,  P = "complement the address".
#  (3) the count lemma: the largest affine subspace on which |y| mod 4 is constant has dimension floor(k/2), k = 2..6;
#      same for the exact weight.  (exhaustive over subspaces by closure; integers)
import itertools, sys
pc = lambda x: bin(x).count("1")
class G:                                   # Gaussian integer
    __slots__ = ("a", "b")
    def __init__(s, a, b=0): s.a, s.b = a, b
    def __add__(s, o): return G(s.a + o.a, s.b + o.b)
    def __mul__(s, o): return G(s.a * o.a - s.b * o.b, s.a * o.b + s.b * o.a)
    def __eq__(s, o): return s.a == o.a and s.b == o.b
I4 = [G(1), G(0, 1), G(-1), G(0, -1)]
def mm(X, Y):
    n = len(X); Z = [[G(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            t = G(0)
            for l in range(n): t = t + X[i][l] * Y[l][j]
            Z[i][j] = t
    return Z
print("(1) three bits, weights 0..3: 2*NAE + 3*parity mod 4 =", [(2 * (0 < w < 3) + 3 * (w & 1)) % 4 for w in range(4)], " as integers:", [2 * (0 < w < 3) + 3 * (w & 1) for w in range(4)])
n = 8
K = [[I4[(-pc(x ^ z)) % 4] for z in range(n)] for x in range(n)]
A = [[G(2 * (pc(x) % 2 == pc(z) % 2) - 4 * (x == z)) for z in range(n)] for x in range(n)]
B = [[G(1, -1) if x == z else (G(1, 1) if x ^ z == n - 1 else G(0)) for z in range(n)] for x in range(n)]
c = G(1, -1) * G(1, -1) * G(1, -1)
AB = mm(A, B)
ok = all(G(8) * K[x][z] == c * AB[x][z] for x in range(n) for z in range(n))
print("(2) 8*K_8 == (1-i)^3 * A * B :", ok)
print("    gates (one gate = a*u + b*v): A = 2 classes * (3 to sum + 4 to subtract) = 14 ; B = 4 pairs * 2 = 8 ; total 22 ; textbook 3*8 = 24 ; 7-gate 4-point unit + one butterfly layer = 22")
# (3) flats
def maxflat(k, mod):
    n = 1 << k; best = 0
    val = [pc(y) % mod if mod else pc(y) for y in range(n)]
    def rec(base, span, dim, start):
        nonlocal best
        best = max(best, dim)
        if dim + (k - dim) <= best: pass
        for v in range(start, n):
            if v in span: continue
            new = {s ^ v for s in span}
            if all(val[base ^ s] == val[base] for s in new):
                rec(base, span | new, dim + 1, v + 1)
    for base in range(n):
        rec(base, frozenset([0]), 0, 1)
    return best
for k in range(2, 7):
    print("(3) k=%d: largest affine subspace with constant |y| mod 4: dim %d ; with constant exact weight: dim %d ; floor(k/2) = %d" % (k, maxflat(k, 4), maxflat(k, 0), k // 2))
    sys.stdout.flush()
