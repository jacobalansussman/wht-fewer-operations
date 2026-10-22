/* whtc_steps.h -- the in-register steps of the kernel, copied word for word from the timed harness
 * (measurements/2026-10-22/x86/harness-hybrid: tb2_nat and kid_nat from bench_hyb.c; tb4_nat, tb8_nat, tb8_balS and
 * g20_nat from kernels_k0.h, which gen_x86.py generated from the circuit files).  check_same_as_harness.py compares
 * them.  Not a public header: whtc_impl.h includes it once per precision.  Every step takes the R vectors v[0..R-1]
 * in place; "one" is the constant 1 in a register the compiler cannot see through (only tb8_balS uses it).
 * V_ADD, V_SUB, V_FMA, V_FMS, V_RFMS and FMADD are defined by the file that includes this one.
 * Licence: Apache-2.0, as the rest of this repository (see README.md in this folder). */

static inline void kid_nat(V *v, V one) { (void)v; (void)one; }
static inline void tb2_nat(V *v, V one) {
  (void)one;
  V a = v[0], b = v[1];
  v[0] = V_ADD(a, b);
  v[1] = V_SUB(a, b);
}

/* tb4_nat: 4 points, 8 lines {'ADD': 4, 'SUB': 4}; from h4_textbook_8.txt */
static inline void tb4_nat(V *v, V one) {
  (void)one;
  V x0 = v[0]; V x1 = v[1]; V x2 = v[2]; V x3 = v[3];
  V t1 = V_ADD(x0, x1);
  V t2 = V_SUB(x0, x1);
  V t3 = V_ADD(x2, x3);
  V t4 = V_SUB(x2, x3);
  V t5 = V_ADD(t1, t3);
  V t6 = V_SUB(t1, t3);
  V t7 = V_ADD(t2, t4);
  V t8 = V_SUB(t2, t4);
  v[0] = t5;
  v[1] = t7;
  v[2] = t6;
  v[3] = t8;
}

/* tb8_nat: 8 points, 24 lines {'ADD': 12, 'SUB': 12}; from h8_textbook_24.txt */
static inline void tb8_nat(V *v, V one) {
  (void)one;
  V x0 = v[0]; V x1 = v[1]; V x2 = v[2]; V x3 = v[3]; V x4 = v[4]; V x5 = v[5]; V x6 = v[6]; V x7 = v[7];
  V t1 = V_ADD(x0, x1);
  V t2 = V_SUB(x0, x1);
  V t3 = V_ADD(x2, x3);
  V t4 = V_SUB(x2, x3);
  V t5 = V_ADD(x4, x5);
  V t6 = V_SUB(x4, x5);
  V t7 = V_ADD(x6, x7);
  V t8 = V_SUB(x6, x7);
  V t9 = V_ADD(t1, t3);
  V t10 = V_SUB(t1, t3);
  V t11 = V_ADD(t2, t4);
  V t12 = V_SUB(t2, t4);
  V t13 = V_ADD(t5, t7);
  V t14 = V_SUB(t5, t7);
  V t15 = V_ADD(t6, t8);
  V t16 = V_SUB(t6, t8);
  V t17 = V_ADD(t9, t13);
  V t18 = V_SUB(t9, t13);
  V t19 = V_ADD(t11, t15);
  V t20 = V_SUB(t11, t15);
  V t21 = V_ADD(t10, t14);
  V t22 = V_SUB(t10, t14);
  V t23 = V_ADD(t12, t16);
  V t24 = V_SUB(t12, t16);
  v[0] = t17;
  v[1] = t19;
  v[2] = t21;
  v[3] = t23;
  v[4] = t18;
  v[5] = t20;
  v[6] = t22;
  v[7] = t24;
}

/* tb8_balS: 8 points, 24 lines {'FMA1': 12, 'SUB': 12} PIPE-BALANCED, SUB BEFORE FMA; from h8_textbook_24.txt */
static inline void tb8_balS(V *v, V one) {
  (void)one;
  V x0 = v[0]; V x1 = v[1]; V x2 = v[2]; V x3 = v[3]; V x4 = v[4]; V x5 = v[5]; V x6 = v[6]; V x7 = v[7];
  V t2 = V_SUB(x0, x1);
  V t1 = FMADD(x1, one, x0);
  V t4 = V_SUB(x2, x3);
  V t3 = FMADD(x3, one, x2);
  V t6 = V_SUB(x4, x5);
  V t5 = FMADD(x5, one, x4);
  V t8 = V_SUB(x6, x7);
  V t7 = FMADD(x7, one, x6);
  V t10 = V_SUB(t1, t3);
  V t9 = FMADD(t3, one, t1);
  V t12 = V_SUB(t2, t4);
  V t11 = FMADD(t4, one, t2);
  V t14 = V_SUB(t5, t7);
  V t13 = FMADD(t7, one, t5);
  V t16 = V_SUB(t6, t8);
  V t15 = FMADD(t8, one, t6);
  V t18 = V_SUB(t9, t13);
  V t17 = FMADD(t13, one, t9);
  V t20 = V_SUB(t11, t15);
  V t19 = FMADD(t15, one, t11);
  V t22 = V_SUB(t10, t14);
  V t21 = FMADD(t14, one, t10);
  V t24 = V_SUB(t12, t16);
  V t23 = FMADD(t16, one, t12);
  v[0] = t17;
  v[1] = t19;
  v[2] = t21;
  v[3] = t23;
  v[4] = t18;
  v[5] = t20;
  v[6] = t22;
  v[7] = t24;
}

/* g20_nat: 8 points, 20 lines {'ADD': 5, 'FMA': 3, 'FMS': 4, 'RFMS': 5, 'SUB': 3}; from h8_G20_family.txt */
static inline void g20_nat(V *v, V one) {
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
  V p14 = V_RFMS(p12, p4, 2.0);
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
