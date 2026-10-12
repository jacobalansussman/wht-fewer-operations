/* variants.h -- the list of transforms that harness.c checks and times.
 *
 * A variant is a function  void f(T *buf, int log_n)  that replaces the 2^log_n numbers at buf by
 * their Walsh-Hadamard transform, in place: output j = sum over i of (-1)^popcount(i & j) x[i]
 * (no division, natural order: this is what FFHT's fht_float and fht_double give).
 *
 * scale_log2 says how the output is scaled:
 *   NULL            the output is H x exactly;
 *   a function s    the output is H x / 2^s(log_n) ("up to scale"); the check multiplies by 2^s.
 *
 * To add a variant: write the wrapper in variants.c (or in a new .c file listed in the Makefile)
 * and add one line to variants_f[] or variants_d[].  The first variant of each list must be
 * FFHT: the check compares every other variant with it.
 */
#ifndef HARNESS_VARIANTS_H
#define HARNESS_VARIANTS_H

typedef void (*fn_f)(float *buf, int log_n);
typedef void (*fn_d)(double *buf, int log_n);
typedef int (*scale_fn)(int log_n);

typedef struct {
    const char *name;        /* short, no spaces: it is a key in the output */
    fn_f f;
    scale_fn scale_log2;     /* NULL = exact */
    int kmin, kmax;          /* the sizes 2^kmin .. 2^kmax the variant accepts */
    const char *what;        /* one line for the listing */
} variant_f;

typedef struct {
    const char *name;
    fn_d f;
    scale_fn scale_log2;
    int kmin, kmax;
    const char *what;
} variant_d;

extern const variant_f variants_f[];
extern const int n_variants_f;
extern const variant_d variants_d[];
extern const int n_variants_d;

#endif
