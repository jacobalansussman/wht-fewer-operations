// inplace.c  (g-3-illconditioned, 2026-10-10)
// Least number of IN-PLACE moves  w_i <- a*w_i + c*w_j  (a, c non-zero; scalings free, so a wire is a projective point)
// on W = 4 + m wires that take (e0, e1, e2, e3, 0^m) to the four target rows, in any order and scaling,
// with the m spare wires left as anything (garbage = 1) or as zero (garbage = 0).
// A move into a wire holding zero is a copy (one move); a move may also clear a wire to zero.
// "shears, one diagonal layer, shears" for the target is exactly this with m = 0 (a diagonal commutes through shears
// by changing their coefficients, so its place does not matter).
// Field GF(p); meet in the middle (the move set is closed under inverses). Exhaustive over GF(p) up to fd + bd moves.
// usage: inplace p m fd bd garbage tablebits rowsfile
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int p, W, m, P4, npts;
static int *canon_idx, *code_of;
static unsigned char (*dig)[4];
typedef struct { uint64_t *key; uint8_t *val; uint64_t mask; uint64_t n; } HT;
static void ht_init(HT *h, int bits) { h->mask = (1ull << bits) - 1; h->key = calloc(h->mask + 1, 8); h->val = calloc(h->mask + 1, 1); h->n = 0;
    if (!h->key || !h->val) { fprintf(stderr, "no memory\n"); exit(2); } }
static inline uint64_t hsh(uint64_t k) { k ^= k >> 33; k *= 0xff51afd7ed558ccdULL; k ^= k >> 33; k *= 0xc4ceb9fe1a85ec53ULL; k ^= k >> 33; return k; }
static int ht_get(HT *h, uint64_t k) { uint64_t i = hsh(k) & h->mask; while (h->key[i]) { if (h->key[i] == k) return h->val[i]; i = (i + 1) & h->mask; } return -1; }
static int ht_put(HT *h, uint64_t k, int v) {
    uint64_t i = hsh(k) & h->mask; while (h->key[i]) { if (h->key[i] == k) return 0; i = (i + 1) & h->mask; }
    h->key[i] = k; h->val[i] = (uint8_t)v; h->n++;
    if (h->n > (h->mask >> 2) * 3) { fprintf(stderr, "table full\n"); printf("TABLE FULL\n"); exit(3); }
    return 1; }
static uint64_t pack(const int *s) { int t[8]; memcpy(t, s, W * sizeof(int));
    for (int a = 1; a < W; a++) { int v = t[a], b = a - 1; while (b >= 0 && t[b] > v) { t[b + 1] = t[b]; b--; } t[b + 1] = v; }
    uint64_t k = 0; for (int a = 0; a < W; a++) k |= (uint64_t)(t[a] + 1) << (12 * a); return k; }
static void unpack(uint64_t k, int *s) { for (int a = 0; a < W; a++) s[a] = (int)((k >> (12 * a)) & 4095) - 1; }
static inline int comb(int ui, int c, int vi) { int code = 0, mult = 1;
    for (int k = 0; k < 4; k++) { int d = (dig[ui][k] + c * dig[vi][k]) % p; code += d * mult; mult *= p; } return canon_idx[code]; }
static void bfs(HT *h, uint64_t *start, size_t ns, int D, const char *name) {
    size_t cap = 1 << 20, nf = 0; uint64_t *fr = malloc(cap * 8);
    for (size_t i = 0; i < ns; i++) if (ht_put(h, start[i], 0)) { if (nf == cap) { cap *= 2; fr = realloc(fr, cap * 8); } fr[nf++] = start[i]; }
    printf("%s depth 0 states %zu\n", name, nf); fflush(stdout);
    for (int d = 1; d <= D; d++) {
        size_t cap2 = nf * 8 + 1024, n2 = 0; uint64_t *nx = malloc(cap2 * 8);
        for (size_t q = 0; q < nf; q++) {
            int s[8], t[8]; unpack(fr[q], s);
            for (int i = 0; i < W; i++) for (int j = 0; j < W; j++) { if (i == j || s[j] == 0) continue;
                int cmax = s[i] == 0 ? 1 : p - 1;
                for (int c = 1; c <= cmax; c++) {
                    memcpy(t, s, W * sizeof(int)); t[i] = comb(s[i], c, s[j]);
                    uint64_t k2 = pack(t);
                    if (ht_put(h, k2, d)) { if (n2 == cap2) { cap2 *= 2; nx = realloc(nx, cap2 * 8); if (!nx) { fprintf(stderr, "no memory\n"); exit(2); } } nx[n2++] = k2; }
                } }
        }
        free(fr); fr = nx; nf = n2;
        printf("%s depth %d new states %zu (total %llu)\n", name, d, nf, (unsigned long long)h->n); fflush(stdout);
    }
    free(fr);
}
static void show(uint64_t k) { int s[8]; unpack(k, s); printf("STATE");
    for (int a = 0; a < W; a++) { printf(" "); for (int q = 0; q < 4; q++) printf("%d%s", dig[s[a]][q], q < 3 ? "," : ""); } printf("\n"); }
