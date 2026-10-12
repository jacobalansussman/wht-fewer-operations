/* core.c -- a second look at the processor core: how long one instruction waits for the
 * one before it (a chain on one register), and how many independent ones finish per unit of time
 * (12 separate chains).  Unit: the time of one vpaddd in a chain, which is one clock cycle on Intel cores.
 * A barrier after every instruction stops the compiler from folding them. */
#include <immintrin.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#define BAR(v) __asm__("" : "+x"(v))
#define R12(X) X X X X X X X X X X X X
static volatile unsigned char SINK[32 * 12];
#define KEEP(v, i) memcpy((void *)(SINK + 32 * (i)), &v, 32)
static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + 1e-9 * t.tv_nsec; }
typedef double (*test)(long);
#define CHAIN(name, T, init, cdecl, op) \
    __attribute__((noinline)) static double name(long n) { T x = init; cdecl; BAR(x); const double t = now(); \
        for (long i = 0; i < n; i++) { R12(x = op; BAR(x);) } const double e = now() - t; KEEP(x, 0); return e; }
CHAIN(ch_paddd, __m256i, _mm256_set1_epi32(1), __m256i c = _mm256_set1_epi32(3); BAR(c), _mm256_add_epi32(x, c))
CHAIN(ch_addps, __m256, _mm256_set1_ps(1.0f), __m256 c = _mm256_set1_ps(1.0f); BAR(c), _mm256_add_ps(x, c))
CHAIN(ch_addpd, __m256d, _mm256_set1_pd(1.0), __m256d c = _mm256_set1_pd(1.0); BAR(c), _mm256_add_pd(x, c))
CHAIN(ch_mulps, __m256, _mm256_set1_ps(1.5f), __m256 c = _mm256_set1_ps(1.0f); BAR(c), _mm256_mul_ps(x, c))
CHAIN(ch_fma_addend, __m256, _mm256_set1_ps(1.5f), __m256 c = _mm256_set1_ps(0.0f); __m256 two = _mm256_set1_ps(2.0f); BAR(c); BAR(two), _mm256_fmadd_ps(two, c, x))
CHAIN(ch_fma_factor, __m256, _mm256_set1_ps(1.5f), __m256 c = _mm256_set1_ps(0.0f); __m256 one = _mm256_set1_ps(1.0f); BAR(c); BAR(one), _mm256_fmadd_ps(x, one, c))
CHAIN(ch_fmapd_addend, __m256d, _mm256_set1_pd(1.5), __m256d c = _mm256_set1_pd(0.0); __m256d two = _mm256_set1_pd(2.0); BAR(c); BAR(two), _mm256_fmadd_pd(two, c, x))
#define WIDE(name, T, init, cdecl, OP) \
    __attribute__((noinline)) static double name(long n) { T a0 = init, a1 = init, a2 = init, a3 = init, a4 = init, a5 = init, a6 = init, a7 = init, a8 = init, a9 = init, a10 = init, a11 = init; cdecl; \
        BAR(a0); BAR(a1); BAR(a2); BAR(a3); BAR(a4); BAR(a5); BAR(a6); BAR(a7); BAR(a8); BAR(a9); BAR(a10); BAR(a11); const double t = now(); \
        for (long i = 0; i < n; i++) { OP(a0) OP(a1) OP(a2) OP(a3) OP(a4) OP(a5) OP(a6) OP(a7) OP(a8) OP(a9) OP(a10) OP(a11) } const double e = now() - t; \
        KEEP(a0, 0); KEEP(a1, 1); KEEP(a2, 2); KEEP(a3, 3); KEEP(a4, 4); KEEP(a5, 5); KEEP(a6, 6); KEEP(a7, 7); KEEP(a8, 8); KEEP(a9, 9); KEEP(a10, 10); KEEP(a11, 11); return e; }
#define OPADD(a) a = _mm256_add_ps(a, c); BAR(a);
#define OPFMA(a) a = _mm256_fmadd_ps(two, c, a); BAR(a);
#define OPPADD(a) a = _mm256_add_epi32(a, c); BAR(a);
WIDE(wd_addps, __m256, _mm256_set1_ps(1.0f), __m256 c = _mm256_set1_ps(1.0f); BAR(c), OPADD)
WIDE(wd_fma, __m256, _mm256_set1_ps(1.5f), __m256 c = _mm256_set1_ps(0.0f); __m256 two = _mm256_set1_ps(2.0f); BAR(c); BAR(two), OPFMA)
WIDE(wd_paddd, __m256i, _mm256_set1_epi32(1), __m256i c = _mm256_set1_epi32(3); BAR(c), OPPADD)
static int cmpd(const void *a, const void *b) { double x = *(const double *)a, y = *(const double *)b; return (x > y) - (x < y); }
int main(void)
{
    static const struct { const char *name; test f; const char *what; } T[] = {
        {"chain vpaddd", ch_paddd, "12 in a chain (the unit: 1 cycle each)"},
        {"chain vaddps", ch_addps, "12 in a chain"}, {"chain vaddpd", ch_addpd, "12 in a chain"}, {"chain vmulps", ch_mulps, "12 in a chain"},
        {"chain vfmadd ps, through the number added", ch_fma_addend, "12 in a chain"},
        {"chain vfmadd ps, through a factor", ch_fma_factor, "12 in a chain"},
        {"chain vfmadd pd, through the number added", ch_fmapd_addend, "12 in a chain"},
        {"12 separate chains vaddps", wd_addps, "12 independent per turn"},
        {"12 separate chains vfmadd ps", wd_fma, "12 independent per turn"},
        {"12 separate chains vpaddd", wd_paddd, "12 independent per turn"} };
    const int nt = (int)(sizeof T / sizeof T[0]);
    double best[16], med[16]; long ns[16];
    for (int i = 0; i < nt; i++) { long n = 1000000; double t = T[i].f(n); t = T[i].f(n); ns[i] = (long)(n * 0.21 / t) + 1; }
    static double r[16][9];
    for (int rep = 0; rep < 9; rep++) for (int j = 0; j < nt; j++) { const int i = (j + rep) % nt; r[i][rep] = T[i].f(ns[i]) / (12.0 * ns[i]) * 1e9; }
    for (int i = 0; i < nt; i++) { qsort(r[i], 9, sizeof(double), cmpd); best[i] = r[i][0]; med[i] = r[i][4]; }
    printf("unit: one vpaddd in a chain = %.4f ns best, %.4f ns median (so %.3f GHz if that is one cycle)\n", best[0], med[0], 1.0 / best[0]);
    for (int i = 0; i < nt; i++)
        printf("%-44s %-38s best %.4f ns = %.2f units; median %.4f ns = %.2f units\n", T[i].name, T[i].what, best[i], best[i] / best[0], med[i], med[i] / med[0]);
    return 0;
}
