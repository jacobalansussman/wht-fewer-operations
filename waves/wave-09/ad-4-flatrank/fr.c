/* fr.c [ad-4-flatrank]  flat rank of quadric signs g(z) = (-1)^(z1 z2 + z3 z4 + ...) on K bits.
   SIGNED FLAT: (-1)^(b.z) on a coset a+V of a subspace V, 0 elsewhere (taken up to a global sign).
   UNSIGNED FLAT: b = 0.
   modes:
     fr K exh        exhaustive, exact (integer Gram determinants): is g in the span of 2 or of 3 signed flats?  (K = 4 only)
     fr K ls r secs seed [unsigned]   local search (FLOATS) for r flats whose span contains g; candidates printed for exact replay
   compile: cc -O3 -o fr fr.c -lm                                                                                     */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
typedef unsigned long long u64;
static int K, N;
static u64 subs[500000]; static int nsub;
static int popc(u64 x){ return __builtin_popcountll(x); }
static int dot(int a, int b){ return popc((u64)(a & b)) & 1; }
/* flats */
static u64 *fsup, *fneg; static signed char *fdm; static int nf; static signed char *F; /* nf x N entries */
static int *fb, *fa; static u64 *fV;
static u64 closure(u64 S, int v){ u64 T = S; for (int s = 0; s < N; s++) if ((S >> s) & 1) T |= 1ULL << (s ^ v); return T; }
static int cmpu(const void *a, const void *b){ u64 x = *(u64*)a, y = *(u64*)b; return x < y ? -1 : x > y; }
static void gen_subs(void){
    /* all subspaces as bit masks over the N points, by closure, level by level */
    static u64 cur[500000], nxt[2000000]; int nc = 1; cur[0] = 1ULL; nsub = 0; subs[nsub++] = 1ULL;
    for (int d = 0; d < K; d++){
        int nn = 0;
        for (int i = 0; i < nc; i++) for (int v = 1; v < N; v++) if (!((cur[i] >> v) & 1)){
            /* only add v if v is the smallest element of the new part: avoids duplicates partially */
            u64 T = closure(cur[i], v); nxt[nn++] = T; if (nn >= 2000000){ qsort(nxt, nn, 8, cmpu); int m = 0; for (int j = 0; j < nn; j++) if (!j || nxt[j] != nxt[j-1]) nxt[m++] = nxt[j]; nn = m; }
        }
        qsort(nxt, nn, 8, cmpu); int m = 0; for (int j = 0; j < nn; j++) if (!j || nxt[j] != nxt[j-1]) nxt[m++] = nxt[j];
        nc = m; memcpy(cur, nxt, 8 * (size_t)m); for (int j = 0; j < m; j++) subs[nsub++] = cur[j];
    }
}
static void gen_flats(int unsigned_only){
    size_t cap = (size_t)nsub * N + 16; fsup = malloc(8 * cap); fneg = malloc(8 * cap); fdm = malloc(cap); fb = malloc(4 * cap); fa = malloc(4 * cap); fV = malloc(8 * cap); nf = 0;
    for (int si = 0; si < nsub; si++){
        u64 V = subs[si]; int d = 0; while ((1 << d) < popc(V)) d++;
        for (int a = 0; a < N; a++){
            /* coset a+V, only once: a must be its smallest element */
            u64 C = 0; int amin = N; for (int s = 0; s < N; s++) if ((V >> s) & 1){ C |= 1ULL << (s ^ a); if ((s ^ a) < amin) amin = s ^ a; }
            if (amin != a) continue;
            /* characters b restricted to V: distinct restrictions only; b runs over representatives */
            static u64 seen[64]; int ns = 0;
            for (int b = 0; b < N; b++){
                u64 neg = 0; for (int s = 0; s < N; s++) if ((C >> s) & 1) if (dot(b, s ^ a)) neg |= 1ULL << s;   /* sign relative to the point a: + at a */
                int dup = 0; for (int j = 0; j < ns; j++) if (seen[j] == neg) dup = 1;
                if (dup) continue; seen[ns++] = neg;
                if (unsigned_only && neg) continue;
                fsup[nf] = C; fneg[nf] = neg; fdm[nf] = d; fb[nf] = b; fa[nf] = a; fV[nf] = V; nf++;
            }
        }
    }
    F = malloc((size_t)nf * N);
    for (int i = 0; i < nf; i++) for (int s = 0; s < N; s++) F[(size_t)i * N + s] = ((fsup[i] >> s) & 1) ? (((fneg[i] >> s) & 1) ? -1 : 1) : 0;
}
static int g[64]; static int nocover = 0;
static void target(void){ for (int z = 0; z < N; z++){ int q = 0; for (int i = 0; i + 1 < K; i += 2) q ^= ((z >> i) & 1) & ((z >> (i + 1)) & 1); g[z] = q ? -1 : 1; }
    if (getenv("TARGET") && !strcmp(getenv("TARGET"), "nb")) for (int z = 0; z < N; z++) g[z] = (popc((u64)z) == 1);   /* control: neighbour sums, known flat rank ceil(K/2) */
    if (getenv("TARGET") && !strcmp(getenv("TARGET"), "cubic")) for (int z = 0; z < N; z++){ int q = 0; for (int i = 0; i + 1 < K; i += 2) q ^= ((z >> i) & 1) & ((z >> (i + 1)) & 1); if (K == 6) q ^= ((z >> 0) & 1) & ((z >> 2) & 1) & ((z >> 4) & 1); g[z] = q ? -1 : 1; } }
