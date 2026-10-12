// lifth.c (ag-1): lift a modulo-2 circuit WITH ONE FREE FORM w to a 2-adic circuit with ONE HALVING.   Count (G).
// Wires are vectors of whole numbers modulo 2^pb (pb = P for wires that do not depend on the halving, P - e after a halving
// by 2^e), known up to odd factors (canonical: first odd entry = 1).
// Slots: every residue of the set S (intermediates) and every target row gets ONE wire, made by a gate a + c*b, c odd.
// One more pair of gates, made together:  V = p + c*q (c odd), where residue(p) + residue(q) = residue(u) for a third
// available wire u (V is the "wasted" gate: second wire with u's residue), and H = (u - s*V)/2^e, s odd, e >= 1 the exact
// power of 2 dividing u - s*V, P - e >= 2; H must have residue w.  (V of the kind u + 2^f z is excluded: then H is a direct
// gate on u and z and the circuit has no halving; see ag-1.md.)
// Targets: a target is added the moment some a + c*b is an odd multiple of its row modulo 2^min(pb); it is then known exactly.
// With EXTRA = 1: one more wire of ANY residue, any gate a + c*b (c any, result primitive), usable everywhere (V, H, u included).
// Search: all orders, all lifts; a candidate that failed at a node is not retried below its later siblings (a wire that can
// be made now can be made first; everything is monotone).
// usage: lifth P rowsfile [extra] < lines "w s1 s2 ..."      rows: n = 8 whole numbers per target
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int P, n = 8, EXTRA = 0, VERB = 0;
static int inv16[16];
typedef struct { int res; uint32_t val; int pb; int kind; int a, b, c, u, s, e; } Wire;   // kind 0 input,1 S,2 target,3 V,4 H,5 extra
static Wire wr[64]; static int nw;
static int nT; static int Tcode[16]; static int Trow[16][8];
static int slotS[256], slotT[256], filled[256];   // filled[res]: a slot wire with this residue exists
static int haveV, haveH, haveX, Wres;
static long long nodes, nodecap = 200000000LL, nmacro, ntri, nresH[256], nacc, naccnew; static int best, capped;
typedef struct { int kind, slot; uint32_t v1, v2; int pb; } Cand;
static Cand forb[20000]; static int nforb;

static inline int ent(uint32_t w, int i) { return (w >> (4 * i)) & 15; }
static inline uint32_t red(uint32_t w, int pb) { uint32_t m = (1u << pb) - 1, r = 0; for (int i = 0; i < n; i++) r |= (uint32_t)(ent(w, i) & m) << (4 * i); return r; }
static inline uint32_t canon(uint32_t w, int pb) {
    int M = 1 << pb, f = 0;
    for (int i = 0; i < n; i++) { int e = ent(w, i) & (M - 1); if (e & 1) { f = inv16[e] & (M - 1); break; } }
    uint32_t r = 0; for (int i = 0; i < n; i++) r |= (uint32_t)((ent(w, i) * f) & (M - 1)) << (4 * i);
    return r;
}
static inline uint32_t comb(uint32_t u, int c, uint32_t v, int pb) {
    int M = 1 << pb; uint32_t r = 0;
    for (int i = 0; i < n; i++) r |= (uint32_t)((ent(u, i) + c * ent(v, i)) & (M - 1)) << (4 * i);
    return r;
}
static inline int res2(uint32_t w) { int c = 0; for (int i = 0; i < n; i++) c = (c << 1) | (ent(w, i) & 1); return c; }
static uint32_t rowval(int t, int pb) { int M = 1 << pb; uint32_t r = 0; for (int i = 0; i < n; i++) r |= (uint32_t)(((Trow[t][i] % M) + M) % M) << (4 * i); return canon(r, pb); }
static int tindex(int code) { for (int t = 0; t < nT; t++) if (Tcode[t] == code) return t; return -1; }

