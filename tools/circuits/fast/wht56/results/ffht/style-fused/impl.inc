/* impl.inc -- one in-place transform  void NAME(ELT *x, int k)  on 2^k numbers, k >= 3.
 *
 * Included once per number type and per 8-point step.  Everything except KERNEL (and KDECL, the
 * constant it may need) is the same text in every variant.  Macros set by the includer:
 *
 *   NAME                 the public function
 *   ELT, V               the number type and the register type
 *   W, LW                numbers in a register (8 floats, 4 doubles, 8 int32, 1 scalar) and log2 W
 *   LOAD(p), STORE(p, v), ADD(a, b), SUB(a, b)
 *   IDECL, INREG(v)      the constants for, and the code of, the LW levels inside one register
 *   KDECL, KERNEL(x0, .., x7)   the 8-point step on 8 registers
 *   PIN(v)               empty, or a barrier that makes the compiler keep a loaded value in a
 *                        register (so that it does not read the same number from memory twice)
 *   BASEMAX              log2 of the largest block that is finished before the next is touched
 *
 * The plan, the same as FFHT's recursive plan:
 *   L = k - LW levels are between registers.  r0 = L mod 3 (or 3 if that is 0, or 0 if L = 0).
 *   The first pass loads 2^r0 neighbouring registers, does the LW levels inside each, then r0
 *   levels between them: 1 level (two registers, add and subtract), 2 levels (four registers,
 *   8 additions and subtractions) or 3 levels (eight registers, KERNEL).  The short pass is
 *   the same text in every variant.
 *   Every later pass does 3 levels with KERNEL on 8 registers at a stride.
 *   A block of 2^base numbers (base <= BASEMAX, base = k mod 3) gets all its passes before the
 *   next block is touched; above that, a block of 2^d numbers is 8 blocks of 2^(d-3), one
 *   after the other, then one pass at stride 2^(d-3).
 */
#define FN2(a, b) a##_##b
#define FN1(a, b) FN2(a, b)
#define FN(s) FN1(NAME, s)

/* one pass of 3 levels at stride S over n numbers (n a multiple of 8 S, S a multiple of W) */
static __attribute__((noinline, noclone)) void FN(pass3)(ELT *x, size_t n, size_t S)
{
    KDECL
    for (size_t b = 0; b < n; b += 8 * S) {
        ELT *p = x + b;
        for (size_t j = 0; j < S; j += W) {
            V x0 = LOAD(p + j), x1 = LOAD(p + j + S), x2 = LOAD(p + j + 2 * S), x3 = LOAD(p + j + 3 * S);
            V x4 = LOAD(p + j + 4 * S), x5 = LOAD(p + j + 5 * S), x6 = LOAD(p + j + 6 * S), x7 = LOAD(p + j + 7 * S);
            PIN(x0); PIN(x1); PIN(x2); PIN(x3); PIN(x4); PIN(x5); PIN(x6); PIN(x7);
            KERNEL(x0, x1, x2, x3, x4, x5, x6, x7);
            STORE(p + j, x0); STORE(p + j + S, x1); STORE(p + j + 2 * S, x2); STORE(p + j + 3 * S, x3);
            STORE(p + j + 4 * S, x4); STORE(p + j + 5 * S, x5); STORE(p + j + 6 * S, x6); STORE(p + j + 7 * S, x7);
        }
    }
}

/* first pass, k = LW: the levels inside a register and nothing else */
static inline __attribute__((unused)) void FN(first0)(ELT *x, size_t n)
{
    IDECL
    for (size_t i = 0; i < n; i += W) {
        V a = LOAD(x + i);
        INREG(a);
        STORE(x + i, a);
    }
}

/* first pass with 1 level between registers */
static inline void FN(first1)(ELT *x, size_t n)
{
    IDECL
    for (size_t i = 0; i < n; i += 2 * W) {
        V a = LOAD(x + i), b = LOAD(x + i + W);
        INREG(a); INREG(b);
        STORE(x + i, ADD(a, b)); STORE(x + i + W, SUB(a, b));
    }
}

/* first pass with 2 levels between registers */
static inline void FN(first2)(ELT *x, size_t n)
{
    IDECL
    for (size_t i = 0; i < n; i += 4 * W) {
        V a = LOAD(x + i), b = LOAD(x + i + W), c = LOAD(x + i + 2 * W), d = LOAD(x + i + 3 * W);
        INREG(a); INREG(b); INREG(c); INREG(d);
        const V s0 = ADD(a, b), d0 = SUB(a, b), s1 = ADD(c, d), d1 = SUB(c, d);
        STORE(x + i, ADD(s0, s1)); STORE(x + i + W, ADD(d0, d1));
        STORE(x + i + 2 * W, SUB(s0, s1)); STORE(x + i + 3 * W, SUB(d0, d1));
    }
}

/* first pass with 3 levels between registers: the 8-point step on 8 neighbouring registers */
static inline void FN(first3)(ELT *x, size_t n)
{
    IDECL
    KDECL
    for (size_t i = 0; i < n; i += 8 * W) {
        V x0 = LOAD(x + i), x1 = LOAD(x + i + W), x2 = LOAD(x + i + 2 * W), x3 = LOAD(x + i + 3 * W);
        V x4 = LOAD(x + i + 4 * W), x5 = LOAD(x + i + 5 * W), x6 = LOAD(x + i + 6 * W), x7 = LOAD(x + i + 7 * W);
        INREG(x0); INREG(x1); INREG(x2); INREG(x3); INREG(x4); INREG(x5); INREG(x6); INREG(x7);
        KERNEL(x0, x1, x2, x3, x4, x5, x6, x7);
        STORE(x + i, x0); STORE(x + i + W, x1); STORE(x + i + 2 * W, x2); STORE(x + i + 3 * W, x3);
        STORE(x + i + 4 * W, x4); STORE(x + i + 5 * W, x5); STORE(x + i + 6 * W, x6); STORE(x + i + 7 * W, x7);
    }
}

/* all passes of one block of n numbers */
static void FN(block)(ELT *x, size_t n, int r0)
{
    size_t S;
    switch (r0) {
    case 0:  FN(first0)(x, n); S = W; break;
    case 1:  FN(first1)(x, n); S = 2 * W; break;
    case 2:  FN(first2)(x, n); S = 4 * W; break;
    default: FN(first3)(x, n); S = 8 * W; break;
    }
    for (; S < n; S *= 8) FN(pass3)(x, n, S);
}

static void FN(rec)(ELT *x, int d, int base, int r0)
{
    const size_t n = (size_t)1 << d;
    if (d <= base) { FN(block)(x, n, r0); return; }
    const size_t sub = n >> 3;
    for (int i = 0; i < 8; i++) FN(rec)(x + (size_t)i * sub, d - 3, base, r0);
    FN(pass3)(x, n, sub);
}

void NAME(ELT *x, int k)
{
    const int L = k - LW;
    const int r0 = L == 0 ? 0 : (L % 3 ? L % 3 : 3);
    int base = k;
    while (base > BASEMAX) base -= 3;
    FN(rec)(x, k, base, r0);
}

#undef FN
#undef FN1
#undef FN2
