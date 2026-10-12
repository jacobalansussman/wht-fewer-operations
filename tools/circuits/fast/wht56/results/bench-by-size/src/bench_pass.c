/* bench_pass.c -- time ONE 8-point pass, by stride.  A control beside bench_size.c: it shows in which
 * passes the two kernels differ.
 *
 *   ./bench_pass [rounds]            default 9
 *
 * An array of 2,048 doubles (16 kilobytes; with the input copy, 32).  For each stride s in
 * 1, 2, 4, 8, 16, 64, 256 one pass is timed: 8 numbers at a time, at distance s from each other,
 *   t8          the textbook, 24 additions and subtractions
 *   o8          the new kernel, 19 additions and subtractions and one halving
 *   o8_scaled   the new kernel with every output multiplied by a constant as it is stored
 * The function passes8 below is copied word for word from wht56.c (it is `static` there; here it
 * is also marked noinline), and
 * the kernels come from the same kernels.h, so the compiler is given the same text.  It may still
 * arrange the machine code differently here than inside wht56.c; this is a control, not the
 * measurement.  Timing as in bench_size.c: (copy, pass) minus (copy), loops of about 0.1 s, the
 * variants take turns, minimum and median over the rounds, nanoseconds per point for one pass.
 */
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <stdint.h>
#include "kernels.h"

#define ROWS(p, s) (p), (p) + (s), (p) + 2 * (s), (p) + 3 * (s), (p) + 4 * (s), (p) + 5 * (s), (p) + 6 * (s), (p) + 7 * (s)

__attribute__((noinline))            /* the one change to the copied text: keep it a function of its own */
static void passes8(double *x, size_t n, size_t s0, size_t s1, int kind, size_t last_s, double c)
{
    for (size_t s = s0; s < s1; s *= 8) {
        if (kind == 0) {
            if (s == 1)
                for (size_t b = 0; b < n; b += 8) wht56_pass_t8(ROWS(x + b, 1), 1);
            else
                for (size_t b = 0; b < n; b += 8 * s) wht56_pass_t8(ROWS(x + b, s), s);
        } else if (s == last_s) {
            if (s == 1)
                for (size_t b = 0; b < n; b += 8) wht56_pass_o8_scaled(ROWS(x + b, 1), 1, c);
            else
                for (size_t b = 0; b < n; b += 8 * s) wht56_pass_o8_scaled(ROWS(x + b, s), s, c);
        } else {
            if (s == 1)
                for (size_t b = 0; b < n; b += 8) wht56_pass_o8(ROWS(x + b, 1), 1);
            else
                for (size_t b = 0; b < n; b += 8 * s) wht56_pass_o8(ROWS(x + b, s), s);
        }
    }
}

static double now(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return (double)t.tv_sec + 1e-9 * (double)t.tv_nsec;
}

static int cmp_double(const void *a, const void *b)
{
    const double x = *(const double *)a, y = *(const double *)b;
    return (x > y) - (x < y);
}

#define N 2048
#define NV 4
static const char *names[NV] = {"copy", "t8", "o8", "o8_scaled"};
static volatile double sink;
static volatile size_t vstride;          /* read through a volatile: the stride is not a constant for the compiler */

static volatile int vkind[NV] = {0, 0, 1, 1};   /* read through a volatile, so that the compiler keeps ONE general
                                                  * passes8, as it does in wht56.c, and writes no special copy per kernel */

static void one(int v, double *buf, size_t s)
{
    if (v != 0) passes8(buf, N, s, 8 * s, vkind[v], v == 3 ? s : 0, v == 3 ? 2.0 : 1.0);
}

static double loop(int v, double *buf, const double *src, size_t reps)
{
    const size_t s = vstride;
    const double t0 = now();
    for (size_t e = 0; e < reps; e++) {
        memcpy(buf, src, N * sizeof(double));
        one(v, buf, s);
        sink = buf[e & (N - 1)];
    }
    return now() - t0;
}

int main(int argc, char **argv)
{
    int rounds = argc > 1 ? atoi(argv[1]) : 9;
    if (rounds < 1) rounds = 1;
    if (rounds > 99) rounds = 99;
    static const size_t strides[7] = {1, 2, 4, 8, 16, 64, 256};
    double *src = aligned_alloc(64, N * sizeof(double));
    double *buf = aligned_alloc(64, N * sizeof(double));
    double *ref = aligned_alloc(64, N * sizeof(double));
    if (!src || !buf || !ref) return 2;
    for (size_t i = 0; i < N; i++) src[i] = (double)((long)((i * 2654435761u) % 2001u) - 1000);

    printf("# bench_pass: one 8-point pass over %d doubles, %d rounds; ns per point for one pass, copy taken off\n", N, rounds);
    printf("# PASS stride t8_min t8_med o8_min o8_med o8s_min o8s_med  o8/t8  o8s/t8  shortest_loop_s\n");
    for (int q = 0; q < 7; q++) {
        const size_t s = strides[q];
        vstride = s;
        /* check: the new pass is half the textbook pass, exactly, on whole numbers */
        memcpy(ref, src, sizeof(double) * N); one(1, ref, s);
        memcpy(buf, src, sizeof(double) * N); one(2, buf, s);
        for (size_t i = 0; i < N; i++) if (2.0 * buf[i] != ref[i]) { printf("CHECK FAILED o8 stride %zu\n", s); return 1; }
        memcpy(buf, src, sizeof(double) * N); one(3, buf, s);
        for (size_t i = 0; i < N; i++) if (buf[i] != ref[i]) { printf("CHECK FAILED o8_scaled stride %zu\n", s); return 1; }

        size_t reps[NV];
        double t[NV][99], shortest = 1e9;
        for (int v = 0; v < NV; v++) {
            size_t r = 16;
            double el = loop(v, buf, src, r);
            while (el < 0.02) { r *= 2; el = loop(v, buf, src, r); }
            for (int again = 0; again < 2; again++) { const double e2 = loop(v, buf, src, r); if (e2 < el) el = e2; }
            reps[v] = (size_t)ceil((double)r * 0.12 / el);
        }
        for (int r = 0; r < rounds; r++)
            for (int j = 0; j < NV; j++) {
                const int v = (j + r) % NV;
                const double el = loop(v, buf, src, reps[v]);
                if (el < shortest) shortest = el;
                t[v][r] = el * 1e9 / ((double)reps[v] * (double)N);
            }
        for (int v = 0; v < NV; v++) qsort(t[v], (size_t)rounds, sizeof(double), cmp_double);
        const double c0 = t[0][0], c1 = t[0][rounds / 2];
        printf("PASS %zu %.4f %.4f %.4f %.4f %.4f %.4f  %.3f  %.3f  %.3f\n", s,
               t[1][0] - c0, t[1][rounds / 2] - c1, t[2][0] - c0, t[2][rounds / 2] - c1, t[3][0] - c0, t[3][rounds / 2] - c1,
               (t[2][0] - c0) / (t[1][0] - c0), (t[3][0] - c0) / (t[1][0] - c0), shortest);
        fflush(stdout);
    }
    (void)names;
    printf("CHECK OK: at every stride the new pass gave half the textbook pass, exactly\n");
    return 0;
}
