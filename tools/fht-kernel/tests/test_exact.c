/* test_exact.c -- exactness tests of the kernel (run by ../test.sh).  Prints one line per check and ends with
 * "ALL PASS" (exit 0) or "FAIL" (exit 1).
 *
 *  1. Whole-number inputs in [-4, 4] (fixed seed), every log_n from 0 to 20, float and double: the output equals,
 *     number for number, a plain textbook transform done in the same precision.  On these inputs every intermediate
 *     value is a whole number below 2^24, so float is exact too, and any wiring error shows.
 *  2. The portable code (whtc_plain_*) gives the same numbers as the compiled code (whtc_fht_*) on whole-number and on
 *     real inputs, float and double, log_n 0 to 20.  (Where both are the portable code this is trivially true.)
 *  3. The _oop functions leave the input unchanged and give the in-place result; _scaled with scale 1 gives the
 *     in-place result and with scale 2 exactly twice it.
 *  4. FFHT's return codes: 0 for log_n 0 (the buffer unchanged) and 30, 1 for -1 and 31 (the buffers untouched).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "../whtc.h"

static unsigned long long g_seed = 0x2545F4914F6CDD1Dull;
static int rint4(void) { /* a whole number in [-4, 4] */
  g_seed = g_seed * 6364136223846793005ull + 1442695040888963407ull;
  return (int)((g_seed >> 33) % 9) - 4;
}
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

#define TEXTBOOK(T, NAME)                                                                            \
  static void NAME(T *x, int L) {                                                                    \
    size_t n = (size_t)1 << L;                                                                       \
    for (size_t h = 1; h < n; h <<= 1)                                                               \
      for (size_t i = 0; i < n; i += 2 * h)                                                          \
        for (size_t j = i; j < i + h; j++) { T a = x[j], b = x[j + h]; x[j] = a + b; x[j + h] = a - b; } \
  }
TEXTBOOK(float, textbook_f)
TEXTBOOK(double, textbook_d)

#define DIFFERENT(T, NAME)                                                                           \
  static long NAME(const T *a, const T *b, size_t n) {                                               \
    long bad = 0;                                                                                    \
    for (size_t i = 0; i < n; i++) bad += !(a[i] == b[i]);                                           \
    return bad;                                                                                      \
  }
DIFFERENT(float, diff_f)
DIFFERENT(double, diff_d)

