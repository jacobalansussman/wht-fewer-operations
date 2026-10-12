/* uports.c -- what this core does with vector additions, multiplications and multiply-adds.
 *
 *   taskset -c CPU ./uports [REPEATS]
 *
 * The unit is the cycle, and the cycle is measured inside the same process and the same repeat
 * by a loop whose turn is a chain of 24 "add $1,%rax": each waits for the one before, one cycle
 * each, so one turn is 24 cycles.  (The loop counter and the jump run beside the chain.)
 *
 *   chain24        that loop alone: gives the length of a cycle
 *   chain24+4add   the same chain with 4 vaddps beside it: still 24 cycles a turn if the core
 *                  does not slow its clock when 256-bit instructions run
 *   tp_*           24 instructions that do not wait for each other: cycles per turn; 24 / that =
 *                  how many of them the core starts per cycle
 *   lat_*          a chain of 12 of one kind on one register: cycles per turn / 12 = the latency
 *
 * All numbers in the registers are zero.
 * Build: gcc -O2 -mavx2 -mfma uports.c -o uports
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

#define CLOB "rax", "ymm0", "ymm1", "ymm2", "ymm3", "ymm4", "ymm5", "ymm6", "ymm7", "ymm8", "ymm9", "ymm10", "ymm11", "ymm12", "ymm13", "ymm14", "ymm15", "cc"
#define Z(r) "vxorps %%ymm" #r ",%%ymm" #r ",%%ymm" #r "\n"
#define ZERO Z(0) Z(1) Z(2) Z(3) Z(4) Z(5) Z(6) Z(7) Z(8) Z(9) Z(10) Z(11) Z(12) Z(13) Z(14) Z(15) "xor %%eax,%%eax\n"
#define A1 "add $1,%%rax\n"
#define A24 A1 A1 A1 A1 A1 A1 A1 A1 A1 A1 A1 A1 A1 A1 A1 A1 A1 A1 A1 A1 A1 A1 A1 A1
/* independent: target r from ymm14 and ymm15, which nobody writes */
#define I(op, r) op " %%ymm15,%%ymm14,%%ymm" #r "\n"
#define I12(op) I(op, 0) I(op, 1) I(op, 2) I(op, 3) I(op, 4) I(op, 5) I(op, 6) I(op, 7) I(op, 8) I(op, 9) I(op, 10) I(op, 11)
/* a multiply-add reads its target; 12 targets, each used twice a turn */
#define F12 I("vfmadd231ps", 0) I("vfmadd231ps", 1) I("vfmadd231ps", 2) I("vfmadd231ps", 3) I("vfmadd231ps", 4) I("vfmadd231ps", 5) \
            I("vfmadd231ps", 6) I("vfmadd231ps", 7) I("vfmadd231ps", 8) I("vfmadd231ps", 9) I("vfmadd231ps", 10) I("vfmadd231ps", 11)
#define SH(r) "vpermilps $0xb1,%%ymm14,%%ymm" #r "\n"
#define SH12 SH(0) SH(1) SH(2) SH(3) SH(4) SH(5) SH(6) SH(7) SH(8) SH(9) SH(10) SH(11)
#define C(op) op " %%ymm15,%%ymm0,%%ymm0\n"
#define C12(op) C(op) C(op) C(op) C(op) C(op) C(op) C(op) C(op) C(op) C(op) C(op) C(op)
#define CF "vfmadd231ps %%ymm15,%%ymm14,%%ymm0\n"          /* ymm0 = ymm0 + ymm14*ymm15: through the sum */
#define CF12 CF CF CF CF CF CF CF CF CF CF CF CF
#define CG "vfmadd132ps %%ymm15,%%ymm14,%%ymm0\n"          /* ymm0 = ymm0*ymm15 + ymm14: through the factor */
#define CG12 CG CG CG CG CG CG CG CG CG CG CG CG

#define LOOP(name, body) \
    static __attribute__((noinline)) void name(uint64_t n) \
    { \
        __asm__ volatile(ZERO ".p2align 6\n1:\n" body "dec %0\n jnz 1b\n vzeroupper\n" : "+r"(n) : : CLOB); \
    }

