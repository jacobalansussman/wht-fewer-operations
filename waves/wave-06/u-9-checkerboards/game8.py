# u-9: a search for a counterexample to the form-game floor at 8 points.  Sets of W wires (the 8 outputs + W - 8 others among
# the 144 other possible wires on the cube tree) are annealed on "number of wires that cannot be derived".  A set with 0 is a
# legal play with W wires.  The floor says: possible for W = 19, impossible for W = 18.  A search is no proof of impossibility.
import random, sys
k = 3; N = 8; W = int(sys.argv[1]); iters = int(sys.argv[2]); seed = int(sys.argv[3])
def norm(C, S): S &= C; return (C, min(S, C & ~S))
nodes = []; size = N
while size >= 1:
    for start in range(0, N, size): nodes.append(sum(1 << x for x in range(start, start + size)))
    size //= 2
internal = [C for C in nodes if bin(C).count("1") > 1]
def kids(C):
    xs = [x for x in range(N) if C >> x & 1]; h = len(xs) // 2
    return sum(1 << x for x in xs[:h]), sum(1 << x for x in xs[h:])
KID = {C: kids(C) for C in internal}
states = []
for C in internal:
    xs = [x for x in range(N) if C >> x & 1]; seen = set()
    for bits in range(1 << len(xs)): seen.add(norm(C, sum(1 << xs[i] for i in range(len(xs)) if bits >> i & 1)))
    states += sorted(seen)
leaves = [norm(1 << x, 0) for x in range(N)]
goal = sorted(set(norm(nodes[0], sum(1 << x for x in range(N) if bin(y & x).count("1") & 1)) for y in range(N)))
others = [s for s in states if s not in goal]
def underivable(sub):
    have = set(leaves); todo = set(sub); progress = True
    while todo and progress:
        progress = False
        for st in list(todo):
            C, S = st; ok = False
            C1, C2 = KID[C]
            for a in (S & C1, C1 & ~S):
                for b in (S & C2, C2 & ~S):
                    if norm(C1, a) in have and norm(C2, b) in have and norm(C, a | b) == st: ok = True
            if not ok:
                for Cp in nodes:
                    if Cp & ~C == 0 and Cp != C:
                        t = norm(C, S ^ Cp)
                        if t != st and t in have: ok = True; break
            if not ok:
                for (PC, PS) in have:
                    if PC != C and C & ~PC == 0 and norm(C, PS) == st:
                        O = PC & ~C
                        if norm(O, PS) in have and O in nodes: ok = True; break       # un-merge
                        for (QC, QS) in have:
                            if QC == PC and (PS ^ QS) & PC in (C, PC & ~C): ok = True; break   # restrict (quotient)
                        if ok: break
            if ok: have.add(st); todo.discard(st); progress = True
    return len(todo)
rnd = random.Random(seed); best = 99
cur = rnd.sample(others, W - 8); cv = underivable(goal + cur)
for it in range(iters):
    T = 1.2 * (1 - it / iters) + 0.05
    i = rnd.randrange(len(cur)); new = rnd.choice(others)
    if new in cur: continue
    old = cur[i]; cur[i] = new; v = underivable(goal + cur)
    if v <= cv or rnd.random() < 2.718 ** ((cv - v) / T): cv = v
    else: cur[i] = old
    if cv < best: best = cv
    if cv == 0: break
print(f"W={W} seed={seed}: least number of underivable wires reached {best} after {it + 1} moves" + ("  -> a legal play with %d wires: %s" % (W, sorted(cur)) if best == 0 else ""), flush=True)
