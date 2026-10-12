/* variants.c -- the wrappers and the two lists.  See variants.h. */
#include <stddef.h>
#include "variants.h"
#include "fht.h"            /* FFHT: -I$(FFHT_DIR); the code itself is FFHT's own fht.o */
#include "wht56.h"          /* our plain C, doubles (ours/wht56.c) */
#include "wht56f.h"         /* the same text with float for double (the Makefile writes it) */

void naive_r2_f(float *buf, int log_n);      /* naive.c, compiled with -O3 -mavx2 */
void naive_r2_d(double *buf, int log_n);

/* ---- FFHT ---- */
static void ffht_f(float *b, int k) { (void)fht_float(b, k); }
static void ffht_d(double *b, int k) { (void)fht_double(b, k); }

/* ---- our plain C: the three programs that take 8 points at a time ---- */
static void t8_d(double *b, int k) { wht56_textbook_r8(b, (size_t)1 << k); }
static void k8_d(double *b, int k) { wht56_k8(b, (size_t)1 << k); }
static void k8raw_d(double *b, int k) { wht56_k8_raw(b, (size_t)1 << k); }
static void t8_f(float *b, int k) { wht56f_textbook_r8(b, (size_t)1 << k); }
static void k8_f(float *b, int k) { wht56f_k8(b, (size_t)1 << k); }
static void k8raw_f(float *b, int k) { wht56f_k8_raw(b, (size_t)1 << k); }

/* wht56_k8_raw leaves H x / 2^floor(log_n / 3): one halving for each 8-point pass */
static int k8raw_scale(int k) { return k / 3; }

const variant_f variants_f[] = {
    {"ffht",  ffht_f,     NULL,        1, 30, "FFHT fht_float: its own fht.o, built by its own Makefile"},
    {"t8",    t8_f,       NULL,        0, 30, "our plain C, textbook, 3 levels per pass (24 add/sub per 8 points)"},
    {"k8",    k8_f,       NULL,        0, 30, "our plain C, 20-operation kernel, exact (n multiplications in the last pass)"},
    {"k8raw", k8raw_f,    k8raw_scale, 0, 30, "our plain C, 20-operation kernel, H x / 2^floor(log_n/3)"},
    {"naive", naive_r2_f, NULL,        0, 30, "plain radix-2 triple loop, gcc -O3 -mavx2"},
};
const int n_variants_f = (int)(sizeof variants_f / sizeof variants_f[0]);

const variant_d variants_d[] = {
    {"ffht",  ffht_d,     NULL,        1, 30, "FFHT fht_double: its own fht.o, built by its own Makefile"},
    {"t8",    t8_d,       NULL,        0, 30, "our plain C, textbook, 3 levels per pass (24 add/sub per 8 points)"},
    {"k8",    k8_d,       NULL,        0, 30, "our plain C, 20-operation kernel, exact (n multiplications in the last pass)"},
    {"k8raw", k8raw_d,    k8raw_scale, 0, 30, "our plain C, 20-operation kernel, H x / 2^floor(log_n/3)"},
    {"naive", naive_r2_d, NULL,        0, 30, "plain radix-2 triple loop, gcc -O3 -mavx2"},
};
const int n_variants_d = (int)(sizeof variants_d / sizeof variants_d[0]);
