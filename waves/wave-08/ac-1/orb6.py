#!/usr/bin/env python3
"""orb6.py [ac-1] EXACT.  Part A of check.py at K = 64 only (orbits of GL(6,2) on 1-, 2-, 3-tuples by union-find)."""
import sys
sys.argv = [sys.argv[0]]
src = open(__file__.replace("orb6.py", "check.py")).read().split("# ---------------- exact linear algebra")[0]
src = src.replace("for k in range(2, kmax + 1):", "for k in (6,):")
exec(src)
