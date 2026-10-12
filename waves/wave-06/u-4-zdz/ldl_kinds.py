# u-4-zdz / ldl_kinds.py : the triangular factorisations of the 8-point transform, sorted by kind.
# For every order of the addresses with non-zero pivots:  D as a sorted list, the set of values in L, off-diagonal non-zeros of L,
# and whether L is "subset sums in disguise" (after undoing the order, L = Z composed with an address map and sign scalings is not
# tested here; what is printed is enough to see whether new values or new diagonals appear).   Exact fractions.
import sys, itertools
sys.argv = [sys.argv[0], 'none', sys.argv[1]]
src = open('ldl.py').read().split("mode = sys.argv[1]")[0]
exec(src)
K = int(sys.argv[2]); N = 1 << K
kinds = {}
for rest in itertools.permutations(range(1, N)):
    p = (0,) + rest                       # address 0 first: by the sign-scaling symmetry this loses nothing
    r = ldl(p)
    if r is None: continue
    L, D = r
    key = (off(L), tuple(sorted(str(d) for d in D)), tuple(sorted({str(L[i][j]) for i in range(N) for j in range(i) if L[i][j] != 0})),
           tuple(sorted(sum(1 for j in range(i) if L[i][j] != 0) for i in range(N))))
    kinds.setdefault(key, []).append(p)
print('N=%d, orders starting with address 0 that factor: %d;  kinds: %d' % (N, sum(len(v) for v in kinds.values()), len(kinds)))
for key in sorted(kinds):
    print('off(L)=%d  D=%s  values of L=%s  non-zeros per row=%s   orders: %d   e.g. %s' % (key[0], key[1], key[2], key[3], len(kinds[key]), kinds[key][0]))
    L, D = ldl(kinds[key][0])
    for row in L: print('      ', ' '.join('%5s' % str(x) for x in row))