static long long det3(long long m[3][3]){ return m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1]) - m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0]) + m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]); }
static long long det4(long long m[4][4]){
    long long d = 0;
    for (int c = 0; c < 4; c++){ long long s[3][3]; for (int i = 1; i < 4; i++){ int cc = 0; for (int j = 0; j < 4; j++) if (j != c) s[i-1][cc++] = m[i][j]; } d += ((c & 1) ? -1 : 1) * m[0][c] * det3(s); }
    return d;
}
static void exh(void){
    /* Gram matrix */
    int *G = malloc(sizeof(int) * (size_t)nf * nf), *b = malloc(sizeof(int) * nf);
    for (int i = 0; i < nf; i++){ int s = 0; for (int z = 0; z < N; z++) s += F[(size_t)i*N+z] * g[z]; b[i] = s;
        for (int j = 0; j < nf; j++){ int t = 0; for (int z = 0; z < N; z++) t += F[(size_t)i*N+z] * F[(size_t)j*N+z]; G[(size_t)i*nf+j] = t; } }
    long long gg = 0; for (int z = 0; z < N; z++) gg += g[z] * g[z];
    u64 full = (N == 64) ? ~0ULL : ((1ULL << N) - 1);
    long long n2 = 0, n3 = 0, n3u = 0, cov = 0; int shown = 0; long long bydims[5][5][5]; memset(bydims, 0, sizeof bydims);
    for (int i = 0; i < nf; i++) for (int j = i + 1; j < nf; j++){
        if (nocover || (fsup[i] | fsup[j]) == full){
            long long m[3][3] = {{G[(size_t)i*nf+i], G[(size_t)i*nf+j], b[i]}, {G[(size_t)i*nf+j], G[(size_t)j*nf+j], b[j]}, {b[i], b[j], gg}};
            if (det3(m) == 0) n2++;
        }
        for (int l = j + 1; l < nf; l++){
            if (!nocover && (fsup[i] | fsup[j] | fsup[l]) != full) continue; cov++;
            int id[3] = {i, j, l}; long long m[4][4];
            for (int x = 0; x < 3; x++){ for (int y = 0; y < 3; y++) m[x][y] = G[(size_t)id[x]*nf+id[y]]; m[x][3] = m[3][x] = b[id[x]]; } m[3][3] = gg;
            if (det4(m) != 0) continue;
            long long m3[3][3]; for (int x = 0; x < 3; x++) for (int y = 0; y < 3; y++) m3[x][y] = m[x][y];
            if (det3(m3) == 0) continue;      /* dependent triple: would be a 2-term case, counted above */
            n3++; int uns = !fneg[i] && !fneg[j] && !fneg[l]; n3u += uns; bydims[(int)fdm[i]][(int)fdm[j]][(int)fdm[l]]++;
            if (shown < 12){ shown++; printf("   3 signed flats: "); for (int x = 0; x < 3; x++) printf("[dim %d sup %llx neg %llx] ", fdm[id[x]], fsup[id[x]], fneg[id[x]]); printf("\n"); }
        }
    }
    printf("K=%d: %d signed flats (up to sign). pairs spanning g: %lld. covering triples: %lld. triples spanning g: %lld, of which unsigned: %lld\n", K, nf, n2, cov, n3, n3u);
    for (int x = 0; x <= K; x++) for (int y = 0; y <= K; y++) for (int z = 0; z <= K; z++) if (bydims[x][y][z]) printf("   dims (%d,%d,%d) in enumeration order: %lld\n", x, y, z, bydims[x][y][z]);
}
/* ---------- local search (floats) ---------- */
static double rnd(void){ return (double)rand() / ((double)RAND_MAX + 1.0); }
static double resid(int *sel, int r, int skip, double *Q, int *nq, double *pg){
    /* orthonormal basis Q of the span of the selected flats except slot 'skip'; pg = g projected off it; returns |pg|^2 */
    int q = 0;
    for (int x = 0; x < r; x++){ if (x == skip) continue; double v[64]; for (int z = 0; z < N; z++) v[z] = F[(size_t)sel[x]*N+z];
        for (int pass = 0; pass < 2; pass++) for (int y = 0; y < q; y++){ double c = 0; for (int z = 0; z < N; z++) c += v[z]*Q[y*64+z]; for (int z = 0; z < N; z++) v[z] -= c*Q[y*64+z]; }
        double n = 0; for (int z = 0; z < N; z++) n += v[z]*v[z]; if (n < 1e-9) continue; n = sqrt(n); for (int z = 0; z < N; z++) Q[q*64+z] = v[z]/n; q++; }
    *nq = q; double s = 0;
    for (int z = 0; z < N; z++) pg[z] = g[z];
    for (int y = 0; y < q; y++){ double c = 0; for (int z = 0; z < N; z++) c += pg[z]*Q[y*64+z]; for (int z = 0; z < N; z++) pg[z] -= c*Q[y*64+z]; }
    for (int z = 0; z < N; z++) s += pg[z]*pg[z]; return s;
}
static void ls(int r, double secs, int seed){
    srand(seed); clock_t t0 = clock(); int sel[64]; double Q[64*64], pg[64]; int nq; long long sweeps = 0, restarts = 0; double bestever = 1e9; int found = 0;
    while ((double)(clock() - t0) / CLOCKS_PER_SEC < secs){
        restarts++; for (int x = 0; x < r; x++) sel[x] = (int)(rnd() * nf);
        double cur = 1e9; int stall = 0;
        while (stall < 2 * r && (double)(clock() - t0) / CLOCKS_PER_SEC < secs){
            int slot = (int)(rnd() * r); double base = resid(sel, r, slot, Q, &nq, pg); sweeps++;
            /* best replacement for this slot */
            double bestv = 1e9; int bestl = -1, ties = 0;
            for (int l = 0; l < nf; l++){
                const signed char *f = F + (size_t)l * N; double ff = 0, gf = 0;
                for (int z = 0; z < N; z++){ ff += f[z] * f[z]; gf += f[z] * pg[z]; }
                for (int y = 0; y < nq; y++){ double c = 0; const double *qq = Q + y * 64; for (int z = 0; z < N; z++) c += f[z] * qq[z]; ff -= c * c; }
                if (ff < 1e-7) continue; double v = base - gf * gf / ff;
                if (v < bestv - 1e-9){ bestv = v; bestl = l; ties = 1; } else if (v < bestv + 1e-9){ ties++; if (rnd() * ties < 1) bestl = l; }
            }
            if (bestl < 0) break; sel[slot] = bestl;
            if (bestv < cur - 1e-9){ cur = bestv; stall = 0; } else stall++;
            if (cur < bestever){ bestever = cur; }
            if (cur < 1e-7){ found++; printf("CANDIDATE r=%d K=%d (floats, replay exactly):", r, K); for (int x = 0; x < r; x++) printf(" %llx:%llx", fsup[sel[x]], fneg[sel[x]]); printf("\n"); fflush(stdout); if (found >= 6) goto done; break; }
        }
    }
done:
    printf("ls K=%d r=%d flats=%d seed=%d: restarts %lld, slot optimisations %lld, candidates %d, least residual |.|^2 seen %.6f (g has |g|^2 = %d)\n", K, r, nf, seed, restarts, sweeps, found, bestever, N);
}
/* ls2: the same slot optimisation, but the replacement is drawn by a soft minimum (Gumbel noise of size tau on the residual), tau annealed
   from tau0 to 0 over 'steps' slot optimisations, then greedy until stalled; then restart.  FLOATS; candidates are replayed exactly elsewhere. */
