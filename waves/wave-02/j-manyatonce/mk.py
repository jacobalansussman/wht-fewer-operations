#!/usr/bin/env python3
"""mk.py : write target files for ds.c.
   mk.py h <k> <copies>      -> copies of the 2^k-point Walsh-Hadamard matrix (direct sum)
   mk.py mat <copies> <rows separated by /, entries by ,>   -> copies of any matrix
"""
import sys

def had(k):
    N = 1 << k
    return [[(-1) ** bin(i & j).count("1") for j in range(N)] for i in range(N)]

def dsum(A, m):
    r, c = len(A), len(A[0])
    out = []
    for b in range(m):
        for row in A:
            out.append([0] * (c * b) + list(row) + [0] * (c * (m - 1 - b)))
    return out

if sys.argv[1] == "h":
    A = had(int(sys.argv[2])); m = int(sys.argv[3])
else:
    m = int(sys.argv[2]); A = [[int(x) for x in r.split(",")] for r in sys.argv[3].split("/")]
B = dsum(A, m)
print(len(B))
for row in B:
    print(" ".join(str(x) for x in row))
