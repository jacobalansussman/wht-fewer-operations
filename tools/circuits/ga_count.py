#!/usr/bin/env python3
"""ga_count.py -- the count stated by Grigoryan and Agaian (2000) beside the count of their algorithm.

usage: python3 -B tools/circuits/ga_count.py

Standard library only.  It takes less than a second.

A. M. Grigoryan and S. S. Agaian, "Split manageable efficient algorithm for Fourier and Hadamard
transforms", IEEE Transactions on Signal Processing 48(1), 2000, pages 172 to 183, state on page 181 that
their algorithm computes the Hadamard transform on N = 2^r points with

    6 * 2^r - r^2 - 3r - 6

additions and subtractions.  The algorithm (pages 179 to 181) applies a "paired transform" of length N,
which costs 2N - 2 additions and subtractions and splits the N-point transform into transforms of lengths
N/2, N/4, ..., 2, 1; these are computed the same way.  So the number of additions and subtractions that the
algorithm performs follows the recursion

    T(N) = (2N - 2) + T(N/2) + T(N/4) + ... + T(1),    T(1) = 0.

The paper does not print this recursion; it is written down here from the description of the algorithm.
This program prints, for N = 2 to 16,384: the stated count, T(N), N log2 N and (N/2) log2 N.  The last is
a lower bound for circuits of additions and subtractions, by the determinant argument of Morgenstern (1973)
as Alman and Rao (2023) quote it; the introduction of the paper gives 0.5 N log N as a lower bound for the
Hadamard transform (page 172).

What it shows: T(N) = N log2 N at every size; the stated count equals it at 2, 4 and 8 points and is
smaller from 16 points on; from 4,096 points on the stated count is below (N/2) log2 N.  So the stated
count is too small, and the algorithm has the textbook count.

The last line is "OK ..." with exit code 0, or "FAILED ..." with exit code 1.  This is arithmetic on two
formulas, not a run of the algorithm and not a proof."""
import sys
sys.dont_write_bytecode = True
from functools import lru_cache


@lru_cache(None)
def T(r):
    """Additions and subtractions for 2^r points: one paired transform, then the smaller transforms."""
    if r == 0:
        return 0
    return 2 * 2 ** r - 2 + sum(T(j) for j in range(r))


def main():
    if len(sys.argv) != 1:
        sys.exit(__doc__)
    print(' r  points  stated count  recursion T(N)   N log2 N  (N/2) log2 N')
    first_below_textbook = first_below_bound = None
    ok = True
    for r in range(1, 15):
        N = 2 ** r
        stated = 6 * N - r * r - 3 * r - 6
        ok = ok and T(r) == N * r
        if stated < N * r and first_below_textbook is None:
            first_below_textbook = N
        if 2 * stated < N * r and first_below_bound is None:
            first_below_bound = N
        print('%2d %7d %13d %15d %10d %13d%s' % (
            r, N, stated, T(r), N * r, N * r // 2,
            '   the stated count is below (N/2) log2 N' if 2 * stated < N * r else ''))
    print()
    if not ok or first_below_textbook != 16 or first_below_bound != 4096:
        print('FAILED: expected T(N) = N log2 N at every size, the stated count below it first at 16 points '
              'and below (N/2) log2 N first at 4096 points; found %s, %s, %s' % (ok, first_below_textbook, first_below_bound))
        sys.exit(1)
    print('OK: the recursion gives N log2 N at every size from 2 to 16384 points; the stated count is below it '
          'from 16 points on and below (N/2) log2 N from 4096 points on.  Arithmetic on two formulas, not a proof.')


if __name__ == '__main__':
    main()
