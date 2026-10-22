// ffht_overloads.cpp -- FFHT's C++ overloads fht(...) through whtc.h with WHTC_FFHT_NAMES (run by test.sh when a
// C++ compiler is present).
#define WHTC_FFHT_NAMES
#include <cstdio>

#include "../whtc.h"

int main() {
  float f[4] = {1, 2, 3, 4}, g[4];
  double d[4] = {1, 2, 3, 4}, e[4];
  int r = fht(f, 2) | fht(d, 2) | fht(f, g, 2) | fht(d, e, 2);
  // H (1,2,3,4) = (10, -2, -4, 0); applied twice: 4 times the input
  bool ok = r == 0 && f[0] == 10 && f[1] == -2 && f[2] == -4 && f[3] == 0 && d[0] == 10 && g[0] == 4 && e[3] == 16;
  std::printf("CHECK FFHT's C++ overloads fht(...) compile and run: %s\n", ok ? "PASS" : "FAIL");
  return ok ? 0 : 1;
}
