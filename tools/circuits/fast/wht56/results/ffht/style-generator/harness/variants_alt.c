/* variants_alt.c -- the list of transforms for the second question of the style-generator job:
 * a plan with one more pass of 8 registers at the 7 sizes where FFHT's shipped plan has one
 * fewer than the size allows (alt_plan.py).  See variants.h and variants.c.
 *
 * ffht   FFHT as it is (its own fht.o, shipped plan, textbook block)
 * aT     the other plan, textbook block: against ffht it says whether the other plan by itself
 *        makes FFHT faster or slower on this machine
 * a20x, a20s, a19f   the other plan with the 20-operation block (exact / up to scale) and with
 *        the 19-gate multiply-add block
 * g20s, g19f         the shipped plan with the same blocks (as in variants.c), for comparison
 * At every size other than the 7, the a-variants are the same code as the g-variants.
 */
#include <stddef.h>
#include "variants.h"
#include "fht.h"

#define DECL(v) int v##_fht_float(float *buf, int log_n); int v##_fht_double(double *buf, int log_n); \
    static void v##_f(float *b, int k) { (void)v##_fht_float(b, k); } \
    static void v##_d(double *b, int k) { (void)v##_fht_double(b, k); }
DECL(aT)
DECL(a20x)
DECL(a20s)
DECL(a19f)
DECL(g20s)
DECL(g19f)

static void ffht_f(float *b, int k) { (void)fht_float(b, k); }
static void ffht_d(double *b, int k) { (void)fht_double(b, k); }

#include "g20s_scale.inc"
static int g20s_scale_f(int k) { (void)k8_passes_float; return k8_scale_float[k]; }
static int g20s_scale_d(int k) { (void)k8_passes_double; return k8_scale_double[k]; }
#include "a20s_scale.inc"       /* the same table for the other plan, names prefixed with alt_ */
static int a20s_scale_f(int k) { (void)alt_k8_passes_float; return alt_k8_scale_float[k]; }
static int a20s_scale_d(int k) { (void)alt_k8_passes_double; return alt_k8_scale_double[k]; }

const variant_f variants_f[] = {
    {"ffht", ffht_f, NULL,         1, 30, "FFHT fht_float: its own fht.o, built by its own Makefile"},
    {"aT",   aT_f,   NULL,         1, 30, "other plan, textbook block"},
    {"a20x", a20x_f, NULL,         1, 30, "other plan, 20-operation block, exact"},
    {"a20s", a20s_f, a20s_scale_f, 1, 30, "other plan, 20-operation block, H x / 2^P"},
    {"a19f", a19f_f, NULL,         1, 30, "other plan, 19-gate block with FMA, exact"},
    {"g20s", g20s_f, g20s_scale_f, 1, 30, "shipped plan, 20-operation block, H x / 2^P"},
    {"g19f", g19f_f, NULL,         1, 30, "shipped plan, 19-gate block with FMA, exact"},
};
const int n_variants_f = (int)(sizeof variants_f / sizeof variants_f[0]);

const variant_d variants_d[] = {
    {"ffht", ffht_d, NULL,         1, 30, "FFHT fht_double: its own fht.o, built by its own Makefile"},
    {"aT",   aT_d,   NULL,         1, 30, "other plan, textbook block"},
    {"a20x", a20x_d, NULL,         1, 30, "other plan, 20-operation block, exact"},
    {"a20s", a20s_d, a20s_scale_d, 1, 30, "other plan, 20-operation block, H x / 2^P"},
    {"a19f", a19f_d, NULL,         1, 30, "other plan, 19-gate block with FMA, exact"},
    {"g20s", g20s_d, g20s_scale_d, 1, 30, "shipped plan, 20-operation block, H x / 2^P"},
    {"g19f", g19f_d, NULL,         1, 30, "shipped plan, 19-gate block with FMA, exact"},
};
const int n_variants_d = (int)(sizeof variants_d / sizeof variants_d[0]);
