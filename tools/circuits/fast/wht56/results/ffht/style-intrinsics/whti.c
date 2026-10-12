/* whti.c -- Walsh-Hadamard transforms with AVX2 intrinsics, in place, 2^k numbers, 3 <= k <= 30,
 * floats and doubles.  Output in natural order.
 *
 * For each number type and each 8-point step (kernels.inc lists them) one function
 *     void whti_<step><style>_<f|d>(T *buf, int k)
 * All of them are ONE text (impl.inc, plans.inc); they differ in the step on 8 registers only.
 *
 * style: how the parts that are NOT the step are written (the same for T and N of a style):
 *   (none)  the levels inside a register with a sign mask: per level one shuffle, one xor with
 *           a constant, one addition (3 instructions; FFHT uses 5 or 6).  Loads as the compiler
 *           likes them (it may use an input straight from memory).
 *   p       the same, and a barrier after the 8 loads of a step, so that all 8 inputs are in
 *           registers before the step starts (FFHT's way).
 *   q       the levels inside a register in FFHT's own sequence of instructions (two shuffles,
 *           0 - x, addsub / blend + add), and the barrier.  The nearest to FFHT in intrinsics.
 *   w       sign-mask levels, done one level at a time over the 8 registers, and the 8-register
 *           passes with the instructions of neighbouring turns staggered (impl.inc, STAGGER;
 *           kernels_w.inc).  Loads as the compiler likes them.
 *   wp      the same with the barrier after the 8 loads.
 *
 * Build: gcc -O3 -march=native -ffp-contract=off   (AVX2 and FMA needed).  -ffp-contract=off
 * matters: without it gcc fuses a multiplication and an addition that follow each other into one
 * instruction on its own, and the steps would not be the steps written in kern.h.
 */
#include <immintrin.h>
#include <stddef.h>
#include <stdint.h>
#include "kern.h"
#include "whti.h"

#define PIN_NONE(v)
#define PIN_REG(v) __asm__("" : "+x"(v))

/* ------------------------------------------------------------------ float ---- */
#define ELT float
#define TSUF f
#define V __m256
#define W 8
#define PLAN_FLOAT
#define LOAD(p) _mm256_loadu_ps(p)
#define STORE(p, v) _mm256_storeu_ps(p, v)
#define ADD(a, b) _mm256_add_ps(a, b)
#define SUB(a, b) _mm256_sub_ps(a, b)
#define MUL(a, b) _mm256_mul_ps(a, b)
#define FMADD(a, b, c) _mm256_fmadd_ps(a, b, c)
#define FMSUB(a, b, c) _mm256_fmsub_ps(a, b, c)
#define FNMADD(a, b, c) _mm256_fnmadd_ps(a, b, c)
#define SET1(c) _mm256_set1_ps(c)

/* sign-mask form: level i = shuffle the partner into place, flip the sign of the upper one, add */
#define INREG_DECL_M \
    const __m256 M0 = _mm256_castsi256_ps(_mm256_setr_epi32(0, INT32_MIN, 0, INT32_MIN, 0, INT32_MIN, 0, INT32_MIN)); \
    const __m256 M1 = _mm256_castsi256_ps(_mm256_setr_epi32(0, 0, INT32_MIN, INT32_MIN, 0, 0, INT32_MIN, INT32_MIN)); \
    const __m256 M2 = _mm256_castsi256_ps(_mm256_setr_epi32(0, 0, 0, 0, INT32_MIN, INT32_MIN, INT32_MIN, INT32_MIN));
#define INREG_M(v) do { \
    v = ADD(_mm256_permute_ps(v, 0xB1), _mm256_xor_ps(v, M0)); \
    v = ADD(_mm256_permute_ps(v, 0x4E), _mm256_xor_ps(v, M1)); \
    v = ADD(_mm256_permute2f128_ps(v, v, 0x01), _mm256_xor_ps(v, M2)); } while (0)
