# p-1-letter16: fewest tree rectangles for the transform with FREE sign scalings on rows and columns.
# Float integer programme (scipy HiGHS): candidates only; every list printed is replayed exactly by replay.py.
# usage: rf.py <design name> <mode: tile|gen> <time limit s> [Mb]
import numpy as np, sys, time, json
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy import sparse as sp
def par(a): return bin(a).count('1') & 1
def span(g):
    S = {0}
    for v in g: S |= {s ^ v for s in S}
    return S
def chain_nodes(N, gens):          # gens: list of generator lists, increasing subgroups; nodes = all cosets + root + singles
    nodes = [tuple(range(N))]
    for g in reversed(gens):
        S = span(g); seen = set()
        for x in range(N):
            if x in seen: continue
            cs = tuple(sorted(x ^ s for s in S)); seen |= set(cs); nodes.append(cs)
    nodes += [(i,) for i in range(N)]
    return nodes
def tree_nodes(t):                 # nested tuples of ints -> list of leaf sets
    out = []
    def rec(u):
        if isinstance(u, int): out.append((u,)); return (u,)
        L = rec(u[0]); R = rec(u[1]); s = tuple(sorted(L + R)); out.append(s); return s
    rec(t); out.sort(key=lambda s: (-len(s), s)); return out
def perp(N, S): return [x for x in range(N) if all(par(x & s) == 0 for s in S)]
def laminar(nodes):
    for a in nodes:
        for b in nodes:
            A, B = set(a), set(b)
            if A & B and not (A <= B or B <= A): return False
    return True
D = {}
# 8 points, g-1's dual chains (control: 13)
D['c8'] = (8, chain_nodes(8, [[6], [6, 3]]), chain_nodes(8, [[7], [7, 1]]), True)
# 16 points, standard dual chains
D['dual16'] = (16, chain_nodes(16, [[1], [1, 2], [1, 2, 4]]), chain_nodes(16, [[8], [8, 4], [8, 4, 2]]), True)
D['dual8'] = (8, chain_nodes(8, [[1], [1, 2]]), chain_nodes(8, [[4], [4, 2]]), True)
D['dual4'] = (4, chain_nodes(4, [[1]]), chain_nodes(4, [[2]]), True)
D['dual32'] = (32, chain_nodes(32, [[1], [1, 2], [1, 2, 4], [1, 2, 4, 8]]), chain_nodes(32, [[16], [16, 8], [16, 8, 4], [16, 8, 4, 2]]), True)
# (c) perpendicular at some levels only
D['half16a'] = (16, chain_nodes(16, [[1], [1, 2], [1, 2, 4]]), chain_nodes(16, [[4], [8, 4], [8, 4, 2]]), True)   # pairs not perp to the 8-sets
D['half16b'] = (16, chain_nodes(16, [[1], [1, 2], [1, 2, 4]]), chain_nodes(16, [[8], [8, 2], [8, 4, 2]]), True)   # fours not perp
D['half16c'] = (16, chain_nodes(16, [[1], [1, 2], [1, 2, 4]]), chain_nodes(16, [[8], [8, 4], [8, 4, 1]]), True)   # eights not perp to pairs
D['same16'] = (16, chain_nodes(16, [[1], [1, 2], [1, 2, 4]]), chain_nodes(16, [[1], [1, 2], [1, 2, 4]]), True)    # same chain (bad by the rank lemma)
D['rev16'] = (16, chain_nodes(16, [[1], [1, 2], [1, 2, 4]]), chain_nodes(16, [[4], [4, 2], [4, 2, 1]]), True)     # reversed bit order inside <1,2,4>
# (d) trees that are not subgroup chains
def cat(order):
    t = order[0]
    for x in order[1:]: t = (t, x)
    return t
