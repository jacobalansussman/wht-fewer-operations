# s-note/check.py : my own recount for WAVE6-NOTE.md. Whole numbers only.
# Corner count of the subset-sum picture: rows = outputs S in a given order, columns = inputs T in a given order,
# entry 1 if T is inside S; a zero row and a zero column are added at the end.
# corners = number of places (i, j) where (row i - row i+1) changes value between column j and column j+1.
# The two-chain program costs N - 2 + corners gates (G).
import re, sys, math
D = 'waves/wave-06/u-0-cornerssearch/'
def corners(rows, cols):
    N = len(rows)
    M = [[1 if (t & s) == t else 0 for t in cols] + [0] for s in rows] + [[0] * (N + 1)]
    c = 0
    for i in range(N):
        d = [M[i][j] - M[i + 1][j] for j in range(N + 1)]
        c += sum(1 for j in range(N) if d[j] != d[j + 1])
    return c
def runs_and_shape(rows, cols):
    # per step: is the step nested (one set inside the other), number of non-zero runs
    N = len(rows); out = []
    ext = list(rows) + [None]
    for i in range(N):
        a = ext[i]; b = ext[i + 1]
        da = [1 if (t & a) == t else 0 for t in cols]
        db = [0] * N if b is None else [1 if (t & b) == t else 0 for t in cols]
        d = [x - y for x, y in zip(da, db)]
        r = 0; prev = 0
        for v in d:
            if v != 0 and v != prev: r += 1
            prev = v
        nested = (b is None) or (a & b) in (a, b)
        out.append((nested, r))
    return out
def read(fn):
    s = open(D + fn).read()
    r = re.search(r'rows \[([0-9, ]+)\]', s); c = re.search(r'cols \[([0-9, ]+)\]', s)
    return [int(x) for x in r.group(1).split(',')], [int(x) for x in c.group(1).split(',')]
print('file            N  corners  per point  gates N-2+c  Yates  nested steps  one-run steps  most runs')
for fn in ['a8.out', 'a16.out', 'r32.out', 'r64_first.out', 't128.out']:
    rows, cols = read(fn); N = len(rows)
    assert sorted(rows) == list(range(N)) and sorted(cols) == list(range(N))
    c = corners(rows, cols); k = N.bit_length() - 1
    sh = runs_and_shape(rows, cols)
    print('%-14s %4d %7d %9.3f %11d %7d %8d/%d %10d/%d %8d' % (fn, N, c, c / N, N - 2 + c, N * k // 2,
          sum(1 for n, r in sh if n), N, sum(1 for n, r in sh if r == 1), N, max(r for n, r in sh)))
print()
print('Gray order on both sides (reflected Gray code on outputs, the same on inputs, best of the four reversals):')
for k in range(2, 10):
    N = 1 << k
    g = [i ^ (i >> 1) for i in range(N)]
    best = min(corners(a, b) for a in (g, g[::-1]) for b in (g, g[::-1]))
    print('  N=%4d corners %6d   7*3^(k-2)+2 = %6d   per point %.2f' % (N, best, 7 * 3 ** (k - 2) + 2, best / N))
print()
print('u-2 displayed bound (5/2)^k / (400 (1 + ln N)): first k where it passes N, 3N, Yates (N/2) k; and the one-flag floor')
def b(k): return 2.5 ** k / (400 * (1 + k * math.log(2)))
for name, f in (('N', lambda k: 2.0 ** k), ('3N', lambda k: 3 * 2.0 ** k), ('Yates', lambda k: 2.0 ** k * k / 2)):
    k = 1
    while b(k) <= f(k): k += 1
    print('  passes %-5s at k = %d' % (name, k))
print('  one-flag floor N - 1 + (N/2) log2 N at 2..64 points:', [(1 << k) - 1 + (1 << k) * k // 2 for k in range(1, 7)],
      ' records 7, 19, 52, 128, 304; textbook', [(1 << k) * k for k in range(1, 7)])
