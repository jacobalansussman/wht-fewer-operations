# z-0/ledger2.py : skeptic's own ledger for x-0 lemmas 1 and 3.  Exact integers (numpy int64; every value here is far below 2^62).
# A circuit = list of gates (i, j, a, b): new wire = a*wire_i + b*wire_j, then divided by the common factor of its entries (primitive).
# Delta_t = largest |N x N minor| among the first N + t wires (the N inputs first).  All minors by Laplace expansion along columns,
# stored by colexicographic rank of the row set, so "subsets of the first m wires" is a prefix of the table.
# Checks, per gate: volume = log2(Delta_t / Delta_(t-1)) <= max(0, log2((|a|+|b|)/g));   a merge: Delta_t/Delta_(t-1) <= max(|a|,|b|);
# number of merges; lemma 2: (|a|+|b|)/g <= 4*M^2 with M = largest entry among the three wires.
import sys, itertools, random
import numpy as np
from math import gcd, comb, log2
from fractions import Fraction as F

def all_minors(W, N):
    R = len(W); A = np.array(W, dtype=np.int64)
    prev = None
    for j in range(1, N + 1):
        C = np.fromiter(itertools.chain.from_iterable(itertools.combinations(range(R), j)), dtype=np.int64, count=comb(R, j) * j).reshape(-1, j)   # sorted rows
        binom = np.array([[comb(r, t) for t in range(j + 2)] for r in range(R + 1)], dtype=np.int64)
        rank = sum(binom[C[:, t], t + 1] for t in range(j))
        cur = np.zeros(comb(R, j), dtype=np.int64)
        if j == 1:
            cur[rank] = A[C[:, 0], 0]
        else:
            val = np.zeros(len(C), dtype=np.int64)
            for t in range(j):                      # remove the t-th row of the set, expand along column j-1
                rest = np.delete(C, t, axis=1)
                rr = sum(binom[rest[:, s], s + 1] for s in range(j - 1))
                sign = 1 if (t + j - 1) % 2 == 0 else -1
                val += sign * A[C[:, t], j - 1] * prev[rr]
            cur[rank] = val
        prev = cur
    return prev                                      # index = colex rank of the N-subset of wires

