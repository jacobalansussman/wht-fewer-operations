// mincirc.c  (d-0-zeta, 2026-10-10)
// Exact minimum linear-circuit search over GF(p), projective count:
//   a gate computes a*u + b*v from two earlier values (inputs or gates), a, b any field elements;
//   scalings are free, so a value is a projective point; an output counts as computed when a gate (or input)
//   is proportional to its row.
// Every non-input target row must be the output of a gate, and making a target the moment it lies on a line through
// two available points never costs more. So: gates = (#non-input targets) + (#intermediate points), and the search is over
// SETS of m intermediate points; after each addition the targets on a line through two available points are added.
// usage: mincirc p n m [rowsfile]  (or rows on stdin)      (rows: n integers per target row, any number of rows; n even, p^n <= ~6e6)
//   prints whether a circuit with m intermediates exists; if yes prints one (the order of the points and how each is made).
// The answer NO is exhaustive over GF(p) for this m (dedup of intermediate sets of size <= 2 is exact: 2 ids packed in 64 bits).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int p, n, h, m;
static uint32_t P4, PN;
static uint32_t *add4;   // P4 x P4
static uint32_t *mul4;   // p x P4
static uint32_t *canon;  // PN
static uint8_t *inR;
static int32_t *cnt;
static uint32_t R[256]; static int nR;
static uint32_t T[64]; static int nT;
static uint32_t order[256]; static int nOrd;
static unsigned long long visited[8];

static inline uint32_t lin(uint32_t u, int a, uint32_t v) {   // canon(u + a v)
    uint32_t uh = u / P4, ul = u % P4, vh = v / P4, vl = v % P4;
    uint32_t hh = add4[(size_t)uh * P4 + mul4[(size_t)a * P4 + vh]];
    uint32_t ll = add4[(size_t)ul * P4 + mul4[(size_t)a * P4 + vl]];
    return canon[hh * P4 + ll];
}
static void add_point(uint32_t w) {
    for (int i = 0; i < nR; i++) for (int a = 1; a < p; a++) cnt[lin(w, a, R[i])]++;
    R[nR++] = w; inR[w] = 1;
}
static void remove_last(void) {
    uint32_t w = R[--nR]; inR[w] = 0;
    for (int i = 0; i < nR; i++) for (int a = 1; a < p; a++) cnt[lin(w, a, R[i])]--;
}
static int closure(void) {      // returns number of points added
    int added = 0, ch = 1;
    while (ch) {
        ch = 0;
        for (int i = 0; i < nT; i++) if (!inR[T[i]] && cnt[T[i]] > 0) { add_point(T[i]); added++; ch = 1; }
    }
    return added;
}
static int all_in(void) { for (int i = 0; i < nT; i++) if (!inR[T[i]]) return 0; return 1; }

// exact dedup of small intermediate sets
#define HB 22
static uint64_t *htab; static uint8_t *hused;
static int seen_set(uint32_t *s, int k) {     // k <= 2
    uint32_t a = s[0], b = k > 1 ? s[1] : 0xFFFFFFu;
    if (k > 1 && a > b) { uint32_t t = a; a = b; b = t; }
    uint64_t key = ((uint64_t)a << 32) | b;
    uint64_t hsh = (key * 0x9E3779B97F4A7C15ull) >> (64 - HB);
    while (hused[hsh]) { if (htab[hsh] == key) return 1; hsh = (hsh + 1) & ((1u << HB) - 1); }
    hused[hsh] = 1; htab[hsh] = key; return 0;
}
static uint32_t inter[16]; static int nI;
static uint32_t sol[256]; static int nSol;

static int dfs(int j) {       // j intermediates left; closure already applied; returns 1 on success
    if (all_in()) { nSol = nR; memcpy(sol, R, sizeof(uint32_t) * nR); return 1; }
    if (j == 0) return 0;
    visited[j]++;
    if (j == 1) {
        // the last intermediate must put some missing target on a line with an available point
        int base = nR;
        for (int i = 0; i < nT; i++) if (!inR[T[i]]) {
            for (int r = 0; r < base; r++) for (int a = 1; a < p; a++) {
                uint32_t w = lin(T[i], a, R[r]);
                if (inR[w] || cnt[w] <= 0) continue;
                add_point(w); int ad = closure();
                int ok = all_in();
                if (ok) { nSol = nR; memcpy(sol, R, sizeof(uint32_t) * nR); }
                for (int k = 0; k <= ad; k++) remove_last();
                if (ok) return 1;
            }
        }
        return 0;
    }
    int base = nR;
    // list the candidates (distinct points on lines through two available points)
    int cap = base * (base - 1) / 2 * (p - 1);
    uint32_t *cand = malloc(sizeof(uint32_t) * (cap + 1)); int nc = 0;
    for (int u = 0; u < base; u++) for (int v = 0; v < u; v++) for (int a = 1; a < p; a++) {
        uint32_t w = lin(R[u], a, R[v]);
        if (inR[w] || w == 0) continue;
        cand[nc++] = w;
    }
    // sort + unique
    int cmp(const void *x, const void *y);
    qsort(cand, nc, sizeof(uint32_t), cmp);
    int k2 = 0; for (int i = 0; i < nc; i++) if (i == 0 || cand[i] != cand[i - 1]) cand[k2++] = cand[i];
    nc = k2;
    for (int i = 0; i < nc; i++) {
        uint32_t w = cand[i];
        int isT = 0; for (int t = 0; t < nT; t++) if (T[t] == w) isT = 1;
        if (isT) continue;                         // cannot happen after closure, kept for safety
        inter[nI++] = w;
        if (nI <= 2 && seen_set(inter, nI)) { nI--; continue; }
        add_point(w); int ad = closure();
        int ok = dfs(j - 1);
        for (int k = 0; k <= ad; k++) remove_last();
        nI--;
        if (ok) { free(cand); return 1; }
    }
    free(cand); return 0;
}
int cmp(const void *x, const void *y) { uint32_t a = *(const uint32_t *)x, b = *(const uint32_t *)y; return a < b ? -1 : a > b; }

