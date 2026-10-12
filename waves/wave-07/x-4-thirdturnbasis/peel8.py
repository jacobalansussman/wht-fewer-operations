# x-4: the necessary condition of Lemma C at 8 points (and 16 as a control), exact and exhaustive.
# Flag depth 2 with first steps m1 != m2 and beta(m1,m2) = 0 needs p, q (values +1, -1 or "other") with
#   (a) for y outside x + {0,m1,m2,m1+m2}:  p(x) = chi(y)  or  q(y) = psi(x)
#   (b) for every x:  p(x) != chi(x)  and  q(x) != psi(x)        (the right side a1 a2 d1(x) is not zero)
#   (c) p(x+m1) = 1/p(x), q(y+m2) = 1/q(y).
# This is necessary, not sufficient.
def pop(v): return bin(v).count('1')

def all_gl(k):
    N = 1 << k; out = []
    def rec(cols, span):
        if len(cols) == k: out.append(tuple(cols)); return
        for v in range(1, N):
            if v not in span: rec(cols + [v], span | {a ^ v for a in span})
    rec([], {0}); return out

def passes(k, beta, m1, m2):
    N = 1 << k
    chi = [(-1)**beta(m1, y) for y in range(N)]; psi = [(-1)**beta(x, m2) for x in range(N)]
    S = {0, m1, m2, m1 ^ m2}
    p = [None]*N; found = [0]
    def rec(x, dom):
        if found[0]: return
        if x == N:
            for y in range(N):
                ok = any((v in dom[y ^ m2]) and v != psi[y] and v != psi[y ^ m2] for v in dom[y])
                if not ok: return
            found[0] = 1; return
        if p[x] is not None: return rec(x + 1, dom)
        for v in (1, -1, 2):
            if v == chi[x] or v == chi[x ^ m1]: continue          # condition (b) for p at x and x+m1
            p[x] = v; p[x ^ m1] = v
            nd = [set(dq) for dq in dom]; ok = True
            for xx in (x, x ^ m1):
                for y in range(N):
                    if (xx ^ y) in S: continue
                    if v != chi[y]:
                        nd[y] &= {psi[xx]}
                        if not nd[y]: ok = False; break
                if not ok: break
            if ok: rec(x + 1, nd)
            p[x] = None; p[x ^ m1] = None
    rec(0, [set((1, -1, 2)) for _ in range(N)])
    return found[0]

def sweep(k, gls):
    N = 1 << k; tot = 0; good = 0; ex = None
    for g in gls:
        def gy(y, g=g):
            r = 0
            for i in range(k):
                if (y >> i) & 1: r ^= g[i]
            return r
        beta = lambda x, y: pop(x & gy(y)) & 1
        for m1 in range(1, N):
            for m2 in range(1, N):
                if m1 == m2 or beta(m1, m2) != 0: continue
                tot += 1
                if passes(k, beta, m1, m2):
                    good += 1
                    if ex is None: ex = (g, m1, m2)
    return tot, good, ex

if __name__ == '__main__':
    # control at 16 points: the known depth-2 solution has beta = pairing of Q (g swaps the bits of each pair), m1 = 0011, m2 = 1100
    g = (2, 1, 8, 4)
    def gy(y):
        r = 0
        for i in range(4):
            if (y >> i) & 1: r ^= g[i]
        return r
    beta = lambda x, y: pop(x & gy(y)) & 1
    print('control, 16 points, the labelling and first steps of the known depth-2 solution: passes =', passes(4, beta, 0b0011, 0b1100))
    print('control, 16 points, same labelling, m1 = 0001, m2 = 0100: passes =', passes(4, beta, 0b0001, 0b0100))
    tot, good, ex = sweep(3, all_gl(3))
    print('8 points: all 168 labellings x all ordered pairs m1 != m2 with beta(m1,m2) = 0: %d cases, %d pass the necessary condition ; first: %s' % (tot, good, ex))
    for k, name in ((5, '32 points'),):
        gl = [tuple(1 << i for i in range(k))]   # dot product only
        tot, good, ex = sweep(k, gl)
        print('%s, dot-product labelling only: %d cases, %d pass' % (name, tot, good))
