/* ds.c : exhaustive search, count (G): a gate is any a*u + b*v, scalings free.
 * Work over GF(p), vectors in GF(p)^n taken up to a scalar (projective points).
 * A circuit = a growing set of points, starting from the n unit vectors; each new point lies on the
 * line through two earlier points. Targets = given points (rows of the matrix, up to scaling).
 * Every target that is not a unit vector needs its own gate, so
 *     gates = (#targets) + (#non-target gates).
 * We search for the fewest non-target gates F. A target is added the moment it lies on a line of two
 * present points (this never hurts: it costs the gate it must cost anyway and only enlarges the set).
 * Order rule to avoid recounting: if the gate chosen now was already available one level up, its code
 * must be larger than the code of the gate chosen one level up.
 *
 * usage: ds p n F part nparts  < targets   (targets: T then T rows of n integers)
 * exit: prints FOUND + the points, or NONE with node counts.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXN 16
#define MAXPTS 64
#define MAXLEV 12
static int p, n, F, part, nparts;
static int inv[64];
static long long npow[MAXN + 1];
static int pts[MAXPTS][MAXN];
static long long pcode[MAXPTS];
static int par1[MAXPTS], par2[MAXPTS], parb[MAXPTS], istgt[MAXPTS];
static int npts;
static unsigned char *present, *target;
static int *stamp[MAXLEV + 1];
static int stampval[MAXLEV + 1];
static int ntargets, nfound;
static long long nodes = 0, leaves = 0;
static int found = 0;
#define MAXCAND 20000
static int candi[MAXLEV + 1][MAXCAND], candj[MAXLEV + 1][MAXCAND], candb[MAXLEV + 1][MAXCAND];
static long long candc[MAXLEV + 1][MAXCAND];

static long long encode(const int *v) {
  int lead = -1;
  for (int i = 0; i < n; i++) if (v[i]) { lead = i; break; }
  if (lead < 0) return -1;
  int s = inv[v[lead]];
  long long c = 0;
  for (int i = 0; i < n; i++) c = c * p + (v[i] * s) % p;
  return c;
}
static void normalise(int *v) {
  int lead = -1;
  for (int i = 0; i < n; i++) if (v[i]) { lead = i; break; }
  int s = inv[v[lead]];
  for (int i = 0; i < n; i++) v[i] = (v[i] * s) % p;
}
static void addpoint(const int *v, int a, int b, int coef, int tg) {
  memcpy(pts[npts], v, sizeof(int) * n);
  normalise(pts[npts]);
  pcode[npts] = encode(v);
  par1[npts] = a; par2[npts] = b; parb[npts] = coef; istgt[npts] = tg;
  present[pcode[npts]] = 1;
  npts++;
}
static void poppoint(void) { npts--; present[pcode[npts]] = 0; }

/* add all targets reachable on lines through at least one point of index >= from; returns number added */
static int closeTargets(int from) {
  int added = 0;
  int v[MAXN];
  for (int j = from; j < npts && nfound < ntargets; j++)   /* npts grows as targets are added */
    for (int i = 0; i < j && nfound < ntargets; i++)
      for (int b = 1; b < p; b++) {
        for (int k = 0; k < n; k++) v[k] = (pts[i][k] + b * pts[j][k]) % p;
        long long c = encode(v);
        if (c >= 0 && target[c] && !present[c]) { addpoint(v, i, j, b, 1); nfound++; added++; }
      }
  return added;
}
static void show(void) {
  printf("FOUND p=%d n=%d nontarget=%d total_gates=%d\n", p, n, npts - n - ntargets, npts - n);
  for (int i = n; i < npts; i++) {
    printf("  g%-2d = n%-2d + %d*n%-2d  %s  [", i, par1[i], parb[i], par2[i], istgt[i] ? "TARGET" : "      ");
    for (int k = 0; k < n; k++) printf("%d%s", pts[i][k], k + 1 < n ? " " : "");
    printf("]\n");
  }
  fflush(stdout);
}
static void search(int lev, long long lastcode) {
  int added = closeTargets(lev == 0 ? 0 : npts - 1);
  nodes++;
  if (nfound == ntargets) { found = 1; show(); goto out; }
  if (lev == F) { leaves++; goto out; }
  {
    int sv = ++stampval[lev];
    int *st = stamp[lev];
    int v[MAXN];
    int base = npts;
    /* pass 1: list every candidate (so that "was available one level up" is complete) */
    int ncand = 0;
    int *ci = candi[lev], *cj = candj[lev], *cb = candb[lev];
    long long *cc = candc[lev];
    for (int i = 0; i < base; i++)
      for (int j = i + 1; j < base; j++)
        for (int b = 1; b < p; b++) {
          for (int k = 0; k < n; k++) v[k] = (pts[i][k] + b * pts[j][k]) % p;
          long long c = encode(v);
          if (c < 0 || present[c]) continue;
          if (st[c] == sv) continue;
          st[c] = sv;
          ci[ncand] = i; cj[ncand] = j; cb[ncand] = b; cc[ncand] = c; ncand++;
        }
    /* pass 2 */
    for (int t = 0; t < ncand && !found; t++) {
      long long c = cc[t];
      if (lev == 0 && (t % nparts) != part) continue;
      if (lev > 0 && stamp[lev - 1][c] == stampval[lev - 1] && c < lastcode) continue;
      for (int k = 0; k < n; k++) v[k] = (pts[ci[t]][k] + cb[t] * pts[cj[t]][k]) % p;
      addpoint(v, ci[t], cj[t], cb[t], 0);
      search(lev + 1, c);
      poppoint();
    }
  }
out:
  for (int k = 0; k < added; k++) { poppoint(); nfound--; }
}
int main(int argc, char **argv) {
  if (argc < 6) { fprintf(stderr, "usage: ds p n F part nparts < targets\n"); return 2; }
  p = atoi(argv[1]); n = atoi(argv[2]); F = atoi(argv[3]); part = atoi(argv[4]); nparts = atoi(argv[5]);
  for (int a = 1; a < p; a++) for (int b = 1; b < p; b++) if ((a * b) % p == 1) inv[a] = b;
  npow[0] = 1; for (int i = 1; i <= n; i++) npow[i] = npow[i - 1] * p;
  present = calloc(npow[n], 1); target = calloc(npow[n], 1);
  for (int l = 0; l <= F; l++) stamp[l] = calloc(npow[n], sizeof(int));
  int v[MAXN];
  for (int i = 0; i < n; i++) { memset(v, 0, sizeof v); v[i] = 1; addpoint(v, -1, -1, 0, 0); }
  int T; if (scanf("%d", &T) != 1) return 2;
  ntargets = 0; nfound = 0;
  for (int t = 0; t < T; t++) {
    for (int k = 0; k < n; k++) { int x; if (scanf("%d", &x) != 1) return 2; v[k] = ((x % p) + p) % p; }
    long long c = encode(v);
    if (c < 0) { fprintf(stderr, "zero target\n"); return 2; }
    if (present[c] || target[c]) continue; /* unit vector or repeated: free */
    target[c] = 1; ntargets++;
  }
  search(0, -1);
  if (!found) printf("NONE p=%d n=%d targets=%d nontarget<=%d (total gates <= %d) part %d/%d nodes=%lld leaves=%lld\n",
                     p, n, ntargets, F, ntargets + F, part, nparts, nodes, leaves);
  return found ? 0 : 1;
}
