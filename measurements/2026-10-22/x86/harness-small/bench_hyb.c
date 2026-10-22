/* bench_hyb.c -- x86-hybrid (22 Oct 2026): FFHT's structure, with this repository's circuits as its in-register kernels.
 *
 * Question: tonight (22 Oct) on Zen 2 the circuits won single passes (0.78-0.82 of the best textbook) but whole transforms
 * came out 0.96-1.03 of FFHT / textbook.  x86-wht's whole transform (bench_k0.c: whole()) is not FFHT's structure.  This
 * file keeps FFHT's structure and changes ONLY the kernel that runs on the vectors held in registers.
 *
 * FFHT (FALCONN-LIB/FFHT, commit fba727a3, gen.py) for AVX, 16 ymm registers, w = log2(lanes) (3 for float, 2 for double):
 *   - composite_step(from, to): load 2^(to-from') vectors (8 at most: 8 inputs + 8 outputs = 16 registers), do every level
 *     from..to-1 in registers, store.  The first step of a block (from = 0) does the w in-lane levels (vpermilps /
 *     vperm2f128 + vaddsubps / vaddps sequences, gen.py float_avx_0/1/2, double_avx_0/1) on each of the 8 vectors and then
 *     3 cross-vector levels; every later step does 3 cross-vector levels on 8 vectors at stride 2^from ("main_step":
 *     vaddps + vsubps, 12 + 12 per 8 vectors = the textbook 8-point transform).  The last step of a group may have 1 or 2.
 *   - greedy_merged(t): the steps [0, w+3), [w+3, w+6), ... on one block of 2^t.
 *   - greedy_merged_recursive(L, thr): blocks of 2^thr by greedy_merged, then layers thr -> thr+3 -> ... -> L; a layer
 *     first recurses into its 8 (or fewer) sub-blocks and then runs one composite step over the whole layer (depth-first).
 *   - thr per L: hall_of_fame_avx.txt (FFHT's own timings); FFHT_THR_F / FFHT_THR_D below.  check_plan.py proves, on the
 *     pinned fht_avx.c, that the hybrid's step sequence (offsets, spans, strides, vector counts) equals FFHT's.
 * The hybrid ("hyb8-<kernel>") is that structure written with intrinsics: same blocks, same order, same loops, same
 *   in-lane sequences; the 8-vector cross step calls <kernel> (textbook tb8 = FFHT's own 24 adds; or the circuits g19,
 *   g20, h20half).  "hyb16-<kernel>" is the same structure with 4 cross levels (16 vectors) per step, which FFHT's
 *   generator would emit if it had 32 registers (composite_step's limit is registers / 2 vectors); its 3-level tail steps
 *   use tb8 (textbook twin) or g20 (circuit variant).  Tail steps of 1 or 2 levels are textbook in every variant.
 *   On 512-bit builds FFHT has no code; the hybrids use x86-wht's in-lane stages and the same thresholds (FFHT itself is
 *   still timed: its AVX2 code).
 *
 * Programs (all in this one binary, same protocol as x86-wht: bench.h, programs take turns, >= 9 repeats, best + median):
 *   rivals:   FFHT (linked, -DWITH_FFHT), x86wht-tb and x86wht-tbbal (bench_k0.c's whole(), textbook and pipe-balanced
 *             textbook, unchanged), hyb8-tb8, hyb8-tb8bal, hyb16-tb16 (FFHT's structure with textbook kernels),
 *             hyb8-tb8balS (twin review, 22 Oct: tb8bal's very lines, operands and signs, each butterfly emitted SUB
 *             before FMA; the FMA-first order costs clang 12 register copies per 8-point step, see kernels_k0.h)
 *   circuits: hyb8-g19 (19 lines), hyb8-g20 (20 lines, family), hyb8-h20half (20 operations, output H/2 per 8-point step:
 *             the whole output is H x / 2^p, p = number of 8-point steps), hyb16-g52 (52 lines, 3-level tails g20)
 * Modes:  check [maxL] | trace K L... | plan L... | whole same|separate L...
 */
#define main bench_k0_main /* bench_k0.c (x86-wht, unchanged copy) gives the types, kernels, whole() and FFHT's wrapper */
#include "bench_k0.c"
#undef main

