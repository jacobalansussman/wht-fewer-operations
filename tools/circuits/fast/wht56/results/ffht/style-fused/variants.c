/* variants.c -- the lists of transforms of this folder.  See variants.h. */
#include <stddef.h>
#include "variants.h"
#include "fht.h"            /* FFHT: -I$(FFHT_DIR); the code itself is FFHT's own fht.o */
#include "whtf.h"

static void ffht_f(float *b, int k) { (void)fht_float(b, k); }
static void ffht_d(double *b, int k) { (void)fht_double(b, k); }
/* the same FFHT source and flags, compiled here with every jump kept inside a 32-byte block */
int Bfht_float(float *buf, int log_n);
int Bfht_double(double *buf, int log_n);
static void ffhtB_f(float *b, int k) { (void)Bfht_float(b, k); }
static void ffhtB_d(double *b, int k) { (void)Bfht_double(b, k); }

const variant_f variants_f[] = {
    {"ffht", ffht_f,     NULL, 1, 30, "FFHT fht_float: its own fht.o, built by its own Makefile"},
    {"ffhtB", ffhtB_f,   NULL, 1, 30, "FFHT fht_float, same source and flags, jumps kept inside 32-byte blocks"},
    {"T",    wht_f_T,    NULL, 3, 30, "intrinsics, textbook step: 24 vaddps/vsubps per 8 registers"},
    {"G19",  wht_f_G19,  NULL, 3, 30, "intrinsics, form G: 7 vaddps/vsubps + 12 fused multiply-adds with 2.0"},
    {"G19a", wht_f_G19a, NULL, 3, 30, "intrinsics, form G with a + b + b: 31 vaddps/vsubps, no multiplier"},
    {"Tp",    wht_f_Tp,    NULL, 3, 30, "T, loaded numbers kept in registers"},
    {"G19p",  wht_f_G19p,  NULL, 3, 30, "G19, loaded numbers kept in registers"},
    {"G19ap", wht_f_G19ap, NULL, 3, 30, "G19a, loaded numbers kept in registers"},
    {"Tfp",   wht_f_Tfp,   NULL, 3, 30, "textbook step, each addition as a fused multiply-add by 1.0; loaded numbers kept in registers"},
};
const int n_variants_f = (int)(sizeof variants_f / sizeof variants_f[0]);

const variant_d variants_d[] = {
    {"ffht", ffht_d,     NULL, 1, 30, "FFHT fht_double: its own fht.o, built by its own Makefile"},
    {"ffhtB", ffhtB_d,   NULL, 1, 30, "FFHT fht_double, same source and flags, jumps kept inside 32-byte blocks"},
    {"T",    wht_d_T,    NULL, 3, 30, "intrinsics, textbook step: 24 vaddpd/vsubpd per 8 registers"},
    {"G19",  wht_d_G19,  NULL, 3, 30, "intrinsics, form G: 7 vaddpd/vsubpd + 12 fused multiply-adds with 2.0"},
    {"G19a", wht_d_G19a, NULL, 3, 30, "intrinsics, form G with a + b + b: 31 vaddpd/vsubpd, no multiplier"},
    {"Tp",    wht_d_Tp,    NULL, 3, 30, "T, loaded numbers kept in registers"},
    {"G19p",  wht_d_G19p,  NULL, 3, 30, "G19, loaded numbers kept in registers"},
    {"G19ap", wht_d_G19ap, NULL, 3, 30, "G19a, loaded numbers kept in registers"},
    {"Tfp",   wht_d_Tfp,   NULL, 3, 30, "textbook step, each addition as a fused multiply-add by 1.0; loaded numbers kept in registers"},
};
const int n_variants_d = (int)(sizeof variants_d / sizeof variants_d[0]);

const variant_i variants_i[] = {
    {"naive", naive_r2_i, NULL, 1, 30, "plain radix-2 triple loop (the reference of the check)"},
    {"T",     wht_i_T,    NULL, 3, 30, "intrinsics, textbook step: 24 vpaddd/vpsubd per 8 registers"},
    {"G19s",  wht_i_G19,  NULL, 3, 30, "intrinsics, form G: 7 vpaddd/vpsubd + 12 lines as shift-by-one and add"},
    {"G19a",  wht_i_G19a, NULL, 3, 30, "intrinsics, form G with a + b + b: 31 vpaddd/vpsubd"},
    {"Tp",    wht_i_Tp,    NULL, 3, 30, "T, loaded numbers kept in registers"},
    {"G19sp", wht_i_G19p,  NULL, 3, 30, "G19s, loaded numbers kept in registers"},
    {"G19ap", wht_i_G19ap, NULL, 3, 30, "G19a, loaded numbers kept in registers"},
    {"sT",    wht_s_T,    NULL, 3, 30, "scalar C, textbook step, vectoriser off"},
    {"sG19",  wht_s_G19,  NULL, 3, 30, "scalar C, form G written a + 2*b (LEA), vectoriser off"},
};
const int n_variants_i = (int)(sizeof variants_i / sizeof variants_i[0]);