D['cat16'] = (16, tree_nodes(cat(list(range(16)))), tree_nodes(cat(list(range(16)))), False)
D['cat16g'] = (16, tree_nodes(cat([0,1,3,2,6,7,5,4,12,13,15,14,10,11,9,8])), tree_nodes(cat([0,8,12,4,6,14,10,2,3,11,15,7,5,13,9,1])), False)
D['catdual16'] = (16, tree_nodes(cat(list(range(16)))), chain_nodes(16, [[8], [8, 4], [8, 4, 2]]), False)
# nodes of 3, 5, 6 points: unbalanced splits 16 = 6 + 10, 6 = 3 + 3, 10 = 5 + 5
def bal(L):
    if len(L) == 1: return L[0]
    h = len(L) // 2; return (bal(L[:h]), bal(L[h:]))
quad = [x for x in range(16) if ((x & 1) and (x >> 1 & 1)) ^ ((x >> 2 & 1) and (x >> 3 & 1))]      # the 6 points of x0x1+x2x3 = 1
rest = [x for x in range(16) if x not in quad]
D['quad16'] = (16, tree_nodes((bal(quad), bal(rest))), tree_nodes((bal(quad), bal(rest))), False)
D['quaddual16'] = (16, tree_nodes((bal(quad), bal(rest))), chain_nodes(16, [[8], [8, 4], [8, 4, 2]]), False)
if __name__ == '__main__':
    name, mode, tl = sys.argv[1], sys.argv[2], float(sys.argv[3]); Mb = float(sys.argv[4]) if len(sys.argv) > 4 else 4.0
    N, rown, coln, inv = D[name]
    assert laminar(rown) and laminar(coln) and len(rown) == 2 * N - 1 and len(coln) == 2 * N - 1
    H = np.array([[(-1) ** par(a & x) for x in range(N)] for a in range(N)], dtype=float)
    rects = [(i, j) for i in range(len(rown)) for j in range(len(coln))]
    if mode == 'tile': rects = [r for r in rects if not (len(rown[r[0]]) == N and len(coln[r[1]]) == N)]
    n = len(rects); NN = N * N
    rr, cc = [], []
    for j, (a, b) in enumerate(rects):
        for y in rown[a]:
            for x in coln[b]: rr.append(y * N + x); cc.append(j)
    A = sp.csr_matrix((np.ones(len(rr)), (rr, cc)), shape=(NN, n))
    # XOR rows: t(y,x) = b_y xor d_x ; variable blocks differ per mode
    def xor_rows(off_b, off_d, off_t, nv):
        R, C, V, lo, hi = [], [], [], [], []; k = 0
        for y in range(N):
            for x in range(N):
                t = off_t + y * N + x; b = off_b + y; d = off_d + x
                for (cb, cd, ub) in ((1, -1, 0), (-1, 1, 0), (-1, -1, 0), (1, 1, 2)):   # cb*b + cd*d - t <= ub  /  t - b - d <= 0 / t + b + d <= 2
                    if (cb, cd) == (-1, -1): R += [k, k, k]; C += [t, b, d]; V += [1, -1, -1]
                    elif (cb, cd) == (1, 1): R += [k, k, k]; C += [t, b, d]; V += [1, 1, 1]
                    else: R += [k, k, k]; C += [b, d, t]; V += [cb, cd, -1]
                    lo.append(-np.inf); hi.append(ub); k += 1
        return sp.csr_matrix((V, (R, C)), shape=(k, nv)), np.array(lo), np.array(hi)
    basis = [0] + [1 << i for i in range(N.bit_length() - 1)]
    if mode == 'tile':
        nv = n + 2 * N + NN; ob, od, ot = n, n + N, n + 2 * N
        E1 = sp.hstack([A, sp.csr_matrix((NN, 2 * N)), -sp.identity(NN)]).tocsr()
        # M = h(y,x)*(1-2t) and cell in E iff M = -1:  e = (1 - M)/2 = (1 - h)/2 + h*t ; A z - h*t = (1-h)/2
        hh = H.ravel(); E1 = sp.hstack([A, sp.csr_matrix((NN, 2 * N)), -sp.diags(hh)]).tocsr(); rhs = (1 - hh) / 2
        X, lo, hi = xor_rows(ob, od, ot, nv)
        lb = np.zeros(nv); ub = np.ones(nv); integ = np.concatenate([np.ones(n + 2 * N), np.zeros(NN)])
        cost = np.concatenate([np.ones(n), np.zeros(2 * N + NN)])
        cons = [LinearConstraint(E1, rhs, rhs), LinearConstraint(X, lo, hi)]
        if inv:
            # valid: c -> c * character moves the rows by a translation (the row tree is made of cosets), so c(e_i) = c(0) = 1 is free.
            # NOT valid at the same time: the same normalisation for r (it translates c and undoes the first). First run had both: OVERFIXED.
            for e in basis: ub[od + e] = 0
        else: ub[od] = 0
    else:
        nv = 2 * n + 2 * N + NN; ob, od, ot = 2 * n, 2 * n + N, 2 * n + 2 * N
        hh = H.ravel()
        E1 = sp.hstack([A, sp.csr_matrix((NN, n)), sp.csr_matrix((NN, 2 * N)), 2 * sp.diags(hh)]).tocsr()
        I = sp.identity(n); Z = sp.csr_matrix((n, 2 * N + NN))
        X, lo, hi = xor_rows(ob, od, ot, nv)
        cons = [LinearConstraint(E1, hh, hh), LinearConstraint(sp.hstack([I, -Mb * I, Z]).tocsr(), -np.inf, 0),
                LinearConstraint(sp.hstack([-I, -Mb * I, Z]).tocsr(), -np.inf, 0), LinearConstraint(X, lo, hi)]
        lb = np.concatenate([-Mb * np.ones(n), np.zeros(nv - n)]); ub = np.concatenate([Mb * np.ones(n), np.ones(nv - n)])
        integ = np.concatenate([np.zeros(n), np.ones(n + 2 * N), np.zeros(NN)])
        cost = np.concatenate([np.zeros(n), np.ones(n), np.zeros(2 * N + NN)])
        if inv:
            for e in basis: ub[od + e] = 0
            ub[ob] = 0
        else: ub[od] = 0; ub[ob] = 0
    t0 = time.time()
    r = milp(cost, constraints=cons, integrality=integ, bounds=Bounds(lb, ub), options={'time_limit': tl, 'disp': False})
    print("design", name, "mode", mode, "Mb", Mb, "N", N, "status", r.status, r.message, " best:", None if r.x is None else round(r.fun) + (1 if mode == 'tile' else 0),
          " lower bound:", None if getattr(r, 'mip_dual_bound', None) is None else r.mip_dual_bound + (1 if mode == 'tile' else 0), " (%.0f s)" % (time.time() - t0))
    if r.x is not None:
        bs = [int(round(v)) for v in r.x[ob:ob + N]]; ds = [int(round(v)) for v in r.x[od:od + N]]
        rs = [1 - 2 * v for v in bs]; cs = [1 - 2 * v for v in ds]
        if mode == 'tile':
            lst = [[list(range(N)), list(range(N)), 1.0]] + [[list(rown[rects[j][0]]), list(coln[rects[j][1]]), -2.0] for j in range(n) if r.x[j] > 0.5]
        else:
            lst = [[list(rown[rects[j][0]]), list(coln[rects[j][1]]), round(float(r.x[j]), 6)] for j in range(n) if abs(r.x[j]) > 1e-6]
        print("  tau", len(lst), " gates N - 2 + tau =", N - 2 + len(lst))
        print("JSON", json.dumps({'design': name, 'N': N, 'r': rs, 'c': cs, 'rects': lst, 'rown': [list(s) for s in rown], 'coln': [list(s) for s in coln]}))
    sys.stdout.flush()
