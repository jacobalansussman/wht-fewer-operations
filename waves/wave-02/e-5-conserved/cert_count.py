# Count the array-level additions in the E8 certificate (read only), to size where count (O) first dips for the published unit.
import json, gzip, sys
d = json.load(gzip.open(sys.argv[1]))
def terms(lst):
    n = 0; halves = 0
    for st in lst:
        for part in st[3:]:
            for t in part:
                n += 1
                if len(t) >= 3 and t[2] != 1: halves += 1
    return n, halves
a = terms(d['A']); b = terms(d['B'])
sc = sum(len(row) for row in d['scat']['table'])
print("h=%d v=%d R=%d cst=%d moves in one pass N=%d" % (d['h'], d['v'], d['R'], d['cst'], d['N']))
print("A: %d steps, %d terms (%d with a coefficient field != 1)" % (len(d['A']), a[0], a[1]))
print("B: %d steps, %d terms (%d with a coefficient field != 1)" % (len(d['B']), b[0], b[1]))
print("scatter: %d terms ; ret: %d" % (sc, len(d['ret'])))
per_inv = a[0] + b[0] + sc
W = 4 * d['v'] + d['R']; m = 5 * d['h']; D = 4 * d['v'] - 5 * d['cst']
print("array additions per invocation (terms): about %d ; five invocations: about %d ; W=%d m=%d D=%d ; W*m=%d" % (per_inv, 5 * per_inv, W, m, D, W * m))
for c in (1.0, 2.5):
    f = 5 * per_inv / (c * D)
    print("  if one move costs c=%.1f operations per point and column: first dip at f > %.0f columns, array length 2^(%d*f) = 2^%d points" % (c, f, m, int(m * (int(f) + 1))))
