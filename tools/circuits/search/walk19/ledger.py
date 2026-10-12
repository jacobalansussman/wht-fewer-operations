#!/usr/bin/env python3
"""g-1 ledger.py: take apart the known winners (7 gates at 4 points, 22 at 8, 56 at 16, 336 at 64) and the textbook.
Count (G).  Exact integers.  For every wire: s = non-zeros written in the inputs, s' = non-zeros written in the outputs
(the circuit's own outputs; the computed matrix M is checked to be a Hadamard matrix: entries +-1, M M^T = N I, and equal to the
Kronecker product it was built from).  For every gate out = a*u + b*v:
  rise = log2 s(out) - log2 min(s(u), s(v))          (a-2's ledger; sum over gates >= N log2 N)
  drop = log2 max(s'(u), s'(v)) - log2 s'(out)       (the same ledger read in the outputs; sum >= N log2 N as well, g-1.md section 2)
"""
import sys, math, itertools
from fractions import Fraction as Fr

def nz(v): return sum(1 for x in v if x != 0)

class Circ:
    def __init__(self, n):
        self.n = n; self.vec = [tuple(1 if i == j else 0 for i in range(n)) for j in range(n)]; self.gates = []
        self.cur = list(range(n))
    def lin(self, a, u, b, v):
        w = tuple(a * x + b * y for x, y in zip(self.vec[u], self.vec[v])); self.vec.append(w)
        self.gates.append((len(self.vec) - 1, u, v, a, b)); return len(self.vec) - 1
    def block4(self, idx):              # J - 2I on four positions: 3 + 4 gates, hub = the sum
        f = [self.cur[i] for i in idx]
        s = self.lin(1, f[0], 1, f[1]); s = self.lin(1, s, 1, f[2]); s = self.lin(1, s, 1, f[3])
        for t, i in enumerate(idx): self.cur[i] = self.lin(1, s, -2, f[t])
    def bfly(self, i, j):
        a, b = self.cur[i], self.cur[j]; self.cur[i] = self.lin(1, a, 1, b); self.cur[j] = self.lin(1, a, -1, b)

def build(k, plan):
    n = 1 << k; c = Circ(n); digits = list(range(k)); pos = 0
    for part in plan:
        blk = digits[pos:pos + part]; pos += part
        rest = [d for d in digits if d not in blk]
        for base in itertools.product((0, 1), repeat=len(rest)):
            addr0 = sum(bit << d for bit, d in zip(base, rest))
            idx = [addr0 + sum(((t >> q) & 1) << d for q, d in enumerate(blk)) for t in range(1 << len(blk))]
            if len(blk) == 2: c.block4(idx)
            else: c.bfly(idx[0], idx[1])
    return c

def report(name, c, verbose):
    n = c.n; k = n.bit_length() - 1
    M = [c.vec[c.cur[i]] for i in range(n)]
    had = all(abs(x) == 1 for r in M for x in r) and all(sum(M[i][t] * M[j][t] for t in range(n)) == (n if i == j else 0) for i in range(n) for j in range(n))
    def sp(v): return nz([sum(r[t] * v[t] for t in range(n)) for r in M])      # coordinates in the outputs are M v / N
    S = [nz(v) for v in c.vec]; T = [sp(v) for v in c.vec]
    fan = [0] * len(c.vec)
    for (w, u, v, a, b) in c.gates: fan[u] += 1; fan[v] += 1
    rise = drop = slack = 0.0; types = {}; cross = [0] * k; crossd = [0] * k
    for (w, u, v, a, b) in c.gates:
        r = max(0.0, math.log2(S[w]) - math.log2(min(S[u], S[v]))); d = max(0.0, math.log2(max(T[u], T[v])) - math.log2(T[w]))
        rise += r; drop += d
        P = max(S[u] * T[u], S[v] * T[v], S[w] * T[w]); slack += math.log2(1 + 2 * P / n)
        lo, hi = sorted(((S[u], T[u]), (S[v], T[v])))
        key = (lo, hi, (S[w], T[w])); types.setdefault(key, [0, r, d])[0] += 1
        for t in range(k):
            if math.log2(S[w]) > t + 1e-9 and math.log2(min(S[u], S[v])) <= t + 1e-9: cross[t] += 1
            if math.log2(T[w]) < t + 1 - 1e-9 and math.log2(max(T[u], T[v])) >= t + 1 - 1e-9: crossd[t] += 1
    nont = {}
    for i in range(n, len(c.vec)):
        if S[i] * T[i] != n: nont.setdefault((S[i], T[i]), []).append(fan[i])
    print("%s: N = %d, gates = %d, N log2 N = %d, computes a Hadamard matrix: %s" % (name, n, len(c.gates), n * k, had))
    print("   ledger: sum of rises = %.2f, sum of drops = %.2f (each must be >= %d); sum of log2(1 + 2P/N) = %.2f" % (rise, drop, n * k, slack))
    print("   gates crossing each whole threshold of log2 s (each must be >= N): %s ; of log2 s' : %s" % (cross, crossd))
    print("   non-tight wires (s, s'): count, s s'/N, fan-out of each (number of gates that read it):")
    for (s, t), f in sorted(nont.items()):
        print("      (s = %d, s' = %d): %d wires, s s' = %sN, each read by %s gates" % (s, t, len(f), Fr(s * t, n), sorted(set(f))))
    if not nont: print("      none")
    print("   gate types (smaller input (s,s'), larger input (s,s'), output (s,s')): count, rise, drop")
    for key, (cnt, r, d) in sorted(types.items()):
        print("      %s + %s -> %s : %d gates, rise %.2f, drop %.2f" % (key[0], key[1], key[2], cnt, r, d))
    if verbose:
        for (w, u, v, a, b) in c.gates:
            print("      g%-3d = %d*w%d + %d*w%d   (s,s'): %s %s -> %s   %s" % (w, a, u, b, v, (S[u], T[u]), (S[v], T[v]), (S[w], T[w]), list(c.vec[w])))
    return rise, drop

if __name__ == "__main__":
    for k, plan in ((2, (1, 1)), (3, (1, 1, 1)), (4, (1, 1, 1, 1)), (6, (1,) * 6)):
        report("textbook", build(k, plan), False)
    for k, plan, verbose in ((2, (2,), True), (3, (2, 1), True), (3, (1, 2), False), (4, (2, 2), False), (6, (2, 2, 2), False)):
        report("bricks %s" % "+".join(str(1 << p) for p in plan), build(k, plan), verbose)
    # the caterpillar: one output of the N-point transform by a chain of N - 1 additions pays the rise ledger almost in full
    for k in (2, 4, 6, 10, 20):
        n = 1 << k; r = sum(math.log2(j + 1) for j in range(1, n))
        print("chain of %d additions (one output of the %d-point transform): sum of rises = log2(N!) = %.1f against N log2 N = %d (ratio %.3f)" % (n - 1, n, r, n * k, r / (n * k)))
