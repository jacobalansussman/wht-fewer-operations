/* naive_i.c -- the plain radix-2 transform for int32, one level per pass: the reference of the check.
 * Also the "transform" that does nothing, for the three types (../harness/empty.c plus int32). */
#include <stddef.h>
#include <stdint.h>
#include "whtf.h"

void naive_r2_i(int32_t *x, int k)
{
    const size_t n = (size_t)1 << k;
    for (size_t s = 1; s < n; s *= 2)
        for (size_t b = 0; b < n; b += 2 * s)
            for (size_t i = 0; i < s; i++) {
                const int32_t u = x[b + i], v = x[b + i + s];
                x[b + i] = u + v;
                x[b + i + s] = u - v;
            }
}

void harness_empty_f(float *buf, int log_n);
void harness_empty_d(double *buf, int log_n);
void harness_empty_i(int32_t *buf, int log_n);
void harness_empty_f(float *buf, int log_n) { (void)buf; (void)log_n; }
void harness_empty_d(double *buf, int log_n) { (void)buf; (void)log_n; }
void harness_empty_i(int32_t *buf, int log_n) { (void)buf; (void)log_n; }
