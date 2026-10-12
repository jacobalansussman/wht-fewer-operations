// rt.c: ROUND TRIPS of the entropy meter on n wires, in place.  x-8-nearlydependent, 11 Oct 2026.
// State: n x n whole-number matrix, rows = wires; rows kept primitive (no common factor), first non-zero entry positive, rows sorted
//   (scaling, sign and order of wires are free: count (G), in place).
// Move: row_i <- a*row_i + b*row_j, (a,b) from a list: T=1: (1,+-1);  T=2: also (1,+-2), (2,+-1).
// Meter: p_il = M_il (M^-1)_li ; Phi = - sum p log2|p| ; rowmass = max over rows of sum_l |p_il| (1 exactly when the row has no negative p).
// For every depth m (breadth-first, every state at its least depth) print:
//   new states; PUMP = max |Phi|; LAND = max Phi over states with every p in [0,1]; ORTH = max Phi over states with orthogonal rows.
// Option RMAX: only states with rowmass <= RMAX are EXPANDED (the way must stay that well conditioned); end states are unrestricted.
// Phi and p are floating point measurements of exact states; the orthogonality test is exact.
// usage: rt n T maxdepth RMAX(0 = no limit) [maxstates]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#define NMAX 5
typedef int16_t ent;
static int n, T; static size_t SZ;
static ent *pool; static size_t npool = 0, cappool;
static uint32_t *tab; static size_t tabsz;
static int gcd(int a, int b){ a = abs(a); b = abs(b); while(b){ int t = a % b; a = b; b = t; } return a; }
static int rowcmp(const void *x, const void *y){ return memcmp(x, y, sizeof(ent)*n); }
static int canon(ent *M){ // returns 0 if a row is zero
  for(int i = 0; i < n; i++){ ent *r = M + i*n; int g = 0, f = 0; for(int l = 0; l < n; l++){ g = gcd(g, r[l]); if(!f && r[l]) f = r[l]; }
    if(!g) return 0; if(f < 0) g = -g; for(int l = 0; l < n; l++) r[l] /= g; }
  // sort rows by a comparison that is a total order: compare as signed values
  for(int i = 1; i < n; i++) for(int j = i; j > 0; j--){ ent *a = M + (j-1)*n, *b = M + j*n; int c = 0; for(int l = 0; l < n && !c; l++) c = (a[l] > b[l]) - (a[l] < b[l]);
      if(c > 0){ ent t[NMAX]; memcpy(t, a, sizeof(ent)*n); memcpy(a, b, sizeof(ent)*n); memcpy(b, t, sizeof(ent)*n); } else break; }
  return 1; }
static uint64_t hsh(const ent *M){ uint64_t h = 1469598103934665603ULL; for(int i = 0; i < n*n; i++){ h ^= (uint16_t)M[i]; h *= 1099511628211ULL; h ^= h >> 29; } return h; }
static int insert(const ent *M){ // 1 if new
  uint64_t h = hsh(M) % tabsz;
  while(tab[h]){ if(!memcmp(pool + (size_t)(tab[h]-1)*SZ, M, sizeof(ent)*SZ)) return 0; if(++h == tabsz) h = 0; }
  if(npool >= cappool) { fprintf(stderr, "pool full\n"); return -1; }
  memcpy(pool + npool*SZ, M, sizeof(ent)*SZ); tab[h] = (uint32_t)(++npool); return 1; }
static int meter(const ent *M, double *phi, double *rowmass, int *landed, double *minp){ // 0 if singular
  double A[NMAX][2*NMAX];
  for(int i = 0; i < n; i++) for(int l = 0; l < n; l++){ A[i][l] = M[i*n+l]; A[i][n+l] = (i == l); }
  for(int c = 0; c < n; c++){ int p = c; for(int i = c+1; i < n; i++) if(fabs(A[i][c]) > fabs(A[p][c])) p = i;
    if(fabs(A[p][c]) < 1e-9) return 0;
    if(p != c) for(int l = 0; l < 2*n; l++){ double t = A[c][l]; A[c][l] = A[p][l]; A[p][l] = t; }
    double d = A[c][c]; for(int l = 0; l < 2*n; l++) A[c][l] /= d;
    for(int i = 0; i < n; i++) if(i != c){ double f = A[i][c]; if(f != 0) for(int l = 0; l < 2*n; l++) A[i][l] -= f*A[c][l]; } }
  double s = 0, rm = 0, mp = 1e9; int ld = 1;
  for(int i = 0; i < n; i++){ double m1 = 0; for(int l = 0; l < n; l++){ double p = M[i*n+l]*A[l][n+i];
      if(fabs(p) > 1e-12) s -= p*log2(fabs(p)); m1 += fabs(p); if(p < -1e-9 || p > 1 + 1e-9) ld = 0; if(p < mp) mp = p; }
    if(m1 > rm) rm = m1; }
  *phi = s; *rowmass = rm; *landed = ld; *minp = mp; return 1; }
