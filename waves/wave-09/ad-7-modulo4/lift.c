// lift.c (ad-7): does a circuit found modulo 2 lift to the whole numbers modulo M = 4, 8, 16 ?
// Input (stdin): lines "SOL c1 .. c7" from enum2 (codes of the intermediate points modulo 2; code = the row read as a
// binary number, first entry = highest bit).  The targets are the rows of rows_B4.txt (argv[2]); n = 8 inputs.
// A lift: every one of the 7 + 8 points gets ONE vector modulo M that reduces to it modulo 2 (targets: the row itself, up to
// a unit), and there is an order in which every point is u + c*v (c a unit modulo M, wires taken up to units) of two earlier
// points or inputs.  Why only units: with 15 gates, a gate with an even coefficient is a copy modulo 2, which would leave a
// circuit with 14 gates modulo 2, and there is none (enum_m6_*.out).
// Exhaustive over all orders and all lifts of the given set (branches are cut only by "this lifted point was already tried
// first at an ancestor", which loses nothing because a derivable point can always be made first).
// usage: lift M rowsfile < solutions
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int M, n = 8, NI = 7;   // NI = number of intermediates per record (argv[3], default 7)
static int inv[16];
static int nT; static int Tcode[16];
static int isT[256], isS[256];
static int have[256]; static uint32_t val[256];      // lifted vector, 4 bits per entry, canonical
static int av[64]; static int nav;
static uint32_t forb[4096]; static int forbc[4096]; static int nforb;
static long long nodes; static int best; static long long nlift;
static int bestset[64]; static uint32_t bestval[64]; static int nbest;

static inline uint32_t canon(uint32_t w) {
    int f = 0;
    for (int i = 0; i < n; i++) { int e = (w >> (4 * i)) & 15; if (e & 1) { f = inv[e]; break; } }
    uint32_t r = 0;
    for (int i = 0; i < n; i++) { int e = (w >> (4 * i)) & 15; r |= (uint32_t)((e * f) % M) << (4 * i); }
    return r;
}
static inline uint32_t comb(uint32_t u, int c, uint32_t v) {
    uint32_t r = 0;
    for (int i = 0; i < n; i++) { int e = (((u >> (4 * i)) & 15) + c * ((v >> (4 * i)) & 15)) % M; r |= (uint32_t)e << (4 * i); }
    return r;
}
static inline int code2(uint32_t w) { int c = 0; for (int i = 0; i < n; i++) c = (c << 1) | ((w >> (4 * i)) & 1); return c; }
static uint32_t rowval(int code) { uint32_t r = 0; for (int i = 0; i < n; i++) if ((code >> (n - 1 - i)) & 1) r |= 1u << (4 * i); return r; }

