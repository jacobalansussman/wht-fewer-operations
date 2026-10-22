/* bench_h512.c -- x86-hybrid512 (built 22 Oct 2026 from x86-hybrid, which is unchanged).
 *
 * Question: does the circuit beat the BEST 512-bit (AVX-512F) whole Walsh-Hadamard transform on Zen 4 / Zen 5,
 * not just FFHT?  Tonight on Zen 5 (EPYC 9B45) a plain 512-bit textbook was 1.30-1.45x faster than any 256-bit code,
 * and inside the old (untuned) 512-bit build the circuit was mixed (0.88-1.07).  That build used x86-wht's in-lane stages
 * (vpermps + add + sub + blend: 4 ops per level) and FFHT's AVX thresholds.  Here the structure is re-made for 512 bits
 * and tuned on the TEXTBOOK first; the circuits then take the textbook's place in the same structure.
 *
 * Structure (FFHT's, gen.py at fba727a3, generalised; the same plan code reproduces FFHT's 256-bit plan step for step,
 * see check_plan.py and the 256-bit "plan" builds in run.sh):
 *   - block of 2^thr: the FIRST step loads R = 2^Kf contiguous vectors, does the LOGL in-lane levels on each (4 for 16
 *     floats, 3 for 8 doubles), then Kf cross-vector levels in registers (the kernel), stores; later steps do up to Kb
 *     cross levels on 2^Kb vectors at stride 2^from (16 vectors only while the stride is <= 2 KB: 16 lines at a 4 KB
 *     multiple share one L1 set, 12 ways on Zen 5 / 8 on Zen 4, which made tonight's hyb16 1.4-1.7x slower at 2^16+).
 *   - above the block: FFHT's depth-first layers of Kl = 3 levels (8 vectors at stride 2^c).
 *   - "h8-*": Kf = Kb = Kl = 3 (8 zmm per step, FFHT's choice).  "h16-*": Kf = Kb = 4 (16 zmm of the 32), Kl = 3.
 * In-lane levels, three forms (FFHT's AVX path does them per vector with immediate shuffles + arithmetic; AVX-512 has no
 * addsub, so):
 *   F: x = fma(x, s_h, swap_h(x))          s_h = +1 / -1 per lane: 1 shuffle + 1 FMA per level (FMA pipes)
 *   A: x = swap_h(x) + (x ^ m_h)            m_h = +0 / -0 per lane: 1 shuffle + 1 xor + 1 add (add pipes)
 *   X: x86-wht's inlane_stage (vpermps by index + add + sub + blend), as in tonight's 512-bit build
 *   swap_h: vshufps/vshufpd with both sources x (distance 1, 2 inside a 128-bit lane; the same lane movement as
 *   vpermilps/vpermilpd), vshuff32x4/vshuff64x2 (128-bit lane swaps: distance 4, 8 floats / 2, 4 doubles).
 *   All three are exact (x * +-1 is exact, one rounding) and do the levels in the reference's order, so the textbook
 *   variants are bit-identical to the double butterfly reference on integers and to each other on real data.
 * Tuning (mode "tune", run on the Colab before timing, on the TEXTBOOK only): the in-lane form (F / A / X) by the best of
 *   the five textbook hybrids at 2^10 and 2^14, then thr per n for each structure (candidates 2^(c-3)..2^(c+1), c = the
 *   32 KB block: 13 floats, 12 doubles).  The circuits inherit the textbook's form and thresholds (never tuned for
 *   themselves: conservative for the circuit).  Without a tune file: form F, thr = min(L, c).
 *
 * Programs (one binary, bench.h protocol as x86-hybrid: programs take turns, >= 9 repeats of >= 0.2 s, best + median):
 *   rivals:   FFHT (256-bit AVX asm, reference), x86wht-tb, x86wht-tbbal (x86-wht's 512-bit whole transforms, the
 *             best 512-bit codes measured tonight), x86wht-tbbalS (the same with tb16balS / tb8balS: copy-free),
 *             h8-tb (tb8 everywhere), h8-tbbal (tb8bal), h8-tbbalS (tb8balS: SUB before FMA, no register copies; the
 *             512-bit port of x86-hybrid's hyb8-tb8balS), h8-tbmix (first step tb8: its in-lane FMAs already fill the
 *             FMA pipes; later steps tb8balS), h16-tbmix (first tb16 / tb8, later tb16balS / tb8balS)
 *   circuits: h8-g19, h8-g20, h8-h20half (output H x / 2^p, p = 3-level steps per element), h8-g20late (first step tb8,
 *             later steps g20: the circuit only where the pipe model says it can help), h16-g52 (16-vector steps g52,
 *             3-level steps g20), h16-g52late (first step textbook, later g52 / g20)
 *   twins:    h8-g19/g20/h20half <-> h8-tb; h8-g20late <-> h8-tbmix; h16-g52, h16-g52late <-> h16-tbmix
 * Modes:  check [maxL] | tune | trace 3|4 L... | plan L... | whole same|separate L...      Env: H512_TUNE=<tune output>
 */
