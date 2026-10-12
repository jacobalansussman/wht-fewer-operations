// u-3-zletter/zmst.c : subset sums Z at N = 2^K points as a letter on ANY input merge tree, PLAIN (all scalings 1), whole numbers.
// For a fixed input tree the number of rectangles is the length of the shortest network joining 0 and the N rows of Z, a step
// being  v -> v + (whole number) * (indicator of one node of the input tree)   [p-8.md section 1].
// This program does NOT allow junction points that are not rows: it takes the minimum SPANNING tree on {0} + rows, where the
// distance of two points is the exact least number of nodes needed to write their difference (a small dynamic programme on the
// tree: Fitch's parsimony count).  So every number it prints is an UPPER bound on tau for that tree, realised over whole numbers.
// It anneals over input trees (move: cut a subtree off and graft it elsewhere).
// Usage: zmst K seed iters T0 [treefile]     treefile: the N-1 internal node masks (64-bit) of a start tree.
// Output: best tau, gates, and the tree.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#define MAXN 128
static int K, N, NN;                 // NN = 2N-1 nodes; leaves 0..N-1, internal N..2N-2
static int par[2*MAXN], ch[2*MAXN][2], root;
static int order[2*MAXN], no;        // postorder of internal nodes
static signed char z[MAXN+1][MAXN];  // rows of Z, and row N = 0
static int W[MAXN+1][MAXN+1];
static uint64_t rng = 88172645463325252ULL;
static inline uint64_t rnd(void){ rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17; return rng; }
static void post(int v){ if(v < N) return; post(ch[v][0]); post(ch[v][1]); order[no++] = v; }
static inline int dist(int a, int b){
    static unsigned char c[2*MAXN][3];
    for(int x = 0; x < N; x++){ int d = z[a][x] - z[b][x] + 1; c[x][0] = d != 0; c[x][1] = d != 1; c[x][2] = d != 2; }
    for(int i = 0; i < no; i++){ int v = order[i], l = ch[v][0], r = ch[v][1];
        int s0 = c[l][0] + c[r][0], s1 = c[l][1] + c[r][1], s2 = c[l][2] + c[r][2];
        int m = s0 < s1 ? s0 : s1; if(s2 < m) m = s2; m++;
        c[v][0] = s0 < m ? s0 : m; c[v][1] = s1 < m ? s1 : m; c[v][2] = s2 < m ? s2 : m; }
    return c[root][1];
}
static int mstpar[MAXN+1];
static int GATES = 0;   // 1: minimise gates = N-1 + (steps, the first step from 0 being free) instead of tau
static int eval(void){
    no = 0; post(root);
    int M = N + 1;
    for(int a = 0; a < M; a++) for(int b = a + 1; b < M; b++) W[a][b] = W[b][a] = dist(a, b) - (GATES && b == N);
    int in[MAXN+1], key[MAXN+1], from[MAXN+1], tot = 0;
    for(int i = 0; i < M; i++){ in[i] = 0; key[i] = 1 << 20; from[i] = -1; }
    key[N] = 0;
    for(int it = 0; it < M; it++){
        int u = -1; for(int i = 0; i < M; i++) if(!in[i] && (u < 0 || key[i] < key[u])) u = i;
        in[u] = 1; tot += key[u]; mstpar[u] = from[u];
        for(int i = 0; i < M; i++) if(!in[i] && W[u][i] < key[i]){ key[i] = W[u][i]; from[i] = u; }
    }
    return tot;
}
static int insub(int v, int u){ while(v >= 0){ if(v == u) return 1; v = par[v]; } return 0; }
// SPR: detach subtree u (u != root, par[u] != -1), regraft above v (v not in subtree(u), v != par[u], v != u)
static int spr(int u, int v){
    int p = par[u]; if(p < 0) return 0;
    if(v == u || v == p || insub(v, u)) return 0;
    int s = ch[p][0] == u ? ch[p][1] : ch[p][0];
    if(v == s) return 0;   // same tree
    int g = par[p];
    // remove p: s takes its place
    par[s] = g; if(g >= 0){ if(ch[g][0] == p) ch[g][0] = s; else ch[g][1] = s; } else root = s;
    // insert p above v
    int q = par[v];
    par[p] = q; if(q >= 0){ if(ch[q][0] == v) ch[q][0] = p; else ch[q][1] = p; } else root = p;
    ch[p][0] = v; ch[p][1] = u; par[v] = p; par[u] = p;
    return 1;
}
static uint64_t maskof(int v){ return v < N ? 1ULL << v : maskof(ch[v][0]) | maskof(ch[v][1]); }
static void printtree(FILE *f){ no = 0; post(root); for(int i = no - 1; i >= 0; i--) fprintf(f, "%llu ", (unsigned long long)maskof(order[i])); fprintf(f, "\n"); }
static int savep[2*MAXN], savec[2*MAXN][2], saver;
static void save(void){ memcpy(savep, par, sizeof par); memcpy(savec, ch, sizeof ch); saver = root; }
static void restore(void){ memcpy(par, savep, sizeof par); memcpy(ch, savec, sizeof ch); root = saver; }
static int bestp[2*MAXN], bestc[2*MAXN][2], bestr;
int main(int argc, char **argv){
    K = atoi(argv[1]); N = 1 << K; NN = 2 * N - 1; GATES = getenv("GATES") != NULL;
    rng ^= (uint64_t)atoll(argv[2]) * 0x9E3779B97F4A7C15ULL; for(int i = 0; i < 20; i++) rnd();
    long iters = atol(argv[3]); double T0 = atof(argv[4]);
    for(int s = 0; s < N; s++) for(int t = 0; t < N; t++) z[s][t] = ((t & s) == t);
    for(int t = 0; t < N; t++) z[N][t] = 0;
    if(argc > 5){
        FILE *f = fopen(argv[5], "r"); uint64_t m[MAXN]; int nm = 0; unsigned long long x;
        while(nm < N - 1 && fscanf(f, "%llu", &x) == 1) m[nm++] = x; fclose(f);
        // sort by size ascending, build
        for(int i = 0; i < nm; i++) for(int j = i + 1; j < nm; j++) if(__builtin_popcountll(m[j]) < __builtin_popcountll(m[i])){ uint64_t t = m[i]; m[i] = m[j]; m[j] = t; }
        uint64_t nm_mask[2*MAXN]; int top[2*MAXN]; for(int i = 0; i < N; i++){ nm_mask[i] = 1ULL << i; par[i] = -1; }
        for(int i = 0; i < nm; i++){ int v = N + i; nm_mask[v] = m[i]; par[v] = -1; int c = 0;
            for(int w = 0; w < v; w++) if(par[w] < 0 && (nm_mask[w] & m[i]) == nm_mask[w]){ if(c >= 2){ fprintf(stderr, "bad tree\n"); return 1; } ch[v][c++] = w; par[w] = v; }
            if(c != 2){ fprintf(stderr, "bad tree (node %d has %d children)\n", i, c); return 1; } (void)top; }
        root = N + nm - 1;
    } else {
        // random tree: random merges
        int live[MAXN], nl = N; for(int i = 0; i < N; i++){ live[i] = i; par[i] = -1; }
        for(int v = N; v < NN; v++){ int a = rnd() % nl; int x = live[a]; live[a] = live[--nl]; int b = rnd() % nl; int y = live[b];
            ch[v][0] = x; ch[v][1] = y; par[x] = v; par[y] = v; par[v] = -1; live[b] = v; }
        root = NN - 1;
    }
    int cur = eval(), best = cur; memcpy(bestp, par, sizeof par); memcpy(bestc, ch, sizeof ch); bestr = root;
    fprintf(stderr, "start %d\n", cur);
    for(long it = 0; it < iters; it++){
        double T = T0 * (1.0 - (double)it / iters) + 0.02;
        save();
        int u = rnd() % NN, v = rnd() % NN;
        if(!spr(u, v)) continue;
        int e = eval();
        if(e <= cur || (double)(rnd() >> 11) / 9007199254740992.0 < exp((cur - e) / T)){
            cur = e; if(cur < best){ best = cur; memcpy(bestp, par, sizeof par); memcpy(bestc, ch, sizeof ch); bestr = root; fprintf(stderr, "it %ld best %d\n", it, best); }
        } else restore();
    }
    memcpy(par, bestp, sizeof par); memcpy(ch, bestc, sizeof ch); root = bestr;
    int tau = eval();
    int deg0 = 0; for(int i = 0; i < N; i++) if(mstpar[i] == N) deg0++;
    if(GATES) printf("K %d gates %d (= N-1 + %d) tau %d deg0 %d\n", K, N - 1 + tau, tau, tau + deg0, deg0); else printf("K %d tau %d deg0 %d\n", K, tau, deg0);
    printtree(stdout);
    for(int i = 0; i < N; i++) printf("row %d from %d cost %d\n", i, mstpar[i], W[i][mstpar[i]] + (GATES && mstpar[i] == N));
    return 0;
}
