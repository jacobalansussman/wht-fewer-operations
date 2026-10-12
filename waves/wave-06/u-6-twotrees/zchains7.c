// u-6-twotrees / zchains.c : SUBSET SUMS with one, two or three input chains, and a TREE walk through the outputs.  Count (G).
// Exact whole-number arithmetic (bit masks of 0/1 rows); the best program found is replayed on all N basis vectors at the end.
// Program shape:  for each chain j (an order c_j of the N inputs) hold the running sums F^j_b = x_(c_j[0]) + ... + x_(c_j[b])
//   (N - 1 gates for the first chain, N - 2 for each further one: the total of all inputs is shared).
//   Outputs: y_S = sum of x_T over T inside S.  Walk: a spanning tree on {0} and the N outputs; a tree edge parent -> child costs
//   the number of running sums of ONE chain needed to write (child - parent): the number of places where that difference changes
//   value along the chain (with a 0 added after the last input).  Each such term is one gate.  The root 0 is free, so the first
//   output made costs (terms - 1); the code reports gates = held + MST - 1.
// The search anneals the chain orders (swap two places, or reverse a segment) with the MST weight as objective.
// usage: zchains k nchains iters seed T0 [start: 0 gray orders rotated, 1 binary orders rotated]     (k <= 7; this is zchains.c with 128-bit rows)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
typedef unsigned long long u64; typedef unsigned __int128 u128;
static int k, N, nc; static int ord[3][128]; static u128 row[3][129];
static int D[129][129], Dj[129][129];
static unsigned long long rs = 88172645463325252ULL;
static inline unsigned rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (unsigned)(rs >> 11); }
static void rows(int j) { for (int S = 0; S < N; S++) { u128 m = 0; for (int b = 0; b < N; b++) if ((ord[j][b] & ~S) == 0) m |= (u128)1 << b; row[j][S] = m; } row[j][N] = 0; }
static inline int runs(u128 a, u128 a2) { u128 P = a & ~a2, M = ~a & a2; u128 x = (P ^ (P >> 1)) | (M ^ (M >> 1)); return __builtin_popcountll((u64)x) + __builtin_popcountll((u64)(x >> 64)); }
static int mst(int *parent, int *pj) {
    for (int a = 0; a <= N; a++) for (int b = a + 1; b <= N; b++) { int best = 1 << 20, bj = 0; for (int j = 0; j < nc; j++) { int r = runs(row[j][a], row[j][b]); if (r < best) { best = r; bj = j; } } D[a][b] = D[b][a] = best; Dj[a][b] = Dj[b][a] = bj; }
    int in[129], key[129], par[129]; for (int i = 0; i <= N; i++) { in[i] = 0; key[i] = 1 << 20; par[i] = -1; } key[N] = 0; int w = 0;
    for (int it = 0; it <= N; it++) { int b = -1; for (int i = 0; i <= N; i++) if (!in[i] && (b < 0 || key[i] < key[b])) b = i; in[b] = 1; w += key[b]; if (parent) { parent[b] = par[b]; pj[b] = par[b] >= 0 ? Dj[b][par[b]] : 0; }
        for (int i = 0; i <= N; i++) if (!in[i] && D[b][i] < key[i]) { key[i] = D[b][i]; par[i] = b; } }
    return w;
}
static int gray(int i) { return i ^ (i >> 1); }
static int rot(int x, int r) { r %= k; return ((x << r) | (x >> (k - r))) & (N - 1); }
// ---- extra vertices (Steiner points): full wires that are not outputs.  Candidates: the indicator of every lattice interval
// [L, S] = {T : L inside T inside S} with L not empty (the wires Yates' method holds).  Same edge cost as before.
static u128 vrow[3][2400]; 
static int mstv(int nv) {
    static int key[2400], in[2400]; int w = 0; for (int i = 0; i < nv; i++) { in[i] = 0; key[i] = 1 << 20; } key[0] = 0;
    for (int it = 0; it < nv; it++) { int b = -1; for (int i = 0; i < nv; i++) if (!in[i] && (b < 0 || key[i] < key[b])) b = i; in[b] = 1; w += key[b];
        for (int i = 0; i < nv; i++) if (!in[i]) { int d = 1 << 20; for (int j = 0; j < nc; j++) { int r = runs(vrow[j][b], vrow[j][i]); if (r < d) d = r; } if (d < key[i]) key[i] = d; } }
    return w;
}
static void steiner(int rounds) {
    int nv = 0; for (int j = 0; j < nc; j++) vrow[j][0] = 0; nv = 1;
    for (int S = 0; S < N; S++) { for (int j = 0; j < nc; j++) vrow[j][nv] = row[j][S]; nv++; }
    int w = mstv(nv), w0 = w, added = 0;
    static int cl[2400], cs[2400], used[2400]; int ncand = 0;
    for (int S = 0; S < N; S++) for (int L = S; L > 0; L = (L - 1) & S) { cl[ncand] = L; cs[ncand] = S; used[ncand] = 0; ncand++; }
    for (int r = 0; r < rounds; r++) {
        int bw = w, bc = -1;
        for (int c = 0; c < ncand; c++) if (!used[c]) {
            for (int j = 0; j < nc; j++) { u128 m = 0; for (int b = 0; b < N; b++) if ((ord[j][b] & ~cs[c]) == 0 && (cl[c] & ~ord[j][b]) == 0) m |= (u128)1 << b; vrow[j][nv] = m; }
            int ww = mstv(nv + 1); if (ww < bw) { bw = ww; bc = c; }
        }
        if (bc < 0) break;
        for (int j = 0; j < nc; j++) { u128 m = 0; for (int b = 0; b < N; b++) if ((ord[j][b] & ~cs[bc]) == 0 && (cl[bc] & ~ord[j][b]) == 0) m |= (u128)1 << b; vrow[j][nv] = m; }
        used[bc] = 1; nv++; w = bw; added++;
    }
    int held = (N - 1) + (nc - 1) * (N - 2);
    printf("WITH EXTRA VERTICES (lattice intervals, greedy, %d candidates): MST %d -> %d with %d extra vertices | GATES = %d | terms per output %.3f\n", ncand, w0, w, added, held + w - 1, (double)w / N);
}
int main(int argc, char **argv) {
    k = atoi(argv[1]); nc = atoi(argv[2]); long iters = atol(argv[3]); rs ^= (u64)atoi(argv[4]) * 0x9E3779B97F4A7C15ULL; double T0 = atof(argv[5]); int start = argc > 6 ? atoi(argv[6]) : 0;
    N = 1 << k;
    for (int j = 0; j < nc; j++) { for (int b = 0; b < N; b++) ord[j][b] = rot(start ? b : gray(b), j * (k / nc ? k / nc : 1)); rows(j); }
    int cur = mst(NULL, NULL), best = cur; int bord[3][128]; memcpy(bord, ord, sizeof ord);
    printf("k=%d N=%d chains=%d start MST=%d\n", k, N, nc, cur);
    for (long it = 0; it < iters; it++) {
        double T = T0 * (1.0 - (double)it / iters) + 1e-9;
        int j = rnd() % nc, a = rnd() % N, b = rnd() % N; if (a == b) continue; if (a > b) { int t = a; a = b; b = t; }
        int sv[128]; memcpy(sv, ord[j], sizeof sv);
        if (rnd() & 1) { int t = ord[j][a]; ord[j][a] = ord[j][b]; ord[j][b] = t; } else { for (int x = a, y = b; x < y; x++, y--) { int t = ord[j][x]; ord[j][x] = ord[j][y]; ord[j][y] = t; } }
        rows(j); int c = mst(NULL, NULL);
        if (c <= cur || (double)(rnd() % 1000000) / 1e6 < exp((cur - c) / T)) { cur = c; if (c < best) { best = c; memcpy(bord, ord, sizeof ord); } }
        else { memcpy(ord[j], sv, sizeof sv); rows(j); }
    }
    memcpy(ord, bord, sizeof ord); for (int j = 0; j < nc; j++) rows(j);
    int parent[129], pj[129]; int w = mst(parent, pj);
    // exact replay: rebuild every output as parent + (terms of one chain) and compare with the subset-sum row
    int terms = 0, bad = 0, used[3] = {0, 0, 0};
    for (int S = 0; S < N; S++) {
        int p = parent[S], j = pj[S]; int v[129]; long acc[128];
        for (int b = 0; b < N; b++) { int a1 = (row[j][S] >> b) & 1, a0 = (row[j][p] >> b) & 1; v[b] = a1 - a0; } v[N] = 0;
        for (int b = 0; b < N; b++) acc[b] = (row[j][p] >> b) & 1;                 // parent, in chain-j coordinates
        for (int b = 0; b < N; b++) { int c = v[b] - v[b + 1]; if (c) { terms++; used[j]++; for (int b2 = 0; b2 <= b; b2++) acc[b2] += c; } }   // add c * F^j_b
        for (int b = 0; b < N; b++) if (acc[b] != (long)((ord[j][b] & ~S) == 0)) bad = 1;
    }
    int held = (N - 1) + (nc - 1) * (N - 2);
    printf("BEST MST=%d  replay terms=%d (per chain %d %d %d) replay %s | held %d | GATES = held + MST - 1 = %d | Yates %d | MST/N = %.3f\n", w, terms, used[0], used[1], used[2], bad ? "FAILED" : "exact", held, held + w - 1, (N / 2) * k, (double)w / N);
    for (int j = 0; j < nc; j++) { printf("chain %d:", j); for (int b = 0; b < N; b++) printf(" %d", ord[j][b]); printf("\n"); }
    int hist[129]; memset(hist, 0, sizeof hist); for (int S = 0; S < N; S++) hist[D[S][parent[S]]]++;
    printf("edge costs:"); for (int c = 0; c <= 128; c++) if (hist[c]) printf(" %d:%d", c, hist[c]); printf("\n");
    if (argc > 7) steiner(atoi(argv[7]));
    return bad;
}
