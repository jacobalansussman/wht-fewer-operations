/* kernels.inc -- one transform per 8-point step, for the number type and the style (SFX, PIN,
 * INREG) that the includer has set.  Each block below names the step and includes impl.inc; the
 * blocks differ in nothing else.
 *
 *   name   every 8-register pass   the one pass that gets P      result
 *   T      KERNEL_T (24 add/sub)   the same                      H x
 *   N      KERNEL_N (19 + 1 mul)   the same                      H x / 2^P   ("up to scale")
 *   NF     KERNEL_NF (17 + 2 fms)  the same                      H x / 2^P
 *   Nm     KERNEL_N                KERNEL_NM: 8 more mul by 2^P  H x
 *   Nc     KERNEL_N                KERNEL_NC: 7 + 1 mul + 12 fma H x
 *   NFc    KERNEL_NF               KERNEL_NC                     H x
 *   Ns     KERNEL_N                the same, then a loop that multiplies every number by 2^P   H x
 *   G      KERNEL_G (7 + 12 fma)   the same                      H x
 *   N2,N3  KERNEL_N in two other orders of its lines             H x / 2^P
 */
#define NM2(a, b, c) whti_##a##b##_##c
#define NM1(a, b, c) NM2(a, b, c)
#define VNAME(kern) NM1(kern, SFX, TSUF)
#define POW2(P) ((ELT)((uint64_t)1 << (P)))

#define NAME VNAME(T)
#define KDECL
#define KDECL_L(P)
#define KERNEL KERNEL_T
#define KERNEL_L KERNEL_T
#define SWEEP_L(P) 0
#include "impl.inc"
#undef NAME
#undef KDECL
#undef KDECL_L
#undef KERNEL
#undef KERNEL_L
#undef SWEEP_L

#define NAME VNAME(N)
#define KDECL const V K_HALF = SET1((ELT)0.5);
#define KDECL_L(P) const V K_HALF = SET1((ELT)0.5);
#define KERNEL KERNEL_N
#define KERNEL_L KERNEL_N
#define SWEEP_L(P) 0
#include "impl.inc"
#undef NAME
#undef KDECL
#undef KDECL_L
#undef KERNEL
#undef KERNEL_L
#undef SWEEP_L

#define NAME VNAME(NF)
#define KDECL const V K_HALF = SET1((ELT)0.5);
#define KDECL_L(P) const V K_HALF = SET1((ELT)0.5);
#define KERNEL KERNEL_NF
#define KERNEL_L KERNEL_NF
#define SWEEP_L(P) 0
#include "impl.inc"
#undef NAME
#undef KDECL
#undef KDECL_L
#undef KERNEL
#undef KERNEL_L
#undef SWEEP_L

#define NAME VNAME(Nm)
#define KDECL const V K_HALF = SET1((ELT)0.5);
#define KDECL_L(P) const V K_HALF = SET1((ELT)0.5); const V K_C = SET1(POW2(P));
#define KERNEL KERNEL_N
#define KERNEL_L KERNEL_NM
#define SWEEP_L(P) 0
#include "impl.inc"
#undef NAME
#undef KDECL
#undef KDECL_L
#undef KERNEL
#undef KERNEL_L
#undef SWEEP_L

#define NAME VNAME(Nc)
#define KDECL const V K_HALF = SET1((ELT)0.5);
#define KDECL_L(P) const V K_C = SET1(POW2(P)); const V K_CH = SET1((ELT)0.5 * POW2(P));
#define KERNEL KERNEL_N
#define KERNEL_L KERNEL_NC
#define SWEEP_L(P) 0
#include "impl.inc"
#undef NAME
#undef KDECL
#undef KDECL_L
#undef KERNEL
#undef KERNEL_L
#undef SWEEP_L

#define NAME VNAME(NFc)
#define KDECL const V K_HALF = SET1((ELT)0.5);
#define KDECL_L(P) const V K_C = SET1(POW2(P)); const V K_CH = SET1((ELT)0.5 * POW2(P));
#define KERNEL KERNEL_NF
#define KERNEL_L KERNEL_NC
#define SWEEP_L(P) 0
#include "impl.inc"
#undef NAME
#undef KDECL
#undef KDECL_L
#undef KERNEL
#undef KERNEL_L
#undef SWEEP_L

#define NAME VNAME(Ns)
#define KDECL const V K_HALF = SET1((ELT)0.5);
#define KDECL_L(P) const V K_HALF = SET1((ELT)0.5);
#define KERNEL KERNEL_N
#define KERNEL_L KERNEL_N
#define SWEEP_L(P) 1
#include "impl.inc"
#undef NAME
#undef KDECL
#undef KDECL_L
#undef KERNEL
#undef KERNEL_L
#undef SWEEP_L

#define NAME VNAME(G)
#define KDECL const V K_TWO = SET1((ELT)2.0);
#define KDECL_L(P) const V K_TWO = SET1((ELT)2.0);
#define KERNEL KERNEL_G
#define KERNEL_L KERNEL_G
#define SWEEP_L(P) 0
#include "impl.inc"
#undef NAME
#undef KDECL
#undef KDECL_L
#undef KERNEL
#undef KERNEL_L
#undef SWEEP_L

#ifdef WITH_ORDERS
#define NAME VNAME(N2)
#define KDECL const V K_HALF = SET1((ELT)0.5);
#define KDECL_L(P) const V K_HALF = SET1((ELT)0.5);
#define KERNEL KERNEL_N2
#define KERNEL_L KERNEL_N2
#define SWEEP_L(P) 0
#include "impl.inc"
#undef NAME
#undef KDECL
#undef KDECL_L
#undef KERNEL
#undef KERNEL_L
#undef SWEEP_L

#define NAME VNAME(N3)
#define KDECL const V K_HALF = SET1((ELT)0.5);
#define KDECL_L(P) const V K_HALF = SET1((ELT)0.5);
#define KERNEL KERNEL_N3
#define KERNEL_L KERNEL_N3
#define SWEEP_L(P) 0
#include "impl.inc"
#undef NAME
#undef KDECL
#undef KDECL_L
#undef KERNEL
#undef KERNEL_L
#undef SWEEP_L
#endif

#undef NM2
#undef NM1
#undef VNAME
#undef POW2
