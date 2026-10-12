# Exploratory, FLOATING POINT (not exact): how fast can the entropy potential rise per count-(O) operation at 16 points?
# State: an orthogonal 16x16 matrix M (the program so far, in place), M = I at the start.  Potential: Phi = -sum M_ij^2 log2 M_ij^2;
# the finished transform (all entries +-1/4) has Phi = 64 = N log2 N, the maximum.
# Gates: butterfly on 2 rows ((u,v) -> (u+v, u-v)/sqrt2), 2 operations; sum-reflection on q rows with signs, I - (2/q) v v^T, 2q operations.
# Greedy: at each step take, among `samples` random gates, the one with the most bits per operation.  Several restarts.
import sys, random, math
N = 16
def ent_rows(M, rows):
    s = 0.0
    for r in rows:
        for x in M[r]:
            y = x * x
            if y > 1e-15: s -= y * math.log2(y)
    return s
def apply(M, rows, signs):
    q = len(rows)
    if q == 2 and signs is None:
        a, b = rows; c = 1 / math.sqrt(2)
        ra = [(x + y) * c for x, y in zip(M[a], M[b])]; rb = [(x - y) * c for x, y in zip(M[a], M[b])]
        return {a: ra, b: rb}
    t = [sum(s * M[r][c] for r, s in zip(rows, signs)) for c in range(N)]
    return {r: [M[r][c] - (2.0 / q) * s * t[c] for c in range(N)] for r, s in zip(rows, signs)}
def run(seed, samples, qmax):
    rnd = random.Random(seed); M = [[1.0 if i == j else 0.0 for j in range(N)] for i in range(N)]
    ops = 0; phi = 0.0; trace = []
    while ops < 80 and phi < 63.999:
        best = None
        for _ in range(samples):
            q = rnd.randint(2, qmax); rows = rnd.sample(range(N), q)
            signs = None if (q == 2) else [rnd.choice((1, -1)) for _ in range(q)]
            if q == 2 and rnd.random() < 0.5: signs = None
            elif q == 2: continue
            new = apply(M, rows, signs)
            old = ent_rows(M, rows); M2 = {r: new[r] for r in rows}
            gain = -sum(y * y * math.log2(y * y) for r in rows for y in M2[r] if y * y > 1e-15) - old
            cost = 2 if q == 2 else 2 * q
            if best is None or gain / cost > best[0]: best = (gain / cost, gain, cost, rows, signs, new)
        if best is None or best[1] <= 1e-9: break
        for r, row in best[5].items(): M[r] = row
        ops += best[2]; phi += best[1]; trace.append((best[2], round(best[1], 3)))
    return ops, phi, trace
for qmax in (4, 6, 8):
    for seed in range(3):
        ops, phi, trace = run(seed, int(sys.argv[1]), qmax)
        # bits reached at the first moment ops >= 32, 48, 56, 64
        acc = 0; b = 0.0; marks = {}
        for c, g in trace:
            acc += c; b += g
            for m in (16, 32, 48, 56, 64, 72, 80):
                if acc <= m: marks[m] = round(b, 2)
        print("qmax=%d seed=%d: bits after at most 16/32/48/56/64/72/80 ops: %s ; gates (ops, bits): %s" % (qmax, seed, [marks.get(m) for m in (16, 32, 48, 56, 64, 72, 80)], trace[:14]))
        sys.stdout.flush()
