#!/usr/bin/env python3
"""r2_exact.py (r-2): exact statements, tau a symbol (sympy, rational arithmetic; no primes).
E1  the facts about K_tau (x) K_tau that the hand proof "no 6-gate circuit at 4 points for any tau other than 0, 1" uses.
E1b the 2 x 2 minors of the weight-only block S_tau (k = 2): the hand proof "no 4-gate circuit unless tau = -1" uses that none vanishes.
E2  the 28th shape (no hub), EVERY naming of inputs and outputs (24 x 24): for which tau does a circuit with that wiring exist?
    wiring (p-0's S27): 4<-(0,1) 5<-(0,2) 6<-(3,4) 7<-(2,6) 8<-(4,7) 9<-(5,6) 10<-(5,8); 0-3 inputs, 4-6 helpers, 7-10 outputs."""
import itertools, sys
from sympy import symbols, Matrix, factor, groebner, factor_list, Poly, cancel, Rational
tau, b4, b5, b6 = symbols('tau b4 b5 b6')
rows = [[tau ** bin(w & x).count('1') for x in range(4)] for w in range(4)]
print('E1. rows of K (x) K:', rows)
# two rows proportional on a pair of columns <=> a 2 x 2 minor vanishes
bad3 = []; pairs_at = {}
for w, v in itertools.combinations(range(4), 2):
    for c in itertools.combinations(range(4), 2):
        mn = factor(rows[w][c[0]] * rows[v][c[1]] - rows[w][c[1]] * rows[v][c[0]])
        pairs_at[(w, v, c)] = mn
print('   2 x 2 minors (rows, columns) that vanish identically:', [k for k, mn in pairs_at.items() if mn == 0])
# two rows proportional on THREE columns: all three minors inside a triple vanish
for w, v in itertools.combinations(range(4), 2):
    for tr in itertools.combinations(range(4), 3):
        ms = [pairs_at[(w, v, c)] for c in itertools.combinations(tr, 2)]
        if all(mn == 0 for mn in ms): bad3.append((w, v, tr))
        else:
            # values of tau at which all three vanish: gcd of the non-zero ones
            from sympy import gcd
            g = 0
            for mn in ms: g = gcd(g, mn)
            fl = [f for f, e in factor_list(g)[1]]
            if any(f not in (tau, tau - 1) for f in fl): print('   !! rows', w, v, 'agree on columns', tr, 'when', fl)
print('   pairs of rows proportional on three columns for every tau:', bad3 or 'none', '(other tau: only factors tau, tau - 1, checked above)')
# three rows pairwise proportional on the same two columns
for tri in itertools.combinations(range(4), 3):
    for c in itertools.combinations(range(4), 2):
        from sympy import gcd
        g = 0
        for w, v in itertools.combinations(tri, 2): g = gcd(g, pairs_at[(w, v, c)])
        fl = [f for f, e in factor_list(g)[1]]
        if g == 0 or any(f not in (tau, tau - 1) for f in fl): print('   !! three rows', tri, 'pairwise proportional on columns', c, 'when', fl)
print('   three rows pairwise proportional on two columns: only at tau = 0 or 1 (no line printed above)')
print('   determinant of K (x) K:', factor(Matrix(rows).det()))
S = Matrix([[1, 2, 1], [1, 1 + tau, tau], [1, 2 * tau, tau ** 2]])
print('E1b. weight-only block S_tau, its nine 2 x 2 minors:')
for w, v in itertools.combinations(range(3), 2):
    print('   rows', w, v, [str(factor(S[w, c[0]] * S[v, c[1]] - S[w, c[1]] * S[v, c[0]])) for c in itertools.combinations(range(3), 2)])
print('   entries:', [str(factor(x)) for x in S], ' determinant:', factor(S.det()))
sys.stdout.flush()
# E2
E = [[int(i == j) for j in range(4)] for i in range(4)]
def minors(u, v, t):
    M = Matrix([u, v, t]); out = []
    for cols in itertools.combinations(range(4), 3):
        d = M[:, list(cols)].det()
        if d != 0: out.append(d)
    return out
found = {}; nsolv = 0
for sg in itertools.permutations(range(4)):
    P = {i: E[sg[i]] for i in range(4)}
    P[4] = [x + b4 * y for x, y in zip(P[0], P[1])]
    P[5] = [x + b5 * y for x, y in zip(P[0], P[2])]
    P[6] = [x + b6 * y for x, y in zip(P[3], P[4])]
    for pi in itertools.permutations(range(4)):
        T = {7 + i: rows[pi[i]] for i in range(4)}
        polys = minors(P[2], P[6], T[7]) + minors(P[4], T[7], T[8]) + minors(P[5], P[6], T[9]) + minors(P[5], T[8], T[10])
        G = groebner(polys, b4, b5, b6, tau, order='lex')
        el = [g for g in G.exprs if g.free_symbols <= {tau}]
        if not el: print('   naming', sg, pi, ': solvable for generic tau ?!', G.exprs); continue
        from sympy import gcd
        g = 0
        for e in el: g = gcd(g, e)
        fl = tuple(sorted(str(f) for f, e in factor_list(g)[1] if f not in (tau, tau - 1)))
        if fl:
            nsolv += 1; found[fl] = found.get(fl, 0) + 1
print('E2. the 28th shape, all 576 namings, tau a symbol (Groebner basis over the rationals, tau eliminated last).')
print('    namings with a solution at some tau other than 0, 1:', nsolv)
for fl, c in sorted(found.items()): print('    condition on tau: one of the factors', fl, 'vanishes  ->', c, 'namings')
