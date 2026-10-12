# Exploratory, FLOATING POINT: annealing over in-place programs at 16 points made of butterflies (2 ops) and sum-reflections on q rows
# with signs (2q ops, q in QS), total count (O) at most BUDGET, maximising the entropy potential Phi (64 = finished transform, flat matrix).
# A hit (Phi > 63.9999) is only a CANDIDATE: it must be replayed in exact arithmetic.  The run with BUDGET 64 is the control:
# a solution exists there (eight 4-point reflections), so if the control does not find it, an empty result at 62 means nothing.
import sys, random, math, time
N = 16
def phi(M):
    s = 0.0
    for row in M:
        for x in row:
            y = x * x
            if y > 1e-15: s -= y * math.log2(y)
    return s
def run_prog(prog):
    M = [[1.0 if i == j else 0.0 for j in range(N)] for i in range(N)]
    c = 1 / math.sqrt(2)
    for rows, signs in prog:
        if signs is None:
            a, b = rows; ra = M[a]; rb = M[b]
            M[a] = [(x + y) * c for x, y in zip(ra, rb)]; M[b] = [(x - y) * c for x, y in zip(ra, rb)]
        else:
            q = len(rows); t = [0.0] * N
            for r, s in zip(rows, signs):
                Mr = M[r]
                for k in range(N): t[k] += s * Mr[k]
            f = 2.0 / q
            for r, s in zip(rows, signs):
                Mr = M[r]; M[r] = [Mr[k] - f * s * t[k] for k in range(N)]
    return M
def cost(prog): return sum(2 if s is None else 2 * len(r) for r, s in prog)
def rgate(rnd, QS):
    q = rnd.choice(QS)
    rows = tuple(rnd.sample(range(N), q))
    return (rows, None) if q == 2 else (rows, tuple(rnd.choice((1, -1)) for _ in range(q)))
def anneal(seed, BUDGET, QS, seconds):
    rnd = random.Random(seed); prog = []
    while cost(prog) <= BUDGET - 8: prog.append(rgate(rnd, QS))
    cur = phi(run_prog(prog)); best = (cur, list(prog)); t0 = time.time(); it = 0
    while time.time() - t0 < seconds:
        it += 1; T = 0.6 * (1 - (time.time() - t0) / seconds) + 0.01
        new = list(prog); k = rnd.random()
        if k < 0.35 and new:
            i = rnd.randrange(len(new)); rows, signs = new[i]; rows = list(rows)
            j = rnd.randrange(len(rows)); cand = [r for r in range(N) if r not in rows]
            rows[j] = rnd.choice(cand); new[i] = (tuple(rows), signs)
        elif k < 0.5 and new:
            i = rnd.randrange(len(new)); rows, signs = new[i]
            if signs is None: continue
            s = list(signs); j = rnd.randrange(len(s)); s[j] = -s[j]; new[i] = (rows, tuple(s))
        elif k < 0.65 and len(new) > 1:
            i = rnd.randrange(len(new) - 1); new[i], new[i + 1] = new[i + 1], new[i]
        elif k < 0.8 and new:
            i = rnd.randrange(len(new)); new[i] = rgate(rnd, QS)
        elif k < 0.9:
            new.insert(rnd.randrange(len(new) + 1), rgate(rnd, QS))
        elif new:
            del new[rnd.randrange(len(new))]
        if cost(new) > BUDGET: continue
        v = phi(run_prog(new))
        if v >= cur or rnd.random() < math.exp((v - cur) / T):
            prog = new; cur = v
            if cur > best[0]: best = (cur, list(prog))
            if cur > 63.9999: break
    return best, it
if __name__ == "__main__":
    BUDGET = int(sys.argv[1]); seconds = float(sys.argv[2]); QS = [int(x) for x in sys.argv[3].split(",")]; seeds = int(sys.argv[4]); off = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    for seed in range(off, off + seeds):
        (b, prog), it = anneal(seed, BUDGET, QS, seconds)
        print("budget %d gates q in %s seed %d: best Phi %.4f of 64 at cost %d, %d gates of sizes %s, %d iterations%s"
              % (BUDGET, QS, seed, b, cost(prog), len(prog), sorted(len(r) for r, s in prog), it, "  CANDIDATE: " + repr(prog) if b > 63.9999 else ""))
        sys.stdout.flush()
