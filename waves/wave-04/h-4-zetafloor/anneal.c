// anneal.c (h-4-zetafloor, 2026-10-11): local search over SETS of m helper points for a linear circuit over GF(p), count (G).
// Same model as d-0-zeta/mincirc.c (tables copied from it): a point (projective) becomes available when it lies on a line
// through two available points; gates = (#non-input targets) + (#helpers that are reached). A state is a set of m helpers.
// Energy = W * (#targets not reached) + (#helpers not reached).  Energy 0 with all targets reached = a circuit with
// (#targets + m) gates over GF(p)  (a CANDIDATE over the rationals until lifted and replayed).
// usage: anneal p n m seconds seed rowsfile [T0] [T1]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <time.h>

static int p, n, h, m;
static uint32_t P4, PN;
static uint32_t *add4, *mul4, *canon;
static uint8_t *inR;
static int32_t *cnt;
static uint32_t R[512]; static int nR;
static uint32_t T[64]; static int nT;
static uint64_t rs;
static inline uint64_t rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static inline uint32_t lin(uint32_t u, int a, uint32_t v) {
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
static void digits(uint32_t x, int *d) { for (int i = n - 1; i >= 0; i--) { d[i] = x % p; x /= p; } }
static uint32_t undigits(int *d) { uint32_t x = 0; for (int i = 0; i < n; i++) x = x * p + d[i]; return x; }

static uint32_t H[64];
static int reachedT, reachedH;
static int W = 4;
// evaluate: returns energy; leaves the reached points in R[n..nR) (caller must call unwind())
static int eval(void) {
    int ch = 1; reachedT = 0; reachedH = 0;
    while (ch) {
        ch = 0;
        for (int i = 0; i < nT; i++) if (!inR[T[i]] && cnt[T[i]] > 0) { add_point(T[i]); reachedT++; ch = 1; }
        for (int i = 0; i < m; i++) if (H[i] && !inR[H[i]] && cnt[H[i]] > 0) { add_point(H[i]); reachedH++; ch = 1; }
    }
    // distinct helpers reached is what matters; duplicates or helpers equal to targets count as unreached-but-harmless
    return W * (nT - reachedT) + (m - reachedH);
}
static void unwind(void) { while (nR > n) remove_last(); }

int main(int argc, char **argv) {
    if (argc < 7) { fprintf(stderr, "usage: anneal p n m seconds seed rowsfile [T0] [T1]\n"); return 2; }
    p = atoi(argv[1]); n = atoi(argv[2]); m = atoi(argv[3]); double secs = atof(argv[4]); rs = 88172645463325252ull ^ (uint64_t)atoll(argv[5]) * 0x9E3779B97F4A7C15ull;
    FILE *f = fopen(argv[6], "r"); if (!f) { fprintf(stderr, "no rows file\n"); return 2; }
    double T0 = argc > 7 ? atof(argv[7]) : 1.2, T1 = argc > 8 ? atof(argv[8]) : 0.25;
    h = n / 2; P4 = 1; for (int i = 0; i < h; i++) P4 *= p; PN = P4 * P4;
    add4 = malloc(sizeof(uint32_t) * (size_t)P4 * P4); mul4 = malloc(sizeof(uint32_t) * (size_t)p * P4);
    canon = malloc(sizeof(uint32_t) * PN); inR = calloc(PN, 1); cnt = calloc(PN, sizeof(int32_t));
    int inv[64]; for (int a = 1; a < p; a++) for (int b = 1; b < p; b++) if (a * b % p == 1) inv[a] = b;
    { int da[32], db[32];
      for (uint32_t x = 0; x < P4; x++) {
        uint32_t t = x; for (int i = h - 1; i >= 0; i--) { da[i] = t % p; t /= p; }
        for (int a = 0; a < p; a++) { uint32_t y = 0; for (int i = 0; i < h; i++) y = y * p + (da[i] * a) % p; mul4[(size_t)a * P4 + x] = y; }
        for (uint32_t z = 0; z < P4; z++) {
            uint32_t t2 = z; for (int i = h - 1; i >= 0; i--) { db[i] = t2 % p; t2 /= p; }
            uint32_t y = 0; for (int i = 0; i < h; i++) y = y * p + (da[i] + db[i]) % p;
            add4[(size_t)x * P4 + z] = y;
        } } }
    { int d[64];
      for (uint32_t x = 0; x < PN; x++) {
        digits(x, d); int fz = -1; for (int i = 0; i < n; i++) if (d[i]) { fz = i; break; }
        if (fz < 0) { canon[x] = 0; continue; }
        int iv = inv[d[fz]]; for (int i = 0; i < n; i++) d[i] = d[i] * iv % p;
        canon[x] = undigits(d);
      } }
    for (int i = 0; i < n; i++) { int d[64] = {0}; d[i] = 1; add_point(undigits(d)); }
    while (1) {
        int d[64]; int okr = 1;
        for (int i = 0; i < n; i++) { int v; if (fscanf(f, "%d", &v) != 1) { okr = 0; break; } d[i] = ((v % p) + p) % p; }
        if (!okr) break;
        uint32_t t = canon[undigits(d)]; if (t == 0) continue;
        int dup = inR[t]; for (int k = 0; k < nT; k++) if (T[k] == t) dup = 1;
        if (!dup) T[nT++] = t;
    }
    printf("anneal p=%d n=%d targets=%d helpers m=%d => gate budget %d ; %.0f s ; seed %s ; T %.2f -> %.2f\n", p, n, nT, m, nT + m, secs, argv[5], T0, T1);
    fflush(stdout);
    uint32_t S0[64]; int nS0 = 0;
    if (argc > 9) { FILE *g = fopen(argv[9], "r"); char buf[256]; while (g && fscanf(g, "%255s", buf) == 1) { int d[64]; if ((int)strlen(buf) != n) continue; for (int i = 0; i < n; i++) d[i] = buf[i] - '0'; S0[nS0++] = canon[undigits(d)]; } printf("start file: %d helpers\n", nS0); }
    time_t t0 = time(NULL);
    unsigned long long evals = 0, restarts = 0, hits = 0; int best = 1 << 30;
    long sweep = 200000L;                       // moves per restart
    while (difftime(time(NULL), t0) < secs) {
        restarts++;
        // random start: helpers on lines through items (inputs, targets, earlier helpers)
        for (int i = 0; i < m; i++) H[i] = 0;
        for (int i = 0; i < m; i++) {
            uint32_t w = 0; int tries = 0;
            while (!w && tries++ < 100) {
                uint32_t a = (rnd() % 3 == 0) ? T[rnd() % nT] : R[rnd() % n];
                uint32_t b = (i > 0 && rnd() % 2) ? H[rnd() % i] : R[rnd() % n];
                if (!b) b = R[rnd() % n];
                w = lin(a, 1 + rnd() % (p - 1), b); if (inR[w]) w = 0;
            }
            H[i] = w;
        }
        if (nS0 >= m) {                          // seeded start: a random m-subset of the start helpers, then 0..2 random replacements
            int idx[64]; for (int i = 0; i < nS0; i++) idx[i] = i;
            for (int i = 0; i < m; i++) { int j = i + rnd() % (nS0 - i); int t = idx[i]; idx[i] = idx[j]; idx[j] = t; H[i] = S0[idx[i]]; }
        }
        int E = eval(); unwind(); evals++;
        for (long it = 0; it < sweep; it++) {
            if ((it & 4095) == 0 && difftime(time(NULL), t0) >= secs) break;
            double temp = T0 + (T1 - T0) * (double)it / sweep;
            int j = rnd() % m; uint32_t old = H[j], w = 0;
            int kind = rnd() % 4;
            // item pool: inputs, targets, helpers
            #define ITEM() ({ uint32_t _x; int _r = rnd() % (n + nT + m); _x = _r < n ? R[_r] : (_r < n + nT ? T[_r - n] : H[_r - n - nT]); _x; })
            uint32_t a, b;
            if (kind == 0) { a = T[rnd() % nT]; b = ITEM(); }          // put a target on a line with an item
            else { a = ITEM(); b = ITEM(); }
            if (!a || !b || a == b) continue;
            w = lin(a, 1 + rnd() % (p - 1), b);
            if (!w || inR[w] || w == old) continue;
            int isT = 0; for (int t = 0; t < nT; t++) if (T[t] == w) isT = 1;
            if (isT) continue;
            int dupl = 0; for (int i = 0; i < m; i++) if (H[i] == w) dupl = 1;
            if (dupl) continue;
            H[j] = w; int E2 = eval(); unwind(); evals++;
            if (E2 <= E || exp((E - E2) / temp) * 18446744073709551615.0 > (double)rnd()) {
                E = E2;
                if (E < best) { best = E; printf("  [%4.0fs] best energy %d (restart %llu)\n", difftime(time(NULL), t0), best, restarts); fflush(stdout); }
                if (E == 0) {
                    hits++;
                    if (hits <= (unsigned long long)(getenv("MAXHITS") ? atoll(getenv("MAXHITS")) : 40)) {
                        printf("HIT %llu: circuit with %d gates over GF(%d). helpers:", hits, nT + m, p);
                        for (int i = 0; i < m; i++) { int d[64]; digits(H[i], d); printf(" ["); for (int q = 0; q < n; q++) printf("%d", d[q]); printf("]"); }
                        printf("\n"); fflush(stdout);
                    }
                    break;
                }
            } else H[j] = old;
        }
    }
    printf("DONE p=%d n=%d m=%d: evals %llu restarts %llu hits %llu best energy %d (energy = %d*missing targets + unreached helpers)\n", p, n, m, evals, restarts, hits, best, W);
    return 0;
}
