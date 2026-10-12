# d-6-excess, third run: does excess follow the determinant?  5 sign rows on 5 inputs.
# Zero excess <=> |det| = 16 = 2^(n-1) (more.py).  Here: exact minimum gate count (engine of i-play/n4.py, helper ratios
# restricted as there) for representatives with |det| = 32 and |det| = 48.   usage: det5.py <32|48> <how many representatives>
import sys, itertools
from fractions import Fraction
sys.path.insert(0, "waves/wave-01/i-play")
import n4
def det(M):
    M = [[Fraction(x) for x in r] for r in M]; n = len(M); d = Fraction(1)
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None: return 0
        if p != c: M[c], M[p] = M[p], M[c]; d = -d
        d *= M[c][c]
        for r in range(c+1, n):
            f = M[r][c] / M[c][c]
            for k in range(c, n): M[r][k] -= f * M[c][k]
    return int(d)
want = int(sys.argv[1]); howmany = int(sys.argv[2])
pats = [(1,) + p for p in itertools.product((1, -1), repeat=4)]
reps = [rows for rows in itertools.combinations(pats, 5) if abs(det(rows)) == want]
step = max(1, len(reps) // howmany)
for rows in reps[::step][:howmany]:
    n4.H4 = list(rows)
    best = None
    for depth in (8, 9, 10, 11):
        sols, targets = n4.search(5, [0, 1, 2, 3, 4], depth, False)
        if sols:
            best = depth
            s = next(iter(sols))
            helpers = sorted(s - targets)
            break
    print("|det| %d rows %s : min gates %s, excess %s, helpers %s" % (want, rows, best, None if best is None else best - 8, helpers if best else "-"), flush=True)
