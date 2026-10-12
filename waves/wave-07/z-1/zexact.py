#!/usr/bin/env python3
"""zexact.py [z-1]  The engine's block-sum law, recomputed with RIGOROUS rational enclosures (no floats).
Every logarithm and exponential is enclosed between two fractions (series with an explicit remainder, outward rounding to
2^-PREC), so each printed verdict "holds"/"fails" is a proved inequality about the block list, not a float comparison.
Block lists: built from the published certificates exactly as R/tools/whatif_copies.py builds them (read only)."""
import sys, json, gzip
from fractions import Fraction as Fr
PREC = 220
ONE = 1 << PREC
def dn(x):  # floor to a multiple of 2^-PREC
    return Fr((x.numerator * ONE) // x.denominator, ONE)
def up(x):
    return Fr(-((-x.numerator * ONE) // x.denominator), ONE)
_ln = {}
def ln_int(n):
    """(lo, hi) enclosing ln n, n a positive integer"""
    if n in _ln: return _ln[n]
    if n == 1: _ln[n] = (Fr(0), Fr(0)); return _ln[n]
    if n == 2:
        y = Fr(1, 3)
    else:
        k = n.bit_length() - 1
        if n == 1 << k:
            lo, hi = ln_int(2); _ln[n] = (k * lo, k * hi); return _ln[n]
        y = Fr(n - (1 << k), n + (1 << k))          # ln(n / 2^k) = 2 atanh(y), 0 < y < 1/3
    s = Fr(0); p = y; y2 = y * y; J = 90
    for j in range(J + 1):
        s += p / (2 * j + 1); p = dn(p * y2) if False else p * y2
        if j % 8 == 7: s = dn(s) ; p = up(p)        # keep sizes small: s rounded down, p rounded up (p only feeds later terms, see below)
    # s is a lower bound up to roundings of p upward (which can only raise s); to stay rigorous recompute plainly:
    s_lo = Fr(0); s_hi = Fr(0); pl = y; pu = y
    for j in range(J + 1):
        s_lo = dn(s_lo + dn(pl / (2 * j + 1))); s_hi = up(s_hi + up(pu / (2 * j + 1)))
        pl = dn(pl * dn(y2)); pu = up(pu * up(y2))
    rem = up(pu / ((2 * J + 3) * (1 - up(y2))))       # tail of the series <= next power / ((2J+3)(1-y^2))
    lo, hi = 2 * s_lo, 2 * (s_hi + rem)
    if n != 2:
        k = n.bit_length() - 1; l2 = ln_int(2); lo, hi = lo + k * l2[0], hi + k * l2[1]
    _ln[n] = (dn(lo), up(hi)); return _ln[n]
def exp_neg(xlo, xhi):
    """enclosure of exp(x) for xlo <= x <= xhi <= 0, |x| < 8"""
    def e(x, upper):
        x = Fr(x)
        # exp(x) = exp(x/16)^16 ; Taylor of exp(t), |t| < 1/2: alternating, terms decreasing -> consecutive partial sums bracket
        t = x / 16; s = Fr(1); term = Fr(1); J = 60
        sums = []
        for j in range(1, J + 2):
            term = term * t / j
            s = s + term
            sums.append(s)
        a, b = sums[-1], sums[-2]
        lo, hi = (a, b) if a < b else (b, a)
        r = dn(lo) if not upper else up(hi)
        for _ in range(4):
            r = dn(r * r) if not upper else up(r * r)
        return r
    return e(dn(xlo), False), e(up(xhi), True)
def pow_enc(r, m, zlo, zhi):
    """enclosure of (r/m)^z, r <= m, z in [zlo, zhi], z > 0"""
    if r == m: return Fr(1), Fr(1)
    a, b = ln_int(r), ln_int(m)
    llo, lhi = a[0] - b[1], a[1] - b[0]            # ln(r/m) in [llo, lhi], both < 0
    assert lhi < 0
    return exp_neg(dn(llo * zhi), up(lhi * zlo))
def moment(blocks, m, z):
    lo = hi = Fr(0)
    for r, n in blocks:
        a, b = pow_enc(r, m, z, z); lo += n * a; hi += n * b
    return lo, hi
def fact(blocks, m, W, eps, S):
    """whole-block fact of R/tools/gen/foldlib.py: (t-1) M(z) + W ((m-1)/m)^z + W (1/m)^z < t W ; S=None: the limit M(z) < W.
    returns True (proved), False (proved false), None (undecided at this precision)"""
    z = 1 - Fr(eps)
    lo, hi = moment(blocks, m, z)
    if S is None:
        return True if hi < W else (False if lo >= W else None)
    t = 1 << S
    a = pow_enc(m - 1, m, z, z); b = pow_enc(1, m, z, z)
    L = (t - 1) * lo + W * (a[0] + b[0]); H = (t - 1) * hi + W * (a[1] + b[1])
    return True if H < t * W else (False if L >= t * W else None)
def best(blocks, m, W, S, scale=10 ** 8):
    lo, hi = 0, scale
    assert fact(blocks, m, W, Fr(0), S) in (True,) or True
    if fact(blocks, m, W, Fr(1, scale), S) is not True: return 0
    while hi - lo > 1:
        mid = (lo + hi) // 2
        f = fact(blocks, m, W, Fr(mid, scale), S)
        assert f is not None, "undecided: raise PREC"
        if f: lo = mid
        else: hi = mid
    return lo
def unit_blocks(h, v, bl, classes):
    B = {}
    for c in classes:
        for r, n in bl[c].items(): B[int(r)] = B.get(int(r), 0) + 5 * n
    for r in (2 * (h - 1) + 4, 2 * (h - 1), h - 1, 4): B[r] = B.get(r, 0) + 2 * v
    return sorted(B.items())
if __name__ == "__main__":
    # self-test of the enclosures against known values
    l2 = ln_int(2); assert l2[0] < Fr(6931471805599453094172321214581765680755001343602552, 10 ** 52) + Fr(1, 10**50) and l2[1] > Fr(6931471805599453094172321214581765680755001343602552, 10 ** 52) - Fr(1, 10**50) and l2[1] - l2[0] < Fr(1, 10 ** 60)
    e1 = exp_neg(Fr(-1), Fr(-1)); assert e1[0] <= Fr(36787944117144232159552377016146086744581113103176783, 10 ** 53) + Fr(1, 10**50) and e1[1] - e1[0] < Fr(1, 10 ** 55), (float(e1[0]), float(e1[1] - e1[0]))
    print("enclosures: width of ln 2 %.1e, of exp(-1) %.1e" % (float(l2[1] - l2[0]), float(e1[1] - e1[0])))
    for path in sys.argv[1:]:
        d = json.load(gzip.open(path)); h, v, R = d["h"], d["v"], d["R"]; bl = d["blocks"]; m, W = 5 * h, 4 * v + R
        cst = sum(int(r) * n for r, n in bl["c"].items())
        print("== %s : h=%d v=%d R=%d m=%d W=%d cst=%d (field cst=%s)" % (path.split("/")[-1], h, v, R, m, W, cst, d.get("cst")))
        for name, classes in (("published unit (x, y, helpers, copies)", "xysc"), ("WHAT-IF no scratch copies (x, y, helpers)", "xys")):
            B = unit_blocks(h, v, bl, classes)
            nb = sum(n for r, n in B); mv = sum(r * n for r, n in B); D = W * m - mv
            assert D == (4 * v - 5 * cst if "c" in classes else 4 * v)
            A13 = best(B, m, W, 13); Ainf = best(B, m, W, None)
            print("   %-42s blocks %d (%.4f per array), moves %d, deficit D = W m - moves = %d (share %.5f %%)" % (name, nb, nb / W, mv, D, 100.0 * D / (W * m)))
            print("      largest A with the whole-block fact proved at A/10^8 : fill 2^13: %d ; fill -> infinity (sum < W): %d ; A+1 proved to FAIL in both" % (A13, Ainf))
            # the per-rank law ("a moves per array"): z = ln(a)/ln(m) with a = moves / W  -- comparison only, floats
            import math
            print("      for comparison, 'moves per array' law 1 - ln(a)/ln(m), floats: %.4e" % (1 - math.log(mv / W) / math.log(m)))
    # the three caps: block lists in units of h (multiply by a common denominator to get integers)
    print("== caps (WHAT-IF block lists; W = 1 array, shears, helpers and copies free)")
    for name, blocks, m in (("r = h/2, three merged blocks (h/2, h, h) of m = 3h", [(1, 1), (2, 2)], 6),
                            ("r = h/3, three merged blocks (2h/3, h, h) of m = 3h", [(2, 1), (3, 2)], 9),
                            ("r = h/3, four blocks: 3 x (2h/3) and one catch-up 2h/3, m = 3h", [(2, 4)], 9),
                            ("r = h/2, four blocks: 3 x (h/2) and one catch-up h, m = 3h", [(1, 3), (2, 1)], 6),
                            ("r = h/2, five-stage word: 10 x (h/2) per 4 arrays + idle (h+2h, h, h/2, 2h) x 2, m = 5h", [(1, 10), (6, 2), (2, 2), (1, 2), (4, 2)], 10)):
        W = 1 if m != 10 else 4
        A = best(blocks, m, W, None, 10 ** 6)
        print("   %-90s saving in [%d, %d) / 10^6" % (name, A, A + 1))
    print("== k equal blocks, skipped share rho: closed form saving = L/(ln k + L), L = ln(1/(1-rho)); check of one instance by enclosure")
    # k = 2, rho = 1/10 : blocks 2 x (9/20 m): m = 20, ranks 9, 9
    A = best([(9, 2)], 20, 1, None, 10 ** 6); import math
    print("   k=2, rho=0.1: enclosure [%d, %d)/10^6 ; closed form %.6f" % (A, A + 1, math.log(1 / 0.9) / (math.log(2) + math.log(1 / 0.9))))
