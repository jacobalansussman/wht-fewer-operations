// p-4-formula: "a bounded number of rectangles per node of the row tree". Exhaustive depth-first search, exact (bit masks).
// Balanced row tree, balanced column tree (aligned intervals). A row node of 2^d rows may carry up to r_d rectangles, each R x (one proper
// column node), the column nodes of one row node pairwise disjoint and not two siblings (their union would be one node).
// mode T (tiling): along a leaf-to-root path all column sets disjoint. mode X: overlaps allowed, minus-sets combine by XOR (then the SUM form needs repairs).
// Required: any two rows differ in exactly N/2 places (a Hadamard matrix). Symmetry cut: children of every row node sorted (sound: swapping them maps solutions to solutions).
// usage: pernode k seconds maxrect r-string(leaf first, e.g. 2111) T|X
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
static int k, N, ncol, xmode; static unsigned colnode[64]; static unsigned E[64], FULL;
static unsigned *om[8]; static int *oc[8]; static int no[8];
static unsigned long long nodes = 0, nsol = 0, nsyl = 0; static int best = 999, bestsyl = 999, maxrect = 999, deepest = -1; static double tlimit; static clock_t t0; static int stopped = 0;
static unsigned bestE[64], bestsylE[64]; static unsigned char *seen;
static int plo[200], psz[200], plev[200], npre = 0, parent[200]; static unsigned accs[200];
static int is_sylvester(void) {
    unsigned r[64];
    for (int y = 0; y < N; y++) { r[y] = E[y] ^ E[0]; if (r[y] & 1) r[y] ^= FULL; seen[r[y]] = 1; }
    int ok = 1;
    for (int y = 0; y < N && ok; y++) for (int z = y + 1; z < N; z++) if (!seen[r[y] ^ r[z]]) { ok = 0; break; }
    for (int y = 0; y < N; y++) seen[r[y]] = 0;
    return ok;
}
static int leaf_ok(int lo, unsigned e) {
    for (int size = 2; size <= N; size *= 2) if (lo % size == size / 2 && !(E[lo - size / 2] < e)) return 0;
    for (int z = 0; z < lo; z++) if (__builtin_popcount(e ^ E[z]) != N / 2) return 0;
    return 1;
}
static void build(int lo, int size, int lev, int par) { int me = npre++; plo[me] = lo; psz[me] = size; plev[me] = lev; parent[me] = par; if (size > 1) { build(lo, size / 2, lev - 1, me); build(lo + size / 2, size / 2, lev - 1, me); } }
static void go(int i, int cnt) {
    if (stopped) return;
    if ((++nodes & 0xFFFFF) == 0 && (double)(clock() - t0) / CLOCKS_PER_SEC > tlimit) { stopped = 1; return; }
    if (i == npre) {
        nsol++; int s = is_sylvester(); if (s) nsyl++;
        if (cnt < best) { best = cnt; memcpy(bestE, E, sizeof E); }
        if (s && cnt < bestsyl) { bestsyl = cnt; memcpy(bestsylE, E, sizeof E); }
        return;
    }
    unsigned acc = parent[i] < 0 ? 0 : accs[parent[i]];
    int d = plev[i]; int nopt = (i == 0) ? 1 : no[d];
    for (int c = 0; c < nopt; c++) {
        unsigned mk = om[d][c]; int cn = cnt + oc[d][c];
        if (cn > maxrect) continue;
        if (!xmode && (acc & mk)) continue;
        unsigned a = xmode ? (acc ^ mk) : (acc | mk);
        accs[i] = a;
        if (psz[i] == 1) { if (!leaf_ok(plo[i], a)) continue; E[plo[i]] = a; if (plo[i] > deepest) deepest = plo[i]; }
        go(i + 1, cn);
    }
}
int main(int argc, char **argv) {
    k = atoi(argv[1]); tlimit = atof(argv[2]); maxrect = atoi(argv[3]); const char *rs = argv[4]; xmode = (argv[5][0] == 'X'); N = 1 << k; FULL = (1u << N) - 1;
    for (int size = 1; size < N; size *= 2) for (int s = 0; s < N; s += size) colnode[ncol++] = (((1u << size) - 1) << s);
    for (int d = 0; d <= k; d++) {
        int r = d < k ? rs[d] - '0' : 0; om[d] = malloc(sizeof(unsigned) * 40000); oc[d] = malloc(sizeof(int) * 40000); no[d] = 0;
        om[d][no[d]] = 0; oc[d][no[d]++] = 0;
        if (r >= 1) for (int a = 0; a < ncol; a++) { om[d][no[d]] = colnode[a]; oc[d][no[d]++] = 1; }
        if (r >= 2) for (int a = 0; a < ncol; a++) for (int b = a + 1; b < ncol; b++) {
            if (colnode[a] & colnode[b]) continue; unsigned u = colnode[a] | colnode[b]; int isnode = (u == FULL);
            for (int c = 0; c < ncol; c++) if (colnode[c] == u) isnode = 1;
            if (isnode) continue; om[d][no[d]] = u; oc[d][no[d]++] = 2; }
        if (r >= 3) for (int a = 0; a < ncol; a++) for (int b = a + 1; b < ncol; b++) for (int c = b + 1; c < ncol; c++) {
            if ((colnode[a] & colnode[b]) || (colnode[a] & colnode[c]) || (colnode[b] & colnode[c])) continue;
            unsigned u = colnode[a] | colnode[b] | colnode[c]; int dup = (u == FULL);
            for (int j = 0; j < no[d]; j++) if (om[d][j] == u) { dup = 1; break; }
            if (dup) continue; om[d][no[d]] = u; oc[d][no[d]++] = 3; }
    }
    seen = calloc(1u << N, 1); build(0, N, k, -1); t0 = clock(); go(0, 0);
    printf("N=%d per-node limits (leaf first) %s mode %s maxrect %d: %s after %.0f s, %llu search nodes, deepest row completed %d | Hadamard matrices of this form (children sorted): %llu, fewest rectangles %d (tau %d, gates %d) | of them the transform up to relabelling and signs: %llu, fewest rectangles %d (tau %d, gates %d)\n",
           N, rs, xmode ? "X (overlaps, XOR)" : "T (tiling)", maxrect, stopped ? "STOPPED (not exhaustive)" : "EXHAUSTIVE", (double)(clock() - t0) / CLOCKS_PER_SEC, nodes, deepest, nsol, best, best + 1, N - 1 + best, nsyl, bestsyl, bestsyl + 1, N - 1 + bestsyl);
    if (nsyl) { printf("  example (transform), minus-set of each row as a hex mask over the columns:"); for (int y = 0; y < N; y++) printf(" %x", bestsylE[y]); printf("\n"); }
    if (nsol && best < bestsyl) { printf("  example (a Hadamard matrix with fewest rectangles):"); for (int y = 0; y < N; y++) printf(" %x", bestE[y]); printf("\n"); }
    return 0;
}
