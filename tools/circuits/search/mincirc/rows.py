# rows.py: print target rows for mincirc.  usage: rows.py zeta k | had k | nbr k | jmi d | mob k
import sys
def kron(A, B): return [[x * y for x in ra for y in rb] for ra in A for rb in B]
def power(M, k):
    R = [[1]]
    for _ in range(k): R = kron(R, M)
    return R
kind, k = sys.argv[1], int(sys.argv[2])
if kind == "zeta": M = power([[1, 0], [1, 1]], k)
elif kind == "mob": M = power([[1, 0], [-1, 1]], k)
elif kind == "had": M = power([[1, 1], [1, -1]], k)
elif kind == "nbr":
    N = 1 << k
    M = [[1 if bin(i ^ j).count("1") == 1 else 0 for j in range(N)] for i in range(N)]
elif kind == "jmi": M = [[0 if i == j else 1 for j in range(k)] for i in range(k)]
for r in M: print(" ".join(map(str, r)))
