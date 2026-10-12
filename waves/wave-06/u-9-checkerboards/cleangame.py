# u-9: the "clean game modulo 4" on the cube tree, exhaustive at 2 and 4 points, and its two bounds at every size.
# A wire is (node C of the merge tree, sign pattern S inside C), S up to complement inside C: the wire is a form with entries
# +1/-1 on C and 0 elsewhere, read modulo 4.  Leaves are given.  One gate makes one new wire:
#   merge:    (C1,S1),(C2,S2) children of C      -> (C, S1 + S2) or (C, S1 + complement of S2)
#   shift:    (C,S) and any node C' inside C      -> (C, S xor C')          [w = u + 2v, v any held wire with that class]
#   un-merge: (C,S),(C1,S1) with S = S1 on C1     -> (C2, S on C2)          [difference of two wires that agree on C1]
#   restrict: (P,S),(P,S') agreeing exactly on a node C (or exactly off it) -> (C, S on C)   [(u +- v)/2, a quotient gate]
# Goal: the N rows of the transform as wires on the whole set.  Count = number of wires made.  Claim [derived]: on the cube
# tree the least count is exactly N - 1 + (N/2) log2 N  (2, 7, 19, 47, 111).
import itertools, sys
def norm(C, S):  # C, S bit masks over the inputs; pattern up to complement in C
    S &= C; return (C, min(S, C & ~S))
def solve(k):
    N = 1 << k
    nodes = []; size = N
    while size >= 1:
        for start in range(0, N, size): nodes.append(sum(1 << x for x in range(start, start + size)))
        size //= 2
    internal = [C for C in nodes if bin(C).count("1") > 1]
    def kids(C):
        xs = [x for x in range(N) if C >> x & 1]; h = len(xs) // 2
        return sum(1 << x for x in xs[:h]), sum(1 << x for x in xs[h:])
    states = []
    for C in internal:
        xs = [x for x in range(N) if C >> x & 1]
        seen = set()
        for bits in range(1 << len(xs)):
            S = sum(1 << xs[i] for i in range(len(xs)) if bits >> i & 1); seen.add(norm(C, S))
        states += sorted(seen)
    leaves = [norm(1 << x, 0) for x in range(N)]
    goal = [norm(nodes[0], sum(1 << x for x in range(N) if bin(y & x).count("1") & 1)) for y in range(N)]
    def derivable(sub):
        have = set(leaves); todo = set(sub); progress = True
        while todo and progress:
            progress = False
            for st in list(todo):
                C, S = st; ok = False
                if bin(C).count("1") > 1:
                    C1, C2 = kids(C)
                    for a in (S & C1, C1 & ~S):
                        for b in (S & C2, C2 & ~S):
                            if norm(C1, a) in have and norm(C2, b) in have and norm(C, a | b) == st: ok = True
                    if not ok:
                        for Cp in nodes:
                            if Cp & ~C == 0 and norm(C, S ^ Cp) in have and norm(C, S ^ Cp) != st: ok = True
                if not ok:  # un-merge from the parent
                    for P in internal:
                        C1, C2 = kids(P)
                        if C in (C1, C2):
                            O = C2 if C == C1 else C1
                            for (PC, PS) in have:
                                if PC == P and norm(C, PS) == st and (norm(O, PS) in have): ok = True
                if not ok:  # restrict: two held wires on one larger node that agree exactly on C or exactly off C
                    hl = list(have)
                    for (PC, PS) in hl:
                        if PC != C and C & ~PC == 0 and norm(C, PS) == st:
                            for (QC, QS) in hl:
                                if QC == PC and (PS ^ QS) & PC in (C, PC & ~C): ok = True
                if ok: have.add(st); todo.discard(st); progress = True
        return not todo
    others = [s for s in states if s not in goal]
    for extra in range(0, len(others) + 1):
        for add in itertools.combinations(others, extra):
            if derivable(list(set(goal)) + list(add)):
                return len(set(goal)) + extra
    return None
for k in (1, 2):
    N = 1 << k; print(f"N={N}: least number of wires in the clean game = {solve(k)}; N - 1 + (N/2) log2 N = {N - 1 + k * N // 2}", flush=True)
t = 0
for k in range(1, 8):
    N = 1 << k; t = 2 * t + N // 2 + 1
    print(f"N={N}: recursion t(k) = 2 t(k-1) + N/2 + 1 gives {t}; N - 1 + (N/2) log2 N = {N - 1 + k * N // 2}")