static int closure(void) {        // add every target that is now a gate away; returns how many were added
    int added = 0, ch = 1;
    while (ch) {
        ch = 0;
        for (int a = 0; a < nav && !ch; a++) for (int b = 0; b < a && !ch; b++) {
            int c0 = av[a] ^ av[b];
            if (!isT[c0] || have[c0]) continue;
            for (int c = 1; c < M; c += 2) {
                uint32_t w = canon(comb(val[av[a]], c, val[av[b]]));
                if (w == rowval(c0)) { have[c0] = 1; val[c0] = w; av[nav++] = c0; added++; ch = 1; break; }
            }
        }
    }
    return added;
}
static int ntargets(void) { int t = 0; for (int i = 0; i < nT; i++) t += have[Tcode[i]]; return t; }
static int dfs(void) {
    int ad = closure(); nodes++;
    int t = ntargets();
    if (t > best) { best = t; nbest = nav; for (int i = 0; i < nav; i++) { bestset[i] = av[i]; bestval[i] = val[av[i]]; } }
    int ok = (t == nT);
    if (!ok) {
        int f0 = nforb;
        // candidates
        static uint32_t cw[64][4096]; static int cc[64][4096]; static int depth = 0;
        int d = depth++; int nc = 0;
        for (int a = 0; a < nav; a++) for (int b = 0; b < a; b++) {
            int c0 = av[a] ^ av[b];
            if (!isS[c0] || have[c0]) continue;
            for (int c = 1; c < M; c += 2) {
                uint32_t w = canon(comb(val[av[a]], c, val[av[b]]));
                int dup = 0;
                for (int k = 0; k < nc; k++) if (cc[d][k] == c0 && cw[d][k] == w) { dup = 1; break; }
                if (!dup) for (int k = 0; k < nforb; k++) if (forbc[k] == c0 && forb[k] == w) { dup = 1; break; }
                if (!dup && nc < 4096) { cc[d][nc] = c0; cw[d][nc] = w; nc++; }
            }
        }
        for (int k = 0; k < nc && !ok; k++) {
            int c0 = cc[d][k]; uint32_t w = cw[d][k];
            have[c0] = 1; val[c0] = w; av[nav++] = c0;
            ok = dfs();
            if (!ok) { nav--; have[c0] = 0; if (nforb < 4096) { forbc[nforb] = c0; forb[nforb] = w; nforb++; } }
        }
        depth--;
        if (!ok) nforb = f0;
    }
    if (!ok) { for (int k = 0; k < ad; k++) { nav--; have[av[nav]] = 0; } }
    return ok;
}
static int cmpi(const void *a, const void *b) { return *(const int *)a - *(const int *)b; }
int main(int argc, char **argv) {
    M = atoi(argv[1]); if (argc > 3) NI = atoi(argv[3]);
    for (int a = 1; a < M; a += 2) for (int b = 1; b < M; b += 2) if (a * b % M == 1) inv[a] = b;
    FILE *f = fopen(argv[2], "r"); int v, k = 0, code = 0;
    while (fscanf(f, "%d", &v) == 1) { code = (code << 1) | (v & 1); if (++k == n) { Tcode[nT++] = code; isT[code] = 1; k = 0; code = 0; } }
    fclose(f);
    // read and dedupe the sets
    static char line[4096]; int cap = 1 << 16, ns = 0; int (*sets)[8] = malloc(sizeof(int[8]) * cap);
    while (fgets(line, sizeof line, stdin)) {
        if (strncmp(line, "SOL ", 4)) continue;
        int s[8], m = 0; char *p = line + 4; char *e;
        while (m < 8) { long x = strtol(p, &e, 10); if (e == p) break; s[m++] = (int)x; p = e; }
        if (m != NI) continue;
        qsort(s, NI, sizeof(int), cmpi);
        if (ns == cap) { cap *= 2; sets = realloc(sets, sizeof(int[8]) * cap); }
        for (int q = NI; q < 8; q++) s[q] = 0; memcpy(sets[ns], s, sizeof(int) * 8); ns++;
    }
    int cmp7(const void *a, const void *b); qsort(sets, ns, sizeof(int[8]), cmp7);
    int nu = 0; for (int i = 0; i < ns; i++) if (i == 0 || memcmp(sets[i], sets[i - 1], sizeof(int) * 8)) memcpy(sets[nu++], sets[i], sizeof(int) * 8);
    printf("modulus %d: %d solution records, %d distinct sets of %d intermediates\n", M, ns, nu, NI);
    long long hist[16] = {0}; long long lifted = 0, totnodes = 0; int control_ok = 0;
    for (int i = 0; i < nu; i++) {
        memset(have, 0, sizeof have); memset(isS, 0, sizeof isS); nav = 0; nforb = 0; best = -1; nodes = 0;
        for (int q = 0; q < NI; q++) isS[sets[i][q]] = 1;
        for (int q = 0; q < n; q++) { int c0 = 1 << (n - 1 - q); have[c0] = 1; val[c0] = rowval(c0); av[nav++] = c0; }
        int ok = dfs(); totnodes += nodes; hist[best]++;
        if (ok) {
            lifted++;
            if (lifted <= 5) {
                printf("LIFT modulo %d of set", M); for (int q = 0; q < NI; q++) printf(" %d", sets[i][q]); printf(" : points in order (code:vector)");
                for (int q = n; q < nav; q++) { printf(" %d:", av[q]); for (int z = 0; z < n; z++) printf("%d", (val[av[q]] >> (4 * z)) & 15); }
                printf("\n");
            }
        } else if (i < 3 || best >= 7) {
            if (control_ok < 12) { control_ok++;
                printf("no lift for set"); for (int q = 0; q < NI; q++) printf(" %d", sets[i][q]);
                printf(" ; most targets reached %d of %d ; a best partial:", best, nT);
                for (int q = n; q < nbest; q++) { printf(" %d%s:", bestset[q], isT[bestset[q]] ? "T" : ""); for (int z = 0; z < n; z++) printf("%d", (bestval[q] >> (4 * z)) & 15); }
                printf("\n"); }
        }
    }
    printf("RESULT modulus %d: %lld of %d sets lift (8 targets + the intermediates).  nodes searched %lld\n", M, lifted, nu, totnodes);
    printf("  histogram of the most targets reachable by any lift of a set: ");
    for (int t = 0; t <= nT; t++) if (hist[t]) printf(" %d targets: %lld sets;", t, hist[t]);
    printf("\n");
    return 0;
}
int cmp7(const void *a, const void *b) { return memcmp(a, b, sizeof(int) * 8); }
