# u-2-onerun: numerical check of every inequality in the "nested runs" lower bound for the two-chain picture of subset sums.
# Plain pictures (no signs).  Whole numbers and fractions; logarithms only in the last, printed, comparison.
# For a pair of orders (rows = output order, cols = input order) it computes
#   corners  = non-zeros of the second difference M               (the two-chain program has N - 2 + corners gates, count (G))
#   R        = number of runs (maximal stretches of inputs, consecutive in the input order, on which the step's difference
#              vector  d_a = row a - row a+1  is one non-zero value)
#   V        = total size of the supports of the d_a = sum of run lengths
#   c(T)     = number of steps whose difference vector is non-zero at input T
#   S(T)     = sum of the lengths of the runs through T
# and checks:  (1) corners >= R + (number of steps)... at least corners >= R
#              (2) nested-run lemma: sort the runs through T by how far they reach to the left; the left part of the j-th lies
#                  inside down(intersection of the first j tops), so it has at most 2^|intersection| <= 2N/j inputs; same on the right
#              (3) S(T) <= 4 N (1 + ln c(T))
#              (4) R = sum_T sum_{runs through T} 1/|run|  >=  sum_T c(T)^2 / S(T)
#              (5) V >= 3^k/2 - N/4 ;  V_j (inputs of size j) >= (j/k) C(k,j) (2^(k-j) - 1/2)
import sys, math, random, ast
from fractions import Fraction
from math import comb

def analyse(k, rows, cols, verbose=True, label=""):
    N = 1 << k
    pos = {cols[b]: b for b in range(N)}
    Z = [[1 if (rows[a] & cols[b]) == cols[b] else 0 for b in range(N)] + [0] for a in range(N)] + [[0] * (N + 1)]
    corners = 0; R = 0; V = 0
    runs_through = [[] for _ in range(N)]     # per position: list of (left, right, top address)
    Vj = [0] * (k + 1)
    for a in range(N):
        d = [Z[a][b] - Z[a + 1][b] for b in range(N + 1)]
        corners += sum(1 for b in range(N) if d[b] != d[b + 1])
        b = 0
        while b < N:
            if d[b] == 0: b += 1; continue
            e = b
            while e + 1 < N and d[e + 1] == d[b]: e += 1
            R += 1; V += e - b + 1
            top = rows[a] if d[b] == 1 else rows[a + 1]       # the output that contains the inputs of this run
            for x in range(b, e + 1):
                runs_through[x].append((b, e, top)); Vj[bin(cols[x]).count('1')] += 1
                assert (cols[x] & top) == cols[x]              # every input of the run lies inside the top
            b = e + 1
    ok2 = ok3 = True; lbA = Fraction(0); lbB = 0.0; sumc2 = 0; worst3 = 0.0
    for p in range(N):
        L = runs_through[p]; c = len(L)
        if c == 0: ok2 = False; continue
        S = sum(e - b + 1 for (b, e, t) in L)
        # (2) left parts
        for side in (0, 1):
            srt = sorted(L, key=(lambda r: r[0]) if side == 0 else (lambda r: -r[1]))
            inter = N - 1
            for j, (b, e, t) in enumerate(srt, 1):
                inter &= t
                part = (p - b + 1) if side == 0 else (e - p + 1)
                if part > (1 << bin(inter).count('1')): ok2 = False
                if part * j > 2 * N: ok2 = False
        if S > 4 * N * (1 + math.log(c)): ok3 = False
        worst3 = max(worst3, S / (4 * N * (1 + math.log(c))))
        lbA += Fraction(c * c, S); lbB += c * c / (4 * N * (1 + math.log(c))); sumc2 += c * c
    okV = (2 * V >= 3 ** k - N // 2)
    okVj = all(Vj[j] * 2 * k >= j * comb(k, j) * (2 ** (k - j + 1) - 1) for j in range(1, k + 1))
    lbC = sum(Fraction(Vj[j] ** 2, comb(k, j)) for j in range(k + 1)) / (4 * N * (1 + math.log(N)))
    if verbose:
        print(f"{label} N={N}: corners {corners}, runs R {R}, volume V {V} (3^k = {3**k}); "
              f"checks: corners>=R {corners >= R}, nested-run lemma {ok2}, S(T)<=4N(1+ln c) {ok3} (worst ratio {worst3:.3f}), "
              f"V bound {okV}, V_j bounds {okVj}; chain: R {R} >= sum c^2/S = {float(lbA):.2f} >= sum c^2/(4N(1+ln c)) = {lbB:.2f}; "
              f"sum c^2 = {sumc2} (5^k = {5**k})")
    return corners, R, V, ok2 and ok3 and okV and okVj and corners >= R and R >= lbA and float(lbA) >= lbB - 1e-9

def general_bound(k):
    N = 1 << k
    s = sum(Fraction(j * j, k * k) * comb(k, j) * (Fraction(2 ** (k - j + 1) - 1, 2)) ** 2 for j in range(1, k + 1))
    return float(s) / (4 * N * (1 + math.log(N)))

def gray(k): return [i ^ (i >> 1) for i in range(1 << k)]

if __name__ == "__main__":
    allok = True
    # the pictures of q-cross (best found by its annealer), if present
    base = "waves/wave-05/q-cross/"
    for f in ("cat3_4.out", "cat3_8.out", "cat3_16.out", "cat3_32.out", "cat3g_64.out"):
        try:
            txt = open(base + f).read().split('BEST')[-1]
            rows = ast.literal_eval(txt.split('rows ')[1].split(' r ')[0]); cols = ast.literal_eval(txt.split('cols ')[1].split(' c ')[0])
            k = len(rows).bit_length() - 1
            c, R, V, ok = analyse(k, rows, cols, True, "q-cross " + f); allok &= ok
        except Exception as ex:
            print("skip", f, ex)
    for k in range(2, 8):
        g = gray(k); N = 1 << k
        c, R, V, ok = analyse(k, g, g, True, "Gray/Gray"); allok &= ok
        c, R, V, ok = analyse(k, list(range(N)), list(range(N)), True, "counting/counting"); allok &= ok
        random.seed(k)
        bad = 0; minc = 10 ** 9
        for t in range(200 if k <= 5 else 30):
            rows = list(range(N)); cols = list(range(N)); random.shuffle(rows); random.shuffle(cols)
            c, R, V, ok = analyse(k, rows, cols, False); bad += (not ok); minc = min(minc, c)
        print(f"  random pairs of orders at N={N}: all checks passed in all but {bad} cases; least corners seen {minc}")
        allok &= (bad == 0)
    print("ALL CHECKS PASSED" if allok else "SOME CHECK FAILED")
    print("The general bound  R >= [sum_j (j/k)^2 C(k,j) (2^(k-j) - 1/2)^2] / (4N(1 + ln N))  against N and Yates' (N/2) log2 N:")
    for k in (4, 5, 6, 8, 10, 16, 20, 30, 40, 44, 50, 54, 56, 60, 80, 100):
        N = 1 << k
        print(f"  k={k}: bound {general_bound(k):.4g}; N = {N:.4g}; (N/2) log2 N = {N*k/2:.4g}; bound/N = {general_bound(k)/N:.4g}; (5/2)^k = {2.5**k:.4g}")