static unsigned long long xs = 88172645463325252ULL;
static inline double urnd(void){ xs ^= xs << 13; xs ^= xs >> 7; xs ^= xs << 17; return ((xs >> 11) + 0.5) / 9007199254740992.0; }
static void ls2(int r, double secs, int seed, double tau0, int steps){
    xs ^= (unsigned long long)seed * 0x9E3779B97F4A7C15ULL; for (int i = 0; i < 20; i++) urnd();
    clock_t t0 = clock(); int sel[64]; double Q[64*64], pg[64]; int nq; long long sweeps = 0, restarts = 0; double bestever = 1e9; int found = 0;
    while ((double)(clock() - t0) / CLOCKS_PER_SEC < secs){
        restarts++; for (int x = 0; x < r; x++) sel[x] = (int)(urnd() * nf);
        int stall = 0; double cur = 1e9;
        for (int step = 0; stall < 3 * r && (double)(clock() - t0) / CLOCKS_PER_SEC < secs; step++){
            double tau = step < steps ? tau0 * (1.0 - (double)step / steps) : 0.0;
            int slot = (int)(urnd() * r); double base = resid(sel, r, slot, Q, &nq, pg); sweeps++;
            double bestv = 1e18, bestreal = 1e9; int bestl = -1;
            for (int l = 0; l < nf; l++){
                const signed char *f = F + (size_t)l * N; double ff = 0, gf = 0;
                for (int z = 0; z < N; z++){ ff += f[z] * f[z]; gf += f[z] * pg[z]; }
                for (int y = 0; y < nq; y++){ double c = 0; const double *qq = Q + y * 64; for (int z = 0; z < N; z++) c += f[z] * qq[z]; ff -= c * c; }
                if (ff < 1e-7) continue; double v = base - gf * gf / ff;
                double key = v + (tau > 0 ? tau * log(-log(urnd())) : 1e-9 * urnd());
                if (key < bestv){ bestv = key; bestl = l; bestreal = v; }
            }
            if (bestl < 0) break; sel[slot] = bestl;
            if (tau == 0){ if (bestreal < cur - 1e-9){ cur = bestreal; stall = 0; } else stall++; }
            if (bestreal < bestever) bestever = bestreal;
            if (bestreal < 1e-7){ found++; printf("CANDIDATE r=%d K=%d (floats, replay exactly):", r, K); for (int x = 0; x < r; x++) printf(" %llx:%llx", fsup[sel[x]], fneg[sel[x]]); printf("\n"); fflush(stdout); if (found >= 6) goto done; break; }
        }
    }
done:
    printf("ls2 K=%d r=%d flats=%d seed=%d tau0=%.2f steps=%d: restarts %lld, slot optimisations %lld, candidates %d, least residual |.|^2 seen %.6f (g has |g|^2 = %d)\n", K, r, nf, seed, tau0, steps, restarts, sweeps, found, bestever, N);
}
/* sym: decompositions with a symmetry.  h = an isometry of the quadratic form of prime order p (a random product of reflections
   z -> z + B(z,v) v, Q(v) = 1).  It permutes the signed flats.  Tested: g in span(one orbit of p flats + at most 2 invariant flats).
   FLOATS for the test; every hit is printed as a CANDIDATE and replayed exactly by verify.py. */