static int orth(const ent *M){ for(int i = 0; i < n; i++) for(int j = i+1; j < n; j++){ long d = 0; for(int l = 0; l < n; l++) d += (long)M[i*n+l]*M[j*n+l]; if(d) return 0; } return 1; }
static void show(const ent *M){ for(int i = 0; i < n; i++){ printf("("); for(int l = 0; l < n; l++) printf("%d%s", M[i*n+l], l < n-1 ? "," : ")"); } }
int main(int argc, char **argv){
  n = atoi(argv[1]); T = atoi(argv[2]); int maxd = atoi(argv[3]); double RMAX = atof(argv[4]);
  cappool = argc > 5 ? strtoull(argv[5], 0, 10) : 40000000ULL; SZ = n*n;
  pool = malloc(cappool*SZ*sizeof(ent)); tabsz = cappool*2 + 7; tab = calloc(tabsz, sizeof(uint32_t));
  int ca[400], cb[400]; int nc = 0;   // rt3: every pair (a,b) without common factor, 1 <= a <= T, 1 <= |b| <= T
  for(int a = 1; a <= T; a++) for(int b = 1; b <= T; b++) if(gcd(a, b) == 1){ ca[nc] = a; cb[nc++] = b; ca[nc] = a; cb[nc++] = -b; }
  ent I[NMAX*NMAX]; memset(I, 0, sizeof I); for(int i = 0; i < n; i++) I[i*n+i] = 1;
  if(argc > 6 + n*n - 1){ for(int i = 0; i < n*n; i++) I[i] = (ent)atoi(argv[6+i]); printf("# START STATE given on the command line\n"); }
  canon(I); insert(I);
  printf("# n=%d wires, coefficients up to %d, in place; way restricted to rowmass <= %s\n", n, T, RMAX > 0 ? argv[4] : "infinity");
  printf("# m new | up = max Phi (positive side) | PUMP max|Phi| (per move) | LAND max Phi with all p in [0,1] (per move) | ORTH max Phi, orthogonal rows (per move) | max rowmass | witnesses\n");
  size_t lo = 0, hi = 1; int full = 0;
  for(int m = 1; m <= maxd && !full; m++){
    for(size_t s = lo; s < hi && !full; s++){
      if(RMAX > 0){ double f, rm, mp; int ld; if(!meter(pool + s*SZ, &f, &rm, &ld, &mp) || rm > RMAX + 1e-9) continue; }
      for(int i = 0; i < n && !full; i++) for(int j = 0; j < n; j++) if(i != j) for(int c = 0; c < nc; c++){
        ent R[NMAX*NMAX]; memcpy(R, pool + s*SZ, sizeof(ent)*SZ); int ok = 1;
        for(int l = 0; l < n; l++){ int v = ca[c]*R[i*n+l] + cb[c]*R[j*n+l]; if(v > 30000 || v < -30000) ok = 0; R[i*n+l] = (ent)v; }
        if(!ok || !canon(R)) continue; if(insert(R) < 0){ full = 1; break; } } }
    lo = hi; hi = npool;
    double bp = 0, bl = -1, bo = -1, brm = 0, bpos = 0; size_t wp = lo, wl = lo, wo = lo; int hl = 0, ho = 0;
    for(size_t s = lo; s < hi; s++){ double f, rm, mp; int ld; if(!meter(pool + s*SZ, &f, &rm, &ld, &mp)) continue;
      if(fabs(f) > fabs(bp)){ bp = f; wp = s; } if(f > bpos) bpos = f; if(rm > brm) brm = rm;
      if(ld && f > bl){ bl = f; wl = s; hl = 1; }
      if(orth(pool + s*SZ) && f > bo){ bo = f; wo = s; ho = 1; } }
    printf("%d %zu | up %.3f | %.3f (%.3f) | %.3f (%.3f) | %.3f (%.3f) | %.1f | pump ", m, hi - lo, bpos, bp, fabs(bp)/m, hl ? bl : 0.0, hl ? bl/m : 0.0, ho ? bo : 0.0, ho ? bo/m : 0.0, brm);
    show(pool + wp*SZ); if(hl){ printf(" land "); show(pool + wl*SZ); } if(ho){ printf(" orth "); show(pool + wo*SZ); } printf("%s\n", full ? "  [POOL FULL: this depth incomplete]" : ""); fflush(stdout); }
  return 0; }
