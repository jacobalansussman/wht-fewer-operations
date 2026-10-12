#!/usr/bin/env python3
"""r2_lift.py (r-2): EXACT existence of each shape for tau a symbol.  Input: reps_p13.json (one named wiring per shape, found modulo 13).
For each shape: helpers = first parent + beta * second parent (beta unknown), each output must lie in the span of its two parents
(3 x 3 minors).  Solve for the betas as rational functions of tau (Groebner basis over the field Q(tau)), then REPLAY: every one of
the 7 gates is checked (child in the span of two independent parents) with tau a symbol and at tau = 3, 5/7, -2, -1, 2, 1/2 with fractions."""
import json, itertools, sys
from sympy import symbols, Matrix, groebner, solve, cancel, Rational, QQ, factor
tau = symbols('tau')
D = json.load(open(sys.argv[1])); src = sys.argv[2]
rows = [[tau ** bin(w & x).count('1') for x in range(4)] for w in range(4)]
E = [[int(i == j) for j in range(4)] for i in range(4)]
def minors3(u, v, t):
    M = Matrix([u, v, t]); return [M[:, list(c)].det() for c in itertools.combinations(range(4), 3)]
def indep(u, v, sub=None):
    for i, j in itertools.combinations(range(4), 2):
        d = cancel(u[i] * v[j] - u[j] * v[i])
        if sub is not None: d = d.subs(sub) if hasattr(d, 'subs') else d
        if d != 0: return True
    return False
TEST = [Rational(3), Rational(5, 7), Rational(-2), Rational(-1), Rational(2), Rational(1, 2)]
nok = 0; n = 0
for name, per in sorted(D['reps'].items()):
    if src not in per: print('shape', name, ': no representative at tau =', src, '(a special shape), skipped'); continue
    n += 1
    w = {g[0]: (g[1], g[2]) for g in per[src][1]}
    be = {c: symbols('b%d' % c) for c in (4, 5, 6)}
    P = {i: E[i] for i in range(4)}; P.update({7 + i: rows[i] for i in range(4)})
    todo = [4, 5, 6]
    while todo:
        for c in list(todo):
            a, b = w[c]
            if a in P and b in P: P[c] = [x + be[c] * y for x, y in zip(P[a], P[b])]; todo.remove(c)
    polys = []
    for c in range(7, 11):
        a, b = w[c]; polys += [m for m in minors3(P[a], P[b], P[c]) if m != 0]
    G = groebner(polys, *be.values(), domain=QQ.frac_field(tau), order='lex')
    sols = solve(G.exprs, list(be.values()), dict=True) if G.exprs != [1] else []
    good = None
    for s in sols:
        if len(s) < 3 or any(v.free_symbols - {tau} for v in s.values()): continue
        Q = {c: [cancel(x.subs(s)) if hasattr(x, 'subs') else x for x in P[c]] for c in P}
        ok = all(all(cancel(m) == 0 for m in minors3(Q[w[c][0]], Q[w[c][1]], Q[c])) and indep(Q[w[c][0]], Q[w[c][1]]) for c in range(4, 11))
        ok = ok and all(indep(Q[i], Q[j]) for i, j in itertools.combinations(range(11), 2))
        if not ok: continue
        # exact replay at numbers
        fails = []
        for t in TEST:
            try:
                Qt = {c: [Rational(x).subs(tau, t) if not hasattr(x, 'subs') else x.subs(tau, t) for x in Q[c]] for c in Q}
                good_t = all(all(m == 0 for m in minors3(Qt[w[c][0]], Qt[w[c][1]], Qt[c])) and indep(Qt[w[c][0]], Qt[w[c][1]]) for c in range(4, 11)) \
                    and all(indep(Qt[i], Qt[j]) for i, j in itertools.combinations(range(11), 2)) and all(all(x.is_finite for x in Qt[c]) for c in Qt)
            except Exception: good_t = False
            if not good_t: fails.append(str(t))
        good = (s, fails); break
    if good:
        nok += 1
        print('shape', name, ': circuit for tau a symbol, betas', {str(k): str(factor(v)) for k, v in good[0].items()}, '| this family degenerates at tau in', good[1] or 'none of 3, 5/7, -2, -1, 2, 1/2', flush=True)
    else: print('shape', name, ': NO family over Q(tau) with this naming; basis', G.exprs, flush=True)
print('shapes with an exact circuit for tau a symbol: %d of %d' % (nok, n))
