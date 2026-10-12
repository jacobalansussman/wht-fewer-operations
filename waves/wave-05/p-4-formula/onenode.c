// p-4-formula: "at most one rectangle per node of the row tree" (the pattern of the 5 and the 13). Exhaustive depth-first search, exact.
// Balanced row tree and balanced column tree (aligned intervals). Each non-root row node R: no rectangle, or one rectangle R x C_R,
// C_R one proper column node; along every leaf-to-root path the C's are disjoint (a tiling). Row y's minus-set E_y = union of C_R, R containing y.
// Required: any two rows differ in exactly N/2 places (S is a Hadamard matrix). tau = 1 + rectangles; gates = N - 2 + tau (count G).
// usage: onenode k seconds [maxrect]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
static int k, N, ncol; static unsigned colnode[64]; static unsigned E[64], FULL;
static unsigned long long nodes = 0, nsol = 0, nsyl = 0; static int best = 999, bestsyl = 999, maxrect = 999; static double tlimit; static clock_t t0; static int stopped = 0;
static unsigned bestE[64], bestsylE[64]; static unsigned char *seen;
static int is_sylvester(void) {
    unsigned r[64];
    for (int y = 0; y < N; y++) { r[y] = E[y] ^ E[0]; if (r[y] & 1) r[y] ^= FULL; seen[r[y]] = 1; }
    int ok = 1;
    for (int y = 0; y < N && ok; y++) for (int z = y + 1; z < N; z++) if (!seen[r[y] ^ r[z]]) { ok = 0; break; }
    for (int y = 0; y < N; y++) seen[r[y]] = 0;
    return ok;
}
// visit the subtree whose rows are [lo, lo+size), acc = union of C's of the ancestors, cnt = rectangles so far
static void rec(int lo, int size, unsigned acc, int cnt);
static void after(int lo, int size, unsigned acc, int cnt) {
    if (size == 1) {
        for (int z = 0; z < lo; z++) if (__builtin_popcount(acc ^ E[z]) != N / 2) return;
        E[lo] = acc;
        return;
    }
}
static int leaf_ok(int lo, unsigned e) { for (int z = 0; z < lo; z++) if (__builtin_popcount(e ^ E[z]) != N / 2) return 0; return 1; }
// continuation-passing by explicit ordering: we enumerate nodes in preorder using an array of (lo,size)
static int plo[200], psz[200], npre = 0, parent[200]; static unsigned accs[200]; static int cnts[200];
static void build(int lo, int size, int par) { int me = npre++; plo[me] = lo; psz[me] = size; parent[me] = par; if (size > 1) { build(lo, size / 2, me); build(lo + size / 2, size / 2, me); } }
static void go(int i, int cnt) {
    if (stopped) return;
    if ((++nodes & 0xFFFFFF) == 0 && (double)(clock() - t0) / CLOCKS_PER_SEC > tlimit) { stopped = 1; return; }
    if (i == npre) {
        nsol++; int s = is_sylvester(); if (s) nsyl++;
        if (cnt < best) { best = cnt; memcpy(bestE, E, sizeof E); }
        if (s && cnt < bestsyl) { bestsyl = cnt; memcpy(bestsylE, E, sizeof E); }
        return;
    }
    unsigned acc = parent[i] < 0 ? 0 : accs[parent[i]];
    int nopt = (i == 0) ? 0 : ncol;
    for (int c = -1; c < nopt; c++) {
        unsigned a = acc; int cn = cnt;
        if (c >= 0) { if (acc & colnode[c]) continue; a |= colnode[c]; cn++; if (cn > maxrect) continue; }
        accs[i] = a;
        if (psz[i] == 1) { if (!leaf_ok(plo[i], a)) continue; E[plo[i]] = a; }
        go(i + 1, cn);
    }
}
int main(int argc, char **argv) {
    k = atoi(argv[1]); tlimit = atof(argv[2]); if (argc > 3) maxrect = atoi(argv[3]); N = 1 << k; FULL = (N == 32) ? 0xFFFFFFFFu : ((1u << N) - 1);
    for (int size = 1; size < N; size *= 2) for (int s = 0; s < N; s += size) colnode[ncol++] = ((size == 32 ? 0xFFFFFFFFu : ((1u << size) - 1)) << s);
    seen = calloc(1u << (N < 26 ? N : 26), 1); build(0, N, -1); t0 = clock(); go(0, 0);
    printf("N=%d maxrect=%d: %s after %.0f s, %llu search nodes | Hadamard matrices of this form: %llu, fewest rectangles %d (tau %d, gates %d) | of them the transform up to relabelling and signs: %llu, fewest rectangles %d (tau %d, gates %d)\n",
           N, maxrect, stopped ? "STOPPED (not exhaustive)" : "EXHAUSTIVE", (double)(clock() - t0) / CLOCKS_PER_SEC, nodes, nsol, best, best + 1, N - 1 + best, nsyl, bestsyl, bestsyl + 1, N - 1 + bestsyl);
    if (nsyl) { printf("  example (transform), minus-set of each row as a bit mask over the columns:"); for (int y = 0; y < N; y++) printf(" %x", bestsylE[y]); printf("\n"); }
    else if (nsol) { printf("  example (a Hadamard matrix, not the transform):"); for (int y = 0; y < N; y++) printf(" %x", bestE[y]); printf("\n"); }
    return 0;
}
