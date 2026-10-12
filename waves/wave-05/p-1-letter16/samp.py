# p-1-letter16: random sign designs, exact-cover tiling count by the float solver (fixed signs: a pure 0/1 cover, fast).
# usage: samp.py <design> <family: quad|cubic|pw2|any> <seconds> <seed>
import sys, time, random, json
from rfix import solve
from rf import D
name, fam, T, seed = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4]); random.seed(seed)
N = D[name][0]; k = N.bit_length() - 1
def bit(x, i): return x >> i & 1
def rnd_poly(deg):
    mons = [m for m in range(1, N) if bin(m).count('1') <= deg]; ch = [m for m in mons if random.random() < 0.5]
    return [(-1) ** (sum(1 for m in ch if (x & m) == m) & 1) for x in range(N)]
def rnd_sparsequad():        # few quadratic terms plus a random linear part
    mons = [m for m in range(1, N) if bin(m).count('1') == 2]; ch = random.sample(mons, random.choice([1, 1, 2, 2, 3])) + [m for m in range(1, N) if bin(m).count('1') == 1 and random.random() < 0.5]
    return [(-1) ** (sum(1 for m in ch if (x & m) == m) & 1) for x in range(N)]
hist = {}; best = None; t0 = time.time(); cnt = 0
while time.time() - t0 < T:
    if fam == 'quad': r, c = (rnd_poly(2), rnd_poly(2)) if random.random() < 0.5 else (rnd_sparsequad(), rnd_sparsequad())
    elif fam == 'cubic': r, c = rnd_poly(3), rnd_poly(3)
    else: r, c = [random.choice([1, -1]) for _ in range(N)], [random.choice([1, -1]) for _ in range(N)]
    b, st, lst = solve(name, 'tile', 20, 4, fam, r, c, quiet=True); cnt += 1
    if b is None or st != 0: hist['unsolved'] = hist.get('unsolved', 0) + 1; continue
    hist[b] = hist.get(b, 0) + 1
    if best is None or b < best[0]:
        best = (b, r, c, lst); print("new best tau", b, "after", cnt, "designs, %.0f s" % (time.time() - t0), " r", r, " c", c); sys.stdout.flush()
print("design", name, "family", fam, "designs", cnt, "histogram of tau (exact-cover model):", sorted(hist.items(), key=lambda t: str(t[0])))
if best: print("JSON", json.dumps({'design': name, 'tag': 'sample ' + fam + ' tile', 'N': N, 'r': best[1], 'c': best[2], 'rects': best[3], 'rown': [list(s) for s in D[name][1]], 'coln': [list(s) for s in D[name][2]]}))
