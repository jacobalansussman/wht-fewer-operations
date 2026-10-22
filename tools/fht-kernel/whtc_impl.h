/* whtc_impl.h -- internal: the kernel for one precision.  whtc_avx2.c and whtc_plain.c include it twice, once for
 * float and once for double, after defining the vector type and its operations exactly as the timed harness did
 * (bench_k0.c): ET, V, LANES, LOGL, XT, LD, ST, SET1, V_ADD, V_SUB, FMADD, FNMADD, FMSUB, MULV and OPQ (and
 * inlane_all for the portable code).  It defines whtc_run(buf, log_n): FFHT's plan with the chosen 8-point step. */

/* the multiply-add forms of the circuit lines, as bench_k0.c defines them; every constant c here is 1 or 2, so the
 * product is exact and one rounding happens per line, as in a plain addition */
#define V_FMA(a, b, c) FMADD((b), SET1((ET)(c)), (a))  /* a + b*c */
#define V_FMS(a, b, c) FNMADD((b), SET1((ET)(c)), (a)) /* a - b*c */
#define V_RFMS(a, b, c) FMSUB((b), SET1((ET)(c)), (a)) /* b*c - a */
#define V_MUL(a, c) MULV((a), SET1((ET)(c)))

#include "whtc_steps.h"
#include "whtc_ffht_plan.h"

DEFHYB(kid_nat, 1)
DEFHYB(tb2_nat, 2)
DEFHYB(tb4_nat, 4)
#if defined(WHTC_BREAK)
/* the broken copy that the tests must catch: g20_nat with ONE line changed (the sign of p12 in p14) */
static inline void g20_broken(V *v, V one) {
  (void)one;
  V x0 = v[0]; V x1 = v[1]; V x2 = v[2]; V x3 = v[3]; V x4 = v[4]; V x5 = v[5]; V x6 = v[6]; V x7 = v[7];
  V p1 = V_ADD(x0, x1);
  V p2 = V_SUB(x2, x3);
  V hub3 = V_SUB(p1, p2);
  V p4 = V_FMA(hub3, x2, 2.0);
  V p5 = V_RFMS(hub3, x0, 2.0);
  V p6 = V_ADD(x4, x5);
  V p7 = V_SUB(x6, x7);
  V hub8 = V_ADD(p6, p7);
  V p9 = V_FMS(hub8, x6, 2.0);
  V p10 = V_RFMS(hub8, x4, 2.0);
  V hub11 = V_ADD(p4, p9);
  V p12 = V_FMS(hub11, p6, 2.0);
  V p13 = V_RFMS(hub11, p1, 2.0);
  V p14 = V_FMA(p12, p4, 2.0); /* the timed g20_nat has V_RFMS here: p14 = 2*p4 - p12 */
  V p15 = V_FMA(p13, p9, 2.0);
  V hub16 = V_ADD(p5, p10);
  V p17 = V_FMA(hub16, p7, 2.0);
  V p18 = V_FMS(hub16, p2, 2.0);
  V p19 = V_RFMS(p17, p5, 2.0);
  V p20 = V_FMS(p18, p10, 2.0);
  v[0] = p14;
  v[1] = p17;
  v[2] = p15;
  v[3] = p18;
  v[4] = p12;
  v[5] = p19;
  v[6] = p13;
  v[7] = p20;
}
DEFHYB(g20_broken, 8)
static const hvar whtc_hv = HV8("g20, broken copy", g20_broken, 1.0);
#elif WHTC_STEP_ID == 1
DEFHYB(g20_nat, 8)
static const hvar whtc_hv = HV8("g20", g20_nat, 1.0);
#elif WHTC_STEP_ID == 2
DEFHYB(tb8_balS, 8)
static const hvar whtc_hv = HV8("tb8balS", tb8_balS, 1.0);
#else
DEFHYB(tb8_nat, 8)
static const hvar whtc_hv = HV8("tb8", tb8_nat, 1.0);
#endif

static void whtc_run(ET *buf, int log_n) { hyb(buf, log_n, &whtc_hv); }

#undef V_FMA
#undef V_FMS
#undef V_RFMS
#undef V_MUL
#undef HTRACE
#undef DEFHYB
#undef HV8
