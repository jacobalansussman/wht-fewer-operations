/* whtc_ffht_plan.h -- FFHT's plan of passes, copied word for word from the timed harness
 * (measurements/2026-10-22/x86/harness-hybrid/bench_hyb.c, and scalar_wht from bench_k0.c); check_same_as_harness.py
 * compares them.  Not a public header: whtc_impl.h includes it once per precision.
 *
 * What is FFHT's here, under FFHT's MIT licence (LICENSE-FFHT in this folder; Copyright (c) 2015 Alexandr Andoni,
 * Piotr Indyk, Thijs Laarhoven, Ilya Razenshteyn, Ludwig Schmidt): the recursion thresholds FFHT_THR_F and FFHT_THR_D
 * (FFHT's hall_of_fame_avx.txt at commit fba727a3), the in-lane instruction sequences of ffht_inlane (FFHT's gen.py,
 * written here with intrinsics), and the order of passes that hyb_block and hyb_rec follow (FFHT's greedy_merged and
 * greedy_merged_recursive).  The C text itself was written for this repository.
 */
/* this kernel does not trace its plan (the timing program printed it with HTRACE to compare it with FFHT's) */
#define HTRACE(base, A, B, C, m, lanes) do { } while (0)

static const int FFHT_THR_F[31] = {0,  1,  2,  3,  4,  5,  6,  7,  6,  9,  10, 11, 12, 11, 12, 13,
                                   13, 12, 12, 13, 12, 9,  11, 9,  12, 7,  12, 12, 7,  12, 6};
static const int FFHT_THR_D[31] = {0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  10, 11, 11, 11, 12, 12,
                                   11, 11, 12, 11, 9,  7,  11, 11, 10, 8,  11, 9,  11, 11, 9};
static int ffht_thr(int L) { return sizeof(ET) == 4 ? FFHT_THR_F[L] : FFHT_THR_D[L]; }

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

static void scalar_wht(ET *x, int L) {
  size_t n = (size_t)1 << L;
  for (size_t h = 1; h < n; h <<= 1)
    for (size_t i = 0; i < n; i += 2 * h)
      for (size_t j = i; j < i + h; j++) { ET a = x[j], b = x[j + h]; x[j] = a + b; x[j + h] = a - b; }
}

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

typedef struct {
  const char *name;
  int K;               /* cross-vector levels per full step: 3 (8 vectors, FFHT's) or 4 (16 vectors) */
  hfirst_fn first[5];  /* by number of cross levels r = 0..K in the block's first step */
  hstep_fn step[5];    /* by number of levels r = 1..K */
  double s8;           /* output scale of the 3-level kernel (h20half: 0.5) */
} hvar;
#define HV8(NM, K8, S8) \
  {NM, 3, {hfirst_kid_nat, hfirst_tb2_nat, hfirst_tb4_nat, hfirst_##K8, NULL}, {NULL, hstep_tb2_nat, hstep_tb4_nat, hstep_##K8, NULL}, S8}

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
