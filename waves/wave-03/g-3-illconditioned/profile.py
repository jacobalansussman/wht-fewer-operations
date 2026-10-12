# profile.py  (g-3-illconditioned)
# Exact replay and "conditioning profile" of in-place programs (moves w_i <- w_i + c*w_j, scalings free).
# For every intermediate state M (rows = wires, exact rationals) it computes the table L = M o M^(-T)
# (entry-by-entry product of M with its inverse transpose; unchanged by any scaling of rows or columns; rows and
# columns sum to 1), and from it, as FLOAT MEASUREMENTS:
#   pot  = sum of -L*log2|L|        (Ailon's potential; identity 0, transform N*log2 N)
#   mass = sum |L| / N              (1 exactly when no entry of L is negative: "perfectly conditioned up to scalings")
#   cond = condition number of M after scaling every row to length 1
# usage: profile.py all4 onpath7.txt | known
import sys, math
from fractions import Fraction as Fr
from math import gcd

def inv(M):
    n = len(M); A = [[Fr(x) for x in r] + [Fr(int(i == j)) for j in range(n)] for i, r in enumerate(M)]
    for c in range(n):
        pr = next(r for r in range(c, n) if A[r][c] != 0)
        A[c], A[pr] = A[pr], A[c]
        pv = A[c][c]; A[c] = [x / pv for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]; A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return [r[n:] for r in A]

def ltable(M):
    Mi = inv(M); n = len(M)
    return [[M[i][j] * Mi[j][i] for j in range(n)] for i in range(n)]

def pot(L): return sum(-float(x) * math.log2(abs(float(x))) for r in L for x in r if x != 0)
def mass(L): return sum(abs(float(x)) for r in L for x in r) / len(L)

