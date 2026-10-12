/* variants_where.c -- the list of transforms for the third question of the style-generator job:
 * the new kernel only in some of the passes of 8 registers.  See variants.h and variants.c.
 *
 * ffht   FFHT as it is
 * g20s   20-operation block in every 8-register pass, H x / 2^P (as in variants.c)
 * p20s   20-operation block in every 8-register pass but the first one (block of 512 bytes or more)
 * p19f   19-gate multiply-add block in the same passes, exact
 * c20s   20-operation block only in passes whose block is 64 KiB or more (outside the first-level cache)
 * d20s   20-operation block only in passes whose block is 512 KiB or more (outside the second-level cache)
 * d20x   the same, exact (8 multiplications in the outermost pass)
 * d19f   19-gate multiply-add block in passes whose block is 512 KiB or more, exact
 * Every other pass is FFHT's textbook block.
 */
#include <stddef.h>
#include "variants.h"
#include "fht.h"

#define DECL(v) int v##_fht_float(float *buf, int log_n); int v##_fht_double(double *buf, int log_n); \
    static void v##_f(float *b, int k) { (void)v##_fht_float(b, k); } \
    static void v##_d(double *b, int k) { (void)v##_fht_double(b, k); }
DECL(g20s)
DECL(p20s)
DECL(p19f)
DECL(c20s)
DECL(d20s)
DECL(d20x)
DECL(d19f)

static void ffht_f(float *b, int k) { (void)fht_float(b, k); }
static void ffht_d(double *b, int k) { (void)fht_double(b, k); }

/* the scale tables, written by the generator; the Makefile prefixes their names */
#include "g20s_scale.inc"
#include "p20s_scale.inc"
#include "c20s_scale.inc"
#include "d20s_scale.inc"
#define SCALE(v) \
    static int v##_scale_f(int k) { (void)v##_k8_passes_float; return v##_k8_scale_float[k]; } \
    static int v##_scale_d(int k) { (void)v##_k8_passes_double; return v##_k8_scale_double[k]; }
SCALE(g20s)
SCALE(p20s)
SCALE(c20s)
SCALE(d20s)

const variant_f variants_f[] = {
    {"ffht", ffht_f, NULL,         1, 30, "FFHT fht_float: its own fht.o, built by its own Makefile"},
    {"g20s", g20s_f, g20s_scale_f, 1, 30, "20-operation block in every 8-register pass, H x / 2^P"},
    {"p20s", p20s_f, p20s_scale_f, 1, 30, "20-operation block in every 8-register pass but the first, H x / 2^P"},
    {"p19f", p19f_f, NULL,         1, 30, "19-gate FMA block in every 8-register pass but the first, exact"},
    {"c20s", c20s_f, c20s_scale_f, 1, 30, "20-operation block in passes with a block of 64 KiB or more, H x / 2^P"},
    {"d20s", d20s_f, d20s_scale_f, 1, 30, "20-operation block in passes with a block of 512 KiB or more, H x / 2^P"},
    {"d20x", d20x_f, NULL,         1, 30, "20-operation block in passes with a block of 512 KiB or more, exact"},
    {"d19f", d19f_f, NULL,         1, 30, "19-gate FMA block in passes with a block of 512 KiB or more, exact"},
};
const int n_variants_f = (int)(sizeof variants_f / sizeof variants_f[0]);

const variant_d variants_d[] = {
    {"ffht", ffht_d, NULL,         1, 30, "FFHT fht_double: its own fht.o, built by its own Makefile"},
    {"g20s", g20s_d, g20s_scale_d, 1, 30, "20-operation block in every 8-register pass, H x / 2^P"},
    {"p20s", p20s_d, p20s_scale_d, 1, 30, "20-operation block in every 8-register pass but the first, H x / 2^P"},
    {"p19f", p19f_d, NULL,         1, 30, "19-gate FMA block in every 8-register pass but the first, exact"},
    {"c20s", c20s_d, c20s_scale_d, 1, 30, "20-operation block in passes with a block of 64 KiB or more, H x / 2^P"},
    {"d20s", d20s_d, d20s_scale_d, 1, 30, "20-operation block in passes with a block of 512 KiB or more, H x / 2^P"},
    {"d20x", d20x_d, NULL,         1, 30, "20-operation block in passes with a block of 512 KiB or more, exact"},
    {"d19f", d19f_d, NULL,         1, 30, "19-gate FMA block in passes with a block of 512 KiB or more, exact"},
};
const int n_variants_d = (int)(sizeof variants_d / sizeof variants_d[0]);
