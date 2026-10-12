#!/usr/bin/env python3
"""n-0 quarter16.py: the cheapest way I found to turn the 56-operation program (H x / 2 at 16 points) into H x / 4,
the length-preserving transform: two kernels (40 operations), then for each of the 8 pairs (a, b)
    s = a + b ;  p = 1/2 * s ;  q = p - b        (p = (a + b)/2, q = (a - b)/2 : three operations instead of four)
Total 64.  Writes the program; check.py replays it."""
import sys
from build import unit
L = []
la, ya = unit([f"x{i}" for i in range(8)], "A_")
lb, yb = unit([f"x{i}" for i in range(8, 16)], "B_")
L += la + lb
outs = [None] * 16
for j in range(8):
    L.append((f"s{j}", "+", ya[j], yb[j]))
    L.append((f"p{j}", "*", "1/2", f"s{j}"))
    L.append((f"q{j}", "-", f"p{j}", yb[j]))
    outs[j], outs[j + 8] = f"p{j}", f"q{j}"
with open(sys.argv[1], "w") as f:
    f.write(f"# n-0 quarter16.py, H x / 4 at 16 points, {len(L)} operations\n")
    for name, op, a, b in L:
        f.write(f"{name} = {a} {op} {b}\n")
    f.write("# OUT " + " ".join(outs) + "\n")
print(f"wrote {sys.argv[1]}: {len(L)} operations")