#define main bench_k0_main /* bench_k0.c (x86-wht, unchanged copy): types, kernels, whole(), FFHT's wrapper */
#include "bench_k0.c"
#undef main
#include "kernels_h512.h" /* tb8_balS, tb16_balS: gen_x86.py, SUB before FMA (same rule as x86-hybrid's twin) */
/* x86-wht's whole transform with the SUB-first balanced kernels (twin port, 22 Oct 2026): x86wht-tbbal is FMA-first and
 * carries register copies in clang (tb16_bal 31, tb8_bal 11 per pass function: hybrid-twin.md); x86wht-tbbalS is its
 * copy-free form, so the best x86-wht rival is not handicapped either.  Same whole(), same passes (bench_k0.c DEF4). */
DEF4(tb16_balS, 16)
DEF4(tb8_balS, 8)
static const kent KS[] = {KE("tb16balS", tb16_balS, 16, 1), KE("tb8balS", tb8_balS, 8, 1)};

#define HMIN(a, b) ((a) < (b) ? (a) : (b))

/* ---- FFHT's AVX thresholds (hall_of_fame_avx.txt at fba727a3): the default table of the 256-bit plan builds ---- */
static const int FFHT_THR_F[31] = {0,  1,  2,  3,  4,  5,  6,  7,  6,  9,  10, 11, 12, 11, 12, 13,
                                   13, 12, 12, 13, 12, 9,  11, 9,  12, 7,  12, 12, 7,  12, 6};
static const int FFHT_THR_D[31] = {0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  10, 11, 11, 11, 12, 12,
                                   11, 11, 12, 11, 9,  7,  11, 11, 10, 8,  11, 9,  11, 11, 9};
#define IS512 (XT == 1 || XT == 3)
#define BLK32K (sizeof(ET) == 4 ? 13 : 12) /* log2 of a 32 KB block */
static int g_thr[2][31];                   /* [0] 8-vector structure, [1] 16-vector structure */
static int g_form = 0;                     /* in-lane form: 0 F, 1 A, 2 X */
static const char *FORMNAME[3] = {"F(shuffle+FMA)", "A(shuffle+xor+add)", "X(x86-wht vpermps+add+sub+blend)"};
static void thr_defaults(void) {
  for (int L = 0; L < 31; L++)
    for (int s = 0; s < 2; s++) g_thr[s][L] = IS512 ? HMIN(L, BLK32K) : (sizeof(ET) == 4 ? FFHT_THR_F[L] : FFHT_THR_D[L]);
}
/* threshold candidates for n = 2^L (the gate checks every one; tune picks among them) */
static int thr_cands(int L, int *c) {
  int k = 0;
  if (!IS512) { c[k++] = g_thr[0][L]; return k; }
  int lo = BLK32K - 3, hi = BLK32K + 1;
  if (L < lo) { c[k++] = L; return k; }
  for (int t = lo; t <= HMIN(L, hi); t++) c[k++] = t;
  return k;
}
static void load_tune(const char *path) {
  FILE *f = fopen(path, "r");
  if (!f) { fprintf(stderr, "H512_TUNE: cannot open %s\n", path); exit(2); }
  char ln[256];
  int nthr = 0, nform = 0;
  while (fgets(ln, sizeof ln, f)) {
    int a, b, c;
    if (sscanf(ln, "FORM %d", &a) == 1 && a >= 0 && a < 3) { g_form = a; nform++; }
    else if (sscanf(ln, "THR %d %d %d", &a, &b, &c) == 3 && a >= 0 && a < 2 && b >= 0 && b < 31 && c >= 1 && c <= b) {
      int cc[8], nc = thr_cands(b, cc), ok = 0;
      for (int i = 0; i < nc; i++) ok |= cc[i] == c;
      if (!ok) { fprintf(stderr, "H512_TUNE: thr %d for 2^%d is not a gated candidate\n", c, b); exit(2); }
      g_thr[a][b] = c;
      nthr++;
    }
  }
  fclose(f);
  printf("# tune file %s: form %s (%d line), %d thresholds\n", path, FORMNAME[g_form], nform, nthr);
}

