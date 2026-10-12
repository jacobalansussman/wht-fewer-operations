// altmin.c (e-7-halftouch): alternating best fits over REAL coefficients (double precision; candidates are replayed exactly
// by replay2.py). Minimise the number of non-zero entries of S = H_N - A*C*B.
//   row step:    with G = C*B fixed, every row x of A is refitted: over all supports of size a among the m rows of G and all
//                a-subsets of positions (or nsamp random ones), solve for the coefficients that match h_x there, count matches.
//   column step: the same for every column y of B with F = A*C fixed.
//   when a sweep brings no gain: kick (re-randomise a few columns of B), keep the best seen.
// C by mode: 0 H_(N/2); 1 I2(x)H_(N/2) (calibration: zero is reachable); 2 I2(x)H_(N/4); 3 H_(N/2)(+)H_(N/4); 4 I3(x)H_(N/4);
//            5 I4(x)H_(N/4) (calibration); 6 H_(N/4) alone; 7 I7(x)H_(N/8); 8 identity of size N/2 (pure rank/rigidity question).
// usage: altmin k mode a b seconds seed nsamp [freediag [initfile]]   (initfile: an earlier output, used as the starting point)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include <time.h>
#define MX 64
static int N, m, freediag = 0;
static double C[MX][MX], H[MX][MX], A[MX][MX], B[MX][MX], F[MX][MX], G[MX][MX], bA[MX][MX], bB[MX][MX], V[MX][MX], tA[MX][MX], tB[MX][MX];
static uint64_t s0 = 88172645463325252ULL;
static inline uint64_t rnd(void){ s0 ^= s0 << 13; s0 ^= s0 >> 7; s0 ^= s0 << 17; return s0; }
static int par(int x){ return __builtin_popcount(x) & 1; }
static void putH(int o, int n){ for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) C[o+i][o+j] = par(i & j) ? -1 : 1; }
static int solve(int n, double M[6][7], double *sol){
  for (int c = 0; c < n; c++){
    int p = c; for (int r = c+1; r < n; r++) if (fabs(M[r][c]) > fabs(M[p][c])) p = r;
    if (fabs(M[p][c]) < 1e-9) return 0;
    if (p != c) for (int j = c; j <= n; j++){ double t = M[c][j]; M[c][j] = M[p][j]; M[p][j] = t; }
    for (int r = c+1; r < n; r++){ double f = M[r][c] / M[c][c]; if (f != 0) for (int j = c; j <= n; j++) M[r][j] -= f * M[c][j]; }
  }
  for (int c = n-1; c >= 0; c--){ double v = M[c][n]; for (int j = c+1; j < n; j++) v -= M[c][j] * sol[j]; sol[c] = v / M[c][c]; }
  return 1;
}
// fit target t[0..L) by at most a of the nb vectors V[i][0..L); skip position `skip` in the count if >= 0 (free diagonal)
static int fit(const double *t, int L, int nb, int a, int nsamp, int skip, int *bestI, double *bestc){
  int I[6], Y[6], best = -1, nties = 0; double M[6][7], sol[6];
  for (int i = 0; i < a; i++) I[i] = i;
  for (;;){
    // positions: exhaustive or sampled
    long cnt = 0; for (int i = 0; i < a; i++) Y[i] = i;
    for (;;){
      if (nsamp > 0){ for (int i = 0; i < a; i++){ again: Y[i] = rnd() % L; for (int j = 0; j < i; j++) if (Y[j] == Y[i]) goto again; } }
      for (int r = 0; r < a; r++){ for (int c = 0; c < a; c++) M[r][c] = V[I[c]][Y[r]]; M[r][a] = t[Y[r]]; }
      if (solve(a, M, sol)){
        int ag = 0;
        for (int p = 0; p < L; p++){ if (p == skip){ ag++; continue; } double v = -t[p]; for (int c = 0; c < a; c++) v += sol[c] * V[I[c]][p]; if (fabs(v) < 1e-7) ag++; }
        if (ag > best){ best = ag; nties = 1; memcpy(bestI, I, sizeof(int)*a); memcpy(bestc, sol, sizeof(double)*a); }
        else if (ag == best){ nties++; if (rnd() % nties == 0){ memcpy(bestI, I, sizeof(int)*a); memcpy(bestc, sol, sizeof(double)*a); } }
      }
      if (nsamp > 0){ if (++cnt >= nsamp) break; }
      else { int i = a-1; while (i >= 0 && Y[i] == L - a + i) i--; if (i < 0) break; Y[i]++; for (int j = i+1; j < a; j++) Y[j] = Y[j-1] + 1; }
    }
    int i = a-1; while (i >= 0 && I[i] == nb - a + i) i--; if (i < 0) break; I[i]++; for (int j = i+1; j < a; j++) I[j] = I[j-1] + 1;
  }
  return best;
}
static int rowstep(int a, int ns){
  for (int i = 0; i < m; i++) for (int y = 0; y < N; y++){ double v = 0; for (int j = 0; j < m; j++) v += C[i][j] * B[j][y]; G[i][y] = v; }
  for (int i = 0; i < m; i++) memcpy(V[i], G[i], sizeof(double)*N);
  int tot = 0, I[6]; double c[6];
  for (int x = 0; x < N; x++){ int ag = fit(H[x], N, m, a, ns, freediag ? x : -1, I, c); if (ag < 0) ag = 0; else { for (int i = 0; i < m; i++) A[x][i] = 0; for (int q = 0; q < a; q++) A[x][I[q]] = c[q]; } tot += N - ag; }
  return tot;
}
static int colstep(int b, int ns){
  for (int x = 0; x < N; x++) for (int j = 0; j < m; j++){ double v = 0; for (int i = 0; i < m; i++) v += A[x][i] * C[i][j]; F[x][j] = v; }
  for (int j = 0; j < m; j++) for (int x = 0; x < N; x++) V[j][x] = F[x][j];
  int tot = 0, I[6]; double c[6], t[MX];
  for (int y = 0; y < N; y++){ for (int x = 0; x < N; x++) t[x] = H[x][y]; int ag = fit(t, N, m, b, ns, freediag ? y : -1, I, c); if (ag < 0) ag = 0; else { for (int j = 0; j < m; j++) B[j][y] = 0; for (int q = 0; q < b; q++) B[I[q]][y] = c[q]; } tot += N - ag; }
  return tot;
}
static void randcol(int y, int b){ static const double vv[] = {1,-1,1,-1,0.5,-0.5,2,-2}; for (int j = 0; j < m; j++) B[j][y] = 0; for (int q = 0; q < b; q++) B[rnd() % m][y] = vv[rnd() % 8]; }
int main(int argc, char **argv){
  if (argc < 8){ fprintf(stderr, "usage\n"); return 2; }
  int k = atoi(argv[1]), mode = atoi(argv[2]), a = atoi(argv[3]), b = atoi(argv[4]); double secs = atof(argv[5]);
  s0 ^= (uint64_t)atol(argv[6]) * 0x9E3779B97F4A7C15ULL; rnd(); rnd(); int ns = atoi(argv[7]); if (argc > 8) freediag = atoi(argv[8]);
  N = 1 << k; memset(C, 0, sizeof C);
  if (mode == 0){ m = N/2; putH(0, N/2); }
  else if (mode == 1){ m = N; putH(0, N/2); putH(N/2, N/2); }
  else if (mode == 2){ m = N/2; putH(0, N/4); putH(N/4, N/4); }
  else if (mode == 3){ m = 3*N/4; putH(0, N/2); putH(N/2, N/4); }
  else if (mode == 4){ m = 3*N/4; for (int q = 0; q < 3; q++) putH(q*N/4, N/4); }
  else if (mode == 5){ m = N; for (int q = 0; q < 4; q++) putH(q*N/4, N/4); }
  else if (mode == 6){ m = N/4; putH(0, N/4); }
  else if (mode == 7){ m = 7*N/8; for (int q = 0; q < 7; q++) putH(q*N/8, N/8); }
  else { m = N/2; for (int i = 0; i < m; i++) C[i][i] = 1; }
  for (int x = 0; x < N; x++) for (int y = 0; y < N; y++) H[x][y] = par(x & y) ? -1 : 1;
  time_t t0 = time(0); int best = N*N + 1, cur = N*N + 1, stall = 0; long sweeps = 0, kicks = 0;
  memset(A, 0, sizeof A); for (int y = 0; y < N; y++) randcol(y, b);
  int hasinit = 0;
  if (argc > 9){ FILE *fp = fopen(argv[9], "r"); char buf[4096]; if (!fp){ fprintf(stderr, "no init file\n"); return 2; }
    if (!fgets(buf, sizeof buf, fp)) return 2; if (fscanf(fp, "%s", buf) != 1) return 2;
    for (int x = 0; x < N; x++) for (int i = 0; i < m; i++) if (fscanf(fp, "%lf", &A[x][i]) != 1) return 2;
    if (fscanf(fp, "%s", buf) != 1) return 2;
    for (int j = 0; j < m; j++) for (int y = 0; y < N; y++) if (fscanf(fp, "%lf", &B[j][y]) != 1) return 2;
    fclose(fp); hasinit = 1; memcpy(bA, A, sizeof A); memcpy(bB, B, sizeof B); }
  while (difftime(time(0), t0) < secs){
    int c1 = rowstep(a, ns); int c2 = colstep(b, ns); sweeps++;
    if (c2 < cur){ cur = c2; stall = 0; memcpy(tA, A, sizeof A); memcpy(tB, B, sizeof B); } else stall++;
    if (cur < best){ best = cur; memcpy(bA, A, sizeof A); memcpy(bB, B, sizeof B); fprintf(stderr, "sweep %ld kicks %ld: best %d\n", sweeps, kicks, best); if (best == 0) break; }
    if (stall >= 3){
      kicks++; stall = 0;
      if (kicks % 12 == 0 && !hasinit){ memset(A, 0, sizeof A); for (int y = 0; y < N; y++) randcol(y, b); cur = N*N + 1; }      // full restart
      else { if (cur > best + N/2 || (kicks % 3 == 0)){ memcpy(A, bA, sizeof A); memcpy(B, bB, sizeof B); } else { memcpy(A, tA, sizeof A); memcpy(B, tB, sizeof B); }
             int q = 1 + rnd() % 3; for (int i = 0; i < q; i++) randcol(rnd() % N, b); cur = N*N + 1; }
    }
  }
  printf("k %d N %d mode %d m %d a %d b %d freediag %d best_nnz %d sweeps %ld kicks %ld\n", k, N, mode, m, a, b, freediag, best, sweeps, kicks);
  printf("A\n"); for (int x = 0; x < N; x++){ for (int i = 0; i < m; i++) printf("%.17g ", bA[x][i]); printf("\n"); }
  printf("B\n"); for (int j = 0; j < m; j++){ for (int y = 0; y < N; y++) printf("%.17g ", bB[j][y]); printf("\n"); }
  return 0;
}
