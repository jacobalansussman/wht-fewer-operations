# m-cross trial 2: (a) the meter on "textbook forwards then textbook again" (the second half undoes the first, up to the factor N):
#     which kind are inverse butterflies?   (b) do difference quotients of two outputs serve anybody else?   exact integers.
import sys, itertools
src = open(sys.argv[1]).read().split("for N in (4, 8, 16, 32)")[0].replace("if len(rows) != N: return None", "pass")
exec(src)
from fractions import Fraction as F
def twice(N):
    g = textbook(N); names = {}
    # outputs of the first pass, in address order: replay names
    cur = ['x%d' % i for i in range(N)]; h = 1; c = 0
    while h < N:
        nxt = list(cur)
        for i in range(N):
            if not i & h:
                c += 1; a = 't%d' % c; c += 1; b = 't%d' % c; nxt[i] = a; nxt[i | h] = b
        cur = nxt; h *= 2
    h = 1; d = 0; g2 = []
    while h < N:
        nxt = list(cur)
        for i in range(N):
            if not i & h:
                d += 1; a = 'r%d' % d; d += 1; b = 'r%d' % d
                g2.append((a, F(1), cur[i], F(1), cur[i | h])); g2.append((b, F(1), cur[i], F(-1), cur[i | h]))
                nxt[i] = a; nxt[i | h] = b
        cur = nxt; h *= 2
    return g, g2
for N in (4, 8, 16):
    g, g2 = twice(N)
    meter('forward then forward again (second half = inverse)', g + g2, N)
    meter('  first half alone', g, N)
# (b) pieces made as (h_a - h_b)/2 : for which ordered pairs (c, d) of outputs is h_d = h_c - 2*piece or h_c + 2*piece ?
for N in (8, 16):
    H = had(N); tot = {}; 
    for a in range(N):
        for b in range(a + 1, N):
            p = [(H[a][x] - H[b][x]) // 2 for x in range(N)]
            users = 0
            for c in range(N):
                for sgn in (1, -1):
                    w = tuple(H[c][x] - 2 * sgn * p[x] for x in range(N))
                    for d in range(N):
                        if d != c and (w == tuple(H[d]) or w == tuple(-t for t in H[d])): users += 1
            tot[users] = tot.get(users, 0) + 1
    print('N=%d: half pieces made from two outputs, by number of ordered output pairs they serve as a shift partner:' % N, sorted(tot.items()))
    # quarter pieces: (p1 - p2)/2 for two half pieces on the same support
    cnt = {}
    for a in range(N):
        for z in range(1, N):
            for w in range(1, N):
                if w == z or a ^ z < a or a ^ w < a or a ^ z ^ w < a: continue
                q = [(H[a][x] - H[a ^ z][x] - H[a ^ w][x] + H[a ^ z ^ w][x]) // 4 for x in range(N)]
                users = 0
                for c in range(N):
                    for sgn in (1, -1):
                        v = [H[c][x] - 2 * sgn * q[x] for x in range(N)]
                        # is v one shift (by a half piece of an output) from an output?  count outputs at Hamming distance N/4 from v with v a sign vector
                        if all(abs(t) == 1 for t in v): users += 1
                cnt[users] = cnt.get(users, 0) + 1
    print('N=%d: quarter pieces (from four outputs), by number of (output, sign) they turn into another sign vector:' % N, sorted(cnt.items()))
# (c) the floor N - 1 + (N/2) log2 N against the records, and the tensor rule  e(A x B) = n e(A) + m e(B) + (m-1)(n-1)
rec = {2: 2, 4: 7, 8: 19, 16: 52, 32: 128, 64: 304}
for N, G in rec.items():
    k = N.bit_length() - 1
    print('N=%2d record %3d  floor N-1+(N/2)log2N = %3d  excess %2d   textbook %3d' % (N, G, N - 1 + N * k // 2, G - (N - 1 + N * k // 2), N * k))