def jacobi_eigs(A):
    n = len(A); A = [list(map(float, r)) for r in A]
    for _ in range(100):
        off = sum(A[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < 1e-22: break
        for p in range(n):
            for q in range(p + 1, n):
                if abs(A[p][q]) < 1e-300: continue
                th = (A[q][q] - A[p][p]) / (2 * A[p][q])
                t = (1 if th >= 0 else -1) / (abs(th) + math.sqrt(th * th + 1)); c = 1 / math.sqrt(t * t + 1); s = t * c
                for k in range(n):
                    akp, akq = A[k][p], A[k][q]; A[k][p] = c * akp - s * akq; A[k][q] = s * akp + c * akq
                for k in range(n):
                    apk, aqk = A[p][k], A[q][k]; A[p][k] = c * apk - s * aqk; A[q][k] = s * apk + c * aqk
    return sorted(A[i][i] for i in range(n))

def cond_rows(M):
    R = []
    for r in M:
        nr = math.sqrt(sum(float(x) ** 2 for x in r)); R.append([float(x) / nr for x in r])
    n = len(R); G = [[sum(R[i][k] * R[j][k] for k in range(n)) for j in range(n)] for i in range(n)]
    e = jacobi_eigs(G)
    return math.sqrt(e[-1] / max(e[0], 1e-300))

def shear_cond(c):   # condition number of the 2x2 matrix [[1, c], [0, 1]]
    c = abs(float(c)); s = (c + math.sqrt(c * c + 4)) / 2
    return s * s

def prim(v):
    den = 1
    for x in v: den = den * Fr(x).denominator // gcd(den, Fr(x).denominator)
    w = [int(Fr(x) * den) for x in v]; g = 0
    for x in w: g = gcd(g, abs(x))
    if g == 0: return tuple(w)
    w = [x // g for x in w]
    f = next(x for x in w if x != 0)
    if f < 0: w = [-x for x in w]
    return tuple(w)

def red(state, p):
    out = []
    for v in state:
        f = next(x for x in v if x % p != 0); iv = pow(f, -1, p)
        out.append(tuple(x * iv % p for x in v))
    return tuple(sorted(out))

def had(k):
    R = [[1]]
    for _ in range(k): R = [[x * y for x in ra for y in rb] for ra in R for rb in [[1, 1], [1, -1]]]
    return R

def run_all4(dump):
    p = 7; layers = {}
    for line in open(dump):
        if line.startswith('#'): continue
        parts = line.split(); t = int(parts[0])
        layers.setdefault(t, set()).add(tuple(sorted(tuple(int(x) for x in w.split(',')) for w in parts[1:])))
    best = max(layers)
    coefs = [Fr(1), Fr(-1), Fr(2), Fr(-2), Fr(1, 2), Fr(-1, 2)]
    start = tuple(sorted(prim(v) for v in [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]))
    target = tuple(sorted(prim(v) for v in had(2)))
    info = {}
    def get(s):
        if s not in info:
            L = ltable([list(v) for v in s]); info[s] = (pot(L), mass(L), cond_rows([list(v) for v in s]))
        return info[s]
    # forward: the layered graph of exact states whose reduction modulo 7 lies on a shortest program modulo 7
    lay = [{start: {}}]            # lay[t][state] = {next_state: number of distinct moves (wire i, wire j, c) giving it}
    for t in range(best):
        nxt = {}
        for s in lay[t]:
            for i in range(4):
                for j in range(4):
                    if i == j: continue
                    for c in coefs:
                        v = prim([Fr(a) + c * b for a, b in zip(s[i], s[j])])
                        if not any(v): continue
                        s2 = tuple(sorted(s[:i] + (v,) + s[i + 1:]))
                        if len(set(s2)) < 4: continue
                        try: r2 = red(s2, p)
                        except StopIteration: continue
                        if r2 not in layers.get(t + 1, ()): continue
                        lay[t][s][s2] = lay[t][s].get(s2, 0) + 1; nxt.setdefault(s2, {})
        lay.append(nxt)
    print("4 points, in place, 4 wires, 8 moves: every shortest program with coefficients +-1, +-2, +-1/2, exact rationals")
    print("(modulo 7 these six values are all the non-zero residues, so the GF(7) dump guides the exact search; only programs")
    print(" that end EXACTLY at the transform's rows over the rationals are kept)")
    print("end states reached:", len(lay[best]), " of which the exact target:", int(target in lay[best]))
    # backward: keep what reaches the exact target
    back = [dict() for _ in range(best + 1)]; back[best] = {target: 1}
    for t in range(best - 1, -1, -1):
        for s, outs in lay[t].items():
            n = sum(mult * back[t + 1].get(s2, 0) for s2, mult in outs.items())
            if n: back[t][s] = n
    fw = [dict() for _ in range(best + 1)]; fw[0] = {start: 1}; fw1 = [dict() for _ in range(best + 1)]; fw1[0] = {start: 1}
    jumps = {}; bigedge = None; bigjump = -1e9
    for t in range(best):
        for s, n in fw[t].items():
            for s2, mult in lay[t][s].items():
                if s2 not in back[t + 1]: continue
                fw[t + 1][s2] = fw[t + 1].get(s2, 0) + n * mult
                j = round(get(s2)[0] - get(s)[0], 3); jumps[(t, j)] = jumps.get((t, j), 0) + n * mult * back[t + 1][s2]
                if j > bigjump: bigjump = j; bigedge = (t, s, s2)
                if get(s2)[1] < 1 + 1e-9 and s in fw1[t]: fw1[t + 1][s2] = fw1[t + 1].get(s2, 0) + fw1[t][s] * mult
    print("layer  exact_states_on_programs  potentials_seen(bits)                                 max_mass  max_cond(rows scaled)")
    for t in range(best + 1):
        S = list(back[t]); pots = sorted(set(round(get(s)[0], 3) for s in S))
        print(f"{t:5d}  {len(S):24d}  {str(pots)[:52]:52s}  {max(get(s)[1] for s in S):8.3f}  {max(get(s)[2] for s in S):8.3f}")
    print("exact shortest programs (as sequences of moves):", fw[best].get(target, 0))
    print("  of these, with no negative entry in any intermediate table L (mass 1 throughout):", fw1[best].get(target, 0))
    print("potential gained per move, by move number (number of programs):")
    for t in range(best):
        print("  move", t + 1, {j: n for (tt, j), n in sorted(jumps.items()) if tt == t})
    # one program through the largest single gain, and one through the largest mass
    def show_path(path, title):
        print(title)
        for t, s in enumerate(path):
            g = get(s); gain = "" if t == 0 else f"{g[0] - get(path[t - 1])[0]:+7.3f}"
            print(f"   after move {t}: pot {g[0]:7.3f} {gain:8s} mass {g[1]:6.3f} cond {g[2]:7.3f}   wires {[list(v) for v in s]}")
    def complete(t, s):       # extend backwards to the start and forwards to the target inside the kept graph
        pre = [s]
        for u in range(t - 1, -1, -1):
            pre.insert(0, next(a for a in back[u] if pre[0] in lay[u][a]))
        post = [s]
        for u in range(t, best):
            post.append(next(b2 for b2 in lay[u][post[-1]] if b2 in back[u + 1]))
        return pre + post[1:]
    t, s, s2 = bigedge
    show_path(complete(t, s)[:t + 1] + complete(t + 1, s2)[t + 1:], f"a shortest program through the largest single gain ({bigjump} bits at move {t + 1}):")
    tm, sm = max(((u, a) for u in range(best + 1) for a in back[u]), key=lambda x: get(x[1])[1])
    show_path(complete(tm, sm), f"a shortest program through the state of largest mass ({get(sm)[1]:.3f}):")

def profile(name, n, prog, show=True):
    M = [[Fr(int(i == j)) for j in range(n)] for i in range(n)]
    L = ltable(M); p0 = pot(L); shears = 0; jumps = {}; mm = 1.0; mc = 1.0; minpot = 0.0
    if show: print(f"{name}: move, coefficient, cond of the move alone, potential after, gain, mass after, cond after (rows scaled)")
    for op in prog:
        if op[0] == 'd': M[op[1]] = [x * op[2] for x in M[op[1]]]; continue
        _, i, j, c = op; M[i] = [a + c * b for a, b in zip(M[i], M[j])]; shears += 1
        L = ltable(M); p1 = pot(L); ms = mass(L); cd = cond_rows(M)
        j2 = round(p1 - p0, 3); jumps[j2] = jumps.get(j2, 0) + 1; mm = max(mm, ms); mc = max(mc, cd); minpot = min(minpot, p1)
        if show: print(f"  w{i} += ({c})*w{j}   {shear_cond(c):7.3f}   {p1:8.3f}  {j2:+7.3f}  {ms:7.3f}  {cd:9.3f}")
        p0 = p1
    return M, shears, jumps, mm, mc, minpot

def textbook(k):
    n = 1 << k; prog = []
    for b in range(k):
        for x in range(n):
            if x >> b & 1: continue
            y = x | 1 << b
            prog += [('s', x, y, Fr(1)), ('d', y, Fr(-2)), ('s', y, x, Fr(1))]
    return prog

def zdz(k):
    n = 1 << k; prog = []
    for b in range(k):
        for x in range(n):
            if not x >> b & 1: prog.append(('s', x, x | 1 << b, Fr(1)))      # Z-transpose: sums over supersets
    for x in range(n): prog.append(('d', x, Fr((-2) ** bin(x).count('1'))))
    for b in range(k):
        for x in range(n):
            if not x >> b & 1: prog.append(('s', x | 1 << b, x, Fr(1)))      # Z: sums over subsets
    return prog

def same_rows(M, T):
    return sorted(prim(r) for r in M) == sorted(prim(r) for r in T)

def run_known():
    for k in (2, 3, 4):
        n = 1 << k
        for name, prog in (("textbook butterflies in place", textbook(k)), ("subset sums, diagonal, subset sums (Z D Z^T)", zdz(k))):
            M, sh, jumps, mm, mc, minpot = profile(f"{n} points, {name}", n, prog, show=(k == 2))
            print(f"{n} points, {name}: shears {sh}; exact result is the transform up to row scaling: {same_rows(M, had(k))}; "
                  f"gains per shear {jumps}; largest mass {mm:.3f}; largest cond (rows scaled) {mc:.3f}; lowest potential {minpot:.3f}")

if __name__ == "__main__":
    if sys.argv[1] == "all4": run_all4(sys.argv[2])
    else: run_known()
