// ab-2-tallpool/tallmin.c : the smallest matrix for which a TALL intermediate wire saves a gate.  Count (G): a gate is any
// a*u + b*v, scalings free; a wire is a point of projective space (a primitive whole-number vector up to sign); a gate puts a new
// point on the line through two points already held.  Gates of a circuit = number of its non-input wires.
// For every set T of m targets of height 1 (entries 0, +1, -1) on NN inputs, up to signed permutations of the inputs:
//   h1 = least number of helper wires when every helper has height 1 (exhaustive);
//   then: is there a circuit with h1 - 1 helpers when helpers may be tall (all but the last helper of height <= MT, exhaustive;
//   the LAST helper of any height up to MLAST: it is found as the meeting point of two lines, so no pool is needed for it).
// usage: tallmin m MT MLAST [full: 1 = targets with no zero entry only] [hcap]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#ifndef NN
#define NN 4
#endif
typedef struct { int e[NN]; } vec;
static int igcd(int a, int b) { a = abs(a); b = abs(b); while (b) { int t = a % b; a = b; b = t; } return a; }
static int norm(vec *v) { int g = 0, s = 0, i; for (i = 0; i < NN; i++) g = igcd(g, v->e[i]); if (!g) return 0;
  for (i = 0; i < NN; i++) if (v->e[i]) { s = v->e[i] > 0 ? 1 : -1; break; }
  for (i = 0; i < NN; i++) v->e[i] = s * v->e[i] / g; return 1; }
static int height(const vec *v) { int h = 0; for (int i = 0; i < NN; i++) if (abs(v->e[i]) > h) h = abs(v->e[i]); return h; }
static int eq(const vec *a, const vec *b) { return !memcmp(a, b, sizeof(vec)); }
// is w in the span of u and v (u, v not parallel)
static int coll(const vec *u, const vec *v, const vec *w) {
  for (int i = 0; i < NN; i++) for (int j = i + 1; j < NN; j++) { long D = (long)u->e[i] * v->e[j] - (long)u->e[j] * v->e[i];
    if (D) { long a = (long)w->e[i] * v->e[j] - (long)w->e[j] * v->e[i], b = (long)u->e[i] * w->e[j] - (long)u->e[j] * w->e[i];
      for (int l = 0; l < NN; l++) if (D * w->e[l] != a * u->e[l] + b * v->e[l]) return 0; return 1; } }
  return 0; }
// meeting point of line(u,v) and line(t,d); 0 if they do not meet in exactly one point
static int meet(const vec *u, const vec *v, const vec *t, const vec *d, vec *c) {
  long M[NN][4]; for (int l = 0; l < NN; l++) { M[l][0] = u->e[l]; M[l][1] = v->e[l]; M[l][2] = -t->e[l]; M[l][3] = -d->e[l]; }
  for (int a = 0; a < NN; a++) for (int b = a + 1; b < NN; b++) for (int g = b + 1; g < NN; g++) {
    long *r0 = M[a], *r1 = M[b], *r2 = M[g], nu[4];
#define DET3(i,j,k) (r0[i]*(r1[j]*r2[k]-r1[k]*r2[j]) - r0[j]*(r1[i]*r2[k]-r1[k]*r2[i]) + r0[k]*(r1[i]*r2[j]-r1[j]*r2[i]))
    nu[0] = DET3(1,2,3); nu[1] = -DET3(0,2,3); nu[2] = DET3(0,1,3); nu[3] = -DET3(0,1,2);
    if (!nu[0] && !nu[1] && !nu[2] && !nu[3]) continue;
    for (int l = 0; l < NN; l++) if (M[l][0]*nu[0] + M[l][1]*nu[1] + M[l][2]*nu[2] + M[l][3]*nu[3]) return 0;
    long big = 0; long t2[NN]; for (int l = 0; l < NN; l++) { t2[l] = nu[0]*u->e[l] + nu[1]*v->e[l]; if (labs(t2[l]) > big) big = labs(t2[l]); }
    if (!big) return 0;
    long gg = 0; for (int l = 0; l < NN; l++) { long x = labs(t2[l]), y = gg; while (x) { long z = y % x; y = x; x = z; } gg = y; }
    for (int l = 0; l < NN; l++) { long x = t2[l] / gg; if (labs(x) > 1000000) return 0; c->e[l] = (int)x; }
    return norm(c); }
  return 0; }
