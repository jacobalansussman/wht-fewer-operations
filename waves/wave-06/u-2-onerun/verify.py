# u-2-onerun: second, independent implementation (pure Python) of the one-run search, and exact replay of a "yes".
#   python3 verify.py tree <k>      every output = one comparable output (or nothing) plus or minus one run: exhaustive
#   python3 verify.py path <k>      the outputs form a path ending in "nothing": exhaustive
# The consecutive-ones test here is written differently from onerun.c: it grows the order element by element (no merging of
# twins into blocks), with the rule "an input may be placed only if every set that is begun and not finished contains it",
# and it returns the order, which is then used to replay a solution on all N basis vectors with whole numbers.
import sys
sys.setrecursionlimit(10000)

def c1p_order(sets, N):
    """sets: list of bit masks over N inputs.  Returns an order (list of inputs) making every set consecutive, or None."""
    elems = [x for x in range(N) if any(s >> x & 1 for s in sets)]
    free = [x for x in range(N) if x not in elems]
    sig = {x: tuple(i for i, s in enumerate(sets) if s >> x & 1) for x in elems}
    size = [bin(s).count('1') for s in sets]
    order = []; cnt = [0] * len(sets); used = set()
    # the number of different signatures can be at most 2n - 1
    if len(set(sig.values())) > 2 * len(sets) - 1: return None
    def rec():
        if len(order) == len(elems): return True
        openm = [i for i in range(len(sets)) if 0 < cnt[i] < size[i]]
        tried = set()
        if not openm:
            # nothing is open: what is placed is closed off, the rest is an independent problem; start it anywhere,
            # but if the rest fails from every start of ONE component, the whole fails.  Take the component of the first unused input.
            first = next(x for x in elems if x not in used)
            comp = {first}; grow = True
            while grow:
                grow = False
                for x in elems:
                    if x in used or x in comp: continue
                    if any(set(sig[x]) & set(sig[y]) for y in comp): comp.add(x); grow = True
            cands = sorted(comp)
        else:
            cands = [x for x in elems if x not in used and all(i in sig[x] for i in openm)]
        for x in cands:
            if sig[x] in tried: continue           # two inputs with the same memberships are interchangeable here
            tried.add(sig[x])
            used.add(x); order.append(x)
            for i in sig[x]: cnt[i] += 1
            if rec(): return True
            for i in sig[x]: cnt[i] -= 1
            order.pop(); used.discard(x)
        return False
    return (order + free) if rec() else None

def main():
    mode, k = sys.argv[1], int(sys.argv[2]); N = 1 << k
    down = [sum(1 << T for T in range(N) if T & S == T) for S in range(N)] + [0]
    nodes = [0]; sol = []
    if mode == 'tree':
        ordv = sorted(range(N), key=lambda v: -bin(v).count('1'))
        uf = list(range(N + 1))
        def find(x):
            while uf[x] != x: x = uf[x]
            return x
        fam = []; par = {}
        deepest = [0]
        def rec(i):
            nodes[0] += 1; deepest[0] = max(deepest[0], i)
            if i == N: sol.append((dict(par), list(fam))); return True
            v = ordv[i]
            for p in range(N, -1, -1):
                if p == v: continue
                if p == N: lo, hi = N, v
                elif v & p == v: lo, hi = v, p
                elif v & p == p: lo, hi = p, v
                else: continue
                rv, rp = find(v), find(p)
                if rv == rp: continue
                fam.append(down[hi] & ~down[lo])
                if c1p_order(fam, N) is not None:
                    par[v] = p; uf[rv] = rp
                    if rec(i + 1): return True
                    uf[rv] = rv; del par[v]
                fam.pop()
            return False
        found = rec(0)
        print(f"k={k} tree (independent Python search): nodes {nodes[0]}, deepest level reached {deepest[0]} of {N}, solution found: {found}")
        if found:
            par, fam = sol[0]
            order = c1p_order(fam, N); pos = {x: i for i, x in enumerate(order)}
            # the circuit: F_b = running sums in this order (N - 1 gates); each tree edge: y_hi = y_lo + (F_j - F_(i-1))
            gates = N - 1; edges = []
            for v, p in par.items():
                lo, hi = (p, v) if (p == N or v & p == p) else (v, p)
                run = down[hi] & ~down[lo]; ps = sorted(pos[x] for x in range(N) if run >> x & 1)
                assert ps == list(range(ps[0], ps[-1] + 1)), "not a run"
                g = (0 if ps[0] == 0 else 1) + (0 if lo == N else 1)   # one subtraction unless the run is a beginning; one addition unless the neighbour is "nothing"
                if ps[0] == 0 and lo == N: g = 0                        # the output IS a running sum
                gates += g; edges.append((lo, hi, ps[0], ps[-1]))
            ok = True
            for e in range(N):                                           # basis vector x_e = 1
                F = []; s = 0
                for b in range(N): s += (1 if order[b] == e else 0); F.append(s)
                y = {N: 0}; todo = list(edges)
                while todo:
                    rest = []
                    for (lo, hi, a, b) in todo:
                        r = F[b] - (F[a - 1] if a else 0)
                        if lo in y: y[hi] = y[lo] + r
                        elif hi in y: y[lo] = y[hi] - r
                        else: rest.append((lo, hi, a, b))
                    todo = rest
                for S in range(N):
                    if y[S] != (1 if S & e == e else 0): ok = False
            print(f"  input order: {order}")
            print(f"  edges (lower output, upper output, first and last position of the run; {N} = nothing): {edges}")
            print(f"  gates (G) = {gates}; Yates = {N//2*k}; exact replay on {N} basis vectors: {ok}")
    else:
        deepest = [0]
        def recp(path, visited, fam):
            nodes[0] += 1; deepest[0] = max(deepest[0], len(path))
            if len(path) == N: return True
            cur = path[-1]
            for v in range(N):
                if visited >> v & 1: continue
                if v & cur == v: lo, hi = v, cur
                elif v & cur == cur: lo, hi = cur, v
                else: continue
                fam.append(down[hi] & ~down[lo])
                if c1p_order(fam, N) is not None:
                    path.append(v)
                    if recp(path, visited | 1 << v, fam): return True
                    path.pop()
                fam.pop()
            return False
        total = False
        for j in (range(k + 1) if len(sys.argv) < 4 else [int(sys.argv[3])]):
            last = (1 << j) - 1
            f = recp([last], 1 << last, [down[last]])
            print(f"k={k} path (independent Python search), last output of size {j}: found {f}; nodes so far {nodes[0]}; longest partial path {deepest[0]} of {N}", flush=True)
            total |= f
        print("ANY SOLUTION:", total)
main()
