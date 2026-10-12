/* naive.c -- the textbook Walsh-Hadamard transform as three plain loops, one level per pass over
 * the whole array.  The Makefile compiles this file with -O3 -mavx2 and nothing else: it is the
 * floor that a few lines of C and a compiler give, with no blocking and no hand-written vector
 * code. */
#include <stddef.h>

void naive_r2_f(float *buf, int log_n);
void naive_r2_d(double *buf, int log_n);

void naive_r2_f(float *buf, int log_n)
{
    const size_t n = (size_t)1 << log_n;
    for (size_t h = 1; h < n; h <<= 1)
        for (size_t j = 0; j < n; j += 2 * h)
            for (size_t i = j; i < j + h; i++) {
                const float u = buf[i], v = buf[i + h];
                buf[i] = u + v;
                buf[i + h] = u - v;
            }
}

void naive_r2_d(double *buf, int log_n)
{
    const size_t n = (size_t)1 << log_n;
    for (size_t h = 1; h < n; h <<= 1)
        for (size_t j = 0; j < n; j += 2 * h)
            for (size_t i = j; i < j + h; i++) {
                const double u = buf[i], v = buf[i + h];
                buf[i] = u + v;
                buf[i + h] = u - v;
            }
}
