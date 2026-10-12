/* uarch.c -- what this core does with the instructions of the two steps: how many it starts per
 * cycle (throughput) and how long one takes (latency).  Measured, to set beside the published tables.
 *
 *   taskset -c CPU ./uarch [REPEATS]
 *
 * Throughput tests: a loop of independent instructions.  Additions and shifts are written
 * "op ymm12, ymm12, ymmN": the result does not depend on any earlier result.  A fused
 * multiply-add needs its target as an input, so the 12 of a turn go to 12 different registers and
 * each waits only for its own result of the turn before (5 cycles, less than a turn).
 * Latency tests: 12 instructions in a chain on one register; cycles per turn / 12 = latency.
 * The length of a cycle is measured in the same repeat by a loop that takes one cycle per turn
 * (the method of ../harness/cpufreq.c and ports.c).  All numbers in the registers are zero.
 *
 * Build: gcc -O2 -mavx2 -mfma uarch.c -o uarch
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

#define CLOBBER "ymm0", "ymm1", "ymm2", "ymm3", "ymm4", "ymm5", "ymm6", "ymm7", "ymm8", "ymm9", "ymm10", "ymm11", "ymm12", "ymm13", "ymm14", "ymm15", "cc"
#define Z(r) "vxorps %%ymm" #r ",%%ymm" #r ",%%ymm" #r "\n"
#define ZERO Z(0) Z(1) Z(2) Z(3) Z(4) Z(5) Z(6) Z(7) Z(8) Z(9) Z(10) Z(11) Z(12) Z(13) Z(14) Z(15)
/* independent: target N from ymm12 alone */
#define I1(op, r) op " %%ymm12,%%ymm12,%%ymm" #r "\n"
#define I12(op) I1(op, 0) I1(op, 1) I1(op, 2) I1(op, 3) I1(op, 4) I1(op, 5) I1(op, 6) I1(op, 7) I1(op, 8) I1(op, 9) I1(op, 10) I1(op, 11)
#define I7(op) I1(op, 13) I1(op, 14) I1(op, 15) I1(op, 13) I1(op, 14) I1(op, 15) I1(op, 13)
/* fused multiply-add on 12 different targets */
#define F1(op, r) op " %%ymm12,%%ymm12,%%ymm" #r "\n"
#define F12(op) F1(op, 0) F1(op, 1) F1(op, 2) F1(op, 3) F1(op, 4) F1(op, 5) F1(op, 6) F1(op, 7) F1(op, 8) F1(op, 9) F1(op, 10) F1(op, 11)
/* shift by one: target N from ymm12 */
#define S1(r) "vpslld $1,%%ymm12,%%ymm" #r "\n"
#define S12 S1(0) S1(1) S1(2) S1(3) S1(4) S1(5) S1(6) S1(7) S1(8) S1(9) S1(10) S1(11)
/* chains on ymm0 */
#define C1(op) op " %%ymm12,%%ymm0,%%ymm0\n"
#define C12(op) C1(op) C1(op) C1(op) C1(op) C1(op) C1(op) C1(op) C1(op) C1(op) C1(op) C1(op) C1(op)
#define CS1 "vpslld $1,%%ymm0,%%ymm0\n"
#define CS12 CS1 CS1 CS1 CS1 CS1 CS1 CS1 CS1 CS1 CS1 CS1 CS1
#define CM1 "vfmadd132ps %%ymm12,%%ymm11,%%ymm0\n"       /* ymm0 = ymm0 * ymm12 + ymm11 */
#define CM12 CM1 CM1 CM1 CM1 CM1 CM1 CM1 CM1 CM1 CM1 CM1 CM1

#define LOOP(name, body) \
    static __attribute__((noinline)) void name(uint64_t n) \
    { \
        __asm__ volatile(ZERO "1:\n" body "dec %0\n jnz 1b\n vzeroupper\n" : "+r"(n) : : CLOBBER); \
    }

LOOP(tp_add12, I12("vaddps"))
LOOP(tp_addpd12, I12("vaddpd"))
LOOP(tp_mul12, I12("vmulps"))
LOOP(tp_fma12, F12("vfmadd231ps"))
LOOP(tp_fmapd12, F12("vfnmadd231pd"))
LOOP(tp_add24, I12("vaddps") I12("vsubps"))                       /* the textbook step's arithmetic */
LOOP(tp_mix19, I7("vaddps") F12("vfmadd231ps"))                   /* form G, fused */
LOOP(tp_add31, I12("vaddps") I12("vsubps") I7("vaddps"))          /* form G, two additions per line */
LOOP(tp_paddd12, I12("vpaddd"))
LOOP(tp_pslld12, S12)
LOOP(tp_paddd24, I12("vpaddd") I12("vpsubd"))
LOOP(tp_int19s, I7("vpaddd") I12("vpaddd") S12)                   /* form G, shift and add: 19 adds + 12 shifts */
LOOP(tp_paddd31, I12("vpaddd") I12("vpsubd") I7("vpaddd"))
LOOP(lat_add, C12("vaddps"))
LOOP(lat_addpd, C12("vaddpd"))
LOOP(lat_mul, C12("vmulps"))
#define CA1 "vfmadd231ps %%ymm12,%%ymm11,%%ymm0\n"       /* ymm0 = ymm0 + ymm11 * ymm12 */
#define CA12 CA1 CA1 CA1 CA1 CA1 CA1 CA1 CA1 CA1 CA1 CA1 CA1
LOOP(lat_fma_addend, CA12)
LOOP(lat_fma_factor, CM12)
LOOP(lat_paddd, C12("vpaddd"))
LOOP(lat_pslld, CS12)