/* ---- FFHT's recursion threshold per log_n (hall_of_fame_avx.txt at fba727a3; greedy_merged / plain_unmerged = L) ---- */
static const int FFHT_THR_F[31] = {0,  1,  2,  3,  4,  5,  6,  7,  6,  9,  10, 11, 12, 11, 12, 13,
                                   13, 12, 12, 13, 12, 9,  11, 9,  12, 7,  12, 12, 7,  12, 6};
static const int FFHT_THR_D[31] = {0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  10, 11, 11, 11, 12, 12,
                                   11, 11, 12, 11, 9,  7,  11, 11, 10, 8,  11, 9,  11, 11, 9};
static int ffht_thr(int L) { return sizeof(ET) == 4 ? FFHT_THR_F[L] : FFHT_THR_D[L]; }

/* ---- FFHT's in-lane levels, written as FFHT's own instruction sequences (gen.py, AT&T operands read right to left) ---- */
#if XT == 0
static inline V ffht_inlane(V x) {
  V z = _mm256_setzero_ps();
  { /* float_avx_0: vpermilps $160, $245; vxorps; vsubps; vaddsubps */
    V a0 = _mm256_permute_ps(x, 160), a1 = _mm256_permute_ps(x, 245);
    x = _mm256_addsub_ps(a0, _mm256_sub_ps(z, a1));
  }
  { /* float_avx_1: vpermilps $68, $238; vxorps; vsubps; vblendps $204; vaddps */
    V a0 = _mm256_permute_ps(x, 68), a1 = _mm256_permute_ps(x, 238);
    V a4 = _mm256_blend_ps(a1, _mm256_sub_ps(z, a1), 204);
    x = _mm256_add_ps(a4, a0);
  }
  { /* float_avx_2: vxorps; vsubps; vperm2f128 $0, $49; vaddps */
    V a1 = _mm256_sub_ps(z, x);
    V a2 = _mm256_permute2f128_ps(x, x, 0x00), a3 = _mm256_permute2f128_ps(x, a1, 0x31);
    x = _mm256_add_ps(a3, a2);
  }
  return x;
}
#elif XT == 2
static inline V ffht_inlane(V x) {
  V z = _mm256_setzero_pd();
  { /* double_avx_0: vpermilpd $0, $15; vxorpd; vsubpd; vaddsubpd */
    V a0 = _mm256_permute_pd(x, 0), a1 = _mm256_permute_pd(x, 15);
    x = _mm256_addsub_pd(a0, _mm256_sub_pd(z, a1));
  }
  { /* double_avx_1: vperm2f128 $0; vxorpd; vsubpd; vperm2f128 $49; vaddpd */
    V a0 = _mm256_permute2f128_pd(x, x, 0x00), a2 = _mm256_sub_pd(z, x);
    V a3 = _mm256_permute2f128_pd(x, a2, 0x31);
    x = _mm256_add_pd(a3, a0);
  }
  return x;
}
#else
static inline V ffht_inlane(V x) { return inlane_all(x); } /* 512 bits: FFHT has no code; x86-wht's in-lane stages */
#endif

/* ---- extra kernels: identity (in-lane only), the 2-point butterfly, and the deliberately broken copy ---- */
static inline void kid_nat(V *v, V one) { (void)v; (void)one; }
static inline void tb2_nat(V *v, V one) {
  (void)one;
  V a = v[0], b = v[1];
  v[0] = V_ADD(a, b);
  v[1] = V_SUB(a, b);
}
static inline void broken_g20(V *v, V one) { /* g20 with outputs 5 and 6 swapped (a wiring error): the gate must FAIL it */
  g20_nat(v, one);
  V t = v[5];
  v[5] = v[6];
  v[6] = t;
}

/* ---- FFHT's composite step with a pluggable kernel on its R vectors (R = 2^levels) ----
 * hfirst: from = 0 (FFHT: k loop of one iteration, operands at stride 2^w = LANES): in-lane levels, then the kernel.
 * hstep:  from >= w: for j (step R*C) { for k < C (step LANES) { R loads at stride C; kernel; R stores } }   */
