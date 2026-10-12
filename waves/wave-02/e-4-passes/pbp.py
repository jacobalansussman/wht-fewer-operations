#!/usr/bin/env python3
"""e-4-passes / pbp.py   exact integer arithmetic throughout.

Words.  H = Sylvester Hadamard matrix on d = 2^m points, H[a][x] = (-1)^popcount(a&x).
A PASS in an order p_0..p_(d-1) is y_(p_i) = x_(p_i) + c_i * y_(p_(i-1)): d-1 gates in count (G).
Its inverse is the "difference" B = I - C*shift (two non-zeros per row): also d-1 gates.
Form PBP (pass, difference-type middle, pass):   H' = B1^-1 * E * B3^-1   <=>   E = B1 * H' * B3,
with H' = H up to free relabelling and scaling.  E must have its non-zeros inside a Hamiltonian path of the
bipartite graph rows/columns (at most 2 per row and column, no cycle) to be ONE pass.  [derived in e-4.md:
every coefficient of B1, B3 is then forced into {1, 0, -1} after normalising one row and one column to ones.]

mode 'pbp d'   : exhaustive search of the PBP form (coefficient 1 everywhere except at most one position per
                 side, which may be 0 or -1), column order reduced by GL(m,2); prints solutions and replays one.
mode 'nnz d'   : exhaustive (d<=8) minimum number of non-zeros of E = D H' D^T over all orders, plain differences.
"""
import sys, itertools
from fractions import Fraction

def had(d):
    return [[1 - 2 * (bin(a & x).count("1") & 1) for x in range(d)] for a in range(d)]

def emat(H, pi, sig, c, cp):
    d = len(pi)
    R = [H[pi[0]][:]] + [[H[pi[i]][x] - c[i] * H[pi[i - 1]][x] for x in range(d)] for i in range(1, d)]
    E = [[R[i][sig[0]]] + [R[i][sig[j]] - cp[j] * R[i][sig[j - 1]] for j in range(1, d)] for i in range(d)]
    return E

def path_ok(E):
    d = len(E)
    for i in range(d):
        if sum(1 for v in E[i] if v) > 2: return False
    for j in range(d):
        if sum(1 for i in range(d) if E[i][j]) > 2: return False
    par = list(range(2 * d))
    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for i in range(d):
        for j in range(d):
            if E[i][j]:
                a, b = f(i), f(d + j)
                if a == b: return False
                par[a] = b
    return True

def reduced_orders(d):
    """column orders with sig[0]=0, one per orbit of GL(m,2) acting on the points (greedy canonical form:
    each new point that is independent of the earlier ones is renamed to the next basis vector)."""
    seen = set(); out = []
    for rest in itertools.permutations(range(1, d)):
        sig = (0,) + rest
        # canonical relabelling
        basis = []; span = {0: 0}; lab = {}
        nxt = 1
        can = []
        for x in sig:
            if x in span:
                can.append(span[x])
            else:
                new = {}
                for s, t in span.items():
                    new[s ^ x] = t ^ nxt
                span.update(new); nxt <<= 1
                can.append(span[x])
        can = tuple(can)
        if can not in seen:
            seen.add(can); out.append(can)
    return out

