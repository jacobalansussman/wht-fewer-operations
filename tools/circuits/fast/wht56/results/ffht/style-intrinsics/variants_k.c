/* variants_k.c -- the list for harness_k: single passes, not transforms.  Written once by a few lines of python (see
 * REPORT.md, files).  Name: <step><style>_3 = the 3-level pass at distance 8 registers alone;
 * <step><style>_1 = the first pass alone.  FFHT is first only because the harness wants it there. */
#include <stddef.h>
#include "variants.h"
#include "fht.h"

static void ffht_f(float *b, int k) { (void)fht_float(b, k); }
static void ffht_d(double *b, int k) { (void)fht_double(b, k); }
void whti_T_f_only3(float *buf, int k);
void whti_T_f_only1(float *buf, int k);
void whti_N_f_only3(float *buf, int k);
void whti_N_f_only1(float *buf, int k);
void whti_NF_f_only3(float *buf, int k);
void whti_NF_f_only1(float *buf, int k);
void whti_G_f_only3(float *buf, int k);
void whti_G_f_only1(float *buf, int k);
void whti_Tp_f_only3(float *buf, int k);
void whti_Tp_f_only1(float *buf, int k);
void whti_Np_f_only3(float *buf, int k);
void whti_Np_f_only1(float *buf, int k);
void whti_NFp_f_only3(float *buf, int k);
void whti_NFp_f_only1(float *buf, int k);
void whti_Gp_f_only3(float *buf, int k);
void whti_Gp_f_only1(float *buf, int k);
void whti_Tw_f_only3(float *buf, int k);
void whti_Tw_f_only1(float *buf, int k);
void whti_Nw_f_only3(float *buf, int k);
void whti_Nw_f_only1(float *buf, int k);
void whti_NFw_f_only3(float *buf, int k);
void whti_NFw_f_only1(float *buf, int k);
void whti_Gw_f_only3(float *buf, int k);
void whti_Gw_f_only1(float *buf, int k);
void whti_Twp_f_only3(float *buf, int k);
void whti_Twp_f_only1(float *buf, int k);
void whti_Nwp_f_only3(float *buf, int k);
void whti_Nwp_f_only1(float *buf, int k);
void whti_NFwp_f_only3(float *buf, int k);
void whti_NFwp_f_only1(float *buf, int k);
void whti_Gwp_f_only3(float *buf, int k);
void whti_Gwp_f_only1(float *buf, int k);
void whti_T_d_only3(double *buf, int k);
void whti_T_d_only1(double *buf, int k);
void whti_N_d_only3(double *buf, int k);
void whti_N_d_only1(double *buf, int k);
void whti_NF_d_only3(double *buf, int k);
void whti_NF_d_only1(double *buf, int k);
void whti_G_d_only3(double *buf, int k);
void whti_G_d_only1(double *buf, int k);
void whti_Tp_d_only3(double *buf, int k);
void whti_Tp_d_only1(double *buf, int k);
void whti_Np_d_only3(double *buf, int k);
void whti_Np_d_only1(double *buf, int k);
void whti_NFp_d_only3(double *buf, int k);
void whti_NFp_d_only1(double *buf, int k);
void whti_Gp_d_only3(double *buf, int k);
void whti_Gp_d_only1(double *buf, int k);
void whti_Tw_d_only3(double *buf, int k);
void whti_Tw_d_only1(double *buf, int k);
void whti_Nw_d_only3(double *buf, int k);
void whti_Nw_d_only1(double *buf, int k);
void whti_NFw_d_only3(double *buf, int k);
void whti_NFw_d_only1(double *buf, int k);
void whti_Gw_d_only3(double *buf, int k);
void whti_Gw_d_only1(double *buf, int k);
void whti_Twp_d_only3(double *buf, int k);
void whti_Twp_d_only1(double *buf, int k);
void whti_Nwp_d_only3(double *buf, int k);
void whti_Nwp_d_only1(double *buf, int k);
void whti_NFwp_d_only3(double *buf, int k);
void whti_NFwp_d_only1(double *buf, int k);
void whti_Gwp_d_only3(double *buf, int k);
void whti_Gwp_d_only1(double *buf, int k);
const variant_f variants_f[] = {
    {"ffht", ffht_f, NULL, 1, 30, "FFHT (a whole transform; here only as the first of the list)"},
    {"T_3", whti_T_f_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step T, style plain"},
    {"N_3", whti_N_f_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step N, style plain"},
    {"NF_3", whti_NF_f_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step NF, style plain"},
    {"G_3", whti_G_f_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step G, style plain"},
    {"Tp_3", whti_Tp_f_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step T, style p"},
    {"Np_3", whti_Np_f_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step N, style p"},
    {"NFp_3", whti_NFp_f_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step NF, style p"},
    {"Gp_3", whti_Gp_f_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step G, style p"},
    {"Tw_3", whti_Tw_f_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step T, style w"},
    {"Nw_3", whti_Nw_f_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step N, style w"},
    {"NFw_3", whti_NFw_f_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step NF, style w"},
    {"Gw_3", whti_Gw_f_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step G, style w"},
    {"Twp_3", whti_Twp_f_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step T, style wp"},
    {"Nwp_3", whti_Nwp_f_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step N, style wp"},
    {"NFwp_3", whti_NFwp_f_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step NF, style wp"},
    {"Gwp_3", whti_Gwp_f_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step G, style wp"},
    {"T_1", whti_T_f_only1, NULL, 9, 30, "the first pass, alone: step T, style plain"},
    {"N_1", whti_N_f_only1, NULL, 9, 30, "the first pass, alone: step N, style plain"},
    {"NF_1", whti_NF_f_only1, NULL, 9, 30, "the first pass, alone: step NF, style plain"},
    {"G_1", whti_G_f_only1, NULL, 9, 30, "the first pass, alone: step G, style plain"},
    {"Tp_1", whti_Tp_f_only1, NULL, 9, 30, "the first pass, alone: step T, style p"},
    {"Np_1", whti_Np_f_only1, NULL, 9, 30, "the first pass, alone: step N, style p"},
    {"NFp_1", whti_NFp_f_only1, NULL, 9, 30, "the first pass, alone: step NF, style p"},
    {"Gp_1", whti_Gp_f_only1, NULL, 9, 30, "the first pass, alone: step G, style p"},
    {"Tw_1", whti_Tw_f_only1, NULL, 9, 30, "the first pass, alone: step T, style w"},
    {"Nw_1", whti_Nw_f_only1, NULL, 9, 30, "the first pass, alone: step N, style w"},
    {"NFw_1", whti_NFw_f_only1, NULL, 9, 30, "the first pass, alone: step NF, style w"},
    {"Gw_1", whti_Gw_f_only1, NULL, 9, 30, "the first pass, alone: step G, style w"},
    {"Twp_1", whti_Twp_f_only1, NULL, 9, 30, "the first pass, alone: step T, style wp"},
    {"Nwp_1", whti_Nwp_f_only1, NULL, 9, 30, "the first pass, alone: step N, style wp"},
    {"NFwp_1", whti_NFwp_f_only1, NULL, 9, 30, "the first pass, alone: step NF, style wp"},
    {"Gwp_1", whti_Gwp_f_only1, NULL, 9, 30, "the first pass, alone: step G, style wp"},
};
const int n_variants_f = (int)(sizeof variants_f / sizeof variants_f[0]);

const variant_d variants_d[] = {
    {"ffht", ffht_d, NULL, 1, 30, "FFHT (a whole transform; here only as the first of the list)"},
    {"T_3", whti_T_d_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step T, style plain"},
    {"N_3", whti_N_d_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step N, style plain"},
    {"NF_3", whti_NF_d_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step NF, style plain"},
    {"G_3", whti_G_d_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step G, style plain"},
    {"Tp_3", whti_Tp_d_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step T, style p"},
    {"Np_3", whti_Np_d_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step N, style p"},
    {"NFp_3", whti_NFp_d_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step NF, style p"},
    {"Gp_3", whti_Gp_d_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step G, style p"},
    {"Tw_3", whti_Tw_d_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step T, style w"},
    {"Nw_3", whti_Nw_d_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step N, style w"},
    {"NFw_3", whti_NFw_d_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step NF, style w"},
    {"Gw_3", whti_Gw_d_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step G, style w"},
    {"Twp_3", whti_Twp_d_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step T, style wp"},
    {"Nwp_3", whti_Nwp_d_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step N, style wp"},
    {"NFwp_3", whti_NFwp_d_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step NF, style wp"},
    {"Gwp_3", whti_Gwp_d_only3, NULL, 9, 30, "the 3-level pass at distance 8 registers, alone: step G, style wp"},
    {"T_1", whti_T_d_only1, NULL, 9, 30, "the first pass, alone: step T, style plain"},
    {"N_1", whti_N_d_only1, NULL, 9, 30, "the first pass, alone: step N, style plain"},
    {"NF_1", whti_NF_d_only1, NULL, 9, 30, "the first pass, alone: step NF, style plain"},
    {"G_1", whti_G_d_only1, NULL, 9, 30, "the first pass, alone: step G, style plain"},
    {"Tp_1", whti_Tp_d_only1, NULL, 9, 30, "the first pass, alone: step T, style p"},
    {"Np_1", whti_Np_d_only1, NULL, 9, 30, "the first pass, alone: step N, style p"},
    {"NFp_1", whti_NFp_d_only1, NULL, 9, 30, "the first pass, alone: step NF, style p"},
    {"Gp_1", whti_Gp_d_only1, NULL, 9, 30, "the first pass, alone: step G, style p"},
    {"Tw_1", whti_Tw_d_only1, NULL, 9, 30, "the first pass, alone: step T, style w"},
    {"Nw_1", whti_Nw_d_only1, NULL, 9, 30, "the first pass, alone: step N, style w"},
    {"NFw_1", whti_NFw_d_only1, NULL, 9, 30, "the first pass, alone: step NF, style w"},
    {"Gw_1", whti_Gw_d_only1, NULL, 9, 30, "the first pass, alone: step G, style w"},
    {"Twp_1", whti_Twp_d_only1, NULL, 9, 30, "the first pass, alone: step T, style wp"},
    {"Nwp_1", whti_Nwp_d_only1, NULL, 9, 30, "the first pass, alone: step N, style wp"},
    {"NFwp_1", whti_NFwp_d_only1, NULL, 9, 30, "the first pass, alone: step NF, style wp"},
    {"Gwp_1", whti_Gwp_d_only1, NULL, 9, 30, "the first pass, alone: step G, style wp"},
};
const int n_variants_d = (int)(sizeof variants_d / sizeof variants_d[0]);
