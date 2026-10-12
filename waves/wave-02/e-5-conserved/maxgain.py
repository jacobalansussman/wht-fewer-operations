# FLOATING POINT exploration: the most entropy a sum-reflection R = I - (2/q)J on q points can add to ANY unit vector x:
# g(x) = H(Rx) - H(x), H(p) = -sum p_j^2 log2 p_j^2.  (The gain of the gate on a whole state is at most q * max g.)
# Compare with the fresh value g(e_1) = h(q) of bits.out.  Random restarts + hill climbing.
import random, math
def H(x): return -sum(a * a * math.log2(a * a) for a in x if a * a > 1e-300)
def R(x):
    q = len(x); s = sum(x) * 2.0 / q
    return [a - s for a in x]
def unit(x):
    n = math.sqrt(sum(a * a for a in x)); return [a / n for a in x]
rnd = random.Random(1)
for q in range(3, 10):
    fresh = H(R([1.0] + [0.0] * (q - 1)))
    best = (fresh, [1.0] + [0.0] * (q - 1))
    for start in range(300):
        x = unit([rnd.gauss(0, 1) * (rnd.random() < 0.5 or 1e-3) for _ in range(q)]) if start % 2 else unit([1.0] + [rnd.gauss(0, 0.05) for _ in range(q - 1)])
        cur = H(R(x)) - H(x); step = 0.3
        for it in range(1500):
            y = unit([a + rnd.gauss(0, step) for a in x]); v = H(R(y)) - H(y)
            if v > cur: x, cur = y, v
            else: step = max(step * 0.995, 1e-6)
        if cur > best[0]: best = (cur, x)
    print("q=%d fresh gain h(q)=%.4f  best found %.4f  (q*best = %.3f bits for %d ops (O): %.4f bits/op)  at x=%s" % (q, fresh, best[0], q * best[0], 2 * q, best[0] / 2, [round(a, 3) for a in sorted(best[1], key=abs, reverse=True)]))
