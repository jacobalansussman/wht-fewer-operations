/* bench_small.c -- x86-hybrid-small (22 Oct 2026): the x86-hybrid comparison at the sizes libraries use.
 *
 * Question: RaBitQ-Library, FAISS and ik_llama.cpp rotate MANY vectors of 64-512 points (mostly single precision).
 * x86-hybrid timed one transform of 2^10..2^20 points at a time.  Here every timed call transforms a BATCH of B
 * independent vectors of n points, stored back to back (vector b at buf + b*n), and the sizes are n = 2^6..2^9 (plus
 * 2^10 and 2^12 to overlap x86-hybrid).  The batch fits in L2 (BATCH_KB, default 512 KB = half of Zen 4/5's 1 MB L2;
 * run.sh sets min(512 KB, L2 per core / 2)), so B = BATCH_KB / (n * sizeof(element)), e.g. B = 2048 at n = 64 f32.
 *
 * This file #includes bench_hyb.c (x86-hybrid's harness, pinned copy; only its main is renamed, so `trace` / `plan` are
 * forwarded and check_plan.py still proves the hyb plans equal FFHT's fht_avx.c), which #includes bench_k0.c (x86-wht).
 *
 * Programs (all in one binary, every one of them on its own copy of the same batch):
 *   rivals   FFHT                 FFHT (fba727a3) called once per vector, as a library calls it
 *            x86wht-tb, -tbbal    x86-wht's whole transform, once per vector (textbook, pipe-balanced textbook)
 *            hyb8-tb8, -tb8bal, -tb8balS
 *                                 FFHT's structure in intrinsics, once per vector, textbook 8-vector kernel; balS =
 *                                 the SUB-first balanced twin (hybrid-twin.md: tb8bal's very lines in another order, no
 *                                 register copies in clang; ported from x86-hybrid after its skeptic said READY)
 *            hyb16-tb16, -tb16bal, -tb16balS
 *                                 the 16-vector form of that structure (tb16bal: open issue A of hybrid-check.md;
 *                                 tb16balS: the same SUB-first order for the 16-vector textbook, added here)
 *            sl4-tb4, sl8-tb8, sl8-tb8bal, sl8-tb8balS, sl16-tb16, sl16-tb16bal, sl16-tb16balS
 *                                 STRAIGHT-LINE in-register transform: when n = R * lanes with R = 4, 8 or 16, ONE step
 *                                 does all of it (in-lane levels on each of the R vectors, then the R-vector kernel), and
 *                                 one function runs that step over the whole batch (no call per vector).  This is FFHT's
 *                                 own first step (bench_hyb.c hfirst_<kernel>) applied to B*n points, with its
 *                                 loads, in-lane levels and stores forced fully unrolled (sl_<kernel>, DEFSL below).
 *   circuits hyb8-g19, hyb8-g20, hyb8-h20half, hyb16-g52   (FFHT's structure, once per vector)
 *            sl8-g19, sl8-g20, sl8-h20half                  (straight-line, n = 8 vectors)
 *            sl16-g52, sl16-g20x2                           (straight-line, n = 16 vectors; g20x2 = g20 on each half +
 *                                                            the 2-point level between the halves, 56 lines)
 *   broken   gate only, never timed: each layout with a deliberately broken kernel, plus a batch loop that skips the
 *            last vector.  Each must FAIL wherever it runs.
 * Layouts (which program exists at which n) are in applies(); `list L...` prints them.  g52 needs 16 vectors in one
 * transform: n = 64 in f64 256-bit (16 x 4), n = 128 in f32 256-bit and f64 512-bit (16 x 8), n = 256 in f32 512-bit
 * (16 x 16), and through the hyb16 structure above that.  At n = 64 in f32 256-bit (8 vectors of 8) no 16-vector layout
 * exists without narrower vectors or a transpose, so g52 is not run there.
 *
 * Timing (bench.h's protocol: calibrate per program, >= 9 repeats of >= 0.2 s of timed work, the programs take turns
 * with the starting program rotating, best and median) with one change, for finite data: x86-hybrid's same-array runs
 * overflowed to inf/NaN after a few dozen calls (x86-headline-harness.md section 7).  Here a repeat is a sequence of
 * SEGMENTS of K back-to-back calls (K even); between segments an UNTIMED pass multiplies the batch by (n s^2)^(-K/2), a
 * power of two (s = the program's output scale, 1 or 2^-p for h20half), which undoes H.H = n I exactly in exponent, so
 * the data returns to about its start (rounding drift only) and provably stays below 2^(L*K/2) <= 2^117 in f32.  Only the
 * K calls are timed (one clock read per segment, >= 18 calls).  After every repeat the batch is checked: finite, no
 * subnormals; the RESULT line says so.  ns per vector = timed ns / (segments * K * B).
 * Modes:  check maxL L...  |  batch L...  |  list L...  |  count L...  |  trace 3|4 L...  |  plan L...
 * Env:    BATCH_KB (default 512), SMALL_SMOKE=1 (Mac smoke test of the timing code: 3 repeats of 2 ms; never a result).
 */
