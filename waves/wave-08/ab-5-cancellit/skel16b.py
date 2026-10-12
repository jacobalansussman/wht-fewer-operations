# ab-5: two more skeletons at 16 points (two-element field), each leaving the totals open.  See skel16.py for conventions.
import subprocess, os, sys, time
here = os.path.dirname(os.path.abspath(__file__))
def vec(idx): return ' '.join('1' if i in idx else '0' for i in range(16))
def zrow(S, off): return [off + T for T in range(8) if (T & S) == T]
lower9 = [zrow(1, 0), zrow(2, 0), [2, 3], zrow(3, 0), [4, 5], [4, 6], zrow(4, 0), zrow(5, 0), zrow(6, 0)]
upper9 = [[i + 8 for i in f] for f in lower9]
tj = [[j, j + 8] for j in range(8)]
both = lambda idx: idx + [i + 8 for i in idx]
ont9 = [both(f) for f in lower9]
def run(free, m, label, built, tag):
    fn = os.path.join(here, 'free16_%s.txt' % tag); open(fn, 'w').write('\n'.join(vec(f) for f in free) + '\n')
    t0 = time.time()
    out = subprocess.run([os.path.join(here, 'mincirc_free'), '2', '16', str(m), os.path.join(here, 'rows_zeta4.txt'), fn], capture_output=True, text=True).stdout
    budget = int(out.split('gate budget')[1].split()[0])
    print('%s: built in advance %d gates; remaining budget %d -> total %d : %s   (%.0f s)' % (label, built, budget, built + budget, 'YES' if 'YES' in out else 'NO (exhaustive)', time.time() - t0), flush=True)
    if 'YES' in out: print(out[out.index('RESULT'):], flush=True)
which = sys.argv[1]
if which == 'D1':
    for m in (2, 3, 4):
        run(lower9 + tj + ont9, m, 'skeleton D1 (lower 9, sums t_j, Yates on t without the chain of the grand total)', 26, 'D1')
if which == 'D2':
    for m in (3, 4):
        run(lower9 + upper9, m, 'skeleton D2 (lower 9 and upper 9: both halves without the chains of their totals)', 18, 'D2')
