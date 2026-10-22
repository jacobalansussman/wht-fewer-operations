/* bench_whtc.c -- time the kernel against FFHT (run by ../bench.sh; x86-64 with AVX2 and FMA).
 *
 *     bench_whtc same|separate L...
 *
 * Programs, all in this one process, taking turns (the timing protocol of the measurements of 22 October 2026:
 * bench.h, at least 9 repeats of at least 0.2 s each, the starting program rotating every round): FFHT (linked from
 * its own fht.c, built with the same compiler and flags), and this library built three times, with the 8-point
 * steps g20, tb8balS and tb8 (bench.sh renames each build's two functions).  Prints the RESULT lines of bench.h and
 * one RATIO line per program: its median time / the median time of the fastest of FFHT, tb8balS and tb8.
 * With -DWHTC_NO_FFHT (a smoke test on a machine without x86) FFHT is left out.
 */
#include "bench.h" /* from measurements/2026-10-22/x86/harness-hybrid */

int G20_fht_float(float *buf, int log_n);
int G20_fht_double(double *buf, int log_n);
int TB8BALS_fht_float(float *buf, int log_n);
int TB8BALS_fht_double(double *buf, int log_n);
int TB8_fht_float(float *buf, int log_n);
int TB8_fht_double(double *buf, int log_n);
#ifndef WHTC_NO_FFHT
#include "fht.h"
#endif

#ifndef PREC_DOUBLE
typedef float ET;
#define PNAME "float"
#define CALL(f) f##_fht_float
#define FFHT_CALL fht_float
#else
typedef double ET;
#define PNAME "double"
#define CALL(f) f##_fht_double
#define FFHT_CALL fht_double
#endif

typedef int (*fn)(ET *, int);
static const struct { const char *name; fn f; int rival; } P[] = {
#ifndef WHTC_NO_FFHT
    {"FFHT", FFHT_CALL, 1},
#endif
    {"whtc-tb8", CALL(TB8), 1},
    {"whtc-tb8balS", CALL(TB8BALS), 1},
    {"whtc-g20", CALL(G20), 0},
};
#define NP (int)(sizeof P / sizeof P[0])

typedef struct { int L, p; bench_pool pool; ET *init; } ctx;
static void c_reset(void *v) {
  ctx *c = v;
  for (int i = 0; i < c->pool.count; i++) memcpy(c->pool.buf[i], c->init, ((size_t)1 << c->L) * sizeof(ET));
}
static void c_run(void *v, long i) { ctx *c = v; P[c->p].f(bench_pool_get(&c->pool, i), c->L); }

int main(int argc, char **argv) {
  bench_init();
  if (argc < 3) { fprintf(stderr, "usage: %s same|separate L...\n", argv[0]); return 2; }
  int mode = !strcmp(argv[1], "separate") ? BENCH_SEPARATE : BENCH_SAME;
  printf("# bench_whtc %s, compiler %s\n", PNAME, __VERSION__);
  for (int a = 2; a < argc; a++) {
    int L = atoi(argv[a]);
    size_t n = (size_t)1 << L;
    /* exactness first: every program on whole numbers equals the double reference */
    ET *x = bench_alloc(n * sizeof(ET));
    double *r = malloc(n * sizeof(double));
    int ok = 1;
    for (int p = 0; p < NP; p++) {
      for (size_t i = 0; i < n; i++) { x[i] = (ET)((int)(i * 2654435761u >> 7) % 9 - 4); r[i] = x[i]; }
      P[p].f(x, L);
      bench_ref_wht_d(r, L);
      for (size_t i = 0; i < n; i++) ok &= (double)x[i] == r[i];
    }
    free(r);
    if (!ok) { printf("CHECK 2^%d: a program is not exact: nothing timed\n", L); return 1; }
    ET *init = x;
    for (size_t i = 0; i < n; i++) init[i] = (ET)bench_rand_pm1();
    ctx c[NP];
    bench_prog bp[NP];
    for (int p = 0; p < NP; p++) {
      c[p] = (ctx){L, p, {0}, init};
      bench_pool_init(&c[p].pool, n * sizeof(ET), mode);
      bp[p] = (bench_prog){P[p].name, c_run, c_reset, &c[p]};
    }
    bench_opts o = BENCH_OPTS_DEFAULT;
    o.units = (double)n;
    char t[96];
    snprintf(t, sizeof t, "whtc %s 2^%d %s", PNAME, L, mode ? "separate" : "same");
    bench_stat st[NP];
    bench_compare(t, bp, NP, &o, st);
    int br = -1;
    for (int p = 0; p < NP; p++)
      if (P[p].rival && (br < 0 || st[p].median < st[br].median)) br = p;
    for (int p = 0; p < NP; p++)
      printf("RATIO %s %s / fastest rival %s: median %.4f best %.4f\n", t, P[p].name, P[br].name,
             st[p].median / st[br].median, st[p].best / st[br].best);
    for (int p = 0; p < NP; p++) bench_pool_free(&c[p].pool);
    free(init);
  }
  return 0;
}
