/* impl.inc -- one in-place Walsh-Hadamard transform  void NAME(ELT *buf, int k)  on 2^k numbers,
 * 3 <= k <= 30.  Output: natural order.  Included once per number type and per variant.
 *
 * EVERYTHING in this file and in plans.inc is the same text for every variant.  A variant
 * differs only in the macros below that name the step on 8 registers:
 *
 *   KERNEL(x0..x7), KDECL          the step used in every 8-register pass, and its constants
 *   KERNEL_L(x0..x7), KDECL_L(P)   the step used in ONE 8-register pass per transform (the one at
 *                                  the highest levels), with constants that may depend on P, the
 *                                  number of 8-register passes every number goes through.  For the
 *                                  variants that repair the scale there, this is where 2^P goes.
 *                                  For all others it is KERNEL again.
 *   SWEEP_L(P)                     1: after the transform, one loop multiplies every number by 2^P
 *
 * The rest is set per number type:
 *   ELT, V, W (numbers in a register), LOAD, STORE, ADD, SUB, MUL, SET1
 *   INREG_DECL, INREG(v)           the levels inside one register (levels 0..2 for 8 floats,
 *                                  0..1 for 4 doubles) and their constants
 *   STAGGER                        0: the passes as described below.  1: the 8-register passes
 *                                  with the instructions of neighbouring turns staggered (see
 *                                  the comment at the second pass3 below); then the step is given
 *                                  in two halves: KCARRY, KFRONT, KBACK (and KFRONT_L, KBACK_L)
 *   PIN(v)                         empty, or a barrier that makes the compiler put a loaded value
 *                                  into a register there (FFHT loads all 8 before it computes)
 *   PLAN_FLOAT or PLAN_DOUBLE      which half of plans.inc to take
 *
 * The passes (n numbers at buf; all bounds are constants where they are called, so the compiler
 * writes each loop for its own size, as FFHT's generator does):
 *   first1/2/4/8   the first pass: 1, 2, 4 or 8 neighbouring registers; the levels inside each
 *                  register, then 0, 1, 2 or 3 levels between them (3 levels = KERNEL)
 *   pass3          3 levels at distance S: 8 registers at p, p+S, .., p+7S through KERNEL
 *   pass2, pass1   2 levels on 4 registers, 1 level on 2 registers: textbook, the same in every variant
 * Which passes a size uses, in which order and on which blocks, is plans.inc: FFHT's own plan.
 */
#define FN2(a, b) a##_##b
#define FN1(a, b) FN2(a, b)
#define FN(s) FN1(NAME, s)
#define AINL static inline __attribute__((always_inline))

#define LOAD8(p, S) \
    V x0 = LOAD(p), x1 = LOAD((p) + (S)), x2 = LOAD((p) + 2 * (S)), x3 = LOAD((p) + 3 * (S)); \
    V x4 = LOAD((p) + 4 * (S)), x5 = LOAD((p) + 5 * (S)), x6 = LOAD((p) + 6 * (S)), x7 = LOAD((p) + 7 * (S)); \
    PIN(x0); PIN(x1); PIN(x2); PIN(x3); PIN(x4); PIN(x5); PIN(x6); PIN(x7);
#define STORE8(p, S) \
    STORE(p, x0); STORE((p) + (S), x1); STORE((p) + 2 * (S), x2); STORE((p) + 3 * (S), x3); \
    STORE((p) + 4 * (S), x4); STORE((p) + 5 * (S), x5); STORE((p) + 6 * (S), x6); STORE((p) + 7 * (S), x7);

#if !STAGGER
AINL void FN(pass3)(ELT *buf, size_t n, size_t S)
{
    KDECL
    for (size_t j = 0; j < n; j += 8 * S) {
        for (size_t i = 0; i < S; i += W) {
            ELT *p = buf + j + i;
            LOAD8(p, S)
            KERNEL(x0, x1, x2, x3, x4, x5, x6, x7);
            STORE8(p, S)
        }
    }
}

AINL void FN(pass3L)(ELT *buf, size_t n, size_t S, int P)
{
    (void)P;
    KDECL_L(P)
    for (size_t j = 0; j < n; j += 8 * S) {
        for (size_t i = 0; i < S; i += W) {
            ELT *p = buf + j + i;
            LOAD8(p, S)
            KERNEL_L(x0, x1, x2, x3, x4, x5, x6, x7);
            STORE8(p, S)
        }
    }
}
#else
/* STAGGER: the same passes with the instructions of neighbouring turns staggered.  One turn does
 * the second half of the step (BACK) for the 8 registers of the turn before, then the first half
 * (FRONT) for the 8 registers of this turn; a few registers carry the values from FRONT to BACK.
 * Every 8 registers get the same operations as in the plain pass, the same loads (BACK of the
 * new step reads six inputs from memory once more) and the same 8 stores.  Why: a value near the
 * end of the new step depends on a chain of 7 operations, the processor keeps only a limited
 * number of waiting instructions, and in program order the end of one step then stands beside
 * the start of the next, which does not have to wait. */
