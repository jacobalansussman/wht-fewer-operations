// h-5 / pairex.c : EXHAUSTIVE search, 8 points, count (G), over helper sets inside a finite pool given with its gates (pool_*.txt).
// Question: is there a circuit with at most 8 + hmax gates (hmax helpers; every output is one gate)?
// Each helper set is visited once: at a node the derivable pool wires are tried in index order and a wire, once tried, is
// forbidden in the later siblings' subtrees (a set containing both would have been found under the earlier one: derivability is monotone).
// Outputs are added the moment they are derivable (never worse).
// Pruning (valid in the pair class, see h-5.md): D(i,t) = dim span{held wires with factor t=(1,+-1) on bit i} (rank modulo 3, 6 spaces of dim 4)
// must reach 24 in all, a gate raises the total by at most 2, a missing output by at most min(2, number of its three spaces where it is new).
// usage: pairex pool.txt hmax [prune 0/1]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXN 400
static int n, ntr, hmax, PR = 1, SYM = 1;
static int vec[MAXN][8], ins[8], outs[8], isout[MAXN];
static int *plist[MAXN], plen[MAXN];           // for wire x: pairs (other, third)
static int *rec[MAXN], rlen[MAXN];             // for wire w: parent pairs (u, v)
static int held[MAXN], cnt[MAXN], forb[MAXN];
static int inK[MAXN][6]; static int rest[MAXN][6][4];
static int bas[6][4][4], bdim[6];              // echelon bases mod 3
static int stack[64], sp; static int savdim[64][6]; static int savbas[64][6][4][4];
static unsigned long long nodes[32]; static int maxinc = 0;
static int HUBP = 1, SYM2 = 1, firstroot = 0;
static short gmap[384][MAXN]; static int stab[384], nstab;   // the symmetry group on the pool; the elements that fix the first helper
static int entslice[MAXN];                      // -1, or 4*m + r for a wire entangled exactly on the pair {0,1,2} minus {m}, with factor r on bit m (r: 0 = e0, 1 = e1, 2 = (1,1), 3 = (1,-1))
static int hub[12];                             // held entangled wires per slice
static int ndb[MAXN], dbslice[MAXN][3], dbk1[MAXN][3], dbk2[MAXN][3];   // ways a wire can be a double birth: slice, the two spaces
static int dlist[MAXN], ndl;
static int reduce(int k, int *v) {              // reduce v by basis k; returns 1 if non-zero remains (v is left reduced)
    for (int r = 0; r < bdim[k]; r++) {
        int pv = -1; for (int c = 0; c < 4; c++) if (bas[k][r][c]) { pv = c; break; }
        if (v[pv]) { int f = (v[pv] * bas[k][r][pv]) % 3;   // bas pivot is 1 or 2; inverse of x mod 3 is x
            for (int c = 0; c < 4; c++) v[c] = ((v[c] - f * bas[k][r][c]) % 3 + 3) % 3; }
    }
    for (int c = 0; c < 4; c++) if (v[c]) return 1;
    return 0;
}
static int newcount(int w) { int k2 = 0; for (int k = 0; k < 6; k++) if (inK[w][k]) { int v[4]; memcpy(v, rest[w][k], sizeof v); if (reduce(k, v)) k2++; } return k2; }
static void add(int w) {
    memcpy(savdim[sp], bdim, sizeof bdim); memcpy(savbas[sp], bas, sizeof bas);
    int inc = 0;
    for (int k = 0; k < 6; k++) if (inK[w][k]) { int v[4]; memcpy(v, rest[w][k], sizeof v); if (reduce(k, v)) { memcpy(bas[k][bdim[k]++], v, sizeof v); inc++; } }
    if (inc > maxinc) maxinc = inc;
    held[w] = 1; stack[sp++] = w; if (entslice[w] >= 0) hub[entslice[w]]++;
    for (int q = 0; q < plen[w]; q += 2) if (held[plist[w][q]]) cnt[plist[w][q + 1]]++;
}
static void undo(void) {
    int w = stack[--sp];
    for (int q = 0; q < plen[w]; q += 2) if (held[plist[w][q]]) cnt[plist[w][q + 1]]--;
    held[w] = 0; if (entslice[w] >= 0) hub[entslice[w]]--; memcpy(bdim, savdim[sp], sizeof bdim); memcpy(bas, savbas[sp], sizeof bas);
}
static int closure(void) { int ad = 0, ch = 1; while (ch) { ch = 0; for (int i = 0; i < 8; i++) if (!held[outs[i]] && cnt[outs[i]] > 0) { add(outs[i]); ad++; ch = 1; } } return ad; }
static int missing(void) { int m = 0; for (int i = 0; i < 8; i++) if (!held[outs[i]]) m++; return m; }
static int sol[64], nsol;
static int dfs(int h) {                         // h helpers used
    int miss = missing();
    if (miss == 0) { nsol = sp; memcpy(sol, stack, sizeof(int) * sp); return 1; }
    if (h == hmax) return 0;
    nodes[h]++;
    int hrem = hmax - h;
    if (PR) {
        int tot = 0; for (int k = 0; k < 6; k++) tot += bdim[k];
        int cap = 2 * hrem; for (int i = 0; i < 8; i++) if (!held[outs[i]]) { int c = newcount(outs[i]); cap += c > 2 ? 2 : c; }
        if (24 - tot > cap) return 0;
        for (int b = 0; b < 3; b++) if (8 - bdim[2 * b] - bdim[2 * b + 1] > hrem + miss) return 0;
        if (HUBP) {     // a wire that raises two spaces at once needs a held wire entangled on that pair in its slice (h-5.md, lemma 2)
            int A = 0, cs[12] = {0}, Dout = 0, Dh = 0, single_out = 0;
            for (int q = 0; q < ndl; q++) { int w = dlist[q]; if (held[w] || (!isout[w] && forb[w])) continue;
                int inA = 0, can = 0, sl[3], ns = 0;
                for (int z = 0; z < ndb[w]; z++) {
                    int v1[4], v2[4]; memcpy(v1, rest[w][dbk1[w][z]], sizeof v1); memcpy(v2, rest[w][dbk2[w][z]], sizeof v2);
                    if (reduce(dbk1[w][z], v1) && reduce(dbk2[w][z], v2)) { can = 1; if (hub[dbslice[w][z]] > 0) inA = 1; else sl[ns++] = dbslice[w][z]; } }
                if (can) { if (isout[w]) Dout++; else Dh++; }
                if (inA) A++; else for (int z = 0; z < ns; z++) cs[sl[z]]++;
            }
            for (int i = 0; i < 8; i++) if (!held[outs[i]] && newcount(outs[i]) > 0) single_out++;
            for (int x = 0; x < 12; x++) for (int y = x + 1; y < 12; y++) if (cs[y] > cs[x]) { int t = cs[x]; cs[x] = cs[y]; cs[y] = t; }
            int best = 0, top = 0;
            for (int e = 0; e <= hrem; e++) {       // e = entangled helpers still to come (each raises the total by at most 1 and opens one slice)
                if (e > 0 && e <= 12) top += cs[e - 1];
                int d = A + top, d2 = Dout + (hrem - e < Dh ? hrem - e : Dh); if (d > d2) d = d2;
                int v = hrem + single_out + d; if (v > best) best = v; }
            if (24 - tot > best) return 0;
        }
    }
    int cand[MAXN], nc = 0;
    if (hrem == 1) {                            // the last helper must be a parent of a missing output, with the other parent held
        static int mark[MAXN]; 
        for (int i = 0; i < 8; i++) if (!held[outs[i]]) { int y = outs[i];
            for (int q = 0; q < rlen[y]; q += 2) { int u = rec[y][q], v = rec[y][q + 1];
                if (held[u] && !held[v] && cnt[v] > 0 && !forb[v] && !isout[v] && !mark[v]) { mark[v] = 1; cand[nc++] = v; }
                if (held[v] && !held[u] && cnt[u] > 0 && !forb[u] && !isout[u] && !mark[u]) { mark[u] = 1; cand[nc++] = u; } } }
        for (int i = 0; i < nc; i++) mark[cand[i]] = 0;
    } else for (int w = 0; w < n; w++) if (!held[w] && cnt[w] > 0 && !forb[w] && !isout[w]) cand[nc++] = w;
    int orbit1[MAXN], no1 = 0;
    if (h == 0 && SYM) {                        // root: the 48 candidates are two orbits of the symmetry group (bit permutations, translations
        int rs = -1, rb = -1;                   // of the address, multiplication by a character): 24 sums of two inputs one bit apart, 24 two bits apart
        for (int i = 0; i < nc; i++) { int w = cand[i], a = -1, b = -1; for (int x = 0; x < 8; x++) if (vec[w][x]) { if (a < 0) a = x; else b = x; }
            int d = a ^ b; if (d == 1 || d == 2 || d == 4) { orbit1[no1++] = w; if (rs < 0) rs = w; } else if (rb < 0) rb = w; }
        if (nc != 48 || no1 != 24) { printf("root orbit check failed %d %d\n", nc, no1); exit(3); }
        cand[0] = rs; cand[1] = rb; nc = 2;
    }
    int ok = 0, done = 0;
    if (h == 1 && SYM && SYM2 && firstroot) {   // second helper under the first root orbit: one representative per orbit of the stabiliser of the first helper;
        static int fl[MAXN * 2]; int nfl = 0;   // after a representative's subtree its whole orbit is barred (the barred set stays closed under the stabiliser)
        for (int i = 0; i < nc && !ok; i++) { int w = cand[i]; if (forb[w]) continue;
            add(w); int ad = closure(); ok = dfs(h + 1); for (int k = 0; k <= ad; k++) undo();
            for (int g = 0; g < nstab; g++) { int x = gmap[stab[g]][w]; if (!forb[x]) { forb[x]++; fl[nfl++] = x; } } }
        for (int i = 0; i < nfl; i++) forb[fl[i]]--;
        return ok;
    }
    for (int i = 0; i < nc && !ok; i++) {
        if (h == 0 && SYM && i == 1) for (int q = 0; q < no1; q++) forb[orbit1[q]]++;
        if (h == 0) firstroot = (SYM && i == 0);
        int w = cand[i]; add(w); int ad = closure();
        ok = dfs(h + 1);
        for (int k = 0; k <= ad; k++) undo();
        forb[w]++; done = i + 1;
    }
    for (int i = 0; i < done; i++) forb[cand[i]]--;
    return ok;
}
int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r"); hmax = atoi(argv[2]); if (argc > 3) PR = atoi(argv[3]); if (argc > 4) SYM = atoi(argv[4]); if (argc > 5) HUBP = atoi(argv[5]); if (argc > 6) SYM2 = atoi(argv[6]);
    if (fscanf(f, "%d %d", &n, &ntr) != 2) return 2;
    for (int i = 0; i < n; i++) for (int j = 0; j < 8; j++) if (fscanf(f, "%d", &vec[i][j]) != 1) return 2;
    for (int i = 0; i < 8; i++) if (fscanf(f, "%d", &ins[i]) != 1) return 2;
    for (int i = 0; i < 8; i++) { if (fscanf(f, "%d", &outs[i]) != 1) return 2; isout[outs[i]] = 1; }
    int (*tr)[3] = malloc(sizeof(int[3]) * ntr);
    for (int t = 0; t < ntr; t++) { if (fscanf(f, "%d %d %d", &tr[t][0], &tr[t][1], &tr[t][2]) != 3) return 2; for (int a = 0; a < 3; a++) { plen[tr[t][a]] += 4; rlen[tr[t][a]] += 2; } }
    for (int i = 0; i < n; i++) { plist[i] = malloc(sizeof(int) * (plen[i] + 1)); rec[i] = malloc(sizeof(int) * (rlen[i] + 1)); plen[i] = rlen[i] = 0; }
    for (int t = 0; t < ntr; t++) for (int a = 0; a < 3; a++) { int x = tr[t][a], y = tr[t][(a + 1) % 3], z = tr[t][(a + 2) % 3];
        plist[x][plen[x]++] = y; plist[x][plen[x]++] = z; plist[x][plen[x]++] = z; plist[x][plen[x]++] = y; rec[x][rlen[x]++] = y; rec[x][rlen[x]++] = z; }
    for (int w = 0; w < n; w++) for (int b = 0; b < 3; b++) for (int s = 0; s < 2; s++) {
        int t = s ? -1 : 1, ok = 1, c = 0;
        for (int x = 0; x < 8; x++) if (!((x >> b) & 1)) { if (vec[w][x | (1 << b)] != t * vec[w][x]) ok = 0; rest[w][2 * b + s][c++] = ((vec[w][x] % 3) + 3) % 3; }
        inK[w][2 * b + s] = ok;
    }
    for (int w = 0; w < n; w++) {
        int r1[3], fac[3];                      // per bit: product across that cut? factor class
        for (int b = 0; b < 3; b++) { int lo[4], hi[4], c = 0, zl = 1, zh = 1, eq = 1, ne = 1, pr = 1;
            for (int x = 0; x < 8; x++) if (!((x >> b) & 1)) { lo[c] = vec[w][x]; hi[c] = vec[w][x | (1 << b)]; c++; }
            for (int a = 0; a < 4; a++) { if (lo[a]) zl = 0; if (hi[a]) zh = 0; if (lo[a] != hi[a]) eq = 0; if (lo[a] != -hi[a]) ne = 0; for (int d = a + 1; d < 4; d++) if (lo[a] * hi[d] != lo[d] * hi[a]) pr = 0; }
            r1[b] = pr; fac[b] = zh ? 0 : zl ? 1 : eq ? 2 : ne ? 3 : 4; }
        entslice[w] = -1;
        if (r1[0] + r1[1] + r1[2] == 1) { int m = r1[0] ? 0 : r1[1] ? 1 : 2; if (fac[m] > 3) { printf("factor outside e0,e1,+,-\n"); exit(4); } entslice[w] = 4 * m + fac[m]; }
        ndb[w] = 0;
        if (r1[0] && r1[1] && r1[2]) for (int m = 0; m < 3; m++) { int i = (m + 1) % 3, j = (m + 2) % 3;
            if (fac[i] >= 2 && fac[j] >= 2 && fac[i] <= 3 && fac[j] <= 3 && fac[m] <= 3) { dbslice[w][ndb[w]] = 4 * m + fac[m]; dbk1[w][ndb[w]] = 2 * i + (fac[i] - 2); dbk2[w][ndb[w]] = 2 * j + (fac[j] - 2); ndb[w]++; } }
        if (ndb[w]) dlist[ndl++] = w;
    }
    printf("wires that can be double births: %d (outputs and half pieces)\n", ndl);
    {   // the group: bit permutations (6) x translations of the address (8) x multiplication by a character (8)
        static int code[6561]; for (int i = 0; i < 6561; i++) code[i] = -1;
        for (int w = 0; w < n; w++) { int c = 0; for (int x = 7; x >= 0; x--) c = c * 3 + vec[w][x] + 1; code[c] = w; }
        int perms[6][3] = {{0,1,2},{0,2,1},{1,0,2},{1,2,0},{2,0,1},{2,1,0}}, ng = 0, bad = 0;
        for (int pi = 0; pi < 6; pi++) for (int a = 0; a < 8; a++) for (int c = 0; c < 8; c++, ng++)
            for (int w = 0; w < n; w++) { int v[8];
                for (int x = 0; x < 8; x++) { int y = 0; for (int b = 0; b < 3; b++) if ((x >> b) & 1) y |= 1 << perms[pi][b];
                    v[x] = (__builtin_popcount(c & x) & 1 ? -1 : 1) * vec[w][y ^ a]; }
                int sgn = 0; for (int x = 0; x < 8 && !sgn; x++) if (v[x]) sgn = v[x];
                int cc = 0; for (int x = 7; x >= 0; x--) cc = cc * 3 + sgn * v[x] + 1;
                if (code[cc] < 0) bad++; gmap[ng][w] = (short)code[cc]; }
        int rs = -1; for (int w = 0; w < n && rs < 0; w++) { int a = -1, b = -1, k2 = 0; for (int x = 0; x < 8; x++) if (vec[w][x]) { k2++; if (a < 0) a = x; else b = x; }
            if (k2 == 2) { int d = a ^ b; if (d == 1 || d == 2 || d == 4) rs = w; } }
        for (int g = 0; g < ng; g++) if (rs >= 0 && gmap[g][rs] == rs) stab[nstab++] = g;
        int tbad = 0;                             // the group must map gates to gates
        for (int g = 0; g < ng; g += 37) for (int t = 0; t < ntr; t += 11) { int x = gmap[g][tr[t][0]], y = gmap[g][tr[t][1]], z = gmap[g][tr[t][2]], f = 0;
            for (int q = 0; q < rlen[x]; q += 2) if ((rec[x][q] == y && rec[x][q + 1] == z) || (rec[x][q] == z && rec[x][q + 1] == y)) f = 1; if (!f) tbad++; }
        printf("symmetry group: %d elements, images outside the pool %d, sampled gates not mapped to gates %d, stabiliser of the first helper %d\n", ng, bad, tbad, nstab);
        if (bad || tbad) SYM2 = 0;
    }
    for (int i = 0; i < 8; i++) add(ins[i]);
    closure();
    int ok = dfs(0);
    printf("pool %s: %d wires, %d gates(triples); helpers allowed %d => at most %d gates; pruning %d; root symmetry %d; hub pruning %d\n", argv[1], n, ntr, hmax, 8 + hmax, PR, SYM, HUBP);
    printf("nodes by helpers used:"); for (int h = 0; h < hmax; h++) printf(" %d:%llu", h, nodes[h]); printf("\nlargest increment of the potential by one wire: %d\n", maxinc);
    if (!ok) { printf("RESULT: NO circuit with at most %d gates in this pool (exhaustive)\n", 8 + hmax); return 0; }
    printf("RESULT: YES, %d gates:\n", nsol - 8);
    for (int i = 8; i < nsol; i++) { printf("  %s", isout[sol[i]] ? "OUT " : "help"); for (int j = 0; j < 8; j++) printf(" %2d", vec[sol[i]][j]); printf("\n"); }
    return 0;
}
