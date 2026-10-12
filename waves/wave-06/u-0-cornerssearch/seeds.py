# u-0: the nine doublings of a picture (rows x cols: copy-copy, copy-reversed copy, twins); writes seed files and prints corner counts.
import sys, ast
txt = open(sys.argv[1]).read().split('BEST')[-1]
rows = ast.literal_eval(txt.split('rows ')[1].split(' r ')[0]); cols = ast.literal_eval(txt.split('cols ')[1].split(' c ')[0])
N = len(rows)
def dbl(o, how, lowfirst):
    lo = list(o); hi = [x + N for x in o]
    if how == 'cc': return lo + hi if lowfirst else hi + lo
    if how == 'cr': return lo + hi[::-1] if lowfirst else hi + lo[::-1]
    return [y for x in o for y in ((x, x + N) if lowfirst else (x + N, x))]
def corners(r, c):
    n = len(r); A = [[1 if (r[a] & c[b]) == c[b] else 0 for b in range(n)] + [0] for a in range(n)] + [[0] * (n + 1)]
    return sum(1 for a in range(n) for b in range(n) if A[a][b] - A[a+1][b] - A[a][b+1] + A[a+1][b+1])
out = []
for hr in ('cc', 'cr', 'tw'):
    for hc in ('cc', 'cr', 'tw'):
        for lr in (True, False):
            for lc in (True, False):
                r = dbl(rows, hr, lr); c = dbl(cols, hc, lc); v = corners(r, c); out.append((v, hr, hc, lr, lc, r, c))
out.sort(key=lambda t: t[0])
for v, hr, hc, lr, lc, r, c in out: print(f" rows {hr} (old half first: {lr})  cols {hc} (old half first: {lc}): corners {v}")
v, hr, hc, lr, lc, r, c = out[0]
open(sys.argv[2], 'w').write(' '.join(map(str, r)) + '\n' + ' '.join(map(str, c)) + '\n')
print("best seed written:", v, "= ", v / len(r), "per point; three times the old count would be", 3 * corners(rows, cols))
