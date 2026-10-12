// ag-6-deepgates/deepmin.c : least gates for a set of targets when the COEFFICIENTS of the gates are restricted and the
// heights of the wires are not.  Count (G).  A wire is a primitive whole-number vector up to sign.  A gate between held wires
// u, v makes the primitive wire w with  g*w = a*u + b*v,  a, b coprime whole numbers, g > 0.  A class of circuits is given by
//   AMASK : the allowed sizes of a and b (bit s set = size s allowed; 6 = {1,2}; 22 = {1,2,4}; 278 = {1,2,4,8}; 14 = {1,2,3})
//   DIV   : 0 = g must be 1 (no division at all); 1 = g must be odd; 2 = g must be 1 or 2 (one halving); 3 = any g;
//           4 = g not divisible by 4; 5 = g not divisible by 8.
// For every set of m targets of height 1 on NN inputs (one per class under signed permutations of the inputs; "full" = no
// zero entry), or for the target sets of a file:
//   href = least helpers in the reference class (AREF, DIV);  then: do href - 1 helpers suffice in the challenger class (ACH, DIV)?
// The search is exhaustive in each class: iterative deepening on the number of helpers; at a node, every wire one allowed gate
// away from the held wires is a candidate; targets one allowed gate away are taken at once (they must be paid anyway and more
// wires never hurt); a candidate tried at a node is not tried again in the subtrees of its later siblings (a wire that can be
// made now can be made first).
// usage: deepmin m AREF ACH DIV [full] [hcap] [-T file] [-E h A]   (-T: target sets from file, one set per line, NN*m numbers;
//        -E h A: with -T, enumerate ALL helper sets of size h in class A and say which are not realisable in class AREF)
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
  for (i = 0; i < NN; i++) v->e[i] = s * v->e[i] / g; return g; }
static int eq(const vec *a, const vec *b) { return !memcmp(a, b, sizeof(vec)); }
static unsigned AM; static int DIV = 3;
static int amok(long a) { a = labs(a); return a >= 1 && a < 32 && ((AM >> a) & 1); }
static int gok(long g) { g = labs(g); if (DIV == 0) return g == 1; if (DIV == 1) return g & 1; if (DIV == 2) return g <= 2; if (DIV == 4) return g % 4 != 0; if (DIV == 5) return g % 8 != 0; return 1; }
// the gate that makes t from u and v: g t = a u + b v.  returns 1 and fills a, b, g (coprime) if t is on the line, else 0
static int gate(const vec *u, const vec *v, const vec *t, long *pa, long *pb, long *pg) {
  for (int i = 0; i < NN; i++) for (int j = i + 1; j < NN; j++) { long D = (long)u->e[i] * v->e[j] - (long)u->e[j] * v->e[i];
    if (D) { long a = (long)t->e[i] * v->e[j] - (long)t->e[j] * v->e[i], b = (long)u->e[i] * t->e[j] - (long)u->e[j] * t->e[i];
      for (int l = 0; l < NN; l++) if (D * t->e[l] != a * u->e[l] + b * v->e[l]) return 0;
      if (!a || !b) return 0;
      long g0 = igcd(igcd((int)labs(a), (int)labs(b)), (int)labs(D)); *pa = a / g0; *pb = b / g0; *pg = labs(D) / g0; return 1; } }
  return 0; }
static int onegate(const vec *u, const vec *v, const vec *t) { long a, b, g; if (!gate(u, v, t, &a, &b, &g)) return 0; return amok(a) && amok(b) && gok(g); }
#define MAXD 40
static vec D[MAXD]; static int nd;
static vec T[12]; static int m; static char done[12];
static vec BAN[200000]; static int nban;
static vec trail[12]; static int ntrail; static vec besttrail[12]; static int nbest;
static int ENUM = 0; static long nsol = 0; static void report(void);
static int held(const vec *c) { for (int i = 0; i < nd; i++) if (eq(&D[i], c)) return 1; return 0; }
static int banned(const vec *c) { for (int i = 0; i < nban; i++) if (eq(&BAN[i], c)) return 1; return 0; }
static void closure(void) { int ch = 1; while (ch) { ch = 0; for (int t = 0; t < m; t++) if (!done[t]) {
    int ok = held(&T[t]); for (int i = 0; i < nd && !ok; i++) for (int j = i + 1; j < nd && !ok; j++) if (onegate(&D[i], &D[j], &T[t])) ok = 1;
    if (ok) { done[t] = 1; if (!held(&T[t])) D[nd++] = T[t]; ch = 1; } } } }
