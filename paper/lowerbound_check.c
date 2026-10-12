/* lowerbound_check.c -- an exhaustive check of Steps 4 and 5 of the proof of the lower bound 2N - 1
   (Proposition "lower bound" of explicit-wht-circuits.tex) at N = 4 and N = 8.

   Steps 1 to 3 of the proof show: a circuit with 2N - 2 lines would consist of a tree that merges the N inputs
   into one value, which is a multiple of a row a of H (so every value of the tree is row a restricted to the
   inputs below it), followed by N - 1 lines that are the other N - 1 rows, each made in ONE line a*u + b*v from
   values already there.  This program takes every tree (every way to split the set of inputs into two parts,
   each part again, down to single inputs) and every row a, and computes how many rows can be reached that way:
   it keeps adding any row that lies in the span of two values already held, until nothing more can be added.
   The proof says: at most 2 rows in all (row a and one more).  A circuit with 2N - 2 lines would need all N.

   Exact integer arithmetic.  cc -O2 -o lowerbound_check lowerbound_check.c ; ./lowerbound_check          */
#include <stdio.h>
#include <string.h>

static int N;
static int rows[16][16];
static long long ntrees, hist[17];
static int masks[64], nm;

static int inspan(const int *u, const int *v, const int *r) {      /* is r in the span of u and v ? */
    int i, j, k;
    for (i = 0; i < N; i++) for (j = i + 1; j < N; j++) {
        int det = u[i] * v[j] - u[j] * v[i];
        if (det) {
            int a = r[i] * v[j] - r[j] * v[i], b = u[i] * r[j] - u[j] * r[i];
            for (k = 0; k < N; k++) if (det * r[k] != a * u[k] + b * v[k]) return 0;
            return 1;
        }
    }
    /* u and v are parallel, or one of them is zero: r must be parallel to the one that is not zero */
    const int *w = u; int nz = 0;
    for (k = 0; k < N; k++) if (u[k]) nz = 1;
    if (!nz) w = v;
    nz = 0; for (k = 0; k < N; k++) if (w[k]) nz = 1;
    if (!nz) return 0;
    for (i = 0; i < N; i++) for (j = i + 1; j < N; j++) if (w[i] * r[j] - w[j] * r[i]) return 0;
    return 1;
}

static void evaluate(void) {
    int a, b, k, p, q, t;
    int full = (1 << N) - 1;
    ntrees++;
    for (a = 0; a < N; a++) {
        int W[48][16], nw = 0, have[16], cnt = 1, changed = 1;
        for (t = 0; t < nm; t++) {
            if (masks[t] == full) continue;
            for (k = 0; k < N; k++) W[nw][k] = ((masks[t] >> k) & 1) ? rows[a][k] : 0;
            nw++;
        }
        for (k = 0; k < N; k++) W[nw][k] = rows[a][k];               /* the root */
        nw++;
        memset(have, 0, sizeof have); have[a] = 1;
        while (changed) {
            changed = 0;
            for (b = 0; b < N; b++) if (!have[b]) {
                int found = 0;
                for (p = 0; p < nw && !found; p++) for (q = p + 1; q < nw && !found; q++)
                    if (inspan(W[p], W[q], rows[b])) found = 1;
                if (found) {
                    have[b] = 1; cnt++; changed = 1;
                    for (k = 0; k < N; k++) W[nw][k] = rows[b][k];
                    nw++;
                }
            }
        }
        hist[cnt]++;
    }
}

static void rec(const int *pending, int np) {
    int newp[32], T, i, n;
    if (np == 0) { evaluate(); return; }
    int S = pending[np - 1];
    masks[nm++] = S;
    int low = S & -S, rest = S ^ low;
    for (T = rest;; T = (T - 1) & rest) {
        if (T != rest) {
            int A = low | T, B = rest ^ T;
            n = np - 1;
            for (i = 0; i < n; i++) newp[i] = pending[i];
            if (__builtin_popcount(A) >= 2) newp[n++] = A;
            if (__builtin_popcount(B) >= 2) newp[n++] = B;
            rec(newp, n);
        }
        if (T == 0) break;
    }
    nm--;
}

int main(void) {
    int k, i, j, c;
    for (k = 2; k <= 3; k++) {
        N = 1 << k;
        for (i = 0; i < N; i++) for (j = 0; j < N; j++) rows[i][j] = (__builtin_popcount(i & j) & 1) ? -1 : 1;
        ntrees = 0; memset(hist, 0, sizeof hist);
        nm = 0;
        for (i = 0; i < N; i++) masks[nm++] = 1 << i;
        int pending[1]; pending[0] = (1 << N) - 1;
        rec(pending, 1);
        printf("N = %d: %lld trees, each with %d choices of the row at the root.\n", N, ntrees, N);
        printf("  number of (tree, root row) cases by the number of rows of H that can be reached:\n");
        int mx = 0;
        for (c = 1; c <= N; c++) if (hist[c]) { printf("    %d row(s): %lld cases\n", c, hist[c]); mx = c; }
        printf("  most rows reached: %d of %d.  A circuit with 2N - 2 = %d lines would need all %d: %s\n",
               mx, N, 2 * N - 2, N, mx < N ? "impossible, as the proof says" : "POSSIBLE -- the proof is contradicted");
        printf("  the proof says at most 2: %s\n", mx <= 2 ? "confirmed" : "NOT CONFIRMED");
    }
    return 0;
}