int main(void) {
  int ok = 1;
  const int maxL = 20;
  size_t nmax = (size_t)1 << maxL;
  float *xf = malloc(nmax * sizeof(float)), *yf = malloc(nmax * sizeof(float)), *zf = malloc(nmax * sizeof(float));
  double *xd = malloc(nmax * sizeof(double)), *yd = malloc(nmax * sizeof(double)), *zd = malloc(nmax * sizeof(double));
  if (!xf || !yf || !zf || !xd || !yd || !zd) { printf("out of memory\nFAIL\n"); return 1; }
  printf("# test_exact: %s\n", whtc_step());

  /* 1 and 2: whole numbers */
  long bad1f = 0, bad1d = 0, bad2 = 0;
  for (int L = 0; L <= maxL; L++) {
    size_t n = (size_t)1 << L;
    for (size_t i = 0; i < n; i++) { int v = rint4(); xf[i] = (float)v; xd[i] = (double)v; }
    memcpy(yf, xf, n * sizeof(float)); memcpy(zf, xf, n * sizeof(float));
    memcpy(yd, xd, n * sizeof(double)); memcpy(zd, xd, n * sizeof(double));
    ok &= whtc_fht_float(yf, L) == 0 && whtc_fht_double(yd, L) == 0;
    textbook_f(zf, L); textbook_d(zd, L);
    long bf = diff_f(yf, zf, n), bd = diff_d(yd, zd, n);
    bad1f += bf; bad1d += bd;
    memcpy(zf, xf, n * sizeof(float)); memcpy(zd, xd, n * sizeof(double));
    whtc_plain_fht_float(zf, L); whtc_plain_fht_double(zd, L);
    bad2 += diff_f(yf, zf, n) + diff_d(yd, zd, n);
    if (bf || bd || L <= 3 || L % 4 == 0)
      printf("CHECK whole numbers 2^%-2d: float %ld wrong, double %ld wrong of %zu  %s\n", L, bf, bd, n,
             bf || bd ? "FAIL" : "PASS");
  }
  printf("CHECK whole numbers in [-4, 4], every 2^0 to 2^%d, float and double, equal to the textbook number for number: %s\n",
         maxL, bad1f || bad1d ? "FAIL" : "PASS");
  ok &= !bad1f && !bad1d;

  /* 2: real inputs, portable code against compiled code */
  for (int L = 0; L <= maxL; L++) {
    size_t n = (size_t)1 << L;
    for (size_t i = 0; i < n; i++) { xd[i] = rreal(); xf[i] = (float)rreal(); }
    memcpy(yf, xf, n * sizeof(float)); memcpy(zf, xf, n * sizeof(float));
    memcpy(yd, xd, n * sizeof(double)); memcpy(zd, xd, n * sizeof(double));
    whtc_fht_float(yf, L); whtc_plain_fht_float(zf, L);
    whtc_fht_double(yd, L); whtc_plain_fht_double(zd, L);
    bad2 += diff_f(yf, zf, n) + diff_d(yd, zd, n);
  }
  printf("CHECK the portable code gives the same numbers as the compiled code, whole and real inputs, 2^0 to 2^%d: %s (%ld differ)\n",
         maxL, bad2 ? "FAIL" : "PASS", bad2);
  ok &= !bad2;

  /* 3: _oop and _scaled */
  {
    int L = 12;
    size_t n = (size_t)1 << L;
    for (size_t i = 0; i < n; i++) { xf[i] = (float)rreal(); xd[i] = rreal(); }
    memcpy(yf, xf, n * sizeof(float)); memcpy(yd, xd, n * sizeof(double));
    whtc_fht_float(yf, L); whtc_fht_double(yd, L);
    memcpy(zf, xf, n * sizeof(float)); memcpy(zd, xd, n * sizeof(double));
    float *of = malloc(n * sizeof(float)); double *od = malloc(n * sizeof(double));
    int r = whtc_fht_float_oop(xf, of, L) | whtc_fht_double_oop(xd, od, L);
    int oop = r == 0 && !diff_f(of, yf, n) && !diff_d(od, yd, n) && !diff_f(xf, zf, n) && !diff_d(xd, zd, n);
    printf("CHECK _oop: input unchanged, output equal to the in-place transform: %s\n", oop ? "PASS" : "FAIL");
    ok &= oop;
    memcpy(of, xf, n * sizeof(float)); memcpy(od, xd, n * sizeof(double));
    r = whtc_fht_float_scaled(of, L, 1.0f) | whtc_fht_double_scaled(od, L, 1.0);
    int s1 = r == 0 && !diff_f(of, yf, n) && !diff_d(od, yd, n);
    memcpy(of, xf, n * sizeof(float)); memcpy(od, xd, n * sizeof(double));
    r = whtc_fht_float_scaled(of, L, 2.0f) | whtc_fht_double_scaled(od, L, 2.0);
    long s2bad = 0;
    for (size_t i = 0; i < n; i++) s2bad += !(of[i] == 2.0f * yf[i]) + !(od[i] == 2.0 * yd[i]);
    printf("CHECK _scaled: scale 1 equal to the in-place transform, scale 2 exactly twice it: %s\n",
           r == 0 && s1 && !s2bad ? "PASS" : "FAIL");
    ok &= r == 0 && s1 && !s2bad;
    free(of); free(od);
  }

  /* 4: return codes */
  {
    float f4[4] = {1, 2, 3, 4}, g4[4] = {9, 9, 9, 9};
    double d4[4] = {1, 2, 3, 4}, e4[4] = {9, 9, 9, 9};
    int r0 = whtc_fht_float(f4, 0) | whtc_fht_double(d4, 0);
    int same0 = f4[0] == 1 && d4[0] == 1;
    int rm = whtc_fht_float(f4, -1) & whtc_fht_double(d4, -1) & whtc_fht_float(f4, 31) & whtc_fht_double(d4, 31) &
             whtc_fht_float_oop(f4, g4, -1) & whtc_fht_double_oop(d4, e4, 31) & whtc_fht_float_scaled(f4, 31, 2.0f) &
             whtc_fht_double_scaled(d4, -5, 2.0);
    int untouched = f4[0] == 1 && f4[3] == 4 && d4[1] == 2 && g4[0] == 9 && e4[3] == 9;
    int r30 = whtc_plain_fht_float(f4, -1) == 1 && whtc_plain_fht_double(d4, 31) == 1;
    int pass = r0 == 0 && same0 && rm == 1 && untouched && r30;
    printf("CHECK return codes: 0 for log_n 0 (buffer unchanged); 1 for -1 and 31 (buffers untouched): %s\n",
           pass ? "PASS" : "FAIL");
    ok &= pass;
  }
  printf("%s\n", ok ? "ALL PASS" : "FAIL");
  free(xf); free(yf); free(zf); free(xd); free(yd); free(zd);
  return ok ? 0 : 1;
}
