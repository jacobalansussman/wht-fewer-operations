/* bench_size.c -- benchmark by size, written for this benchmark (added to the snapshot of
 * wht56/c; wht56.c, wht56.h and kernels.h are used unchanged).
 *
 *   ./bench_size [runs [k1 k2 ...]]     default: 9 runs; k = 3 6 9 10 12 15 16 18 20 21 24
 *
 * One array of N = 2^k doubles, held in memory, one thread.  Five loops are timed:
 *   copy        copy the input into the work array, nothing else
 *   r2          copy, then the textbook transform, one address bit per pass
 *   r8          copy, then the textbook transform, three address bits per pass (24 +/- per 8 points)
 *   new_exact   copy, then the 20-operation kernel with the final multiplications (H x exactly)
 *   new_scaled  copy, then the 20-operation kernel without them (H x / 2^floor(k/3))
 * When k is not a multiple of 3, wht56.c does the one or two bits left over first, by textbook
 * radix-2 passes, in r8, new_exact and new_scaled alike.
 *
 * CHECK, before any timing, at every size:
 *   (a) integer-valued input (whole numbers from -1000 to 1000 held in doubles): new_exact, r8 and
 *       new_scaled * 2^floor(k/3) are compared with r2 by exact equality on all N outputs; at
 *       k <= 12 r2 is compared, by exact equality, with the definition summed in 64-bit integers;
 *   (b) real input in (-1, 1): the same comparisons up to rounding (1e-12 * N).
 * The program stops with exit code 1 at the first failure.
 *
 * TIMING.  For each variant the number of repetitions of (copy, transform) is chosen so that one
 * timed loop lasts about 0.30 s (never less than two repetitions).  Then `runs` rounds; in each
 * round every variant is timed once, and the order of the variants turns by one place each round,
 * so that drift of the machine falls on all of them.  Output: one line "ROW" per variant with
 * the minimum, median and maximum over the rounds, in nanoseconds per point INCLUDING the copy
 * (the copy is taken off afterwards, by tables.py), and one line "REP" with every round.
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
static uint64_t rnd64(void)
{
    rng_state ^= rng_state << 13;
    rng_state ^= rng_state >> 7;
    rng_state ^= rng_state << 17;
    return rng_state;
}
static double rnd(void) { return (double)(rnd64() >> 11) / 9007199254740992.0 * 2.0 - 1.0; }

static int cmp_double(const void *a, const void *b)
{
    const double x = *(const double *)a, y = *(const double *)b;
    return (x > y) - (x < y);
}

static void copy_only(double *x, size_t n) { (void)x; (void)n; }

typedef void (*fn_t)(double *, size_t);
#define NV 5
#define MAXRUNS 99
static const char *names[NV] = {"copy", "r2", "r8", "new_exact", "new_scaled"};
static fn_t fns[NV];
static volatile double sink;

static double loop(int v, double *buf, const double *src, size_t n, size_t reps, double *cpu_s)
{
    const double t0 = now(), c0 = cpu();
    for (size_t e = 0; e < reps; e++) {
        memcpy(buf, src, n * sizeof(double));
        fns[v](buf, n);
        sink = buf[e & (n - 1)];
    }
    const double t1 = now(), c1 = cpu();
    *cpu_s = c1 - c0;
    return t1 - t0;
}

int main(int argc, char **argv)
{
    int runs = 9;
    int ks[32], nk = 0;
    const double target = 0.30;   /* 0.25 in the first run; a few loops then came out under 0.2 s */
    fns[0] = copy_only; fns[1] = wht56_textbook_r2; fns[2] = wht56_textbook_r8;
    fns[3] = wht56_k8; fns[4] = wht56_k8_raw;
    if (argc > 1) runs = atoi(argv[1]);
    for (int i = 2; i < argc && nk < 32; i++) ks[nk++] = atoi(argv[i]);
    if (nk == 0) {
        static const int d[11] = {3, 6, 9, 10, 12, 15, 16, 18, 20, 21, 24};
        for (int i = 0; i < 11; i++) ks[nk++] = d[i];
    }
    if (runs < 1) runs = 1;
    if (runs > MAXRUNS) runs = MAXRUNS;
    for (int q = 0; q < nk; q++)
        if (ks[q] < 0 || ks[q] > 27) { fprintf(stderr, "k from 0 to 27; got %d\n", ks[q]); return 2; }

    printf("# bench_size: %d rounds per cell, target %.2f s per timed loop; times in ns per point, copy included\n", runs, target);
    printf("# ROW k N variant reps loop_s_min wall_min wall_median wall_max cpu_min\n");
    for (int q = 0; q < nk; q++) {
        const int k = ks[q];
        const size_t n = (size_t)1 << k;
        const size_t bytes = n * sizeof(double) < 64 ? 64 : n * sizeof(double);
        double *src = aligned_alloc(64, bytes);
        double *buf = aligned_alloc(64, bytes);
        double *ref = aligned_alloc(64, bytes);
        if (!src || !buf || !ref) { fprintf(stderr, "no memory\n"); return 2; }
        const double pow2m = (double)((size_t)1 << (k / 3));

        /* ---- check (a): integer-valued input, exact equality ---- */
        for (size_t i = 0; i < n; i++) src[i] = (double)((long)(rnd64() % 2001u) - 1000);
        memcpy(ref, src, n * sizeof(double));
        wht56_textbook_r2(ref, n);
        double biggest = 0;
        for (size_t i = 0; i < n; i++) if (fabs(ref[i]) > biggest) biggest = fabs(ref[i]);
        int defn = 0;
        if (k <= 12) {
            for (size_t j = 0; j < n; j++) {
                int64_t s = 0;
                for (size_t i = 0; i < n; i++) {
                    const int64_t xi = (int64_t)src[i];
                    s += (__builtin_popcountll((unsigned long long)(i & j)) & 1) ? -xi : xi;
                }
                if ((double)s != ref[j]) { printf("CHECK FAILED: r2 against the definition, k=%d, output %zu\n", k, j); return 1; }
            }
            defn = 1;
        }
        for (int v = 2; v < NV; v++) {
            memcpy(buf, src, n * sizeof(double));
            fns[v](buf, n);
            const double f = (v == 4) ? pow2m : 1.0;      /* times a power of two: exact */
            for (size_t i = 0; i < n; i++)
                if (buf[i] * f != ref[i]) {
                    printf("CHECK FAILED (integer input, exact): %s at k=%d, output %zu: %.17g against %.17g\n",
                           names[v], k, i, buf[i] * f, ref[i]);
                    return 1;
                }
        }
        printf("CHECK k=%d N=%zu integer input: new_exact = r2, r8 = r2, new_scaled*%g = r2, exactly, on all %zu outputs; "
               "r2 = definition in 64-bit integers: %s; largest |output| %.0f\n",
               k, n, pow2m, n, defn ? "yes, all outputs" : "not run (k > 12)", biggest);

        /* ---- check (b): real input, up to rounding ---- */
        for (size_t i = 0; i < n; i++) src[i] = rnd();
        memcpy(ref, src, n * sizeof(double));
        wht56_textbook_r2(ref, n);
        const double tol = 1e-12 * (double)n;
        double worst_all = 0;
        for (int v = 2; v < NV; v++) {
            memcpy(buf, src, n * sizeof(double));
            fns[v](buf, n);
            const double f = (v == 4) ? pow2m : 1.0;
            double worst = 0;
            for (size_t i = 0; i < n; i++) {
                const double d = fabs(buf[i] * f - ref[i]);
                if (d > worst) worst = d;
            }
            if (worst > tol) { printf("CHECK FAILED (real input): %s at k=%d: difference %g\n", names[v], k, worst); return 1; }
            if (worst > worst_all) worst_all = worst;
        }
        printf("CHECK k=%d real input: largest difference from r2 %.3g (allowed %.3g)\n", k, worst_all, tol);

        /* ---- calibrate: repetitions so that one timed loop lasts about `target` seconds ---- */
        size_t reps[NV];
        for (int v = 0; v < NV; v++) {
            size_t r = 2;
            double c, el = loop(v, buf, src, n, r, &c);
            while (el < 0.04 && r < ((size_t)1 << 40)) { r *= 2; el = loop(v, buf, src, n, r, &c); }
            for (int again = 0; again < 2; again++) {   /* the quickest of three: a slow moment must not shorten the loop */
                const double e2 = loop(v, buf, src, n, r, &c);
                if (e2 < el) el = e2;
            }
            double want = (double)r * target / el;
            if (want < 2) want = 2;
            reps[v] = (size_t)ceil(want);
        }

        /* ---- time ---- */
        static double t[NV][MAXRUNS], tc[NV][MAXRUNS], secs[NV][MAXRUNS];
        for (int r = 0; r < runs; r++) {
            for (int j = 0; j < NV; j++) {
                const int v = (j + r) % NV;
                double c;
                const double el = loop(v, buf, src, n, reps[v], &c);
                secs[v][r] = el;
                t[v][r] = el * 1e9 / ((double)reps[v] * (double)n);
                tc[v][r] = c * 1e9 / ((double)reps[v] * (double)n);
            }
        }
        for (int v = 0; v < NV; v++) {
            printf("REP k=%d %s", k, names[v]);
            for (int r = 0; r < runs; r++) printf(" %.4f", t[v][r]);
            printf("\n");
        }
        for (int v = 0; v < NV; v++) {
            qsort(t[v], (size_t)runs, sizeof(double), cmp_double);
            qsort(tc[v], (size_t)runs, sizeof(double), cmp_double);
            qsort(secs[v], (size_t)runs, sizeof(double), cmp_double);
            printf("ROW %d %zu %s %zu %.3f %.4f %.4f %.4f %.4f\n", k, n, names[v], reps[v], secs[v][0],
                   t[v][0], t[v][runs / 2], t[v][runs - 1], tc[v][0]);
        }
        fflush(stdout);
        free(src); free(buf); free(ref);
    }
    printf("CHECK OK: all checks passed at every size above\n");
    return 0;
}
