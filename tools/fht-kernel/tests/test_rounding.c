/* test_rounding.c -- how far the kernel's results are from the textbook's, and from the exact transform, on real
 * inputs (run by ../test.sh).  Prints a table; it has no pass or fail of its own.
 *
 * Inputs: numbers uniform in [-1, 1) (fixed seed), log_n 5 to 20, in float and in double.  For each size:
 *   kernel - textbook   the largest difference between the kernel's output and a plain textbook transform done in the
 *                       same precision in FFHT's order of levels (FFHT's own output on these inputs), divided by the
 *                       largest output;
 *   kernel - exact      the same against the exact transform;
 *   textbook - exact    the textbook's own error, for comparison.
 * The exact transform is computed as a textbook in double-double arithmetic (each sum kept as two doubles, about 106
 * bits): its own error is far below every figure printed here.  Long double is not used, since on some machines (for
 * example arm64 macOS) it is the same as double.
 */
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "../whtc.h"

/* real inputs: xorshift64*, the generator (and the seed) of the timing harness's bench.h.  A plain 64-bit linear
 * congruential generator is not used for real inputs: its lattice lines up with the transform's index bits, and on
 * its numbers both the textbook and the circuit show about four times the rounding error of well-mixed inputs. */
static unsigned long long g_xs = 0x9E3779B97F4A7C15ull;
static double rreal(void) { /* uniform in [-1, 1) */
  g_xs ^= g_xs >> 12;
  g_xs ^= g_xs << 25;
  g_xs ^= g_xs >> 27;
  return (double)((g_xs * 0x2545F4914F6CDD1Dull) >> 11) * (2.0 / 9007199254740992.0) - 1.0;
}

/* double-double: hi + lo, with an error-free sum (Knuth's TwoSum) at every butterfly */
typedef struct { double hi, lo; } dd;
static dd two_sum(double a, double b) {
  dd r;
  r.hi = a + b;
  double bb = r.hi - a;
  r.lo = (a - (r.hi - bb)) + (b - bb);
  return r;
}
static dd dd_add(dd a, dd b) {
  dd s = two_sum(a.hi, b.hi);
  double lo = s.lo + a.lo + b.lo;
  return two_sum(s.hi, lo);
}
static dd dd_neg(dd a) { a.hi = -a.hi; a.lo = -a.lo; return a; }
static void exact(dd *x, int L) {
  size_t n = (size_t)1 << L;
  for (size_t h = 1; h < n; h <<= 1)
    for (size_t i = 0; i < n; i += 2 * h)
      for (size_t j = i; j < i + h; j++) { dd a = x[j], b = x[j + h]; x[j] = dd_add(a, b); x[j + h] = dd_add(a, dd_neg(b)); }
}
#define TEXTBOOK(T, NAME)                                                                            \
  static void NAME(T *x, int L) {                                                                    \
    size_t n = (size_t)1 << L;                                                                       \
    for (size_t h = 1; h < n; h <<= 1)                                                               \
      for (size_t i = 0; i < n; i += 2 * h)                                                          \
        for (size_t j = i; j < i + h; j++) { T a = x[j], b = x[j + h]; x[j] = a + b; x[j + h] = a - b; } \
  }
TEXTBOOK(float, textbook_f)
TEXTBOOK(double, textbook_d)

int main(void) {
  const int lo = 5, hi = 20;
  size_t nmax = (size_t)1 << hi;
  float *xf = malloc(nmax * sizeof(float)), *kf = malloc(nmax * sizeof(float)), *tf = malloc(nmax * sizeof(float));
  double *xd = malloc(nmax * sizeof(double)), *kd = malloc(nmax * sizeof(double)), *td = malloc(nmax * sizeof(double));
  dd *ef = malloc(nmax * sizeof(dd)), *ed = malloc(nmax * sizeof(dd));
  if (!xf || !kf || !tf || !xd || !kd || !td || !ef || !ed) { printf("out of memory\n"); return 1; }
  printf("# test_rounding: %s\n", whtc_step());
  printf("# relative to the largest output; real inputs uniform in [-1, 1); exact = double-double textbook\n");
  printf("# %-5s | %-11s %-11s %-11s | %-11s %-11s %-11s\n", "n", "float:", "", "", "double:", "", "");
  printf("# %-5s | %-11s %-11s %-11s | %-11s %-11s %-11s\n", "", "kernel-tb", "kernel-ex", "tb-ex", "kernel-tb",
         "kernel-ex", "tb-ex");
  double worst[6] = {0, 0, 0, 0, 0, 0};
  for (int L = lo; L <= hi; L++) {
    size_t n = (size_t)1 << L;
    for (size_t i = 0; i < n; i++) {
      xd[i] = rreal();
      xf[i] = (float)rreal();
    }
    memcpy(kf, xf, n * sizeof(float)); memcpy(tf, xf, n * sizeof(float));
    memcpy(kd, xd, n * sizeof(double)); memcpy(td, xd, n * sizeof(double));
    whtc_fht_float(kf, L); textbook_f(tf, L);
    whtc_fht_double(kd, L); textbook_d(td, L);
    for (size_t i = 0; i < n; i++) { ef[i].hi = xf[i]; ef[i].lo = 0; ed[i].hi = xd[i]; ed[i].lo = 0; }
    exact(ef, L); exact(ed, L);
    double m[6] = {0, 0, 0, 0, 0, 0}, yf = 0, yd = 0;
    for (size_t i = 0; i < n; i++) {
      double xef = ef[i].hi + ef[i].lo, xed_hi = ed[i].hi, xed_lo = ed[i].lo;
      if (fabs(xef) > yf) yf = fabs(xef);
      if (fabs(xed_hi) > yd) yd = fabs(xed_hi);
      double a[6] = {fabs((double)kf[i] - (double)tf[i]), fabs((double)kf[i] - xef), fabs((double)tf[i] - xef),
                     fabs(kd[i] - td[i]), fabs((kd[i] - xed_hi) - xed_lo), fabs((td[i] - xed_hi) - xed_lo)};
      for (int k = 0; k < 6; k++) if (!(a[k] <= m[k])) m[k] = a[k];
    }
    for (int k = 0; k < 3; k++) m[k] /= yf;
    for (int k = 3; k < 6; k++) m[k] /= yd;
    for (int k = 0; k < 6; k++) if (m[k] > worst[k]) worst[k] = m[k];
    printf("  2^%-3d | %-11.2e %-11.2e %-11.2e | %-11.2e %-11.2e %-11.2e\n", L, m[0], m[1], m[2], m[3], m[4], m[5]);
  }
  printf("  worst | %-11.2e %-11.2e %-11.2e | %-11.2e %-11.2e %-11.2e\n", worst[0], worst[1], worst[2], worst[3],
         worst[4], worst[5]);
  printf("# float: the kernel differs from the textbook by at most %.2e of the largest output (2^%d to 2^%d)\n",
         worst[0], lo, hi);
  printf("# double: the kernel differs from the textbook by at most %.2e of the largest output (2^%d to 2^%d)\n",
         worst[3], lo, hi);
  free(xf); free(kf); free(tf); free(xd); free(kd); free(td); free(ef); free(ed);
  return 0;
}
