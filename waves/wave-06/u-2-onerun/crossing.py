# where the general bound of chain_check.py passes N, 3N and Yates' (N/2) log2 N
from chain_check import general_bound
a = b = c = None
for k in range(4, 120):
    N = 1 << k; g = general_bound(k)
    if a is None and g >= N: a = k
    if b is None and g >= 3 * N: b = k
    if c is None and g >= N * k / 2: c = k
print("bound >= N from k =", a, "; >= 3N from k =", b, "; >= (N/2) log2 N from k =", c)
import math
print("growth of the bound per bit at k = 100:", general_bound(101) / general_bound(100))
