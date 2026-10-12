/* whtf.c -- Walsh-Hadamard transforms with AVX2 + FMA intrinsics, in place, 2^k numbers, k >= 3.
 *
 * For each number type (f = float, d = double, i = int32) three functions that differ ONLY in
 * the step that combines 8 registers (KERNEL); the plan of the passes and the levels inside a
 * register are one text (impl.inc):
 *
 *   wht_X_T     textbook step: 24 additions and subtractions
 *   wht_X_G19   form G (h8_19gates.txt): 7 additions/subtractions, then 12 lines a + 2b, a - 2b, 2b - a
 *                 float, double: each line ONE fused multiply-add with a register holding 2.0
 *                                (vfmadd, vfnmadd, vfmsub): 19 arithmetic instructions
 *                 int32:         each line a shift left by one and an add/sub: 31 instructions
 *   wht_X_G19a  form G with each of the 12 lines done as two additions/subtractions, a + b + b:
 *               31 instructions, no multiplier.  The control for what the fused instruction buys.
 *   wht_X_Tf    (float, double) the textbook step with each of its 24 additions written as a fused
 *               multiply-add by 1.0: the control for what the KIND of instruction costs.
 *
 * Each of the nine exists twice: as the compiler makes it from the intrinsics (no suffix), and
 * with a barrier after the 8 loads of a step that makes the compiler keep each loaded number in a
 * register (suffix p).  Without the barrier gcc 13 reads some inputs from memory two or three
 * times instead of keeping them (see NOTES.md).
 *
 * Output: H x exactly, natural order, no scaling, in every function.
 *
 * Build: gcc -O3 -march=native -fno-tree-reassoc (needs AVX2 and FMA; -fno-tree-reassoc: without it
 * gcc regroups the integer sums and the integer steps come out longer than written).
 * BASEMAX_4 / BASEMAX_8: log2 of the largest block of 4-byte / 8-byte numbers that is finished
 * before the next one is touched.
 */
#include <immintrin.h>
#include <stddef.h>
#include <stdint.h>
#include "kern.h"
#include "whtf.h"

#ifndef BASEMAX_4
#define BASEMAX_4 12        /* 2^12 floats or int32 = 16 KiB */
#endif
#ifndef BASEMAX_8
#define BASEMAX_8 11        /* 2^11 doubles = 16 KiB */
#endif

/* ------------------------------------------------------------------ float ---- */
#define PFX wht_f_
#define ELT float
#define V __m256
#define W 8
#define LW 3
#define BASEMAX BASEMAX_4
#define LOAD(p) _mm256_loadu_ps(p)
#define STORE(p, v) _mm256_storeu_ps(p, v)
#define ADD(a, b) _mm256_add_ps(a, b)
#define SUB(a, b) _mm256_sub_ps(a, b)
/* a level inside a register: bring the partner into place, change the sign of the lower of the
 * two (a sign-bit flip), add.  3 instructions per level and register. */
#define IDECL \
    const __m256 M0 = _mm256_castsi256_ps(_mm256_setr_epi32(0, INT32_MIN, 0, INT32_MIN, 0, INT32_MIN, 0, INT32_MIN)); \
    const __m256 M1 = _mm256_castsi256_ps(_mm256_setr_epi32(0, 0, INT32_MIN, INT32_MIN, 0, 0, INT32_MIN, INT32_MIN)); \
    const __m256 M2 = _mm256_castsi256_ps(_mm256_setr_epi32(0, 0, 0, 0, INT32_MIN, INT32_MIN, INT32_MIN, INT32_MIN));
#define INREG(v) do { \
    v = ADD(_mm256_permute_ps(v, 0xB1), _mm256_xor_ps(v, M0)); \
    v = ADD(_mm256_permute_ps(v, 0x4E), _mm256_xor_ps(v, M1)); \
    v = ADD(_mm256_permute2f128_ps(v, v, 0x01), _mm256_xor_ps(v, M2)); } while (0)
#define FKDECL const __m256 TWO = _mm256_set1_ps(2.0f);
#define FPL2(a, b) _mm256_fmadd_ps(TWO, b, a)       /* a + 2b */
#define FMI2(a, b) _mm256_fnmadd_ps(TWO, b, a)      /* a - 2b */
#define FRS2(a, b) _mm256_fmsub_ps(TWO, b, a)       /* 2b - a */
#define FONE_DECL const __m256 ONE = _mm256_set1_ps(1.0f);
#define FA(a, b) _mm256_fmadd_ps(ONE, b, a)        /* a + 1.0 b: the control Tf */
#define FS(a, b) _mm256_fnmadd_ps(ONE, b, a)       /* a - 1.0 b */

#define PIN(v)
#define SFX
#include "three.inc"
#undef PIN
#undef SFX
#define PIN(v) __asm__("" : "+x"(v))
#define SFX p
#include "three.inc"
#undef PIN
#undef SFX

#undef PFX
#undef ELT
#undef V
#undef W
#undef LW
#undef BASEMAX
#undef LOAD
#undef STORE
#undef ADD
#undef SUB
#undef IDECL
#undef INREG
#undef FKDECL
#undef FPL2
#undef FMI2
#undef FRS2
#ifdef FONE_DECL
#undef FONE_DECL
#undef FA
#undef FS
#endif