static uint64_t step_down(HT *h, uint64_t k, int want) {   // a neighbour at depth `want`
    int s[8], t[8]; unpack(k, s);
    for (int i = 0; i < W; i++) for (int j = 0; j < W; j++) { if (i == j || s[j] == 0) continue;
        int cmax = s[i] == 0 ? 1 : p - 1;
        for (int c = 1; c <= cmax; c++) { memcpy(t, s, W * sizeof(int)); t[i] = comb(s[i], c, s[j]); uint64_t k2 = pack(t); if (ht_get(h, k2) == want) return k2; } }
    fprintf(stderr, "path broken\n"); exit(4);
}
int main(int argc, char **argv) {
    if (argc < 8) { fprintf(stderr, "usage: inplace p m fd bd garbage tablebits rowsfile\n"); return 1; }
    p = atoi(argv[1]); m = atoi(argv[2]); int fd = atoi(argv[3]), bd = atoi(argv[4]), garbage = atoi(argv[5]), bits = atoi(argv[6]);
    W = 4 + m; P4 = p * p * p * p;
    canon_idx = malloc(P4 * sizeof(int)); code_of = malloc(P4 * sizeof(int)); dig = malloc((size_t)P4 * 4);
    int inv[64]; for (int a = 1; a < p; a++) for (int b = 1; b < p; b++) if (a * b % p == 1) inv[a] = b;
    npts = 0; code_of[npts++] = 0;
    for (int code = 1; code < P4; code++) { int d[4], c = code; for (int k = 0; k < 4; k++) { d[k] = c % p; c /= p; }
        int f = 0; while (d[f] == 0) f++; if (d[f] == 1) code_of[npts++] = code; }
    int *idx_of = calloc(P4, sizeof(int));
    for (int i = 0; i < npts; i++) { idx_of[code_of[i]] = i; int c = code_of[i]; for (int k = 0; k < 4; k++) { dig[i][k] = c % p; c /= p; } }
    for (int code = 0; code < P4; code++) { int d[4], c = code; for (int k = 0; k < 4; k++) { d[k] = c % p; c /= p; }
        int f = 0; while (f < 4 && d[f] == 0) f++; if (f == 4) { canon_idx[code] = 0; continue; }
        int iv = inv[d[f]], cc = 0, mult = 1; for (int k = 0; k < 4; k++) { cc += (d[k] * iv % p) * mult; mult *= p; } canon_idx[code] = idx_of[cc]; }
    if (npts > 4094) { fprintf(stderr, "p too large for 12-bit packing\n"); return 1; }
    FILE *f = fopen(argv[7], "r"); int tg[4];
    for (int r = 0; r < 4; r++) { int code = 0, mult = 1; for (int k = 0; k < 4; k++) { int v; if (fscanf(f, "%d", &v) != 1) return 1; v = ((v % p) + p) % p; code += v * mult; mult *= p; } tg[r] = canon_idx[code]; }
    fclose(f);
    printf("inplace p=%d wires=%d fd=%d bd=%d garbage=%d points=%d\n", p, W, fd, bd, garbage, npts);
    HT F, B; ht_init(&F, bits); ht_init(&B, bits);
    int s[8]; for (int a = 0; a < 4; a++) { int code = 1; for (int q = 0; q < a; q++) code *= p; s[a] = canon_idx[code]; } for (int a = 4; a < W; a++) s[a] = 0;
    uint64_t st = pack(s); bfs(&F, &st, 1, fd, "forward");
    size_t nb = 0; uint64_t *bs = malloc(((size_t)npts + 4) * 8);
    for (int a = 0; a < 4; a++) s[a] = tg[a];
    if (m == 0) bs[nb++] = pack(s);
    else if (m == 1) { if (garbage) { for (int g = 0; g < npts; g++) { s[4] = g; bs[nb++] = pack(s); } } else { s[4] = 0; bs[nb++] = pack(s); } }
    else { fprintf(stderr, "m <= 1 only\n"); return 1; }
    bfs(&B, bs, nb, bd, "backward");
    int best = 1000; uint64_t wit = 0; unsigned long long nwit = 0;
    for (uint64_t i = 0; i <= B.mask; i++) if (B.key[i]) { int v = ht_get(&F, B.key[i]); if (v >= 0) { int tot = v + B.val[i];
        if (tot < best) { best = tot; wit = B.key[i]; nwit = 1; } else if (tot == best) nwit++; } }
    if (best == 1000) { printf("RESULT p=%d wires=%d garbage=%d: NO program with <= %d moves over GF(%d)\n", p, W, garbage, fd + bd, p); return 0; }
    printf("RESULT p=%d wires=%d garbage=%d: least number of moves = %d over GF(%d) (meeting states at that length: %llu)\n", p, W, garbage, best, p, nwit);
    if (argc > 8) {   // dump every state that lies on some shortest program, with its layer
        HT O; ht_init(&O, 22); size_t qc = 1 << 16, qn = 0, qh = 0; uint64_t *q = malloc(qc * 8);
        for (uint64_t i = 0; i <= B.mask; i++) if (B.key[i]) { int v = ht_get(&F, B.key[i]);
            if (v >= 0 && v + B.val[i] == best && ht_put(&O, B.key[i], v)) { if (qn == qc) { qc *= 2; q = realloc(q, qc * 8); } q[qn++] = B.key[i]; } }
        while (qh < qn) { uint64_t k0 = q[qh++]; int t = ht_get(&O, k0); int s0[8], t0[8]; unpack(k0, s0);
            int downF = (t > 0 && ht_get(&F, k0) == t), downB = (best - t > 0 && ht_get(&B, k0) == best - t);
            for (int i = 0; i < W; i++) for (int j = 0; j < W; j++) { if (i == j || s0[j] == 0) continue;
                int cmax = s0[i] == 0 ? 1 : p - 1;
                for (int c = 1; c <= cmax; c++) { memcpy(t0, s0, W * sizeof(int)); t0[i] = comb(s0[i], c, s0[j]); uint64_t k2 = pack(t0);
                    int lay = -1;
                    if (downF && ht_get(&F, k2) == t - 1) lay = t - 1;
                    else if (downB && ht_get(&B, k2) == best - t - 1) lay = t + 1;
                    if (lay >= 0 && ht_put(&O, k2, lay)) { if (qn == qc) { qc *= 2; q = realloc(q, qc * 8); } q[qn++] = k2; } } }
        }
        FILE *g = fopen(argv[8], "w"); fprintf(g, "# p=%d wires=%d best=%d : layer, then the wires (sorted), digits modulo p\n", p, W, best);
        unsigned long long per[64]; memset(per, 0, sizeof per);
        for (uint64_t i = 0; i <= O.mask; i++) if (O.key[i]) { int s1[8]; unpack(O.key[i], s1); per[O.val[i]]++; fprintf(g, "%d", O.val[i]);
            for (int a = 0; a < W; a++) { fprintf(g, " "); for (int z = 0; z < 4; z++) fprintf(g, "%d%s", dig[s1[a]][z], z < 3 ? "," : ""); } fprintf(g, "\n"); }
        fclose(g); printf("states on shortest programs, by layer:"); for (int t = 0; t <= best; t++) printf(" %llu", per[t]); printf("\n");
    }
    // print one path
    uint64_t path[64]; int np = 0; int df = ht_get(&F, wit); uint64_t k = wit; uint64_t tmp[64]; int nt = 0;
    tmp[nt++] = k; for (int d = df - 1; d >= 0; d--) { k = step_down(&F, k, d); tmp[nt++] = k; }
    for (int i = nt - 1; i >= 0; i--) path[np++] = tmp[i];
    k = wit; int db = ht_get(&B, wit); for (int d = db - 1; d >= 0; d--) { k = step_down(&B, k, d); path[np++] = k; }
    printf("PATH p=%d wires=%d moves=%d\n", p, W, np - 1);
    for (int i = 0; i < np; i++) show(path[i]);
    printf("END\n");
    return 0;
}
