// wht_cuda_cpucheck.cpp -- CPU check of wht_cuda.cu's device code (stage indexing, shared-memory padding, the
// generated circuit kernels), compiled as plain C++ with HOST_EMU.  Threads of one stage are independent (each owns
// R positions), so running them one after another between stages is exactly the GPU's semantics.
// Build: clang++ -std=c++17 -O1 wht_cuda_cpucheck.cpp -o cpucheck && ./cpucheck
#define HOST_EMU
#include "wht_cuda.cu"
#include <vector>
static void ref(double *x, int n) {
  for (int h = 1; h < n; h <<= 1)
    for (int i = 0; i < n; i += 2 * h)
      for (int j = i; j < i + h; j++) { double a = x[j], b = x[j + h]; x[j] = a + b; x[j + h] = a - b; }
}
template <int N, int R, int KID> static int run(const char *nm, int broken) {
  std::vector<float> sm(N + N / 32);
  std::vector<double> x(N);
  for (int i = 0; i < N; i++) { x[i] = (double)((rand() % 17) - 8); sm[pad(i)] = (float)x[i]; }
  for (int S = 1; S < N; S *= R)
    for (int t = 0; t < N / R; t++) stage<R, KID>(sm.data(), t, S);
  if (broken) sm[pad(N / 2 + 1)] += 1.0f;
  ref(x.data(), N);
  long bad = 0;
  for (int i = 0; i < N; i++) bad += (x[i] != (double)sm[pad(i)]);
  printf("CPUCHECK N=%-5d R=%-2d %-6s %s: %ld wrong of %d  %s\n", N, R, nm, broken ? "(broken copy)" : "", bad, N,
         broken ? (bad ? "CAUGHT" : "NOT CAUGHT") : (bad ? "FAIL" : "PASS"));
  return broken ? bad != 0 : bad == 0;
}
int main() {
  int ok = 1;
  ok &= run<256, 16, 0>("tb16", 0); ok &= run<256, 16, 1>("g52", 0); ok &= run<256, 16, 2>("g56d6", 0);
  ok &= run<4096, 16, 0>("tb16", 0); ok &= run<4096, 16, 1>("g52", 0); ok &= run<4096, 16, 2>("g56d6", 0);
  ok &= run<512, 8, 0>("tb8", 0); ok &= run<512, 8, 1>("g19", 0); ok &= run<512, 8, 2>("g22d4", 0);
  ok &= run<4096, 8, 0>("tb8", 0); ok &= run<4096, 8, 1>("g19", 0); ok &= run<4096, 8, 2>("g22d4", 0);
  ok &= run<4096, 16, 1>("g52", 1);
  printf("ALL %s\n", ok ? "PASS" : "FAIL");
  return !ok;
}
