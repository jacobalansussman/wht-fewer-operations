// x-2-floorhatch/hatch.c : the "form game" of u-9 with ONE hatch open.  Count (G): a gate is any a*u + b*v.
// A circuit is kept as its SET of wires (primitive whole-number vectors up to sign).  A wire is derivable when it lies in the
// span of two derivable wires (the inputs are derivable).  A set of W wires that contains the N rows of the transform and is
// derivable to the last wire is a circuit of W gates.  The annealer moves one wire at a time and minimises the number of
// wires that are not derivable.  A search is no proof that a count is impossible.
// usage: hatch N mode W iters seed [seedfile [starting temperature, default 1.2]]
//   mode 0 T : sign vectors on the nodes of the cube tree (the class of the floor theorem; floor N - 1 + (N/2) log2 N)
//   mode 1 A : sign vectors on ANY coset of ANY subspace            (hatch a: sets that cross the tree, still affine)
//   mode 2 C : sign vectors on tree nodes and on three quarters of a tree node   (hatch c: non-affine sets)
//   mode 3 S : sign vectors on any set                              (a and c together)
//   mode 4 D : +-1 on a tree node, 0 or +-2 anywhere outside it      (hatch b: dirty wires)
//   mode 5 E : any primitive vector with entries 0, +-1, +-2
//   mode 6 F : any primitive vector with entries of size at most 3
// seedfile: lines of N whole numbers (wires of a known circuit, already in the standard address order); extras are dropped at random.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#define MAXN 16
#define MAXM 128
typedef struct { signed char e[MAXN]; unsigned supp; } vec;
static int N, K, mode, W, M;
static uint64_t rs = 88172645463325252ULL;
static inline uint64_t rnd(void){ rs ^= rs<<13; rs ^= rs>>7; rs ^= rs<<17; return rs; }
static inline double urand(void){ return (rnd()>>11) * (1.0/9007199254740992.0); }
static unsigned char *affine;
static unsigned blockmask(int s, int st){ return ((s >= 32) ? ~0u : ((1u<<s)-1u)) << st; }
static int istree(unsigned m){
  if(!m) return 0; int cnt = __builtin_popcount(m); if(cnt & (cnt-1)) return 0;
  int lo = __builtin_ctz(m); if(lo % cnt) return 0; return m == blockmask(cnt, lo);
}
static int is34(unsigned m){
  int cnt = __builtin_popcount(m); if(cnt % 3) return 0; int q = cnt/3; if(q < 1 || (q & (q-1))) return 0;
  int s = 4*q; if(s > N) return 0;
  for(int st = 0; st < N; st += s){ unsigned node = blockmask(s, st); if((m & ~node) == 0){ unsigned miss = node & ~m; return istree(miss) && __builtin_popcount(miss) == q; } }
  return 0;
}
static int gcd(int a, int b){ a = abs(a); b = abs(b); while(b){ int t = a % b; a = b; b = t; } return a; }
// normalise an int vector into a vec; return 0 if zero or out of the pool
static int mk(const int *w, vec *out){
  int g = 0; for(int i = 0; i < N; i++) g = gcd(g, w[i]); if(!g) return 0;
  int sg = 0; unsigned supp = 0, odd = 0; int mx = 0;
  for(int i = 0; i < N; i++){ int t = w[i]/g; if(!sg && t) sg = t > 0 ? 1 : -1; t *= sg ? sg : 1; if(abs(t) > 3) return 0; out->e[i] = (signed char)t; if(t) supp |= 1u<<i; if(t & 1) odd |= 1u<<i; if(abs(t) > mx) mx = abs(t); }
  out->supp = supp;
  switch(mode){
    case 0: return mx == 1 && istree(supp);
    case 1: return mx == 1 && affine[supp];
    case 2: return mx == 1 && (istree(supp) || is34(supp));
    case 3: return mx == 1;
    case 4: if(mx > 2) return 0; for(int i = 0; i < N; i++) if(abs(out->e[i]) == 2 && 0) return 0; return istree(odd);
    case 5: return mx <= 2;
    case 6: return mx <= 3;
  }
  return 0;
}
static vec H[MAXM];
static int spans(const vec *u, const vec *v, const vec *w){   // is w in the span of u and v (u, v, w pairwise not proportional)?
  unsigned su = u->supp, sv = v->supp, sw = w->supp;
  if((sw & ~(su | sv)) || (su & ~(sv | sw)) || (sv & ~(su | sw))) return 0;
  int i = __builtin_ctz(su), j = -1, d = 0;
  for(int t = 0; t < N; t++){ d = u->e[i]*v->e[t] - u->e[t]*v->e[i]; if(d){ j = t; break; } }
  if(j < 0) return 0;
  int a = w->e[i]*v->e[j] - w->e[j]*v->e[i], b = u->e[i]*w->e[j] - u->e[j]*w->e[i];
  for(int t = 0; t < N; t++) if(d*w->e[t] != a*u->e[t] + b*v->e[t]) return 0;
  return 1;
}
typedef struct { uint64_t a, b; } bits;
static bits rel[MAXM][MAXM];     // rel[w][u] = set of v with w in span(u, v)
static inline void setb(bits *x, int i){ if(i < 64) x->a |= 1ULL<<i; else x->b |= 1ULL<<(i-64); }
static inline void clrb(bits *x, int i){ if(i < 64) x->a &= ~(1ULL<<i); else x->b &= ~(1ULL<<(i-64)); }
static inline int getb(const bits *x, int i){ return i < 64 ? (x->a>>i)&1 : (x->b>>(i-64))&1; }
static void refresh(int i){      // recompute every relation that involves wire i
  for(int w = 0; w < M; w++){ rel[w][i].a = rel[w][i].b = 0; rel[i][w].a = rel[i][w].b = 0; for(int u = 0; u < M; u++) clrb(&rel[w][u], i); }
  for(int u = 0; u < M; u++) if(u != i) for(int v = u+1; v < M; v++) if(v != i && spans(&H[u], &H[v], &H[i])){ setb(&rel[i][u], v); setb(&rel[i][v], u); }
  for(int w = N; w < M; w++) if(w != i) for(int u = 0; u < M; u++) if(u != i && u != w && spans(&H[i], &H[u], &H[w])){ setb(&rel[w][i], u); setb(&rel[w][u], i); }
}
static int par[MAXM][2], ord[MAXM], nord;
static int cost(int record){
  bits D = {0, 0}; for(int i = 0; i < N; i++) setb(&D, i);
  int done = N, prog = 1; nord = 0;
  while(prog && done < M){
    prog = 0;
    for(int w = N; w < M; w++) if(!getb(&D, w)){
      for(int u = 0; u < M; u++) if(getb(&D, u)){
        uint64_t x = rel[w][u].a & D.a, y = rel[w][u].b & D.b;
        if(x | y){ if(record){ par[w][0] = u; par[w][1] = x ? __builtin_ctzll(x) : 64 + __builtin_ctzll(y); ord[nord++] = w; } setb(&D, w); done++; prog = 1; break; }
      }
    }
  }
  return M - done;
}
static int same(const vec *a, const vec *b){ return a->supp == b->supp && !memcmp(a->e, b->e, N); }
static int held(const vec *x){ for(int i = 0; i < M; i++) if(same(&H[i], x)) return 1; return 0; }
static int randpool(vec *out){
  int w[MAXN];
  for(int tries = 0; tries < 200; tries++){
    if(mode == 0 || mode == 2 || mode == 4){
      int lev = 1 + rnd() % K; int s = 1 << lev; int st = (rnd() % (N/s)) * s;
      for(int i = 0; i < N; i++) w[i] = (i >= st && i < st+s) ? ((rnd()&1) ? 1 : -1) : 0;
      if(mode == 2 && s >= 4 && (rnd() & 1)){ int q = s/4, c = rnd() % 4; for(int i = st + c*q; i < st + (c+1)*q; i++) w[i] = 0; }
      if(mode == 4 && (rnd() & 1)){ int lev2 = rnd() % (K+1); int s2 = 1 << lev2; int st2 = (rnd() % (N/s2)) * s2; for(int i = st2; i < st2+s2; i++) if(!w[i]) w[i] = (rnd()&1) ? 2 : -2; }
    } else if(mode == 1){
      unsigned m; do { m = rnd() & ((1u<<N)-1); } while(!affine[m] || __builtin_popcount(m) < 2);
      for(int i = 0; i < N; i++) w[i] = (m>>i & 1) ? ((rnd()&1) ? 1 : -1) : 0;
    } else {
      int mx = mode == 3 ? 1 : (mode == 5 ? 2 : 3);
      for(int i = 0; i < N; i++) w[i] = (int)(rnd() % (2*mx+1)) - mx;
    }
    if(mk(w, out) && __builtin_popcount(out->supp) > 1) return 1;
  }
  return 0;
}
static const int CA[12] = {1, 1, 1, 1, 2, 2, 1, 1, 3, 3, 1, 1}, CB[12] = {1, -1, 2, -2, 1, -1, 3, -3, 1, -1, 4, -4};
static int propose(vec *out){
  int w[MAXN]; double r = urand();
  for(int tries = 0; tries < 50; tries++){
    if(r < 0.55){            // a combination of two held wires
      int u = rnd() % M, v = rnd() % M; if(u == v) continue; int c = rnd() % (mode >= 4 ? 12 : 6);
      for(int i = 0; i < N; i++) w[i] = CA[c]*H[u].e[i] + CB[c]*H[v].e[i];
      if(mk(w, out) && __builtin_popcount(out->supp) > 1 && !held(out)) return 1;
    } else if(r < 0.85){     // a held wire cut down to, or flipped on, a block or a hyperplane; or one entry changed
      int u = N + rnd() % (M - N); for(int i = 0; i < N; i++) w[i] = H[u].e[i];
      int what = rnd() % 5; unsigned m;
      if(what < 2){ int lev = rnd() % K; int s = 1 << lev; int st = (rnd() % (N/s)) * s; m = blockmask(s, st); }
      else if(what < 4){ unsigned y = 1 + rnd() % (N-1); m = 0; for(int x = 0; x < N; x++) if(__builtin_popcount(x & y) & 1) m |= 1u<<x; if(rnd()&1) m = ~m & ((1u<<N)-1); if(rnd()&1){ unsigned y2 = 1 + rnd() % (N-1); for(int x = 0; x < N; x++) if(__builtin_popcount(x & y2) & 1) m &= ~(1u<<x); } }
      else m = 1u << (rnd() % N);
      int op = rnd() % 4;
      for(int i = 0; i < N; i++) if(m>>i & 1){ if(op == 0) w[i] = -w[i]; else if(op == 1) w[i] = 0; else if(op == 2 && mode >= 4) w[i] = w[i] ? 0 : 2; } else if(op == 3) w[i] = 0;
      if(mk(w, out) && __builtin_popcount(out->supp) > 1 && !held(out)) return 1;
    } else { if(randpool(out) && !held(out)) return 1; }
  }
  return 0;
}
int main(int argc, char **argv){
  if(argc < 6){ fprintf(stderr, "usage: hatch N mode W iters seed [seedfile]\n"); return 2; }
  N = atoi(argv[1]); mode = atoi(argv[2]); W = atoi(argv[3]); long iters = atol(argv[4]); rs ^= (uint64_t)atol(argv[5]) * 0x9E3779B97F4A7C15ULL; for(int i = 0; i < 20; i++) rnd();
  K = 0; while((1 << K) < N) K++; M = N + W; if(M > MAXM){ fprintf(stderr, "too many wires\n"); return 2; }
  affine = calloc(1u << N, 1);
  for(int dim = 0; dim <= K; dim++){ }
  { // every coset of every subspace: grow subspaces by closure
    unsigned char *sub = calloc(1u << N, 1); unsigned *list = malloc(sizeof(unsigned) * 70000); int nl = 0;
    sub[1] = 1; list[nl++] = 1;   // the zero subspace {0}
    for(int t = 0; t < nl; t++){ unsigned V = list[t];
      for(int x = 1; x < N; x++) if(!(V>>x & 1)){ unsigned V2 = V; for(int y = 0; y < N; y++) if(V>>y & 1) V2 |= 1u << (y ^ x); if(!sub[V2]){ sub[V2] = 1; list[nl++] = V2; } } }
    for(int t = 0; t < nl; t++){ unsigned V = list[t]; for(int x = 0; x < N; x++){ unsigned C = 0; for(int y = 0; y < N; y++) if(V>>y & 1) C |= 1u << (y ^ x); affine[C] = 1; } }
    free(sub); free(list);
  }
  int w[MAXN]; double T0 = argc > 7 ? atof(argv[7]) : 1.2;
  for(int i = 0; i < N; i++){ for(int j = 0; j < N; j++) w[j] = (i == j); int sv = mode; mode = 6; mk(w, &H[i]); mode = sv; }
  for(int y = 0; y < N; y++){ for(int x = 0; x < N; x++) w[x] = (__builtin_popcount(x & y) & 1) ? -1 : 1; int sv = mode; mode = 6; mk(w, &H[N+y]); mode = sv; }
  int have = 2*N;
  if(argc > 6){
    FILE *f = fopen(argv[6], "r"); if(!f){ fprintf(stderr, "no seed file\n"); return 2; }
    vec cand[400]; int nc = 0; char line[4096];
    while(fgets(line, sizeof line, f)){ if(line[0] == '#') continue; char *p = line; int ok = 1; for(int i = 0; i < N; i++){ char *q; long t = strtol(p, &q, 10); if(q == p){ ok = 0; break; } w[i] = (int)t; p = q; }
      if(!ok) continue; vec x; if(!mk(w, &x)){ fprintf(stderr, "seed wire outside the pool of this mode, skipped\n"); continue; } if(__builtin_popcount(x.supp) < 2) continue; int dup = 0; for(int i = 0; i < 2*N; i++) if(same(&H[i], &x)) dup = 1; for(int i = 0; i < nc; i++) if(same(&cand[i], &x)) dup = 1; if(!dup && nc < 400) cand[nc++] = x; }
    fclose(f);
    while(nc > W - N){ int i = rnd() % nc; cand[i] = cand[--nc]; }
    for(int i = 0; i < nc; i++) H[have++] = cand[i];
  }
  while(have < M){ vec x; if(randpool(&x)){ int dup = 0; for(int i = 0; i < have; i++) if(same(&H[i], &x)) dup = 1; if(!dup) H[have++] = x; } }
  for(int i = 0; i < M; i++) refresh(i);
  int cv = cost(0), best = cv; long it = 0;
  for(it = 0; it < iters && cv > 0; it++){
    double T = T0 * (1.0 - (double)it / iters) + 0.05;
    int i = 2*N + rnd() % (M - 2*N); vec nw; if(!propose(&nw)) continue;
    vec old = H[i]; H[i] = nw; refresh(i); int v = cost(0);
    if(v <= cv || urand() < exp((cv - v) / T)) cv = v; else { H[i] = old; refresh(i); }
    if(cv < best) best = cv;
  }
  printf("N=%d mode=%d W=%d seed=%s: least number of underivable wires %d after %ld moves\n", N, mode, W, argv[5], best, it);
  if(cv == 0){
    cost(1);
    printf("CIRCUIT %d gates (wire : entries : made from wires a, b ; inputs are 0..%d)\n", W, N-1);
    for(int t = 0; t < nord; t++){ int x = ord[t]; printf("w %d :", x); for(int i = 0; i < N; i++) printf(" %d", H[x].e[i]); printf(" : %d %d\n", par[x][0], par[x][1]); }
  }
  return 0;
}
