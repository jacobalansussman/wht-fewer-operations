// d-2-letters: complex Levenberg-Marquardt for words  D0 * T1 * D1 * T2 * D2 * ... * Tm * Dm = target,
// T_i = W_i * diag(c_i) * W_i^T (W_i given: an orthonormal many-scale basis), D_i = diag(d_i).  All unknowns complex.
// stdin: repeated cases:  N m restarts seed tag ; then m matrices W_i (N*N reals, row major) ; then target (N*N reals).
// stdout per case: tag, best residual, #converged, and for the first converged start: nullity of the Jacobian (solution-family
// dimension = nullity - 2m gauge scalings), and for every diagonal the ratio max|.|/min|.| and "nonscalar" = max |d_z/d_0 - 1|.
// FLOATING POINT: a discovery instrument, not a proof.
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <complex.h>
#include <string.h>
typedef double complex cd;
static int N, m, P, F;
static double *W;      // m * N * N
static cd *tgt, *x, *xn, *Lp, *Rs, *UU, *VV, *M, *R, *A, *g, *del, *tmp, *A2;
static unsigned long long rs;
static double rnd(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (rs >> 11) * (1.0 / 9007199254740992.0); }
#define IX(a,b) ((a)*N+(b))
static void mul(cd *C, const cd *Aa, const cd *B){ // C = Aa*B (N x N)
  for (int i = 0; i < N; i++) for (int j = 0; j < N; j++){ cd s = 0; for (int l = 0; l < N; l++) s += Aa[IX(i,l)] * B[IX(l,j)]; C[IX(i,j)] = s; } }
static void factor(cd *Fm, int j, const cd *xx){ // factor j of the word as a dense matrix
  if (j % 2 == 0){ memset(Fm, 0, sizeof(cd)*N*N); for (int z = 0; z < N; z++) Fm[IX(z,z)] = xx[j*N+z]; }
  else { const double *w = W + ((j-1)/2)*N*N;
    for (int i = 0; i < N; i++) for (int l = 0; l < N; l++){ cd s = 0; for (int a = 0; a < N; a++) s += w[IX(i,a)] * xx[j*N+a] * w[IX(l,a)]; Fm[IX(i,l)] = s; } } }
static double eval(const cd *xx, int full){ // builds M, R; if full also UU (N x P), VV (P x N)
  cd *Fm = tmp, *T2 = tmp + N*N;
  // prefix
  for (int i = 0; i < N*N; i++) Lp[i] = 0; for (int i = 0; i < N; i++) Lp[IX(i,i)] = 1;
  for (int j = 0; j < F; j++){ factor(Fm, j, xx); mul(Lp + (j+1)*N*N, Lp + j*N*N, Fm); }
  memcpy(M, Lp + F*N*N, sizeof(cd)*N*N);
  double f = 0; for (int i = 0; i < N*N; i++){ R[i] = M[i] - tgt[i]; f += creal(R[i])*creal(R[i]) + cimag(R[i])*cimag(R[i]); }
  if (!full) return f;
  cd *S = Rs + (F-1)*N*N; for (int i = 0; i < N*N; i++) S[i] = 0; for (int i = 0; i < N; i++) S[IX(i,i)] = 1;
  for (int j = F-1; j >= 1; j--){ factor(Fm, j, xx); mul(Rs + (j-1)*N*N, Fm, Rs + j*N*N); }
  for (int j = 0; j < F; j++){
    const cd *L = Lp + j*N*N, *Rr = Rs + j*N*N;
    if (j % 2 == 0){ for (int a = 0; a < N; a++) for (int r = 0; r < N; r++){ UU[r*P + j*N+a] = L[IX(r,a)]; VV[(j*N+a)*N + r] = Rr[IX(a,r)]; } }
    else { const double *w = W + ((j-1)/2)*N*N;
      for (int a = 0; a < N; a++) for (int r = 0; r < N; r++){ cd s = 0, t = 0; for (int l = 0; l < N; l++){ s += L[IX(r,l)] * w[IX(l,a)]; t += w[IX(l,a)] * Rr[IX(l,r)]; }
        UU[r*P + j*N+a] = s; VV[(j*N+a)*N + r] = t; } } }
  return f; }
static void normal(void){ // A = J^H J, g = J^H R
  for (int p = 0; p < P; p++) for (int q = p; q < P; q++){ cd su = 0, sv = 0;
      for (int r = 0; r < N; r++){ su += conj(UU[r*P+p]) * UU[r*P+q]; sv += conj(VV[p*N+r]) * VV[q*N+r]; }
      A[p*P+q] = su * sv; A[q*P+p] = conj(su * sv); }
  for (int p = 0; p < P; p++){ cd s = 0; for (int r = 0; r < N; r++){ cd t = 0; for (int c = 0; c < N; c++) t += R[IX(r,c)] * conj(VV[p*N+c]); s += conj(UU[r*P+p]) * t; } g[p] = s; } }
