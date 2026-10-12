/* kloop_main.c -- time one pass of 8 registers and 3 levels, alone, for every kernel.
 *
 *   taskset -c CPU ./kloop [REPEATS] [SECONDS]        (through harness/locked_run.sh)
 *
 * The passes are in kloop_passes.c (written by kloop_gen.py from the patched generator).  For
 * each type and each array size: the kernels take turns; REPEATS repeats (default 15) of a loop
 * of SECONDS (default 0.25).  A loop is: copy the input back, run the pass 16 times on the same
 * array (16 passes multiply the numbers by at most 8^16, far inside the range of a float), and
 * again.  The copy (2 or 16 KiB) is inside the timed loop for every kernel alike, and the line
 * "copy" gives its cost: the same loop with a function that does nothing.
 *
 * Output per kernel: nanoseconds per block of 8 registers (best, median, worst), and the same in
 * processor cycles, with the cycle length measured in this program before and after each size:
 * a loop of 2^27 dependent integer additions, one cycle per turn.
 *
 * Two rules, added after the first run (out/kloop-1.txt), in which another process on the same
 * core spoiled two of the four sizes:
 *   - a loop shorter than 0.2 s is not counted: it is made longer and run again ("redone");
 *   - cycle_ok=0 marks a size whose two measurements of the cycle differ by more than 5 % or
 *     are longer than 0.40 ns (the core ran at 0.375 to 0.380 ns per cycle whenever it was
 *     undisturbed): its cycle counts are not usable.
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "kloop_list.inc"

static double now(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return (double)t.tv_sec + 1e-9 * (double)t.tv_nsec;
}

/* nanoseconds per processor cycle: a chain of additions, one cycle each */
static double ns_per_cycle(void)
{
    double best = 1e30;
    for (int rep = 0; rep < 5; rep++) {
        unsigned long x = (unsigned long)rep, n = 1ul << 27;
        const double t0 = now();
        for (unsigned long i = 0; i < n; i++) { x += i; __asm__ volatile("" : "+r"(x)); }
        const double t = (now() - t0) * 1e9 / (double)n;
        if (t < best) best = t;
        if (x == 42) puts("");
    }
    return best;
}

static int cmp(const void *a, const void *b)
{
    const double x = *(const double *)a, y = *(const double *)b;
    return (x > y) - (x < y);
}

void kloop_nothing_f(float *buf);
void kloop_nothing_d(double *buf);

