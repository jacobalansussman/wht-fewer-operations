// v-1: independent exhaustive test of u-2's claim "no one-run path at 16 points".
// A one-run path: outputs S_1..S_N, neighbours comparable, the sets down(big) minus down(small) and down(S_N)
// all consecutive in ONE order of the inputs.  Path built from the end; NO symmetry reduction.
// Consecutive-ones test: my own, a search over the SET of inputs already placed (not the author's method):
// from a placed set P, the next input x must lie in every family set that is begun and not finished.
#include <stdio.h>
#ifndef K
#define K 4
#endif
#define N (1<<K)
#define FULL ((1u<<N)-1u)
static unsigned down[N], fam[N+1]; static int nf, used[N], best;
static unsigned stamp[1u<<N], cur;
static long long nodes, tests, states, found;
static int rec(unsigned P){
    if (P == FULL) return 1;
    if (stamp[P] == cur) return 0;
    stamp[P] = cur; states++;
    unsigned req = FULL;
    for (int i = 0; i < nf; i++){ unsigned A = fam[i]; if ((A & P) && (A & ~P)) req &= A; }
    unsigned cand = req & ~P & FULL;
    while (cand){ unsigned x = cand & (0u - cand); cand ^= x; if (rec(P | x)) return 1; }
    return 0;
}
static int c1p(void){ cur++; tests++; return rec(0); }
static void dfs(int depth, int last){
    nodes++;
    if (depth > best) best = depth;
    if (depth == N){ found++; return; }
    for (int s = 0; s < N; s++){
        if (used[s]) continue;
        unsigned X;
        if ((s & ~last) == 0) X = down[last] & ~down[s];
        else if ((last & ~s) == 0) X = down[s] & ~down[last];
        else continue;
        fam[nf++] = X;
        if (c1p()){ used[s] = 1; dfs(depth + 1, s); used[s] = 0; }
        nf--;
    }
}
int main(void){
    for (int s = 0; s < N; s++){ unsigned m = 0; for (int t = 0; t < N; t++) if ((t & ~s) == 0) m |= 1u << t; down[s] = m; }
    for (int s = 0; s < N; s++){
        nf = 0; fam[nf++] = down[s]; used[s] = 1; dfs(1, s); used[s] = 0;
        printf("last output %d done: paths %lld nodes %lld longest %d\n", s, found, nodes, best); fflush(stdout);
    }
    printf("K=%d: one-run paths found %lld ; nodes %lld ; tests %lld ; states %lld ; longest partial path %d of %d\n", K, found, nodes, tests, states, best, N);
    return 0;
}