static int qd(int z){ int q = 0; for (int i = 0; i + 1 < K; i += 2) q ^= ((z >> i) & 1) & ((z >> (i + 1)) & 1); return q; }
static int *ordx;
static int cmpord(const void *a, const void *b){ int i = *(int*)a, j = *(int*)b; if (fsup[i] != fsup[j]) return fsup[i] < fsup[j] ? -1 : 1; if (fneg[i] != fneg[j]) return fneg[i] < fneg[j] ? -1 : 1; return 0; }
static int findflat(u64 sup, u64 neg){
    int low = __builtin_ctzll(sup); if ((neg >> low) & 1) neg = sup & ~neg;
    int lo = 0, hi = nf - 1;
    while (lo <= hi){ int mid = (lo + hi) / 2, i = ordx[mid];
        if (fsup[i] == sup && fneg[i] == neg) return i;
        if (fsup[i] < sup || (fsup[i] == sup && fneg[i] < neg)) lo = mid + 1; else hi = mid - 1; }
    return -1;
}
static void sym(int p, int seed, int maxinv){
    srand(seed); int perm[64], ns = 0, nsv[64]; for (int v = 1; v < N; v++) if (qd(v)) nsv[ns++] = v;
    for (;;){
        for (int z = 0; z < N; z++) perm[z] = z;
        int nr = 2 + rand() % 5;
        for (int t = 0; t < nr; t++){ int v = nsv[rand() % ns]; for (int z = 0; z < N; z++){ int y = perm[z]; int b = qd(y ^ v) ^ qd(y) ^ qd(v); perm[z] = b ? (y ^ v) : y; } }
        int cur[64], e = 0, id; for (int z = 0; z < N; z++) cur[z] = z;
        do { for (int z = 0; z < N; z++) cur[z] = perm[cur[z]]; e++; id = 1; for (int z = 0; z < N; z++) if (cur[z] != z) id = 0; } while (!id && e < 200);
        if (e == p) break;
    }
    int fixed = 0; for (int z = 0; z < N; z++) fixed += perm[z] == z;
    ordx = malloc(sizeof(int) * nf); for (int i = 0; i < nf; i++) ordx[i] = i; qsort(ordx, nf, sizeof(int), cmpord);
    int *img = malloc(sizeof(int) * nf);
    for (int i = 0; i < nf; i++){ u64 s2 = 0, n2 = 0; for (int z = 0; z < N; z++) if ((fsup[i] >> z) & 1){ s2 |= 1ULL << perm[z]; if ((fneg[i] >> z) & 1) n2 |= 1ULL << perm[z]; } img[i] = findflat(s2, n2); if (img[i] < 0){ printf("image not found\n"); return; } }
    int *inv = malloc(sizeof(int) * nf), ninv = 0; char *seen = calloc(nf, 1);
    for (int i = 0; i < nf; i++) if (img[i] == i) inv[ninv++] = i;
    printf("sym K=%d p=%d seed=%d: isometry of order %d with %d fixed points; %d signed flats, %d invariant, %d orbits of %d\n", K, p, seed, p, fixed, nf, ninv, (nf - ninv) / p, p);
    int ni = ninv < maxinv ? ninv : maxinv; if (ni < ninv) printf("   (only the first %d invariant flats are used for pairs)\n", ni);
    double *W = malloc(sizeof(double) * (size_t)ninv * 64), *ww = malloc(sizeof(double) * ninv), *gw = malloc(sizeof(double) * ninv);
    double Q[64*64], pg[64]; int nq; long long hits[4] = {0,0,0,0}, shown[4] = {0,0,0,0}; long long norb = 0;
    for (int i = 0; i < nf; i++){
        if (seen[i] || img[i] == i) continue; int orb[16], no = 0, j = i; do { orb[no++] = j; seen[j] = 1; j = img[j]; } while (j != i && no < 16);
        norb++; double base = resid(orb, no, -1, Q, &nq, pg);
        if (base < 1e-7){ hits[0]++; if (shown[0]++ < 3){ printf("CANDIDATE r=%d K=%d (floats, replay exactly):", no, K); for (int x = 0; x < no; x++) printf(" %llx:%llx", fsup[orb[x]], fneg[orb[x]]); printf("\n"); } continue; }
        for (int a = 0; a < ninv; a++){ double *w = W + (size_t)a * 64; const signed char *f = F + (size_t)inv[a] * N; for (int z = 0; z < N; z++) w[z] = f[z];
            for (int y = 0; y < nq; y++){ double c = 0; const double *qq = Q + y * 64; for (int z = 0; z < N; z++) c += w[z] * qq[z]; for (int z = 0; z < N; z++) w[z] -= c * qq[z]; }
            double s1 = 0, s2 = 0; for (int z = 0; z < N; z++){ s1 += w[z] * w[z]; s2 += w[z] * pg[z]; } ww[a] = s1; gw[a] = s2;
            if (s1 > 1e-7 && base - s2 * s2 / s1 < 1e-7){ hits[1]++; if (shown[1]++ < 4){ printf("CANDIDATE r=%d K=%d (floats, replay exactly):", no + 1, K); for (int x = 0; x < no; x++) printf(" %llx:%llx", fsup[orb[x]], fneg[orb[x]]); printf(" %llx:%llx\n", fsup[inv[a]], fneg[inv[a]]); } } }
        for (int a = 0; a < ni; a++) for (int b = a + 1; b < ni; b++){
            const double *wa = W + (size_t)a * 64, *wb = W + (size_t)b * 64; double ab = 0; for (int z = 0; z < N; z++) ab += wa[z] * wb[z];
            double det = ww[a] * ww[b] - ab * ab; if (det < 1e-7) continue;
            double res = base - (gw[a] * gw[a] * ww[b] - 2 * gw[a] * gw[b] * ab + gw[b] * gw[b] * ww[a]) / det;
            if (res < 1e-7){ hits[2]++; if (shown[2]++ < 6){ printf("CANDIDATE r=%d K=%d (floats, replay exactly):", no + 2, K); for (int x = 0; x < no; x++) printf(" %llx:%llx", fsup[orb[x]], fneg[orb[x]]); printf(" %llx:%llx %llx:%llx\n", fsup[inv[a]], fneg[inv[a]], fsup[inv[b]], fneg[inv[b]]); } } }
    }
    printf("sym K=%d p=%d: %lld orbits tested. g in span(orbit): %lld ; orbit + 1 invariant flat: %lld ; orbit + 2 invariant flats: %lld   (flats: %d, %d, %d)\n", K, p, norb, hits[0], hits[1], hits[2], p, p + 1, p + 2);
}
/* sym2: two orbits of an isometry h of prime order p, plus at most one invariant flat.  Since g is invariant under h, g lies in the span of
   the flats iff it lies in the span of the ORBIT SUMS and the invariant flats.  EXACT: integer Gram determinants.  part/nparts splits the work. */