/* ---- in-lane levels ---- */
static inline V swap_lv(V x, int i) { /* lanes l <-> l ^ (1 << i) */
#if XT == 1
  switch (i) {
    case 0: return _mm512_shuffle_ps(x, x, 0xB1); /* = vpermilps $0xB1 (SIMDe has no _mm512_permute_ps) */
    case 1: return _mm512_shuffle_ps(x, x, 0x4E);
    case 2: return _mm512_shuffle_f32x4(x, x, 0xB1);
    default: return _mm512_shuffle_f32x4(x, x, 0x4E);
  }
#elif XT == 3
  switch (i) {
    case 0: return _mm512_shuffle_pd(x, x, 0x55); /* = vpermilpd $0x55 */
    case 1: return _mm512_shuffle_f64x2(x, x, 0xB1);
    default: return _mm512_shuffle_f64x2(x, x, 0x4E);
  }
#elif XT == 0
  switch (i) {
    case 0: return _mm256_permute_ps(x, 0xB1);
    case 1: return _mm256_permute_ps(x, 0x4E);
    default: return _mm256_permute2f128_ps(x, x, 1);
  }
#else
  switch (i) {
    case 0: return _mm256_permute_pd(x, 0x5);
    default: return _mm256_permute2f128_pd(x, x, 1);
  }
#endif
}
#if XT == 1
#define XORV(a, b) _mm512_castsi512_ps(_mm512_xor_si512(_mm512_castps_si512(a), _mm512_castps_si512(b)))
#elif XT == 3
#define XORV(a, b) _mm512_castsi512_pd(_mm512_xor_si512(_mm512_castpd_si512(a), _mm512_castpd_si512(b)))
#elif XT == 0
#define XORV _mm256_xor_ps
#else
#define XORV _mm256_xor_pd
#endif
typedef struct { V c[LOGL]; } inlc;
static inline inlc inl_consts(int form) { /* F: +1 / -1 (lane bit i set -> -1); A: +0 / -0 */
  inlc k;
  for (int i = 0; i < LOGL; i++) {
    ET a[LANES] __attribute__((aligned(64)));
    for (int l = 0; l < LANES; l++) a[l] = ((l >> i) & 1) ? (form == 0 ? (ET)-1 : (ET)-0.0) : (form == 0 ? (ET)1 : (ET)0);
    k.c[i] = LD(a);
  }
  return k;
}
/* lane bit clear: x_l + x_(l^h) (the lower element gets the sum); set: x_(l^h) - x_l (lower minus upper) */
static inline V inl_0(V x, const inlc *k) {
  for (int i = 0; i < LOGL; i++) x = FMADD(x, k->c[i], swap_lv(x, i));
  return x;
}
static inline V inl_1(V x, const inlc *k) {
  for (int i = 0; i < LOGL; i++) x = V_ADD(swap_lv(x, i), XORV(x, k->c[i]));
  return x;
}
static inline V inl_2(V x, const inlc *k) { (void)k; return inlane_all(x); }

/* ---- extra kernels: identity, 2-point, and the deliberately broken copies ---- */
static inline void kid_nat(V *v, V one) { (void)v; (void)one; }
static inline void tb2_nat(V *v, V one) {
  (void)one;
  V a = v[0], b = v[1];
  v[0] = V_ADD(a, b);
  v[1] = V_SUB(a, b);
}
static inline void broken_g20(V *v, V one) { /* g20 with outputs 5 and 6 swapped: the gate must FAIL it */
  g20_nat(v, one);
  V t = v[5]; v[5] = v[6]; v[6] = t;
}
static inline void broken_g52(V *v, V one) { /* g52 with outputs 5 and 6 swapped */
  g52_nat(v, one);
  V t = v[5]; v[5] = v[6]; v[6] = t;
}

/* ---- composite steps with a pluggable kernel on R = 2^r vectors ----
 * hfF_K(buf, n): a block's first step (from = 0): R contiguous vectors, in-lane levels (form F) on each, kernel, store.
 * hs_K(buf, n, C): a later step: for j (step R*C) { for k < C (step LANES) { R loads at stride C; kernel; R stores } } */
typedef void (*hfirst_fn)(ET *, size_t);
typedef void (*hstep_fn)(ET *, size_t, size_t);
#define DEFHF(K, R, FM)                                                                                \
  __attribute__((unused)) static void hf##FM##_##K(ET *buf, size_t n) {                               \
    V one = SET1((ET)1);                                                                               \
    OPQ(one);                                                                                          \
    inlc kc;                                                                                           \
    if ((FM) < 2) {                                                                                    \
      kc = inl_consts(FM);                                                                             \
      for (int i = 0; i < LOGL; i++) OPQ(kc.c[i]);                                                     \
    } else memset(&kc, 0, sizeof kc);                                                                  \
    for (size_t j = 0; j < n; j += (size_t)(R) * LANES) {                                              \
      V v[R];                                                                                          \
      for (int l = 0; l < (R); l++) v[l] = inl_##FM(LD(buf + j + (size_t)l * LANES), &kc);            \
      K(v, one);                                                                                       \
      for (int l = 0; l < (R); l++) ST(buf + j + (size_t)l * LANES, v[l]);                            \
    }                                                                                                  \
  }
#define DEFHS(K, R)                                                                                    \
  __attribute__((unused)) static void hs_##K(ET *buf, size_t n, size_t C) {                           \
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
#define DEFHF3(K, R) DEFHF(K, R, 0) DEFHF(K, R, 1) DEFHF(K, R, 2)
DEFHF3(kid_nat, 1)
DEFHF3(tb2_nat, 2)
DEFHF3(tb4_nat, 4)
DEFHF3(tb8_nat, 8)
DEFHF3(tb8_bal, 8)
DEFHF3(tb8_balS, 8)
DEFHF3(g19_nat, 8)
DEFHF3(g20_nat, 8)
DEFHF3(h20_nat, 8)
DEFHF3(broken_g20, 8)
DEFHF3(tb16_nat, 16)
DEFHF3(g52_nat, 16)
DEFHF3(broken_g52, 16)
DEFHS(tb2_nat, 2)
DEFHS(tb4_nat, 4)
DEFHS(tb8_nat, 8)
DEFHS(tb8_bal, 8)
DEFHS(tb8_balS, 8)
DEFHS(g19_nat, 8)
DEFHS(g20_nat, 8)
DEFHS(h20_nat, 8)
DEFHS(broken_g20, 8)
DEFHS(tb16_balS, 16)
DEFHS(g52_nat, 16)
DEFHS(broken_g52, 16)