#define FRONT_AT(q, FRONTM) do { LOAD8(q, S) FRONTM(x0, x1, x2, x3, x4, x5, x6, x7); } while (0)
#define BACK_AT(q, BACKM) do { \
    const V u1 = LOAD((q) + S), u3 = LOAD((q) + 3 * S), u4 = LOAD((q) + 4 * S); \
    const V u5 = LOAD((q) + 5 * S), u6 = LOAD((q) + 6 * S), u7 = LOAD((q) + 7 * S); \
    (void)u1; (void)u3; (void)u4; (void)u5; (void)u6; (void)u7; \
    BACKM(u1, u3, u4, u5, u6, u7, y0, y1, y2, y3, y4, y5, y6, y7) \
    STORE(q, y0); STORE((q) + S, y1); STORE((q) + 2 * S, y2); STORE((q) + 3 * S, y3); \
    STORE((q) + 4 * S, y4); STORE((q) + 5 * S, y5); STORE((q) + 6 * S, y6); STORE((q) + 7 * S, y7); } while (0)

AINL void FN(pass3)(ELT *buf, size_t n, size_t S)
{
    KDECL
    KCARRY
    for (size_t j = 0; j < n; j += 8 * S) {
        ELT *p = buf + j;
        FRONT_AT(p, KFRONT);
        for (size_t i = W; i < S; i += W) {
            BACK_AT(p + i - W, KBACK);
            FRONT_AT(p + i, KFRONT);
        }
        BACK_AT(p + S - W, KBACK);
    }
}

AINL void FN(pass3L)(ELT *buf, size_t n, size_t S, int P)
{
    (void)P;
    KDECL_L(P)
    KCARRY
    for (size_t j = 0; j < n; j += 8 * S) {
        ELT *p = buf + j;
        FRONT_AT(p, KFRONT_L);
        for (size_t i = W; i < S; i += W) {
            BACK_AT(p + i - W, KBACK_L);
            FRONT_AT(p + i, KFRONT_L);
        }
        BACK_AT(p + S - W, KBACK_L);
    }
}
#undef FRONT_AT
#undef BACK_AT
#endif

AINL void FN(pass2)(ELT *buf, size_t n, size_t S)
{
    for (size_t j = 0; j < n; j += 4 * S) {
        for (size_t i = 0; i < S; i += W) {
            ELT *p = buf + j + i;
            V x0 = LOAD(p), x1 = LOAD(p + S), x2 = LOAD(p + 2 * S), x3 = LOAD(p + 3 * S);
            PIN(x0); PIN(x1); PIN(x2); PIN(x3);
            const V a0 = ADD(x0, x1), a1 = SUB(x0, x1), a2 = ADD(x2, x3), a3 = SUB(x2, x3);
            STORE(p, ADD(a0, a2)); STORE(p + 2 * S, SUB(a0, a2));
            STORE(p + S, ADD(a1, a3)); STORE(p + 3 * S, SUB(a1, a3));
        }
    }
}

AINL void FN(pass1)(ELT *buf, size_t n, size_t S)
{
    for (size_t j = 0; j < n; j += 2 * S) {
        for (size_t i = 0; i < S; i += W) {
            ELT *p = buf + j + i;
            V x0 = LOAD(p), x1 = LOAD(p + S);
            PIN(x0); PIN(x1);
            STORE(p, ADD(x0, x1)); STORE(p + S, SUB(x0, x1));
        }
    }
}

#if !STAGGER
AINL void FN(first8)(ELT *buf, size_t n)
{
    INREG_DECL
    KDECL
    for (size_t j = 0; j < n; j += 8 * W) {
        ELT *p = buf + j;
        LOAD8(p, W)
        INREG(x0); INREG(x1); INREG(x2); INREG(x3); INREG(x4); INREG(x5); INREG(x6); INREG(x7);
        KERNEL(x0, x1, x2, x3, x4, x5, x6, x7);
        STORE8(p, W)
    }
}

AINL void FN(first8L)(ELT *buf, size_t n, int P)
{
    (void)P;
    INREG_DECL
    KDECL_L(P)
    for (size_t j = 0; j < n; j += 8 * W) {
        ELT *p = buf + j;
        LOAD8(p, W)
        INREG(x0); INREG(x1); INREG(x2); INREG(x3); INREG(x4); INREG(x5); INREG(x6); INREG(x7);
        KERNEL_L(x0, x1, x2, x3, x4, x5, x6, x7);
        STORE8(p, W)
    }
}
#else
/* STAGGER, first pass: one turn does the 8-point step and the 8 stores for the 8 registers of the
 * turn before, then loads the next 8 registers and does the levels inside them, one level at a
 * time over all 8 (FFHT's order).  The 8 registers are carried from one turn to the next. */
#define INSIDE8(q) do { \
    x0 = LOAD(q); x1 = LOAD((q) + W); x2 = LOAD((q) + 2 * W); x3 = LOAD((q) + 3 * W); \
    x4 = LOAD((q) + 4 * W); x5 = LOAD((q) + 5 * W); x6 = LOAD((q) + 6 * W); x7 = LOAD((q) + 7 * W); \
    PIN(x0); PIN(x1); PIN(x2); PIN(x3); PIN(x4); PIN(x5); PIN(x6); PIN(x7); \
    INREG_BY_LEVEL(x0, x1, x2, x3, x4, x5, x6, x7); } while (0)
