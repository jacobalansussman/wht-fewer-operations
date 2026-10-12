// x-0-twojobs/exh8.c : a RESTRICTED exhaustive search for 18 gates at 8 points.  Kept fixed: the six tree wires g1..g6 of
// g-1's 19 (two halves g5, g6 of the inputs).  Free: the centre c, any pool wire on the line through g5 and g6 (argument:
// which one), and THREE more helper wires, any pool wires, each derivable when it is added (the third: any wire that completes
// the circuit).  10 helpers + 8 outputs = 18 gates.  Pool: primitive whole-number vectors with |entries| in the allowed set.
// usage: exh8 ALLOW s19.txt centre_index seconds
#define N 8
#define main tj_main
#include "tj.c"
#undef main
static int level1(vec *out, int maxo) {
  static vec W[MAXW + 2 * N + 4]; char der[MAXW + 2 * N + 4]; int queue[MAXW + 2 * N + 4];
  int n = build(W, -1, -1), qn = 0, no = 0; memset(der, 0, n + 1); for (int i = 0; i < N; i++) { der[i] = 1; queue[qn++] = i; }
  closeq(W, n, der, queue, qn, 0, 0, 0, 0);
  gen1++; for (int i = 0; i < n; i++) hins(ht1, hg1, gen1, &W[i]);
  for (int q = 0; q < n; q++) if (der[q]) for (int r = q + 1; r < n; r++) if (der[r])
    for (int c = 0; c < ncp; c++) { vec t; if (comb(&W[q], &W[r], CPa[c], CPb[c], &t) && hins(ht1, hg1, gen1, &t)) { if (no < maxo) out[no] = t; no++; } }
  return no;
}
int main(int argc, char **argv) {
  ALLOW = (unsigned)atoi(argv[1]); int ci = atoi(argv[3]); double secs = atof(argv[4]);
  int L = 0; for (int i = 0; i < 32; i++) if ((ALLOW >> i) & 1) L = i;
  K = 2 * L * L; for (int a = 1; a <= K; a++) for (int b = -K; b <= K; b++) if (b && igcd(a, b) == 1) { CPa[ncp] = a; CPb[ncp] = b; ncp++; }
  ht1 = malloc(sizeof(vec) << HB); ht2 = malloc(sizeof(vec) << HB); hg1 = calloc(1u << HB, sizeof(unsigned)); hg2 = calloc(1u << HB, sizeof(unsigned));
  for (int i = 0; i < N; i++) { int t[N]; for (int j = 0; j < N; j++) t[j] = (i == j); normv(t, &IN[i]); for (int j = 0; j < N; j++) t[j] = __builtin_parity(i & j) ? -1 : 1; normv(t, &OUT[i]); }
  FILE *f = fopen(argv[2], "r"); vec G[16]; int ng = 0;
  for (;;) { int t[N], ok = 1; for (int j = 0; j < N; j++) if (fscanf(f, "%d", &t[j]) != 1) ok = 0; if (!ok || ng >= 16) break; normv(t, &G[ng++]); }
  fclose(f);
  static vec C[64]; int nc = 0;
  for (int c = 0; c < ncp; c++) { vec t; if (comb(&G[4], &G[5], CPa[c], CPb[c], &t)) { int dup = 0; for (int z = 0; z < nc; z++) if (!memcmp(&C[z], &t, N)) dup = 1; if (!dup) C[nc++] = t; } }
  printf("# exh8 ALLOW=%u: %d possible centres on the line g5, g6; this run: centre %d = [", ALLOW, nc, ci);
  if (ci >= nc) { printf("none]\n"); return 0; }
  for (int i = 0; i < N; i++) printf("%d%s", C[ci].e[i], i < N - 1 ? " " : "]\n");
  int B = 7; for (int i = 0; i < 6; i++) Hh[i] = G[i]; Hh[6] = C[ci]; nh = 7;
  if (argc > 5) { Hh[7] = G[7]; nh = 8; B = 8; printf("# CONTROL: g8 of the 19 added as a fixed helper, so circuits found have 19 gates\n"); }
  static vec L1[20000], L2[20000], found[16]; int n1 = level1(L1, 20000);
  printf("# first free helper: %d candidates\n", n1); fflush(stdout);
  // index of L1 members
  static vec *k3; static int *v3; static unsigned char *u3; k3 = malloc(sizeof(vec) << 16); v3 = malloc(sizeof(int) << 16); u3 = calloc(1 << 16, 1);
  for (int i = 0; i < n1; i++) { u64 h = hv(&L1[i]) & 0xffff; while (u3[h]) h = (h + 1) & 0xffff; u3[h] = 1; k3[h] = L1[i]; v3[h] = i; }
  time_t t0 = time(0); long pairs = 0, hits18 = 0, hits17 = 0; int i;
  for (i = 0; i < n1; i++) {
    if (difftime(time(0), t0) > secs) break;
    Hh[B] = L1[i]; nh = B + 1; int n2 = level1(L2, 20000); if (n2 > 20000) n2 = 20000;
    for (int j = 0; j < n2; j++) {
      u64 h = hv(&L2[j]) & 0xffff; int idx = -1; while (u3[h]) { if (!memcmp(&k3[h], &L2[j], N)) { idx = v3[h]; break; } h = (h + 1) & 0xffff; }
      if (idx >= 0 && idx < i) continue;
      Hh[B + 1] = L2[j]; Hh[B + 2] = IN[0]; nh = B + 3; pairs++;
      int nf = cands(B + 2, -1, found, 16, 0);
      if (nf == -1) { hits17++; nh = B + 2; printf("# ONE GATE FEWER?\n"); ledger("exh8-fewer", 1, 0); }
      else if (nf > 0) { hits18++; if (hits18 <= 3) { Hh[B + 2] = found[0]; nh = B + 3; ledger("exh8-found", 1, 0); } }
      nh = B + 1;
    }
    if (i % 100 == 0) { printf("# first helper %d of %d, pairs %ld, circuits found %ld, %.0f s\n", i, n1, pairs, hits18, difftime(time(0), t0)); fflush(stdout); }
  }
  printf("# END centre %d: first helpers done %d of %d (%s), pairs of helpers tried %ld, circuits found (%d gates) %ld, with one gate fewer %ld, %.0f s\n", ci, i, n1, i == n1 ? "COMPLETE" : "INCOMPLETE", pairs, B + 3 + N, hits18, hits17, difftime(time(0), t0));
  return 0;
}