#define HYB_NO_MAIN
#include "bench_hyb.c"
#include <float.h>

/* ---- the extra kernels ---- */
/* g20x2: H16 = H2 (x) H8 with index i = 8*hi + lo: g20 on v[0..7] and on v[8..15] (H8 on lo), then the 2-point level
 * between the halves (H2 on hi).  2 x 20 + 16 = 56 lines (textbook 64, g52 52).  Natural order out. */
static inline void g20_x2(V *v, V one) {
  g20_nat(v, one);
  g20_nat(v + 8, one);
  for (int i = 0; i < 8; i++) {
    V a = v[i], b = v[i + 8];
    v[i] = V_ADD(a, b);
    v[i + 8] = V_SUB(a, b);
  }
}
static inline void broken_g20x2(V *v, V one) { /* the g20 on the first half has outputs 5 and 6 swapped */
  broken_g20(v, one);
  g20_nat(v + 8, one);
  for (int i = 0; i < 8; i++) {
    V a = v[i], b = v[i + 8];
    v[i] = V_ADD(a, b);
    v[i + 8] = V_SUB(a, b);
  }
}
static inline void broken_g52(V *v, V one) { /* g52 with outputs 5 and 6 swapped */
  g52_nat(v, one);
  V t = v[5];
  v[5] = v[6];
  v[6] = t;
}
DEFHYB(tb16_bal, 16)
DEFHYB(tb16_balS, 16)
DEFHYB(broken_g52, 16)
/* ---- the straight-line step: bench_hyb.c's hfirst_<K> (FFHT's from = 0 step) with the R loads, in-lane levels and
 * stores FORCED fully unrolled.  Review on this Mac (clang 21 x86-64 objects): hfirst_<16-vector kernel> kept its
 * 16-iteration in-lane / store loops rolled at f32 (1 store instruction, 24-60 stack accesses even with 32 registers),
 * i.e. not straight-line; the 8-vector ones were already unrolled.  The hyb structure keeps hfirst unchanged (it is
 * x86-hybrid's timed code). */
#define DEFSL(K, R)                                                                                    \
  __attribute__((unused)) static void sl_##K(ET *buf, size_t n) {                                      \
    V one = SET1((ET)1);                                                                               \
    OPQ(one);                                                                                          \
    for (size_t j = 0; j < n; j += (size_t)(R) * LANES) {                                              \
      V v[R];                                                                                          \
      _Pragma("GCC unroll 16") for (int l = 0; l < (R); l++) v[l] = ffht_inlane(LD(buf + j + (size_t)l * LANES)); \
      K(v, one);                                                                                       \
      _Pragma("GCC unroll 16") for (int l = 0; l < (R); l++) ST(buf + j + (size_t)l * LANES, v[l]);    \
    }                                                                                                  \
  }
DEFSL(tb4_nat, 4)
DEFSL(tb8_nat, 8)
DEFSL(tb8_bal, 8)
DEFSL(tb8_balS, 8)
DEFSL(g19_nat, 8)
DEFSL(g20_nat, 8)
DEFSL(h20_nat, 8)
DEFSL(broken_g20, 8)
DEFSL(tb16_nat, 16)
DEFSL(tb16_bal, 16)
DEFSL(tb16_balS, 16)
DEFSL(g52_nat, 16)
DEFSL(g20_x2, 16)
DEFSL(broken_g52, 16)
DEFSL(broken_g20x2, 16)
static const hvar HS[] = {
    HV16("hyb16-tb16bal", tb16_bal, tb8_bal),
    HV16("BROKEN-hyb16-g52swap", broken_g52, g20_nat),
    HV16("hyb16-tb16balS", tb16_balS, tb8_balS),
};

