/* wht56.h -- see wht56.c */
#ifndef WHT56_H
#define WHT56_H
#include <stddef.h>

/* n must be a power of two (1, 2, 4, ...).  For any other n, 0 included, the four transforms
 * return at once and leave x untouched, and wht56_k8_raw_factor returns 0.  Test a length with
 * wht56_valid_length(n) before the call.  All four work in place on n doubles. */
int wht56_valid_length(size_t n);              /* 1 if n is a power of two, 0 otherwise */
void wht56_textbook_r2(double *x, size_t n);   /* H x, textbook, one bit per pass */
void wht56_textbook_r8(double *x, size_t n);   /* H x, textbook, three bits per pass */
void wht56_k8_raw(double *x, size_t n);        /* H x * wht56_k8_raw_factor(n), 20-operation circuit */
void wht56_k8(double *x, size_t n);            /* H x, 20-operation circuit and n multiplications */
double wht56_k8_raw_factor(size_t n);          /* 1 / 2^floor(log2(n)/3) */

#endif
