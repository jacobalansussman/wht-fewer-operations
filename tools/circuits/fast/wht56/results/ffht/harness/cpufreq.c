/* cpufreq.c -- how fast does the processor core really run?
 *
 *   taskset -c CPU ./cpufreq [REPEATS]
 *
 * The name of the processor says 2.20 GHz, but a core can run faster than its name (turbo).  To
 * turn a time into processor cycles one needs the real number.  This program times a loop that
 * takes one cycle per turn on this kind of processor: each turn adds to a number that the next
 * turn needs, and ends in one jump.  Turns per nanosecond is then the frequency of the core in
 * GHz.  (If something slows the loop down the figure comes out too low, never too high.)  It also
 * prints the frequency of the time-stamp counter, which is the nominal frequency.
 *
 * Build: gcc -O2 cpufreq.c -o cpufreq
 */
#define _GNU_SOURCE
#include <sched.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <x86intrin.h>

static double now(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return (double)t.tv_sec + 1e-9 * (double)t.tv_nsec;
}

static __attribute__((noinline)) uint64_t chain(uint64_t n)
{
    uint64_t x = 0;
    for (uint64_t i = 0; i < n; i++) {
        x += i;
        __asm__ volatile("" : "+r"(x));      /* the compiler must keep the loop as it is */
    }
    return x;
}

int main(int argc, char **argv)
{
    const int repeats = argc > 1 ? atoi(argv[1]) : 9;
    const uint64_t n = 400000000ull;            /* about 0.12 to 0.2 seconds */
    volatile uint64_t sink = 0;
    double best = 0, worst = 1e30;
    printf("# cpufreq: processor %d; %d repeats of %llu turns\n", sched_getcpu(), repeats, (unsigned long long)n);
    sink += chain(n);                           /* warm up */
    for (int r = 0; r < repeats; r++) {
        const uint64_t c0 = __rdtsc();
        const double t0 = now();
        sink += chain(n);
        const double t1 = now();
        const uint64_t c1 = __rdtsc();
        const double ghz = (double)n / ((t1 - t0) * 1e9);
        const double tsc = (double)(c1 - c0) / ((t1 - t0) * 1e9);
        printf("F repeat=%d seconds=%.4f turns_per_ns=%.4f tsc_ticks_per_ns=%.4f\n", r, t1 - t0, ghz, tsc);
        if (ghz > best) best = ghz;
        if (ghz < worst) worst = ghz;
    }
    printf("F best_turns_per_ns=%.4f worst=%.4f  (the core ran at about %.2f GHz at its best)\n", best, worst, best);
    return 0;
}