/* ---- the programs ---- */
enum { K_X86WHT, K_FFHT, K_HYB, K_SL, K_SLSKIP };
typedef struct {
  const char *name;
  int kind;
  int role;         /* 1 rival, 0 circuit, -1 deliberately broken (gate only, never timed) */
  const hvar *H;    /* K_HYB: the plan's kernels */
  hfirst_fn f;      /* K_SL / K_SLSKIP: the straight-line step, run over the whole batch */
  int R;            /* K_SL: vectors per transform */
  double s;         /* K_SL: output scale per transform (sl8-h20half: 0.5) */
  int w;            /* K_X86WHT: index into bench_k0.c's WV[] */
} sprog;
#define HYP(NM, HP, ROLE) {NM, K_HYB, ROLE, HP, NULL, 0, 1.0, 0}
#define SLP(NM, K, R, S, ROLE) {NM, K_SL, ROLE, NULL, sl_##K, R, S, 0}
static const sprog SP[] = {
#ifdef WITH_FFHT
    {"FFHT", K_FFHT, 1, NULL, NULL, 0, 1.0, 0},
#endif
    {"x86wht-tb", K_X86WHT, 1, NULL, NULL, 0, 1.0, 0},
    {"x86wht-tbbal", K_X86WHT, 1, NULL, NULL, 0, 1.0, 1},
    HYP("hyb8-tb8", &HV[0], 1),
    HYP("hyb8-tb8bal", &HV[1], 1),
    HYP("hyb8-tb8balS", &HV[7], 1),
    HYP("hyb16-tb16", &HV[2], 1),
    HYP("hyb16-tb16bal", &HS[0], 1),
    HYP("hyb16-tb16balS", &HS[2], 1),
    SLP("sl4-tb4", tb4_nat, 4, 1.0, 1),
    SLP("sl8-tb8", tb8_nat, 8, 1.0, 1),
    SLP("sl8-tb8bal", tb8_bal, 8, 1.0, 1),
    SLP("sl8-tb8balS", tb8_balS, 8, 1.0, 1),
    SLP("sl16-tb16", tb16_nat, 16, 1.0, 1),
    SLP("sl16-tb16bal", tb16_bal, 16, 1.0, 1),
    SLP("sl16-tb16balS", tb16_balS, 16, 1.0, 1),
    HYP("hyb8-g19", &HV[3], 0),
    HYP("hyb8-g20", &HV[4], 0),
    HYP("hyb8-h20half", &HV[5], 0),
    HYP("hyb16-g52", &HV[6], 0),
    SLP("sl8-g19", g19_nat, 8, 1.0, 0),
    SLP("sl8-g20", g20_nat, 8, 1.0, 0),
    SLP("sl8-h20half", h20_nat, 8, 0.5, 0),
    SLP("sl16-g52", g52_nat, 16, 1.0, 0),
    SLP("sl16-g20x2", g20_x2, 16, 1.0, 0),
    HYP("BROKEN-hyb8-g20swap", &HBROKEN, -1),
    HYP("BROKEN-hyb16-g52swap", &HS[1], -1),
    SLP("BROKEN-sl8-g20swap", broken_g20, 8, 1.0, -1),
    SLP("BROKEN-sl16-g52swap", broken_g52, 16, 1.0, -1),
    SLP("BROKEN-sl16-g20x2swap", broken_g20x2, 16, 1.0, -1),
    {"BROKEN-sl8-g20-skiplast", K_SLSKIP, -1, NULL, sl_g20_nat, 8, 1.0, 0},
};
#define NSP (int)(sizeof SP / sizeof SP[0])