typedef void (*hfirst_fn)(ET *, size_t);
typedef void (*hstep_fn)(ET *, size_t, size_t);
#define DEFHYB(K, R)                                                                                   \
  __attribute__((unused)) static void hfirst_##K(ET *buf, size_t n) {                                  \
    V one = SET1((ET)1);                                                                               \
    OPQ(one);                                                                                          \
    for (size_t j = 0; j < n; j += (size_t)(R) * LANES) {                                              \
      V v[R];                                                                                          \
      for (int l = 0; l < (R); l++) v[l] = ffht_inlane(LD(buf + j + (size_t)l * LANES));              \
      K(v, one);                                                                                       \
      for (int l = 0; l < (R); l++) ST(buf + j + (size_t)l * LANES, v[l]);                            \
    }                                                                                                  \
  }                                                                                                    \
  __attribute__((unused)) static void hstep_##K(ET *buf, size_t n, size_t C) {                         \
    V one = SET1((ET)1);                                                                               \
    OPQ(one);                                                                                          \
    for (size_t j = 0; j < n; j += (size_t)(R) * C)                                                    \
      for (size_t k = 0; k < C; k += LANES) {                                                          \
        V v[R];                                                                                        \
        for (int l = 0; l < (R); l++) v[l] = LD(buf + j + k + (size_t)l * C);                         \
        K(v, one);                                                                                     \
        for (int l = 0; l < (R); l++) ST(buf + j + k + (size_t)l * C, v[l]);                          \
      }                                                                                                \
  }
DEFHYB(kid_nat, 1)
DEFHYB(tb2_nat, 2)
DEFHYB(tb4_nat, 4)
DEFHYB(tb8_nat, 8)
DEFHYB(tb8_bal, 8)
DEFHYB(tb8_balS, 8)
DEFHYB(g19_nat, 8)
DEFHYB(g20_nat, 8)
DEFHYB(h20_nat, 8)
DEFHYB(broken_g20, 8)
DEFHYB(tb16_nat, 16)
DEFHYB(g52_nat, 16)