#define RUN(T, SUF, LIST, NOTHING, W)                                                            \
static void run_##SUF(int repeats, double secs)                                                  \
{                                                                                                \
    const int total = (int)(sizeof LIST / sizeof LIST[0]);                                       \
    int sizes[8], ns = 0;                                                                        \
    for (int i = 0; i < total; i++) {                                                            \
        int seen = 0;                                                                            \
        for (int j = 0; j < ns; j++) if (sizes[j] == LIST[i].log_n) seen = 1;                    \
        if (!seen) sizes[ns++] = LIST[i].log_n;                                                  \
    }                                                                                            \
    for (int s = 0; s < ns; s++) {                                                               \
        const int L = sizes[s];                                                                  \
        const size_t n = (size_t)1 << L, bytes = n * sizeof(T);                                  \
        const double blocks = (double)n / (8.0 * W);                                             \
        T *src = aligned_alloc(64, bytes), *buf = aligned_alloc(64, bytes);                      \
        unsigned long long st = 88172645463325252ull + (unsigned long long)L;                    \
        for (size_t i = 0; i < n; i++) { st ^= st << 13; st ^= st >> 7; st ^= st << 17;          \
                                         src[i] = (T)((int)((st >> 20) % 3) - 1); }              \
        void (*fn[16])(T *); const char *nm[16]; int nv = 0;                                     \
        for (int i = 0; i < total; i++) if (LIST[i].log_n == L) { fn[nv] = LIST[i].f; nm[nv++] = LIST[i].kernel; } \
        fn[nv] = NOTHING; nm[nv] = "copy";                                                       \
        const double cyc0 = ns_per_cycle();                                                      \
        static double tt[16][128];                                                               \
        long G[16];                                                                              \
        double shortest = 1e30;                                                                  \
        int redone = 0;                                                                          \
        for (int a = 0; a <= nv; a++) {              /* calibration and warm-up */               \
            long g = 64;                                                                         \
            for (;;) {                                                                           \
                const double t0 = now();                                                         \
                for (long i = 0; i < g; i++) { memcpy(buf, src, bytes); for (int r = 0; r < 16; r++) fn[a](buf); } \
                const double t = now() - t0;                                                     \
                if (t >= 0.05) { G[a] = (long)(1.15 * secs * (double)g / t) + 1; break; }          \
                g *= 2;                                                                          \
            }                                                                                    \
        }                                                                                        \
        for (int r = 0; r < repeats; r++)                                                        \
            for (int q = 0; q <= nv; q++) {                                                      \
                const int a = (q + r) % (nv + 1);                                                \
                double t;                                                                        \
                /* a loop counts only from 0.2 s: if the calibration was slowed by another       \
                 * process the loop comes out too short; make it longer and run it again */      \
                for (int tries = 0;; tries++) {                                                  \
                    const double t0 = now();                                                     \
                    for (long i = 0; i < G[a]; i++) { memcpy(buf, src, bytes); for (int k = 0; k < 16; k++) fn[a](buf); } \
                    t = now() - t0;                                                              \
                    if (t >= 0.2 || tries >= 20) break;                                          \
                    G[a] = (long)((double)G[a] * 1.15 * secs / (t > 1e-9 ? t : 1e-9)) + 1;       \
                    redone++;                                                                    \
                }                                                                                \
                if (t < shortest) shortest = t;                                                  \
                tt[a][r] = t * 1e9 / ((double)G[a] * 16.0 * blocks);                             \
            }                                                                                    \
        const double cyc1 = ns_per_cycle();                                                      \
        const double cyc = cyc0 < cyc1 ? cyc0 : cyc1;                                            \
        for (int a = 0; a <= nv; a++) qsort(tt[a], (size_t)repeats, sizeof(double), cmp);        \
        const double copy = tt[nv][0];                                                           \
        for (int a = 0; a <= nv; a++)                                                            \
            printf("K type=%s log_n=%d bytes=%zu kernel=%s ns_per_block_min=%.3f med=%.3f max=%.3f "  \
                   "net_min=%.3f cycles_per_block_net_min=%.2f net_med=%.2f ns_per_cycle=%.4f (%.4f before, %.4f after) " \
                   "repeats=%d shortest_loop_s=%.3f redone=%d cycle_ok=%d\n",                    \
                   #T, L, bytes, nm[a], tt[a][0], tt[a][repeats / 2], tt[a][repeats - 1],        \
                   a == nv ? 0.0 : tt[a][0] - copy, a == nv ? 0.0 : (tt[a][0] - copy) / cyc,     \
                   a == nv ? 0.0 : (tt[a][repeats / 2] - copy) / cyc, cyc, cyc0, cyc1, repeats, shortest, redone, \
                   (cyc0 < 1.05 * cyc1 && cyc1 < 1.05 * cyc0 && cyc < 0.40) ? 1 : 0);              \
        fflush(stdout);                                                                          \
        free(src); free(buf);                                                                    \
    }                                                                                            \
}

RUN(float, f, list_float, kloop_nothing_f, 8)
RUN(double, d, list_double, kloop_nothing_d, 4)

int main(int argc, char **argv)
{
    const int repeats = argc > 1 ? atoi(argv[1]) : 15;
    const double secs = argc > 2 ? atof(argv[2]) : 0.25;
    if (repeats < 1 || repeats > 127) return 2;
    char when[64];
    time_t t = time(NULL);
    strftime(when, sizeof when, "%Y-%m-%d %H:%M:%S UTC", gmtime(&t));
    printf("# kloop: %s; gcc %s; %d repeats; a loop aims at %.2f s x 1.15\n", when, __VERSION__, repeats, secs);
    run_f(repeats, secs);
    run_d(repeats, secs);
    printf("# done\n");
    return 0;
}
