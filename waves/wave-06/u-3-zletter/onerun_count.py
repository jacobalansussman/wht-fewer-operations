# u-3-zletter/onerun_count.py : the interval-spacing count (u-3.md section 6).  On a chain input tree, a one-run step whose larger
# end is a row S of size m uses an interval of length >= 2^(m-1), and two such intervals for DIFFERENT rows of size m overlap in at
# most half of either, so their starts are at least 2^(m-2) apart: at most 2^(k-m+2) + 1 rows of size m can be the larger end of
# a one-run step.  In a path every row is an end of at most two steps, and the empty set is the smaller end of at most two.
# Upper bound on the number of one-run steps of a two-chain picture, against the N - 1 steps there are.
from math import comb
for k in range(3, 17):
    N = 1 << k
    ub = 2 + sum(2 * min(comb(k, m), (1 << (k - m + 2)) + 1) for m in range(2, k + 1))
    print('k', k, 'N', N, 'steps', N - 1, 'one-run steps at most', ub, 'ALL ONE-RUN IMPOSSIBLE' if ub < N - 1 else '', ' fraction at most %.3f' % min(1, ub / (N - 1)))
