/* three.inc -- the three steps for one number type and one setting of PIN.  Included by whtf.c.
 * Needs: PFX (wht_f_, wht_d_, wht_i_), SFX (empty or p), PIN(v), and for the fused lines
 * FKDECL, FPL2, FMI2, FRS2. */
#define NM2(a, b, c) a##b##c
#define NM1(a, b, c) NM2(a, b, c)
#define NM(v) NM1(PFX, v, SFX)

#define NAME NM(T)
#define KDECL
#define KERNEL KERNEL_T
#include "impl.inc"
#undef NAME
#undef KDECL
#undef KERNEL

#define NAME NM(G19)
#define KDECL FKDECL
#define KERNEL KERNEL_G
#define PL2(a, b) FPL2(a, b)
#define MI2(a, b) FMI2(a, b)
#define RS2(a, b) FRS2(a, b)
#include "impl.inc"
#undef NAME
#undef KDECL
#undef PL2
#undef MI2
#undef RS2

#define NAME NM(G19a)
#define KDECL
#define PL2(a, b) ADD(ADD(a, b), b)
#define MI2(a, b) SUB(SUB(a, b), b)
#define RS2(a, b) ADD(SUB(b, a), b)
#include "impl.inc"
#undef NAME
#undef KDECL
#undef KERNEL
#undef PL2
#undef MI2
#undef RS2

#ifdef FONE_DECL
#define NAME NM(Tf)
#define KDECL FONE_DECL
#define KERNEL KERNEL_TF
#include "impl.inc"
#undef NAME
#undef KDECL
#undef KERNEL
#endif

#undef NM
#undef NM1
#undef NM2
