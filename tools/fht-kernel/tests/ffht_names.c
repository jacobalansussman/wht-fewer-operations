/* ffht_names.c -- code written for FFHT: it calls FFHT's four functions by FFHT's names and nothing else.  test.sh
 * compiles it against this library built with -DWHTC_FFHT_NAMES, to show that such code links unchanged.  It
 * declares the functions exactly as FFHT's fht.h does (commit fba727a3). */
#include <stdio.h>
#include <string.h>

int fht_float(float *buf, int log_n);
int fht_double(double *buf, int log_n);
int fht_float_oop(float *in, float *out, int log_n);
int fht_double_oop(double *in, double *out, int log_n);

int main(void) {
  float f[8] = {1, 0, 0, 0, 0, 0, 0, 0}, g[8];
  double d[8] = {0, 1, 0, 0, 0, 0, 0, 0}, e[8];
  int r = fht_float(f, 3) | fht_double(d, 3) | fht_float_oop(f, g, 3) | fht_double_oop(d, e, 3);
  /* H e0 = all ones; H e1 = (+1, -1, +1, -1, ...); applied twice: 8 times the input */
  int ok = r == 0 && f[0] == 1 && f[7] == 1 && d[0] == 1 && d[1] == -1 && g[0] == 8 && g[1] == 0 && e[1] == 8 && e[0] == 0;
  ok &= fht_float(f, 31) == 1 && fht_double(d, -1) == 1;
  printf("CHECK code written for FFHT (fht_float, fht_double, fht_float_oop, fht_double_oop) links and runs: %s\n",
         ok ? "PASS" : "FAIL");
  return ok ? 0 : 1;
}