static int dfs(int hleft) {
  int snd = nd; char sdone[12]; memcpy(sdone, done, 12);
  closure(); int all = 1; for (int t = 0; t < m; t++) if (!done[t]) all = 0;
  if (all) { if (hleft == 0 || !ENUM) { nbest = ntrail; memcpy(besttrail, trail, sizeof(trail)); if (ENUM) { nsol++; report(); } }
    nd = snd; memcpy(done, sdone, 12); return ENUM ? 0 : 1; }
  if (hleft == 0) { nd = snd; memcpy(done, sdone, 12); return 0; }
  int n0 = nd; static vec candbuf[16][4096]; vec *cand = candbuf[hleft]; int nc = 0;
  for (int i = 0; i < n0; i++) for (int j = i + 1; j < n0; j++) for (int a = 1; a < 32; a++) if ((AM >> a) & 1) for (int b = 1; b < 32; b++) if ((AM >> b) & 1) {
    if (igcd(a, b) != 1) continue;
    for (int s = -1; s <= 1; s += 2) { vec c; for (int l = 0; l < NN; l++) c.e[l] = a * D[i].e[l] + s * b * D[j].e[l];
      int g = norm(&c); if (!g || !gok(g)) continue; if (held(&c) || banned(&c)) continue;
      int dup = 0; for (int q = 0; q < nc && !dup; q++) if (eq(&cand[q], &c)) dup = 1; if (dup) continue;
      if (nc < 4096) cand[nc++] = c; else { fprintf(stderr, "candidate overflow\n"); exit(3); } } }
  int nban0 = nban;
  for (int q = 0; q < nc; q++) { D[nd++] = cand[q]; trail[ntrail++] = cand[q]; int r = dfs(hleft - 1); ntrail--; nd = n0;
    if (r) { nban = nban0; nd = snd; memcpy(done, sdone, 12); return 1; }
    if (nban < 200000) BAN[nban++] = cand[q]; else { fprintf(stderr, "ban overflow\n"); exit(3); } }
  nban = nban0; nd = snd; memcpy(done, sdone, 12); return 0; }
static void reset(void) { nd = 0; for (int i = 0; i < NN; i++) { memset(&D[nd], 0, sizeof(vec)); D[nd].e[i] = 1; nd++; } memset(done, 0, 12); ntrail = 0; nban = 0; }
static void pv(const vec *v) { printf("("); for (int i = 0; i < NN; i++) printf("%d%s", v->e[i], i + 1 < NN ? "," : ")"); }
// is the wire set {inputs, helpers hs[0..nh-1], targets} realisable in the class (am, DIV) in SOME order?  prints the gates if show
static int realisable(const vec *hs, int nh, unsigned am, int show) {
  unsigned sam = AM; AM = am; vec S[MAXD]; int ns = 0; char got[MAXD]; vec all[MAXD]; int na = 0;
  for (int i = 0; i < nh; i++) all[na++] = hs[i]; for (int i = 0; i < m; i++) { int d = 0; for (int q = 0; q < na; q++) if (eq(&all[q], &T[i])) d = 1; if (!d) all[na++] = T[i]; }
  memset(got, 0, sizeof(got)); for (int i = 0; i < NN; i++) { memset(&S[ns], 0, sizeof(vec)); S[ns].e[i] = 1; ns++; }
  for (int q = 0; q < na; q++) for (int i = 0; i < NN; i++) if (eq(&all[q], &S[i])) got[q] = 1;
  int ch = 1; while (ch) { ch = 0; for (int q = 0; q < na; q++) if (!got[q]) { int ok = 0;
      for (int i = 0; i < ns && !ok; i++) for (int j = i + 1; j < ns && !ok; j++) if (onegate(&S[i], &S[j], &all[q])) { ok = 1;
        if (show) { long a, b, g; gate(&S[i], &S[j], &all[q], &a, &b, &g); printf("    %ld*", g); pv(&all[q]); printf(" = %ld*", a); pv(&S[i]); printf(" + %ld*", b); pv(&S[j]); printf("\n"); } }
      if (ok) { got[q] = 1; S[ns++] = all[q]; ch = 1; } } }
  AM = sam; for (int q = 0; q < na; q++) if (!got[q]) return 0; return 1; }
