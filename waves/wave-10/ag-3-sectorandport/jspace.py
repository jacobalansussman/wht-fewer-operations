#!/usr/bin/env python3
"""jspace.py [ag-3-sectorandport]  EXACT (phases are fourth roots of 1, kept as integers modulo 4; no floats, no primes).
Question: for a given set of FREE steps, is there a linear map J on the data of one array with
      J a = a J for every free step a      and      J D = - D J      (D = the move along the port p, on all f columns)?
If J is not 0, the count "f free moves need f + 1 shears" holds for that set of free steps (lemma in ag-3.md section 2).
In the character basis (simultaneous eigenvectors of all shifts) every step of the engine is MONOMIAL:
  a configuration is f characters chi_1..chi_f of the h address bits of a column;
  D_p            : diagonal, i^(number of columns with chi_c.p = 1)
  shift S_w      : diagonal, (-1)^(chi_c.w) on each column it acts on
  sign pattern   : chi_c -> chi_c + psi
  address map g  : chi_c -> A chi_c,  A = inverse transpose of g
So J a = a J reads  J[a j, a k] = phase_a(j) / phase_a(k) * J[j, k], and J D = - D J reads J[j, k] = 0 unless D_j = - D_k.
dim of the solution space = number of orbits of pairs (j, k) on which D_j = - D_k throughout and the phases are consistent.
Computed by a union-find with phases.  Controls: one column (no J: D has eigenvalues 1 and i only); D itself added to the free steps (no J)."""
import sys, itertools
def par(x): return bin(x).count("1") & 1
def run(h, f, p, gens_spec, label):
    n = 1 << h; N = n ** f
    cfg = [tuple((i // n ** c) % n for c in range(f)) for i in range(N)]
    idx = lambda xs: sum(x * n ** c for c, x in enumerate(xs))
    Dph = [sum(par(x & p) for x in xs) % 4 for xs in cfg]
    gens = []     # (perm list, phase list modulo 4)
    def lin(cols):   # linear map on h-bit ints given images of basis bits
        def A(x):
            y = 0
            for b in range(h):
                if x >> b & 1: y ^= cols[b]
            return y
        return A
    for g in gens_spec:
        kind = g[0]
        if kind == "shift":          # ("shift", w, columns or None)
            w, cs = g[1], (range(f) if g[2] is None else g[2])
            gens.append((list(range(N)), [2 * sum(par(xs[c] & w) for c in cs) % 4 for xs in cfg]))
        elif kind == "sign":
            psi, cs = g[1], (range(f) if g[2] is None else g[2])
            gens.append(([idx(tuple(x ^ psi if c in cs else x for c, x in enumerate(xs))) for xs in cfg], [0] * N))
        elif kind == "map":          # ("map", images of basis bits on CHARACTERS, columns or None)
            A, cs = lin(g[1]), (range(f) if g[2] is None else g[2])
            assert len({A(x) for x in range(n)}) == n
            gens.append(([idx(tuple(A(x) if c in cs else x for c, x in enumerate(xs))) for xs in cfg], [0] * N))
        elif kind == "D":            # control: the move itself as a free step
            gens.append((list(range(N)), Dph[:]))
        elif kind == "colperm":      # permutation of the columns (never an engine step; control)
            s = g[1]
            gens.append(([idx(tuple(xs[s[c]] for c in range(f))) for xs in cfg], [0] * N))
    M = N * N
    parent = list(range(M)); ph = [0] * M; dead = [False] * M
    def find(x):
        path = []
        while parent[x] != x:
            path.append(x); x = parent[x]
        # compress with phases: ph[node] = exponent with J_node = i^ph * J_parent
        acc = 0
        for y in reversed(path):
            acc = (acc + ph[y]) % 4; ph[y] = acc; parent[y] = x
        return x
    for j in range(N):
        for k in range(N):
            if (Dph[j] - Dph[k]) % 4 != 2: dead[j * N + k] = True
    for perm, phase in gens:
        for j in range(N):
            aj = perm[j]; pj = phase[j]
            for k in range(N):
                a = j * N + k; b = aj * N + perm[k]; d = (pj - phase[k]) % 4      # J_b = i^d J_a
                ra = find(a); rb = find(b)
                if ra == rb:
                    if (ph[b] - ph[a] - d) % 4 != 0: dead[ra] = True
                else:
                    # J_a = i^ph[a] J_ra ; J_b = i^ph[b] J_rb ; want J_b = i^d J_a  =>  J_rb = i^(d + ph[a] - ph[b]) J_ra
                    parent[rb] = ra; ph[rb] = (d + ph[a] - ph[b]) % 4
                    if dead[rb]: dead[ra] = True
    # a root is alive if no member is dead
    alive = {}
    for x in range(M):
        r = find(x)
        if dead[x]: dead[r] = True
    roots = {find(x) for x in range(M)}
    live = [r for r in roots if not dead[r]]
    # describe the smallest live orbit
    desc = ""
    if live:
        size = {}
        for x in range(M): size[find(x)] = size.get(find(x), 0) + 1
        r = min(live, key=lambda r: size[r]); j, k = divmod(r, N)
        desc = " ; smallest orbit has %d pairs, e.g. J sends configuration %s to %s" % (size[r], cfg[k], cfg[j])
    print("h=%d f=%d port %s  %-58s : dim of the J space = %d%s" % (h, f, bin(p)[2:].zfill(h), label, len(live), desc), flush=True)
    return len(live)
def classes(h, f, p):
    E = [1 << b for b in range(h)]
    sh = [("shift", w, None) for w in E]; sg = [("sign", w, None) for w in E]
    base = sh + sg
    out = [("scalars only", []), ("shifts and sign patterns (alike on all columns)", base)]
    out.append(("CONTROL: the move D itself free", base + [("D",)]))
    if f >= 2: out.append(("CONTROL: + a permutation of two columns", base + [("colperm", [1, 0] + list(range(2, f)))]))
    if h == 2 and p == 1:
        out.append(("+ address shear along p (x2 -> x2 + p)", base + [("map", [1 | 2, 2], None)]))        # character map chi -> chi + e2 (p.chi): bit0 image = e1+e2
        out.append(("+ address map exchanging p and q", base + [("map", [2, 1], None)]))
        out.append(("+ every address map (all of GL(2,2))", base + [("map", [2, 1], None), ("map", [3, 2], None)]))
    if h == 3 and p == 1:
        out.append(("+ orthogonal maps fixing p (swap of bits 2,3)", base + [("map", [1, 4, 2], None)]))
        out.append(("+ all maps fixing p and psi = p (GL(2,2) on bits 2,3)", base + [("map", [1, 4, 2], None), ("map", [1, 2 | 4, 4], None)]))
        out.append(("+ address shear along p (x2 -> x2 + p)", base + [("map", [1 | 2, 2, 4], None)]))
        out.append(("+ address map exchanging p and q (bits 1,2)", base + [("map", [2, 1, 4], None)]))
        out.append(("+ every orthogonal map (all permutations of bits)", base + [("map", [2, 1, 4], None), ("map", [1, 4, 2], None)]))
        out.append(("+ every address map (all of GL(3,2))", base + [("map", [2, 1, 4], None), ("map", [2, 4, 1], None), ("map", [3, 2, 4], None)]))
    if h == 3 and p == 7:
        out.append(("+ every orthogonal map (they all fix p = 111)", base + [("map", [2, 1, 4], None), ("map", [1, 4, 2], None)]))
        out.append(("+ every address map (all of GL(3,2))", base + [("map", [2, 1, 4], None), ("map", [2, 4, 1], None), ("map", [3, 2, 4], None)]))
    if f >= 2:
        out.append(("+ shift along p on column 0 only", base + [("shift", p, [0])]))
        out.append(("+ shift along p on EACH column separately", base + [("shift", p, [c]) for c in range(f)]))
        out.append(("+ shift along p on each column but one", base + [("shift", p, [c]) for c in range(1, f)]))
        out.append(("+ shift along p on each column but two", base + [("shift", p, [c]) for c in range(2, f)]))
        out.append(("+ every sign pattern on column 0 only", base + [("sign", w, [0]) for w in E]))
        out.append(("+ every sign pattern on EACH column separately", base + [("sign", w, [c]) for w in E for c in range(f)]))
        out.append(("+ every sign pattern on each column but two", base + [("sign", w, [c]) for w in E for c in range(2, f)]))
        out.append(("+ shifts and signs on each column but two", base + [("sign", w, [c]) for w in E for c in range(2, f)] + [("shift", w, [c]) for w in E for c in range(2, f)]))
    return out
if __name__ == "__main__":
    jobs = sys.argv[1:] or ["2,1,1", "2,2,1", "2,3,1", "3,2,1", "3,2,7"]
    for job in jobs:
        h, f, p = map(int, job.split(","))
        for label, spec in classes(h, f, p): run(h, f, p, spec, label)
        print()