static vec D[64]; static int nd;
static vec T[10]; static int m; static char done[10];
static vec POOL[70000]; static int np; static int MPOOL = 1, MLAST = 1;
static vec trail[10]; static int ntrail; static vec besttrail[10]; static int nbest;
static int isderived(const vec *c) { for (int i = 0; i < nd; i++) if (eq(&D[i], c)) return 1; return 0; }
static int istarget(const vec *c) { for (int i = 0; i < m; i++) if (eq(&T[i], c)) return 1; return 0; }
static void closure(void) { int ch = 1; while (ch) { ch = 0; for (int t = 0; t < m; t++) if (!done[t]) {
    int ok = 0; for (int i = 0; i < nd && !ok; i++) for (int j = i + 1; j < nd && !ok; j++) if (coll(&D[i], &D[j], &T[t])) ok = 1;
    if (ok) { done[t] = 1; D[nd++] = T[t]; ch = 1; } } } }
static int dfs(int hleft) {
  int snd = nd; char sdone[10]; memcpy(sdone, done, 10);
  closure(); int all = 1; for (int t = 0; t < m; t++) if (!done[t]) all = 0;
  if (all) { nbest = ntrail; memcpy(besttrail, trail, sizeof(trail)); nd = snd; memcpy(done, sdone, 10); return 1; }
  if (hleft == 0) { nd = snd; memcpy(done, sdone, 10); return 0; }
  int n0 = nd;
  if (hleft == 1) {
    for (int i = 0; i < n0; i++) for (int j = i + 1; j < n0; j++) for (int t = 0; t < m; t++) if (!done[t]) for (int d = 0; d < n0; d++) {
      vec c; if (!meet(&D[i], &D[j], &T[t], &D[d], &c)) continue; if (height(&c) > MLAST) continue; if (isderived(&c) || istarget(&c)) continue;
      D[nd++] = c; trail[ntrail++] = c; int r = dfs(0); ntrail--; nd = n0; if (r) { nd = snd; memcpy(done, sdone, 10); return 1; } }
  } else {
    for (int p = 0; p < np; p++) { const vec *c = &POOL[p]; if (height(c) > MPOOL) continue; if (isderived(c) || istarget(c)) continue;
      int ok = 0; for (int i = 0; i < n0 && !ok; i++) for (int j = i + 1; j < n0 && !ok; j++) if (coll(&D[i], &D[j], c)) ok = 1;
      if (!ok) continue;
      D[nd++] = *c; trail[ntrail++] = *c; int r = dfs(hleft - 1); ntrail--; nd = n0; if (r) { nd = snd; memcpy(done, sdone, 10); return 1; } }
  }
  nd = snd; memcpy(done, sdone, 10); return 0; }
