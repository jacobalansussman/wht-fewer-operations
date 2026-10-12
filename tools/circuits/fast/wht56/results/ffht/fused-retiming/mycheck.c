/* mycheck.c -- a second exactness check, written separately from the harness.
 * Integer-valued inputs.  k <= 12: exact equality with the O(N^2) definition (64-bit integers).
 * k > 12: exact equality with FFHT on the same input (float, double); int32 against FFHT double. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include "fht.h"
#include "whtf.h"

void O2_wht_f_Tp(float *, int);  void O2_wht_f_G19p(float *, int); void O2_wht_f_G19ap(float *, int);
void GEN_wht_f_Tp(float *, int); void GEN_wht_f_G19p(float *, int); void GEN_wht_f_G19ap(float *, int);
static const struct { const char *name; void (*f)(float *, int); } VF[] = {
    {"T", wht_f_T}, {"G19", wht_f_G19}, {"G19a", wht_f_G19a}, {"Tp", wht_f_Tp}, {"G19p", wht_f_G19p}, {"G19ap", wht_f_G19ap},
    {"Tf", wht_f_Tf}, {"Tfp", wht_f_Tfp},
    {"O2:Tp", O2_wht_f_Tp}, {"O2:G19p", O2_wht_f_G19p}, {"O2:G19ap", O2_wht_f_G19ap},
    {"gen:Tp", GEN_wht_f_Tp}, {"gen:G19p", GEN_wht_f_G19p}, {"gen:G19ap", GEN_wht_f_G19ap} };
static const struct { const char *name; void (*f)(double *, int); } VD[] = {
    {"T", wht_d_T}, {"G19", wht_d_G19}, {"G19a", wht_d_G19a}, {"Tp", wht_d_Tp}, {"G19p", wht_d_G19p}, {"G19ap", wht_d_G19ap},
    {"Tf", wht_d_Tf}, {"Tfp", wht_d_Tfp} };
static const struct { const char *name; void (*f)(int32_t *, int); } VI[] = {
    {"T", wht_i_T}, {"G19s", wht_i_G19}, {"G19a", wht_i_G19a}, {"Tp", wht_i_Tp}, {"G19sp", wht_i_G19p}, {"G19ap", wht_i_G19ap},
    {"sT", wht_s_T}, {"sG19", wht_s_G19} };
#define N_OF(a) ((int)(sizeof a / sizeof a[0]))

static uint64_t S = 88172645463325252ull;
static int rnd(int amp) { S ^= S << 13; S ^= S >> 7; S ^= S << 17; return (int)(S % (uint64_t)(2 * amp + 1)) - amp; }

int main(int argc, char **argv)
{
    const int kmin = argc > 1 ? atoi(argv[1]) : 3, kmax = argc > 2 ? atoi(argv[2]) : 20;
    long bad = 0, done = 0;
    for (int k = kmin; k <= kmax; k++) {
        const size_t n = (size_t)1 << k;
        int32_t *x = malloc(n * sizeof *x); int64_t *ref = malloc(n * sizeof *ref);
        float *f = aligned_alloc(64, n * sizeof *f), *ff = aligned_alloc(64, n * sizeof *ff);
        double *d = aligned_alloc(64, n * sizeof *d), *fd = aligned_alloc(64, n * sizeof *fd);
        int32_t *iv = aligned_alloc(64, n * sizeof *iv);
        for (int trial = 0; trial < 2; trial++) {
            for (int type = 0; type < 3; type++) {
                /* float: sums below 2^23 in size; double: below 2^31; int32: below 2^30 */
                const int amp = type == 0 ? (k <= 19 ? 7 : 3) : type == 1 ? 1000 : 500;
                for (size_t i = 0; i < n; i++) x[i] = rnd(amp);
                if (trial == 1 && k <= 12) { memset(x, 0, n * sizeof *x); x[(size_t)rnd(1000000) % n + 0] = amp; x[n - 1 - ((n / 3) | 1) % n] += -amp; } /* two spikes: order of outputs */
                if (k <= 12) for (size_t j = 0; j < n; j++) { int64_t s = 0; for (size_t i = 0; i < n; i++) s += (__builtin_popcountll(i & j) & 1) ? -(int64_t)x[i] : (int64_t)x[i]; ref[j] = s; }
                /* FFHT on the same input, in the type under test (double for int32) */
                for (size_t i = 0; i < n; i++) { ff[i] = (float)x[i]; fd[i] = (double)x[i]; }
                if (type == 0) fht_float(ff, k); else fht_double(fd, k);
                if (k <= 12) { size_t m = 0; for (size_t j = 0; j < n; j++) m += type == 0 ? ((int64_t)ff[j] != ref[j] || ff[j] != (float)ref[j]) : (fd[j] != (double)ref[j]);
                    done++; if (m) { bad++; printf("FAIL type=%d k=%d FFHT against the definition: %zu wrong\n", type, k, m); } }
                const int nv = type == 0 ? N_OF(VF) : type == 1 ? N_OF(VD) : N_OF(VI);
                for (int v = 0; v < nv; v++) {
                    size_t m = 0; const char *name;
                    if (type == 0) { name = VF[v].name; for (size_t i = 0; i < n; i++) f[i] = (float)x[i]; VF[v].f(f, k);
                        for (size_t j = 0; j < n; j++) m += k <= 12 ? (f[j] != (float)ref[j] || (int64_t)f[j] != ref[j]) : (f[j] != ff[j]); }
                    else if (type == 1) { name = VD[v].name; for (size_t i = 0; i < n; i++) d[i] = (double)x[i]; VD[v].f(d, k);
                        for (size_t j = 0; j < n; j++) m += k <= 12 ? (d[j] != (double)ref[j]) : (d[j] != fd[j]); }
                    else { name = VI[v].name; memcpy(iv, x, n * sizeof *x); VI[v].f(iv, k);
                        for (size_t j = 0; j < n; j++) m += k <= 12 ? ((int64_t)iv[j] != ref[j]) : ((double)iv[j] != fd[j]); }
                    done++;
                    if (m) { bad++; printf("FAIL type=%s k=%d trial=%d variant=%s: %zu of %zu outputs wrong\n", type == 0 ? "float" : type == 1 ? "double" : "int32", k, trial, name, m, n); }
                }
            }
        }
        printf("k=%d checked (%s)\n", k, k <= 12 ? "against the O(N^2) definition" : "against FFHT"); fflush(stdout);
        free(x); free(ref); free(f); free(ff); free(d); free(fd); free(iv);
    }
    printf("RESULT: %ld comparisons, %ld failed\n", done, bad);
    return bad != 0;
}
