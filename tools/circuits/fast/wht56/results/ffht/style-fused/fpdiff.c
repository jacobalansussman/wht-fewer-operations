/* fpdiff.c -- two questions about the fused lines.
 *
 * 1. On inputs that are integers small enough for every sum to be held exactly, are the three
 *    variants BIT-identical (memcmp), for 2^3 .. 2^KMAX numbers?  float: inputs -7..7 up to 2^12,
 *    -1..1 above (every sum is an integer of size at most 2^24, which a float holds exactly);
 *    double: -1000..1000 (sums below 2^53); int32: -1000..1000 up to 2^20, -15..15 above.
 *
 * 2. On arbitrary floats the fused line rounds once where two instructions round twice.  How far
 *    apart are the results, and which is closer to the true value?  The true value is computed
 *    with more digits: in double for float data, in 113-bit quad for double data.  Two kinds of
 *    input: uniform in [-1, 1), and sign * 2^e * (1 + u) with e uniform in -20 .. 20.
 *
 *   ./fpdiff [KMAX_IDENT] [KMAX_ARBITRARY]
 */
#include <math.h>
#include <quadmath.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "whtf.h"

static uint64_t rs = 0x243F6A8885A308D3ull;
static uint64_t rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static double unif(void) { return (double)(rnd() >> 11) / 9007199254740992.0; }      /* [0, 1) */

static void *alloc(size_t bytes) { void *p = aligned_alloc(64, (bytes + 63) / 64 * 64); if (!p) exit(2); return p; }

#define IDENT(T, SUF, NAMEA, FA, NAMEB, FB, NAMEC, FC, AMPEXPR) \
    static int ident_##SUF(int kmax) \
    { \
        int bad = 0; \
        for (int k = 3; k <= kmax; k++) { \
            const size_t n = (size_t)1 << k; \
            const int amp = (AMPEXPR); \
            T *src = alloc(n * sizeof(T)), *a = alloc(n * sizeof(T)), *b = alloc(n * sizeof(T)), *c = alloc(n * sizeof(T)); \
            for (size_t i = 0; i < n; i++) src[i] = (T)((int)(rnd() % (uint64_t)(2 * amp + 1)) - amp); \
            memcpy(a, src, n * sizeof(T)); memcpy(b, src, n * sizeof(T)); memcpy(c, src, n * sizeof(T)); \
            FA(a, k); FB(b, k); FC(c, k); \
            const int ab = memcmp(a, b, n * sizeof(T)) != 0, ac = memcmp(a, c, n * sizeof(T)) != 0; \
            printf("I type=%s k=%d amp=%d %s_vs_%s=%s %s_vs_%s=%s\n", #T, k, amp, NAMEB, NAMEA, ab ? "DIFFERENT" : "bit-identical", \
                   NAMEC, NAMEA, ac ? "DIFFERENT" : "bit-identical"); \
            bad += ab + ac; \
            free(src); free(a); free(b); free(c); \
        } \
        return bad; \
    }

IDENT(float, f, "T", wht_f_T, "G19", wht_f_G19, "G19a", wht_f_G19a, k <= 12 ? 7 : 1)
IDENT(double, d, "T", wht_d_T, "G19", wht_d_G19, "G19a", wht_d_G19a, 1000)
IDENT(int32_t, i, "T", wht_i_T, "G19s", wht_i_G19, "G19a", wht_i_G19a, k <= 20 ? 1000 : 15)
IDENT(int32_t, s, "T", wht_i_T, "sT", wht_s_T, "sG19", wht_s_G19, k <= 20 ? 1000 : 15)

static double draw(int kind)
{
    if (kind == 0) return 2.0 * unif() - 1.0;
    const int e = (int)(rnd() % 41) - 20;
    const double m = ldexp(1.0 + unif(), e);
    return (rnd() & 1) ? -m : m;
}

/* float data, truth in double (a double carries 29 more bits than a float: its own rounding
 * error is 2^-29 of a float's and is not seen below) */
