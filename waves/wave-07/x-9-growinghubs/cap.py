#!/usr/bin/env python3
"""x-9-growinghubs/cap.py: the Parseval cap, tested exhaustively at 8 points modulo 3 and 5 (and at 4 points modulo 5, 7).
Claim (derived in x-9.md, any coefficients, any field of odd characteristic): a wire M is one gate from at most
1/(1 - 2 phi)^2 rows of H with a partner (witness) of support <= phi*N, phi < 1/2.   8 points: support <= 1 -> 1 row; <= 2 -> 4 rows.
The witness of row O through M is O - a*M for some a != 0; its support is where a*M differs from O."""
import itertools, sys
def rowsH(N): return [tuple(-1 if bin(w & x).count('1') & 1 else 1 for x in range(N)) for w in range(N)]
for N, p in ((4, 5), (4, 7), (8, 3), (8, 5)):
    R = [tuple(v % p for v in r) for r in rowsH(N)]
    best = [0] * (N + 1); arg = [None] * (N + 1)
    for M in itertools.product(range(p), repeat=N):
        if not any(M): continue
        mins = []
        for O in R:
            m = N
            for al in range(1, p):
                d = 0
                for i in range(N):
                    if (al * M[i] - O[i]) % p: d += 1
                if d < m: m = d
            mins.append(m)
        for s in range(N + 1):
            c = sum(1 for m in mins if m <= s)
            if c > best[s]: best[s] = c; arg[s] = M
    print('N=%d modulo %d, all %d wires M: most rows one gate away with a witness of support <= s:' % (N, p, p ** N - 1))
    for s in range(1, N // 2 + 1):
        phi = s / N; cap = 'no cap' if 2 * s >= N else '%.2f' % (1 / (1 - 2 * phi) ** 2)
        print('   s=%d: %d rows (Parseval cap %s)  e.g. M = %s' % (s, best[s], cap, [x if x <= p // 2 else x - p for x in arg[s]]))
    sys.stdout.flush()