static void sym2(int p, int seed, int part, int nparts){
    srand(seed); int perm[64], ns = 0, nsv[64]; for (int v = 1; v < N; v++) if (qd(v)) nsv[ns++] = v;
    for (;;){
        for (int z = 0; z < N; z++) perm[z] = z;
        int nr = 2 + rand() % 5;
        for (int t = 0; t < nr; t++){ int v = nsv[rand() % ns]; for (int z = 0; z < N; z++){ int y = perm[z]; int b = qd(y ^ v) ^ qd(y) ^ qd(v); perm[z] = b ? (y ^ v) : y; } }
        int cur[64], e = 0, id; for (int z = 0; z < N; z++) cur[z] = z;
        do { for (int z = 0; z < N; z++) cur[z] = perm[cur[z]]; e++; id = 1; for (int z = 0; z < N; z++) if (cur[z] != z) id = 0; } while (!id && e < 200);
        if (e == p) break;
    }
    ordx = malloc(sizeof(int) * nf); for (int i = 0; i < nf; i++) ordx[i] = i; qsort(ordx, nf, sizeof(int), cmpord);
    int *img = malloc(sizeof(int) * nf);
    for (int i = 0; i < nf; i++){ u64 s2 = 0, n2 = 0; for (int z = 0; z < N; z++) if ((fsup[i] >> z) & 1){ s2 |= 1ULL << perm[z]; if ((fneg[i] >> z) & 1) n2 |= 1ULL << perm[z]; } img[i] = findflat(s2, n2); }
    char *seen = calloc(nf, 1); int norb = 0, ninv = 0; int *first = malloc(sizeof(int) * nf), *inv = malloc(sizeof(int) * nf);
    for (int i = 0; i < nf; i++){ if (img[i] == i){ inv[ninv++] = i; continue; } if (seen[i]) continue; int j = i; do { seen[j] = 1; j = img[j]; } while (j != i); first[norb++] = i; }
    signed char *S = malloc((size_t)norb * 64); u64 *mk = malloc(8 * (size_t)norb); int *nn = malloc(4 * (size_t)norb), *bb = malloc(4 * (size_t)norb);
    int *sa = malloc(sizeof(int) * (size_t)norb * (ninv ? ninv : 1));
    for (int o = 0; o < norb; o++){ int v[64], w[64]; for (int z = 0; z < N; z++){ v[z] = F[(size_t)first[o] * N + z]; w[z] = v[z]; }
        for (int t = 1; t < p; t++){ int u[64]; for (int z = 0; z < N; z++) u[perm[z]] = w[z]; for (int z = 0; z < N; z++){ w[z] = u[z]; v[z] += u[z]; } }
        u64 m = 0; int n = 0, b = 0; for (int z = 0; z < N; z++){ S[(size_t)o * 64 + z] = (signed char)v[z]; if (v[z]) m |= 1ULL << z; n += v[z] * v[z]; b += v[z] * g[z]; }
        mk[o] = m; nn[o] = n; bb[o] = b;
        for (int a = 0; a < ninv; a++){ int t = 0; for (int z = 0; z < N; z++) t += v[z] * F[(size_t)inv[a] * N + z]; sa[(size_t)o * ninv + a] = t; } }
    int aa[4096], ga[4096]; u64 ma[4096]; for (int a = 0; a < ninv && a < 4096; a++){ aa[a] = popc(fsup[inv[a]]); ma[a] = fsup[inv[a]]; int t = 0; for (int z = 0; z < N; z++) t += F[(size_t)inv[a] * N + z] * g[z]; ga[a] = t; }
    u64 full = (N == 64) ? ~0ULL : ((1ULL << N) - 1); long long h2 = 0, h3 = 0, tested2 = 0, tested3 = 0;
    int ninvuse = getenv("NOINV") ? 0 : ninv;
    fprintf(stderr, "sym2 K=%d p=%d: %d orbits, %d invariant flats, part %d of %d\n", K, p, norb, ninv, part, nparts);
    for (int i = part; i < norb; i += nparts) for (int j = i + 1; j < norb; j++){
        u64 m = mk[i] | mk[j]; int have = 0; long long ip = 0;
        if (m == full){ const signed char *x = S + (size_t)i * 64, *y = S + (size_t)j * 64; for (int z = 0; z < N; z++) ip += x[z] * y[z]; have = 1; tested2++;
            long long m3[3][3] = {{nn[i], ip, bb[i]}, {ip, nn[j], bb[j]}, {bb[i], bb[j], N}};
            if (det3(m3) == 0 && (long long)nn[i] * nn[j] - ip * ip != 0){ h2++; if (h2 <= 6){ printf("CANDIDATE r=%d K=%d (floats, replay exactly):", 2 * p, K); for (int o = 0; o < 2; o++){ int f0 = first[o ? j : i], f = f0; do { printf(" %llx:%llx", fsup[f], fneg[f]); f = img[f]; } while (f != f0); } printf("\n"); fflush(stdout); } } }
        for (int a = 0; a < ninvuse; a++){
            if ((m | ma[a]) != full) continue;
            if (!have){ const signed char *x = S + (size_t)i * 64, *y = S + (size_t)j * 64; for (int z = 0; z < N; z++) ip += x[z] * y[z]; have = 1; }
            tested3++; long long ia = sa[(size_t)i * ninv + a], ja = sa[(size_t)j * ninv + a];
            long long m4[4][4] = {{nn[i], ip, ia, bb[i]}, {ip, nn[j], ja, bb[j]}, {ia, ja, aa[a], ga[a]}, {bb[i], bb[j], ga[a], N}};
            if (det4(m4) != 0) continue;
            long long m3[3][3] = {{nn[i], ip, ia}, {ip, nn[j], ja}, {ia, ja, aa[a]}}; if (det3(m3) == 0) continue;
            h3++; if (h3 <= 6){ printf("CANDIDATE r=%d K=%d (floats, replay exactly):", 2 * p + 1, K); for (int o = 0; o < 2; o++){ int f0 = first[o ? j : i], f = f0; do { printf(" %llx:%llx", fsup[f], fneg[f]); f = img[f]; } while (f != f0); } printf(" %llx:%llx\n", fsup[inv[a]], fneg[inv[a]]); fflush(stdout); }
        }
    }
    printf("sym2 K=%d p=%d seed=%d part %d/%d: %d orbits, %d invariant flats. two orbits (%d flats): %lld covering pairs tested exactly, %lld span g ; two orbits + 1 invariant flat (%d flats): %lld covering triples tested exactly, %lld span g\n", K, p, seed, part, nparts, norb, ninv, 2 * p, tested2, h2, 2 * p + 1, tested3, h3);
}
/* rs: free row and column signs.  The K bits are (x, y): x = bits 0,2,4,..., y = bits 1,3,5,...; g(z) = H(x,y).
   Is there a set E with  (1 - 2 [z in E]) = a(x) H(x,y) b(y)  for some sign vectors a, b, where E is one flat (2 flats with the constant),
   or built from two flats F1, F2 so that 1 - 2[E] is a combination of the constant and two SIGNED flats: E = F1 + F2 (disjoint),
   E = F1 minus F2 (nested), E = F1 xor F2 (the intersection is half of one of them)?   EXACT (bit masks).  Run with 'unsigned'. */
