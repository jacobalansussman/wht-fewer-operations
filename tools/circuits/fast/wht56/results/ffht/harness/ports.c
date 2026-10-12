/* ports.c -- how many vector additions (multiplications, multiply-adds) per cycle can this core do?
 *
 *   taskset -c CPU ./ports [REPEATS]
 *
 * Why: FFHT's passes are mostly vaddps / vsubps.  If the core can start only one of them per cycle,
 * the number of additions is the bottleneck and a kernel with fewer additions gains its full share;
 * a kernel that turns additions into multiply-adds would gain more than its share, for a reason
 * that has nothing to do with the number of operations.  If the core can start two per cycle,
 * neither holds.  This program measures it instead of trusting a table.
 *
 * Each test is a loop of 12 instructions of one kind on 12 different registers (so they do not wait
 * for each other inside a turn; from one turn to the next each register waits for its own previous
 * result, which is 3 to 5 cycles and less than the 6 or 12 cycles a turn needs).  Beside it the
 * loop of cpufreq.c, which takes one cycle per turn, gives the length of a cycle in the same
 * repeat.  Printed: cycles per turn, and instructions per cycle = 12 / that.  One per cycle means
 * one unit for that kind of instruction, two per cycle means two.
 *
 * The numbers in the registers are all zero: no overflow, no denormal number.
 *
 * Build: gcc -O2 -mavx2 -mfma ports.c -o ports
 */
#define _GNU_SOURCE
#include <sched.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

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
        __asm__ volatile("" : "+r"(x));
    }
    return x;
}

#define CLOBBER "ymm0", "ymm1", "ymm2", "ymm3", "ymm4", "ymm5", "ymm6", "ymm7", "ymm8", "ymm9", "ymm10", "ymm11", "ymm12", "cc"
#define ZERO13 \
    "vxorps %%ymm0,%%ymm0,%%ymm0\n vxorps %%ymm1,%%ymm1,%%ymm1\n vxorps %%ymm2,%%ymm2,%%ymm2\n" \
    "vxorps %%ymm3,%%ymm3,%%ymm3\n vxorps %%ymm4,%%ymm4,%%ymm4\n vxorps %%ymm5,%%ymm5,%%ymm5\n" \
    "vxorps %%ymm6,%%ymm6,%%ymm6\n vxorps %%ymm7,%%ymm7,%%ymm7\n vxorps %%ymm8,%%ymm8,%%ymm8\n" \
    "vxorps %%ymm9,%%ymm9,%%ymm9\n vxorps %%ymm10,%%ymm10,%%ymm10\n vxorps %%ymm11,%%ymm11,%%ymm11\n" \
    "vxorps %%ymm12,%%ymm12,%%ymm12\n"
#define TWELVE(op) \
    op " %%ymm12,%%ymm0,%%ymm0\n" op " %%ymm12,%%ymm1,%%ymm1\n" op " %%ymm12,%%ymm2,%%ymm2\n" \
    op " %%ymm12,%%ymm3,%%ymm3\n" op " %%ymm12,%%ymm4,%%ymm4\n" op " %%ymm12,%%ymm5,%%ymm5\n" \
    op " %%ymm12,%%ymm6,%%ymm6\n" op " %%ymm12,%%ymm7,%%ymm7\n" op " %%ymm12,%%ymm8,%%ymm8\n" \
    op " %%ymm12,%%ymm9,%%ymm9\n" op " %%ymm12,%%ymm10,%%ymm10\n" op " %%ymm12,%%ymm11,%%ymm11\n"
#define LOOP(name, op) \
    static __attribute__((noinline)) void name(uint64_t n) \
    { \
        __asm__ volatile(ZERO13 "1:\n" TWELVE(op) "dec %0\n jnz 1b\n vzeroupper\n" : "+r"(n) : : CLOBBER); \
    }

LOOP(loop_add, "vaddps")
LOOP(loop_sub, "vsubps")
LOOP(loop_mul, "vmulps")
LOOP(loop_fma, "vfmadd231ps")          /* ymm_i = ymm_i + ymm12 * ymm_i */
LOOP(loop_addpd, "vaddpd")

typedef void (*loop_fn)(uint64_t);

int main(int argc, char **argv)
{
    const int repeats = argc > 1 ? atoi(argv[1]) : 9;
    const uint64_t nchain = 200000000ull, nloop = 20000000ull;
    static const struct { const char *name; loop_fn f; } tests[] = {
        {"vaddps", loop_add}, {"vsubps", loop_sub}, {"vaddpd", loop_addpd}, {"vmulps", loop_mul}, {"vfmadd231ps", loop_fma},
    };
    const int nt = (int)(sizeof tests / sizeof tests[0]);
    volatile uint64_t sink = 0;
    double best[8];
    printf("# ports: processor %d; %d repeats; each test: %llu turns of 12 instructions\n", sched_getcpu(), repeats, (unsigned long long)nloop);
    sink += chain(nchain);
    for (int t = 0; t < nt; t++) { tests[t].f(nloop / 10); best[t] = 1e30; }
    for (int r = 0; r < repeats; r++) {
        for (int t = 0; t < nt; t++) {
            double t0 = now();
            sink += chain(nchain);
            const double cyc_a = (now() - t0) / (double)nchain;      /* seconds per cycle, before */
            t0 = now();
            tests[t].f(nloop);
            const double per_turn = (now() - t0) / (double)nloop;
            t0 = now();
            sink += chain(nchain);
            const double cyc_b = (now() - t0) / (double)nchain;      /* and after */
            const double cyc = cyc_a < cyc_b ? cyc_a : cyc_b;
            const double c = per_turn / cyc;
            printf("P repeat=%d test=%s ns_per_turn=%.4f ns_per_cycle=%.4f (before %.4f, after %.4f) cycles_per_turn=%.3f instructions_per_cycle=%.3f\n",
                   r, tests[t].name, per_turn * 1e9, cyc * 1e9, cyc_a * 1e9, cyc_b * 1e9, c, 12.0 / c);
            if (c < best[t]) best[t] = c;
        }
    }
    for (int t = 0; t < nt; t++)
        printf("P best test=%s cycles_per_turn=%.3f instructions_per_cycle=%.3f\n", tests[t].name, best[t], 12.0 / best[t]);
    return 0;
}