typedef void (*loop_fn)(uint64_t);

int main(int argc, char **argv)
{
    const int repeats = argc > 1 ? atoi(argv[1]) : 9;
    const uint64_t nchain = 100000000ull, nloop = 10000000ull;
    static const struct { const char *name; loop_fn f; int ninstr; const char *what; } tests[] = {
        {"tp_vaddps_x12", tp_add12, 12, "12 independent vaddps"},
        {"tp_vaddpd_x12", tp_addpd12, 12, "12 independent vaddpd"},
        {"tp_vmulps_x12", tp_mul12, 12, "12 independent vmulps"},
        {"tp_vfmadd231ps_x12", tp_fma12, 12, "12 vfmadd231ps on 12 registers"},
        {"tp_vfnmadd231pd_x12", tp_fmapd12, 12, "12 vfnmadd231pd on 12 registers"},
        {"tp_T_24add", tp_add24, 24, "textbook step: 12 vaddps + 12 vsubps"},
        {"tp_G19_7add_12fma", tp_mix19, 19, "form G fused: 7 vaddps + 12 vfmadd231ps"},
        {"tp_G19a_31add", tp_add31, 31, "form G two additions: 31 vaddps/vsubps"},
        {"tp_vpaddd_x12", tp_paddd12, 12, "12 independent vpaddd"},
        {"tp_vpslld_x12", tp_pslld12, 12, "12 independent vpslld by 1"},
        {"tp_iT_24add", tp_paddd24, 24, "int textbook step: 12 vpaddd + 12 vpsubd"},
        {"tp_iG19s_19add_12shift", tp_int19s, 31, "int form G: 19 vpaddd + 12 vpslld"},
        {"tp_iG19a_31add", tp_paddd31, 31, "int form G two additions: 31 vpaddd/vpsubd"},
        {"lat_vaddps", lat_add, 12, "chain of 12 vaddps"},
        {"lat_vaddpd", lat_addpd, 12, "chain of 12 vaddpd"},
        {"lat_vmulps", lat_mul, 12, "chain of 12 vmulps"},
        {"lat_vfmadd231ps", lat_fma_addend, 12, "chain of 12 vfmadd231ps through the sum"},
        {"lat_vfmadd132ps", lat_fma_factor, 12, "chain of 12 vfmadd132ps through the factor"},
        {"lat_vpaddd", lat_paddd, 12, "chain of 12 vpaddd"},
        {"lat_vpslld", lat_pslld, 12, "chain of 12 vpslld"},
    };
    const int nt = (int)(sizeof tests / sizeof tests[0]);
    volatile uint64_t sink = 0;
    double best[32], after[32];
    printf("# uarch: processor %d; %d repeats; each test: %llu turns\n", sched_getcpu(), repeats, (unsigned long long)nloop);
    sink += chain(nchain);
    for (int t = 0; t < nt; t++) { tests[t].f(nloop / 10); best[t] = 1e30; after[t] = 1e30; }
    /* The best time of each test and the best time of the one-cycle loop are taken separately,
     * each over all repeats: another program on the hyper-thread sibling slows the one-cycle loop
     * by about 2 and a latency chain not at all, so a ratio taken inside one repeat can come out
     * far too small.  The frequency is taken as constant between the best moments. */
    double fbest = 1e30;
    for (int r = 0; r < repeats; r++) {
        for (int t = 0; t < nt; t++) {
            double t0 = now();
            sink += chain(nchain);
            const double cyc = (now() - t0) / (double)nchain;
            if (cyc < fbest) fbest = cyc;
            t0 = now();
            tests[t].f(nloop);
            const double per_turn = (now() - t0) / (double)nloop;
            if (per_turn < best[t]) best[t] = per_turn;
            /* the one-cycle loop for 0.1 ms right after the test: does the core run slower just
             * after this kind of instruction (a lower frequency for wide multiply-adds)? */
            t0 = now();
            sink += chain(300000);
            const double ca = (now() - t0) / 300000.0;
            if (ca < after[t]) after[t] = ca;
        }
    }
    printf("# shortest cycle seen: %.4f ns (%.3f GHz)\n", fbest * 1e9, 1e-9 / fbest);
    for (int t = 0; t < nt; t++) {
        const double c = best[t] / fbest;
        printf("U test=%s instructions=%d ns_per_turn=%.4f cycles_per_turn=%.2f cycles_per_instruction=%.3f instructions_per_cycle=%.2f cycle_ns_right_after=%.4f   (%s; best of %d)\n",
               tests[t].name, tests[t].ninstr, best[t] * 1e9, c, c / tests[t].ninstr, tests[t].ninstr / c, after[t] * 1e9, tests[t].what, repeats);
    }
    return 0;
}
