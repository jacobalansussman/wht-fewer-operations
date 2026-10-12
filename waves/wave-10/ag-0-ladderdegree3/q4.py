#!/usr/bin/env python3
"""q4.py [ag-0-ladderdegree3]  The 4-bit two-colour design of ag-0.md section 5:
bits p1 p2 q1 q2 (bits 0..3).  colour 0 forgets p1 where q1 = 0, p2 where q1 = 1.
colour 1 forgets q2 where p1 = p2 = 0, q1 elsewhere.  With one selector bit: 32 points."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from designs import pair_from_design, rule_D, good
def a0(y): return 2 if (y >> 2) & 1 else 1
def a1(y): return 8 if (y & 3) == 0 else 4
m, acts = 4, [a0, a1]
print("rule D violations, atoms:", rule_D(m, acts))
# the y graph alone as a pair on 4 bits (P1 = colour 0 classes, P2 = colour 1 classes)
N = 16
l1 = [(y & ~a0(y)) * 16 + a0(y) for y in range(N)]; l2 = [(y & ~a1(y)) * 16 + a1(y) for y in range(N)]
for d in (2, 3, 4): print("  4-bit pair (no selector): degree <= %d good %s classes %s components %s" % ((d,) + good(4, d, l1, l2)))
k, t, L1, L2 = pair_from_design(m, acts)
for d in (3, 4, 5): print("  with selector, k=%d: degree <= %d good %s classes %s components %s" % ((k, d) + good(k, d, L1, L2)))