def prim(v):
    g = 0
    for x in v: g = gcd(g, abs(x))
    return [x // g for x in v], g

def ledger(N, gates, name, quiet=False):
    W = [[1 if i == j else 0 for j in range(N)] for i in range(N)]
    grp = list(range(N)); info = []
    for (i, j, a, b) in gates:
        g0 = gcd(a, b); a //= g0; b //= g0
        w = [a * x + b * y for x, y in zip(W[i], W[j])]
        w, g = prim(w)
        su = {grp[k] for k in range(N) if W[i][k]}; sv = {grp[k] for k in range(N) if W[j][k]}
        assert len(su) == 1 and len(sv) == 1
        gu, gv = su.pop(), sv.pop(); merge = (gu != gv)
        if merge:
            assert g == 1
            grp = [gu if x == gv else x for x in grp]
        hM = max(max(abs(x) for x in W[i]), max(abs(x) for x in W[j]), max(abs(x) for x in w))
        info.append((a, b, g, merge, hM)); W.append(w)
    T = np.abs(all_minors(W, N))
    D = [int(T[:comb(N + t, N)].max()) for t in range(len(gates) + 1)]
    assert D[0] == 1
    bad = 0; nm = 0; totvol = 0.0; lines = []
    for t, (a, b, g, merge, hM) in enumerate(info, 1):
        ratio = F(D[t], D[t - 1]); bud = F(abs(a) + abs(b), g)
        if ratio > max(F(1), bud): bad += 1
        if merge:
            nm += 1
            if ratio > max(abs(a), abs(b)): bad += 1
        if bud > 4 * hM * hM: bad += 1
        lines.append('   gate %2d (%d,%d)/%d %s height %d  Delta x %s  budget %s' % (t, a, b, g, 'MERGE' if merge else '     ', hM, ratio, bud))
    if not quiet:
        print(name); print('\n'.join(lines))
        print('   merges %d ; final Delta %d = 2^%.3f ; violations %d ; connected groups left %d' % (nm, D[-1], log2(D[-1]), bad, len(set(grp))))
    return bad, nm, D[-1], len(set(grp)), info, W

def parse(path, N):
    names = {'x%d' % i: i for i in range(N)}; gates = []; order = []
    for line in open(path):
        line = line.split('#')[0].strip()
        if not line or '=' not in line: continue
        lhs, rhs = [s.strip() for s in line.split('=')]
        rhs = rhs.replace('- ', '+ -').replace('+ -', '+ -')
        parts = [p.strip() for p in rhs.split('+')]
        terms = []
        for p in parts:
            p = p.replace(' ', '')
            if '*' in p: c, nm = p.split('*'); c = F(c)
            elif p.startswith('-'): c, nm = F(-1), p[1:]
            else: c, nm = F(1), p
            terms.append((c, names[nm]))
        assert len(terms) == 2, line
        den = terms[0][0].denominator * terms[1][0].denominator          # fractions -> whole numbers (the ledger reduces them)
        gates.append((terms[0][1], terms[1][1], int(terms[0][0] * den), int(terms[1][0] * den))); names[lhs] = N + len(gates) - 1; order.append(lhs)
    return gates

def holds_H(W, N):
    S = {tuple(w) for w in W} | {tuple(-x for x in w) for w in W}
    k = N.bit_length() - 1
    return all(tuple((-1) ** bin(y & x).count('1') for x in range(N)) in S for y in range(N))

mode = sys.argv[1]
if mode == 'files':
    N = int(sys.argv[2])
    for path in sys.argv[3:]:
        gates = parse(path, N)
        bad, nm, Dl, groups, info, W = ledger(N, gates, path.split('/')[-1] + '  (%d gates)' % len(gates))
        tall = max(h for *_, h in info)
        need = (N // 2) * log2(N)
        print('   holds every row of H: %s ; (N/2)log2 N = %.1f ; largest height M = %d ; lemma 3 with this M: %.2f gates' % (
            holds_H(W, N), need, tall, N - 1 + (need - (N - 1) * log2(tall)) / (log2(4 * tall * tall) if tall > 1 else log2(3))))
        capsum = sum(max(0.0, log2((abs(a) + abs(b)) / g)) if not m else log2(max(abs(a), abs(b))) for a, b, g, m, h in info)
        print('   sum of the per-gate caps (merge: log2 max(|a|,|b|); other: max(0, budget)) = %.3f' % capsum)
elif mode == 'random':
    N, ngates, trials, cmax, seed = map(int, sys.argv[2:7]); rnd = random.Random(seed)
    tot = 0; totbad = 0; merges_seen = 0; negb = 0; quot = 0; tallest = 0; fullconn = 0; wrongmerge = 0
    for tr in range(trials):
        W = [[1 if i == j else 0 for j in range(N)] for i in range(N)]; gates = []
        while len(gates) < ngates:
            i, j = rnd.sample(range(len(W)), 2)
            if rnd.random() < 0.35:          # look for a combination with a common factor (a quotient gate)
                cand = [(a, b) for a in range(-cmax, cmax + 1) for b in range(-cmax, cmax + 1) if a and b and gcd(a, b) == 1
                        and prim([a * x + b * y for x, y in zip(W[i], W[j])])[1] > 1 and any(a * x + b * y for x, y in zip(W[i], W[j]))]
                if not cand: continue
                a, b = rnd.choice(cand)
            else:
                a = rnd.choice([c for c in range(-cmax, cmax + 1) if c]); b = rnd.choice([c for c in range(-cmax, cmax + 1) if c])
            w = [a * x + b * y for x, y in zip(W[i], W[j])]
            if not any(w): continue
            w, g = prim(w)
            if w in W or [-x for x in w] in W: continue
            if max(abs(x) for x in w) > 40: continue
            gates.append((i, j, a, b)); W.append(w)
        bad, nm, Dl, groups, info, W2 = ledger(N, gates, '', quiet=True)
        tot += len(gates); totbad += bad; merges_seen += nm
        negb += sum(1 for a, b, g, m, h in info if abs(a) + abs(b) < g); quot += sum(1 for a, b, g, m, h in info if g > 1)
        tallest = max(tallest, max(h for *_, h in info))
        if groups == 1:
            fullconn += 1
            if nm != N - 1: wrongmerge += 1
        elif nm != N - groups: wrongmerge += 1
    print('random circuits: N=%d gates each=%d trials=%d coefficients up to %d seed=%d' % (N, ngates, trials, cmax, seed))
    print('   gate lines %d ; merges %d ; quotient gates (g>1) %d ; gates with negative budget %d ; tallest wire %d' % (tot, merges_seen, quot, negb, tallest))
    print('   circuits that end connected %d ; circuits whose merge count is not N - (groups left) %d' % (fullconn, wrongmerge))
    print('   VIOLATIONS of (volume <= max(0,budget)) or (merge factor <= max(|a|,|b|)) or (budget <= 4 M^2): %d' % totbad)