#define INREG_M0(v) v = ADD(_mm256_permute_ps(v, 0xB1), _mm256_xor_ps(v, M0))
#define INREG_M1(v) v = ADD(_mm256_permute_ps(v, 0x4E), _mm256_xor_ps(v, M1))
#define INREG_M2(v) v = ADD(_mm256_permute2f128_ps(v, v, 0x01), _mm256_xor_ps(v, M2))
#define INREG_BY_LEVEL_M(a, b, c, d, e, f, g, h) do { \
    INREG_M0(a); INREG_M0(b); INREG_M0(c); INREG_M0(d); INREG_M0(e); INREG_M0(f); INREG_M0(g); INREG_M0(h); \
    INREG_M1(a); INREG_M1(b); INREG_M1(c); INREG_M1(d); INREG_M1(e); INREG_M1(f); INREG_M1(g); INREG_M1(h); \
    INREG_M2(a); INREG_M2(b); INREG_M2(c); INREG_M2(d); INREG_M2(e); INREG_M2(f); INREG_M2(g); INREG_M2(h); } while (0)
/* FFHT's own sequence (gen.py of FFHT, the three float steps inside a register), in intrinsics */
#define INREG_DECL_Q const __m256 ZERO = _mm256_setzero_ps();
#define INREG_Q(v) do { \
    __m256 p_ = _mm256_permute_ps(v, 0xA0), q_ = _mm256_permute_ps(v, 0xF5); \
    __m256 m_ = SUB(ZERO, q_); \
    v = _mm256_addsub_ps(p_, m_); \
    p_ = _mm256_permute_ps(v, 0x44); q_ = _mm256_permute_ps(v, 0xEE); \
    m_ = SUB(ZERO, q_); \
    v = ADD(p_, _mm256_blend_ps(q_, m_, 0xCC)); \
    m_ = SUB(ZERO, v); \
    p_ = _mm256_permute2f128_ps(v, v, 0x00); q_ = _mm256_permute2f128_ps(v, m_, 0x31); \
    v = ADD(p_, q_); } while (0)

#define STAGGER 0
#define WITH_ORDERS
#define SFX
#define PIN PIN_NONE
#define INREG_DECL INREG_DECL_M
#define INREG INREG_M
#include "kernels.inc"
#undef SFX
#undef PIN
#define SFX p
#define PIN PIN_REG
#include "kernels.inc"
#undef SFX
#undef INREG_DECL
#undef INREG
#undef WITH_ORDERS
#define SFX q
#define INREG_DECL INREG_DECL_Q
#define INREG INREG_Q
#include "kernels.inc"
#undef SFX
#undef PIN
#undef INREG_DECL
#undef INREG
#undef STAGGER

/* the staggered passes (impl.inc, STAGGER): sign-mask levels, one level at a time over the 8 registers */
#define STAGGER 1
#define INREG_DECL INREG_DECL_M
#define INREG INREG_M
#define INREG_BY_LEVEL INREG_BY_LEVEL_M
#define SFX w
#define PIN PIN_NONE
#include "kernels_w.inc"
#undef SFX
#undef PIN
#define SFX wp
#define PIN PIN_REG
#include "kernels_w.inc"
#undef SFX
#undef PIN
#undef INREG_DECL
#undef INREG
#undef INREG_BY_LEVEL
#undef STAGGER

#undef ELT
#undef TSUF
#undef V
#undef W
#undef PLAN_FLOAT
#undef LOAD
#undef STORE
#undef ADD
#undef SUB
#undef MUL
#undef FMADD
#undef FMSUB
#undef FNMADD
#undef SET1
#undef INREG_DECL_M
#undef INREG_M
#undef INREG_M0
#undef INREG_M1
#undef INREG_M2
#undef INREG_BY_LEVEL_M
#undef INREG_DECL_Q
#undef INREG_Q

/* ----------------------------------------------------------------- double ---- */
#define ELT double
#define TSUF d
#define V __m256d
#define W 4
#define PLAN_DOUBLE
#define LOAD(p) _mm256_loadu_pd(p)
#define STORE(p, v) _mm256_storeu_pd(p, v)
#define ADD(a, b) _mm256_add_pd(a, b)
#define SUB(a, b) _mm256_sub_pd(a, b)
#define MUL(a, b) _mm256_mul_pd(a, b)
#define FMADD(a, b, c) _mm256_fmadd_pd(a, b, c)
#define FMSUB(a, b, c) _mm256_fmsub_pd(a, b, c)
#define FNMADD(a, b, c) _mm256_fnmadd_pd(a, b, c)
#define SET1(c) _mm256_set1_pd(c)