static unsigned AREF, ACH; static long ndeep = 0, nshown = 0;
static long nirr = 0;
static void report(void) { for (int i = 0; i < nbest; i++) { vec hs[12]; int k = 0; for (int q = 0; q < nbest; q++) if (q != i) hs[k++] = besttrail[q]; if (realisable(hs, k, AM, 0)) return; }
  nirr++; int r = realisable(besttrail, nbest, AREF, 0); if (!r) { ndeep++; if (nshown < 6) { nshown++; printf("  NOT realisable in the reference class: helpers"); for (int i = 0; i < nbest; i++) { printf(" "); pv(&besttrail[i]); } printf("\n"); realisable(besttrail, nbest, AM, 1); } } }
static vec C[1024]; static int nc; static int *act; static int ng;
static int cidx(const vec *v) { for (int i = 0; i < nc; i++) if (eq(&C[i], v)) return i; return -1; }
static int cmpi(const void *a, const void *b) { return *(const int *)a - *(const int *)b; }
static long orbits = 0, saved = 0, capped = 0, hist[16];
static void one(int hcap) {
  int href = -1; AM = AREF; for (int h = 0; h <= hcap; h++) { reset(); if (dfs(h)) { href = h; break; } }
  if (getenv("VERB")) { printf("SET href=%d:", href); for (int i = 0; i < m; i++) { printf(" "); pv(&T[i]); } printf("\n"); }
  if (href < 0) { capped++; return; }
  hist[href]++; vec f1[12]; int nf1 = nbest; memcpy(f1, besttrail, sizeof(f1));
  if (href >= 1) { AM = ACH; reset(); if (dfs(href - 1)) { saved++;
      printf("SAVE targets:"); for (int i = 0; i < m; i++) { printf(" "); pv(&T[i]); } printf("  reference: %d helpers =", href); for (int i = 0; i < nf1; i++) { printf(" "); pv(&f1[i]); }
      printf("  | challenger: %d helpers =", href - 1); for (int i = 0; i < nbest; i++) { printf(" "); pv(&besttrail[i]); } printf("\n");
      vec bt[12]; int nb = nbest; memcpy(bt, besttrail, sizeof(bt)); realisable(bt, nb, ACH, 1);
      if (href >= 2) { reset(); if (dfs(href - 2)) printf("SAVE2 (two gates saved)\n"); } fflush(stdout); } } }
