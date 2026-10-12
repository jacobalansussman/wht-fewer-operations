// r2_brute.c (r-2, 11 October 2026): an INDEPENDENT count of helper sets for minimum circuits in count (G) over GF(p).
// Count (G): a gate is any a*u + b*v; scalings free, so a wire is a point of projective space; an output counts when a wire
// is proportional to its row.  A circuit with m helpers = a set of m points (not inputs, not targets) such that, starting
// from the inputs, every helper and every target can be added one at a time, each on a line through two points already there.
// Method here (different from d-0's mincirc on purpose):
//   - collinearity by a table of line numbers for all pairs of points (no counting array, no "last helper" shortcut);
//   - the first (m - B) helpers are taken among the points buildable at their turn (forced: the first non-target wire built
//     after the inputs and the targets that follow is buildable);
//   - the last B helpers are taken over ALL points of the space, with the one condition that at least one of them is buildable
//     at once (forced for the same reason); then a plain fixpoint decides whether everything can be built.
// usage: r2_brute p n m B [print]  < rows       prints the number of distinct helper sets; with print=1 every set ("SET ...").
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int p, n, m, B, NP, PN, doprint;
static int *code2id, *id2code; static int32_t *lid;
static int inv[128];
static int canon_code(int *d) { int f = -1; for (int i = 0; i < n; i++) if (d[i]) { f = i; break; } if (f < 0) return -1;
    int iv = inv[d[f]], c = 0; for (int i = 0; i < n; i++) c = c * p + d[i] * iv % p; return c; }
static void digits(int c, int *d) { for (int i = n - 1; i >= 0; i--) { d[i] = c % p; c /= p; } }
#define L(a, b) lid[(size_t)(a) * NP + (b)]
static int av[64], nav; static int tg[64], ntg; static uint8_t *isav, *istg;
static int helpers[16]; static int nh;
static int *sols; static size_t nsol, capsol;
static int buildable(int x) { for (int u = 0; u < nav; u++) { int l = L(av[u], x); for (int v = u + 1; v < nav; v++) if (L(av[u], av[v]) == l) return 1; } return 0; }
static int closure(void) { int added = 0, ch = 1; while (ch) { ch = 0; for (int i = 0; i < ntg; i++) if (!isav[tg[i]] && buildable(tg[i])) { av[nav++] = tg[i]; isav[tg[i]] = 1; added++; ch = 1; } } return added; }
static int alltg(void) { for (int i = 0; i < ntg; i++) if (!isav[tg[i]]) return 0; return 1; }
static void record(void) { if (nsol == capsol) { capsol = capsol ? 2 * capsol : 4096; sols = realloc(sols, capsol * m * sizeof(int)); }
    int *d = sols + nsol * m; memcpy(d, helpers, m * sizeof(int));
    for (int i = 0; i < m; i++) for (int j = i + 1; j < m; j++) if (d[j] < d[i]) { int t = d[i]; d[i] = d[j]; d[j] = t; } nsol++; }
static int fix(int *pend, int np) {      // can all pending points be built from av?  (av is not changed)
    int A[64], P[32], na = nav; memcpy(A, av, nav * sizeof(int)); memcpy(P, pend, np * sizeof(int));
    int ch = 1;
    while (np > 0 && ch) { ch = 0;
        for (int i = 0; i < np; i++) { int x = P[i], found = 0;
            for (int u = 0; u < na && !found; u++) { int l = L(A[u], x); for (int v = u + 1; v < na; v++) if (L(A[u], A[v]) == l) { found = 1; break; } }
            if (found) { A[na++] = x; P[i] = P[--np]; i--; ch = 1; } } }
    return np == 0; }
static unsigned long long nfix;
static void brute(void) {
    int pend[32], np0 = 0; for (int i = 0; i < ntg; i++) if (!isav[tg[i]]) pend[np0++] = tg[i];
    if (np0 == 0) return;                               // fewer helpers suffice: not a set of exactly m
    uint8_t *cons = calloc(NP, 1); int *cl = malloc(NP * sizeof(int)); int nc = 0;
    for (int x = 0; x < NP; x++) if (!isav[x] && !istg[x] && buildable(x)) { cons[x] = 1; cl[nc++] = x; }
    if (B == 1) { for (int i = 0; i < nc; i++) { int x = cl[i]; pend[np0] = x; nfix++; if (fix(pend, np0 + 1)) { helpers[nh] = x; record(); } } }
    else if (B == 2) { for (int i = 0; i < nc; i++) { int x = cl[i]; pend[np0] = x;
            for (int y = 0; y < NP; y++) { if (y == x || isav[y] || istg[y]) continue; pend[np0 + 1] = y; nfix++;
                if (fix(pend, np0 + 2)) { helpers[nh] = x; helpers[nh + 1] = y; record(); } } } }
    else if (B == 3) { for (int i = 0; i < nc; i++) { int x = cl[i]; pend[np0] = x;
            for (int y = 0; y < NP; y++) { if (y == x || isav[y] || istg[y]) continue; pend[np0 + 1] = y;
                for (int z = y + 1; z < NP; z++) { if (z == x || isav[z] || istg[z]) continue; pend[np0 + 2] = z; nfix++;
                    if (fix(pend, np0 + 3)) { helpers[nh] = x; helpers[nh + 1] = y; helpers[nh + 2] = z; record(); } } } } }
    free(cons); free(cl); }
