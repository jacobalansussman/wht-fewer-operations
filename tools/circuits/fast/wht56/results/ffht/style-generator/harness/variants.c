/* variants.c -- the list of transforms for the style-generator job.  See variants.h.
 *
 * ffht   FFHT as it is: its own fht.o from the untouched clone, built by its own Makefile.
 * The others are FFHT's fht.c built the same way (same Makefile, same flags) around an fht_avx.c
 * that the patched generator wrote with FFHT's own shipped plan; only the block that takes 8
 * registers through 3 levels differs (build_variants.sh):
 *   gT     the textbook block: this fht_avx.c is FFHT's own file, byte for byte.  A second copy
 *          of the same code at another place in the program: what it differs from ffht by is
 *          what the placement of code and the noise of the run are worth.
 *   g20x   the 20-operation block (19 additions and subtractions, one halving); the last such
 *          pass multiplies by 2^P, so the result is H x itself
 *   g20s   the same without those multiplications: H x / 2^P, P = the number of such passes
 *   g19f   the 19-gate block: 7 additions and subtractions and 12 multiply-add instructions
 *          (FMA) with the constant 2 as a memory operand; H x itself
 *   g19r   the same with the constant 2 loaded once per block into a register
 */
#include <stddef.h>
#include "variants.h"
#include "fht.h"            /* FFHT: -I$(FFHT_DIR) */

#define DECL(v) int v##_fht_float(float *buf, int log_n); int v##_fht_double(double *buf, int log_n); \
    static void v##_f(float *b, int k) { (void)v##_fht_float(b, k); } \
    static void v##_d(double *b, int k) { (void)v##_fht_double(b, k); }
DECL(gT)
DECL(g20x)
DECL(g20s)
DECL(g19f)
DECL(g19r)

static void ffht_f(float *b, int k) { (void)fht_float(b, k); }
static void ffht_d(double *b, int k) { (void)fht_double(b, k); }

/* the power of two by which g20s leaves the result divided, written by the generator */
#include "g20s_scale.inc"
static int g20s_scale_f(int k) { (void)k8_passes_float; return k8_scale_float[k]; }
static int g20s_scale_d(int k) { (void)k8_passes_double; return k8_scale_double[k]; }

const variant_f variants_f[] = {
    {"ffht", ffht_f, NULL,         1, 30, "FFHT fht_float: its own fht.o, built by its own Makefile"},
    {"gT",   gT_f,   NULL,         1, 30, "regenerated, textbook block (the same source as ffht, byte for byte)"},
    {"g20x", g20x_f, NULL,         1, 30, "regenerated, 20-operation block, exact (8 multiplications in the last 8-register pass)"},
    {"g20s", g20s_f, g20s_scale_f, 1, 30, "regenerated, 20-operation block, H x / 2^P"},
    {"g19f", g19f_f, NULL,         1, 30, "regenerated, 19-gate block with FMA, constant 2 in memory, exact"},
    {"g19r", g19r_f, NULL,         1, 30, "regenerated, 19-gate block with FMA, constant 2 in a register, exact"},
};
const int n_variants_f = (int)(sizeof variants_f / sizeof variants_f[0]);

const variant_d variants_d[] = {
    {"ffht", ffht_d, NULL,         1, 30, "FFHT fht_double: its own fht.o, built by its own Makefile"},
    {"gT",   gT_d,   NULL,         1, 30, "regenerated, textbook block (the same source as ffht, byte for byte)"},
    {"g20x", g20x_d, NULL,         1, 30, "regenerated, 20-operation block, exact (8 multiplications in the last 8-register pass)"},
    {"g20s", g20s_d, g20s_scale_d, 1, 30, "regenerated, 20-operation block, H x / 2^P"},
    {"g19f", g19f_d, NULL,         1, 30, "regenerated, 19-gate block with FMA, constant 2 in memory, exact"},
    {"g19r", g19r_d, NULL,         1, 30, "regenerated, 19-gate block with FMA, constant 2 in a register, exact"},
};
const int n_variants_d = (int)(sizeof variants_d / sizeof variants_d[0]);