typedef struct {
  const char *name;
  int K;               /* cross-vector levels per full step: 3 (8 vectors, FFHT's) or 4 (16 vectors) */
  hfirst_fn first[5];  /* by number of cross levels r = 0..K in the block's first step */
  hstep_fn step[5];    /* by number of levels r = 1..K */
  double s8;           /* output scale of the 3-level kernel (h20half: 0.5) */
} hvar;
#define HV8(NM, K8, S8) \
  {NM, 3, {hfirst_kid_nat, hfirst_tb2_nat, hfirst_tb4_nat, hfirst_##K8, NULL}, {NULL, hstep_tb2_nat, hstep_tb4_nat, hstep_##K8, NULL}, S8}
#define HV16(NM, K16, K8)                                                                          \
  {NM, 4, {hfirst_kid_nat, hfirst_tb2_nat, hfirst_tb4_nat, hfirst_##K8, hfirst_##K16},             \
   {NULL, hstep_tb2_nat, hstep_tb4_nat, hstep_##K8, hstep_##K16}, 1.0}
static const hvar HV[] = {
    HV8("hyb8-tb8", tb8_nat, 1.0),     HV8("hyb8-tb8bal", tb8_bal, 1.0), HV16("hyb16-tb16", tb16_nat, tb8_nat),
    HV8("hyb8-g19", g19_nat, 1.0),     HV8("hyb8-g20", g20_nat, 1.0),    HV8("hyb8-h20half", h20_nat, 0.5),
    HV16("hyb16-g52", g52_nat, g20_nat),        HV8("hyb8-tb8balS", tb8_balS, 1.0), /* appended: HV[0], HV[2] fixed */
};
static const hvar HBROKEN = HV8("BROKEN-hyb8-g20swap", broken_g20, 1.0);

/* ---- the plan: gen.py greedy_merged (one block) and greedy_merged_recursive (layers), same order ---- */
static int g_trace = 0;
static ET *g_trace_base = NULL;
/* one line per step, in execution order: "S <offset> <A> <B> <C> <m> <lanes>" = for (j = 0; j < A; j += B) for (k = 0;
 * k < C; k += LANES) { m vectors at buf + offset + j + k + l*C }, lanes = 1 if the step also does the in-lane levels */
#define HTRACE(base, A, B, C, m, lanes)                                                                          \
  do {                                                                                                         \
    if (g_trace) printf("S %zu %zu %zu %zu %d %d\n", (size_t)((base) - g_trace_base), (size_t)(A), (size_t)(B), \
                        (size_t)(C), (int)(m), (int)(lanes));                                                  \
  } while (0)
static void hyb_block(ET *buf, int t, const hvar *H) {
  if (t < LOGL) { scalar_wht(buf, t); return; } /* FFHT: plain_unmerged */
  size_t n = (size_t)1 << t;
  int to = t < LOGL + H->K ? t : LOGL + H->K, r = to - LOGL;
  HTRACE(buf, n, (size_t)1 << to, LANES, 1 << r, 1);
  H->first[r](buf, n);
  for (int cur = to; cur < t; cur = to) {
    to = t < cur + H->K ? t : cur + H->K;
    HTRACE(buf, n, (size_t)1 << to, (size_t)1 << cur, 1 << (to - cur), 0);
    H->step[to - cur](buf, n, (size_t)1 << cur);
  }
}
static void hyb_rec(ET *buf, int L, int depth, int thr, const hvar *H) {
  if (depth == thr) { hyb_block(buf, thr, H); return; }
  int c = thr; /* the layers are thr = c0 < c1 < ... < L with c(i+1) = min(L, c(i) + K); depth is one of them */
  for (;;) {
    int nx = L < c + H->K ? L : c + H->K;
    if (nx == depth) break;
    c = nx;
  }
  size_t sub = (size_t)1 << c;
  for (size_t i = 0; i < ((size_t)1 << (depth - c)); i++) hyb_rec(buf + i * sub, L, c, thr, H);
  HTRACE(buf, (size_t)1 << depth, (size_t)1 << depth, sub, 1 << (depth - c), 0);
  H->step[depth - c](buf, (size_t)1 << depth, sub);
}
static void hyb(ET *buf, int L, const hvar *H) {
  if (L <= 0) return;
  hyb_rec(buf, L, L, ffht_thr(L), H);
}
/* number of 3-level steps every element passes through (h20half's output is H x / 2^this) */
static int hyb_count8(int L, const hvar *H) {
  if (L < LOGL) return 0;
  int thr = ffht_thr(L), c = 0, to = thr < LOGL + H->K ? thr : LOGL + H->K;
  c += (to - LOGL == 3);
  for (int cur = to; cur < thr; cur = to) { to = thr < cur + H->K ? thr : cur + H->K; c += (to - cur == 3); }
  for (int cur = thr; cur < L; cur = to) { to = L < cur + H->K ? L : cur + H->K; c += (to - cur == 3); }
  return c;
}
static void plan_text(char *s, size_t sz, int L, const hvar *H) { /* e.g. "block 2^12 [0-6 6-9 9-12] layers [12-15 15-18 18-20]" */
  int thr = ffht_thr(L), p = 0;
  p += snprintf(s + p, sz - p, "block 2^%d [", thr);
  if (thr < LOGL) p += snprintf(s + p, sz - p, "scalar");
  else {
    int to = thr < LOGL + H->K ? thr : LOGL + H->K;
    p += snprintf(s + p, sz - p, "0-%d(lanes %d + %d)", to, LOGL, to - LOGL);
    for (int cur = to; cur < thr; cur = to) { to = thr < cur + H->K ? thr : cur + H->K; p += snprintf(s + p, sz - p, " %d-%d", cur, to); }
  }
  p += snprintf(s + p, sz - p, "] layers [");
  for (int cur = thr, to; cur < L; cur = to) { to = L < cur + H->K ? L : cur + H->K; p += snprintf(s + p, sz - p, " %d-%d", cur, to); }
  snprintf(s + p, sz - p, " ]");
}

/* ---- the programs ---- */
typedef struct {
  const char *name;
  int kind;  /* 0: x86-wht whole() (WV index), 1: FFHT, 2: hybrid (HV index) */
  int idx;
  int rival; /* 1 = rival (no circuit), 0 = circuit variant */
} prog;
static const prog PR[] = {
#ifdef WITH_FFHT
    {"FFHT", 1, NWV, 1},
#endif
    {"x86wht-tb", 0, 0, 1},     {"x86wht-tbbal", 0, 1, 1}, {"hyb8-tb8", 2, 0, 1},     {"hyb8-tb8bal", 2, 1, 1},
    {"hyb16-tb16", 2, 2, 1},    {"hyb8-tb8balS", 2, 7, 1}, {"hyb8-g19", 2, 3, 0},     {"hyb8-g20", 2, 4, 0},
    {"hyb8-h20half", 2, 5, 0},  {"hyb16-g52", 2, 6, 0},
};
#define NPR (int)(sizeof PR / sizeof PR[0])
/* review fix (22 Oct): bench_k0.c's wrun() runs kfind() (a strcmp scan of the kernel table) twice on EVERY call, a cost
 * only the x86wht rivals paid here (about 12-16 ns per call on the M4, about 4 % of a 2^10 transform).  The kernels are
 * now looked up once (wk_init, called first in main); whole() itself is unchanged. */
static const kent *g_wk16[NWV], *g_wk8[NWV];
static void wk_init(void) {
  for (int w = 0; w < NWV; w++) { g_wk16[w] = kfind(WV[w].k16); g_wk8[w] = kfind(WV[w].k8); }
}
static void prun(const prog *p, ET *b, int L) {
  if (p->kind == 2) hyb(b, L, &HV[p->idx]);
  else if (p->kind == 0) whole(b, L, g_wk16[p->idx], g_wk8[p->idx]); /* = wrun(idx) without its per-call lookup */
  else wrun(p->idx, b, L); /* FFHT, exactly as x86-wht calls it */
}
static double pscale(const prog *p, int L) {
  if (p->kind != 2 || HV[p->idx].s8 == 1.0) return 1.0;
  return pow(HV[p->idx].s8, hyb_count8(L, &HV[p->idx]));
}

/* ---- the exactness gate ---- */
static uint64_t g_seed = 0x2545F4914F6CDD1Dull;
static int rint8(void) { /* random integer in [-8, 8] */
  g_seed = g_seed * 6364136223846793005ull + 1442695040888963407ull;
  return (int)((g_seed >> 33) % 17) - 8;
}
static long mismatches(const ET *y, const double *r, size_t n, double scale) {
  long bad = 0;
  for (size_t i = 0; i < n; i++)
    if (!((double)y[i] == scale * r[i])) bad++;
  return bad;
}
static int check_inlane(void) { /* ffht_inlane on random integer vectors = the LANES-point transform, exactly */
  long bad = 0;
  ET in[LANES], out[LANES];
  double r[LANES];
  for (int t = 0; t < 64 + LANES; t++) {
    for (int l = 0; l < LANES; l++) { in[l] = (ET)(t < LANES ? (l == t) : rint8()); r[l] = in[l]; }
    ST(out, ffht_inlane(LD(in)));
    bench_ref_wht_d(r, LOGL);
    bad += mismatches(out, r, LANES, 1.0);
  }
  printf("CHECK in-lane levels (%s), %d vectors: %ld wrong %s\n", XT == 0 || XT == 2 ? "FFHT's sequences" : "x86-wht's stages",
         64 + LANES, bad, bad ? "FAIL" : "PASS");
  return bad == 0;
}
static int hcheck(int maxL) {
  int ok = 1;
  const char *kn[] = {"tb8", "tb8bal", "g19", "g20", "h20half", "tb16", "g52"};
  for (int q = 0; q < (int)(sizeof kn / sizeof kn[0]); q++) {
    const kent *k = kfind(kn[q]);
    ok &= check_kernel(k->name, k->k, k->R, k->scale, 0);
  }
  ok &= check_kernel("tb8balS", tb8_balS, 8, 1, 0);
  ok &= check_kernel("tb4", tb4_nat, 4, 1, 0);
  ok &= check_kernel("tb2", tb2_nat, 2, 1, 0);
  int kcaught = !check_kernel("BROKEN", broken_g20, 8, 1, 1);
  printf("CHECK the broken kernel (g20, outputs 5 and 6 swapped) alone is %s\n", kcaught ? "CAUGHT (good)" : "NOT CAUGHT");
  ok &= kcaught;
  ok &= check_inlane();
  int caught_all = 1;
  for (int L = 1; L <= maxL; L++) {
    size_t n = (size_t)1 << L;
    ET *x = bench_alloc(n * sizeof(ET)), *y = bench_alloc(n * sizeof(ET));
    double *r = malloc(n * sizeof(double));
    for (size_t i = 0; i < n; i++) { x[i] = (ET)rint8(); r[i] = x[i]; }
    if (L <= 12) { /* the reference itself against the definition y_j = sum_i (-1)^popcount(i & j) x_i */
      double *d = malloc(n * sizeof(double));
      for (size_t j = 0; j < n; j++) {
        double s = 0;
        for (size_t i = 0; i < n; i++) s += Hsign((int)j, (int)i) * (double)x[i];
        d[j] = s;
      }
      bench_ref_wht_d(r, L);
      long bd = 0;
      for (size_t j = 0; j < n; j++) bd += d[j] != r[j];
      if (bd || L == 12) printf("CHECK 2^%-2d reference = definition (direct sum): %ld wrong %s\n", L, bd, bd ? "FAIL" : "PASS");
      ok &= bd == 0;
      free(d);
    } else bench_ref_wht_d(r, L);
    int lok = 1;
    for (int p = 0; p < NPR; p++) {
      memcpy(y, x, n * sizeof(ET));
      prun(&PR[p], y, L);
      double sc = pscale(&PR[p], L);
      long bad = mismatches(y, r, n, sc);
      lok &= bad == 0;
      if (bad || L >= 10 || L <= 3)
        printf("CHECK %s whole 2^%-2d %-14s exact on integers (output = H x * %g): %ld wrong of %zu %s\n", XNAME, L,
               PR[p].name, sc, bad, n, bad ? "FAIL" : "PASS");
    }
    memcpy(y, x, n * sizeof(ET));
    hyb(y, L, &HBROKEN);
    long bb = mismatches(y, r, n, 1.0);
    int needs = hyb_count8(L, &HBROKEN) > 0; /* the plan runs the (broken) 8-point kernel at this size */
    if ((needs && !bb) || (L >= 10 && !needs)) caught_all = 0; /* every timed size (2^10 and up) must exercise it */
    if (needs) printf("CHECK %s whole 2^%-2d %-14s %ld wrong of %zu: %s\n", XNAME, L, HBROKEN.name, bb, n,
                      bb ? "FAIL (caught, good)" : "PASS (NOT CAUGHT: the gate is blind)");
    else if (L >= LOGL) printf("CHECK %s whole 2^%-2d %-14s not exercised (this plan has no 8-point step at 2^%d)\n", XNAME, L,
                               HBROKEN.name, L);
    if (!lok) printf("CHECK 2^%d: at least one variant FAILED\n", L);
    ok &= lok;
    /* real inputs in [-1, 1): relative error against the double reference (same tolerance as x86-wht) */
    if (L == 10 || L == maxL) {
      for (size_t i = 0; i < n; i++) { x[i] = (ET)bench_rand_pm1(); r[i] = x[i]; }
      bench_ref_wht_d(r, L);
      double mx = 0, tol = sizeof(ET) == 4 ? 1e-5 : 1e-12;
      for (size_t i = 0; i < n; i++) if (fabs(r[i]) > mx) mx = fabs(r[i]);
      for (int p = 0; p < NPR; p++) {
        memcpy(y, x, n * sizeof(ET));
        prun(&PR[p], y, L);
        double sc = pscale(&PR[p], L), e = 0;
        for (size_t i = 0; i < n; i++) { double d = fabs((double)y[i] / sc - r[i]); if (!(d <= e)) e = d; }
        int pass = e / mx < tol;
        ok &= pass;
        printf("CHECK %s whole 2^%-2d %-14s real inputs: rel err %.3e (tol %.0e) %s\n", XNAME, L, PR[p].name, e / mx, tol,
               pass ? "PASS" : "FAIL");
      }
    }
    free(x); free(y); free(r);
  }
  printf("CHECK the deliberately broken copy (%s) fails at every 2^L whose plan runs an 8-point step, and every L >= 10 "
         "runs one (up to 2^%d): %s\n", HBROKEN.name, maxL, caught_all ? "YES (good)" : "NO (the gate is blind)");
  ok &= caught_all;
  printf("ALL %s\n", ok ? "PASS" : "FAIL");
  return !ok;
}

/* ---- timing ---- */
typedef struct { int L; const prog *p; bench_pool pool; ET *init; } hctx;
static void h_reset(void *v) {
  hctx *c = v;
  for (int i = 0; i < c->pool.count; i++) memcpy(c->pool.buf[i], c->init, ((size_t)1 << c->L) * sizeof(ET));
}
static void h_run(void *v, long i) { hctx *c = v; prun(c->p, bench_pool_get(&c->pool, i), c->L); }

#ifdef HYB_NO_MAIN /* x86-hybrid-small (22 Oct 2026): bench_small.c includes this file; its main forwards trace / plan here */
#define HYB_MAIN bench_hyb_main
#else
#define HYB_MAIN main
#endif
int HYB_MAIN(int argc, char **argv) {
  bench_init();
  wk_init();
  printf("# bench_hyb %s, %d lanes, %d vector registers, compiler %s, FFHT %s\n", XNAME, LANES, NREGS, __VERSION__,
#ifdef WITH_FFHT
         "linked"
#else
         "NOT linked"
#endif
  );
  if (argc < 2 || !strcmp(argv[1], "check")) return hcheck(argc > 2 ? atoi(argv[2]) : 20);
  if (!strcmp(argv[1], "trace") && argc > 3) { /* trace K L...: the step sequence of the K-level plan, as check_plan.py reads it */
    const hvar *H = atoi(argv[2]) == 4 ? &HV[2] : &HV[0];
    for (int a = 3; a < argc; a++) {
      int L = atoi(argv[a]);
      ET *b = bench_alloc(((size_t)1 << L) * sizeof(ET));
      printf("L %d thr %d\n", L, ffht_thr(L));
      g_trace = 1; g_trace_base = b;
      hyb(b, L, H);
      g_trace = 0;
      free(b);
    }
    return 0;
  }
  if (!strcmp(argv[1], "plan")) {
    char s8[512], s16[512];
    for (int a = 2; a < argc; a++) {
      int L = atoi(argv[a]);
      plan_text(s8, sizeof s8, L, &HV[0]);
      plan_text(s16, sizeof s16, L, &HV[2]);
      printf("PLAN 2^%d FFHT threshold %d | hyb8: %s (8-point steps per element: %d) | hyb16: %s\n", L, ffht_thr(L), s8,
             hyb_count8(L, &HV[0]), s16);
    }
    return 0;
  }
  if (!strcmp(argv[1], "whole") && argc > 3) {
    int mode = !strcmp(argv[2], "separate") ? BENCH_SEPARATE : BENCH_SAME;
    bench_opts o = BENCH_OPTS_DEFAULT;
    for (int a = 3; a < argc; a++) {
      int L = atoi(argv[a]);
      if (L < 1 || L > 26) continue;
      size_t n = (size_t)1 << L;
      char s8[512], s16[512];
      plan_text(s8, sizeof s8, L, &HV[0]);
      plan_text(s16, sizeof s16, L, &HV[2]);
      printf("# PLAN 2^%d: FFHT threshold %d; hyb8 %s; hyb16 %s\n", L, ffht_thr(L), s8, s16);
      ET *init = bench_alloc(n * sizeof(ET));
      for (size_t i = 0; i < n; i++) init[i] = (ET)bench_rand_pm1();
      hctx c[NPR];
      bench_prog p[NPR];
      for (int w = 0; w < NPR; w++) {
        c[w] = (hctx){L, &PR[w], {0}, init};
        bench_pool_init(&c[w].pool, n * sizeof(ET), mode);
        p[w] = (bench_prog){PR[w].name, h_run, h_reset, &c[w]};
      }
      o.units = (double)n;
      char t[128];
      snprintf(t, sizeof t, "x86-hybrid whole %s 2^%d %s", XNAME, L, mode ? "separate" : "same");
      bench_stat st[NPR];
      bench_compare(t, p, NPR, &o, st);
      int br = -1;
      for (int w = 0; w < NPR; w++)
        if (PR[w].rival && (br < 0 || st[w].median < st[br].median)) br = w;
      for (int w = 0; w < NPR; w++)
        printf("RATIO %s %s / best rival %s: median %.4f best %.4f\n", t, PR[w].name, PR[br].name,
               st[w].median / st[br].median, st[w].best / st[br].best);
      for (int w = 0; w < NPR; w++) bench_pool_free(&c[w].pool);
      free(init);
    }
    return 0;
  }
  fprintf(stderr, "usage: %s check [maxL] | trace 3|4 L... | plan L... | whole same|separate L...\n", argv[0]);
  return 2;
}