typedef struct {
  const char *name;
  int Kf, Kb, Kl;            /* cross levels: a block's first step; later in-block steps (max); layer steps */
  hfirst_fn first[5][3];     /* by r = cross levels in the first step (0..Kf), then in-lane form */
  hstep_fn step[5];          /* by levels r (1..4) */
  int scaled;                /* 1: every 3-level step outputs H/2 (h20half) */
  int tbl;                   /* threshold table: 0 = 8-vector structure, 1 = 16-vector structure */
} hvar;
#define FT(K) {hf0_##K, hf1_##K, hf2_##K}
#define V8(NM, F3, S3, SC) {NM, 3, 3, 3, {FT(kid_nat), FT(tb2_nat), FT(tb4_nat), FT(F3), {0, 0, 0}}, \
                            {NULL, hs_tb2_nat, hs_tb4_nat, hs_##S3, NULL}, SC, 0}
#define V16(NM, F4, F3, S4, S3) {NM, 4, 4, 3, {FT(kid_nat), FT(tb2_nat), FT(tb4_nat), FT(F3), FT(F4)}, \
                                 {NULL, hs_tb2_nat, hs_tb4_nat, hs_##S3, hs_##S4}, 0, 1}
enum { H8TB, H8TBBAL, H8TBBALS, H8TBMIX, H16TBMIX, H8G19, H8G20, H8H20, H8G20L, H16G52, H16G52L, NHV };
static const hvar HV[NHV] = {
    V8("h8-tb", tb8_nat, tb8_nat, 0),
    V8("h8-tbbal", tb8_bal, tb8_bal, 0),
    V8("h8-tbbalS", tb8_balS, tb8_balS, 0),
    V8("h8-tbmix", tb8_nat, tb8_balS, 0),
    V16("h16-tbmix", tb16_nat, tb8_nat, tb16_balS, tb8_balS),
    V8("h8-g19", g19_nat, g19_nat, 0),
    V8("h8-g20", g20_nat, g20_nat, 0),
    V8("h8-h20half", h20_nat, h20_nat, 1),
    V8("h8-g20late", tb8_nat, g20_nat, 0),
    V16("h16-g52", g52_nat, g20_nat, g52_nat, g20_nat),
    V16("h16-g52late", tb16_nat, tb8_nat, g52_nat, g20_nat),
};
static const hvar HB8 = V8("BROKEN-h8-g20swap", broken_g20, broken_g20, 0);
static const hvar HB16 = V16("BROKEN-h16-g52swap", broken_g52, g20_nat, broken_g52, g20_nat);

/* ---- the plan: FFHT's greedy_merged (one block) and greedy_merged_recursive (layers), generalised ---- */
static int g_trace = 0;
static ET *g_trace_base = NULL;
/* one line per step, in execution order: "S <offset> <A> <B> <C> <m> <lanes>" (as check_plan.py reads it) */
#define HTRACE(base, A, B, C, m, lanes)                                                                          \
  do {                                                                                                         \
    if (g_trace) printf("S %zu %zu %zu %zu %d %d\n", (size_t)((base) - g_trace_base), (size_t)(A), (size_t)(B), \
                        (size_t)(C), (int)(m), (int)(lanes));                                                  \
  } while (0)
static inline int kb_at(const hvar *H, int cur) { /* 16 vectors only while the stride is <= 2 KB */
  return (H->Kb > 3 && ((size_t)sizeof(ET) << cur) > 2048) ? 3 : H->Kb;
}
static void h5_block(ET *buf, int t, const hvar *H) {
  if (t < LOGL) { scalar_wht(buf, t); return; } /* FFHT: plain_unmerged */
  size_t n = (size_t)1 << t;
  int to = HMIN(t, LOGL + H->Kf), r = to - LOGL;
  HTRACE(buf, n, (size_t)1 << to, LANES, 1 << r, 1);
  H->first[r][g_form](buf, n);
  for (int cur = to; cur < t; cur = to) {
    to = HMIN(t, cur + kb_at(H, cur));
    HTRACE(buf, n, (size_t)1 << to, (size_t)1 << cur, 1 << (to - cur), 0);
    H->step[to - cur](buf, n, (size_t)1 << cur);
  }
}
static void h5_rec(ET *buf, int L, int depth, int thr, const hvar *H) {
  if (depth == thr) { h5_block(buf, thr, H); return; }
  int c = thr; /* layers thr = c0 < c1 < ... < L, c(i+1) = min(L, c(i) + Kl); depth is one of them */
  for (;;) {
    int nx = HMIN(L, c + H->Kl);
    if (nx == depth) break;
    c = nx;
  }
  size_t sub = (size_t)1 << c;
  for (size_t i = 0; i < ((size_t)1 << (depth - c)); i++) h5_rec(buf + i * sub, L, c, thr, H);
  HTRACE(buf, (size_t)1 << depth, (size_t)1 << depth, sub, 1 << (depth - c), 0);
  H->step[depth - c](buf, (size_t)1 << depth, sub);
}
static void h5(ET *buf, int L, const hvar *H, int thr) {
  if (L <= 0) return;
  h5_rec(buf, L, L, thr, H);
}
/* number of steps of exactly r levels every element passes through (r = 3: h20half's scale is 2^-this) */
static int nsteps(int L, const hvar *H, int thr, int r) {
  if (L <= 0) return 0;
  int c = 0;
  if (thr >= LOGL) {
    int to = HMIN(thr, LOGL + H->Kf);
    c += (to - LOGL == r);
    for (int cur = to; cur < thr; cur = to) { to = HMIN(thr, cur + kb_at(H, cur)); c += (to - cur == r); }
  }
  for (int cur = thr, to; cur < L; cur = to) { to = HMIN(L, cur + H->Kl); c += (to - cur == r); }
  return c;
}
static void plan_text(char *s, size_t sz, int L, const hvar *H, int thr) { /* "block 2^13 [0-7 7-10 10-13] layers [ 13-16]" */
  int p = 0;
  p += snprintf(s + p, sz - p, "thr %d: block [", thr);
  if (thr < LOGL) p += snprintf(s + p, sz - p, "scalar");
  else {
    int to = HMIN(thr, LOGL + H->Kf);
    p += snprintf(s + p, sz - p, "0-%d(lanes %d + %d)", to, LOGL, to - LOGL);
    for (int cur = to; cur < thr; cur = to) { to = HMIN(thr, cur + kb_at(H, cur)); p += snprintf(s + p, sz - p, " %d-%d", cur, to); }
  }
  p += snprintf(s + p, sz - p, "] layers [");
  for (int cur = thr, to; cur < L; cur = to) { to = HMIN(L, cur + H->Kl); p += snprintf(s + p, sz - p, " %d-%d", cur, to); }
  snprintf(s + p, sz - p, " ]");
}

/* ---- the programs ---- */
typedef struct {
  const char *name;
  int kind;  /* 0: x86-wht whole() (WV index), 1: FFHT, 2: hybrid (HV index), 3: x86-wht whole() with KS (balS) */
  int idx;
  int rival; /* 1 = rival (no circuit), 0 = circuit variant */
} prog;
static const prog PR[] = {
#ifdef WITH_FFHT
    {"FFHT", 1, NWV, 1},
#endif
    {"x86wht-tb", 0, 0, 1},          {"x86wht-tbbal", 0, 1, 1},       {"x86wht-tbbalS", 3, 0, 1},      {"h8-tb", 2, H8TB, 1},
    {"h8-tbbal", 2, H8TBBAL, 1},     {"h8-tbbalS", 2, H8TBBALS, 1},   {"h8-tbmix", 2, H8TBMIX, 1},
    {"h16-tbmix", 2, H16TBMIX, 1},   {"h8-g19", 2, H8G19, 0},         {"h8-g20", 2, H8G20, 0},
    {"h8-h20half", 2, H8H20, 0},     {"h8-g20late", 2, H8G20L, 0},    {"h16-g52", 2, H16G52, 0},
    {"h16-g52late", 2, H16G52L, 0},
};
#define NPR (int)(sizeof PR / sizeof PR[0])
/* x86-hybrid review fix 1, kept: the x86wht kernels are looked up once, not twice per call (bench_k0.c's wrun) */
static const kent *g_wk16[NWV], *g_wk8[NWV];
static void wk_init(void) {
  for (int w = 0; w < NWV; w++) { g_wk16[w] = kfind(WV[w].k16); g_wk8[w] = kfind(WV[w].k8); }
}
static inline int hthr(const hvar *H, int L) { return g_thr[H->tbl][L]; }
static void prun(const prog *p, ET *b, int L) {
  if (p->kind == 2) h5(b, L, &HV[p->idx], hthr(&HV[p->idx], L));
  else if (p->kind == 0) whole(b, L, g_wk16[p->idx], g_wk8[p->idx]);
  else if (p->kind == 3) whole(b, L, &KS[0], &KS[1]);
  else wrun(p->idx, b, L); /* FFHT, exactly as x86-wht calls it */
}
static double hscale(const hvar *H, int L, int thr) { return H->scaled ? pow(0.5, nsteps(L, H, thr, 3)) : 1.0; }
static double pscale(const prog *p, int L) {
  if (p->kind != 2) return 1.0;
  return hscale(&HV[p->idx], L, hthr(&HV[p->idx], L));
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
static int check_inlane(void) { /* every form on random integer vectors = the LANES-point transform, exactly */
  int ok = 1;
  for (int f = 0; f < 3; f++) {
    long bad = 0;
    ET in[LANES], out[LANES];
    double r[LANES];
    inlc kc = inl_consts(f);
    for (int t = 0; t < 64 + LANES; t++) {
      for (int l = 0; l < LANES; l++) { in[l] = (ET)(t < LANES ? (l == t) : rint8()); r[l] = in[l]; }
      V x = LD(in);
      ST(out, f == 0 ? inl_0(x, &kc) : f == 1 ? inl_1(x, &kc) : inl_2(x, &kc));
      bench_ref_wht_d(r, LOGL);
      bad += mismatches(out, r, LANES, 1.0);
    }
    printf("CHECK in-lane levels, form %s, %d vectors: %ld wrong %s\n", FORMNAME[f], 64 + LANES, bad, bad ? "FAIL" : "PASS");
    ok &= bad == 0;
  }
  return ok;
}
static int hcheck(int maxL) {
  int ok = 1;
  const char *kn[] = {"tb8", "tb8bal", "g19", "g20", "h20half", "tb16", "tb16bal", "g52"};
  for (int q = 0; q < (int)(sizeof kn / sizeof kn[0]); q++) {
    const kent *k = kfind(kn[q]);
    ok &= check_kernel(k->name, k->k, k->R, k->scale, 0);
  }
  ok &= check_kernel("tb8balS", tb8_balS, 8, 1, 0);
  ok &= check_kernel("tb16balS", tb16_balS, 16, 1, 0);
  ok &= check_kernel("tb4", tb4_nat, 4, 1, 0);
  ok &= check_kernel("tb2", tb2_nat, 2, 1, 0);
  int kc8 = !check_kernel("BROKEN8", broken_g20, 8, 1, 1), kc16 = !check_kernel("BROKEN16", broken_g52, 16, 1, 1);
  printf("CHECK the broken kernels alone (g20 and g52, outputs 5 and 6 swapped): %s, %s\n", kc8 ? "CAUGHT (good)" : "NOT CAUGHT",
         kc16 ? "CAUGHT (good)" : "NOT CAUGHT");
  ok &= kc8 && kc16;
  ok &= check_inlane();
  printf("# active configuration: in-lane form %s; thresholds 8-vector / 16-vector per 2^L:", FORMNAME[g_form]);
  for (int L = 1; L <= maxL; L++) printf(" %d:%d/%d", L, g_thr[0][L], g_thr[1][L]);
  printf("\n");
  int caught_all = 1, form0 = g_form;
  long nsweep = 0;
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
    /* (1) every program, exactly as timed (active form and thresholds) */
    for (int p = 0; p < NPR; p++) {
      memcpy(y, x, n * sizeof(ET));
      prun(&PR[p], y, L);
      double sc = pscale(&PR[p], L);
      long bad = mismatches(y, r, n, sc);
      lok &= bad == 0;
      if (bad || L >= 8 || L <= 3)
        printf("CHECK %s whole 2^%-2d %-13s exact on integers (output = H x * %g): %ld wrong of %zu %s\n", XNAME, L,
               PR[p].name, sc, bad, n, bad ? "FAIL" : "PASS");
    }
    /* (2) every hybrid in every in-lane form at every threshold candidate (anything tune may choose) */
    int cc[8], nc = thr_cands(L, cc);
    long sbad = 0, scount = 0;
    for (int f = 0; f < 3; f++)
      for (int v = 0; v < NHV; v++)
        for (int q = 0; q < nc; q++) {
          g_form = f;
          memcpy(y, x, n * sizeof(ET));
          h5(y, L, &HV[v], cc[q]);
          long bad = mismatches(y, r, n, hscale(&HV[v], L, cc[q]));
          if (bad) printf("CHECK %s whole 2^%-2d %-13s form %d thr %d: %ld wrong FAIL\n", XNAME, L, HV[v].name, f, cc[q], bad);
          sbad += bad != 0;
          scount++;
        }
    g_form = form0;
    nsweep += scount;
    if (sbad || L >= 8)
      printf("CHECK %s whole 2^%-2d sweep: %d hybrids x 3 in-lane forms x %d thresholds (%d..%d) = %ld transforms, %ld wrong %s\n",
             XNAME, L, NHV, nc, cc[0], cc[nc - 1], scount, sbad, sbad ? "FAIL" : "PASS");
    lok &= sbad == 0;
    /* (3) the broken copies must fail wherever their plan runs the broken kernel; every L >= 8 must run it */
    const hvar *BB[2] = {&HB8, &HB16};
    for (int b = 0; b < 2; b++) {
      int R = b ? 4 : 3, runs = 0, caught = 0;
      for (int f = 0; f < 3; f++)
        for (int q = 0; q < nc; q++) {
          if (!nsteps(L, BB[b], cc[q], R)) continue;
          g_form = f;
          memcpy(y, x, n * sizeof(ET));
          h5(y, L, BB[b], cc[q]);
          runs++;
          caught += mismatches(y, r, n, 1.0) > 0;
        }
      g_form = form0;
      int need = (L >= 8);
      if (runs != caught || (need && runs == 0)) caught_all = 0;
      if (runs || L >= 8)
        printf("CHECK %s whole 2^%-2d %-19s plans that run it: %d, failed (caught): %d %s\n", XNAME, L, BB[b]->name, runs,
               caught, runs == caught && (runs || !need) ? "(good)" : "(THE GATE IS BLIND)");
    }
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
        printf("CHECK %s whole 2^%-2d %-13s real inputs: rel err %.3e (tol %.0e) %s\n", XNAME, L, PR[p].name, e / mx, tol,
               pass ? "PASS" : "FAIL");
      }
    }
    free(x); free(y); free(r);
  }
  printf("CHECK sweep total: %ld hybrid transforms (every form, every threshold candidate) exact\n", nsweep);
  printf("CHECK the deliberately broken copies (%s, %s) fail in every plan that runs them, and every L >= 8 runs them "
         "(up to 2^%d): %s\n", HB8.name, HB16.name, maxL, caught_all ? "YES (good)" : "NO (the gate is blind)");
  ok &= caught_all;
  printf("ALL %s\n", ok ? "PASS" : "FAIL");
  return !ok;
}

