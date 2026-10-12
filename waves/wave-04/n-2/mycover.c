/* mycover.c  M W K out [forbidden mask] [root lo] [root hi]     (n-2, written from scratch; integers only)
   Lists every count vector n on the non-zero M-bit directions with at most K moves such that every quadratic form q
   (no constant term) with q(I)=1 selects at least W moves.   Output lines: T frozenmask n_1..n_(2^M-1)  (a "leaf");
   every feasible vector = exactly one leaf + extra moves on directions not frozen at that leaf.
   Forms are indexed by (diagonal bits d, off-diagonal bits o): q(z) = parity(d&z) + sum_{i<j} o_ij z_i z_j.
   Bounds (both valid): (1) a form short by d needs d more moves; (2) product forms (a.z)(b.z), a.b=1: the sum of their
   shortfalls drops by at most c per move, c = the largest number of still-short product forms through one free direction. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static int M, W, K, NP, NF;
static uint32_t *fm; static unsigned char *cnt;
static int **inl, *inn;
static int n[64], T;
static uint32_t frozen;
static int *prod, nprod;
static long long nodes, leaves;
static FILE *out;
static int rlo = 0, rhi = 1 << 30;
static int par(unsigned x) { return __builtin_popcount(x) & 1; }
static void addp(int z) { n[z]++; T++; int *l = inl[z]; for (int t = 0; t < inn[z]; t++) cnt[l[t]]++; }
static void remp(int z) { n[z]--; T--; int *l = inl[z]; for (int t = 0; t < inn[z]; t++) cnt[l[t]]--; }
static void dfs(int depth) {
    nodes++;
    int R = K - T;
    /* bound 2 */
    int def = 0; int cov[64]; memset(cov, 0, sizeof cov);
    for (int i = 0; i < nprod; i++) { int f = prod[i]; int d = W - cnt[f]; if (d > 0) { def += d; uint32_t mk = fm[f] & ~frozen; while (mk) { int z = __builtin_ctz(mk); mk &= mk - 1; cov[z]++; } } }
    int c = 0; for (int z = 0; z < NP; z++) if (cov[z] > c) c = cov[z];
    if (def > c * R) return;
    int best = -1, bc = 1000, bd = 0;
    for (int f = 0; f < NF; f++) if (cnt[f] < W) {
        int d = W - cnt[f]; if (d > R) return;
        int fc = __builtin_popcount(fm[f] & ~frozen); if (!fc) return;
        if (fc < bc || (fc == bc && d > bd)) { best = f; bc = fc; bd = d; }
    }
    if (best < 0) { leaves++; fprintf(out, "%d %u", T, frozen); for (int z = 0; z < NP; z++) fprintf(out, " %d", n[z]); fprintf(out, "\n"); return; }
    uint32_t saved = frozen, cand = fm[best] & ~frozen; int idx = 0;
    while (cand) {
        int z = 31 - __builtin_clz(cand); cand &= ~(1u << z);          /* highest first (the other program goes lowest first) */
        if (depth > 0 || (idx >= rlo && idx < rhi)) { addp(z); dfs(depth + 1); remp(z); }
        frozen |= 1u << z; idx++;
    }
    frozen = saved;
}
int main(int argc, char **argv) {
    M = atoi(argv[1]); W = atoi(argv[2]); K = atoi(argv[3]); out = fopen(argv[4], "w");
    if (argc > 5) frozen = (uint32_t)strtoul(argv[5], 0, 10);
    if (argc > 7) { rlo = atoi(argv[6]); rhi = atoi(argv[7]); }
    NP = (1 << M) - 1; int no = M * (M - 1) / 2;
    fm = malloc(sizeof(uint32_t) << (M + no)); NF = 0;
    for (unsigned d = 0; d < (1u << M); d++) if (par(d)) for (unsigned o = 0; o < (1u << no); o++) {
        uint32_t mk = 0;
        for (unsigned z = 1; z <= (unsigned)NP; z++) { int s = par(d & z), t = 0; for (int i = 0; i < M; i++) for (int j = i + 1; j < M; j++, t++) if ((o >> t & 1) && (z >> i & 1) && (z >> j & 1)) s ^= 1; if (s) mk |= 1u << (z - 1); }
        fm[NF++] = mk;
    }
    cnt = calloc(NF, 1); inl = malloc(sizeof(int *) * NP); inn = calloc(NP, sizeof(int));
    for (int z = 0; z < NP; z++) { inl[z] = malloc(sizeof(int) * NF); for (int f = 0; f < NF; f++) if (fm[f] >> z & 1) inl[z][inn[z]++] = f; }
    prod = malloc(sizeof(int) * NP * NP); nprod = 0;
    for (unsigned a = 1; a <= (unsigned)NP; a++) for (unsigned b = a + 1; b <= (unsigned)NP; b++) if (par(a & b)) {
        uint32_t mk = 0; for (unsigned z = 1; z <= (unsigned)NP; z++) if (par(a & z) && par(b & z)) mk |= 1u << (z - 1);
        int f = -1; for (int g = 0; g < NF; g++) if (fm[g] == mk) { f = g; break; }
        if (f < 0) { fprintf(stderr, "product form missing\n"); return 1; }
        prod[nprod++] = f;
    }
    printf("M=%d W=%d K=%d forms=%d products=%d frozen0=%u root=[%d,%d)\n", M, W, K, NF, nprod, frozen, rlo, rhi);
    dfs(0);
    printf("nodes %lld leaves %lld\n", nodes, leaves);
    fclose(out); return 0;
}