static void reset(void) { nd = 0; for (int i = 0; i < NN; i++) { memset(&D[nd], 0, sizeof(vec)); D[nd].e[i] = 1; nd++; } memset(done, 0, 10); ntrail = 0; }
static void pv(const vec *v) { printf("("); for (int i = 0; i < NN; i++) printf("%d%s", v->e[i], i + 1 < NN ? "," : ")"); }
static vec C[512]; static int nc; static int *act; static int ng;
static int cidx(const vec *v) { for (int i = 0; i < nc; i++) if (eq(&C[i], v)) return i; return -1; }
static int cmpi(const void *a, const void *b) { return *(const int *)a - *(const int *)b; }
int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage: tallmin m MT MLAST [full] [hcap]\n"); return 2; }
  m = atoi(argv[1]); int MT = atoi(argv[2]), ML = atoi(argv[3]); int full = argc > 4 ? atoi(argv[4]) : 0; int hcap = argc > 5 ? atoi(argv[5]) : 5;
  // pool of all primitive points of height <= MT
  { int tot = 1; for (int i = 0; i < NN; i++) tot *= (2 * MT + 1);
    for (int x = 0; x < tot; x++) { vec v; int y = x; for (int i = 0; i < NN; i++) { v.e[i] = y % (2 * MT + 1) - MT; y /= (2 * MT + 1); }
      vec w = v; if (!norm(&w)) continue; if (!eq(&w, &v)) continue; int sup = 0; for (int i = 0; i < NN; i++) if (v.e[i]) sup++;
      if (sup < 2) continue; POOL[np++] = v;
      if (height(&v) == 1 && (!full || sup == NN)) C[nc++] = v; } }
  // signed permutations acting on the candidate targets
  { int perm[NN]; for (int i = 0; i < NN; i++) perm[i] = i; int nperm = 1; for (int i = 2; i <= NN; i++) nperm *= i;
    act = malloc(sizeof(int) * nperm * (1 << NN) * nc); ng = 0;
    for (int pi = 0; pi < nperm; pi++) {
      for (int s = 0; s < (1 << NN); s++) { for (int c = 0; c < nc; c++) { vec w; for (int i = 0; i < NN; i++) w.e[perm[i]] = ((s >> i) & 1) ? -C[c].e[i] : C[c].e[i]; norm(&w); act[ng * nc + c] = cidx(&w); } ng++; }
      // next permutation
      int i = NN - 2; while (i >= 0 && perm[i] > perm[i + 1]) i--; if (i < 0) break; int j = NN - 1; while (perm[j] < perm[i]) j--; int t = perm[i]; perm[i] = perm[j]; perm[j] = t;
      for (int a = i + 1, b = NN - 1; a < b; a++, b--) { t = perm[a]; perm[a] = perm[b]; perm[b] = t; } } }
  printf("# tallmin NN=%d m=%d pool(height<=%d)=%d candidates targets=%d group=%d MLAST=%d full=%d hcap=%d\n", NN, m, MT, np, nc, ng, ML, full, hcap);
  int idx[10]; for (int i = 0; i < m; i++) idx[i] = i; long orbits = 0, saved = 0, capped = 0; long hist[12] = {0};
  for (;;) {
    // canonical?
    int canon = 1; for (int g = 0; g < ng && canon; g++) { int im[10]; for (int i = 0; i < m; i++) im[i] = act[g * nc + idx[i]]; qsort(im, m, sizeof(int), cmpi);
      for (int i = 0; i < m; i++) { if (im[i] < idx[i]) { canon = 0; break; } if (im[i] > idx[i]) break; } }
    if (canon) { orbits++; for (int i = 0; i < m; i++) T[i] = C[idx[i]];
      int h1 = -1; MPOOL = 1; MLAST = 1; for (int h = 0; h <= hcap; h++) { reset(); if (dfs(h)) { h1 = h; break; } }
      if (getenv("VERB")) { printf("ORBIT h1=%d:", h1); for (int i = 0; i < m; i++) { printf(" "); pv(&T[i]); } printf("\n"); }
      if (h1 < 0) { capped++; }
      else { hist[h1]++; vec f1[10]; int nf1 = nbest; memcpy(f1, besttrail, sizeof(f1));
        if (h1 >= 1) { MPOOL = MT; MLAST = ML; reset(); if (dfs(h1 - 1)) { saved++;
            printf("SAVE targets:"); for (int i = 0; i < m; i++) { printf(" "); pv(&T[i]); } printf("  forms: %d helpers =", h1); for (int i = 0; i < nf1; i++) { printf(" "); pv(&f1[i]); }
            printf("  | tall: %d helpers =", h1 - 1); for (int i = 0; i < nbest; i++) { printf(" "); pv(&besttrail[i]); } printf("\n"); fflush(stdout);
            if (h1 >= 2) { reset(); if (dfs(h1 - 2)) { printf("SAVE2 (two gates saved) targets:"); for (int i = 0; i < m; i++) { printf(" "); pv(&T[i]); } printf(" | tall: %d helpers =", h1 - 2); for (int i = 0; i < nbest; i++) { printf(" "); pv(&besttrail[i]); } printf("\n"); } } } } } }
    int i = m - 1; while (i >= 0 && idx[i] == nc - m + i) i--; if (i < 0) break; idx[i]++; for (int j = i + 1; j < m; j++) idx[j] = idx[j - 1] + 1; }
  printf("# orbits=%ld  forms helpers histogram:", orbits); for (int h = 0; h <= hcap; h++) printf(" h=%d:%ld", h, hist[h]); printf("  above cap=%ld\n# target sets (orbits) where a tall wire saves a gate: %ld\n", capped, saved);
  return 0; }