int main(int argc, char **argv) {
  if (argc < 5) { fprintf(stderr, "usage: deepmin m AREF ACH DIV [full] [hcap] [-T file] [-E h A]\n"); return 2; }
  m = atoi(argv[1]); AREF = (unsigned)atoi(argv[2]); ACH = (unsigned)atoi(argv[3]); DIV = atoi(argv[4]);
  int full = 0, hcap = 5, eh = -1; unsigned ea = 0; const char *tf = 0; int pos = 0;
  for (int i = 5; i < argc; i++) { if (!strcmp(argv[i], "-T")) tf = argv[++i]; else if (!strcmp(argv[i], "-E")) { eh = atoi(argv[++i]); ea = (unsigned)atoi(argv[++i]); }
    else { if (pos == 0) full = atoi(argv[i]); else hcap = atoi(argv[i]); pos++; } }
  printf("# deepmin NN=%d m=%d AREF=%u ACH=%u DIV=%d full=%d hcap=%d\n", NN, m, AREF, ACH, DIV, full, hcap);
  if (tf) { FILE *f = fopen(tf, "r"); if (!f) { perror(tf); return 2; } for (;;) { int okr = 1; for (int i = 0; i < m && okr; i++) for (int l = 0; l < NN && okr; l++) if (fscanf(f, "%d", &T[i].e[l]) != 1) okr = 0;
      if (!okr) break; for (int i = 0; i < m; i++) norm(&T[i]); orbits++;
      if (eh >= 0) { AM = ea; ENUM = 1; nsol = 0; ndeep = 0; nshown = 0; nirr = 0; reset(); dfs(eh); ENUM = 0;
        printf("ENUM targets:"); for (int i = 0; i < m; i++) { printf(" "); pv(&T[i]); } printf("  class A=%u DIV=%d, exactly %d helpers: %ld helper sets, %ld of them with no helper that can be dropped; of these, not realisable in the reference class A=%u: %ld\n", ea, DIV, eh, nsol, nirr, AREF, ndeep); }
      else { long s0 = saved; one(hcap); printf("SETDONE targets:"); for (int i = 0; i < m; i++) { printf(" "); pv(&T[i]); } printf(" saved=%ld\n", saved - s0); } }
    fclose(f); }
  else {
    { int tot = 1; for (int i = 0; i < NN; i++) tot *= 3;
      for (int x = 0; x < tot; x++) { vec v; int y = x; for (int i = 0; i < NN; i++) { v.e[i] = y % 3 - 1; y /= 3; }
        vec w = v; if (!norm(&w)) continue; if (!eq(&w, &v)) continue; int sup = 0; for (int i = 0; i < NN; i++) if (v.e[i]) sup++;
        if (sup < 2) continue; if (!full || sup == NN) C[nc++] = v; } }
    { int perm[NN]; for (int i = 0; i < NN; i++) perm[i] = i; int nperm = 1; for (int i = 2; i <= NN; i++) nperm *= i;
      act = malloc(sizeof(int) * nperm * (1 << NN) * nc); ng = 0;
      for (int pi = 0; pi < nperm; pi++) {
        for (int s = 0; s < (1 << NN); s++) { for (int c = 0; c < nc; c++) { vec w; for (int i = 0; i < NN; i++) w.e[perm[i]] = ((s >> i) & 1) ? -C[c].e[i] : C[c].e[i]; norm(&w); act[ng * nc + c] = cidx(&w); } ng++; }
        int i = NN - 2; while (i >= 0 && perm[i] > perm[i + 1]) i--; if (i < 0) break; int j = NN - 1; while (perm[j] < perm[i]) j--; int t = perm[i]; perm[i] = perm[j]; perm[j] = t;
        for (int a = i + 1, b = NN - 1; a < b; a++, b--) { t = perm[a]; perm[a] = perm[b]; perm[b] = t; } } }
    printf("# candidate targets=%d group=%d\n", nc, ng);
    int idx[12]; for (int i = 0; i < m; i++) idx[i] = i; long smod = 0, sres = 0, ndone = 0;
    if (getenv("SPLIT")) { sscanf(getenv("SPLIT"), "%ld/%ld", &sres, &smod); printf("# only the classes whose number is %ld modulo %ld\n", sres, smod); }
    for (;;) {
      int canon = 1; for (int g = 0; g < ng && canon; g++) { int im[12]; for (int i = 0; i < m; i++) im[i] = act[g * nc + idx[i]]; qsort(im, m, sizeof(int), cmpi);
        for (int i = 0; i < m; i++) { if (im[i] < idx[i]) { canon = 0; break; } if (im[i] > idx[i]) break; } }
      if (canon) { orbits++; if (!smod || orbits % smod == sres) { for (int i = 0; i < m; i++) T[i] = C[idx[i]]; one(hcap); ndone++;
          if (ndone % 100 == 0) { printf("# progress: %ld sets done (class number %ld), saved so far %ld, histogram so far:", ndone, orbits, saved); for (int h = 0; h <= hcap; h++) printf(" h=%d:%ld", h, hist[h]); printf(" above cap=%ld\n", capped); fflush(stdout); } } }
      int i = m - 1; while (i >= 0 && idx[i] == nc - m + i) i--; if (i < 0) break; idx[i]++; for (int j = i + 1; j < m; j++) idx[j] = idx[j - 1] + 1; } }
  printf("# sets=%ld  reference helpers histogram:", orbits); for (int h = 0; h <= hcap; h++) printf(" h=%d:%ld", h, hist[h]); printf("  above cap=%ld\n# target sets where the challenger class saves a gate: %ld\n", capped, saved);
  return 0; }