/* number of full K-level steps (K = 3: 8-vector, K = 4: 16-vector) every element passes through in the hyb plan */
static int hyb_countK(int L, const hvar *H) {
  if (L < LOGL) return 0;
  int K = H->K, thr = ffht_thr(L), c = 0, to = thr < LOGL + K ? thr : LOGL + K;
  c += (to - LOGL == K);
  for (int cur = to; cur < thr; cur = to) { to = thr < cur + K ? thr : cur + K; c += (to - cur == K); }
  for (int cur = thr; cur < L; cur = to) { to = L < cur + K ? L : cur + K; c += (to - cur == K); }
  return c;
}
static int R_of(int L) { return L >= LOGL ? 1 << (L - LOGL) : 0; } /* vectors per transform */
/* which program runs at which size (the same rule for a layout's rivals, circuits and broken copy) */
static int applies(const sprog *p, int L) {
  int R = R_of(L);
  if (L < 1) return 0;
  switch (p->kind) {
    case K_FFHT:
    case K_X86WHT: return 1;
    case K_SL:
    case K_SLSKIP: return R == p->R;
    case K_HYB: {
      int nK = hyb_countK(L, p->H);
      if (p->H->K == 3) return p->H == &HV[0] ? 1 : nK > 0; /* tb8 always; the rest only where an 8-vector step runs */
      /* 16-vector form: only where a 16-vector step runs, and not where its whole plan is that one step (= sl16 with
       * a call per vector) */
      return nK > 0 && !(R == 16 && ffht_thr(L) == L);
    }
  }
  return 0;
}
static double pscale_s(const sprog *p, int L) { /* output = scale * H x */
  if (p->kind == K_HYB) return p->H->s8 == 1.0 ? 1.0 : pow(p->H->s8, hyb_countK(L, p->H));
  if (p->kind == K_SL || p->kind == K_SLSKIP) return p->s;
  return 1.0;
}
/* the timed call: B vectors of 2^L points, back to back */
static void sbatch(const sprog *p, ET *buf, int L, long B) {
  size_t n = (size_t)1 << L;
  switch (p->kind) {
    case K_X86WHT: {
      const kent *k16 = g_wk16[p->w], *k8 = g_wk8[p->w];
      for (long b = 0; b < B; b++) whole(buf + (size_t)b * n, L, k16, k8);
      break;
    }
    case K_FFHT:
#ifdef WITH_FFHT
      for (long b = 0; b < B; b++)
#if XT == 0 || XT == 1
        fht_float(buf + (size_t)b * n, L);
#else
        fht_double(buf + (size_t)b * n, L);
#endif
#endif
      break;
    case K_HYB:
      for (long b = 0; b < B; b++) hyb(buf + (size_t)b * n, L, p->H);
      break;
    case K_SL: p->f(buf, (size_t)B * n); break;
    case K_SLSKIP: p->f(buf, (size_t)(B - 1) * n); break; /* broken: the last vector is never transformed */
  }
}

/* ---- batch size and segment length ---- */
static long g_batch_kb = 512;
static long batch_of(int L) {
  long B = g_batch_kb * 1024 / ((long)((size_t)1 << L) * (long)sizeof(ET));
  return B < 2 ? 2 : B;
}
/* K = 2M calls per timed segment.  After 2m calls the data is (n s^2)^m x (up to rounding); every intermediate value of
 * the segment is at most n^M max|x| (each level at most doubles, and H.H = n I).  M = floor(E / L) - 1 keeps n^M <= 2^(E-L)
 * with E = 126 (f32) or 1022 (f64), capped at 16. */
static int kcalls(int L) {
  int M = (sizeof(ET) == 4 ? 126 : 1022) / L - 1;
  if (M > 16) M = 16;
  if (M < 1) M = 1;
  return 2 * M;
}
static double rescale_of(const sprog *p, int L, int K) { /* (n s^2)^(-K/2), an exact power of two */
  int e = L + 2 * (int)lround(log2(pscale_s(p, L)));
  return ldexp(1.0, -e * (K / 2));
}