/* ----------------------------------------------------------------- double ---- */
#define PFX wht_d_
#define ELT double
#define V __m256d
#define W 4
#define LW 2
#define BASEMAX BASEMAX_8
#define LOAD(p) _mm256_loadu_pd(p)
#define STORE(p, v) _mm256_storeu_pd(p, v)
#define ADD(a, b) _mm256_add_pd(a, b)
#define SUB(a, b) _mm256_sub_pd(a, b)
#define IDECL \
    const __m256d M0 = _mm256_castsi256_pd(_mm256_setr_epi64x(0, INT64_MIN, 0, INT64_MIN)); \
    const __m256d M1 = _mm256_castsi256_pd(_mm256_setr_epi64x(0, 0, INT64_MIN, INT64_MIN));
#define INREG(v) do { \
    v = ADD(_mm256_permute_pd(v, 0x5), _mm256_xor_pd(v, M0)); \
    v = ADD(_mm256_permute2f128_pd(v, v, 0x01), _mm256_xor_pd(v, M1)); } while (0)
#define FKDECL const __m256d TWO = _mm256_set1_pd(2.0);
#define FPL2(a, b) _mm256_fmadd_pd(TWO, b, a)
#define FMI2(a, b) _mm256_fnmadd_pd(TWO, b, a)
#define FRS2(a, b) _mm256_fmsub_pd(TWO, b, a)
#define FONE_DECL const __m256d ONE = _mm256_set1_pd(1.0);
#define FA(a, b) _mm256_fmadd_pd(ONE, b, a)
#define FS(a, b) _mm256_fnmadd_pd(ONE, b, a)

#define PIN(v)
#define SFX
#include "three.inc"
#undef PIN
#undef SFX
#define PIN(v) __asm__("" : "+x"(v))
#define SFX p
#include "three.inc"
#undef PIN
#undef SFX

#undef PFX
#undef ELT
#undef V
#undef W
#undef LW
#undef BASEMAX
#undef LOAD
#undef STORE
#undef ADD
#undef SUB
#undef IDECL
#undef INREG
#undef FKDECL
#undef FPL2
#undef FMI2
#undef FRS2
#ifdef FONE_DECL
#undef FONE_DECL
#undef FA
#undef FS
#endif

/* ------------------------------------------------------------------ int32 ---- */
#define PFX wht_i_
#define ELT int32_t
#define V __m256i
#define W 8
#define LW 3
#define BASEMAX BASEMAX_4
#define LOAD(p) _mm256_loadu_si256((const __m256i *)(p))
#define STORE(p, v) _mm256_storeu_si256((__m256i *)(p), v)
#define ADD(a, b) _mm256_add_epi32(a, b)
#define SUB(a, b) ISUB(a, b)
/* gcc rewrites integer differences (a - (b - c) becomes a + (c - b), and c - b is computed beside
 * b - c): the textbook step comes out with 27 instructions instead of 24.  In the p variants every
 * difference passes a barrier, so the step is compiled as written. */
static inline __attribute__((always_inline)) __m256i opaque_sub(__m256i a, __m256i b)
{
    __m256i t = _mm256_sub_epi32(a, b);
    __asm__("" : "+x"(t));
    return t;
}
/* a level inside a register: bring the partner into place, negate the lower of the two
 * (vpsignd with a register of +1 and -1), add.  3 instructions per level and register. */
#define IDECL \
    const __m256i M0 = _mm256_setr_epi32(1, -1, 1, -1, 1, -1, 1, -1); \
    const __m256i M1 = _mm256_setr_epi32(1, 1, -1, -1, 1, 1, -1, -1); \
    const __m256i M2 = _mm256_setr_epi32(1, 1, 1, 1, -1, -1, -1, -1);
#define INREG(v) do { \
    v = ADD(_mm256_shuffle_epi32(v, 0xB1), _mm256_sign_epi32(v, M0)); \
    v = ADD(_mm256_shuffle_epi32(v, 0x4E), _mm256_sign_epi32(v, M1)); \
    v = ADD(_mm256_permute2x128_si256(v, v, 0x01), _mm256_sign_epi32(v, M2)); } while (0)
#define FKDECL
#define SL1(b) _mm256_slli_epi32(b, 1)
#define FPL2(a, b) ADD(a, SL1(b))                   /* shift and add */
#define FMI2(a, b) SUB(a, SL1(b))
#define FRS2(a, b) SUB(SL1(b), a)

#define PIN(v)
#define SFX
#define ISUB(a, b) _mm256_sub_epi32(a, b)
#include "three.inc"
#undef PIN
#undef SFX
#undef ISUB
#define PIN(v) __asm__("" : "+x"(v))
#define SFX p
#define ISUB(a, b) opaque_sub(a, b)
#include "three.inc"
#undef PIN
#undef SFX

#undef PFX
#undef ELT
#undef V
#undef W
#undef LW
#undef BASEMAX
#undef LOAD
#undef STORE
#undef ADD
#undef SUB
#undef IDECL
#undef INREG
#undef FKDECL
#undef FPL2
#undef FMI2
#undef FRS2
#ifdef FONE_DECL
#undef FONE_DECL
#undef FA
#undef FS
#endif
