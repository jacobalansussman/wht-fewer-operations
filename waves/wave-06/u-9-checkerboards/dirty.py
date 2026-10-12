# u-9: the "dirty" circuit: a whole-number circuit whose N outputs are congruent to the rows of the transform modulo 4, in which
# EVERY wire, read modulo 2, is the indicator of a node of ONE merge tree (the cube tree), with no division by 2 anywhere.
# The trick: a wire may carry entries 2 (modulo 4) OUTSIDE its class.  Count (G): a gate is a*u + b*v.
# Wires are whole-number vectors over the N inputs; every gate is replayed exactly; the check is on all N x N entries.
import sys
def pc(v): return bin(v).count("1")
def run(k):
    N = 1 << k; gates = [0]; wires = []
    def gate(a, u, b, v):
        gates[0] += 1; w = [a * p + b * q for p, q in zip(u, v)]; wires.append(w); return w
    unit = [[1 if i == x else 0 for i in range(N)] for x in range(N)]
    # tree sums: node (depth d, prefix p) = addresses whose top d bits are p ; bit index of depth d (1-based) is k - d
    tsum = {}
    for x in range(N): tsum[(k, x)] = unit[x]
    for d in range(k - 1, -1, -1):
        for p in range(1 << d): tsum[(d, p)] = gate(1, tsum[(d + 1, 2 * p)], 1, tsum[(d + 1, 2 * p + 1)])
    def build(d, p, dirs):
        # returns {u: wire congruent to (indicator of the node) + 2 * (indicator of {x : u.x odd}) modulo 4}, u in the span of dirs
        if not dirs: return {0: tsum[(d, p)]}
        if len(dirs) == 1 or d == k:
            out = {0: tsum[(d, p)]}
            # walk through the span of dirs in Gray order; adding direction bit i costs one shift per node of the hyperplane
            span = [0]
            for i in dirs: span = span + [u | (1 << i) for u in reversed(span)]
            for a in range(1, len(span)):
                i = (span[a] ^ span[a - 1]).bit_length() - 1; dd = k - i          # bit i is decided at depth dd
                w = out[span[a - 1]]
                for q in range(1 << dd):
                    if q & 1: w = gate(1, w, 2, tsum[(dd, q)])                       # shift by 2 x (a tree wire)
                out[span[a]] = w
            return out
        h = len(dirs) // 2
        A = build(d + 1, 2 * p, dirs[:h]); B = build(d + 1, 2 * p + 1, dirs[h:])
        return {u1 | u2: gate(1, A[u1], 1, B[u2]) for u1 in A for u2 in B}
    out = build(0, 0, list(range(k)))
    ok = all((out[y][x] - (-1) ** pc(y & x)) % 4 == 0 for y in range(N) for x in range(N))
    exact = all(out[y][x] == (-1) ** pc(y & x) for y in range(N) for x in range(N))
    # classes: primitive form modulo 2 of every wire (entries are whole numbers; divide out common powers of 2)
    nodes = set()
    for d in range(k + 1):
        for p in range(1 << d): nodes.add(frozenset(x for x in range(N) if x >> (k - d) == p))
    good = True; dirty = 0
    for w in wires:
        v = w[:]
        while all(e % 2 == 0 for e in v): v = [e // 2 for e in v]
        cls = frozenset(x for x in range(N) if v[x] % 2)
        good &= cls in nodes; dirty += any(v[x] % 4 == 2 for x in range(N))
    print(f"N={N}: {gates[0]} gates (G) = {gates[0] / N:.2f} N ; congruent to the transform modulo 4: {ok} ; equal to it: {exact} ; every wire's class is a node of the cube tree: {good} ; "
          f"wires carrying a 2 (mod 4) outside their class: {dirty} ; clean-game floor N - 1 + (N/2) log2 N = {N - 1 + k * N // 2} ; textbook {N * k}", flush=True)
for k in range(1, 9): run(k)
