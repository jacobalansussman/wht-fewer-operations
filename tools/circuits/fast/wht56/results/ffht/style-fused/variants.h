/* variants.h -- (style-fused copy: ../harness/variants.h plus the int32 list.)
 *
 * A variant is a function  void f(T *buf, int log_n)  that replaces the 2^log_n numbers at buf by
 * their Walsh-Hadamard transform, in place: output j = sum over i of (-1)^popcount(i & j) x[i].
 * scale_log2 = NULL: the output is H x exactly.  The first variant of each list is the reference
 * of the check: FFHT for float and double, a plain radix-2 loop for int32.
 */
#ifndef HARNESS_VARIANTS_H
#define HARNESS_VARIANTS_H
#include <stdint.h>

typedef void (*fn_f)(float *buf, int log_n);
typedef void (*fn_d)(double *buf, int log_n);
typedef void (*fn_i)(int32_t *buf, int log_n);
typedef int (*scale_fn)(int log_n);

typedef struct { const char *name; fn_f f; scale_fn scale_log2; int kmin, kmax; const char *what; } variant_f;
typedef struct { const char *name; fn_d f; scale_fn scale_log2; int kmin, kmax; const char *what; } variant_d;
typedef struct { const char *name; fn_i f; scale_fn scale_log2; int kmin, kmax; const char *what; } variant_i;

extern const variant_f variants_f[];
extern const int n_variants_f;
extern const variant_d variants_d[];
extern const int n_variants_d;
extern const variant_i variants_i[];
extern const int n_variants_i;

#endif