def pbp(d):
    H = had(d)
    sigs = reduced_orders(d) if d <= 8 else None
    print("d =", d, " column orders up to GL:", len(sigs))
    opts = [(None, 1)] + [(j, v) for j in range(1, d) for v in (0, -1)]
    nsol = 0; first = None; tested = 0
    for sig in sigs:
        for (js, v) in opts:
            cp = [1] * d
            if js is not None: cp[js] = v
            # row vector of chi_a - c*chi_b after the column differences; feasible if at most 2 non-zeros
            def rowv(a, b, c):
                R = [H[a][x] - (c * H[b][x] if b is not None else 0) for x in range(d)]
                return [R[sig[0]]] + [R[sig[j]] - cp[j] * R[sig[j - 1]] for j in range(1, d)]
            if sum(1 for t in rowv(0, None, 0) if t) > 2: continue
            ok = {}
            for a in range(d):
                for b in range(d):
                    if a != b:
                        for c in (1, 0, -1):
                            ok[(a, b, c)] = sum(1 for t in rowv(a, b, c) if t) <= 2
            def dfs(pi, cs, used_exc):
                nonlocal nsol, first, tested
                if len(pi) == d:
                    tested += 1
                    E = emat(H, pi, sig, cs, cp)
                    if path_ok(E):
                        nsol += 1
                        if first is None: first = (tuple(pi), sig, tuple(cs), tuple(cp), E)
                    return
                b = pi[-1]
                for a in range(d):
                    if a in pi: continue
                    for c in (1, 0, -1):
                        if c != 1 and used_exc: continue
                        if ok[(a, b, c)]:
                            dfs(pi + [a], cs + [c], used_exc or c != 1)
            dfs([0], [1], False)
    print("  full row orders that passed the row test:", tested, "  PBP solutions:", nsol)
    if first:
        pi, sig, cs, cp, E = first
        print("  example: row order", pi, "c", cs, " column order", sig, "c'", cp)
        for r in E: print("    ", r)
        # replay as three passes on unit vectors, exact
        ok = replay(d, H, pi, sig, cs, cp, E)
        print("  replayed as pass, middle pass, pass on the d unit vectors, equals H (rows in order pi, columns sig):", ok)
    return nsol

def replay(d, H, pi, sig, cs, cp, E):
    # H'[i][j] = H[pi[i]][sig[j]] ;  E = B1 H' B3,  B1 = I - C S (rows), B3 = (I - C' S)^T (columns)
    # so H' = B1^-1 E B3^-1 ;  apply to a vector x (indexed by column position j):
    #   u = B3^-1 x : B3[j'][j] : column j of B3 has 1 at j and -cp[j] at j-1  -> (B3 u)[k] = u[k] - cp[k+1] u[k+1] = x[k]
    #                 so u[d-1] = x[d-1], u[k] = x[k] + cp[k+1]*u[k+1]      (a pass run downward, d-1 gates)
    #   v = E u                                                             (the middle; counted separately)
    #   z = B1^-1 v : z[0] = v[0], z[i] = v[i] + cs[i]*z[i-1]               (a pass run upward, d-1 gates)
    good = True
    for e in range(d):
        x = [Fraction(int(k == e)) for k in range(d)]
        u = x[:]
        for k in range(d - 2, -1, -1): u[k] = x[k] + cp[k + 1] * u[k + 1]
        v = [sum(E[i][j] * u[j] for j in range(d)) for i in range(d)]
        z = v[:]
        for i in range(1, d): z[i] = v[i] + cs[i] * z[i - 1]
        if any(z[i] != H[pi[i]][sig[e]] for i in range(d)): good = False
    return good

def nnz(d):
    H = had(d)
    sigs = reduced_orders(d)
    best = None; hist = {}
    ones = [1] * d
    for sig in sigs:
        for rest in itertools.permutations(range(1, d)):
            pi = (0,) + rest
            E = emat(H, pi, sig, ones, ones)
            n = sum(1 for r in E for v in r if v)
            hist[n] = hist.get(n, 0) + 1
            if best is None or n < best[0]: best = (n, pi, sig, E)
    print("d =", d, " plain differences on both sides, all orders (columns up to GL): histogram of non-zeros", sorted(hist.items()))
    n, pi, sig, E = best
    print("  minimum", n, " row order", pi, " column order", sig, "  gates (G) for pass + E + pass: ", n + d - 2)
    for r in E: print("    ", r)

if __name__ == "__main__":
    mode, d = sys.argv[1], int(sys.argv[2])
    if mode == "pbp": pbp(d)
    if mode == "nnz": nnz(d)
