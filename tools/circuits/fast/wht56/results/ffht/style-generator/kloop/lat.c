/* lat.c -- how many cycles does this core need before the result of a vector addition (a
 * multiplication, a multiply-add) can be used by the next instruction?
 *
 *   taskset -c CPU ./lat [REPEATS]
 *
 * Why: the 20-operation block has fewer instructions than the textbook block but its longest
 * chain is 7 operations where the textbook's is 3.  How long a chain takes is (operations on
 * it) x (this number).  This program measures the number instead of trusting a table.
 *
 * Each test is a loop of 12 instructions of one kind in which every instruction needs the
 * result of the one before it (all write ymm0 and read ymm0).  Beside it a loop of integer
 * additions that takes one cycle per turn gives the length of a cycle.  Printed: cycles per
 * instruction.  The numbers are 1.0, +0.0 and x1.0: nothing overflows, nothing is denormal.
 *
 * Build: gcc -O2 -mavx2 -mfma lat.c -o lat
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

static const float one[8] __attribute__((aligned(32))) = {1, 1, 1, 1, 1, 1, 1, 1};

#define TWELVE(op) op op op op op op op op op op op op
/* ymm0 = 1.0 (the chain), ymm1 = 0.0, ymm2 = 1.0 */
#define LOOP(name, op) \
    static __attribute__((noinline)) void name(uint64_t n) \
    { \
        __asm__ volatile("vmovaps %1, %%ymm0\n vmovaps %1, %%ymm2\n vxorps %%ymm1, %%ymm1, %%ymm1\n" \
                         "1:\n" TWELVE(op) "dec %0\n jnz 1b\n vzeroupper\n" \
                         : "+r"(n) : "m"(one) : "ymm0", "ymm1", "ymm2", "cc"); \
    }

LOOP(loop_add, "vaddps %%ymm1, %%ymm0, %%ymm0\n")
LOOP(loop_sub, "vsubps %%ymm1, %%ymm0, %%ymm0\n")
LOOP(loop_addpd, "vaddpd %%ymm1, %%ymm0, %%ymm0\n")
LOOP(loop_mul, "vmulps %%ymm2, %%ymm0, %%ymm0\n")
LOOP(loop_fma_mul, "vfmadd132ps %%ymm2, %%ymm1, %%ymm0\n")      /* ymm0 = ymm0 * 1 + 0: chain through the factor */
LOOP(loop_fma_add, "vfmadd231ps %%ymm2, %%ymm1, %%ymm0\n")      /* ymm0 = 0 * 1 + ymm0: chain through the addend */

typedef void (*loop_fn)(uint64_t);

int main(int argc, char **argv)
{
    const int repeats = argc > 1 ? atoi(argv[1]) : 9;
    const uint64_t nchain = 100000000ull, nloop = 5000000ull;
    static const struct { const char *name; loop_fn f; } tests[] = {
        {"vaddps", loop_add}, {"vsubps", loop_sub}, {"vaddpd", loop_addpd}, {"vmulps", loop_mul},
        {"vfmadd132ps(through-the-factor)", loop_fma_mul}, {"vfmadd231ps(through-the-addend)", loop_fma_add},
    };
    const int nt = (int)(sizeof tests / sizeof tests[0]);
    volatile uint64_t sink = 0;
    double best[8], bestcyc = 1e30;
    printf("# lat: processor %d; %d repeats; each test: %llu turns of 12 dependent instructions\n",
           sched_getcpu(), repeats, (unsigned long long)nloop);
    sink += chain(nchain);
    for (int t = 0; t < nt; t++) { tests[t].f(nloop / 10); best[t] = 1e30; }
    for (int r = 0; r < repeats; r++) {
        for (int t = 0; t < nt; t++) {
            double t0 = now();
            sink += chain(nchain);
            const double cyc_a = (now() - t0) / (double)nchain;
            t0 = now();
            tests[t].f(nloop);
            const double per_ins = (now() - t0) / (double)nloop / 12.0;
            t0 = now();
            sink += chain(nchain);
            const double cyc_b = (now() - t0) / (double)nchain;
            const double cyc = cyc_a < cyc_b ? cyc_a : cyc_b;
            printf("L repeat=%d test=%s ns_per_instruction=%.4f ns_per_cycle=%.4f cycles_per_instruction=%.3f\n",
                   r, tests[t].name, per_ins * 1e9, cyc * 1e9, per_ins / cyc);
            if (per_ins / cyc < best[t]) best[t] = per_ins / cyc;
            if (cyc < bestcyc) bestcyc = cyc;
        }
    }
    for (int t = 0; t < nt; t++)
        printf("L best test=%s cycles_per_instruction=%.3f\n", tests[t].name, best[t]);
    printf("L best ns_per_cycle=%.4f (%.3f GHz)\n", bestcyc * 1e9, 1e-9 / bestcyc);
    return 0;
}
