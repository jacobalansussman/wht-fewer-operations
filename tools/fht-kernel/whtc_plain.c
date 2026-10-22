/* whtc_plain.c -- the kernel in portable C, and the entry points shared by both kinds of code.
 *
 * The portable code runs the same text as the AVX2 code (whtc_steps.h, whtc_ffht_plan.h) on a vector written as a
 * plain C array of the same number of lanes (8 floats, 4 doubles).  Every operation is the same operation on the
 * same numbers in the same order, so its results equal the AVX2 code's bit for bit (the tests check this).  The
 * in-lane levels, which FFHT does with shuffles, are done here as the textbook's butterflies, which give the same
 * numbers.  The multiply-adds become a product and a sum: the factor is always 1 or 2, so the product is exact and
 * the result is the same as with a fused multiply-add (except within a factor 2 of the largest finite number).
 * This code is not meant to be fast.
 *
 * Always defined here: whtc_plain_fht_float, whtc_plain_fht_double, the _oop and _scaled entry points, whtc_step,
 * and, with WHTC_FFHT_NAMES, FFHT's four names.  whtc_fht_float and whtc_fht_double are defined here only when the
 * AVX2 code is not compiled (whtc.h, WHTC_USE_AVX2).
 * Licence: Apache-2.0; the parts named in whtc_ffht_plan.h are FFHT's (MIT, LICENSE-FFHT). */
#include "whtc.h"

#include <stddef.h>
#include <stdlib.h>
#include <string.h>

#include "whtc_names.h"

/* ---- a vector of N lanes as a plain array, with the operations the steps use ---- */
#define WHTC_DEFVEC(T, N, VT, P)                                                                       \
  typedef struct { T l[N]; } VT;                                                                     \
  static inline VT P##ld(const T *p) { VT r; memcpy(r.l, p, sizeof r.l); return r; }                \
  static inline void P##st(T *p, VT a) { memcpy(p, a.l, sizeof a.l); }                               \
  static inline VT P##set1(T c) { VT r; for (int i = 0; i < N; i++) r.l[i] = c; return r; }         \
  static inline VT P##add(VT a, VT b) { VT r; for (int i = 0; i < N; i++) r.l[i] = a.l[i] + b.l[i]; return r; } \
  static inline VT P##sub(VT a, VT b) { VT r; for (int i = 0; i < N; i++) r.l[i] = a.l[i] - b.l[i]; return r; } \
  /* a*b + c, -(a*b) + c and a*b - c: the forms of _mm256_fmadd, _mm256_fnmadd and _mm256_fmsub */           \
  static inline VT P##fmadd(VT a, VT b, VT c) { VT r; for (int i = 0; i < N; i++) r.l[i] = a.l[i] * b.l[i] + c.l[i]; return r; } \
  static inline VT P##fnmadd(VT a, VT b, VT c) { VT r; for (int i = 0; i < N; i++) r.l[i] = c.l[i] - a.l[i] * b.l[i]; return r; } \
  static inline VT P##fmsub(VT a, VT b, VT c) { VT r; for (int i = 0; i < N; i++) r.l[i] = a.l[i] * b.l[i] - c.l[i]; return r; } \
  /* the in-lane levels: the textbook's butterflies at strides 1, 2, ... N/2, in that order, as FFHT's shuffles do */ \
  static inline VT P##inlane(VT x) {                                                                 \
    for (int h = 1; h < N; h <<= 1)                                                                  \
      for (int i = 0; i < N; i += 2 * h)                                                             \
        for (int j = i; j < i + h; j++) { T a = x.l[j], b = x.l[j + h]; x.l[j] = a + b; x.l[j + h] = a - b; } \
    return x;                                                                                        \
  }
WHTC_DEFVEC(float, 8, whtc_vf, whtc_vf_)
WHTC_DEFVEC(double, 4, whtc_vd, whtc_vd_)

#define OPQ(x) ((void)0)

