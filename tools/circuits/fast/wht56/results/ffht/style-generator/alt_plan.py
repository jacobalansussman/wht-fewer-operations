#!/usr/bin/env python3
"""alt_plan.py -- FFHT's shipped plan with 7 sizes changed: on stdout, in the hall-of-fame format.

    python3 -B alt_plan.py ../FFHT/hall_of_fame_avx.txt > gen/alt_plan.txt

A transform of 2^k floats has k - 3 levels between registers (k - 2 for doubles), so at most
floor((k - 3) / 3) passes can take 8 registers through 3 levels (floor((k - 2) / 3) for
doubles).  FFHT's shipped plan has one such pass fewer than that at 7 sizes, because it has two
short passes there (one at the top of the base block and one at the top of the recursion):
floats 2^13, 2^15, 2^22 and doubles 2^14, 2^20, 2^21, 2^24.  This plan gives those 7 sizes the
base block that FFHT itself uses most often for its neighbours (2^12 floats, 2^11 doubles: 16 KiB),
which brings the number of 8-register passes to the largest possible.  Every other size is as
shipped.  The times in the file are FFHT's and mean nothing for the changed lines.
"""
import re
import sys

CHANGE = {('float', 13): 12, ('float', 15): 12, ('float', 22): 12,
          ('double', 14): 11, ('double', 20): 11, ('double', 21): 11, ('double', 24): 11}

for raw in open(sys.argv[1]):
    m = re.match(r'type_name = (\w+); log_n = (\d+); (best_time = \S+); best_desc = (.+)$', raw.strip())
    key = (m.group(1), int(m.group(2)))
    desc = m.group(4)
    if key in CHANGE:
        desc = 'greedy_merged_recursive %d' % CHANGE[key]
    sys.stdout.write('type_name = %s; log_n = %d; %s; best_desc = %s\n' % (key[0], key[1], m.group(3), desc))
