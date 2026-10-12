#!/usr/bin/env python3
"""g-1 ledger19.py: the ledger (s, s', rise, drop, fan-out) of the 19-gate circuit of c19.py.  Count (G).  Exact integers."""
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from ledger import Circ, report
C19 = [("g1", 1, "x0", 1, "x7"), ("g2", 1, "x1", 1, "x6"), ("g3", 1, "x2", -1, "x5"), ("g4", 1, "x3", -1, "x4"),
       ("g5", 1, "g1", -1, "g2"), ("g6", 1, "g3", 1, "g4"), ("g7", 1, "g5", -1, "g6"),
       ("g8", 1, "g7", -2, "x7"), ("g9", 1, "g7", -2, "x5"), ("g10", 1, "g8", 2, "x6"), ("g11", 1, "g9", -2, "x4"),
       ("y7", 1, "g10", 2, "g4"), ("y3", 1, "g9", 2, "x3"), ("y5", -1, "y3", 2, "g5"), ("y1", 1, "g10", 2, "g3"),
       ("y6", 1, "g11", 2, "g2"), ("y2", 1, "g8", 2, "x1"), ("y4", 1, "y2", 2, "g6"), ("y0", -1, "g11", 2, "g1")]
c = Circ(8); name = {"x%d" % i: i for i in range(8)}
for (n, a, u, b, v) in C19: name[n] = c.lin(a, name[u], b, name[v])
c.cur = [name["y%d" % j] for j in range(8)]
report("the 19-gate circuit", c, True)
