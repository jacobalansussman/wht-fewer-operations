/* cover.c K  -- exact enumeration of the count vectors that pass counting, block size 5, W = 4.   [h-2-clique17]
   Points: the 31 non-zero directions z.  Forms: the 16384 quadratic forms q (no constant term) with q(I) = 1.
   Counting: every such form must select at least 4 moves:  sum over z with q(z) = 1 of n_z >= 4.
   Depth-first search, integers only.  At a node take a violated form with the fewest points still allowed, branch on the
   point to add; after a branch returns that point is frozen for the later branches (so every feasible vector lies above
   exactly one leaf, with its extra moves on points that are not frozen at that leaf).
   Pruning (valid): each point lies in at most 64 of the 240 product forms (a.z)(b.z), a.b = 1, so
   (sum of their positive deficits) <= 64 * (moves left); and (largest deficit) <= moves left.
   Output: one line per leaf:  T  frozenmask  n_1 .. n_31                                                             */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define NP 31
static uint32_t mask[16384]; static int nf = 0;
static int *lst[NP], lstn[NP];
static int cnt[16384], n[NP], T = 0, K;
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
    for (int i = 0; i < nprod; i++) { int d = 4 - cnt[prodidx[i]]; if (d > 0) defP += d; }
    if (defP > 64 * R) return;
    int best = -1, bestc = 99, bestd = 0;
    for (int q = 0; q < nf; q++) if (cnt[q] < 4) {
        int d = 4 - cnt[q]; if (d > R) return;
        int c = __builtin_popcount(mask[q] & ~frozen); if (c == 0) return;
        if (c < bestc || (c == bestc && d > bestd)) { best = q; bestc = c; bestd = d; }
    }
    if (best < 0) {
        leaves++; fprintf(out, "%d %u", T, frozen);
        for (int z = 0; z < NP; z++) fprintf(out, " %d", n[z]);
        fprintf(out, "\n"); return;
    }
    uint32_t saved = frozen, cand = mask[best] & ~frozen;
    while (cand) { int z = __builtin_ctz(cand); cand &= cand - 1; add(z); dfs(); rem(z); frozen |= 1u << z; }
    frozen = saved;
}
int main(int argc, char **argv) {
    K = atoi(argv[1]); out = fopen(argv[2], "w");
    int pi[15], pj[15], np = 0;
    for (int i = 0; i < 5; i++) for (int j = i; j < 5; j++) { pi[np] = i; pj[np] = j; np++; }
    for (int Q = 1; Q < (1 << 15); Q++) {
        int lam = 0; for (int t = 0; t < 15; t++) if ((Q >> t & 1) && pi[t] == pj[t]) lam ^= 1;
        if (!lam) continue;
        uint32_t mk = 0;
        for (int z = 1; z < 32; z++) { int s = 0; for (int t = 0; t < 15; t++) if ((Q >> t & 1) && (z >> pi[t] & 1) && (z >> pj[t] & 1)) s ^= 1; if (s) mk |= 1u << (z - 1); }
        mask[nf++] = mk;
    }
    for (int z = 0; z < NP; z++) { lst[z] = malloc(sizeof(int) * nf); lstn[z] = 0; for (int q = 0; q < nf; q++) if (mask[q] >> z & 1) lst[z][lstn[z]++] = q; }
    for (int a = 1; a < 32; a++) for (int b = a + 1; b < 32; b++) if (dot(a, b)) {
        uint32_t mk = 0; for (int z = 1; z < 32; z++) if (dot(a, z) && dot(b, z)) mk |= 1u << (z - 1);
        int f = -1; for (int q = 0; q < nf; q++) if (mask[q] == mk) { f = q; break; }
        if (f < 0) { fprintf(stderr, "product form not found\n"); return 1; }
        prodidx[nprod++] = f;
    }
    int mx = 0; for (int z = 0; z < NP; z++) { int c = 0; for (int i = 0; i < nprod; i++) if (mask[prodidx[i]] >> z & 1) c++; if (c > mx) mx = c; }
    printf("forms with q(I)=1: %d; product forms: %d; a point lies in at most %d of them; K = %d\n", nf, nprod, mx, K);
    if (mx > 64) { fprintf(stderr, "bound constant wrong\n"); return 1; }
    dfs();
    printf("nodes %lld, leaves %lld\n", nodes, leaves);
    fclose(out); return 0;
}