/* ---- timing: bench.h's protocol over segments, finite data ---- */
typedef struct {
  const sprog *p;
  int L, K;
  long B;
  size_t tot;
  ET *buf, *init;
  ET resc;
  long nonfinite, subnormal; /* over every repeat's end state */
  double maxabs;
} sctx;
static void s_rescale(sctx *c) {
  ET f = c->resc, *b = c->buf;
  for (size_t i = 0; i < c->tot; i++) b[i] *= f;
}
/* untimed reset to the batch's start; segs segments of K timed calls; the exact rescale between segments untimed */
static double s_run(sctx *c, long segs) {
  memcpy(c->buf, c->init, c->tot * sizeof(ET));
  double ns = 0;
  for (long s = 0; s < segs; s++) {
    if (s) s_rescale(c);
    uint64_t t0 = bench_now_ns();
    for (int k = 0; k < c->K; k++) sbatch(c->p, c->buf, c->L, c->B);
    ns += (double)(bench_now_ns() - t0);
  }
  return ns;
}
static void s_inspect(sctx *c) { /* untimed: the state after a repeat must be finite and free of subnormals */
  for (size_t i = 0; i < c->tot; i++) {
    double v = (double)c->buf[i];
    if (!isfinite(v)) c->nonfinite++;
    else {
      if (v != 0 && fabs(v) < (sizeof(ET) == 4 ? (double)FLT_MIN : DBL_MIN)) c->subnormal++;
      if (fabs(v) > c->maxabs) c->maxabs = fabs(v);
    }
  }
}
static int g_smoke = 0;
static long s_calibrate(sctx *c, double min_s) {
  long k = 1;
  s_run(c, 1); /* warm-up */
  for (;;) {
    double ns = s_run(c, k);
    if (ns >= min_s * 1e9) return k;
    if (ns < min_s * 1e9 / 16) k *= 8;
    else k = (long)ceil((double)k * min_s * 1e9 * 1.1 / ns);
  }
}
static void s_compare(const char *title, sctx *c, int np, bench_stat *st) {
  int reps = g_smoke ? 3 : 9;
  double min_s = g_smoke ? 0.002 : 0.2;
  long segs[64];
  printf("## %s  (%d repeats of >= %.3f s of timed calls each, programs take turns; ns per vector)\n", title, reps, min_s);
  for (int j = 0; j < np; j++) {
    st[j].name = c[j].p->name;
    st[j].nrep = reps;
    segs[j] = s_calibrate(&c[j], min_s);
    st[j].calls_per_rep = segs[j] * c[j].K;
  }
  for (int r = 0; r < reps; r++) {
    for (int jj = 0; jj < np; jj++) {
      int j = (jj + r) % np;
      double ns = s_run(&c[j], segs[j]);
      s_inspect(&c[j]);
      st[j].rep[r] = ns / ((double)segs[j] * c[j].K * (double)c[j].B);
      printf("rep %2d  %-28s %12.4f\n", r, c[j].p->name, st[j].rep[r]);
    }
  }
  for (int j = 0; j < np; j++) {
    double tmp[BENCH_MAX_REPS];
    memcpy(tmp, st[j].rep, sizeof(double) * reps);
    qsort(tmp, reps, sizeof(double), bench_cmp_d);
    st[j].best = tmp[0];
    st[j].median = (reps & 1) ? tmp[reps / 2] : 0.5 * (tmp[reps / 2 - 1] + tmp[reps / 2]);
  }
  for (int j = 0; j < np; j++)
    printf("RESULT %s %-24s best %10.4f median %10.4f ns/vector | %.5f ns/point | %.2f us/call | calls/rep %ld K %d B %ld "
           "| finite %s nonfinite %ld subnormal %ld max|x| %.3g%s\n",
           title, st[j].name, st[j].best, st[j].median, st[j].median / (double)((size_t)1 << c[j].L),
           st[j].median * (double)c[j].B / 1000.0, st[j].calls_per_rep, c[j].K, c[j].B,
           c[j].nonfinite || c[j].subnormal ? "NO" : "yes", c[j].nonfinite, c[j].subnormal, c[j].maxabs,
           g_smoke ? " SMOKE-TEST-NOT-A-RESULT" : "");
  fflush(stdout);
}

