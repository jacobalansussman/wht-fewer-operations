# ab-5: two skeleton tests at 16 points over the two-element field (mincirc_free, exhaustive for the budget given).
# Inputs 0..7 = lower half x', 8..15 = upper half x''.  Targets: all 16 subset sums.
# Free wires = a part built in advance whose gates are counted by hand; question: can the rest be finished below Yates's 32?
import subprocess, os
here = os.path.dirname(os.path.abspath(__file__))
def vec(idx): return ' '.join('1' if i in idx else '0' for i in range(16))
def zrow(S, off): return [off + T for T in range(8) if (T & S) == T]
rows = [vec(zrow(S, 0)) for S in range(8)] + [vec(zrow(S, 0) + zrow(S, 8)) for S in range(8)]
open(os.path.join(here, 'rows_zeta4.txt'), 'w').write('\n'.join(rows) + '\n')
# lower half without the private chain of its total: 9 gates
lower9 = [zrow(1, 0), zrow(2, 0), [2, 3], zrow(3, 0), [4, 5], [4, 6], zrow(4, 0), zrow(5, 0), zrow(6, 0)]
# Yates on the upper half alone: 12 gates
upper12 = [zrow(1, 8), zrow(2, 8), [10, 11], zrow(3, 8), [12, 13], [12, 14], [14, 15], [12, 13, 14, 15], zrow(4, 8), zrow(5, 8), zrow(6, 8), zrow(7, 8)]
# the 8 sums t_j = x'_j + x''_j and Yates on them: 8 + 12 gates
tj = [[j, j + 8] for j in range(8)]
both = lambda idx: idx + [i + 8 for i in idx]
ont12 = [both(zrow(1, 0)), both(zrow(2, 0)), both([2, 3]), both(zrow(3, 0)), both([4, 5]), both([4, 6]), both([6, 7]), both([4, 5, 6, 7]),
         both(zrow(4, 0)), both(zrow(5, 0)), both(zrow(6, 0)), both(zrow(7, 0))]
def run(free, m, label, built):
    fn = os.path.join(here, 'free16_tmp.txt'); open(fn, 'w').write('\n'.join(vec(f) for f in free) + '\n')
    out = subprocess.run([os.path.join(here, 'mincirc_free'), '2', '16', str(m), os.path.join(here, 'rows_zeta4.txt'), fn], capture_output=True, text=True).stdout
    nfree = out.count('free form added'); budget = int(out.split('gate budget')[1].split()[0])
    print('%s: built in advance %d gates (%d free wires); remaining budget %d -> total %d : %s' % (label, built, nfree, budget, built + budget, 'YES' if 'YES' in out else 'NO (exhaustive)'))
for m in (0, 1, 2):
    run(lower9 + upper12, m, 'skeleton A (upper half transformed alone, lower half without the chain of its total)', 21)
for m in (0, 1, 2):
    run(lower9 + tj + ont12, m, 'skeleton B (sums t_j first, then Yates on them; lower half without the chain of its total)', 29)
# skeleton C: only the sums t_j and the lower 9 are fixed; how many more gates?  (deep search: only the first budgets)
for m in (0, 1, 2):
    run(lower9 + tj, m, 'skeleton C (lower 9 and the 8 sums t_j only)', 17)
