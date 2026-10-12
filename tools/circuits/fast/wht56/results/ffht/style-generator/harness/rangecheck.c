/* rangecheck.c -- do the numbers stay ordinary while the harness times a variant?
 *
 *   ./rangecheck          (not a timing; a check of the timing's data)
 *
 * The harness times R transforms in a row on the same array, starting from the same input each
 * time.  A variant that leaves its result divided by 2^P (g20s) grows more slowly than FFHT.
 * If its numbers ever became denormal (smaller than the smallest ordinary float), the processor
 * would handle them much more slowly, and the timing would show that instead of the kernel.
 * This program repeats exactly what the harness does to the data (the same input, the same
 * rule for R) for ffht, g20x, g20s and g19f, and after EVERY transform counts the numbers that
 * are denormal, infinite or not a number, and notes the smallest and the largest size seen.
 */
#include <float.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "fht.h"

int g20x_fht_float(float *, int);  int g20x_fht_double(double *, int);
int g20s_fht_float(float *, int);  int g20s_fht_double(double *, int);
int g19f_fht_float(float *, int);  int g19f_fht_double(double *, int);

#define RUN(T, SUF, EXP_SAFE, TMIN)                                                             \
static int run_##SUF(const char *name, int (*f)(T *, int), int k)                               \
{                                                                                               \
    const size_t n = (size_t)1 << k;                                                            \
    T *x = aligned_alloc(64, n * sizeof(T) < 64 ? 64 : n * sizeof(T));                          \
    uint64_t s = (uint64_t)(77 * k + (int)sizeof(T)) * 0x9E3779B97F4A7C15ull + 0xD1B54A32D192ED03ull; \
    for (size_t i = 0; i < n; i++) { s ^= s << 13; s ^= s >> 7; s ^= s << 17;                   \
                                     x[i] = (T)((int)((s >> 20) % 3u) - 1); }                    \
    long R = 2 * (long)(EXP_SAFE / (k > 0 ? k : 1));                                            \
    if (R < 2) R = 2;                                                                           \
    size_t den = 0, bad = 0;                                                                    \
    double lo = 1e300, hi = 0;                                                                  \
    for (long r = 0; r < R; r++) {                                                              \
        f(x, k);                                                                                \
        for (size_t i = 0; i < n; i++) {                                                        \
            const double a = fabs((double)x[i]);                                                \
            if (!(a <= DBL_MAX)) { bad++; continue; }                                           \
            if (a == 0) continue;                                                               \
            if (a < TMIN) den++;                                                                \
            if (a < lo) lo = a;                                                                 \
            if (a > hi) hi = a;                                                                 \
        }                                                                                       \
    }                                                                                           \
    printf("R type=%s k=%d variant=%s transforms_in_a_row=%ld denormal=%zu inf_or_nan=%zu "     \
           "smallest_nonzero=2^%.1f largest=2^%.1f %s\n", #T, k, name, R, den, bad,             \
           log2(lo), log2(hi), (den || bad) ? "NOT ORDINARY" : "ok");                           \
    free(x);                                                                                    \
    return (den || bad) ? 1 : 0;                                                                \
}

RUN(float, f, 120, FLT_MIN)
RUN(double, d, 1000, DBL_MIN)

int main(void)
{
    int bad = 0;
    for (int k = 3; k <= 24; k++) {
        bad += run_f("ffht", fht_float, k);
        bad += run_f("g20x", g20x_fht_float, k);
        bad += run_f("g20s", g20s_fht_float, k);
        bad += run_f("g19f", g19f_fht_float, k);
    }
    for (int k = 3; k <= 24; k++) {
        bad += run_d("ffht", fht_double, k);
        bad += run_d("g20x", g20x_fht_double, k);
        bad += run_d("g20s", g20s_fht_double, k);
        bad += run_d("g19f", g19f_fht_double, k);
    }
    printf("# rangecheck: %s\n", bad ? "SOME NUMBERS WERE NOT ORDINARY" : "every number ordinary in every case");
    return bad ? 1 : 0;
}