static void forced(int level) {
    if (level == m - B) { brute(); return; }
    if (alltg()) return;
    int *cl = malloc(NP * sizeof(int)); int nc = 0;
    for (int x = 0; x < NP; x++) if (!isav[x] && !istg[x] && buildable(x)) cl[nc++] = x;
    for (int i = 0; i < nc; i++) { int x = cl[i]; av[nav++] = x; isav[x] = 1; helpers[nh++] = x; int ad = closure();
        forced(level + 1);
        for (int k = 0; k < ad; k++) isav[av[--nav]] = 0; isav[av[--nav]] = 0; nh--; }
    free(cl); }
static int cmpm(const void *x, const void *y) { return memcmp(x, y, m * sizeof(int)); }
int main(int argc, char **argv) {
    p = atoi(argv[1]); n = atoi(argv[2]); m = atoi(argv[3]); B = atoi(argv[4]); doprint = argc > 5 ? atoi(argv[5]) : 0;
    if (B > m) B = m;
    for (int a = 1; a < p; a++) for (int b = 1; b < p; b++) if (a * b % p == 1) inv[a] = b;
    PN = 1; for (int i = 0; i < n; i++) PN *= p; NP = (PN - 1) / (p - 1);
    code2id = malloc(PN * sizeof(int)); id2code = malloc(NP * sizeof(int)); int d[64], e[64], f[64]; int id = 0;
    for (int c = 0; c < PN; c++) { code2id[c] = -1; digits(c, d); if (canon_code(d) == c) { code2id[c] = id; id2code[id++] = c; } }
    lid = malloc((size_t)NP * NP * sizeof(int32_t)); memset(lid, 0xff, (size_t)NP * NP * sizeof(int32_t));
    int nl = 0; int *Ls = malloc((p + 1) * sizeof(int));
    for (int a = 0; a < NP; a++) for (int b = a + 1; b < NP; b++) if (L(a, b) < 0) {
        digits(id2code[a], d); digits(id2code[b], e); int k = 0; Ls[k++] = a;
        for (int t = 0; t < p; t++) { for (int i = 0; i < n; i++) f[i] = (e[i] + t * d[i]) % p; Ls[k++] = code2id[canon_code(f)]; }
        for (int i = 0; i < k; i++) for (int j = 0; j < k; j++) if (i != j) L(Ls[i], Ls[j]) = nl;
        nl++; }
    isav = calloc(NP, 1); istg = calloc(NP, 1);
    for (int i = 0; i < n; i++) { for (int j = 0; j < n; j++) d[j] = (i == j); int x = code2id[canon_code(d)]; av[nav++] = x; isav[x] = 1; }
    while (1) { int ok = 1; for (int i = 0; i < n; i++) { int v; if (scanf("%d", &v) != 1) { ok = 0; break; } d[i] = ((v % p) + p) % p; } if (!ok) break;
        int c = canon_code(d); if (c < 0) continue; int x = code2id[c]; if (isav[x] || istg[x]) continue; istg[x] = 1; tg[ntg++] = x; }
    closure();
    forced(0);
    qsort(sols, nsol, m * sizeof(int), cmpm); size_t u = 0;
    for (size_t i = 0; i < nsol; i++) if (i == 0 || memcmp(sols + i * m, sols + (i - 1) * m, m * sizeof(int))) { memmove(sols + u * m, sols + i * m, m * sizeof(int)); u++; }
    printf("R2 p=%d n=%d points=%d lines=%d targets=%d helpers m=%d (last %d over all points): %zu distinct helper sets, gates %d  [fixpoint tests %llu]\n", p, n, NP, nl, ntg, m, B, u, ntg + m, nfix);
    if (doprint) for (size_t i = 0; i < u; i++) { printf("SET"); for (int k = 0; k < m; k++) { digits(id2code[sols[i * m + k]], d); printf(" "); for (int q = 0; q < n; q++) printf(q ? ",%d" : "%d", d[q]); } printf("\n"); }
    return 0; }
