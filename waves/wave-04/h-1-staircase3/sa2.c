/* h-1-staircase3 / sa.c : annealer over sets of helper wires with entries 0,+1,-1 (up to an overall sign), count (G).
   A gate is a collinear triple: w on the line through u and v.  For 0/+-1 vectors the only such w are
   u+-v (when the overlap cancels or the supports are equal) and the flips u -+ 2v (v = +-u on its support).
   State = set of helpers.  A state is a circuit when every helper and every output is derivable in some order.
   gates = helpers + N.  Exact by construction (integer vectors); every hit is replayed with fractions by check.py.
   usage: sa2 K seedfile seconds rngseed temp outfile A B [targetsfile]   (targets replace the N characters as the wires that must be derivable; gates = helpers + targets)                                                   */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <time.h>
typedef uint64_t u64;
typedef struct { u64 s, m; } W;
static int K, N, BASE; static u64 FULL;
static inline W nrm(W w){ if (w.m & (w.s & (~w.s + 1))) w.m ^= w.s; return w; }
#define MAXW 600
#define HS 8192
static W wire[MAXW]; static int nw;
static int htab[HS]; static int derived[MAXW], queue[MAXW];
static u64 rs;
static inline u64 rnd(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static inline double urand(void){ return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
static inline unsigned hsh(W w){ u64 x = (w.s * 0x9E3779B97F4A7C15ULL) ^ (w.m * 0xC2B2AE3D27D4EB4FULL); return (unsigned)(x >> 45) & (HS - 1); }
static int lookup(W w){ unsigned h = hsh(w); while (htab[h] >= 0){ int i = htab[h]; if (wire[i].s == w.s && wire[i].m == w.m) return i; h = (h + 1) & (HS - 1);} return -1; }
static void build(void){ memset(htab, -1, sizeof htab); for (int i = 0; i < nw; i++){ unsigned h = hsh(wire[i]); while (htab[h] >= 0) h = (h + 1) & (HS - 1); htab[h] = i; } }
static inline int combos(W u, W v, W *out){
  int n = 0; u64 I = u.s & v.s; u64 opp = (u.m ^ v.m) & I; u64 same = I & ~opp; W r;
  if (I == 0){ r.s = u.s | v.s; r.m = u.m | v.m; out[n++] = nrm(r); r.m = u.m | (v.m ^ v.s); out[n++] = nrm(r); return n; }
  if (u.s == v.s){ if (same && opp){ r.s = same; r.m = u.m & same; out[n++] = nrm(r); r.s = opp; r.m = u.m & opp; out[n++] = nrm(r);} return n; }
  if (same == 0){ r.s = u.s ^ v.s; r.m = (u.m & ~I) | (v.m & ~I); out[n++] = nrm(r); }
  if (opp == 0){ r.s = u.s ^ v.s; r.m = (u.m & ~I) | ((v.m ^ v.s) & ~I); out[n++] = nrm(r); }
  if (same == 0 || opp == 0){
    if (I == v.s){ r.s = u.s; r.m = u.m ^ v.s; out[n++] = nrm(r); }
    else if (I == u.s){ r.s = v.s; r.m = v.m ^ u.s; out[n++] = nrm(r); } }
  return n;
}
static int dead, missing;
static void closure(void){
  build(); memset(derived, 0, sizeof(int) * nw); int qt = 0;
  for (int i = 0; i < N; i++){ derived[i] = 1; queue[qt++] = i; }
  W out[6];
  for (int qh = 0; qh < qt; qh++){ W a = wire[queue[qh]];
    for (int j = 0; j < qh; j++){ int n = combos(a, wire[queue[j]], out);
      for (int t = 0; t < n; t++){ int i = lookup(out[t]); if (i >= 0 && !derived[i]){ derived[i] = 1; queue[qt++] = i; } } } }
  missing = 0; dead = 0;
  for (int i = N; i < BASE; i++) if (!derived[i]) missing++;
  for (int i = BASE; i < nw; i++) if (!derived[i]) dead++;
}
static double A = 1.0, B = 1.0;
static double energy(void){ closure(); return (nw - BASE) + A * dead + B * missing; }
static int present(W w){ for (int i = 0; i < nw; i++) if (wire[i].s == w.s && wire[i].m == w.m) return 1; return 0; }
/* propose a wire one gate away from two random derived wires (uses derived[] of the current state) */
static int propose(W *res){
  for (int tries = 0; tries < 40; tries++){
    int a = rnd() % nw, b = rnd() % nw; if (a == b || !derived[a] || !derived[b]) continue;
    W out[6]; int n = combos(wire[a], wire[b], out); if (!n) continue;
    W r = out[rnd() % n]; if (r.s == 0 || present(r)) continue; *res = r; return 1; }
  return 0;
}
static void dump(const char *fn, int gates){
  FILE *f = fopen(fn, "w"); fprintf(f, "# K=%d gates=%d helpers=%d (helper wires, entries 0,1,-1; order arbitrary)\n", K, gates, nw - BASE);
  for (int i = BASE; i < nw; i++){ for (int x = 0; x < N; x++) fprintf(f, "%d ", (wire[i].s >> x & 1) ? ((wire[i].m >> x & 1) ? -1 : 1) : 0); fprintf(f, "\n"); }
  fclose(f);
}
int main(int argc, char **argv){
  K = atoi(argv[1]); N = 1 << K; FULL = (N == 64) ? ~0ULL : ((1ULL << N) - 1);
  double secs = atof(argv[3]); rs = 88172645463325252ULL ^ (strtoull(argv[4], 0, 10) * 0x9E3779B97F4A7C15ULL); double temp = atof(argv[5]); const char *outfn = argv[6];
  if (argc > 8){ A = atof(argv[7]); B = atof(argv[8]); }
  nw = 0; for (int i = 0; i < N; i++){ wire[nw].s = 1ULL << i; wire[nw].m = 0; nw++; }
  if (argc > 9){ FILE *tf = fopen(argv[9], "r"); char ln[4096];
    while (tf && fgets(ln, sizeof ln, tf)){ if (ln[0] == '#') continue; W w; w.s = 0; w.m = 0; char *p = ln; int x = 0;
      while (x < N){ char *e; long v = strtol(p, &e, 10); if (e == p) break; if (v){ w.s |= 1ULL << x; if (v < 0) w.m |= 1ULL << x; } p = e; x++; }
      if (x == N && w.s){ w = nrm(w); if (!present(w)) wire[nw++] = w; } }
    if (tf) fclose(tf); }
  else for (int a = 0; a < N; a++){ W w; w.s = FULL; w.m = 0; for (int x = 0; x < N; x++) if (__builtin_popcount(a & x) & 1) w.m |= 1ULL << x; wire[nw++] = nrm(w); }
  BASE = nw;
  FILE *f = fopen(argv[2], "r"); char line[4096];
  while (f && fgets(line, sizeof line, f)){ if (line[0] == '#') continue; W w; w.s = 0; w.m = 0; char *p = line; int x = 0, ok = 0;
    while (x < N){ char *e; long v = strtol(p, &e, 10); if (e == p) break; if (v){ w.s |= 1ULL << x; if (v < 0) w.m |= 1ULL << x; } p = e; x++; ok = 1; }
    if (ok && x == N && w.s){ w = nrm(w); if (!present(w)) wire[nw++] = w; } }
  if (f) fclose(f);
  double E = energy(); int best = (dead == 0 && missing == 0) ? nw - N : 1 << 30; printf("targets %d\n", BASE - N);
  printf("start: helpers %d dead %d missing %d gates %d\n", nw - BASE, dead, missing, nw - N); fflush(stdout);
  static W bestw[MAXW]; int bestnw = nw; memcpy(bestw, wire, sizeof(W) * nw);
  static W save[MAXW]; time_t t0 = time(0); u64 it = 0, acc = 0; u64 hist[MAXW]; memset(hist, 0, sizeof hist);
  u64 sincebest = 0;
  while (1){
    if ((it & 1023) == 0 && difftime(time(0), t0) >= secs) break;
    it++; sincebest++;
    if (sincebest > 3000000 && best < (1 << 30)){ memcpy(wire, bestw, sizeof(W) * bestnw); nw = bestnw; E = energy(); sincebest = 0; }
    int snw = nw; memcpy(save, wire, sizeof(W) * nw);
    /* derived[] must describe the current state for propose() */
    double mv = urand(); int changed = 0; int h = nw - BASE;
    if (mv < 0.30){ W r; if (nw < MAXW - 2 && propose(&r)){ wire[nw++] = r; changed = 1; } }
    else if (mv < 0.60){ if (h > 0){ int i = BASE + rnd() % h; wire[i] = wire[--nw]; changed = 1; } }
    else if (mv < 0.85){ W r; if (h > 0 && propose(&r)){ int i = BASE + rnd() % h; wire[i] = r; changed = 1; } }
    else { W r; if (h > 1 && propose(&r)){ int i = BASE + rnd() % h; wire[i] = wire[--nw]; h--; i = BASE + rnd() % h; wire[i] = r; changed = 1; } }
    if (!changed) continue;
    double E2 = energy();
    if (E2 <= E || urand() < exp(-(E2 - E) / temp)){ E = E2; acc++;
      if (dead == 0 && missing == 0){ int g = nw - N; hist[g]++;
        if (g < best){ best = g; bestnw = nw; memcpy(bestw, wire, sizeof(W) * nw); sincebest = 0; printf("t=%.0fs it=%llu: circuit with %d gates\n", difftime(time(0), t0), (unsigned long long)it, g); fflush(stdout); dump(outfn, g); } } }
    else { nw = snw; memcpy(wire, save, sizeof(W) * nw); closure(); }
  }
  printf("done: %llu moves, %llu accepted, best %d gates; feasible states visited by gate count:", (unsigned long long)it, (unsigned long long)acc, best);
  for (int g = 0; g < MAXW; g++) if (hist[g]) printf(" %d:%llu", g, (unsigned long long)hist[g]);
  printf("\n"); return 0;
}
