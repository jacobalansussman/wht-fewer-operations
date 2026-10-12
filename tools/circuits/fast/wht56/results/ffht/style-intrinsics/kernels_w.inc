/* kernels_w.inc -- the staggered transforms (STAGGER = 1 in impl.inc), one per 8-point step, for
 * the number type and the style (SFX, PIN) that the includer has set.  As in kernels.inc, the
 * blocks differ only in the macros that name the step; here the step is also given in its two
 * halves (kern.h, "The steps in two halves").
 *
 *   name   every 8-register pass     the one pass that gets P          result
 *   T      textbook, 24 add/sub      the same                          H x
 *   N      19 add/sub + 1 mul        the same                          H x / 2^P
 *   NF     17 add/sub + 2 fmsub      the same                          H x / 2^P
 *   Nc     as N                      7 add/sub + 1 mul + 12 fma, 2^P   H x
 *   NFc    as NF                     7 add/sub + 1 mul + 12 fma, 2^P   H x
 *   G      7 add/sub + 12 fma        the same                          H x
 */
#define NM2(a, b, c) whti_##a##b##_##c
#define NM1(a, b, c) NM2(a, b, c)
#define VNAME(kern) NM1(kern, SFX, TSUF)
#define POW2(P) ((ELT)((uint64_t)1 << (P)))
#define SWEEP_L(P) 0

#define NAME VNAME(T)
#define KDECL
#define KDECL_L(P)
#define KERNEL KERNEL_T
#define KERNEL_L KERNEL_T
#define KCARRY KT_CARRY
#define KFRONT KT_FRONT
#define KBACK KT_BACK
#define KFRONT_L KT_FRONT
#define KBACK_L KT_BACK
#include "impl.inc"
#undef NAME
#undef KDECL
#undef KDECL_L
#undef KERNEL
#undef KERNEL_L
#undef KCARRY
#undef KFRONT
#undef KBACK
#undef KFRONT_L
#undef KBACK_L

#define NAME VNAME(N)
#define KDECL const V K_HALF = SET1((ELT)0.5);
#define KDECL_L(P) const V K_HALF = SET1((ELT)0.5);
#define KERNEL KERNEL_N
#define KERNEL_L KERNEL_N
#define KCARRY KN_CARRY
#define KFRONT KN_FRONT
#define KBACK KN_BACK
#define KFRONT_L KN_FRONT
#define KBACK_L KN_BACK
#include "impl.inc"
#undef NAME
#undef KDECL
#undef KDECL_L
#undef KERNEL
#undef KERNEL_L
#undef KCARRY
#undef KFRONT
#undef KBACK
#undef KFRONT_L
#undef KBACK_L

#define NAME VNAME(NF)
#define KDECL const V K_HALF = SET1((ELT)0.5);
#define KDECL_L(P) const V K_HALF = SET1((ELT)0.5);
#define KERNEL KERNEL_NF
#define KERNEL_L KERNEL_NF
#define KCARRY KN_CARRY
#define KFRONT KNF_FRONT
#define KBACK KNF_BACK
#define KFRONT_L KNF_FRONT
#define KBACK_L KNF_BACK
#include "impl.inc"
#undef NAME
#undef KDECL
#undef KDECL_L
#undef KERNEL
#undef KERNEL_L
#undef KCARRY
#undef KFRONT
#undef KBACK
#undef KFRONT_L
#undef KBACK_L

#define NAME VNAME(Nc)
#define KDECL const V K_HALF = SET1((ELT)0.5);
#define KDECL_L(P) const V K_C = SET1(POW2(P)); const V K_CH = SET1((ELT)0.5 * POW2(P));
#define KERNEL KERNEL_N
#define KERNEL_L KERNEL_NC
#define KCARRY KN_CARRY
#define KFRONT KN_FRONT
#define KBACK KN_BACK
#define KFRONT_L KNC_FRONT
#define KBACK_L KNC_BACK
#include "impl.inc"
#undef NAME
#undef KDECL
#undef KDECL_L
#undef KERNEL
#undef KERNEL_L
#undef KCARRY
#undef KFRONT
#undef KBACK
#undef KFRONT_L
#undef KBACK_L

#define NAME VNAME(NFc)
#define KDECL const V K_HALF = SET1((ELT)0.5);
#define KDECL_L(P) const V K_C = SET1(POW2(P)); const V K_CH = SET1((ELT)0.5 * POW2(P));
#define KERNEL KERNEL_NF
#define KERNEL_L KERNEL_NC
#define KCARRY KN_CARRY
#define KFRONT KNF_FRONT
#define KBACK KNF_BACK
#define KFRONT_L KNC_FRONT
#define KBACK_L KNC_BACK
#include "impl.inc"
#undef NAME
#undef KDECL
#undef KDECL_L
#undef KERNEL
#undef KERNEL_L
#undef KCARRY
#undef KFRONT
#undef KBACK
#undef KFRONT_L
#undef KBACK_L

#define NAME VNAME(G)
#define KDECL const V K_TWO = SET1((ELT)2.0);
#define KDECL_L(P) const V K_TWO = SET1((ELT)2.0);
#define KERNEL KERNEL_G
#define KERNEL_L KERNEL_G
#define KCARRY KN_CARRY
#define KFRONT KNF_FRONT
#define KBACK KG_BACK
#define KFRONT_L KNF_FRONT
#define KBACK_L KG_BACK
#include "impl.inc"
#undef NAME
#undef KDECL
#undef KDECL_L
#undef KERNEL
#undef KERNEL_L
#undef KCARRY
#undef KFRONT
#undef KBACK
#undef KFRONT_L
#undef KBACK_L

#undef SWEEP_L
#undef NM2
#undef NM1
#undef VNAME
#undef POW2