#define STEP8(q, KERNELM) do { \
    KERNELM(x0, x1, x2, x3, x4, x5, x6, x7); \
    STORE8(q, W) } while (0)

AINL void FN(first8)(ELT *buf, size_t n)
{
    INREG_DECL
    KDECL
    V x0, x1, x2, x3, x4, x5, x6, x7;
    INSIDE8(buf);
    for (size_t j = 8 * W; j < n; j += 8 * W) {
        STEP8(buf + j - 8 * W, KERNEL);
        INSIDE8(buf + j);
    }
    STEP8(buf + n - 8 * W, KERNEL);
}

AINL void FN(first8L)(ELT *buf, size_t n, int P)
{
    (void)P;
    INREG_DECL
    KDECL_L(P)
    V x0, x1, x2, x3, x4, x5, x6, x7;
    INSIDE8(buf);
    for (size_t j = 8 * W; j < n; j += 8 * W) {
        STEP8(buf + j - 8 * W, KERNEL_L);
        INSIDE8(buf + j);
    }
    STEP8(buf + n - 8 * W, KERNEL_L);
}
#undef INSIDE8
#undef STEP8
#endif

AINL void FN(first4)(ELT *buf, size_t n)
{
    INREG_DECL
    for (size_t j = 0; j < n; j += 4 * W) {
        ELT *p = buf + j;
        V x0 = LOAD(p), x1 = LOAD(p + W), x2 = LOAD(p + 2 * W), x3 = LOAD(p + 3 * W);
        PIN(x0); PIN(x1); PIN(x2); PIN(x3);
        INREG(x0); INREG(x1); INREG(x2); INREG(x3);
        const V a0 = ADD(x0, x1), a1 = SUB(x0, x1), a2 = ADD(x2, x3), a3 = SUB(x2, x3);
        STORE(p, ADD(a0, a2)); STORE(p + 2 * W, SUB(a0, a2));
        STORE(p + W, ADD(a1, a3)); STORE(p + 3 * W, SUB(a1, a3));
    }
}

AINL void FN(first2)(ELT *buf, size_t n)
{
    INREG_DECL
    for (size_t j = 0; j < n; j += 2 * W) {
        ELT *p = buf + j;
        V x0 = LOAD(p), x1 = LOAD(p + W);
        PIN(x0); PIN(x1);
        INREG(x0); INREG(x1);
        STORE(p, ADD(x0, x1)); STORE(p + W, SUB(x0, x1));
    }
}

AINL void FN(first1)(ELT *buf, size_t n)
{
    INREG_DECL
    for (size_t j = 0; j < n; j += W) {
        ELT *p = buf + j;
        V x0 = LOAD(p);
        PIN(x0);
        INREG(x0);
        STORE(p, x0);
    }
}

AINL void FN(sweep)(ELT *buf, size_t n, int P)
{
    const V c = SET1((ELT)((uint64_t)1 << P));
    for (size_t j = 0; j < n; j += W) STORE(buf + j, MUL(LOAD(buf + j), c));
}

#define FIRST1(b, n) FN(first1)(b, n)
#define FIRST2(b, n) FN(first2)(b, n)
#define FIRST4(b, n) FN(first4)(b, n)
#define FIRST8(b, n) FN(first8)(b, n)
#define FIRST8L(b, n, P) FN(first8L)(b, n, P)
#define PASS1(b, n, S) FN(pass1)(b, n, S)
#define PASS2(b, n, S) FN(pass2)(b, n, S)
#define PASS3(b, n, S) FN(pass3)(b, n, S)
#define PASS3L(b, n, S, P) FN(pass3L)(b, n, S, P)
#if SWEEP_L(0)
#define SWEEP(b, n, P) FN(sweep)(b, n, P)
#else
#define SWEEP(b, n, P) ((void)0)
#endif
#define BLOCK static __attribute__((noinline)) void
#define TOP static inline void

#ifndef STEP_ONLY
#include "plans.inc"
#else
/* STEP_ONLY (the program harness_k): not a transform.  Two functions that apply ONE pass to the
 * 2^k numbers at buf, so that the pass can be timed by itself:
 *   NAME_only3   the 3-level pass at distance 8 W (64 floats, 32 doubles): 8-point step only
 *   NAME_only1   the first pass: the levels inside the registers and the 8-point step */
void FN(only3)(ELT *buf, int k) { PASS3(buf, (size_t)1 << k, 8 * W); }
void FN(only1)(ELT *buf, int k) { FIRST8(buf, (size_t)1 << k); }
#endif

#undef FIRST1
#undef FIRST2
#undef FIRST4
#undef FIRST8
#undef FIRST8L
#undef PASS1
#undef PASS2
#undef PASS3
#undef PASS3L
#undef SWEEP
#undef BLOCK
#undef TOP
#undef LOAD8
#undef STORE8
#undef AINL
#undef FN
#undef FN1
#undef FN2
