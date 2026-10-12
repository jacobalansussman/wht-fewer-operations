// anneal.c  (e-7-halftouch)  exact integer search.
// Minimise the number of non-zero entries of  S = H_N - A * C * B
// A is N x m, B is m x N, entries from a small value set (half-units: stored integer v means v/2),
// C is the "child" (mode 0: H_(N/2); 1: I2 (x) H_(N/2) [calibration, 0 reachable]; 2: I2 (x) H_(N/4);
//                    3: H_(N/2) (+) H_(N/4); 4: I3 (x) H_(N/4)).
// limits: ra = non-zeros per row of A, ca = per column of A, rb = per row of B, cb = per column of B.
// usage: anneal k mode ra ca rb cb steps restarts seed valset [T0 T1]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#define MX 64
static int N, m;
static int C[MX][MX], Ht[MX][MX], A[MX][MX], B[MX][MX], bA[MX][MX], bB[MX][MX];
static long F[MX][MX], G[MX][MX], M[MX][MX];
static int rowA[MX], colA[MX], rowB[MX], colB[MX];
static uint64_t s0 = 88172645463325252ULL;
static inline uint64_t rnd(void){ s0 ^= s0 << 13; s0 ^= s0 >> 7; s0 ^= s0 << 17; return s0; }
static inline double urnd(void){ return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
static int par(int x){ return __builtin_popcount(x) & 1; }
static void putH(int r0, int c0, int n){ for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) C[r0+i][c0+j] = par(i & j) ? -1 : 1; }
int main(int argc, char **argv){
  if (argc < 11){ fprintf(stderr, "args\n"); return 2; }
  int k = atoi(argv[1]), mode = atoi(argv[2]), ra = atoi(argv[3]), ca = atoi(argv[4]), rb = atoi(argv[5]), cb = atoi(argv[6]);
  long steps = atol(argv[7]); int restarts = atoi(argv[8]); s0 ^= (uint64_t)atol(argv[9]) * 0x9E3779B97F4A7C15ULL; int vs = atoi(argv[10]);
  double T0 = argc > 11 ? atof(argv[11]) : 1.5, T1 = argc > 12 ? atof(argv[12]) : 0.08;
  N = 1 << k; memset(C, 0, sizeof C);
  if (mode == 0){ m = N/2; putH(0,0,N/2); }
  else if (mode == 1){ m = N; putH(0,0,N/2); putH(N/2,N/2,N/2); }
  else if (mode == 2){ m = N/2; putH(0,0,N/4); putH(N/4,N/4,N/4); }
  else if (mode == 3){ m = 3*N/4; putH(0,0,N/2); putH(N/2,N/2,N/4); }
  else { m = 3*N/4; putH(0,0,N/4); putH(N/4,N/4,N/4); putH(N/2,N/2,N/4); }
  int vals[16], nv = 0;
  if (vs == 0){ int v[] = {0,2,-2}; nv = 3; memcpy(vals, v, sizeof v); }                       // 0, +-1
  else if (vs == 1){ int v[] = {0,1,-1,2,-2,4,-4}; nv = 7; memcpy(vals, v, sizeof v); }        // 0, +-1/2, +-1, +-2
  else { int v[] = {0,1,-1,2,-2,3,-3,4,-4,6,-6,8,-8}; nv = 13; memcpy(vals, v, sizeof v); }    // more
  for (int x = 0; x < N; x++) for (int y = 0; y < N; y++) Ht[x][y] = 4 * (par(x & y) ? -1 : 1);
  int best = N*N + 1;
  for (int r = 0; r < restarts; r++){
    memset(A,0,sizeof A); memset(B,0,sizeof B); memset(F,0,sizeof F); memset(G,0,sizeof G); memset(M,0,sizeof M);
    memset(rowA,0,sizeof rowA); memset(colA,0,sizeof colA); memset(rowB,0,sizeof rowB); memset(colB,0,sizeof colB);
    int cost = N*N, rbest = cost;
    double T = T0, mul = pow(T1/T0, 1.0/(double)steps);
    for (long st = 0; st < steps; st++, T *= mul){
      if (rnd() & 1){
        int x = rnd() % N, i = rnd() % m, old = A[x][i], nw = vals[rnd() % nv]; if (nw == old) continue;
        if (old == 0 && (rowA[x] >= ra || colA[i] >= ca)) continue;
        int d = nw - old, dc = 0;
        for (int y = 0; y < N; y++){ long g = G[i][y]; if (!g) continue; long a0 = M[x][y], a1 = a0 + d*g; dc += (a1 != Ht[x][y]) - (a0 != Ht[x][y]); }
        if (dc > 0 && urnd() >= exp(-dc / T)) continue;
        for (int y = 0; y < N; y++) M[x][y] += d * G[i][y];
        for (int j = 0; j < m; j++) F[x][j] += d * C[i][j];
        A[x][i] = nw; if (old == 0){ rowA[x]++; colA[i]++; } if (nw == 0){ rowA[x]--; colA[i]--; } cost += dc;
      } else {
        int j = rnd() % m, y = rnd() % N, old = B[j][y], nw = vals[rnd() % nv]; if (nw == old) continue;
        if (old == 0 && (rowB[j] >= rb || colB[y] >= cb)) continue;
        int d = nw - old, dc = 0;
        for (int x = 0; x < N; x++){ long f = F[x][j]; if (!f) continue; long a0 = M[x][y], a1 = a0 + d*f; dc += (a1 != Ht[x][y]) - (a0 != Ht[x][y]); }
        if (dc > 0 && urnd() >= exp(-dc / T)) continue;
        for (int x = 0; x < N; x++) M[x][y] += d * F[x][j];
        for (int i = 0; i < m; i++) G[i][y] += d * C[i][j];
        B[j][y] = nw; if (old == 0){ rowB[j]++; colB[y]++; } if (nw == 0){ rowB[j]--; colB[y]--; } cost += dc;
      }
      if (cost < rbest){ rbest = cost; if (cost < best){ best = cost; memcpy(bA,A,sizeof A); memcpy(bB,B,sizeof B); } }
    }
    fprintf(stderr, "restart %d: best of run %d, overall %d\n", r, rbest, best);
  }
  printf("k %d N %d mode %d m %d limits %d %d %d %d valset %d best_nnz %d\n", k, N, mode, m, ra, ca, rb, cb, vs, best);
  printf("A\n"); for (int x = 0; x < N; x++){ for (int i = 0; i < m; i++) printf("%d ", bA[x][i]); printf("\n"); }
  printf("B\n"); for (int j = 0; j < m; j++){ for (int y = 0; y < N; y++) printf("%d ", bB[j][y]); printf("\n"); }
  return 0;
}
