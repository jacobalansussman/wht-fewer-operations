// search.c (g-0-mirror): reduced model of the 16-point mirror.  Points: 16 targets (0..15), 30 roots (16..45).
// Collinear triples: (target, target, root) for the 120 secants, and the 80 collinear root triples.
// For every set X of x roots: is W = targets + X generated from some 6 of its points by the rule
// "a point on a line through two present points may be added"?  If yes, the mirror basis costs 10 + (10 + x) gates (count G).
// usage: search x [maxprint]
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int nR, nRT; static int rootv[30][6]; static int sec[30][4][2]; static int rt[80][3];
static uint64_t trip[200]; static int nTrip;
static inline int pc(uint64_t x) { return __builtin_popcountll(x); }
int main(int argc, char **argv) {
    int x = atoi(argv[1]); int maxprint = argc > 2 ? atoi(argv[2]) : 5;
    FILE *f = fopen("tables.txt", "r"); if (!f) return 2;
    fscanf(f, "%d %d", &nR, &nRT);
    for (int r = 0; r < nR; r++) { for (int k = 0; k < 6; k++) fscanf(f, "%d", &rootv[r][k]); for (int k = 0; k < 4; k++) fscanf(f, "%d %d", &sec[r][k][0], &sec[r][k][1]); }
    for (int i = 0; i < nRT; i++) fscanf(f, "%d %d %d", &rt[i][0], &rt[i][1], &rt[i][2]);
    fclose(f);
    for (int r = 0; r < nR; r++) for (int k = 0; k < 4; k++) trip[nTrip++] = (1ull << sec[r][k][0]) | (1ull << sec[r][k][1]) | (1ull << (16 + r));
    for (int i = 0; i < nRT; i++) trip[nTrip++] = (1ull << (16 + rt[i][0])) | (1ull << (16 + rt[i][1])) | (1ull << (16 + rt[i][2]));
    long long nX = 0, nFeas = 0; int printed = 0;
    int idx[8]; for (int i = 0; i < x; i++) idx[i] = i;
    while (1) {
        uint64_t W = 0xFFFFull; for (int i = 0; i < x; i++) W |= 1ull << (16 + idx[i]);
        // compress W to bits 0..15+x
        int pos[46]; int np = 0; for (int b = 0; b < 46; b++) if (W >> b & 1) pos[b] = np++; else pos[b] = -1;
        uint32_t tm[64]; int nt = 0;
        for (int i = 0; i < nTrip; i++) if ((trip[i] & W) == trip[i]) { uint32_t m = 0; for (int b = 0; b < 46; b++) if (trip[i] >> b & 1) m |= 1u << pos[b]; tm[nt++] = m; }
        uint32_t full = (np == 32) ? 0xFFFFFFFFu : ((1u << np) - 1);
        uint32_t covered = 0; for (int i = 0; i < nt; i++) covered |= tm[i];
        uint32_t must = full & ~covered;       // points in no triple must be in the basis
        nX++; int feas = 0;
        if (nt >= np - 6 && pc(must) <= 6) {
            uint32_t B = (1u << 6) - 1;
            while (B < (1u << np)) {
                if ((B & must) == must) {
                    uint32_t Sx = B; int ch = 1;
                    while (ch) { ch = 0; for (int i = 0; i < nt; i++) if (pc(Sx & tm[i]) == 2) { Sx |= tm[i]; ch = 1; } }
                    if (Sx == full) {
                        feas = 1;
                        if (printed < maxprint) {
                            printed++;
                            printf("FOUND x=%d roots:", x); for (int i = 0; i < x; i++) { printf(" ["); for (int k = 0; k < 6; k++) printf("%d%s", rootv[idx[i]][k], k < 5 ? "," : ""); printf("]"); }
                            printf("  basis points:"); for (int b = 0; b < 46; b++) if (pos[b] >= 0 && (B >> pos[b] & 1)) { if (b < 16) printf(" t%d", b); else printf(" r%d", b - 16); }
                            printf("\n");
                        }
                        break;
                    }
                }
                uint32_t c = B & -B, r2 = B + c; B = (((r2 ^ B) >> 2) / c) | r2;
            }
        }
        nFeas += feas;
        int k = x - 1; while (k >= 0 && idx[k] == nR - x + k) k--;
        if (k < 0) break;
        idx[k]++; for (int j = k + 1; j < x; j++) idx[j] = idx[j - 1] + 1;
    }
    printf("RESULT x=%d: %lld sets of roots tried, %lld generate all 16 targets from 6 points  => gates for C^T = %d, for C = %d\n", x, nX, nFeas, 10 + x, 20 + x);
    return 0;
}
