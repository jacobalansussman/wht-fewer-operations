# rows.py k d [p]: the matrix "all polynomials of degree at most d at all 2^k cube points" (= subset sums with only the
# inputs of size <= d kept).  One row per output address y, one column per set S of at most d bits, entry 1 if S inside y.
# A zero column is appended when the number of columns is odd (mincirc wants an even number of inputs).
import sys
from itertools import combinations
k=int(sys.argv[1]); d=int(sys.argv[2])
sets=[]
for j in range(d+1):
    for c in combinations(range(k),j):
        sets.append(sum(1<<i for i in c))
pad = len(sets)%2
for y in range(1<<k):
    row=[1 if (s & y)==s else 0 for s in sets]+[0]*pad
    print(' '.join(map(str,row)))