/* ---- the exactness gate ---- */
#define GUARD 64 /* elements before and after the batch: a step that writes outside its batch is caught */
static const ET SENT = (ET)1234.5;
typedef struct { long bad, guard; double relerr; int finite_ok; double resc_dev; } gres;
static gres gate_one(const sprog *p, int L, long B, int full) {
  gres g = {0, 0, 0, 1, 0};
  size_t n = (size_t)1 << L, tot = (size_t)B * n;
  ET *mem = bench_alloc((tot + 2 * GUARD) * sizeof(ET)), *x = mem + GUARD;
  double *r = malloc(tot * sizeof(double));
  for (int i = 0; i < GUARD; i++) { mem[i] = SENT; x[tot + i] = SENT; }
  for (size_t i = 0; i < tot; i++) { x[i] = (ET)rint8(); r[i] = x[i]; }
  for (long b = 0; b < B; b++) bench_ref_wht_d(r + (size_t)b * n, L);
  sbatch(p, x, L, B);
  double sc = pscale_s(p, L);
  g.bad = mismatches(x, r, tot, sc);
  for (int i = 0; i < GUARD; i++) g.guard += (mem[i] != SENT) + (x[tot + i] != SENT);
  if (full) {
    /* real inputs in [-1, 1): relative error against the double reference (x86-hybrid's tolerance) */
    for (size_t i = 0; i < tot; i++) { x[i] = (ET)bench_rand_pm1(); r[i] = x[i]; }
    for (long b = 0; b < B; b++) bench_ref_wht_d(r + (size_t)b * n, L);
    sbatch(p, x, L, B);
    double mx = 0, e = 0;
    for (size_t i = 0; i < tot; i++) if (fabs(r[i]) > mx) mx = fabs(r[i]);
    for (size_t i = 0; i < tot; i++) { double d = fabs((double)x[i] / sc - r[i]); if (!(d <= e)) e = d; }
    g.relerr = e / mx;
    /* the timing loop itself (s_run: 2 segments of K calls, the exact rescale between them), then one more rescale:
     * the batch must be back at its start up to rounding, and finite throughout */
    sctx c = {p, L, kcalls(L), B, tot, x, bench_alloc(tot * sizeof(ET)), 0, 0, 0, 0};
    c.resc = (ET)rescale_of(p, L, c.K);
    for (size_t i = 0; i < tot; i++) c.init[i] = (ET)bench_rand_pm1();
    s_run(&c, 2);
    s_inspect(&c);
    g.finite_ok = !c.nonfinite && !c.subnormal;
    s_rescale(&c);
    double dev = 0, m0 = 0;
    for (size_t i = 0; i < tot; i++) {
      double d = fabs((double)x[i] - (double)c.init[i]);
      if (!(d <= dev)) dev = d;
      if (fabs((double)c.init[i]) > m0) m0 = fabs((double)c.init[i]);
    }
    g.resc_dev = dev / m0;
    free(c.init);
  }
  free(mem);
  free(r);
  return g;
}
static int scheck(int maxL, const int *Ls, int nL) {
  int ok = 1;
  printf("CHECK batch footprint %ld KB; timed sizes:", g_batch_kb);
  for (int i = 0; i < nL; i++) printf(" 2^%d (B %ld, K %d)", Ls[i], batch_of(Ls[i]), kcalls(Ls[i]));
  printf("\n");
  /* kernels: unit vectors + random integers, exact; the broken kernels must be caught */
  const char *kn[] = {"tb8", "tb8bal", "g19", "g20", "h20half", "tb16", "tb16bal", "g52"};
  for (int q = 0; q < (int)(sizeof kn / sizeof kn[0]); q++) {
    const kent *k = kfind(kn[q]);
    ok &= check_kernel(k->name, k->k, k->R, k->scale, 0);
  }
  ok &= check_kernel("tb8balS", tb8_balS, 8, 1, 0);
  ok &= check_kernel("tb16balS", tb16_balS, 16, 1, 0);
  ok &= check_kernel("g20x2", g20_x2, 16, 1, 0);
  ok &= check_kernel("tb4", tb4_nat, 4, 1, 0);
  struct { const char *nm; kfn k; int R; } bk[] = {{"broken_g20", broken_g20, 8}, {"broken_g52", broken_g52, 16},
                                                   {"broken_g20x2", broken_g20x2, 16}};
  for (int q = 0; q < 3; q++) {
    int caught = !check_kernel(bk[q].nm, bk[q].k, bk[q].R, 1, 1);
    printf("CHECK kernel %-13s alone is %s\n", bk[q].nm, caught ? "CAUGHT (good)" : "NOT CAUGHT (the gate is blind)");
    ok &= caught;
  }
  ok &= check_inlane();
  /* the reference against the definition y_j = sum_i (-1)^popcount(i & j) x_i */
  for (int L = 1; L <= maxL && L <= 12; L++) {
    size_t n = (size_t)1 << L;
    double *x = malloc(n * sizeof(double)), *r = malloc(n * sizeof(double));
    for (size_t i = 0; i < n; i++) { x[i] = rint8(); r[i] = x[i]; }
    bench_ref_wht_d(r, L);
    long bd = 0;
    for (size_t j = 0; j < n; j++) {
      double s = 0;
      for (size_t i = 0; i < n; i++) s += Hsign((int)j, (int)i) * x[i];
      bd += s != r[j];
    }
    if (bd || L == maxL) printf("CHECK 2^%-2d reference = definition (direct sum): %ld wrong %s\n", L, bd, bd ? "FAIL" : "PASS");
    ok &= bd == 0;
    free(x); free(r);
  }
  /* pass 1: every size 2^1..2^maxL, a batch of 3 vectors; pass 2: every timed size with its timing batch B */
  int caught_all = 1;
  long ncheck = 0;
  for (int pass = 1; pass <= 2; pass++) {
    int nl = pass == 1 ? maxL : nL;
    for (int li = 0; li < nl; li++) {
      int L = pass == 1 ? li + 1 : Ls[li];
      long B = pass == 1 ? 3 : batch_of(L);
      for (int q = 0; q < NSP; q++) {
        const sprog *p = &SP[q];
        if (!applies(p, L)) continue;
        gres g = gate_one(p, L, B, pass == 2 && p->role >= 0);
        ncheck++;
        if (p->role < 0) {
          int caught = g.bad > 0;
          caught_all &= caught;
          printf("CHECK %s 2^%-2d B %-5ld %-24s %ld wrong of %zu: %s\n", XNAME, L, B, p->name, g.bad,
                 (size_t)B << L, caught ? "FAIL (caught, good)" : "PASS (NOT CAUGHT: the gate is blind)");
          continue;
        }
        int pass_ok = g.bad == 0 && g.guard == 0;
        if (pass == 2) {
          double tol = sizeof(ET) == 4 ? 1e-5 : 1e-12, rtol = sizeof(ET) == 4 ? 1e-3 : 1e-9;
          int rel_ok = g.relerr < tol, res_ok = g.finite_ok && g.resc_dev < rtol;
          printf("CHECK %s 2^%-2d B %-5ld %-24s exact on integers (output = H x * %g): %ld wrong, guard %ld %s | real rel err "
                 "%.2e %s | timing loop: finite %s, back to start after rescale (dev %.1e) %s\n",
                 XNAME, L, B, p->name, pscale_s(p, L), g.bad, g.guard, pass_ok ? "PASS" : "FAIL", g.relerr,
                 rel_ok ? "PASS" : "FAIL", g.finite_ok ? "yes" : "NO", g.resc_dev, res_ok ? "PASS" : "FAIL");
          pass_ok &= rel_ok && res_ok;
        } else if (!pass_ok || L <= 2 || L == maxL)
          printf("CHECK %s 2^%-2d B %-5ld %-24s exact on integers (output = H x * %g): %ld wrong, guard %ld %s\n", XNAME, L,
                 B, p->name, pscale_s(p, L), g.bad, g.guard, pass_ok ? "PASS" : "FAIL");
        ok &= pass_ok;
      }
    }
  }
  /* every layout that is timed somewhere has its broken copy run (and caught) at that size */
  int covered = 1;
  for (int li = 0; li < nL; li++) {
    int L = Ls[li];
    int fam[4] = {0, 0, 0, 0}, brk[4] = {0, 0, 0, 0}; /* hyb8, hyb16, sl8, sl16 */
    for (int q = 0; q < NSP; q++) {
      const sprog *p = &SP[q];
      if (!applies(p, L) || p->kind == K_FFHT || p->kind == K_X86WHT || p->kind == K_SLSKIP) continue;
      int f = p->kind == K_HYB ? (p->H->K == 3 ? 0 : 1) : (p->R == 8 ? 2 : p->R == 16 ? 3 : -1);
      if (f < 0) continue;
      if (p->role == 0) fam[f] = 1;
      if (p->role < 0) brk[f] = 1;
    }
    for (int f = 0; f < 4; f++)
      if (fam[f] && !brk[f]) { covered = 0; printf("CHECK 2^%d: a circuit layout (%d) runs without its broken copy FAIL\n", L, f); }
  }
  printf("CHECK %ld (program, size, batch) cases; every deliberately broken copy fails wherever it runs: %s; every timed "
         "circuit layout has its broken copy run at the same size: %s\n", ncheck, caught_all ? "YES (good)" : "NO (the gate is blind)",
         covered ? "YES" : "NO");
  ok &= caught_all && covered;
  printf("ALL %s\n", ok ? "PASS" : "FAIL");
  return !ok;
}

