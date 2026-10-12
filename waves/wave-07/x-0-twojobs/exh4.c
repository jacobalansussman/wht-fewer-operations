// x-0-twojobs/exh4.c : EXHAUSTIVE at 4 points. Every set of H helper wires from the pool (primitive whole-number vectors with
// |entries| in the allowed set, inputs and outputs excluded) such that helpers + the 4 outputs form a circuit (every wire in the
// span of two wires derived before it).  Gates = H + 4.  For each circuit: the ledger profile of tj.c.   usage: exh4 ALLOW H
#define N 4
#define main tj_main
#include "tj.c"
#undef main
int main(int argc, char **argv) {
  ALLOW = (unsigned)atoi(argv[1]); int Hn = atoi(argv[2]); int L = 0; for (int i = 0; i < 32; i++) if ((ALLOW >> i) & 1) L = i;
  for (int i = 0; i < N; i++) { int t[N]; for (int j = 0; j < N; j++) t[j] = (i == j); normv(t, &IN[i]); for (int j = 0; j < N; j++) t[j] = __builtin_parity(i & j) ? -1 : 1; normv(t, &OUT[i]); }
  static vec P[20000]; int np = 0; int t[N];
  for (t[0] = -L; t[0] <= L; t[0]++) for (t[1] = -L; t[1] <= L; t[1]++) for (t[2] = -L; t[2] <= L; t[2]++) for (t[3] = -L; t[3] <= L; t[3]++) {
    vec v; if (!normv(t, &v)) continue; int same = 1; for (int i = 0; i < N; i++) if (v.e[i] != t[i]) same = 0; if (!same) continue;   // primitive, sign-normalised representative only
    int skip = 0; for (int i = 0; i < N; i++) if (!memcmp(&v, &IN[i], N) || !memcmp(&v, &OUT[i], N)) skip = 1; if (skip) continue;
    P[np++] = v; }
  printf("# exh4 ALLOW=%u pool=%d wires, helpers=%d, gates=%d\n", ALLOW, np, Hn, Hn + 4);
  static char profs[400][256]; static long profn[400]; int nprof = 0; long valid = 0, tested = 0; int idx[4];
  static vec W[64]; char der[64];
  for (idx[0] = 0; idx[0] < np; idx[0]++) for (idx[1] = (Hn > 1 ? idx[0] + 1 : np - 1); idx[1] < np; idx[1]++) for (idx[2] = (Hn > 2 ? idx[1] + 1 : np - 1); idx[2] < np; idx[2]++) {
    nh = Hn; for (int z = 0; z < Hn; z++) Hh[z] = P[idx[z]]; tested++;
    int n = build(W, -1, -1); if (!fullclose(W, n, der, 0, 0, 0, 0)) continue;
    valid++; ledger("", 1, 1); int z; for (z = 0; z < nprof; z++) if (!strcmp(profs[z], PROF)) break;
    if (z == nprof && nprof < 400) { strcpy(profs[nprof++], PROF); profn[z] = 0; char tg[64]; snprintf(tg, sizeof tg, "exh4-A%u-profile%d", ALLOW, nprof); ledger(tg, 1, 0); }
    if (z < 400) profn[z]++;
  }
  printf("# tested %ld helper sets, circuits %ld\n", tested, valid);
  for (int z = 0; z < nprof; z++) printf("PROFILE %ld circuits: %s\n", profn[z], profs[z]);
  return 0;
}
