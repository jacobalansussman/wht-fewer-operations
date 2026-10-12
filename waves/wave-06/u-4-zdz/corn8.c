/* u-4-zdz / corn8.c : exact least number of corners of an 8 x 8 matrix over ALL orders of the rows and of the columns,
   plain (signs=0) or with every row free to be multiplied by -1 (signs=1).
   corners = non-zeros of the second difference M[a][b] = A[a][b]-A[a+1][b]-A[a][b+1]+A[a+1][b+1], one zero row and one zero
   column added after the last (the convention of q-cross/zreplay.py).  Two-chain program: N - 2 + corners gates (G).
   For a fixed column order the count is a sum over neighbouring rows, so the best row order is a shortest path through the
   rows (dynamic programme over subsets); the column orders are enumerated (8! = 40320).  Integers only.
   input: 64 integers (the matrix, row by row).  usage: corn8 signs < matrix */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 8
int A[N][N], B[2*N+1][N+1], w[2*N+1][2*N+1], f[1<<N][2*N];
int main(int argc, char **argv) {
    int signs = argc > 1 ? atoi(argv[1]) : 0, p[N], best = 1 << 30, bp[N], hist[200]; long cnt = 0;
    memset(hist, 0, sizeof hist);
    for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) if (scanf("%d", &A[i][j]) != 1) return 1;
    for (int i = 0; i < N; i++) p[i] = i;
    int R = signs ? 2 * N : N;                      /* signed rows: r and N + r (= minus row r); index R = the zero row */
    for (;;) {
        for (int r = 0; r < N; r++) for (int b = 0; b < N; b++) { B[r][b] = A[r][p[b]]; B[N + r][b] = -A[r][p[b]]; }
        for (int r = 0; r < 2 * N; r++) B[r][N] = 0;
        for (int b = 0; b <= N; b++) B[2 * N][b] = 0;
        for (int u = 0; u < R; u++) for (int v = 0; v <= R; v++) {
            int vv = v == R ? 2 * N : v, c = 0;
            for (int b = 0; b < N; b++) if (B[u][b] - B[vv][b] != B[u][b + 1] - B[vv][b + 1]) c++;
            w[u][v] = c;
        }
        for (int m = 0; m < (1 << N); m++) for (int l = 0; l < R; l++) f[m][l] = 1 << 29;
        for (int l = 0; l < N; l++) f[1 << l][l] = 0;          /* first row with sign + (a global sign changes nothing) */
        for (int m = 1; m < (1 << N); m++) for (int l = 0; l < R; l++) {
            int cur = f[m][l]; if (cur >= (1 << 29)) continue;
            for (int t = 0; t < R; t++) { int tr = t % N; if (m >> tr & 1) continue;
                int nm = m | 1 << tr, val = cur + w[l][t]; if (val < f[nm][t]) f[nm][t] = val; }
        }
        int loc = 1 << 30;
        for (int l = 0; l < R; l++) { int val = f[(1 << N) - 1][l] + w[l][R]; if (val < loc) loc = val; }
        if (loc < 200) hist[loc]++;
        if (loc < best) { best = loc; memcpy(bp, p, sizeof p); }
        cnt++;
        int i = N - 2; while (i >= 0 && p[i] > p[i + 1]) i--;
        if (i < 0) break;
        int j = N - 1; while (p[j] < p[i]) j--;
        int t = p[i]; p[i] = p[j]; p[j] = t;
        for (int a = i + 1, b = N - 1; a < b; a++, b--) { t = p[a]; p[a] = p[b]; p[b] = t; }
    }
    printf("signs=%d column orders=%ld least corners=%d (gates %d) best column order:", signs, cnt, best, N - 2 + best);
    for (int i = 0; i < N; i++) printf(" %d", bp[i]);
    printf("  | column orders by their best count:");
    for (int c = 0; c < 200; c++) if (hist[c]) printf(" %d:%d", c, hist[c]);
    printf("\n");
    return 0;
}
