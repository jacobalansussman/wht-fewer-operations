# grid.py: rows of the 2-D prefix-sum matrix on an a x b array (zeta transform of a product of two chains),
# padded with unused inputs to n columns.  usage: grid.py a b n
import sys
a, b, n = map(int, sys.argv[1:4])
for i in range(a):
    for j in range(b):
        row = [1 if (i2 <= i and j2 <= j) else 0 for i2 in range(a) for j2 in range(b)] + [0] * (n - a * b)
        print(" ".join(map(str, row)))
