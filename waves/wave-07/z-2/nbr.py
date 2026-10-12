# z-2: neighbour sums on the cube with ADDITIONS ONLY (every gate u + v, no subtraction, no coefficient).
# Lower bound proved in z-2.md: N (k - 1 - floor(k/2)/2).  Upper bound: the pairing program, built and replayed here.
# Also the two facts the bound uses: two addresses have at most 2 common neighbours; three addresses at most 1.
import itertools
for k in range(2, 11):
    N = 1 << k
    nb = [frozenset(x ^ (1 << j) for j in range(k)) for x in range(N)]
    if k <= 7:
        two = max(len(nb[x] & nb[y]) for x in range(N) for y in range(x + 1, N))
        three = max(len(nb[0] & nb[y] & nb[z]) for y in range(1, N) for z in range(y + 1, N)) if k <= 6 else 'not run'
    else:
        two = three = 'not run'
    # pairing program: bits (0,1), (2,3), ...; a last single bit if k is odd
    gates = {}          # support (frozenset) -> True ; every gate is a disjoint union of two earlier supports
    def add(a, b):
        assert not (a & b)
        s = a | b
        gates[s] = True
        return s
    outs = []
    for y in range(N):
        parts = []
        for i in range(k // 2):
            a = frozenset([y ^ (1 << (2 * i))]); b = frozenset([y ^ (1 << (2 * i + 1))])
            parts.append(a | b)
            gates[a | b] = True
        if k % 2: parts.append(frozenset([y ^ (1 << (k - 1))]))
        cur = parts[0]
        for p in parts[1:]: cur = add(cur, p)
        outs.append(cur)
    ok = all(outs[y] == nb[y] for y in range(N))
    lower = N * (k - 1) - N * (k // 2) // 2 if (N * (k // 2)) % 2 == 0 else None
    print(f"k={k} N={N}: pairing program {len(gates)} gates, outputs exact: {ok};  lower bound N(k-1-floor(k/2)/2) = {N*(k-1) - N*(k//2)/2:.0f};"
          f"  textbook transform N k = {N*k};  gates per point {len(gates)/N:.2f};  most common neighbours of 2 addresses: {two}, of 3: {three}")
