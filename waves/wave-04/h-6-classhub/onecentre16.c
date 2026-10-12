// h-6-classhub / onecentre16.c : g-1's "one merge tree + flip walk" model at 16 points (tau = -1, count (G)), with a better tree heuristic.
// Model [read, g-1.md / exact8.py]: a sign vector F0 (the centre, 15 gates), tree nodes = cosets of V1 < V2 < V3 (pairs, fours, eights);
// a vertex is the set D where the current sign vector differs from F0 (D ~ complement); one gate toggles one point, or a tree node
// lying wholly inside or wholly outside D.  Gates = 15 + (edges of a tree in this graph containing the empty set and the 16 targets).
// Here: UPPER bound by a minimum spanning tree in the graph metric over {empty, targets} plus greedily added Steiner vertices.
// Also prints MST/2 rounded up, which is a LOWER bound for the model with that centre (Steiner ratio 2).
// usage: onecentre16 mode rounds     mode 0: the 64 quadratic centres; mode 1: all 2048 centres of degree <= 4 without linear part
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define NV 32768
static unsigned short nodes[14]; static int dist[64][NV]; static unsigned short q[NV];
static inline unsigned canon(unsigned D) { return (D & 1) ? (D ^ 0xFFFF) : D; }
static void bfs(unsigned src, int *d) {
    for (int i = 0; i < NV; i++) d[i] = -1;
    int h = 0, t = 0; d[src >> 1] = 0; q[t++] = src >> 1;
    while (h < t) {
        unsigned D = (unsigned)q[h++] << 1; int dd = d[D >> 1] + 1;
        for (int p = 0; p < 16; p++) { unsigned E = canon(D ^ (1u << p)); if (d[E >> 1] < 0) { d[E >> 1] = dd; q[t++] = E >> 1; } }
        for (int a = 0; a < 14; a++) { unsigned A = nodes[a]; if ((D & A) == 0 || (D & A) == A) { unsigned E = canon(D ^ A); if (d[E >> 1] < 0) { d[E >> 1] = dd; q[t++] = E >> 1; } } }
    }
}
static int prim(int n, unsigned *vs, int extra /* vertex id or -1 */) {
    int in[80], key[80]; int m = n + (extra >= 0); int w = 0;
    for (int i = 0; i < m; i++) { in[i] = 0; key[i] = 1 << 30; }
    key[0] = 0;
    for (int it = 0; it < m; it++) {
        int b = -1; for (int i = 0; i < m; i++) if (!in[i] && (b < 0 || key[i] < key[b])) b = i;
        in[b] = 1; w += key[b];
        for (int i = 0; i < m; i++) if (!in[i]) {
            int dd;
            if (b < n) dd = (i < n) ? dist[b][vs[i] >> 1] : dist[b][extra];
            else dd = dist[i][extra];
            if (dd < key[i]) key[i] = dd;
        }
    }
    return w;
}
int main(int argc, char **argv) {
    int mode = atoi(argv[1]), rounds = atoi(argv[2]);
    for (int i = 0; i < 8; i++) nodes[i] = 3u << (2 * i);
    for (int i = 0; i < 4; i++) nodes[8 + i] = 0xFu << (4 * i);
    nodes[12] = 0xFF; nodes[13] = 0xFF00;
    int mono[11], nm = 0;
    for (int m = 1; m < 16; m++) { int pc = __builtin_popcount(m); if (pc >= 2 && (mode == 1 || pc == 2)) mono[nm++] = m; }
    int best = 1 << 30; int hist[200]; memset(hist, 0, sizeof hist);
    for (int code = 0; code < (1 << nm); code++) {
        unsigned F = 0;                                   // bit x set <=> F0(x) = -1
        for (int x = 0; x < 16; x++) { int g = 0; for (int i = 0; i < nm; i++) if ((code >> i & 1) && (x & mono[i]) == mono[i]) g ^= 1; if (g) F |= 1u << x; }
        unsigned vs[80]; int n = 0; vs[n++] = 0;
        for (int j = 0; j < 16; j++) {
            unsigned C = 0; for (int x = 0; x < 16; x++) if (__builtin_popcount(j & x) & 1) C |= 1u << x;
            unsigned D = canon(C ^ F); int dup = 0; for (int i = 0; i < n; i++) if (vs[i] == D) dup = 1;
            if (!dup) vs[n++] = D;
        }
        int nt = n;
        for (int i = 0; i < n; i++) bfs(vs[i], dist[i]);
        int w0 = prim(n, vs, -1), w = w0;
        for (int r = 0; r < rounds && n < 60; r++) {
            int bw = w, bv = -1;
            for (int v = 0; v < NV; v++) { int ww = prim(n, vs, v); if (ww < bw) { bw = ww; bv = v; } }
            if (bv < 0) break;
            vs[n] = (unsigned)bv << 1; bfs(vs[n], dist[n]); n++; w = bw;
        }
        hist[15 + w]++;
        if (15 + w < best || code == 0) {
            if (15 + w < best) best = 15 + w;
            printf("centre code %d (monomials", code); for (int i = 0; i < nm; i++) if (code >> i & 1) printf(" %d", mono[i]);
            printf(") F0mask %u | distinct non-input targets %d | MST of targets %d (lower bound for this centre: 15 + %d) | with %d Steiner vertices: %d | GATES <= %d\n  vertices:", F, nt - 1, w0, (w0 + 1) / 2, n - nt, w, 15 + w);
            for (int i = 0; i < n; i++) printf(" %u", vs[i]); printf("\n"); fflush(stdout);
        }
    }
    printf("histogram of the upper bound over %d centres:", 1 << nm); for (int g = 0; g < 200; g++) if (hist[g]) printf(" %d:%d", g, hist[g]); printf("\nBEST upper bound in this model and heuristic: %d gates (record 52, textbook 64)\n", best);
    return 0;
}
