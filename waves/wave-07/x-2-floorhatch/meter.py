# x-2-floorhatch/meter.py : replay a circuit found by hatch.c EXACTLY (Fractions) and run the floor's bookkeeping on it.
# Count (G).  usage: python3 -B meter.py N file [file ...]     (a file is the output of hatch, or lines "w id : entries : a b")
# 1. Replay: every wire must be a*u + b*v of its two named earlier wires (a, b solved exactly), and the N rows of the transform
#    must all be held.
# 2. The bookkeeping, valid for EVERY linear circuit [derived in x-2.md section 1]:  for a node X of the cube tree (a block of
#    addresses) call a gate NEW AT X when its wire, cut down to X, is not zero, not an input and not proportional to the cut of
#    an earlier wire.  n(X) = number of gates new at X.  The cuts are a circuit for the transform on X, so n(X) >= least count.
#    With X0, X1 the halves:  n(X) = n(X0) + n(X1) + E(X) - B(X),  E = new at X and at neither half, B = new at both halves.
#    The floor theorem is: in its class B = 0 and E >= |X|/2 + 1.   The pairs give E >= |X|/2 in every circuit.
# 3. Which line of the proof fails: (a) a full wire made otherwise than by a join of an X0-wire and an X1-wire or a shift of a
#    full wire; (b) a gate new at both halves (B > 0) or a cut that is not a wire of the class; (c)/(d) E - B < |X|/2 + 1.
import sys
from fractions import Fraction as F
def prim(v):
    nz = [t for t in v if t != 0]
    if not nz: return None
    s = nz[0]; return tuple(F(t) / s for t in v)
def solve(u, v, w, N):
    for i in range(N):
        for j in range(N):
            d = u[i] * v[j] - u[j] * v[i]
            if d != 0:
                a = F(w[i] * v[j] - w[j] * v[i], d); b = F(u[i] * w[j] - u[j] * w[i], d)
                return (a, b) if all(a * u[t] + b * v[t] == w[t] for t in range(N)) else None
    return None
def load(path, N):
    wires = {i: [int(i == j) for j in range(N)] for i in range(N)}; order = []; gates = []
    for line in open(path):
        if not line.startswith('w '): continue
        a, b, c = line[2:].split(':'); x = int(a); vec = [int(t) for t in b.split()]; p, q = [int(t) for t in c.split()]
        assert p in wires and q in wires, 'parent not yet made'
        ab = solve(wires[p], wires[q], vec, N); assert ab is not None, 'not one gate'
        wires[x] = vec; order.append(x); gates.append((x, p, q, ab))
    return wires, order, gates
def kind(u, v, w, ab, N):
    a, b = ab; su = {i for i in range(N) if u[i]}; sv = {i for i in range(N) if v[i]}
    if not (su & sv): return 'join'
    if su == sv: return 'quotient' if abs(a) == abs(b) else 'other'
    if abs(a) * 2 == abs(b) or abs(b) * 2 == abs(a): return 'shift'
    if su < sv or sv < su: return 'unmerge'
    return 'symdiff'
def run(path, N):
    wires, order, gates = load(path, N); k = N.bit_length() - 1
    rows = {tuple(F((-1) ** bin(y & x).count('1')) for x in range(N)) for y in range(N)}
    got = {prim(wires[x]) for x in order}
    assert rows <= got, 'not all rows held'
    kinds = {}
    for (x, p, q, ab) in gates:
        kd = kind(wires[p], wires[q], wires[x], ab, N); kinds[kd] = kinds.get(kd, 0) + 1
    mx = max(abs(t) for x in order for t in wires[x]); nonform = sum(1 for x in order if max(abs(t) for t in wires[x]) > 1)
    fl = N - 1 + (N // 2) * k
    print('%s: N=%d gates=%d (replayed exactly, all %d rows held); floor %d; excess %d; kinds %s; largest entry %d; wires that are not sign vectors %d'
          % (path.split('/')[-1], N, len(order), N, fl, len(order) - fl, dict(sorted(kinds.items())), mx, nonform))
    # the bookkeeping at every node
    def new_at(X):
        seen = set(); out = []
        for x in order:
            c = prim([wires[x][i] for i in X])
            if c is None or sum(1 for t in c if t != 0) < 2 and len(X) > 1 and False: continue
            if sum(1 for t in c if t != 0) == 1: continue
            if c in seen: continue
            seen.add(c); out.append(x)
        return set(out)
    tot = {}; cache = {}
    def rec(X):
        s = len(X); nx = new_at(X); cache[tuple(X)] = nx
        if s == 1: return
        X0, X1 = X[:s // 2], X[s // 2:]; rec(X0); rec(X1)
        n0, n1 = cache[tuple(X0)], cache[tuple(X1)]
        assert n0 <= nx and n1 <= nx
        B = len(n0 & n1); E = len(nx - n0 - n1)
        assert len(nx) == len(n0) + len(n1) + E - B
        t = tot.setdefault(s, [0, 0, 0, 0, 10 ** 9]); t[0] += 1; t[1] += len(nx); t[2] += E; t[3] += B; t[4] = min(t[4], E - B - s // 2 - 1)
    rec(list(range(N)))
    for s in sorted(tot):
        c, n, E, B, dm = tot[s]
        print('   nodes of size %2d: %2d nodes; gates new there, in all %3d (floor %d each); E in all %3d; B in all %3d; sum of (E - B - s/2 - 1) = %3d; least over the nodes %d'
              % (s, c, n, s - 1 + (s // 2) * (s.bit_length() - 1), E, B, E - B - c * (s // 2 + 1), dm))
    # line (a): how each full wire is made
    full = [g for g in gates if all(t != 0 for t in wires[g[0]])]
    h = N // 2; bad = []
    for (x, p, q, ab) in full:
        u, v = wires[p], wires[q]; su = {i for i in range(N) if u[i]}; sv = {i for i in range(N) if v[i]}
        ok = (su == set(range(h)) and sv == set(range(h, N))) or (sv == set(range(h)) and su == set(range(h, N))) or len(su) == N or len(sv) == N
        if not ok: bad.append((x, sorted(su), sorted(sv)))
    print('   full wires %d; made otherwise than "left + right" or from a full wire (line (a) fails): %d %s' % (len(full), len(bad), bad[:4]))
for path in sys.argv[2:]: run(path, int(sys.argv[1]))
