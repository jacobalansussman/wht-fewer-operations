// flat3.c (ab-0): can the indicator of E = {0, e_1, .., e_6} in F_2^6 (seven affinely independent points: neighbour sums
// at k = 7 seen inside the odd-weight hyperplane) be a combination of THREE signed flats?  Necessary conditions on the
// three supports S1, S2, S3 (any non-zero coefficients, any sign patterns): (a) E is covered; (b) a point covered by
// exactly one flat lies in E.  This program lists every triple of supports that passes (a) and (b), exhaustively.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint64_t u64;
static const u64 A[6] = {0x5555555555555555ull, 0x3333333333333333ull, 0x0F0F0F0F0F0F0F0Full, 0x00FF00FF00FF00FFull, 0x0000FFFF0000FFFFull, 0x00000000FFFFFFFFull};
static inline u64 tr(u64 m, int v) { for (int t = 0; t < 6; t++) if (v >> t & 1) m = ((m & A[t]) << (1 << t)) | ((m >> (1 << t)) & A[t]); return m; }
static u64 hull(u64 M) {
    int b = __builtin_ctzll(M); u64 W = 1, R = M;
    while (R) { int x = __builtin_ctzll(R); R &= R - 1; int v = x ^ b; if (!(W >> v & 1)) W |= tr(W, v); }
    return tr(W, b);
}
int main(int argc, char **argv) {
    static u64 F[40000]; static int D[40000]; int nF = 0; FILE *f = fopen(argv[1], "r");
    unsigned long long m; int d; while (fscanf(f, "%d %llu", &d, &m) == 2) { D[nF] = d; F[nF++] = m; }
    int ne = argc > 2 ? atoi(argv[2]) : 6; u64 E = 1; for (int j = 0; j < ne; j++) E |= 1ull << (1 << j);   /* E = {0, e_1..e_ne} */
    unsigned long long pairs = 0, hullok = 0, triples = 0;
    for (int i = 0; i < nF; i++) for (int j = i + 1; j < nF; j++) {
        u64 S1 = F[i], S2 = F[j], U = S1 | S2; pairs++;
        u64 Must = ((S1 ^ S2) & ~E) | (E & ~U), May = U | E;
        if (Must) { u64 H = hull(Must); if (H & ~May) continue; }
        hullok++;
        for (int l = j + 1; l < nF; l++) {
            u64 S3 = F[l];
            if (S3 & ~May) continue; if (Must & ~S3) continue;
            u64 once = (S1 ^ S2 ^ S3) & ~(S1 & S2 & S3);
            if (once & ~E) continue; if (E & ~(U | S3)) continue;
            triples++;
            printf("T %d %d %d  %llu %llu %llu\n", D[i], D[j], D[l], (unsigned long long)S1, (unsigned long long)S2, (unsigned long long)S3);
        }
    }
    printf("flats %d pairs %llu pairs passing the hull test %llu support triples %llu\n", nF, pairs, hullok, triples);
    return 0;
}
