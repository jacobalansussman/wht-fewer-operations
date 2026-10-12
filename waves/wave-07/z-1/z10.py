# z10.py [z-1]: the same rigorous enclosures as zexact.py, at the README's scale 10^10, in a narrow window around the published figures
import sys, json, gzip
from fractions import Fraction as Fr
import zexact as Z
C = "not-in-this-repository/wht-power-saving-r4-candidate/tools/certificate/"
for f, lo0, hi0 in (("gcert1-e8-r783.json.gz", 8762400, 8762600), ("gcert1-p11-pr193.json.gz", 7474500, 7474600)):
    d = json.load(gzip.open(C + f)); h, v, R = d["h"], d["v"], d["R"]; m, W = 5 * h, 4 * v + R
    B = Z.unit_blocks(h, v, d["blocks"], "xysc")
    for S in (13, None):
        lo, hi = lo0, hi0
        assert Z.fact(B, m, W, Fr(lo, 10 ** 10), S) is True and Z.fact(B, m, W, Fr(hi, 10 ** 10), S) is False
        while hi - lo > 1:
            mid = (lo + hi) // 2; t = Z.fact(B, m, W, Fr(mid, 10 ** 10), S); assert t is not None
            if t: lo = mid
            else: hi = mid
        print("%s  fill %s : whole-block inequality PROVED at %d/10^10 and PROVED FALSE at %d/10^10" % (f, "2^13" if S else "-> infinity", lo, hi), flush=True)