/* ---- tune: the textbook picks the in-lane form and the thresholds; the circuits inherit them ---- */
typedef struct { const hvar *H; int form, thr; long k; double t[16]; } tcfg;
static double tune_ms = 10.0;
static int tune_reps = 5;
static double tcall(tcfg *c, ET *buf, const ET *init, int L, long k) { /* ns per point over k calls (same array) */
  memcpy(buf, init, ((size_t)1 << L) * sizeof(ET));
  g_form = c->form;
  uint64_t t0 = bench_now_ns();
  for (long i = 0; i < k; i++) h5(buf, L, c->H, c->thr);
  return (double)(bench_now_ns() - t0) / ((double)k * (double)((size_t)1 << L));
}
static double dmed(double *a, int n) {
  double t[16];
  memcpy(t, a, n * sizeof(double));
  qsort(t, n, sizeof(double), bench_cmp_d);
  return n & 1 ? t[n / 2] : 0.5 * (t[n / 2 - 1] + t[n / 2]);
}
static void tune_cmp(tcfg *c, int nc, int L) { /* programs take turns, tune_reps rounds of >= tune_ms each */
  size_t n = (size_t)1 << L;
  ET *init = bench_alloc(n * sizeof(ET)), *buf = bench_alloc(n * sizeof(ET));
  for (size_t i = 0; i < n; i++) init[i] = (ET)bench_rand_pm1();
  for (int j = 0; j < nc; j++) { /* calibrate: warm-up, then enough calls for tune_ms */
    tcall(&c[j], buf, init, L, 1);
    long k = 1;
    for (;;) {
      double ns = tcall(&c[j], buf, init, L, k) * k * n;
      if (ns >= tune_ms * 1e6) break;
      k = ns < tune_ms * 1e6 / 16 ? k * 8 : (long)ceil(k * tune_ms * 1e6 * 1.1 / ns);
    }
    c[j].k = k;
  }
  for (int r = 0; r < tune_reps; r++)
    for (int jj = 0; jj < nc; jj++) {
      int j = (jj + r) % nc;
      c[j].t[r] = tcall(&c[j], buf, init, L, c[j].k);
    }
  free(init); free(buf);
}
static int tune(void) {
  if (getenv("H512_TUNE_MS")) tune_ms = atof(getenv("H512_TUNE_MS"));
  if (getenv("H512_TUNE_REPS")) tune_reps = atoi(getenv("H512_TUNE_REPS"));
  if (tune_reps < 1) tune_reps = 1;
  if (tune_reps > 16) tune_reps = 16;
  printf("# tune %s: %d rounds of >= %.1f ms per configuration, configurations take turns; same array; ns per point; "
         "textbook variants only\n", XNAME, tune_reps, tune_ms);
  /* 1. in-lane form: the five textbook hybrids x three forms at 2^10 and 2^14 (default thresholds) */
  const int TV[5] = {H8TB, H8TBBAL, H8TBBALS, H8TBMIX, H16TBMIX};
  const int TL[2] = {10, 14};
  double score[3] = {0, 0, 0};
  for (int a = 0; a < 2; a++) {
    int L = TL[a];
    tcfg c[15];
    for (int f = 0; f < 3; f++)
      for (int v = 0; v < 5; v++) c[f * 5 + v] = (tcfg){&HV[TV[v]], f, hthr(&HV[TV[v]], L), 0, {0}};
    tune_cmp(c, 15, L);
    for (int f = 0; f < 3; f++) {
      double best = 1e30;
      for (int v = 0; v < 5; v++) {
        double m = dmed(c[f * 5 + v].t, tune_reps);
        printf("TUNEFORM 2^%d form %d %-11s thr %d median %.4f\n", L, f, HV[TV[v]].name, c[f * 5 + v].thr, m);
        if (m < best) best = m;
      }
      score[f] += best;
    }
  }
  int bf = 0;
  for (int f = 1; f < 3; f++) if (score[f] < score[bf]) bf = f;
  printf("TUNEFORM score (sum over 2^10, 2^14 of the best textbook's median): F %.4f, A %.4f, X %.4f -> %s\n", score[0],
         score[1], score[2], FORMNAME[bf]);
  printf("FORM %d\n", bf);
  g_form = bf;
  /* 2. thresholds per n, per structure: 8-vector by the better of h8-tbmix and h8-tbbalS, 16-vector by h16-tbmix */
  for (int L = 8; L <= 20; L++) {
    int cc[8], nc = thr_cands(L, cc);
    tcfg c[24];
    int m = 0;
    for (int q = 0; q < nc; q++) {
      c[m++] = (tcfg){&HV[H8TBMIX], bf, cc[q], 0, {0}};
      c[m++] = (tcfg){&HV[H8TBBALS], bf, cc[q], 0, {0}};
      c[m++] = (tcfg){&HV[H16TBMIX], bf, cc[q], 0, {0}};
    }
    tune_cmp(c, m, L);
    for (int s = 0; s < 2; s++) {
      double best = 1e30;
      int bt = cc[0];
      for (int j = 0; j < m; j++) {
        if (c[j].H->tbl != s) continue;
        double md = dmed(c[j].t, tune_reps);
        printf("TUNETHR %d 2^%d thr %d %-11s median %.4f\n", s, L, c[j].thr, c[j].H->name, md);
        if (md < best) { best = md; bt = c[j].thr; }
      }
      printf("THR %d %d %d\n", s, L, bt);
      g_thr[s][L] = bt;
    }
    fflush(stdout);
  }
  g_form = bf;
  return 0;
}