static void rs(void){
    u64 gneg = 0, xm = 0, ym = 0; for (int z = 0; z < N; z++) if (g[z] < 0) gneg |= 1ULL << z;
    for (int i = 0; i < K; i += 2){ xm |= 1ULL << i; ym |= 1ULL << (i + 1); }
    int zx[64], zy[64]; for (int z = 0; z < N; z++){ zx[z] = z & (int)xm; zy[z] = z & (int)ym; }
    long long h1 = 0, h2 = 0, t2 = 0; int shown = 0;
    #define RANK1(E, res) { u64 m = (E) ^ gneg; int okk = 1; int b0 = (int)(m & 1); for (int z = 0; z < N && okk; z++) if ((((m >> z) ^ (m >> zx[z]) ^ (m >> zy[z])) & 1) != b0) okk = 0; res = okk; }
    for (int i = 0; i < nf; i++){ int r1; RANK1(fsup[i], r1); if (r1){ h1++; if (shown < 6){ shown++; printf("   one flat E = %llx (dim %d): 1 - 2[E] is a sign-rescaled transform\n", fsup[i], fdm[i]); } } }
    shown = 0;
    for (int i = 0; i < nf; i++) for (int j = i + 1; j < nf; j++){
        u64 A = fsup[i], B = fsup[j], I = A & B, E; int ok = 0;
        if (!I){ E = A | B; ok = 1; }
        else if (I == B){ E = A & ~B; ok = 1; }
        else if (I == A){ E = B & ~A; ok = 1; }
        else if (2 * popc(I) == popc(A) || 2 * popc(I) == popc(B)){ E = A ^ B; ok = 1; }
        if (!ok) continue; t2++; int r1; RANK1(E, r1);
        if (r1){ h2++; if (shown < 8){ shown++; printf("   two flats %llx (dim %d), %llx (dim %d), E = %llx (%d points): 1 - 2[E] is a sign-rescaled transform\n", A, fdm[i], B, fdm[j], E, popc(E)); fflush(stdout); } }
    }
    printf("rs K=%d (N=%d points, doubled): %d unsigned flats. E = one flat: %lld hits. E from two flats: %lld sets tested, %lld hits\n", K, 1 << (K / 2), nf, h1, t2, h2);
    /* case B-i of the report: two complementary half-spaces with any signs, P = (-1)^(l l'), times (1 - 2 [F3]) for any flat F3 */
    long long t3 = 0, h3 = 0, h3aff = 0; shown = 0;
    for (int u = 1; u < N; u++) for (int v = u + 1; v < N; v++){
        u64 pneg = 0; for (int z = 0; z < N; z++) if ((popc((u64)(u & z)) & 1) && (popc((u64)(v & z)) & 1)) pneg |= 1ULL << z;
        for (int i = 0; i < nf; i++){ int r1; t3++; RANK1(fsup[i] ^ pneg, r1); if (r1){ h3++;
            { int w[3] = {u, v, u ^ v}; int aff = 0; for (int q = 0; q < 3; q++){ int c0 = -1, cst = 1; for (int z = 0; z < N && cst; z++) if ((fsup[i] >> z) & 1){ int b = popc((u64)(w[q] & z)) & 1; if (c0 < 0) c0 = b; else if (b != c0) cst = 0; } if (cst) aff = 1; }
              if (aff){ h3aff++; if (h3aff <= 6) printf("   THREE FLATS: l = %x, l' = %x, F3 = %llx (dim %d), (-1)^(l l') is a signed constant on F3\n", u, v, fsup[i], fdm[i]); } }
            if (shown < 2){ shown++; printf("   l = %x, l' = %x, F3 = %llx (dim %d): (-1)^(l l') (1 - 2[F3]) is a sign-rescaled transform\n", u, v, fsup[i], fdm[i]); } } }
        { int r1; t3++; RANK1(pneg, r1); if (r1) printf("   (-1)^(l l') itself is a sign-rescaled transform: l = %x l' = %x\n", u, v); }
    }
    printf("rs K=%d: (-1)^(l l') (1 - 2 [F3]) over all pairs of linear forms and all flats: %lld tested, %lld hits (4 flats in general), of which with (-1)^(l l') a signed constant on F3 (3 flats): %lld\n", K, t3, h3, h3aff);
}
int main(int argc, char **argv){
    K = atoi(argv[1]); N = 1 << K; gen_subs(); int uns = (argc > 6 && !strcmp(argv[6], "unsigned")) || (argc > 3 && !strcmp(argv[argc-1], "unsigned"));
    gen_flats(uns); target(); nocover = getenv("TARGET") != NULL;
    fprintf(stderr, "K=%d subspaces %d flats %d (%s)\n", K, nsub, nf, uns ? "unsigned" : "signed");
    if (!strcmp(argv[2], "exh")) exh();
    else if (!strcmp(argv[2], "ls")) ls(atoi(argv[3]), atof(argv[4]), atoi(argv[5]));
    else if (!strcmp(argv[2], "sym")) sym(atoi(argv[3]), atoi(argv[4]), argc > 5 ? atoi(argv[5]) : 400);
    else if (!strcmp(argv[2], "sym2")) sym2(atoi(argv[3]), atoi(argv[4]), atoi(argv[5]), atoi(argv[6]));
    else if (!strcmp(argv[2], "rs")) rs();
    else if (!strcmp(argv[2], "ls2")) ls2(atoi(argv[3]), atof(argv[4]), atoi(argv[5]), atof(argv[6]), atoi(argv[7]));
    return 0;
}