/* ---- float: 8 lanes, as the AVX2 code ---- */
#define WHTC_SUFFIX f
#define XT 4 /* neither 0 nor 2: ffht_inlane is then inlane_all, the textbook's in-lane levels */
#define ET float
#define V whtc_vf
#define LANES 8
#define LOGL 3
#define LD whtc_vf_ld
#define ST whtc_vf_st
#define SET1 whtc_vf_set1
#define V_ADD whtc_vf_add
#define V_SUB whtc_vf_sub
#define FMADD whtc_vf_fmadd
#define FNMADD whtc_vf_fnmadd
#define FMSUB whtc_vf_fmsub
#define MULV whtc_no_scaling_line /* V_MUL: the steps used here have no scaling line */
static inline whtc_vf inlane_all(whtc_vf x) { return whtc_vf_inlane(x); }
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
#define XT 4
#define ET double
#define V whtc_vd
#define LANES 4
#define LOGL 2
#define LD whtc_vd_ld
#define ST whtc_vd_st
#define SET1 whtc_vd_set1
#define V_ADD whtc_vd_add
#define V_SUB whtc_vd_sub
#define FMADD whtc_vd_fmadd
#define FNMADD whtc_vd_fnmadd
#define FMSUB whtc_vd_fmsub
#define MULV whtc_no_scaling_line
static inline whtc_vd inlane_all(whtc_vd x) { return whtc_vd_inlane(x); }
#include "whtc_impl.h"

/* ---- entry points ---- */
int whtc_plain_fht_float(float *buf, int log_n) {
  if (log_n < 0 || log_n > 30) return 1;
  whtc_run_f(buf, log_n);
  return 0;
}
int whtc_plain_fht_double(double *buf, int log_n) {
  if (log_n < 0 || log_n > 30) return 1;
  whtc_run_d(buf, log_n);
  return 0;
}

#if !WHTC_USE_AVX2
int whtc_fht_float(float *buf, int log_n) { return whtc_plain_fht_float(buf, log_n); }
int whtc_fht_double(double *buf, int log_n) { return whtc_plain_fht_double(buf, log_n); }
#endif

/* FFHT's _oop functions copy, then transform in place.  Here a log_n out of range returns 1 before anything is
 * touched (FFHT computes the copy's size first). */
int whtc_fht_float_oop(float *in, float *out, int log_n) {
  if (log_n < 0 || log_n > 30) return 1;
  if (in != out) memmove(out, in, sizeof(float) << log_n);
  return whtc_fht_float(out, log_n);
}
int whtc_fht_double_oop(double *in, double *out, int log_n) {
  if (log_n < 0 || log_n > 30) return 1;
  if (in != out) memmove(out, in, sizeof(double) << log_n);
  return whtc_fht_double(out, log_n);
}

int whtc_fht_float_scaled(float *buf, int log_n, float scale) {
  int r = whtc_fht_float(buf, log_n);
  if (r == 0 && scale != 1.0f)
    for (size_t i = 0; i < (size_t)1 << log_n; i++) buf[i] *= scale;
  return r;
}
int whtc_fht_double_scaled(double *buf, int log_n, double scale) {
  int r = whtc_fht_double(buf, log_n);
  if (r == 0 && scale != 1.0)
    for (size_t i = 0; i < (size_t)1 << log_n; i++) buf[i] *= scale;
  return r;
}

#if defined(WHTC_BREAK)
#define WHTC_NAME_STEP "g20 (BROKEN COPY, for the test that must fail)"
#else
#define WHTC_NAME_STEP WHTC_STEP_NAME
#endif
const char *whtc_step(void) {
#if WHTC_USE_AVX2 && defined(WHTC_SIMDE)
  return WHTC_NAME_STEP ", AVX2 and FMA through SIMDe (emulated: for testing, not for speed)";
#elif WHTC_USE_AVX2
  return WHTC_NAME_STEP ", AVX2 and FMA";
#else
  return WHTC_NAME_STEP ", portable C";
#endif
}

#ifdef WHTC_FFHT_NAMES
int fht_float(float *buf, int log_n) { return whtc_fht_float(buf, log_n); }
int fht_double(double *buf, int log_n) { return whtc_fht_double(buf, log_n); }
int fht_float_oop(float *in, float *out, int log_n) { return whtc_fht_float_oop(in, out, log_n); }
int fht_double_oop(double *in, double *out, int log_n) { return whtc_fht_double_oop(in, out, log_n); }
#endif
