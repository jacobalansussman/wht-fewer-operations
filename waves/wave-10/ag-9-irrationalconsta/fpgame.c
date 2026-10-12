// ag-9 fpgame.c : the "form game" of x-2/hatch.c with wires and coefficients in the field of whole numbers modulo a prime p.
// Count (G): a gate is any a*u + b*v, scalings free, so a wire is a projective point (first non-zero entry scaled to 1).
// A set of W wires that contains the N rows of the transform (reduced modulo p) and in which every wire lies on the line
// through two wires derived before it is a circuit of W gates over GF(p).  The annealer moves one helper at a time and
// minimises the number of wires not derivable.  A hit is a CANDIDATE (to be lifted to a ring and replayed exactly);
// "none found" is an annealer's result, not a proof.
// usage: fpgame p N W iters seed T0 pool [seedfile]
//   pool 2: half the proposals as pool 1, half as pool 0 (keeps the walk near the known circuits);
//   pool 0: coefficients any non-zero residue; 1: coefficients only +-1, +-2, +-1/2 (control, the rational small pool)
//   seedfile: lines of N whole numbers (helpers of a known circuit); extras are dropped at random
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#define MAXN 16
#define MAXM 128
typedef struct { unsigned char e[MAXN]; unsigned supp; } vec;
static int p, N, K, W, M, pool;
static int inv[256];
static uint64_t rs = 88172645463325252ULL;
static inline uint64_t rnd(void){ rs ^= rs<<13; rs ^= rs>>7; rs ^= rs<<17; return rs; }
static inline double urand(void){ return (rnd()>>11) * (1.0/9007199254740992.0); }
static int mk(const int *w, vec *out){            // normalise; 0 if zero vector
  int lead = 0; unsigned supp = 0;
  for(int i = 0; i < N; i++){ int t = ((w[i] % p) + p) % p; if(!lead && t) lead = inv[t]; t = (t * (lead ? lead : 1)) % p; out->e[i] = (unsigned char)t; if(t) supp |= 1u<<i; }
  out->supp = supp; return supp != 0;
}
static vec H[MAXM];
static int spans(const vec *u, const vec *v, const vec *w){
  unsigned su = u->supp, sv = v->supp, sw = w->supp;
  if((sw & ~(su | sv)) || (su & ~(sv | sw)) || (sv & ~(su | sw))) return 0;
  int i = __builtin_ctz(su), j = -1, d = 0;
  for(int t = 0; t < N; t++){ d = (u->e[i]*v->e[t] - u->e[t]*v->e[i]) % p; if(d){ j = t; break; } }
  if(j < 0) return 0;
  int a = (w->e[i]*v->e[j] - w->e[j]*v->e[i]) % p, b = (u->e[i]*w->e[j] - u->e[j]*w->e[i]) % p;
  if(a == 0 || b == 0) return 0;
  for(int t = 0; t < N; t++) if((d*w->e[t] - a*u->e[t] - b*v->e[t]) % p) return 0;
  return 1;
}
typedef struct { uint64_t a, b; } bits;
static bits rel[MAXM][MAXM];
static inline void setb(bits *x, int i){ if(i < 64) x->a |= 1ULL<<i; else x->b |= 1ULL<<(i-64); }
static inline void clrb(bits *x, int i){ if(i < 64) x->a &= ~(1ULL<<i); else x->b &= ~(1ULL<<(i-64)); }
static inline int getb(const bits *x, int i){ return i < 64 ? (x->a>>i)&1 : (x->b>>(i-64))&1; }
static void refresh(int i){
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
static int rcoef(void){
  if(pool == 1){ static int c6[6]; c6[0] = 1; c6[1] = p-1; c6[2] = 2; c6[3] = p-2; c6[4] = inv[2]; c6[5] = p - inv[2]; return c6[rnd() % 6]; }
  if(pool == 2 && (rnd() & 1)){ int c6[6] = {1, p-1, 2, p-2, inv[2], p - inv[2]}; return c6[rnd() % 6]; }
  return 1 + rnd() % (p-1);
}
static int rentry(void){   // a random entry: half the time 0, +1, -1; else anything
  int r = rnd() % 8; if(r < 2) return 0; if(r < 4) return 1; if(r < 6) return p-1; return rnd() % p;
}
static unsigned blockmask(int s, int st){ return ((s >= 32) ? ~0u : ((1u<<s)-1u)) << st; }
static int propose(vec *out){
  int w[MAXN]; double r = urand();
  for(int tries = 0; tries < 50; tries++){
    if(r < 0.55){
      int u = rnd() % M, v = rnd() % M; if(u == v) continue; int c = rcoef();
      for(int i = 0; i < N; i++) w[i] = H[u].e[i] + c*H[v].e[i];
      if(mk(w, out) && __builtin_popcount(out->supp) > 1 && !held(out)) return 1;
    } else if(r < 0.88){
      int u = N + rnd() % (M - N); for(int i = 0; i < N; i++) w[i] = H[u].e[i];
      int what = rnd() % 5; unsigned m;
      if(what < 2){ int lev = rnd() % K; int s = 1 << lev; int st = (rnd() % (N/s)) * s; m = blockmask(s, st); }
      else if(what < 4){ unsigned y = 1 + rnd() % (N-1); m = 0; for(int x = 0; x < N; x++) if(__builtin_popcount(x & y) & 1) m |= 1u<<x; if(rnd()&1) m = ~m & ((1u<<N)-1); if(rnd()&1){ unsigned y2 = 1 + rnd() % (N-1); for(int x = 0; x < N; x++) if(__builtin_popcount(x & y2) & 1) m &= ~(1u<<x); } }
      else m = 1u << (rnd() % N);
      int op = rnd() % 4; int c = (op == 0) ? rcoef() : 0; if(op == 0 && c == 1) c = p-1;
      for(int i = 0; i < N; i++) if(m>>i & 1){ if(op == 0) w[i] = c*w[i]; else if(op == 1) w[i] = 0; else if(op == 2) w[i] = rentry(); } else if(op == 3) w[i] = 0;
      if(mk(w, out) && __builtin_popcount(out->supp) > 1 && !held(out)) return 1;
    } else {
      for(int i = 0; i < N; i++) w[i] = rentry();
      if(mk(w, out) && __builtin_popcount(out->supp) > 1 && !held(out)) return 1;
    }
  }
  return 0;
}
int main(int argc, char **argv){
  if(argc < 8){ fprintf(stderr, "usage: fpgame p N W iters seed T0 pool [seedfile]\n"); return 2; }
  p = atoi(argv[1]); N = atoi(argv[2]); W = atoi(argv[3]); long iters = atol(argv[4]); rs ^= (uint64_t)atol(argv[5]) * 0x9E3779B97F4A7C15ULL; for(int i = 0; i < 20; i++) rnd();
  double T0 = atof(argv[6]); pool = atoi(argv[7]);
  if(p < 3 || p > 251){ fprintf(stderr, "p out of range\n"); return 2; }
  for(int a = 1; a < p; a++) for(int b = 1; b < p; b++) if((a*b) % p == 1) inv[a] = b;
  K = 0; while((1 << K) < N) K++; M = N + W; if(M > MAXM){ fprintf(stderr, "too many wires\n"); return 2; }
  int w[MAXN];
  for(int i = 0; i < N; i++){ for(int j = 0; j < N; j++) w[j] = (i == j); mk(w, &H[i]); }
  for(int y = 0; y < N; y++){ for(int x = 0; x < N; x++) w[x] = (__builtin_popcount(x & y) & 1) ? -1 : 1; mk(w, &H[N+y]); }
  int have = 2*N;
  if(argc > 8){
    FILE *f = fopen(argv[8], "r"); if(!f){ fprintf(stderr, "no seed file\n"); return 2; }
    static vec cand[400]; int nc = 0; char line[4096];
    while(fgets(line, sizeof line, f)){ if(line[0] == '#') continue; char *q0 = line; int ok = 1; for(int i = 0; i < N; i++){ char *q; long t = strtol(q0, &q, 10); if(q == q0){ ok = 0; break; } w[i] = (int)t; q0 = q; }
      if(!ok) continue; vec x; if(!mk(w, &x)) continue; if(__builtin_popcount(x.supp) < 2) continue; int dup = 0; for(int i = 0; i < 2*N; i++) if(same(&H[i], &x)) dup = 1; for(int i = 0; i < nc; i++) if(same(&cand[i], &x)) dup = 1; if(!dup && nc < 400) cand[nc++] = x; }
    fclose(f);
    while(nc > W - N){ int i = rnd() % nc; cand[i] = cand[--nc]; }
    for(int i = 0; i < nc; i++) H[have++] = cand[i];
  }
  while(have < M){ vec x; for(int i = 0; i < N; i++) w[i] = rentry(); if(mk(w, &x) && __builtin_popcount(x.supp) > 1){ int dup = 0; for(int i = 0; i < have; i++) if(same(&H[i], &x)) dup = 1; if(!dup) H[have++] = x; } }
  for(int i = 0; i < M; i++) refresh(i);
  int cv = cost(0), best = cv; long it = 0, hits = 0;
  for(it = 0; it < iters && cv > 0; it++){
    double T = T0 * (1.0 - (double)it / iters) + 0.05;
    int i = 2*N + rnd() % (M - 2*N); vec nw; if(!propose(&nw)) continue;
    vec old = H[i]; H[i] = nw; refresh(i); int v = cost(0);
    if(v <= cv || urand() < exp((cv - v) / T)) cv = v; else { H[i] = old; refresh(i); }
    if(cv < best) best = cv;
  }
  printf("p=%d N=%d W=%d pool=%d seed=%s T0=%s: least number of underivable wires %d after %ld moves\n", p, N, W, pool, argv[5], argv[6], best, it);
  if(cv == 0){
    cost(1);
    printf("CIRCUIT %d gates over GF(%d) (wire : entries : made from wires a, b ; inputs are 0..%d)\n", W, p, N-1);
    for(int t = 0; t < nord; t++){ int x = ord[t]; printf("w %d :", x); for(int i = 0; i < N; i++) printf(" %d", H[x].e[i]); printf(" : %d %d\n", par[x][0], par[x][1]); }
  }
  (void)hits; return 0;
}