#define INREG_DECL_M \
    const __m256d M0 = _mm256_castsi256_pd(_mm256_setr_epi64x(0, INT64_MIN, 0, INT64_MIN)); \
    const __m256d M1 = _mm256_castsi256_pd(_mm256_setr_epi64x(0, 0, INT64_MIN, INT64_MIN));
#define INREG_M(v) do { \
    v = ADD(_mm256_permute_pd(v, 0x5), _mm256_xor_pd(v, M0)); \
    v = ADD(_mm256_permute2f128_pd(v, v, 0x01), _mm256_xor_pd(v, M1)); } while (0)
#define INREG_M0(v) v = ADD(_mm256_permute_pd(v, 0x5), _mm256_xor_pd(v, M0))
#define INREG_M1(v) v = ADD(_mm256_permute2f128_pd(v, v, 0x01), _mm256_xor_pd(v, M1))
#define INREG_BY_LEVEL_M(a, b, c, d, e, f, g, h) do { \
    INREG_M0(a); INREG_M0(b); INREG_M0(c); INREG_M0(d); INREG_M0(e); INREG_M0(f); INREG_M0(g); INREG_M0(h); \
    INREG_M1(a); INREG_M1(b); INREG_M1(c); INREG_M1(d); INREG_M1(e); INREG_M1(f); INREG_M1(g); INREG_M1(h); } while (0)
#define INREG_DECL_Q const __m256d ZERO = _mm256_setzero_pd();
#define INREG_Q(v) do { \
    __m256d p_ = _mm256_permute_pd(v, 0x0), q_ = _mm256_permute_pd(v, 0xF); \
    __m256d m_ = SUB(ZERO, q_); \
    v = _mm256_addsub_pd(p_, m_); \
    p_ = _mm256_permute2f128_pd(v, v, 0x00); \
    m_ = SUB(ZERO, v); \
    q_ = _mm256_permute2f128_pd(v, m_, 0x31); \
    v = ADD(p_, q_); } while (0)

#define STAGGER 0
#define WITH_ORDERS
#define SFX
#define PIN PIN_NONE
#define INREG_DECL INREG_DECL_M
#define INREG INREG_M
#include "kernels.inc"
#undef SFX
#undef PIN
#define SFX p
#define PIN PIN_REG
#include "kernels.inc"
#undef SFX
#undef INREG_DECL
#undef INREG
#undef WITH_ORDERS
#define SFX q
#define INREG_DECL INREG_DECL_Q
#define INREG INREG_Q
#include "kernels.inc"
#undef SFX
#undef PIN
#undef INREG_DECL
#undef INREG
#undef STAGGER

/* the staggered passes (impl.inc, STAGGER): sign-mask levels, one level at a time over the 8 registers */
#define STAGGER 1
#define INREG_DECL INREG_DECL_M
#define INREG INREG_M
#define INREG_BY_LEVEL INREG_BY_LEVEL_M
#define SFX w
#define PIN PIN_NONE
#include "kernels_w.inc"
#undef SFX
#undef PIN
#define SFX wp
#define PIN PIN_REG
#include "kernels_w.inc"
#undef SFX
#undef PIN
#undef INREG_DECL
#undef INREG
#undef INREG_BY_LEVEL
#undef STAGGER

#undef ELT
#undef TSUF
#undef V
#undef W
#undef PLAN_DOUBLE
#undef LOAD
#undef STORE
#undef ADD
#undef SUB
#undef MUL
#undef FMADD
#undef FMSUB
#undef FNMADD
#undef SET1
#undef INREG_DECL_M
#undef INREG_M
#undef INREG_M0
#undef INREG_M1
#undef INREG_M2
#undef INREG_BY_LEVEL_M
#undef INREG_DECL_Q
#undef INREG_Q

#ifndef STEP_ONLY
/* P(k): the number of 8-register passes of the plan of 2^k numbers; the up-to-scale variants
 * return H x / 2^P(k) */
#define PLAN_P_FLOAT
#define PLAN_P_DOUBLE
#include "plans.inc"
int whti_P_f(int k) { return (k >= 0 && k <= 30 && plan_P_float[k] > 0) ? plan_P_float[k] : 0; }
int whti_P_d(int k) { return (k >= 0 && k <= 30 && plan_P_double[k] > 0) ? plan_P_double[k] : 0; }
#endif
