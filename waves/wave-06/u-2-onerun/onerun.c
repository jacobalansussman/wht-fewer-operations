// u-2-onerun: exact search for "every output is its neighbour plus or minus ONE run of inputs" for subset sums at N = 2^k points.
// Plain version.  Outputs = subsets S of {1..k} (addresses 0..N-1) plus one extra element BOT below everything (empty row).
// A step joins two comparable outputs lo < hi; its set is  down(hi) minus down(lo)  (down(S) = all T inside S; down(BOT) = empty).
// PATH mode: a path through all outputs ending at BOT (depth-first from the BOT end).
// TREE mode: every output chooses a parent (a comparable output or BOT), no cycles.
// At every node the family of sets so far must have the consecutive-ones property (exact test below), which only gets harder.
// usage: onerun <k> <mode: path|tree> <maxsolutions> [uselemma 0/1] [nodecap]
// Exact: whole-number bit sets only.  Count (G): a yes gives a circuit of at most 3N - 4 gates (path) or 3N - 1 (tree).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned long long u64;
static int k, N;
static u64 down[65];            // down[S] as a bit set over inputs; down[N] (BOT) = 0
static u64 fam[70]; static int nf;   // the family of sets so far
static unsigned long long nodes = 0, c1pcalls = 0, lemmacuts = 0, nodecap = 0;
static int uselemma = 1;

