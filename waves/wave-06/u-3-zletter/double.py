# u-3-zletter/double.py : from an input tree at N points (internal node masks) make an input tree at 2N points.
# mode A: split the root by the new top address bit, a copy of the tree in each half.
# mode B: every leaf T becomes the pair {T, T + new bit}, the old tree on the pairs.
# Usage: python3 -B double.py K A|B infile > outfile      (infile: a zmst output or a line of masks)
import sys
K = int(sys.argv[1]); N = 1 << K; mode = sys.argv[2]
lines = [l for l in open(sys.argv[3]).read().splitlines() if l.strip() and not l.startswith('K') and not l.startswith('row')]
masks = [int(x) for x in lines[0].split()]
assert len(masks) == N - 1
if mode == 'A':
    out = [(1 << (2 * N)) - 1] + masks + [m << N for m in masks]
else:
    out = [m | (m << N) for m in masks] + [(1 << t) | (1 << (t + N)) for t in range(N)]
assert len(out) == 2 * N - 1
print(*out)
