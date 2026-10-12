// ag-6-deepgates/tjd.c = x-0-twojobs/tj.c with one change: env AMK restricts the coefficient sizes of every gate (see inspan).
// x-0-twojobs/tj.c : local walk over circuits for the N-point Walsh-Hadamard transform, count (G): a gate is any a*u + b*v,
// scalings free.  A circuit is a set of wires (primitive whole-number vectors up to sign) in which every non-input wire lies in
// the span of two wires derived before it.  POOL: primitive vectors whose entries have absolute values in an allowed set
// (bit mask ALLOW: 3 = {0,1} the forms; 7 = {0,1,2} = form + 2 x form on a disjoint set; 23 = {0,1,2,4}; 15 = {0,1,2,3}; ...).
// Moves: drop one helper; remove two helpers and add one pool wire (exhaustive over the wires that can matter); swap one helper
// for a pool wire (plateau move, random, avoiding states seen).   Exact small-integer arithmetic throughout.
// LEDGER printed for every circuit kept (N = 8 only for the volume column):
//   gate w = (a u + b v)/g between primitive wires, budget log2((|a|+|b|)/g);
//   vol = log2 of the growth of the largest N x N minor of all wires held so far (Morgenstern's potential; it depends only on the
//   ORDER of the wires, not on the choice of parents); join = the two parents have disjoint sets;
//   merge = the gate joins two connected components of inputs (inputs are connected when some held wire contains both).
// usage: tj ALLOW seconds seed startfile [pairs_per_state (0 = all)] [tag] [three-to-two samples per state, default 40] [profile every so many states, 0 = never] [kick percent]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>
#ifndef N
#define N 8
#endif
#define MAXW 120
typedef unsigned long long u64;
typedef struct { signed char e[N]; } vec;
static unsigned ALLOW = 7; static int K = 8; static unsigned AMK = 0;   // AMK (ag-6): allowed sizes of the two coefficients of a gate on primitive wires (bit s = size s); 0 = all
static int igcd(int a, int b) { a = abs(a); b = abs(b); while (b) { int t = a % b; a = b; b = t; } return a; }
static int normv(const int *t, vec *out) {
  int g = 0, s = 0, i;
  for (i = 0; i < N; i++) g = igcd(g, t[i]);
  if (!g) return 0;
  for (i = 0; i < N; i++) if (t[i]) { s = t[i] > 0 ? 1 : -1; break; }
  for (i = 0; i < N; i++) { int x = s * t[i] / g; int ax = abs(x); if (ax > 31 || !((ALLOW >> ax) & 1)) return 0; out->e[i] = (signed char)x; }
  return 1;
}
static int inspan(const vec *p, const vec *q, const vec *r, int *al, int *be, int *DD) {
  int i, j, l;
  for (i = 0; i < N; i++) { if (!q->e[i] && !r->e[i]) continue;
    for (j = i + 1; j < N; j++) {
      int D = q->e[i] * r->e[j] - q->e[j] * r->e[i];
      if (D) {
        int a = p->e[i] * r->e[j] - p->e[j] * r->e[i], b = q->e[i] * p->e[j] - q->e[j] * p->e[i];
        for (l = 0; l < N; l++) if (D * p->e[l] != a * q->e[l] + b * r->e[l]) return 0;
        if (AMK) { int g0 = igcd(igcd(a, b), D); int a1 = abs(a / g0), b1 = abs(b / g0); if (!a1 || !b1 || a1 > 31 || b1 > 31 || !((AMK >> a1) & 1) || !((AMK >> b1) & 1)) return 0; }
        if (al) { *al = a; *be = b; *DD = D; }
        return 1;
      } } }
  return 0;
}
static u64 hv(const vec *v) { u64 h = 1469598103934665603ULL; for (int i = 0; i < N; i++) { h ^= (unsigned char)v->e[i]; h *= 1099511628211ULL; } return h ^ (h >> 29); }
#define HB 22
#define HM ((1u << HB) - 1)
static vec *ht1, *ht2; static unsigned *hg1, *hg2; static unsigned gen1 = 1, gen2 = 1;
static int hins(vec *ht, unsigned *hg, unsigned gen, const vec *v) { u64 h = hv(v) & HM; while (hg[h] == gen) { if (!memcmp(&ht[h], v, N)) return 0; h = (h + 1) & HM; } hg[h] = gen; ht[h] = *v; return 1; }
static int hhas(vec *ht, unsigned *hg, unsigned gen, const vec *v) { u64 h = hv(v) & HM; while (hg[h] == gen) { if (!memcmp(&ht[h], v, N)) return 1; h = (h + 1) & HM; } return 0; }
static int CPa[8192], CPb[8192], ncp;
static vec IN[N], OUT[N], Hh[MAXW]; static int nh;
static vec EX[2]; static int nex = 0;
static int build(vec *W, int s1, int s2) { int n = 0, i; for (i = 0; i < N; i++) W[n++] = IN[i]; for (i = 0; i < nh; i++) if (i != s1 && i != s2) W[n++] = Hh[i]; for (i = 0; i < nex; i++) W[n++] = EX[i]; for (i = 0; i < N; i++) W[n++] = OUT[i]; return n; }
// closure by a queue: der[] marks derived wires; queue holds wires whose pairs are still to be used
static int closeq(const vec *W, int n, char *der, int *queue, int qn, int *p1, int *p2, int *ord, int *cnt) {
  int qh = 0;
  while (qh < qn) { int x = queue[qh++];
    for (int i = 0; i < n; i++) if (!der[i]) {
      for (int q = 0; q < n; q++) if (der[q] && q != x && inspan(&W[i], &W[x], &W[q], 0, 0, 0)) {
        der[i] = 1; queue[qn++] = i; if (p1) { p1[i] = x; p2[i] = q; } if (ord) ord[(*cnt)++] = i; break; } } }
  return qn;
}
static int fullclose(const vec *W, int n, char *der, int *p1, int *p2, int *ord, int *cnt) {
  int queue[MAXW + 2 * N + 4], qn = 0; memset(der, 0, n); for (int i = 0; i < N; i++) { der[i] = 1; queue[qn++] = i; }
  if (cnt) *cnt = 0; closeq(W, n, der, queue, qn, p1, p2, ord, cnt);
  for (int i = 0; i < n; i++) if (!der[i]) return 0;   // every wire, helpers included, derived
  return 1;
}
static int outs_ok(const char *der, int n, int nout0) { for (int i = nout0; i < nout0 + N; i++) if (!der[i]) return 0; return 1; }
static int comb(const vec *u, const vec *v, int a, int b, vec *c) { int t[N]; for (int i = 0; i < N; i++) t[i] = a * u->e[i] + b * v->e[i]; return normv(t, c); }
// candidates after removing helpers s1 (and s2): returns the number of wires c for which (helpers - removed + c) derives all outputs
static int cands(int s1, int s2, vec *found, int maxf, int mode) {
  static vec W[MAXW + 2 * N + 4]; char der[MAXW + 2 * N + 4], der2[MAXW + 2 * N + 4]; int queue[MAXW + 2 * N + 4];
  int n = build(W, s1, s2), nout0 = n - N, nf = 0;
  int qn = 0; memset(der, 0, n + 1); for (int i = 0; i < N; i++) { der[i] = 1; queue[qn++] = i; }
  closeq(W, n, der, queue, qn, 0, 0, 0, 0);
  if (outs_ok(der, n, nout0)) return -1;
  gen1++; gen2++;
  for (int q = 0; q < n; q++) if (der[q]) for (int r = q + 1; r < n; r++) if (der[r])
    for (int c = 0; c < ncp; c++) { vec t; if (comb(&W[q], &W[r], CPa[c], CPb[c], &t)) hins(ht1, hg1, gen1, &t); }
  for (int i = 0; i < n; i++) hins(ht2, hg2, gen2, &W[i]);
  for (int p = 0; p < n; p++) if (!der[p]) for (int q = 0; q < n; q++) if (der[q])
    for (int c = 0; c < ncp; c++) { vec t;
      if (!comb(&W[p], &W[q], CPa[c], CPb[c], &t)) continue;
      if (!hhas(ht1, hg1, gen1, &t)) continue;
      if (!hins(ht2, hg2, gen2, &t)) continue;      // already a wire, or already tested
      if (s1 >= 0 && !memcmp(&t, &Hh[s1], N)) continue;
      if (s2 >= 0 && !memcmp(&t, &Hh[s2], N)) continue;
      if (mode == 1) { if (nf < maxf) found[nf] = t; nf++; continue; }
      W[n] = t; memcpy(der2, der, n); der2[n] = 1; queue[0] = n; closeq(W, n + 1, der2, queue, 1, 0, 0, 0, 0);
      if (outs_ok(der2, n, nout0)) { if (nf < maxf) found[nf] = t; nf++; }
    }
  return nf;
}
static long long det(long long A[N][N]) {
  long long prev = 1; int sign = 1;
  for (int k = 0; k < N - 1; k++) {
    if (!A[k][k]) { int r = -1; for (int i = k + 1; i < N; i++) if (A[i][k]) { r = i; break; } if (r < 0) return 0;
      for (int j = 0; j < N; j++) { long long t = A[k][j]; A[k][j] = A[r][j]; A[r][j] = t; } sign = -sign; }
    for (int i = k + 1; i < N; i++) for (int j = k + 1; j < N; j++) A[i][j] = (A[i][j] * A[k][k] - A[i][k] * A[k][j]) / prev;
    prev = A[k][k];
  }
  return sign * A[N - 1][N - 1];
}
static const vec *LW; static int Lidx[N]; static long long Lbest;
static void rec(int pos, int start, int m) {
  if (pos == N) { long long A[N][N]; for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) A[i][j] = LW[Lidx[i]].e[j];
    long long d = det(A); if (d < 0) d = -d; if (d > Lbest) Lbest = d; return; }
  for (int i = start; i <= m - (N - pos); i++) { Lidx[pos] = i; rec(pos + 1, i + 1, m); }
}
static int find(int *uf, int x) { while (uf[x] != x) x = uf[x] = uf[uf[x]]; return x; }
static char PROF[256];
static void ledger(const char *tag, int dovol, int quiet) {
  static vec W[MAXW + 2 * N + 4], S[MAXW + 2 * N + 4]; char der[MAXW + 2 * N + 4]; int p1[MAXW + 2 * N + 4], p2[MAXW + 2 * N + 4], ord[MAXW + 2 * N + 4], cnt = 0;
  int n = build(W, -1, -1);
  if (!fullclose(W, n, der, p1, p2, ord, &cnt)) { if (!quiet) printf("LEDGER %s: not every wire is derived (dead helper)\n", tag); }
  int m = N; for (int i = 0; i < N; i++) S[i] = IN[i];
  int k = 0; while ((1 << k) < N) k++;
  int floorN = N - 1 + (N / 2) * k;
  if (!quiet) printf("CIRCUIT %s  N=%d gates=%d  floor f(N)=%d  excess=%d\n", tag, N, cnt, floorN, cnt - floorN);
  int uf[N]; for (int i = 0; i < N; i++) uf[i] = i;
  long long delta = 1; double totb = 0, totv = 0; int ndirty = 0, big = 1, njoin = 0, njoinvol = 0, nmerge = 0, nmergevol = 0, n2 = 0, nq = 0; double v2 = 0, vmax = 0; int nvol = 0, nbigc = 0;
  for (int t = 0; t < cnt; t++) {
    const vec *w = &W[ord[t]];
    // best parents among wires already placed: least budget
    int bu = -1, bv = -1, ba = 0, bb = 0, bg = 1; double bbud = 1e9;
    for (int q = 0; q < m; q++) for (int r = q + 1; r < m; r++) { int al, be, D;
      if (inspan(w, &S[q], &S[r], &al, &be, &D)) { int g0 = igcd(igcd(al, be), D); al /= g0; be /= g0; D /= g0;
        if (!al || !be) continue; double bud = log2((double)(abs(al) + abs(be)) / abs(D));
        if (bud < bbud - 1e-9) { bbud = bud; bu = q; bv = r; ba = al; bb = be; bg = D; } } }
    if (bg < 0) { bg = -bg; ba = -ba; bb = -bb; }
    int disjoint = 1; for (int i = 0; i < N; i++) if (S[bu].e[i] && S[bv].e[i]) disjoint = 0;
    // components before
    int cu = -1, cv = -1, merge = 0;
    for (int i = 0; i < N; i++) if (w->e[i]) { int c = find(uf, i); if (cu < 0) cu = c; else if (c != cu) { merge = 1; cv = c; uf[c] = cu; } }
    (void)cv;
    S[m] = *w; m++;
    double vol = 0;
    if (dovol) { LW = S; Lbest = 0; Lidx[0] = m - 1; rec(1, 0, m - 1); if (Lbest > delta) { vol = log2((double)Lbest / delta); delta = Lbest; } }
    int amax = abs(ba) > abs(bb) ? abs(ba) : abs(bb), amin = abs(ba) < abs(bb) ? abs(ba) : abs(bb);
    char nm[2][16]; int pp[2] = {bu, bv}; for (int z = 0; z < 2; z++) { if (pp[z] < N) sprintf(nm[z], "x%d", pp[z]); else sprintf(nm[z], "w%d", pp[z] - N + 1); }
    if (!quiet) {
    printf("w%d = ", t + 1);
    if (bg == 1) printf("%d*%s + %d*%s", ba, nm[0], bb, nm[1]); else printf("%d/%d*%s + %d/%d*%s", ba, bg, nm[0], bb, bg, nm[1]);
    printf("   # [");
    for (int i = 0; i < N; i++) printf("%d%s", w->e[i], i < N - 1 ? " " : "");
    printf("] kind (%d,%d)/%d budget %.2f%s%s", amin, amax, bg, bbud, disjoint ? " JOIN" : "", merge ? " MERGE" : "");
    if (dovol) printf(" vol %.3f", vol);
    printf("\n");
    }
    { int dz = 0; for (int i = 0; i < N; i++) if (abs(w->e[i]) > 1) dz = 1; ndirty += dz; }
    totb += bbud; totv += vol; if (amax > big) big = amax; if (bg > 1) nq++;
    if (disjoint) { njoin++; if (vol > 1e-9) njoinvol++; }
    if (merge) { nmerge++; if (vol > 1e-9) nmergevol++; }
    if (amax == 2 && amin == 1 && bg == 1) { n2++; v2 += vol; }
    if (amax > 2) nbigc++;
    if (vol > 1e-9) nvol++; if (vol > vmax) vmax = vol;
  }
  snprintf(PROF, sizeof PROF, "gates=%d excess=%d volume=%.2f merges-with-volume=%d joins-with-volume=%d coefficient-2-gates=%d gates-with-coefficient-above-2=%d quotient-gates=%d largest-coefficient=%d most-units-from-one-gate=%.3f wires-with-an-entry-above-1=%d", cnt, cnt - floorN, totv, nmergevol, njoinvol, n2, nbigc, nq, big, vmax, ndirty);
  if (!quiet) printf("SUMMARY %s  gates=%d excess=%d  budget=%.2f  volume=%.2f (needed %d)  joins=%d of which carry volume=%d  merges=%d of which carry volume=%d  coefficient-2 gates=%d bringing %.2f units (%.3f each)  gates with a coefficient above 2=%d  quotient gates=%d  largest coefficient=%d  gates that bring volume=%d  most units from one gate=%.3f\n",
         tag, cnt, cnt - floorN, totb, totv, (N / 2) * k, njoin, njoinvol, nmerge, nmergevol, n2, v2, n2 ? v2 / n2 : 0.0, nbigc, nq, big, nvol, vmax);
  fflush(stdout);
}
static u64 statehash(void) { u64 h = 0; for (int i = 0; i < nh; i++) { u64 x = hv(&Hh[i]); h += x * (x | 1); } return h; }
#define VIS (1 << 20)
static u64 vis[VIS]; static int nvis;
static int seen(u64 h) { for (u64 i = h % VIS;; i = (i + 1) % VIS) { if (!vis[i]) return 0; if (vis[i] == h) return 1; } }
static void mark(u64 h) { if (nvis > VIS / 2) return; for (u64 i = h % VIS;; i = (i + 1) % VIS) { if (!vis[i]) { vis[i] = h; nvis++; return; } if (vis[i] == h) return; } }
int main(int argc, char **argv) {
  if (argc < 5) { fprintf(stderr, "usage: tj ALLOW seconds seed startfile [pairs_per_state] [tag]\n"); return 2; }
  ALLOW = (unsigned)atoi(argv[1]); double secs = atof(argv[2]); srand((unsigned)atoi(argv[3]));
  int pps = argc > 5 ? atoi(argv[5]) : 0; const char *tag = argc > 6 ? argv[6] : "run";
  int L = 0; for (int i = 0; i < 32; i++) if ((ALLOW >> i) & 1) L = i;
  K = 2 * L * L; if (K > 40) K = 40;
  if (getenv("KMAX")) { int km = atoi(getenv("KMAX")); if (km < K) K = km; }   // optional cap on the coefficients tried (a restriction, say so)
  if (getenv("AMK")) AMK = (unsigned)atoi(getenv("AMK"));
  for (int a = 1; a <= K; a++) for (int b = -K; b <= K; b++) if (b && igcd(a, b) == 1) { if (AMK && (a > 31 || abs(b) > 31 || !((AMK >> a) & 1) || !((AMK >> abs(b)) & 1))) continue; CPa[ncp] = a; CPb[ncp] = b; ncp++; }
  printf("# tjd (ag-6): tj with the gates restricted to coefficient sizes in mask AMK=%u (0 = unrestricted); division by the common factor stays free\n", AMK);
  ht1 = malloc(sizeof(vec) << HB); ht2 = malloc(sizeof(vec) << HB); hg1 = calloc(1u << HB, sizeof(unsigned)); hg2 = calloc(1u << HB, sizeof(unsigned));
  for (int i = 0; i < N; i++) { int t[N]; for (int j = 0; j < N; j++) t[j] = (i == j); normv(t, &IN[i]); for (int j = 0; j < N; j++) t[j] = __builtin_parity(i & j) ? -1 : 1; normv(t, &OUT[i]); }
  FILE *f = fopen(argv[4], "r"); if (!f) { perror("start"); return 2; }
  for (;;) { int t[N], ok = 1; for (int j = 0; j < N; j++) if (fscanf(f, "%d", &t[j]) != 1) ok = 0; if (!ok) break; if (!normv(t, &Hh[nh])) { fprintf(stderr, "start wire %d not in pool\n", nh); return 2; } nh++; }
  fclose(f);
  printf("# tj N=%d ALLOW=%u (largest entry %d, coefficient box %d, %d coefficient pairs) seconds=%.0f seed=%s start=%s helpers=%d\n", N, ALLOW, L, K, ncp, secs, argv[3], argv[4], nh);
  { static vec W[MAXW + 2 * N + 4]; char der[MAXW + 2 * N + 4]; int n = build(W, -1, -1); if (!fullclose(W, n, der, 0, 0, 0, 0)) { printf("start circuit is not valid in this pool\n"); return 1; } }
  char tg[128]; snprintf(tg, sizeof tg, "%s-start", tag); ledger(tg, N <= 8 && nh + N <= 30, 0);
  time_t t0 = time(0); int best = nh, states = 0, kept = 0, swaps2 = 0, stuck = 0, wander = 0, kicks = 0; int every = argc > 8 ? atoi(argv[8]) : 0, kickpct = argc > 9 ? atoi(argv[9]) : 0; static char profs[400][256]; static int profn[400]; int nprof = 0; static vec found[4096], f1[4096]; int T32 = argc > 7 ? atoi(argv[7]) : 40;
  mark(statehash());
  while (difftime(time(0), t0) < secs) {
    states++;
    int improved = 0;
    if (every && states % every == 0) {
      ledger("", N <= 8 && nh + N <= 30, 1); int z; for (z = 0; z < nprof; z++) if (!strcmp(profs[z], PROF)) break;
      if (z == nprof && nprof < 400) { strcpy(profs[nprof++], PROF); profn[z] = 0; snprintf(tg, sizeof tg, "%s-profile%d", tag, nprof); ledger(tg, N <= 8 && nh + N <= 30, 0); }
      if (z < 400) profn[z]++;
    }
    if (wander > 0) { wander--; goto plateau; }
    // 1. drop
    for (int i = 0; i < nh && !improved; i++) { if (cands(i, -1, found, 0, 0) == -1) { Hh[i] = Hh[nh - 1]; nh--; improved = 1; } }
    // 2. two -> one
    if (!improved) {
      int tot = nh * (nh - 1) / 2, lim = pps && pps < tot ? pps : tot;
      for (int z = 0; z < lim && !improved; z++) {
        int i, j;
        if (lim == tot) { int c = z; i = 0; while (c >= nh - 1 - i) { c -= nh - 1 - i; i++; } j = i + 1 + c; }
        else { i = rand() % nh; j = rand() % nh; if (i == j) continue; if (i > j) { int t = i; i = j; j = t; } }
        int nf = cands(i, j, found, 4096, 0);
        if (nf > 0) { vec c = found[rand() % (nf < 4096 ? nf : 4096)]; Hh[j] = Hh[nh - 1]; nh--; Hh[i] = c; improved = 1; }
        if (difftime(time(0), t0) > secs) break;
      }
    }
    // 2b. three -> two, sampled: remove k for good, then remove i, j, add c1 (any wire that makes progress) and look for c2
    if (!improved && nh >= 3) {
      for (int z = 0; z < T32 && !improved; z++) {
        int k = rand() % nh; vec keep = Hh[k]; Hh[k] = Hh[nh - 1]; nh--;
        int i = rand() % nh, j = rand() % nh; if (i == j) { Hh[nh] = Hh[k]; Hh[k] = keep; nh++; continue; } if (i > j) { int t = i; i = j; j = t; }
        nex = 0; int n1 = cands(i, j, f1, 4096, 1); if (n1 > 4096) n1 = 4096;
        for (int y = 0; y < 6 && n1 > 0 && !improved; y++) {
          EX[0] = f1[rand() % n1]; nex = 1; int n2 = cands(i, j, found, 4096, 0); nex = 0;
          if (n2 == -1) { Hh[i] = EX[0]; Hh[j] = Hh[nh - 1]; nh--; improved = 1; }
          else if (n2 > 0) { Hh[i] = EX[0]; Hh[j] = found[rand() % (n2 < 4096 ? n2 : 4096)]; improved = 1; }
        }
        if (!improved) { Hh[nh] = Hh[k]; Hh[k] = keep; nh++; }
      }
    }
    if (improved) {
      mark(statehash());
      if (nh < best) { best = nh; kept++; snprintf(tg, sizeof tg, "%s-best%d", tag, nh + N); printf("# NEW BEST %d gates after %d states, %.0f s\n", nh + N, states, difftime(time(0), t0)); ledger(tg, N <= 8 && nh + N <= 30, 0); }
      continue;
    }
    // 3. swap (plateau)
  plateau:;
    int done = 0;
    if (kickpct && nh == best && rand() % 100 < kickpct) {   // kick: remove i, add two wires; then wander before improving
      for (int tries = 0; tries < 20 && !done; tries++) {
        int i = rand() % nh; nex = 0; int n1 = cands(i, -1, f1, 4096, 1); if (n1 <= 0) continue; if (n1 > 4096) n1 = 4096;
        for (int y = 0; y < 8 && !done; y++) {
          EX[0] = f1[rand() % n1]; nex = 1; int n2 = cands(i, -1, found, 4096, 0); nex = 0;
          if (n2 > 0) { Hh[i] = EX[0]; Hh[nh++] = found[rand() % (n2 < 4096 ? n2 : 4096)]; done = 1; mark(statehash()); kicks++; wander = 12; }
        }
      }
      if (done) continue;
    }
    if (rand() % 2) {   // two-swap: remove i, j; add c1 (progress) and c2 (completing)
      for (int tries = 0; tries < 40 && !done; tries++) {
        int i = rand() % nh, j = rand() % nh; if (i == j) continue; if (i > j) { int t = i; i = j; j = t; }
        nex = 0; int n1 = cands(i, j, f1, 4096, 1); if (n1 <= 0) continue; if (n1 > 4096) n1 = 4096;
        for (int y = 0; y < 8 && !done; y++) {
          EX[0] = f1[rand() % n1]; nex = 1; int n2 = cands(i, j, found, 4096, 0); nex = 0;
          if (n2 > 0) { Hh[i] = EX[0]; Hh[j] = found[rand() % (n2 < 4096 ? n2 : 4096)]; done = 1; mark(statehash()); swaps2++; }
        }
      }
    }
    for (int tries = 0; tries < 4 * nh && !done; tries++) {
      int i = rand() % nh; int nf = cands(i, -1, found, 4096, 0); if (nf <= 0) continue; if (nf > 4096) nf = 4096;
      vec old = Hh[i]; int start = rand() % nf;
      for (int z = 0; z < nf; z++) { Hh[i] = found[(start + z) % nf]; u64 h = statehash(); if (!seen(h)) { mark(h); done = 1; break; } }
      if (!done) { if (tries > 2 * nh) { Hh[i] = found[start]; done = 1; } else Hh[i] = old; }
    }
    if (!done) stuck++;
    if (states % 200 == 0) { printf("# %d states, %.0f s, current %d gates, best %d, distinct states seen %d\n", states, difftime(time(0), t0), nh + N, best + N, nvis); fflush(stdout); }
  }
  printf("# END states=%d distinct=%d two-swaps=%d rounds without a move=%d best=%d gates, current=%d, %.0f s\n", states, nvis, swaps2, stuck, best + N, nh + N, difftime(time(0), t0));
  printf("# kicks=%d\n", kicks); for (int z = 0; z < nprof; z++) printf("PROFILE seen %d times: %s\n", profn[z], profs[z]);
  snprintf(tg, sizeof tg, "%s-last", tag); ledger(tg, N <= 8 && nh + N <= 30, 0);
  return 0;
}