/* ---- listing ---- */
static int list_programs(int L, const sprog **out, int timed_only) {
  int np = 0;
  for (int q = 0; q < NSP; q++)
    if (applies(&SP[q], L) && (!timed_only || SP[q].role >= 0)) out[np++] = &SP[q];
  return np;
}

int main(int argc, char **argv) {
  if (argc > 1 && (!strcmp(argv[1], "trace") || !strcmp(argv[1], "plan"))) return bench_hyb_main(argc, argv);
  bench_init();
  wk_init();
  if (getenv("BATCH_KB")) g_batch_kb = atol(getenv("BATCH_KB"));
  if (g_batch_kb < 4) g_batch_kb = 4;
  g_smoke = getenv("SMALL_SMOKE") && atoi(getenv("SMALL_SMOKE")) == 1;
  printf("# bench_small %s, %d lanes, %d vector registers, compiler %s, FFHT %s, batch %ld KB\n", XNAME, LANES, NREGS,
         __VERSION__,
#ifdef WITH_FFHT
         "linked",
#else
         "NOT linked",
#endif
         g_batch_kb);
  if (argc < 2) goto usage;
  int Ls[32], nL = 0;
  const char *mode = argv[1];
  int a0 = !strcmp(mode, "check") ? 3 : 2;
  if (!strcmp(mode, "check") && argc < 3) goto usage;
  for (int a = a0; a < argc && nL < 32; a++) {
    int L = atoi(argv[a]);
    if (L >= 1 && L <= 16) Ls[nL++] = L;
  }
  if (!strcmp(mode, "check")) return scheck(atoi(argv[2]) > 0 && atoi(argv[2]) <= 16 ? atoi(argv[2]) : 12, Ls, nL);
  if (!strcmp(mode, "count")) { /* number of timed (program, size) pairs, for run.sh's time budget */
    const sprog *ps[NSP];
    int t = 0;
    for (int i = 0; i < nL; i++) t += list_programs(Ls[i], ps, 1);
    printf("COUNT %d\n", t);
    return 0;
  }
  if (!strcmp(mode, "list")) {
    for (int i = 0; i < nL; i++) {
      int L = Ls[i];
      const sprog *ps[NSP];
      int np = list_programs(L, ps, 0);
      char s8[512], s16[512];
      plan_text(s8, sizeof s8, L, &HV[0]);
      plan_text(s16, sizeof s16, L, &HV[2]);
      printf("SIZE %s 2^%d: n = %d = %d vectors of %d; B %ld (%ld KB), K %d; hyb8 %s (8-vector steps %d); hyb16 %s "
             "(16-vector steps %d)\n  programs:", XNAME, L, 1 << L, R_of(L), LANES, batch_of(L),
             batch_of(L) * ((long)1 << L) * (long)sizeof(ET) / 1024, kcalls(L), s8, hyb_countK(L, &HV[0]), s16,
             hyb_countK(L, &HV[2]));
      for (int j = 0; j < np; j++) printf(" %s%s", ps[j]->name, ps[j]->role == 1 ? "(r)" : ps[j]->role == 0 ? "(c)" : "(gate)");
      printf("\n");
    }
    return 0;
  }
  if (!strcmp(mode, "batch")) {
    for (int i = 0; i < nL; i++) {
      int L = Ls[i];
      size_t n = (size_t)1 << L;
      long B = batch_of(L);
      int K = kcalls(L);
      const sprog *ps[NSP];
      int np = list_programs(L, ps, 1);
      char s8[512], s16[512];
      plan_text(s8, sizeof s8, L, &HV[0]);
      plan_text(s16, sizeof s16, L, &HV[2]);
      printf("# SIZE 2^%d: %zu points = %d vectors of %d lanes; batch B = %ld vectors (%ld KB); K = %d calls per timed "
             "segment; FFHT threshold %d; hyb8 %s; hyb16 %s\n", L, n, R_of(L), LANES, B, (long)(B * n * sizeof(ET) / 1024),
             K, ffht_thr(L), s8, s16);
      ET *init = bench_alloc(B * n * sizeof(ET));
      for (size_t k = 0; k < B * n; k++) init[k] = (ET)bench_rand_pm1();
      sctx c[NSP];
      for (int j = 0; j < np; j++) {
        c[j] = (sctx){ps[j], L, K, B, B * n, bench_alloc(B * n * sizeof(ET)), init, 0, 0, 0, 0};
        c[j].resc = (ET)rescale_of(ps[j], L, K);
      }
      char t[160];
      snprintf(t, sizeof t, "x86-hybrid-small %s 2^%d B=%ld", XNAME, L, B);
      bench_stat st[NSP];
      s_compare(t, c, np, st);
      int br = -1;
      for (int j = 0; j < np; j++)
        if (ps[j]->role == 1 && (br < 0 || st[j].median < st[br].median)) br = j;
      for (int j = 0; j < np; j++)
        if (ps[j]->role == 0)
          printf("RATIO %s %s / best rival %s: median %.4f best %.4f\n", t, ps[j]->name, ps[br]->name,
                 st[j].median / st[br].median, st[j].best / st[br].best);
      for (int j = 0; j < np; j++) free(c[j].buf);
      free(init);
    }
    return 0;
  }
usage:
  fprintf(stderr, "usage: %s check maxL L... | batch L... | list L... | count L... | trace 3|4 L... | plan L...\n", argv[0]);
  return 2;
}
