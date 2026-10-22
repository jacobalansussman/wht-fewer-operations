/* whtc.h -- the Walsh-Hadamard transform with FFHT's entry points, its plan of passes, and this repository's 20-line
 * 8-point step (g20, the 3/4 family's 8-point step) as the step it runs in registers.
 *
 * Every function computes y = H x in place (unnormalised: no division by sqrt(n)) on n = 2^log_n numbers, like
 * FFHT's.  It returns 0 for log_n from 0 to 30 and 1 for any other log_n, without touching the buffers.  log_n = 0
 * leaves the buffer as it is.  The buffers need no alignment.  The functions keep no state and allocate nothing.
 *
 * Which code runs is chosen when the library is compiled:
 *   - AVX2 and FMA code when the compiler targets them (__AVX2__ and __FMA__ defined, e.g. -mavx2 -mfma or
 *     -march=native on a recent x86-64), unless WHTC_PLAIN is defined; also with WHTC_SIMDE, which builds the same
 *     code on any machine through the SIMDe library (for testing only);
 *   - otherwise portable C (whtc_plain.c), which runs the same plan and the same step on plain C arrays and gives
 *     the same results, bit for bit.  It is not meant to be fast.
 *   - The step: -DWHTC_STEP=G20 (default), TB8BALS (the textbook with half its additions as multiply-adds by 1,
 *     written subtraction first) or TB8 (the textbook, FFHT's own 24 additions and subtractions).
 * Compile both .c files of this folder; the one that is not chosen compiles to nothing but the portable names below.
 *
 * Results are the same as FFHT's on whole-number inputs (both are exact there).  On other inputs G20 rounds
 * differently from the textbook (README.md gives the measured differences), so this is not a drop-in where
 * bit-identical output is required.  TB8 and TB8BALS give the textbook's results bit for bit.
 *
 * Licence: Apache-2.0, as the rest of this repository; the lines marked "FFHT" below are FFHT's (MIT, LICENSE-FFHT).
 */
#ifndef WHTC_H
#define WHTC_H

#ifdef __cplusplus
extern "C" {
#endif

#if (defined(__AVX2__) && defined(__FMA__) && !defined(WHTC_PLAIN)) || defined(WHTC_SIMDE)
#define WHTC_USE_AVX2 1
#else
#define WHTC_USE_AVX2 0
#endif

/* FFHT's four signatures and return codes, under this library's names */
int whtc_fht_float(float *buf, int log_n);
int whtc_fht_double(double *buf, int log_n);
int whtc_fht_float_oop(float *in, float *out, int log_n);    /* copies in to out, then transforms out */
int whtc_fht_double_oop(double *in, double *out, int log_n);

/* scale * H x (for example scale = 1/sqrt(n) for the orthonormal transform); one more rounding unless scale is a
 * power of 2 */
int whtc_fht_float_scaled(float *buf, int log_n, float scale);
int whtc_fht_double_scaled(double *buf, int log_n, double scale);

/* which step and which code were compiled in, e.g. "g20, AVX2 and FMA" or "g20, portable C" */
const char *whtc_step(void);

/* the portable code under its own names, always present (the tests compare it with the AVX2 code) */
int whtc_plain_fht_float(float *buf, int log_n);
int whtc_plain_fht_double(double *buf, int log_n);

#ifdef WHTC_FFHT_NAMES
/* With -DWHTC_FFHT_NAMES (when the library is compiled and where this header is included), the library also defines
 * FFHT's own four functions, so that code written for FFHT compiles and links against this library unchanged.
 * Do not link it together with FFHT itself in that case. */
int fht_float(float *buf, int log_n);
int fht_double(double *buf, int log_n);
int fht_float_oop(float *in, float *out, int log_n);
int fht_double_oop(double *in, double *out, int log_n);
#endif

#ifdef __cplusplus
} /* extern "C" */

#ifdef WHTC_FFHT_NAMES
/* FFHT: the C++ overloads of FFHT's fht.h (commit fba727a3), unchanged (MIT, LICENSE-FFHT) */
static inline int fht(float *buf, int log_n) {
    return fht_float(buf, log_n);
}

static inline int fht(double *buf, int log_n) {
    return fht_double(buf, log_n);
}

static inline int fht(float *buf, float *out, int log_n) {
    return fht_float_oop(buf, out, log_n);
}

static inline int fht(double *buf, double *out, int log_n) {
    return fht_double_oop(buf, out, log_n);
}
#endif
#endif

#endif /* WHTC_H */
