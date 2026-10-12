/* whtf.h -- the transforms of whtf.c (AVX2 + FMA) and whts.c (scalar int32).  In place, 2^k numbers,
 * k >= 3, output H x exactly, natural order. */
#ifndef STYLE_FUSED_WHTF_H
#define STYLE_FUSED_WHTF_H
#include <stdint.h>

void wht_f_T(float *x, int k);
void wht_f_G19(float *x, int k);
void wht_f_G19a(float *x, int k);
void wht_f_Tp(float *x, int k);
void wht_f_G19p(float *x, int k);
void wht_f_G19ap(float *x, int k);
void wht_f_Tf(float *x, int k);
void wht_f_Tfp(float *x, int k);

void wht_d_T(double *x, int k);
void wht_d_G19(double *x, int k);
void wht_d_G19a(double *x, int k);
void wht_d_Tp(double *x, int k);
void wht_d_G19p(double *x, int k);
void wht_d_G19ap(double *x, int k);
void wht_d_Tf(double *x, int k);
void wht_d_Tfp(double *x, int k);

void wht_i_T(int32_t *x, int k);
void wht_i_G19(int32_t *x, int k);
void wht_i_G19a(int32_t *x, int k);
void wht_i_Tp(int32_t *x, int k);
void wht_i_G19p(int32_t *x, int k);
void wht_i_G19ap(int32_t *x, int k);

/* whts.c: one number at a time, the compiler's vectoriser switched off */
void wht_s_T(int32_t *x, int k);
void wht_s_G19(int32_t *x, int k);

/* naive_i.c: three plain loops, one level per pass; the reference for int32 */
void naive_r2_i(int32_t *x, int k);

#endif