// ---------- exact consecutive-ones test ----------
// classes of inputs with equal membership signature are placed as one block (twins may be taken adjacent).
static int ncl; static u64 sig[70]; static int clcnt[70];
static int cnt[70], sz[70]; static int used[70];
static int rec(int placed, int incomp, u64 open) {
    if (placed == incomp) return 1;
    for (int c = 0; c < ncl; c++) if (!used[c] && used[c] != 2) {
        if (open & ~sig[c]) continue;                 // an open set would be interrupted
        // place class c
        u64 s = sig[c], nopen = open; used[c] = 1;
        for (u64 t = s; t; t &= t - 1) { int i = __builtin_ctzll(t); cnt[i] += clcnt[c]; if (cnt[i] == sz[i]) nopen &= ~(1ULL << i); else nopen |= (1ULL << i); }
        int ok = rec(placed + 1, incomp, nopen);
        for (u64 t = s; t; t &= t - 1) { int i = __builtin_ctzll(t); cnt[i] -= clcnt[c]; }
        used[c] = 0;
        if (ok) return 1;
    }
    return 0;
}
static int comp_of[70];
static int c1p(void) {
    c1pcalls++;
    // signatures
    static u64 esig[64]; ncl = 0;
    for (int x = 0; x < N; x++) { u64 s = 0; for (int i = 0; i < nf; i++) if (fam[i] >> x & 1) s |= 1ULL << i; esig[x] = s; }
    for (int x = 0; x < N; x++) { if (!esig[x]) continue; int c; for (c = 0; c < ncl; c++) if (sig[c] == esig[x]) break; if (c == ncl) { sig[ncl] = esig[x]; clcnt[ncl] = 0; ncl++; } clcnt[c]++; }
    if (ncl > 2 * nf - 1) return 0;                    // n intervals cut the line into at most 2n - 1 occupied cells
    for (int i = 0; i < nf; i++) { sz[i] = __builtin_popcountll(fam[i]); cnt[i] = 0; }
    // components of classes (two classes are linked when a set contains both)
    for (int c = 0; c < ncl; c++) comp_of[c] = c;
    int changed = 1;
    while (changed) { changed = 0; for (int a = 0; a < ncl; a++) for (int b = a + 1; b < ncl; b++) if ((sig[a] & sig[b]) && comp_of[a] != comp_of[b]) { int m = comp_of[a] < comp_of[b] ? comp_of[a] : comp_of[b]; int o = comp_of[a] + comp_of[b] - m; for (int c = 0; c < ncl; c++) if (comp_of[c] == o) comp_of[c] = m; changed = 1; } }
    for (int root = 0; root < ncl; root++) if (comp_of[root] == root) {
        int incomp = 0; for (int c = 0; c < ncl; c++) { if (comp_of[c] == root) { used[c] = 0; incomp++; } else used[c] = 2; }
        // rec skips classes with used != 0, so mark others as 2
        int ok = 0;
        // rec's loop condition: !used[c]
        ok = rec(0, incomp, 0);
        if (!ok) return 0;
    }
    return 1;
}
// ---------- the two-chains lemma as a cheap filter ----------
// For three sets with a common input: one lies inside the union of the other two, and one contains the intersection of the other two.
static int lemma_ok_with_new(void) {
    u64 c = fam[nf - 1];
    for (int a = 0; a < nf - 1; a++) { u64 A = fam[a]; if (!(A & c)) continue;
        for (int b = a + 1; b < nf - 1; b++) { u64 B = fam[b]; if (!(A & B & c)) continue;
            int un = !(A & ~(B | c)) || !(B & ~(A | c)) || !(c & ~(A | B));
            int in = !((A & B) & ~c) || !((A & c) & ~B) || !((B & c) & ~A);
            if (!un || !in) return 0; } }
    return 1;
}
// ---------- PATH mode ----------
static int path[70]; static u64 visited; static long long nsol = 0, maxsol = 1; static int bestdepth = 0;
static void print_solution_path(int len) {
    printf("SOLUTION path (first output first, last output is one run):");
    for (int i = len - 1; i >= 0; i--) printf(" %d", path[i]);
    printf("\n  sets (as input bit masks), from the last step: ");
    for (int i = 0; i < nf; i++) printf(" %llx", fam[i]);
    printf("\n"); fflush(stdout);
}
static void dfs_path(int len) {
    nodes++;
    if (nodecap && nodes > nodecap) return;
    if (len > bestdepth) { bestdepth = len; fprintf(stderr, "depth %d of %d at node %llu\n", len, N, nodes); }
    if (len == N) { nsol++; if (nsol <= 3) print_solution_path(len); return; }
    int cur = path[len - 1];
    for (int v = 0; v < N; v++) {
        if (visited >> v & 1) continue;
        int lo, hi;
        if ((v & cur) == v) { lo = v; hi = cur; } else if ((v & cur) == cur) { lo = cur; hi = v; } else continue;
        fam[nf++] = down[hi] & ~down[lo];
        int ok = (!uselemma || lemma_ok_with_new());
        if (!ok) lemmacuts++;
        if (ok) ok = c1p();
        if (ok) { path[len] = v; visited |= 1ULL << v; dfs_path(len + 1); visited &= ~(1ULL << v); }
        nf--;
        if (nsol >= maxsol) return;
        if (nodecap && nodes > nodecap) return;
    }
}
// ---------- TREE mode: vertices choose parents in the order given by ord[] ----------
static int par[70], uf[70], ord[70];
static int find(int x) { while (uf[x] != x) x = uf[x]; return x; }
static void dfs_tree(int idx) {
    nodes++;
    if (nodecap && nodes > nodecap) return;
    if (idx > bestdepth) { bestdepth = idx; fprintf(stderr, "depth %d of %d at node %llu\n", idx, N, nodes); }
    if (idx == N) { nsol++; if (nsol <= 3) { printf("SOLUTION tree: parent of each output (%d = BOT):", N); for (int v = 0; v < N; v++) printf(" %d<-%d", v, par[v]); printf("\n  sets:"); for (int i = 0; i < nf; i++) printf(" %llx", fam[i]); printf("\n"); fflush(stdout); } return; }
    int v = ord[idx];
    for (int p = N; p >= 0; p--) {
        if (p == v) continue;
        int lo, hi;
        if (p == N) { lo = N; hi = v; } else if ((v & p) == v) { lo = v; hi = p; } else if ((v & p) == p) { lo = p; hi = v; } else continue;
        int rv = find(v), rp = find(p); if (rv == rp) continue;
        // v's "parent edge": to keep each tree counted once we need an orientation; here every vertex picks ONE edge and the
        // edges must be acyclic: N edges on N + 1 vertices without cycle = spanning tree; each tree arises from exactly one choice
        // (orient towards BOT) only if the edge chosen by v leads towards BOT; we do not enforce that, so trees are over-counted, never missed.
        fam[nf++] = down[hi] & ~down[lo];
        int ok = (!uselemma || lemma_ok_with_new());
        if (!ok) lemmacuts++;
        if (ok) ok = c1p();
        if (ok) { par[v] = p; uf[rv] = rp; dfs_tree(idx + 1); uf[rv] = rv; }
        nf--;
        if (nsol >= maxsol) return;
        if (nodecap && nodes > nodecap) return;
    }
}
int main(int argc, char **argv) {
    k = atoi(argv[1]); N = 1 << k; const char *mode = argv[2]; maxsol = atoll(argv[3]);
    if (argc > 4) uselemma = atoi(argv[4]);
    if (argc > 5) nodecap = strtoull(argv[5], 0, 10);
    for (int S = 0; S < N; S++) { u64 d = 0; for (int T = 0; T < N; T++) if ((T & S) == T) d |= 1ULL << T; down[S] = d; }
    down[N] = 0;
    if (!strcmp(mode, "path")) {
        // last output: up to permutations of the bits it is {1..j}, j = 0..k
        for (int j = 0; j <= k && nsol < maxsol; j++) {
            int last = (1 << j) - 1; nf = 0; fam[nf++] = down[last]; path[0] = last; visited = 1ULL << last;
            unsigned long long n0 = nodes; long long s0 = nsol; bestdepth = 0;
            dfs_path(1);
            printf("k=%d path, last output of size %d: nodes %llu, solutions found %lld (cap %lld)%s\n", k, j, nodes - n0, nsol - s0, maxsol, (nodecap && nodes > nodecap) ? "  NODE CAP HIT: not exhaustive" : ""); fflush(stdout);
            if (nodecap && nodes > nodecap) break;
        }
    } else {
        // order: by size, largest first (the top has the fewest choices)
        int m = 0; for (int s = k; s >= 0; s--) for (int v = 0; v < N; v++) if (__builtin_popcount(v) == s) ord[m++] = v;
        for (int v = 0; v <= N; v++) uf[v] = v;
        nf = 0; dfs_tree(0);
        printf("k=%d tree: nodes %llu, solutions found %lld (cap %lld)%s\n", k, nodes, nsol, maxsol, (nodecap && nodes > nodecap) ? "  NODE CAP HIT: not exhaustive" : "");
    }
    printf("total nodes %llu, consecutive-ones tests %llu, cut by the three-set lemma first %llu\n", nodes, c1pcalls, lemmacuts);
    return 0;
}
