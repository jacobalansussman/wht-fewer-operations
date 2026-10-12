import sys
sys.path.insert(0, "waves/wave-03/c-0")
import verify as V
c = V.w["g7"]; tot = 0; rows = []; neg = []
for j in range(8):
    y = V.w["y%d" % j]; d = sum(1 for a, b in zip(y, c) if a != b)
    if d > 4: neg.append(j)
    d = min(d, 8 - d); tot += d; rows.append(d)
print("centre g7 =", c, "; number of inputs where the output row differs from +-centre, for y0..y7:", rows, "; total", tot)
print("so, with the rows", neg, "negated, H_8 = (every row equal to the centre) + (a matrix with %d non-zero entries, all +-2)" % tot)
reads = {}
for (n, a, u, b, v) in V.G:
    for z in (u, v): reads[z] = reads.get(z, 0) + 1
print("fan-out of the non-output full wires:", {k: reads[k] for k in ("g7", "g8", "g9", "g10", "g11")})