/* ---- timing ---- */
typedef struct { int L; const prog *p; bench_pool pool; ET *init; } hctx;
static void h_reset(void *v) {
  hctx *c = v;
  for (int i = 0; i < c->pool.count; i++) memcpy(c->pool.buf[i], c->init, ((size_t)1 << c->L) * sizeof(ET));
}
static void h_run(void *v, long i) { hctx *c = v; prun(c->p, bench_pool_get(&c->pool, i), c->L); }

int main(int argc, char **argv) {
  bench_init();
  wk_init();
  thr_defaults();
  if (getenv("H512_TUNE") && *getenv("H512_TUNE")) load_tune(getenv("H512_TUNE"));
  printf("# bench_h512 %s, %d lanes, %d vector registers, compiler %s, FFHT %s, in-lane form %s\n", XNAME, LANES, NREGS,
         __VERSION__,
#ifdef WITH_FFHT
         "linked",
#else
         "NOT linked",
#endif
         FORMNAME[g_form]);
  if (argc < 2 || !strcmp(argv[1], "check")) return hcheck(argc > 2 ? atoi(argv[2]) : 20);
  if (!strcmp(argv[1], "tune")) return tune();
  if (!strcmp(argv[1], "trace") && argc > 3) { /* trace K L...: the step sequence, as check_plan.py reads it */
    const hvar *H = atoi(argv[2]) == 4 ? &HV[H16TBMIX] : &HV[H8TB];
    for (int a = 3; a < argc; a++) {
      int L = atoi(argv[a]);
      ET *b = bench_alloc(((size_t)1 << L) * sizeof(ET));
      printf("L %d thr %d\n", L, hthr(H, L));
      g_trace = 1; g_trace_base = b;
      h5(b, L, H, hthr(H, L));
      g_trace = 0;
      free(b);
    }
    return 0;
  }
  if (!strcmp(argv[1], "plan")) {
    char s8[512], s16[512];
    for (int a = 2; a < argc; a++) {
      int L = atoi(argv[a]);
      plan_text(s8, sizeof s8, L, &HV[H8TB], hthr(&HV[H8TB], L));
      plan_text(s16, sizeof s16, L, &HV[H16TBMIX], hthr(&HV[H16TBMIX], L));
      printf("PLAN 2^%d form %s | h8: %s (3-level steps per element %d) | h16: %s (4-level %d, 3-level %d)\n", L,
             FORMNAME[g_form], s8, nsteps(L, &HV[H8TB], hthr(&HV[H8TB], L), 3), s16,
             nsteps(L, &HV[H16TBMIX], hthr(&HV[H16TBMIX], L), 4), nsteps(L, &HV[H16TBMIX], hthr(&HV[H16TBMIX], L), 3));
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
      plan_text(s8, sizeof s8, L, &HV[H8TB], hthr(&HV[H8TB], L));
      plan_text(s16, sizeof s16, L, &HV[H16TBMIX], hthr(&HV[H16TBMIX], L));
      printf("# PLAN 2^%d: form %s; h8 %s; h16 %s\n", L, FORMNAME[g_form], s8, s16);
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
      snprintf(t, sizeof t, "x86-hybrid512 whole %s 2^%d %s", XNAME, L, mode ? "separate" : "same");
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
  fprintf(stderr, "usage: %s check [maxL] | tune | trace 3|4 L... | plan L... | whole same|separate L...\n", argv[0]);
  return 2;
}
