# u-4-zdz: write one representative L (8 x 8) for each kind of triangular factorisation found by ldl_kinds.py, and Z itself.
import sys, itertools
sys.argv = [sys.argv[0], 'none', '3']
src = open('ldl.py').read().split("mode = sys.argv[1]")[0]
exec(src)
N = 8; kinds = {}
for rest in itertools.permutations(range(1, N)):
    p = (0,) + rest; r = ldl(p)
    if r is None: continue
    L, D = r
    key = (off(L), tuple(sorted(str(d) for d in D)), tuple(sorted({str(L[i][j]) for i in range(N) for j in range(i) if L[i][j] != 0})),
           tuple(sorted(sum(1 for j in range(i) if L[i][j] != 0) for i in range(N))))
    kinds.setdefault(key, (p, L, D))
with open('kinds8.txt', 'w') as f:
    for i, key in enumerate(sorted(kinds)):
        p, L, D = kinds[key]
        f.write('%d | off=%d D=%s order=%s | %s\n' % (i, key[0], ' '.join(str(d) for d in D), ' '.join(map(str, p)), ' '.join(str(int(x)) for row in L for x in row)))
print(open('kinds8.txt').read())
