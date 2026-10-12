/* cover_g.c m W K outfile  -- cover.c for any block size m <= 5 and any number W of arrays.   [h-2-clique17]
   Exact enumeration of the count vectors with at most K moves in which every form with q(I) = 1 selects at least W moves.
   Same search and the same two prunings as cover.c (the constant 'a point lies in at most mx product forms' is computed). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int m, W, NP, nf = 0, T = 0, K, mx = 0;
static uint32_t mask[16384];
static int *lst[31], lstn[31], cnt[16384], n[31];
static uint32_t frozen = 0;
static long long nodes = 0, leaves = 0;
static int prodidx[512], nprod = 0;
static FILE *out;
static int dot(int a, int b) { return __builtin_popcount(a & b) & 1; }
static void add(int z) { n[z]++; T++; for (int t = 0; t < lstn[z]; t++) cnt[lst[z][t]]++; }
static void rem(int z) { n[z]--; T--; for (int t = 0; t < lstn[z]; t++) cnt[lst[z][t]]--; }
static void dfs(void) {
    nodes++;
    int R = K - T, defP = 0;
    for (int i = 0; i < nprod; i++) { int d = W - cnt[prodidx[i]]; if (d > 0) defP += d; }
    if (defP > mx * R) return;
    int best = -1, bestc = 99, bestd = 0;
    for (int q = 0; q < nf; q++) if (cnt[q] < W) {
        int d = W - cnt[q]; if (d > R) return;
        int c = __builtin_popcount(mask[q] & ~frozen); if (c == 0) return;
        if (c < bestc || (c == bestc && d > bestd)) { best = q; bestc = c; bestd = d; }
    }
    if (best < 0) { leaves++; fprintf(out, "%d %u", T, frozen); for (int z = 0; z < NP; z++) fprintf(out, " %d", n[z]); fprintf(out, "\n"); return; }
    uint32_t saved = frozen, cand = mask[best] & ~frozen;
    while (cand) { int z = __builtin_ctz(cand); cand &= cand - 1; add(z); dfs(); rem(z); frozen |= 1u << z; }
    frozen = saved;
}
int main(int argc, char **argv) {
    m = atoi(argv[1]); W = atoi(argv[2]); K = atoi(argv[3]); out = fopen(argv[4], "w"); NP = (1 << m) - 1;
    int pi[15], pj[15], np = 0;
    for (int i = 0; i < m; i++) for (int j = i; j < m; j++) { pi[np] = i; pj[np] = j; np++; }
    for (int Q = 1; Q < (1 << np); Q++) {
        int lam = 0; for (int t = 0; t < np; t++) if ((Q >> t & 1) && pi[t] == pj[t]) lam ^= 1;
        if (!lam) continue;
        uint32_t mk = 0;
        for (int z = 1; z <= NP; z++) { int s = 0; for (int t = 0; t < np; t++) if ((Q >> t & 1) && (z >> pi[t] & 1) && (z >> pj[t] & 1)) s ^= 1; if (s) mk |= 1u << (z - 1); }
        mask[nf++] = mk;
    }
    for (int z = 0; z < NP; z++) { lst[z] = malloc(sizeof(int) * nf); lstn[z] = 0; for (int q = 0; q < nf; q++) if (mask[q] >> z & 1) lst[z][lstn[z]++] = q; }
    for (int a = 1; a <= NP; a++) for (int b = a + 1; b <= NP; b++) if (dot(a, b)) {
        uint32_t mk = 0; for (int z = 1; z <= NP; z++) if (dot(a, z) && dot(b, z)) mk |= 1u << (z - 1);
        int f = -1; for (int q = 0; q < nf; q++) if (mask[q] == mk) { f = q; break; }
        if (f < 0) { fprintf(stderr, "product form not found\n"); return 1; }
        prodidx[nprod++] = f;
    }
    for (int z = 0; z < NP; z++) { int c = 0; for (int i = 0; i < nprod; i++) if (mask[prodidx[i]] >> z & 1) c++; if (c > mx) mx = c; }
    printf("m = %d, W = %d, K = %d: forms with q(I)=1: %d; product forms: %d; a point lies in at most %d of them\n", m, W, K, nf, nprod, mx);
    dfs();
    printf("nodes %lld, leaves %lld\n", nodes, leaves);
    fclose(out); return 0;
}
