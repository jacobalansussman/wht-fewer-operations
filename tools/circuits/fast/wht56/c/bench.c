/* bench.c -- check the four C transforms against each other and time them.
 *
 *   ./bench [runs [k1 k2 ...]]        default: 9 runs; sizes 2^9 2^12 2^15 2^18 2^21
 *
 * CHECK.  At every size the four results are compared on one random input (and at sizes up to
 * 2^12 the textbook is compared with the definition, n^2 operations).  The program stops with
 * exit code 1 at the first difference above rounding.
 *
 * TIMING.  One run of one variant: copy the input into the work array and transform it, `reps`
 * times, with `reps` chosen so that a run handles about 2^23 numbers.  The same loop with the
 * copy alone is timed too, and its best time is taken off.  The variants take turns inside each
 * run, so a busy moment of the machine falls on all of them.  Reported: the best run and the
 * median run, in nanoseconds per point (per number of the array, for one whole transform), by
 * the wall clock.  "spread" is (median - best) / best: a measure of how noisy the machine was.
 * "cpu best" is the best run by the processor time of this process, which leaves out the time
 * when the system had given the processor to another job.
 */
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <stdint.h>
#include "wht56.h"

static double now(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return (double)t.tv_sec + 1e-9 * (double)t.tv_nsec;
}

static double cpu(void)
{
    struct timespec t;
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &t);
    return (double)t.tv_sec + 1e-9 * (double)t.tv_nsec;
}

static uint64_t rng_state = 0x9E3779B97F4A7C15ull;
static double rnd(void)
{
    rng_state ^= rng_state << 13;
    rng_state ^= rng_state >> 7;
    rng_state ^= rng_state << 17;
    return (double)(rng_state >> 11) / 9007199254740992.0 * 2.0 - 1.0;
}

static int cmp_double(const void *a, const void *b)
{
    const double x = *(const double *)a, y = *(const double *)b;
    return (x > y) - (x < y);
}

static void copy_only(double *x, size_t n) { (void)x; (void)n; }

typedef void (*fn_t)(double *, size_t);
#define NV 5
static const char *names[NV] = {"copy only", "textbook radix 2", "textbook radix 8", "k8 raw (20 ops)", "k8 exact (20 ops + scale)"};
static fn_t fns[NV];
static volatile double sink;

int main(int argc, char **argv)
{
    int runs = 9;
    int ks[32], nk = 0;
    fns[0] = copy_only; fns[1] = wht56_textbook_r2; fns[2] = wht56_textbook_r8;
    fns[3] = wht56_k8_raw; fns[4] = wht56_k8;
    if (argc > 1) runs = atoi(argv[1]);
    for (int i = 2; i < argc && nk < 32; i++) ks[nk++] = atoi(argv[i]);
    if (nk == 0) { ks[0] = 9; ks[1] = 12; ks[2] = 15; ks[3] = 18; ks[4] = 21; nk = 5; }
    if (runs < 1) runs = 1;
    if (runs > 99) runs = 99;
    for (int q = 0; q < nk; q++)
        if (ks[q] < 0 || ks[q] > 27) {
            fprintf(stderr, "bench: the sizes are 2^k points with k from 0 to 27; got k = %d\n", ks[q]);
            return 2;
        }

    printf("# best of %d runs; nanoseconds per point for one transform; copy time taken off\n", runs);
    printf("%-8s %-28s %10s %10s %8s %10s %8s\n", "points", "variant", "best", "median", "spread", "cpu best", "reps");
    for (int q = 0; q < nk; q++) {
        const int k = ks[q];
        const size_t n = (size_t)1 << k;
        double *src = aligned_alloc(64, n * sizeof(double) < 64 ? 64 : n * sizeof(double));
        double *buf = aligned_alloc(64, n * sizeof(double) < 64 ? 64 : n * sizeof(double));
        double *ref = aligned_alloc(64, n * sizeof(double) < 64 ? 64 : n * sizeof(double));
        if (!src || !buf || !ref) { fprintf(stderr, "no memory\n"); return 2; }
        for (size_t i = 0; i < n; i++) src[i] = rnd();

        /* ---- check ---- */
        memcpy(ref, src, n * sizeof(double));
        wht56_textbook_r2(ref, n);
        const double tol = 1e-12 * (double)n;       /* inputs are below 1 in size; sums below n */
        if (k <= 12) {
            double worst = 0;
            for (size_t j = 0; j < n; j++) {
                double s = 0;
                for (size_t i = 0; i < n; i++)
                    s += (__builtin_popcountll((unsigned long long)(i & j)) & 1) ? -src[i] : src[i];
                if (fabs(s - ref[j]) > worst) worst = fabs(s - ref[j]);
            }
            if (worst > tol) { printf("CHECK FAILED: textbook against the definition, 2^%d: %g\n", k, worst); return 1; }
        }
        for (int v = 2; v < NV; v++) {
            memcpy(buf, src, n * sizeof(double));
            fns[v](buf, n);
            const double f = (v == 3) ? wht56_k8_raw_factor(n) : 1.0;
            double worst = 0;
            for (size_t i = 0; i < n; i++) {
                const double d = fabs(buf[i] - f * ref[i]);
                if (d > worst) worst = d;
            }
            if (worst > tol) { printf("CHECK FAILED: %s at 2^%d: difference %g\n", names[v], k, worst); return 1; }
        }

        /* ---- time ---- */
        size_t reps = ((size_t)1 << 23) / n;
        if (reps < 2) reps = 2;
        double t[NV][99], tc[NV][99];
        for (int r = -1; r < runs; r++) {           /* run -1 is a warm-up and is thrown away */
            for (int v = 0; v < NV; v++) {
                const double t0 = now(), c0 = cpu();
                for (size_t e = 0; e < reps; e++) {
                    memcpy(buf, src, n * sizeof(double));
                    fns[v](buf, n);
                    sink = buf[e & (n - 1)];
                }
                const double t1 = now(), c1 = cpu();
                if (r >= 0) {
                    t[v][r] = (t1 - t0) * 1e9 / ((double)reps * (double)n);
                    tc[v][r] = (c1 - c0) * 1e9 / ((double)reps * (double)n);
                }
            }
        }
        for (int v = 0; v < NV; v++) {
            qsort(t[v], (size_t)runs, sizeof(double), cmp_double);
            qsort(tc[v], (size_t)runs, sizeof(double), cmp_double);
        }
        const double copy = t[0][0], ccopy = tc[0][0];
        for (int v = 0; v < NV; v++) {
            const double best = t[v][0] - (v ? copy : 0.0);
            const double med = t[v][runs / 2] - (v ? copy : 0.0);
            printf("2^%-6d %-28s %10.3f %10.3f %7.0f%% %10.3f %8zu\n", k, names[v], best, med,
                   best > 0 ? 100.0 * (med - best) / best : 0.0, tc[v][0] - (v ? ccopy : 0.0), reps);
        }
        free(src); free(buf); free(ref);
    }
    printf("CHECK OK: the four transforms agree at every size above\n");
    return 0;
}
