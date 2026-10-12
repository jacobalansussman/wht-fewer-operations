// u-6-twotrees / twotrees16.c : the shift game at 16 points with SEVERAL merge trees.  Count (G).  Exact whole-number bookkeeping only.
// Adapted from h-6-classhub/onecentre16.c.
// A vertex is a full sign vector s (a set of addresses where the sign is -1, up to complement = global sign).
// A move flips s on one node A of one of the trees (or on one single address).  In AGREE mode the flip on a node A of tree t is
// allowed only if s equals the centre C_t of that tree on A, up to one sign (the held tree wire on A is C_t restricted to A).
// In FREE mode every node may always be flipped (this is not a circuit: it is the count of the sketch).
// Trees: tree t is the cube tree carried by an invertible 4 x 4 bit matrix M_t given by its 4 rows r1..r4 (as masks of the address
// bits): level-i nodes are the sets where (r1.x, ..., ri.x) is fixed, i = 1, 2, 3.  A bit order (b1,b2,b3,b4) is rows 1<<(b-1).
// Terminals: the 16 outputs (up to sign) and the centres that are declared hubs.
// Output: weight of a minimum spanning tree (MST) of the terminals in the true graph distance = an UPPER bound on the shifts;
// ceil(MST/2) = a LOWER bound for these centres (Steiner ratio 2); and the MST after greedily adding extra vertices.
// usage: twotrees16 <agree 0/1> <rounds> <ntrees> then per tree: r1 r2 r3 r4 centreMask hubFlag
//        twotrees16 scan <ntrees=2> r1..r4 r1..r4 <sameCentre 0/1> <linear 0/1> : all quadratic centres (x linear parts for tree 2)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define NV 32768
#define MAXT 70
static int nm; static unsigned short mvA[400], mvP[400]; static unsigned char mvFree[400];
static int dist[MAXT][NV]; static unsigned short q[NV];
static int agree = 1;
static inline unsigned canon(unsigned D) { return (D & 1) ? (D ^ 0xFFFF) : D; }
static inline int par(unsigned v) { return __builtin_popcount(v) & 1; }
static void bfs(unsigned src, int *d) {
    for (int i = 0; i < NV; i++) d[i] = -1;
    int h = 0, t = 0; d[src >> 1] = 0; q[t++] = src >> 1;
    while (h < t) {
        unsigned D = (unsigned)q[h++] << 1; int dd = d[D >> 1] + 1;
        for (int m = 0; m < nm; m++) {
            unsigned A = mvA[m];
            if (agree && !mvFree[m]) { unsigned z = (D ^ mvP[m]) & A; if (z != 0 && z != A) continue; }
            unsigned E = canon(D ^ A); if (d[E >> 1] < 0) { d[E >> 1] = dd; q[t++] = E >> 1; }
        }
    }
}
static int prim(int n, unsigned *vs, int extra) {
    int in[MAXT + 2], key[MAXT + 2]; int m = n + (extra >= 0); int w = 0;
    for (int i = 0; i < m; i++) { in[i] = 0; key[i] = 1 << 28; }
    key[0] = 0;
    for (int it = 0; it < m; it++) {
        int b = -1; for (int i = 0; i < m; i++) if (!in[i] && (b < 0 || key[i] < key[b])) b = i;
        in[b] = 1; w += key[b];
        for (int i = 0; i < m; i++) if (!in[i]) {
            int dd;
            if (b < n) dd = (i < n) ? dist[b][vs[i] >> 1] : dist[b][extra];
            else dd = dist[i][extra];
            if (dd < 0) dd = 1 << 20;
            if (dd < key[i]) key[i] = dd;
        }
    }
    return w;
}
static int addtree(int *r, unsigned centre, int *nodes_out) {          // returns number of node moves added
    int cnt = 0;
    for (int lev = 1; lev <= 3; lev++) for (int a = 0; a < (1 << lev); a++) {
        unsigned A = 0;
        for (int x = 0; x < 16; x++) { int ok = 1; for (int j = 0; j < lev; j++) if (par(r[j] & x) != ((a >> j) & 1)) ok = 0; if (ok) A |= 1u << x; }
        mvA[nm] = A; mvP[nm] = centre; mvFree[nm] = 0; nm++; cnt++;
        if (nodes_out) nodes_out[cnt - 1] = A;
    }
    return cnt;
}
static unsigned quad(int code, int lin) {                               // bit x set <=> (-1)^(Q(x)+lin.x) = -1
    static const int mono[6] = {3, 5, 6, 9, 10, 12}; unsigned F = 0;
    for (int x = 0; x < 16; x++) { int g = par(lin & x); for (int i = 0; i < 6; i++) if ((code >> i & 1) && (x & mono[i]) == mono[i]) g ^= 1; if (g) F |= 1u << x; }
    return F;
}
static int run(int ntrees, int R[][4], unsigned *C, int *hub, int rounds, int verbose, int *w0out, int *distinct) {
    nm = 0;
    for (int p = 0; p < 16; p++) { mvA[nm] = 1u << p; mvP[nm] = 0; mvFree[nm] = 1; nm++; }
    unsigned short seen[200]; int ns = 0;
    for (int t = 0; t < ntrees; t++) addtree(R[t], C[t], NULL);
    // count distinct held tree wires (node, pattern up to sign): a node shared by two trees with the same pattern is one wire
    int held = 0;
    for (int m = 16; m < nm; m++) { int dup = 0; for (int m2 = 16; m2 < m; m2++) if (mvA[m2] == mvA[m]) { unsigned z = (mvP[m] ^ mvP[m2]) & mvA[m]; if (z == 0 || z == mvA[m]) dup = 1; } if (!dup) held++; }
    (void)seen; (void)ns;
    unsigned vs[MAXT]; int n = 0;
    for (int t = 0; t < ntrees; t++) if (hub[t]) { unsigned D = canon(C[t]); int dup = 0; for (int i = 0; i < n; i++) if (vs[i] == D) dup = 1; if (!dup) vs[n++] = D; }
    int nh = n;
    for (int j = 0; j < 16; j++) { unsigned Cj = 0; for (int x = 0; x < 16; x++) if (par(j & x)) Cj |= 1u << x; unsigned D = canon(Cj); int dup = 0; for (int i = 0; i < n; i++) if (vs[i] == D) dup = 1; if (!dup) vs[n++] = D; }
    int nt = n;
    for (int i = 0; i < n; i++) bfs(vs[i], dist[i]);
    int w0 = prim(n, vs, -1), w = w0;
    for (int r = 0; r < rounds && n < MAXT - 1; r++) {
        int bw = w, bv = -1;
        for (int v = 0; v < NV; v++) { int ww = prim(n, vs, v); if (ww < bw) { bw = ww; bv = v; } }
        if (bv < 0) break;
        vs[n] = (unsigned)bv << 1; bfs(vs[n], dist[n]); n++; w = bw;
    }
    *w0out = w0; *distinct = held;
    if (verbose) {
        printf("  held tree wires (node, pattern) other than singles: %d ; hubs as terminals: %d ; terminals: %d\n", held, nh, nt);
        printf("  MST of terminals: %d shifts (lower bound for these centres: %d) ; with %d extra vertices: %d shifts\n", w0, (w0 + 1) / 2, n - nt, w);
        printf("  distances hub0 -> outputs:"); for (int i = nh; i < nt; i++) printf(" %d", dist[0][vs[i] >> 1]); printf("\n");
        printf("  distances output0 -> outputs:"); for (int i = nh; i < nt; i++) printf(" %d", dist[nh][vs[i] >> 1]); printf("\n");
    }
    return w;
}
int main(int argc, char **argv) {
    int R[4][4]; unsigned C[4]; int hub[4];
    if (!strcmp(argv[1], "mask")) { printf("%u\n", quad(atoi(argv[2]), atoi(argv[3]))); return 0; }
    if (!strcmp(argv[1], "scan")) {
        // scan <rounds> <r1..r4 tree1> <r1..r4 tree2> <mode>   mode 0: G0 = F0 ; 1: G0 any quadratic ; 2: G0 any quadratic + linear part ; 3: one tree only
        int rounds = atoi(argv[2]); for (int t = 0; t < 2; t++) for (int j = 0; j < 4; j++) R[t][j] = atoi(argv[3 + 4 * t + j]);
        int mode = atoi(argv[11]); int hub2 = argc > 12 ? atoi(argv[12]) : 0;
        int best = 1 << 28, bestw0 = 1 << 28; long hist[400]; memset(hist, 0, sizeof hist);
        for (int c1 = 0; c1 < 64; c1++) {
            int n2 = (mode == 0 || mode == 3) ? 1 : 64, nl = (mode == 2) ? 16 : 1;
            for (int c2i = 0; c2i < n2; c2i++) for (int l = 0; l < nl; l++) {
                int c2 = (mode == 0 || mode == 3) ? c1 : c2i;
                C[0] = quad(c1, 0); C[1] = quad(c2, l); hub[0] = 1; hub[1] = hub2;
                int w0, held; int w = run(mode == 3 ? 1 : 2, R, C, hub, rounds, 0, &w0, &held);
                int same = (canon(C[0]) == canon(C[1]));
                int total = 15 + (held - 14) + ((hub2 && !same && mode != 3) ? 1 : 0) + w;       // 15 = the first centre with its tree
                hist[total]++;
                if (total < best || w0 < bestw0) { if (total < best) best = total; if (w0 < bestw0) bestw0 = w0;
                    printf("F0 quad %d  G0 quad %d lin %d | held %d | MST %d (lb %d) | after %d rounds %d shifts | GATES <= %d\n", c1, c2, l, held, w0, (w0 + 1) / 2, rounds, w, total); fflush(stdout); }
            }
        }
        printf("histogram of the upper bound:"); for (int g = 0; g < 400; g++) if (hist[g]) printf(" %d:%ld", g, hist[g]);
        printf("\nBEST upper bound: %d gates ; least MST of terminals: %d\n", best, bestw0);
        return 0;
    }
    agree = atoi(argv[1]); int rounds = atoi(argv[2]); int nt = atoi(argv[3]);
    for (int t = 0; t < nt; t++) { for (int j = 0; j < 4; j++) R[t][j] = atoi(argv[4 + 6 * t + j]); C[t] = (unsigned)atoi(argv[4 + 6 * t + 4]); hub[t] = atoi(argv[4 + 6 * t + 5]); }
    int w0, held; int w = run(nt, R, C, hub, rounds, 1, &w0, &held);
    printf("  shifts <= %d ; held tree wires %d\n", w, held);
    return 0;
}
