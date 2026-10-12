#include "kernels.h"
#define ROWS(p, s) (p), (p) + (s), (p) + 2 * (s), (p) + 3 * (s), (p) + 4 * (s), (p) + 5 * (s), (p) + 6 * (s), (p) + 7 * (s)
void t8(double *x, size_t s) { wht56_pass_t8(ROWS(x, s), s); }
void o8(double *x, size_t s) { wht56_pass_o8(ROWS(x, s), s); }
void o8s(double *x, size_t s, double c) { wht56_pass_o8_scaled(ROWS(x, s), s, c); }
