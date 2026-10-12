# x-3 boxrelations: the telescoping bound for the family of ADDRESS MAPS (boxes = permutation matrices x -> g x, g an invertible bit matrix).
# For two maps the bound is rank(P (x) P - P' (x) P') / rank(P - P'), and with h = g' g^-1 this is (K^2 - cycles of h x h) / (K - cycles of h).
# Exact (cycle counting). Printed: the largest value over all h != 1, and which h reaches it.
import itertools, sys
def cyc(perm):
    seen = [False]*len(perm); c = 0
    for i in range(len(perm)):
        if not seen[i]:
            c += 1; j = i
            while not seen[j]: seen[j] = True; j = perm[j]
    return c
for k in (2, 3, 4):
    K = 1 << k; best = (0, None); vals = {}
    for cols in itertools.product(range(1, K), repeat=k):
        img = []
        for x in range(K):
            y = 0
            for b in range(k):
                if x >> b & 1: y ^= cols[b]
            img.append(y)
        if len(set(img)) != K or img == list(range(K)): continue
        c1 = cyc(img); c2 = cyc([img[x]*K + img[y] for x in range(K) for y in range(K)])
        num, den = K*K - c2, K - c1
        fixed = sum(img[x] == x for x in range(K))
        vals[(den, num, fixed)] = vals.get((den, num, fixed), 0) + 1
    top = max(vals, key=lambda t: t[1]/t[0])
    print('K = %2d: %5d address maps other than the identity; largest bound = %d/%d = %.3f calls (K + K/2 = %.1f; textbook 2K = %d); reached by maps with %d fixed addresses'
          % (K, sum(vals.values()), top[1], top[0], top[1]/top[0], 1.5*K, 2*K, top[2]))
    for (den, num, fixed), n in sorted(vals.items()): print('     rank(P-1) = %2d, rank(P(x)P-1) = %3d, fixed addresses %2d: bound %.3f  (%d maps)' % (den, num, fixed, num/den, n))
