# potts.py  (g-3-illconditioned)
# The "Potts matrix" W_N = t*I + (J - I)  (t on the diagonal, 1 elsewhere), with t + 1/t = 2 - N.
# Claims checked here, exactly in Q(sqrt d) (numbers a + b*sqrt(d) with rational a, b):
#   1. W_N is "flat on both sides": the table L = W o W^(-T) has every entry 1/N (so Ailon's potential is N*log2 N, the
#      same as the transform's).
#   2. Count (G): 2N - 1 gates (one chain for the sum, one gate per output).  In place: 3N - 3 moves.  Both replayed exactly.
#   3. |t| = 1 exactly when N <= 4 (N = 2: t = i, N = 3: t = a cube root of unity, N = 4: t = -1, the 7-gate brick).
# Float MEASUREMENTS (labelled): potential after each in-place move, condition numbers.
import sys, math
from fractions import Fraction as Fr

def sqfree(n):
    s, d = 1, n; f = 2
    while f * f <= d:
        while d % (f * f) == 0: d //= f * f; s *= f
        f += 1
    return s, d

class Q:   # a + b*sqrt(D)
    D = 2
    __slots__ = ("a", "b")
    def __init__(s, a, b=0): s.a = Fr(a); s.b = Fr(b)
    def __add__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __neg__(s): return Q(-s.a, -s.b)
    def __sub__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return Q(o) - s
    def __mul__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.a * o.a + Q.D * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def inv(s): n = s.a * s.a - Q.D * s.b * s.b; return Q(s.a / n, -s.b / n)
    def __truediv__(s, o): o = o if isinstance(o, Q) else Q(o); return s * o.inv()
    def __eq__(s, o): o = o if isinstance(o, Q) else Q(o); return s.a == o.a and s.b == o.b
    def __float__(s): return float(s.a) + float(s.b) * math.sqrt(Q.D)
    def __repr__(s): return f"({s.a}+{s.b}r{Q.D})"

def finv(M):   # float inverse
    n = len(M); A = [list(map(float, r)) + [float(i == j) for j in range(n)] for i, r in enumerate(M)]
    for c in range(n):
        pr = max(range(c, n), key=lambda r: abs(A[r][c])); A[c], A[pr] = A[pr], A[c]
        pv = A[c][c]; A[c] = [x / pv for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0.0:
                f = A[r][c]; Ac = A[c]; A[r] = [x - f * y for x, y in zip(A[r], Ac)]
    return [r[n:] for r in A]

def fpot(M):
    Mi = finv(M); n = len(M); tot = 0.0; ms = 0.0
    for i in range(n):
        for j in range(n):
            x = M[i][j] * Mi[j][i]
            if abs(x) > 1e-13: tot -= x * math.log2(abs(x))
            ms += abs(x)
    return tot, ms / n

def run(N, profile=True):
    s, d = sqfree(N * (N - 4)); Q.D = d
    t = Q(Fr(2 - N, 2), Fr(s, 2)); al = t - 1
    assert t + t.inv() == Q(2 - N)
    # 1. exact table L from the closed form of the inverse: W^-1 = (1/al) (I - J/(al + N))
    Ldiag = t * (al.inv() * (1 - (al + N).inv())); Loff = -(al * (al + N)).inv()
    flat = (Ldiag == Q(Fr(1, N)) and Loff == Q(Fr(1, N)))
    W = [[t if i == j else Q(1) for j in range(N)] for i in range(N)]
    # check the closed form of the inverse on the first two rows (exact)
    Wi = [[(al.inv() * ((1 if i == j else 0) - (al + N).inv())) for j in range(N)] for i in range(N)]
    okinv = all(sum((W[i][k] * Wi[k][j] for k in range(N)), Q(0)) == Q(int(i == j)) for i in range(2) for j in range(N))
    # 2a. count (G): chain for S, then al*x_i + S
    def vec(i): return [Q(int(i == j)) for j in range(N)]
    S = vec(0); gates = 0
    for i in range(1, N): S = [a + b for a, b in zip(S, vec(i))]; gates += 1
    outs = []
    for i in range(N): outs.append([al * a + b for a, b in zip(vec(i), S)]); gates += 1
    okG = outs == W
    # 2b. in place, 3N - 3 moves
    w = [vec(i) for i in range(N)]; states = []; moves = 0
    def snap(): states.append([[float(x) for x in r] for r in w])
    snap()
    for i in range(1, N): w[0] = [a + b for a, b in zip(w[0], w[i])]; moves += 1; snap()
    for i in range(1, N): w[i] = [al * a + b for a, b in zip(w[i], w[0])]; moves += 1; snap()
    w[0] = [(al + N) * a for a in w[0]]
    for i in range(1, N): w[0] = [a - b for a, b in zip(w[0], w[i])]; moves += 1; snap()
    okI = w == W
    cond = abs(float(al + N)) / abs(float(al))
    line = (f"N={N:3d}  t = {float(t):+.6f} (in Q(sqrt {d}))  table L flat (all 1/N), exact: {flat}; inverse formula exact: {okinv}; "
            f"(G) {gates} gates exact: {okG}; in place {moves} moves exact: {okI}; cond(W) = {cond:.2f} [float]; "
            f"potential N*log2 N = {N * math.log2(N):.1f} bits; textbook transform in place: {int(N * math.log2(N)) if N & (N - 1) == 0 else '-'} moves")
    print(line)
    if profile:
        prev = 0.0; best = (-1e9, 0); worst = (1e9, 0); mm = 1.0; rows = []
        for k, M in enumerate(states):
            pt, ms = fpot(M); g = pt - prev; mm = max(mm, ms)
            if k and g > best[0]: best = (g, k)
            if k and g < worst[0]: worst = (g, k)
            rows.append((k, pt, g, ms)); prev = pt
        print(f"        [float measurement] largest single-move gain {best[0]:.3f} bits at move {best[1]}; largest loss {worst[0]:.3f} at move {worst[1]}; "
              f"largest mass {mm:.3f}; final potential {rows[-1][1]:.3f}; bits per move overall {rows[-1][1] / moves:.3f}")
        if N in (8, 16):
            print("        move: potential after (gain) mass   -- phase 1 = moves 1..N-1 (sum), phase 2 = next N-1 (outputs), phase 3 = last N-1 (repair wire 0)")
            print("        " + "  ".join(f"{k}:{pt:.2f}({g:+.2f}){ms:.2f}" for k, pt, g, ms in rows[1:]))

if __name__ == "__main__":
    print("N <= 4: t + 1/t = 2 - N has |t| = 1: N=2 t=i; N=3 t=(-1+sqrt(-3))/2; N=4 t=-1 (the 7-gate brick: J - 2I).  N >= 5: t real, not +-1.")
    for N in (5, 6, 8, 12, 16, 32, 64):
        run(N, profile=True)