static int solve(double mu){ // (A + mu*diag) del = -g, Gaussian elimination with partial pivoting
  memcpy(A2, A, sizeof(cd)*P*P); for (int p = 0; p < P; p++){ A2[p*P+p] += mu * (1.0 + cabs(A[p*P+p])); del[p] = -g[p]; }
  for (int c = 0; c < P; c++){ int b = c; double bv = cabs(A2[c*P+c]);
    for (int r = c+1; r < P; r++) if (cabs(A2[r*P+c]) > bv){ bv = cabs(A2[r*P+c]); b = r; }
    if (bv < 1e-300) return 0;
    if (b != c){ for (int l = 0; l < P; l++){ cd t = A2[c*P+l]; A2[c*P+l] = A2[b*P+l]; A2[b*P+l] = t; } cd t = del[c]; del[c] = del[b]; del[b] = t; }
    for (int r = c+1; r < P; r++){ cd fct = A2[r*P+c] / A2[c*P+c]; if (fct == 0) continue; for (int l = c; l < P; l++) A2[r*P+l] -= fct * A2[c*P+l]; del[r] -= fct * del[c]; } }
  for (int c = P-1; c >= 0; c--){ cd s = del[c]; for (int l = c+1; l < P; l++) s -= A2[c*P+l] * del[l]; del[c] = s / A2[c*P+c]; }
  return 1; }
static int nullity(void){ // pivoted Cholesky-like elimination on A (Hermitian PSD): count pivots below 1e-9 * largest
  memcpy(A2, A, sizeof(cd)*P*P); double big = 0; for (int p = 0; p < P; p++) if (creal(A2[p*P+p]) > big) big = creal(A2[p*P+p]);
  char *used = calloc(P, 1); int rank = 0;
  for (int it = 0; it < P; it++){ int b = -1; double bv = 1e-9 * big;
    for (int p = 0; p < P; p++) if (!used[p] && creal(A2[p*P+p]) > bv){ bv = creal(A2[p*P+p]); b = p; }
    if (b < 0) break; used[b] = 1; rank++;
    for (int r = 0; r < P; r++) if (!used[r]){ cd fct = A2[r*P+b] / A2[b*P+b]; for (int l = 0; l < P; l++) if (!used[l]) A2[r*P+l] -= fct * A2[b*P+l]; } }
  free(used); return P - rank; }
int main(void){
  int restarts; unsigned long long seed; char tag[256];
  while (scanf("%d %d %d %llu %255s", &N, &m, &restarts, &seed, tag) == 5){
    F = 2*m + 1; P = F * N; rs = seed * 2654435761ULL + 88172645463325252ULL;
    W = malloc(sizeof(double)*m*N*N); tgt = malloc(sizeof(cd)*N*N); x = malloc(sizeof(cd)*P); xn = malloc(sizeof(cd)*P);
    Lp = malloc(sizeof(cd)*(F+1)*N*N); Rs = malloc(sizeof(cd)*F*N*N); UU = malloc(sizeof(cd)*N*P); VV = malloc(sizeof(cd)*P*N);
    M = malloc(sizeof(cd)*N*N); R = malloc(sizeof(cd)*N*N); A = malloc(sizeof(cd)*P*P); A2 = malloc(sizeof(cd)*P*P); g = malloc(sizeof(cd)*P); del = malloc(sizeof(cd)*P); tmp = malloc(sizeof(cd)*2*N*N);
    for (int i = 0; i < m*N*N; i++) if (scanf("%lf", &W[i]) != 1) return 2;
    for (int i = 0; i < N*N; i++){ double t; if (scanf("%lf", &t) != 1) return 2; tgt[i] = t; }
    double best = 1e300; int nconv = 0, shown = 0; char info[4096] = "";
    for (int rep = 0; rep < restarts; rep++){
      for (int p = 0; p < P; p++){ double mod = exp(0.6 * (2*rnd() - 1)), ph = 6.283185307179586 * rnd(); x[p] = mod * cexp(I * ph); }
      double mu = 1e-2, f = eval(x, 1); int it;
      for (it = 0; it < 400 && f > 1e-22; it++){
        normal(); int ok = 0;
        for (int tr = 0; tr < 12; tr++){ if (!solve(mu)){ mu *= 10; continue; }
          for (int p = 0; p < P; p++) xn[p] = x[p] + del[p];
          double fn = eval(xn, 0);
          if (fn < f){ memcpy(x, xn, sizeof(cd)*P); mu *= 0.3; if (mu < 1e-14) mu = 1e-14; ok = 1; break; } mu *= 5; }
        if (!ok) break; f = eval(x, 1); }
      if (f < best) best = f;
      if (f < 1e-18){ nconv++;
        if (shown < 2){ shown++; eval(x, 1); normal(); int nul = nullity(); char *q = info + strlen(info);
          q += sprintf(q, " | sol%d nullity=%d family_dim=%d", shown, nul, nul - 2*m);
          for (int j = 0; j < F; j++){ double mx = 0, mn = 1e300, ns = 0; for (int z = 0; z < N; z++){ double a = cabs(x[j*N+z]); if (a > mx) mx = a; if (a < mn) mn = a; double d = cabs(x[j*N+z] / x[j*N] - 1); if (d > ns) ns = d; }
            q += sprintf(q, " %s%d[spread=%.3g nonscalar=%.3g]", j % 2 ? "c" : "d", j % 2 ? (j+1)/2 : j/2, mx / mn, ns); }
          if (getenv("LM_DUMP")){ q += sprintf(q, " x="); for (int p = 0; p < P && q - info < 3500; p++) q += sprintf(q, "%.6f%+.6fi,", creal(x[p]), cimag(x[p])); } } } }
    printf("%s N=%d m=%d best=%.3e conv=%d/%d%s\n", tag, N, m, best, nconv, restarts, info); fflush(stdout);
    free(W); free(tgt); free(x); free(xn); free(Lp); free(Rs); free(UU); free(VV); free(M); free(R); free(A); free(A2); free(g); free(del); free(tmp); }
  return 0; }
