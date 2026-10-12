# ab-5: skeleton E, the direct analogue of the 8-point tying circuit.  Two-element field, exhaustive for each budget.
# Fixed in advance: the lower half without the private chain of its total; the sums t_j = x'_j + x''_j for every j but the
# last; Yates on the t_j for every output but the grand total.  Open: the lower total and the grand total, that is the two
# private chains (2 + 3 = 5 gates at 8 points, 3 + 4 = 7 gates at 16 points by the textbook).
import subprocess, os, sys, time
here = os.path.dirname(os.path.abspath(__file__))
def run(n, h, free, m, label, built, tag):
    vec = lambda idx: ' '.join('1' if i in idx else '0' for i in range(n))
    fn = os.path.join(here, 'freeE_%s.txt' % tag); open(fn, 'w').write('\n'.join(vec(f) for f in free) + '\n')
    rows = os.path.join(here, 'rows_zeta%d.txt' % {8: 3, 16: 4}[n])
    t0 = time.time()
    out = subprocess.run([os.path.join(here, 'mincirc_free'), '2', str(n), str(m), rows, fn], capture_output=True, text=True).stdout
    budget = int(out.split('gate budget')[1].split()[0])
    print('%s: fixed %d gates; open budget %d -> total %d : %s  (%.0f s)' % (label, built, budget, built + budget, 'YES' if 'YES' in out else 'NO (exhaustive)', time.time() - t0), flush=True)
    if 'YES' in out: print(out[out.index('RESULT'):], flush=True)
if sys.argv[1] == '8':
    # lower = inputs 0..3, upper = 4..7
    z = lambda S, off: [off + T for T in range(4) if (T & S) == T]
    both = lambda idx: idx + [i + 4 for i in idx]
    free = [z(1, 0), z(2, 0)] + [[j, j + 4] for j in range(3)] + [both(z(1, 0)), both(z(2, 0))]
    for m in (2, 3): run(8, 4, free, m, 'E at 8 points', 7, 'E8')
else:
    z = lambda S, off: [off + T for T in range(8) if (T & S) == T]
    both = lambda idx: idx + [i + 8 for i in idx]
    lower9 = [z(1, 0), z(2, 0), [2, 3], z(3, 0), [4, 5], [4, 6], z(4, 0), z(5, 0), z(6, 0)]
    free = lower9 + [[j, j + 8] for j in range(7)] + [both(f) for f in lower9]
    for m in (3, 4): run(16, 8, free, m, 'E at 16 points', 25, 'E16')