static int closure(void) {
    int added = 0, ch = 1;
    while (ch) {
        ch = 0;
        for (int a = 0; a < nw && !ch; a++) for (int b = 0; b < a && !ch; b++) {
            int c0 = wr[a].res ^ wr[b].res;
            if (!slotT[c0] || filled[c0]) continue;
            int pb = wr[a].pb < wr[b].pb ? wr[a].pb : wr[b].pb; int t = tindex(c0);
            for (int c = 1; c < (1 << pb); c += 2)
                if (canon(comb(wr[a].val, c, wr[b].val, pb), pb) == rowval(t, pb)) {
                    filled[c0] = 1; wr[nw] = (Wire){c0, rowval(t, P), P, 2, a, b, c, 0, 0, 0}; nw++; added++; ch = 1; break; }
        }
        if (EXTRA && !ch) for (int a = 0; a < nw && !ch; a++) for (int b = 0; b < nw && !ch; b++) {
            int c0 = wr[a].res; if (a == b || !slotT[c0] || filled[c0]) continue;
            int pb = wr[a].pb < wr[b].pb ? wr[a].pb : wr[b].pb; int t = tindex(c0);
            for (int c = 2; c < (1 << pb); c += 2)
                if (canon(comb(wr[a].val, c, wr[b].val, pb), pb) == rowval(t, pb)) {
                    filled[c0] = 1; wr[nw] = (Wire){c0, rowval(t, P), P, 2, a, b, c, 0, 0, 0}; nw++; added++; ch = 1; break; }
        }
    }
    return added;
}
static int ntargets(void) { int t = 0; for (int i = 0; i < nT; i++) t += filled[Tcode[i]]; return t; }
static int isforb(Cand *c) { for (int k = 0; k < nforb; k++) if (forb[k].kind == c->kind && forb[k].slot == c->slot && forb[k].v1 == c->v1 && forb[k].v2 == c->v2 && forb[k].pb == c->pb) return 1; return 0; }
static Wire solw[64]; static int nsol;
static int dfs(void) {
    int ad = closure(); nodes++;
    int t = ntargets(); if (t > best) best = t;
    int ok = (t == nT);
    if (ok) { nsol = nw; memcpy(solw, wr, sizeof(Wire) * nw); }
    if (!ok && nodes > nodecap) capped = 1;
    if (!ok && !capped) {
        int f0 = nforb; int cap = 4096, nc = 0; Cand *cd = malloc(sizeof(Cand) * cap); Wire *cwv = malloc(sizeof(Wire) * cap * 2);
        #define PUSH(K, SL, V1, V2, PB, W1, W2) do { Cand cc = {K, SL, V1, V2, PB}; int dup = isforb(&cc); \
            for (int k = 0; k < nc && !dup; k++) if (cd[k].kind == cc.kind && cd[k].slot == cc.slot && cd[k].v1 == cc.v1 && cd[k].v2 == cc.v2 && cd[k].pb == cc.pb) dup = 1; \
            if (!dup) { if (nc == cap) { cap *= 2; cd = realloc(cd, sizeof(Cand) * cap); cwv = realloc(cwv, sizeof(Wire) * cap * 2); } cd[nc] = cc; cwv[2 * nc] = W1; cwv[2 * nc + 1] = W2; nc++; } } while (0)
        // (1) the pair V, H
        if (!haveV) for (int u = 0; u < nw; u++) for (int p = 0; p < nw; p++) for (int q = 0; q < nw; q++) {
            if (p == u || q == u || p == q) continue;
            int tri = ((wr[p].res ^ wr[q].res) == wr[u].res) && q < p;       // V = p + c*q, c odd: the triangle
            int kii = EXTRA && wr[p].res == wr[u].res;                         // V = p + c*q, c even, p a second wire with u's residue
            if (!tri && !kii) continue;
            if (wr[u].pb != P || wr[p].pb != P || wr[q].pb != P) continue;
            for (int c = 1; c < (1 << P); c++) {
                if ((c & 1) && !tri) continue;
                if (!(c & 1) && !kii) continue;
                uint32_t V = canon(comb(wr[p].val, c, wr[q].val, P), P);
                if (V == wr[u].val) continue;
                for (int s = 1; s < (1 << P); s += 2) {
                    uint32_t d = comb(wr[u].val, (1 << P) - s, V, P);
                    int e = 99; for (int i = 0; i < n; i++) { int x = ent(d, i); if (x) { int z = __builtin_ctz(x); if (z < e) e = z; } }
                    if (e == 99 || e < 1 || P - e < 2) continue;
                    uint32_t H = 0; for (int i = 0; i < n; i++) H |= (uint32_t)(ent(d, i) >> e) << (4 * i);
                    H = canon(H, P - e);
                    ntri++; nresH[res2(H)]++;
                    { int own = (wr[u].kind && ((wr[u].a == p && wr[u].b == q) || (wr[u].a == q && wr[u].b == p))) || (wr[p].kind && ((wr[p].a == u && wr[p].b == q) || (wr[p].a == q && wr[p].b == u))) || (wr[q].kind && ((wr[q].a == u && wr[q].b == p) || (wr[q].a == p && wr[q].b == u)));
                      if (!own) { nacc++; int isold = 0; for (int z = 0; z < nw; z++) if (wr[z].res == res2(H)) isold = 1; if (!isold) naccnew++; } }
                    if (res2(H) != Wres) continue;
                    nmacro++;
                    int offrow = 0;
                    if (slotT[Wres]) { int ti = tindex(Wres); if (H != rowval(ti, P - e)) { if (EXTRA && !haveX) offrow = 1; else continue; } }
                    Wire wv = {wr[u].res, V, P, 3, p, q, c, 0, 0, 0}; Wire wh = {Wres, H, P - e, 4, u, nw, 0, u, s, e};
                    PUSH(3 + 4 * offrow, wr[u].res, V, H, P - e, wv, wh);
                }
            }
        }
        // (2) the slots of S
        for (int a = 0; a < nw; a++) for (int b = 0; b < a; b++) {
            int c0 = wr[a].res ^ wr[b].res;
            if (!slotS[c0] || filled[c0]) continue;
            int pb = wr[a].pb < wr[b].pb ? wr[a].pb : wr[b].pb;
            for (int c = 1; c < (1 << pb); c += 2) {
                uint32_t w = canon(comb(wr[a].val, c, wr[b].val, pb), pb);
                Wire w1 = {c0, w, pb, 1, a, b, c, 0, 0, 0};
                PUSH(1, c0, w, 0, pb, w1, w1);
            }
        }
        // (3) one extra wire of any residue
        if (EXTRA && !haveX) for (int a = 0; a < nw; a++) for (int b = 0; b < nw; b++) {
            if (a == b) continue;
            int pb = wr[a].pb < wr[b].pb ? wr[a].pb : wr[b].pb;
            for (int c = 1; c < (1 << pb); c++) {
                if (!(c & 1) && b > a && 0) continue;
                if ((c & 1) && b > a) continue;                    // odd c: unordered pair; even c: a + c*b ordered
                uint32_t w0 = comb(wr[a].val, c, wr[b].val, pb); int r = res2(w0); if (!r) continue;
                uint32_t w = canon(w0, pb);
                int same = 0; for (int k = 0; k < nw; k++) if (wr[k].res == r && wr[k].val == w && wr[k].pb >= pb) same = 1;
                if (same) continue;
                Wire w1 = {r, w, pb, 5, a, b, c, 0, 0, 0};
                PUSH(5, r, w, 0, pb, w1, w1);
            }
        }
        for (int k = 0; k < nc && !ok && !capped; k++) {
            int save = nw;
            if (cd[k].kind == 3) { wr[nw++] = cwv[2 * k]; Wire h = cwv[2 * k + 1]; h.b = nw - 1; wr[nw++] = h; haveV = 1; haveH = 1; if (slotT[Wres] || slotS[Wres]) filled[Wres] = 1; }
            else if (cd[k].kind == 7) { wr[nw++] = cwv[2 * k]; Wire h = cwv[2 * k + 1]; h.b = nw - 1; wr[nw++] = h; haveV = 1; haveH = 1; haveX = 1; }
            else if (cd[k].kind == 1) { wr[nw++] = cwv[2 * k]; filled[cd[k].slot] = 1; }
            else { wr[nw++] = cwv[2 * k]; haveX = 1; }
            ok = dfs();
            if (!ok) {
                nw = save;
                if (cd[k].kind == 3) { haveV = 0; haveH = 0; if (slotT[Wres] || slotS[Wres]) filled[Wres] = 0; }
                else if (cd[k].kind == 7) { haveV = 0; haveH = 0; haveX = 0; }
                else if (cd[k].kind == 1) filled[cd[k].slot] = 0; else haveX = 0;
                if (nforb < 20000) forb[nforb++] = cd[k];
            }
        }
        free(cd); free(cwv);
        if (!ok) nforb = f0;
    }
    if (!ok) { for (int k = 0; k < ad; k++) { nw--; filled[wr[nw].res] = 0; } }
    return ok;
}
static void pv(uint32_t v) { for (int i = 0; i < n; i++) printf("%d%s", ent(v, i), i + 1 < n ? "," : ""); }
int main(int argc, char **argv) {
    P = atoi(argv[1]); if (argc > 3) EXTRA = atoi(argv[3]); if (argc > 4) nodecap = atoll(argv[4]);
    for (int a = 1; a < 16; a += 2) for (int b = 1; b < 16; b += 2) if (a * b % 16 == 1) inv16[a] = b;
    FILE *f = fopen(argv[2], "r"); int v, k = 0, code = 0;
    while (fscanf(f, "%d", &v) == 1) { Trow[nT][k] = v; code = (code << 1) | (v & 1); if (++k == n) { Tcode[nT++] = code; k = 0; code = 0; } }
    fclose(f);
    static char line[4096]; long long nsets = 0, nlift = 0, totnodes = 0, ncapped = 0; long long hist[17] = {0};
    while (fgets(line, sizeof line, stdin)) {
        int s[32], m = 0; char *p = line, *e;
        while (m < 32) { long x = strtol(p, &e, 10); if (e == p) break; s[m++] = (int)x; p = e; }
        if (m < 1) continue;
        memset(slotS, 0, sizeof slotS); memset(slotT, 0, sizeof slotT); memset(filled, 0, sizeof filled);
        nw = 0; nforb = 0; best = -1; nodes = 0; capped = 0; haveV = haveH = haveX = 0; Wres = s[0];
        for (int t = 0; t < nT; t++) slotT[Tcode[t]] = 1;
        for (int q = 1; q < m; q++) slotS[s[q]] = 1;
        for (int q = 0; q < n; q++) { int c0 = 1 << (n - 1 - q); wr[nw] = (Wire){c0, 1u << (4 * q), P, 0, 0, 0, 0, 0, 0, 0}; nw++; filled[c0] = 1; }
        int ok = dfs(); nsets++; totnodes += nodes; if (nsets % 100 == 0) { printf("PROGRESS %lld sets done, %lld lifted, halvings with residue w so far %lld\n", nsets, nlift, nmacro); fflush(stdout); } if (best >= 0) hist[best]++; if (capped) ncapped++;
        if (ok) {
            nlift++;
            if (nlift <= 20) {
                printf("LIFT w=%d set", Wres); for (int q = 1; q < m; q++) printf(" %d", s[q]); printf(" : %d gates\n", nsol - n);
                for (int i = n; i < nsol; i++) { Wire *w = &solw[i]; const char *kn[] = {"in", "S", "TARGET", "V(wasted)", "H(halving)", "extra"};
                    printf("   #%d %s res=%d pb=%d [", i, kn[w->kind], w->res, w->pb); pv(w->val); printf("] = ");
                    if (w->kind == 4) printf("(#%d - %d*#%d)/2^%d\n", w->u, w->s, w->b, w->e); else printf("#%d + %d*#%d\n", w->a, w->c, w->b); }
            }
        } else if (VERB) { printf("no lift w=%d best %d\n", Wres, best); }
        fflush(stdout);
    }
    printf("RESULT P=%d (wires modulo %d before the halving) extra=%d: %lld of %lld sets lift; nodes %lld; sets stopped at the node cap: %lld\n", P, 1 << P, EXTRA, nlift, nsets, totnodes, ncapped);
    printf("  halvings examined (u, p, q, c, s with a primitive half): %lld ; of them with the residue w: %lld\n", ntri, nmacro);
    if (getenv("RESH")) { printf("  residues of the halves seen (code:count):"); for (int r = 0; r < 256; r++) if (nresH[r]) printf(" %d:%lld", r, nresH[r]); printf("\n"); }
    printf("  of the halvings examined, on a triple where no wire is the gate of the other two: %lld ; of those, with a residue no wire has yet: %lld\n", nacc, naccnew);
    printf("  histogram of the most targets reached: "); for (int t = 0; t <= nT; t++) if (hist[t]) printf(" %d targets: %lld sets;", t, hist[t]); printf("\n");
    return 0;
}
