# u-9: do tonight's record circuits satisfy the hypotheses of the form-game floor (section 4 of u-9.md)?
# For each gate-list file: replay exactly, then for every wire: is it a form (entries 0, +c, -c)?  is its set a coset of a
# subspace of addresses?  are all sets nested or disjoint (one tree)?  do the subspaces form one chain (a "coset tree")?
import re, sys
from fractions import Fraction
def parse(fn):
    wires = {}; order = []; n = 0
    for line in open(fn):
        line = line.split("#")[0].strip()
        if "=" not in line: continue
        name, rhs = [s.strip() for s in line.split("=", 1)]
        terms = re.findall(r"([+-]?\s*\d*(?:/\d+)?)\s*\*?\s*([A-Za-z_]\w*)", rhs)
        t2 = []
        for c, v in terms:
            c = c.replace(" ", "")
            c = Fraction(1) if c in ("", "+") else Fraction(-1) if c == "-" else Fraction(c)
            t2.append((c, v))
            if re.fullmatch(r"x\d+", v): n = max(n, int(v[1:]) + 1)
        order.append((name, t2))
    N = 1
    while N < n: N *= 2
    for i in range(N): wires[f"x{i}"] = [Fraction(int(i == j)) for j in range(N)]
    gates = 0
    for name, t2 in order:
        vec = [Fraction(0)] * N
        for c, v in t2: vec = [a + c * b for a, b in zip(vec, wires[v])]
        wires[name] = vec; gates += 1
    return N, gates, order, wires
def is_coset(sup):
    sup = sorted(sup); b = sup[0]; diffs = set(s ^ b for s in sup)
    return all((p ^ q) in diffs for p in diffs for q in diffs), frozenset(diffs)
for fn in sys.argv[1:]:
    N, gates, order, wires = parse(fn); k = N.bit_length() - 1
    H = [[(-1) ** bin(y & x).count("1") for x in range(N)] for y in range(N)]
    outs = 0
    for name, _ in order:
        v = wires[name]
        for y in range(N):
            if any(v) and (all(a == b for a, b in zip(v, H[y])) or all(a == -b for a, b in zip(v, H[y]))): outs += 1; break
    nonform = []; noncoset = []; sets = set(); spaces = set()
    for name, t2 in order:
        v = wires[name]; nz = [abs(a) for a in v if a]
        if len(set(nz)) != 1: nonform.append(name)
        sup = [x for x in range(N) if v[x]]; sets.add(frozenset(sup))
        ok, sp = is_coset(sup)
        if not ok: noncoset.append(name)
        else: spaces.add(sp)
    laminar = all(a <= b or b <= a or not (a & b) for a in sets for b in sets)
    chain = all(a <= b or b <= a for a in spaces for b in spaces)
    maxterms = max(len(t2) for _, t2 in order)
    print(f"{fn.split('/')[-2]}/{fn.split('/')[-1]}: N={N}, lines {gates} (largest number of terms on a line {maxterms}), lines that are rows of H up to sign {outs}; "
          f"non-form wires {len(nonform)} {nonform[:6]}; sets that are not cosets {len(noncoset)}; all sets nested or disjoint: {laminar}; "
          f"subspaces form one chain: {chain}; form floor N-1+(N/2)log2N = {N - 1 + k * N // 2}", flush=True)
