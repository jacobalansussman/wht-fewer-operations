/* whtc_avx2.c -- the kernel in AVX2 and FMA intrinsics, float and double.
 *
 * It is the timed program's code (measurements/2026-10-22/x86/harness-hybrid): FFHT's plan of passes, with the
 * 8-point step that runs in registers chosen by WHTC_STEP (whtc.h).  The vector macros below are bench_k0.c's for
 * -DXT=0 (256-bit float) and -DXT=2 (256-bit double).  This file compiles to nothing unless WHTC_USE_AVX2 (whtc.h):
 * the portable code in whtc_plain.c then provides the functions.  The other entry points (_oop, _scaled, whtc_step,
 * FFHT's names) are in whtc_plain.c for both cases.
 * Licence: Apache-2.0; the parts named in whtc_ffht_plan.h are FFHT's (MIT, LICENSE-FFHT). */
#include "whtc.h"

#if WHTC_USE_AVX2
#include <stddef.h>
#include <stdlib.h>
#ifdef WHTC_SIMDE /* the same source on a machine without AVX2 (SIMDe emulates the intrinsics): for testing only */
#define SIMDE_ENABLE_NATIVE_ALIASES
#include <simde/x86/avx2.h>
#include <simde/x86/fma.h>
#define OPQ(x) __asm__ volatile("" : : "r"(&(x)) : "memory")
#else
#include <immintrin.h>
#if defined(__AVX512F__)
#define OPQ(x) __asm__ volatile("" : "+v"(x)) /* any of the 32 registers */
#else
#define OPQ(x) __asm__ volatile("" : "+x"(x))
#endif
#endif
#include "whtc_names.h"

/* ---- float: 8 lanes ---- */
#define WHTC_SUFFIX f
#define XT 0
#define ET float
#define V __m256
#define LANES 8
#define LOGL 3
#define LD _mm256_loadu_ps
#define ST _mm256_storeu_ps
#define SET1 _mm256_set1_ps
#define V_ADD _mm256_add_ps
#define V_SUB _mm256_sub_ps
#define FMADD _mm256_fmadd_ps
#define FNMADD _mm256_fnmadd_ps
#define FMSUB _mm256_fmsub_ps
#define MULV _mm256_mul_ps
#include "whtc_impl.h"
#undef WHTC_SUFFIX
#undef XT
#undef ET
#undef V
#undef LANES
#undef LOGL
#undef LD
#undef ST
#undef SET1
#undef V_ADD
#undef V_SUB
#undef FMADD
#undef FNMADD
#undef FMSUB
#undef MULV

/* ---- double: 4 lanes ---- */
#define WHTC_SUFFIX d
#define XT 2
#define ET double
#define V __m256d
#define LANES 4
#define LOGL 2
#define LD _mm256_loadu_pd
#define ST _mm256_storeu_pd
#define SET1 _mm256_set1_pd
#define V_ADD _mm256_add_pd
#define V_SUB _mm256_sub_pd
#define FMADD _mm256_fmadd_pd
#define FNMADD _mm256_fnmadd_pd
#define FMSUB _mm256_fmsub_pd
#define MULV _mm256_mul_pd
#include "whtc_impl.h"

int whtc_fht_float(float *buf, int log_n) {
  if (log_n < 0 || log_n > 30) return 1;
  whtc_run_f(buf, log_n);
  return 0;
}
int whtc_fht_double(double *buf, int log_n) {
  if (log_n < 0 || log_n > 30) return 1;
  whtc_run_d(buf, log_n);
  return 0;
}
#else
typedef int whtc_avx2_not_compiled; /* ISO C wants at least one declaration in a file */
#endif