static void digits(uint32_t x, int *d) { for (int i = n - 1; i >= 0; i--) { d[i] = x % p; x /= p; } }
static uint32_t undigits(int *d) { uint32_t x = 0; for (int i = 0; i < n; i++) x = x * p + d[i]; return x; }

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: mincirc p n m < rows\n"); return 2; }
    p = atoi(argv[1]); n = atoi(argv[2]); m = atoi(argv[3]); h = n / 2;
    if (argc > 4 && !freopen(argv[4], "r", stdin)) { fprintf(stderr, "cannot open rows file\n"); return 2; }   // rows file instead of stdin
    P4 = 1; for (int i = 0; i < h; i++) P4 *= p; PN = P4 * P4;
    add4 = malloc(sizeof(uint32_t) * (size_t)P4 * P4); mul4 = malloc(sizeof(uint32_t) * (size_t)p * P4);
    canon = malloc(sizeof(uint32_t) * PN); inR = calloc(PN, 1); cnt = calloc(PN, sizeof(int32_t));
    htab = malloc(sizeof(uint64_t) << HB); hused = calloc(1u << HB, 1);
    int inv[64]; for (int a = 1; a < p; a++) for (int b = 1; b < p; b++) if (a * b % p == 1) inv[a] = b;
    {   // half tables
        int da[32], db[32];
        for (uint32_t x = 0; x < P4; x++) {
            uint32_t t = x; for (int i = h - 1; i >= 0; i--) { da[i] = t % p; t /= p; }
            for (int a = 0; a < p; a++) { uint32_t y = 0; for (int i = 0; i < h; i++) y = y * p + (da[i] * a) % p; mul4[(size_t)a * P4 + x] = y; }
            for (uint32_t z = 0; z < P4; z++) {
                uint32_t t2 = z; for (int i = h - 1; i >= 0; i--) { db[i] = t2 % p; t2 /= p; }
                uint32_t y = 0; for (int i = 0; i < h; i++) y = y * p + (da[i] + db[i]) % p;
                add4[(size_t)x * P4 + z] = y;
            }
        }
    }
    {
        int d[64];
        for (uint32_t x = 0; x < PN; x++) {
            digits(x, d); int f = -1; for (int i = 0; i < n; i++) if (d[i]) { f = i; break; }
            if (f < 0) { canon[x] = 0; continue; }
            int iv = inv[d[f]]; for (int i = 0; i < n; i++) d[i] = d[i] * iv % p;
            canon[x] = undigits(d);
        }
    }
    // inputs
    for (int i = 0; i < n; i++) { int d[64] = {0}; d[i] = 1; add_point(undigits(d)); }
    // targets
    int nrows = 0;
    while (1) {
        int d[64]; int okr = 1;
        for (int i = 0; i < n; i++) { int v; if (scanf("%d", &v) != 1) { okr = 0; break; } d[i] = ((v % p) + p) % p; }
        if (!okr) break;
        uint32_t t = canon[undigits(d)]; nrows++;
        if (t == 0) { printf("row %d is zero mod %d: skipped\n", nrows, p); continue; }
        int dup = inR[t]; for (int k = 0; k < nT; k++) if (T[k] == t) dup = 1;
        if (!dup) T[nT++] = t;
    }
    printf("p=%d n=%d rows=%d non-input distinct targets=%d  intermediates allowed m=%d  => gate budget %d\n", p, n, nrows, nT, m, nT + m);
    closure();
    int ok = dfs(m);
    printf("visited states by remaining budget:"); for (int j = m; j >= 1; j--) printf(" j=%d:%llu", j, visited[j]); printf("\n");
    if (!ok) { printf("RESULT p=%d: NO circuit with %d gates (exhaustive over GF(%d))\n", p, nT + m, p); return 0; }
    printf("RESULT p=%d: YES, circuit with %d gates. points in order (after the %d inputs):\n", p, nSol - n, n);
    for (int i = n; i < nSol; i++) {
        int d[64]; digits(sol[i], d);
        int isT = 0; for (int t = 0; t < nT; t++) if (T[t] == sol[i]) isT = 1;
        // find a pair
        int fu = -1, fv = -1, fa = 0, fb = 0;
        for (int u = 0; u < i && fu < 0; u++) for (int v = 0; v < u && fu < 0; v++) for (int a = 1; a < p && fu < 0; a++)
            if (lin(sol[u], a, sol[v]) == sol[i]) { fu = u; fv = v; fa = 1; fb = a; }
        printf("  g%-2d %s = [", i, isT ? "TARGET" : "inter ");
        for (int k = 0; k < n; k++) printf("%d%s", d[k], k + 1 < n ? " " : "");
        printf("]  from #%d + %d*#%d (projectively)\n", fu, fb, fv);
    }
    return 0;
}
