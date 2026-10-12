# moore_exact.py : the step "graph statement -> number of gates" of ag-7 section 4, in exact whole-number arithmetic.
#
# Setting (two-element field).  N = 2^k outputs, degree d, shortest relation delta = 2^(d+1), rank R = number of
# sets of at most d bits.  V = number of wires that are not outputs (inputs included).  gates = N + V - R.
# Lemma, form A: a graph on v = V + 1 vertices with E = N - 1 edges and no cycle shorter than 2r, r = 2^d - 1.
# Lemma, form B: at most V outputs carry a label; the other E - V are edges of a graph on V vertices with no cycle
#                shorter than 2r, r = 2^d.
# Theorem used (Alon, Hoory, Linial, "The Moore bound for irregular graphs", Graphs and Combinatorics 18 (2002) 53-57):
#   a graph with v vertices, average degree D >= 2 and no cycle shorter than 2r has v >= 2 (1 + (D-1) + ... + (D-1)^(r-1)).
# With e edges, D - 1 = (2e - v)/v = x/v.  For x > v the sum is (x^r - v^r) / ((x - v) v^(r-1)), so the theorem
# FORBIDS (v, e) exactly when   x^r > (e - v + 1) v^r     [x = 2e - v > v].       (*)
# For e <= v nothing is forbidden (a forest plus a few long cycles).  (*) is monotone: if v is forbidden so is v - 1.
# So the least allowed v is found by bisection; the bisection uses 60-digit decimals to choose where to look and
# the final answer is CERTIFIED by two exact whole-number tests of (*): v_min allowed, v_min - 1 forbidden.
import sys
from math import comb
from decimal import Decimal, getcontext
getcontext().prec = 80

def forbidden_exact(v, e, r):
    x = 2 * e - v
    if x <= v: return False
    return x ** r > (e - v + 1) * v ** r

def forbidden_fast(v, e, r):
    x = 2 * e - v
    if x <= v: return False
    return r * (Decimal(x) / Decimal(v)).ln() > Decimal(e - v + 1).ln()

def least_vertices(e, r, exact_limit_bits=3_000_000):
    """least v such that (v, e) is not forbidden for girth >= 2r; certified exactly when the powers are small enough"""
    lo, hi = 1, e          # (e, e): x = v, never forbidden
    if forbidden_fast(1, e, r) is False: return 1, True
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if forbidden_fast(mid, e, r): lo = mid
        else: hi = mid
    bits = r * (2 * e).bit_length()
    if bits <= exact_limit_bits:
        ok = (not forbidden_exact(hi, e, r)) and forbidden_exact(hi - 1, e, r)
        if not ok:      # decimal search was off by a hair: walk exactly
            while forbidden_exact(hi, e, r): hi += 1
            while hi > 1 and not forbidden_exact(hi - 1, e, r): hi -= 1
        return hi, True
    return hi, False

def formA(N, d):
    v, cert = least_vertices(N - 1, 2 ** d - 1)
    return v - 1, cert            # V >= v - 1

def formB(N, d):
    # least V with: (N - 1 - V) edges on V vertices allowed for girth >= 2 * 2^d
    r = 2 ** d
    E = N - 1
    def bad(V, exact):
        e = E - V
        if e <= 0: return False
        return forbidden_exact(V, e, r) if exact else forbidden_fast(V, e, r)
    lo, hi = 1, E
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if bad(mid, False): lo = mid
        else: hi = mid
    cert = r * (2 * E).bit_length() <= 3_000_000
    if cert:
        while bad(hi, True): hi += 1
        while hi > 1 and not bad(hi - 1, True): hi -= 1
    return hi, cert

def show(num, den, places=4):
    q = (num * 10 ** places) // den          # rounded DOWN, exact
    s = str(q).rjust(places + 1, '0')
    return s[:-places] + '.' + s[-places:]

ks = [int(a) for a in sys.argv[1:]] or [8, 16, 32, 64, 128, 256]
print("exact; every figure is rounded DOWN; 'cert' = the threshold was confirmed by two exact whole-number tests")
print("k    d   rank/N      V/N >= (A)  V/N >= (B)  gates/N >=   cert   ag-7 law.out gates/N")
ag7 = {(8,2):1.1842,(8,3):1.3287,(16,2):1.1089,(16,3):1.3480,(16,4):1.6415,(16,5):1.7480,(16,6):1.7063,(16,7):1.5683,
       (32,2):1.0078,(32,3):1.1080,(32,4):1.3810,(32,5):1.6727,(32,6):1.8396,(32,7):1.9219,(32,8):1.9595,(32,10):1.9664,(32,12):1.8904,
       (64,2):1.0000,(64,3):1.0077,(64,4):1.1066,(64,5):1.3909,(64,6):1.6696,(64,7):1.8340,(64,8):1.9181,(64,10):1.9802,(64,12):1.9952,(64,16):1.9997,
       (128,2):1.0000,(128,3):1.0000,(128,4):1.0077,(128,5):1.1085,(128,6):1.3955,(128,7):1.6681,(128,8):1.8312,(128,10):1.9582,(128,12):1.9897,(128,16):1.9994}
for k in ks:
    N = 2 ** k
    for d in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16):
        if d >= k / 2: continue
        if d >= 14 and k > 128: continue
        R = sum(comb(k, j) for j in range(d + 1))
        A, ca = formA(N, d)
        B, cb = formB(N, d)
        V = max(A, B)
        helpers = max(0, V - (R - 1))
        gates = N - 1 + helpers
        prev = ag7.get((k, d))
        flag = ''
        if prev is not None:
            mine = gates * 10000 // N
            flag = f"{prev:.4f}" + ('' if abs(mine - round(prev * 10000)) <= 1 else '   <-- differs')
        print(f"{k:<4d} {d:<3d} {R / N:<11.3g} {show(A, N):<11s} {show(B, N):<11s} {show(gates, N):<12s} {'yes' if (ca and cb) else 'no':<6s} {flag}", flush=True)
    print()