static void arbitrary_f(int k, int kind)
{
    const size_t n = (size_t)1 << k;
    float *src = alloc(n * 4), *t = alloc(n * 4), *g = alloc(n * 4), *a = alloc(n * 4);
    double *ref = alloc(n * 8);
    for (size_t i = 0; i < n; i++) { src[i] = (float)draw(kind); ref[i] = (double)src[i]; }
    memcpy(t, src, n * 4); memcpy(g, src, n * 4); memcpy(a, src, n * 4);
    wht_f_T(t, k); wht_f_G19(g, k); wht_f_G19a(a, k);
    for (size_t s = 1; s < n; s *= 2)
        for (size_t b = 0; b < n; b += 2 * s)
            for (size_t i = 0; i < s; i++) { const double u = ref[b + i], v = ref[b + i + s]; ref[b + i] = u + v; ref[b + i + s] = u - v; }
    double rms = 0, et = 0, eg = 0, ea = 0, mt = 0, mg = 0, ma = 0, dgt = 0, dat = 0, relgt = 0;
    size_t ngt = 0, nat = 0;
    for (size_t i = 0; i < n; i++) {
        rms += ref[i] * ref[i];
        const double dt = t[i] - ref[i], dg = g[i] - ref[i], da = a[i] - ref[i];
        et += dt * dt; eg += dg * dg; ea += da * da;
        if (fabs(dt) > mt) mt = fabs(dt);
        if (fabs(dg) > mg) mg = fabs(dg);
        if (fabs(da) > ma) ma = fabs(da);
        const double d1 = fabs((double)g[i] - (double)t[i]), d2 = fabs((double)a[i] - (double)t[i]);
        if (d1 > dgt) dgt = d1;
        if (d2 > dat) dat = d2;
        if (g[i] != t[i]) ngt++;
        if (a[i] != t[i]) nat++;
        if (t[i] != 0 && d1 / fabs((double)t[i]) > relgt) relgt = d1 / fabs((double)t[i]);
    }
    rms = sqrt(rms / (double)n);
    printf("A type=float k=%d input=%s rms_of_output=%.4g | error against the true value, in units of that rms: "
           "T rms %.3g max %.3g; G19 rms %.3g max %.3g; G19a rms %.3g max %.3g | G19 against T: %zu of %zu numbers differ, "
           "largest difference %.3g of the rms, largest difference relative to the number itself %.3g | G19a against T: %zu differ, largest %.3g of the rms\n",
           k, kind ? "wide" : "uniform", rms, sqrt(et / (double)n) / rms, mt / rms, sqrt(eg / (double)n) / rms, mg / rms,
           sqrt(ea / (double)n) / rms, ma / rms, ngt, n, dgt / rms, relgt, nat, dat / rms);
    free(src); free(t); free(g); free(a); free(ref);
}

static void arbitrary_d(int k, int kind)
{
    const size_t n = (size_t)1 << k;
    double *src = alloc(n * 8), *t = alloc(n * 8), *g = alloc(n * 8), *a = alloc(n * 8);
    __float128 *ref = alloc(n * 16);
    for (size_t i = 0; i < n; i++) { src[i] = draw(kind); ref[i] = (__float128)src[i]; }
    memcpy(t, src, n * 8); memcpy(g, src, n * 8); memcpy(a, src, n * 8);
    wht_d_T(t, k); wht_d_G19(g, k); wht_d_G19a(a, k);
    for (size_t s = 1; s < n; s *= 2)
        for (size_t b = 0; b < n; b += 2 * s)
            for (size_t i = 0; i < s; i++) { const __float128 u = ref[b + i], v = ref[b + i + s]; ref[b + i] = u + v; ref[b + i + s] = u - v; }
    double rms = 0, et = 0, eg = 0, ea = 0, mt = 0, mg = 0, ma = 0, dgt = 0, dat = 0, relgt = 0;
    size_t ngt = 0, nat = 0;
    for (size_t i = 0; i < n; i++) {
        const double r = (double)ref[i];
        rms += r * r;
        const double dt = (double)((__float128)t[i] - ref[i]), dg = (double)((__float128)g[i] - ref[i]), da = (double)((__float128)a[i] - ref[i]);
        et += dt * dt; eg += dg * dg; ea += da * da;
        if (fabs(dt) > mt) mt = fabs(dt);
        if (fabs(dg) > mg) mg = fabs(dg);
        if (fabs(da) > ma) ma = fabs(da);
        const double d1 = fabs(g[i] - t[i]), d2 = fabs(a[i] - t[i]);
        if (d1 > dgt) dgt = d1;
        if (d2 > dat) dat = d2;
        if (g[i] != t[i]) ngt++;
        if (a[i] != t[i]) nat++;
        if (t[i] != 0 && d1 / fabs(t[i]) > relgt) relgt = d1 / fabs(t[i]);
    }
    rms = sqrt(rms / (double)n);
    printf("A type=double k=%d input=%s rms_of_output=%.4g | error against the true value, in units of that rms: "
           "T rms %.3g max %.3g; G19 rms %.3g max %.3g; G19a rms %.3g max %.3g | G19 against T: %zu of %zu numbers differ, "
           "largest difference %.3g of the rms, largest difference relative to the number itself %.3g | G19a against T: %zu differ, largest %.3g of the rms\n",
           k, kind ? "wide" : "uniform", rms, sqrt(et / (double)n) / rms, mt / rms, sqrt(eg / (double)n) / rms, mg / rms,
           sqrt(ea / (double)n) / rms, ma / rms, ngt, n, dgt / rms, relgt, nat, dat / rms);
    free(src); free(t); free(g); free(a); free(ref);
}

int main(int argc, char **argv)
{
    const int kident = argc > 1 ? atoi(argv[1]) : 24;
    const int karb = argc > 2 ? atoi(argv[2]) : 18;
    int bad = ident_f(kident) + ident_d(kident) + ident_i(kident) + ident_s(kident);
    printf("# bit-identity: %s (%d comparisons differ)\n", bad ? "FAILED" : "all bit-identical", bad);
    for (int kind = 0; kind < 2; kind++)
        for (int k = 3; k <= karb; k += 3) { arbitrary_f(k, kind); arbitrary_d(k, kind); }
    return bad ? 1 : 0;
}
