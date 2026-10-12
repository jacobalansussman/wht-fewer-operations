/* kernels.h -- written by wht56/codegen.py (python3 -m wht56 --gen kernels).  Do not edit.
 *
 * Each function applies one 8-point circuit to s columns: a0..a7 are 8 rows of s numbers,
 * and column i of the rows is replaced by the circuit applied to it.
 *
 *   wht56_pass_t8         the textbook on 8 points: 24 additions and subtractions; H x
 *                         (from circuits/O_textbook_8.txt)
 *   wht56_pass_o8         the 20-operation circuit: 19 additions and subtractions and one
 *                         halving; (1/2) H x   (from circuits/h8_half_20ops.txt)
 *   wht56_pass_o8_scaled  the same, with every output multiplied by c: 8 more multiplications
 */
#ifndef WHT56_KERNELS_H
#define WHT56_KERNELS_H
#include <stddef.h>

static inline void wht56_pass_t8(double *restrict a0, double *restrict a1, double *restrict a2, double *restrict a3, double *restrict a4, double *restrict a5, double *restrict a6, double *restrict a7, size_t s)
{
    for (size_t i = 0; i < s; i++) {
        const double x0 = a0[i], x1 = a1[i], x2 = a2[i], x3 = a3[i], x4 = a4[i], x5 = a5[i], x6 = a6[i], x7 = a7[i];
        const double t1 = x0 + x1;
        const double t2 = x0 - x1;
        const double t3 = x2 + x3;
        const double t4 = x2 - x3;
        const double t5 = x4 + x5;
        const double t6 = x4 - x5;
        const double t7 = x6 + x7;
        const double t8 = x6 - x7;
        const double t9 = t1 + t3;
        const double t10 = t1 - t3;
        const double t11 = t2 + t4;
        const double t12 = t2 - t4;
        const double t13 = t5 + t7;
        const double t14 = t5 - t7;
        const double t15 = t6 + t8;
        const double t16 = t6 - t8;
        const double t17 = t9 + t13;
        const double t18 = t9 - t13;
        const double t19 = t11 + t15;
        const double t20 = t11 - t15;
        const double t21 = t10 + t14;
        const double t22 = t10 - t14;
        const double t23 = t12 + t16;
        const double t24 = t12 - t16;
        a0[i] = t17;
        a1[i] = t19;
        a2[i] = t21;
        a3[i] = t23;
        a4[i] = t18;
        a5[i] = t20;
        a6[i] = t22;
        a7[i] = t24;
    }
}

static inline void wht56_pass_o8(double *restrict a0, double *restrict a1, double *restrict a2, double *restrict a3, double *restrict a4, double *restrict a5, double *restrict a6, double *restrict a7, size_t s)
{
    for (size_t i = 0; i < s; i++) {
        const double x0 = a0[i], x1 = a1[i], x2 = a2[i], x3 = a3[i], x4 = a4[i], x5 = a5[i], x6 = a6[i], x7 = a7[i];
        const double g1 = x0 + x7;
        const double g2 = x1 + x6;
        const double g3 = x2 - x5;
        const double g4 = x3 - x4;
        const double g5 = g1 - g2;
        const double g6 = g3 + g4;
        const double g7 = g5 - g6;
        const double m8 = 0.5*g7;
        const double g9 = m8 - x7;
        const double g10 = m8 - x5;
        const double g11 = g9 + x6;
        const double g12 = g10 - x4;
        const double g13 = g11 + g4;
        const double g14 = g10 + x3;
        const double g15 = g5 - g14;
        const double g16 = g11 + g3;
        const double g17 = g12 + g2;
        const double g18 = g9 + x1;
        const double g19 = g18 + g6;
        const double g20 = g1 - g12;
        a0[i] = g20;
        a1[i] = g16;
        a2[i] = g18;
        a3[i] = g14;
        a4[i] = g19;
        a5[i] = g15;
        a6[i] = g17;
        a7[i] = g13;
    }
}

static inline void wht56_pass_o8_scaled(double *restrict a0, double *restrict a1, double *restrict a2, double *restrict a3, double *restrict a4, double *restrict a5, double *restrict a6, double *restrict a7, size_t s, double c)
{
    for (size_t i = 0; i < s; i++) {
        const double x0 = a0[i], x1 = a1[i], x2 = a2[i], x3 = a3[i], x4 = a4[i], x5 = a5[i], x6 = a6[i], x7 = a7[i];
        const double g1 = x0 + x7;
        const double g2 = x1 + x6;
        const double g3 = x2 - x5;
        const double g4 = x3 - x4;
        const double g5 = g1 - g2;
        const double g6 = g3 + g4;
        const double g7 = g5 - g6;
        const double m8 = 0.5*g7;
        const double g9 = m8 - x7;
        const double g10 = m8 - x5;
        const double g11 = g9 + x6;
        const double g12 = g10 - x4;
        const double g13 = g11 + g4;
        const double g14 = g10 + x3;
        const double g15 = g5 - g14;
        const double g16 = g11 + g3;
        const double g17 = g12 + g2;
        const double g18 = g9 + x1;
        const double g19 = g18 + g6;
        const double g20 = g1 - g12;
        a0[i] = c * g20;
        a1[i] = c * g16;
        a2[i] = c * g18;
        a3[i] = c * g14;
        a4[i] = c * g19;
        a5[i] = c * g15;
        a6[i] = c * g17;
        a7[i] = c * g13;
    }
}

#endif
