# x-5-weightedz / pairid.py : the potential, pair by pair. Exact integers.
# Coupling a string of length a+1 with one of length b+1: weight block w has m_w = min(w, a, b, a+b-w) + 1 vectors.
# Claim: sum over w of m_w (m_w - 1) = sum of f(d) for d = |a-b|, |a-b|+2, ..., a+b  -  (b+1) f(a)  -  (a+1) f(b),
#        f(d) = (d+1) d (d-1) / 3.
f = lambda d: (d + 1) * d * (d - 1) // 3
bad = 0; n = 0
for a in range(0, 81):
    for b in range(0, 81):
        price = sum((min(w, a, b, a + b - w) + 1) * min(w, a, b, a + b - w) for w in range(a + b + 1))
        pot = sum(f(d) for d in range(abs(a - b), a + b + 1, 2)) - (b + 1) * f(a) - (a + 1) * f(b)
        n += 1
        if price != pot: bad += 1
print("pairs (a, b) with 0 <= a, b <= 80: %d checked, %d failures" % (n, bad))