LOOP(l_chain, A24)
LOOP(l_chain_add, A24 I("vaddps", 0) I("vaddps", 1) I("vaddps", 2) I("vaddps", 3))
LOOP(l_tp_add, I12("vaddps") I12("vsubps"))
LOOP(l_tp_addpd, I12("vaddpd") I12("vsubpd"))
LOOP(l_tp_mul, I12("vmulps") I12("vmulps"))
LOOP(l_tp_fma, F12 F12)
LOOP(l_tp_add_fma, I12("vaddps") F12)
LOOP(l_tp_add_mul, I12("vaddps") I12("vmulps"))
LOOP(l_tp_shuf, SH12 SH12)
LOOP(l_tp_xor, I12("vxorps") I12("vxorps"))
LOOP(l_tp_add_shuf, I12("vaddps") SH12)
LOOP(l_lat_add, C12("vaddps"))
LOOP(l_lat_mul, C12("vmulps"))
LOOP(l_lat_fma_sum, CF12)
LOOP(l_lat_fma_factor, CG12)

typedef void (*loop_fn)(uint64_t);
static const struct { const char *name; loop_fn f; int ins; const char *what; } tests[] = {
    {"chain24+4add", l_chain_add, 0, "the 24-cycle chain with 4 vaddps beside it"},
    {"tp_add", l_tp_add, 24, "12 vaddps + 12 vsubps, independent"},
    {"tp_addpd", l_tp_addpd, 24, "12 vaddpd + 12 vsubpd, independent"},
    {"tp_mul", l_tp_mul, 24, "24 vmulps, independent"},
    {"tp_fma", l_tp_fma, 24, "24 vfmadd231ps on 12 registers"},
    {"tp_add_fma", l_tp_add_fma, 24, "12 vaddps + 12 vfmadd231ps"},
    {"tp_add_mul", l_tp_add_mul, 24, "12 vaddps + 12 vmulps"},
    {"tp_shuf", l_tp_shuf, 24, "24 vpermilps, independent"},
    {"tp_xor", l_tp_xor, 24, "24 vxorps, independent"},
    {"tp_add_shuf", l_tp_add_shuf, 24, "12 vaddps + 12 vpermilps"},
    {"lat_add", l_lat_add, -12, "chain of 12 vaddps"},
    {"lat_mul", l_lat_mul, -12, "chain of 12 vmulps"},
    {"lat_fma_sum", l_lat_fma_sum, -12, "chain of 12 vfmadd231ps through the sum"},
    {"lat_fma_factor", l_lat_fma_factor, -12, "chain of 12 vfmadd132ps through the factor"},
};

int main(int argc, char **argv)
{
    const int repeats = argc > 1 ? atoi(argv[1]) : 9;
    const uint64_t turns = 4000000ull;
    const int nt = (int)(sizeof tests / sizeof tests[0]);
    double best[32], bestcyc = 1e30;
    printf("# uports: processor %d; %d repeats; %llu turns per loop\n", sched_getcpu(), repeats, (unsigned long long)turns);
    for (int t = 0; t < nt; t++) { tests[t].f(turns / 10); best[t] = 1e30; }
    l_chain(turns / 10);
    for (int r = 0; r < repeats; r++) {
        for (int t = 0; t < nt; t++) {
            double t0 = now();
            l_chain(turns);
            const double ca = (now() - t0) / (double)turns / 24.0;
            t0 = now();
            tests[t].f(turns);
            const double per_turn = (now() - t0) / (double)turns;
            t0 = now();
            l_chain(turns);
            const double cb = (now() - t0) / (double)turns / 24.0;
            const double cyc = ca < cb ? ca : cb;
            if (cyc < bestcyc) bestcyc = cyc;
            const double c = per_turn / cyc;
            if (c < best[t]) best[t] = c;
        }
    }
    printf("# shortest cycle seen: %.4f ns (%.2f GHz)\n", bestcyc * 1e9, 1e-9 / bestcyc);
    for (int t = 0; t < nt; t++) {
        if (tests[t].ins > 0)
            printf("U test=%s cycles_per_turn=%.2f per_cycle=%.2f   (%s; best of %d)\n", tests[t].name, best[t], tests[t].ins / best[t], tests[t].what, repeats);
        else if (tests[t].ins < 0)
            printf("U test=%s cycles_per_turn=%.2f latency_cycles=%.2f   (%s; best of %d)\n", tests[t].name, best[t], best[t] / -tests[t].ins, tests[t].what, repeats);
        else
            printf("U test=%s cycles_per_turn=%.2f   (%s; best of %d)\n", tests[t].name, best[t], tests[t].what, repeats);
    }
    return 0;
}
