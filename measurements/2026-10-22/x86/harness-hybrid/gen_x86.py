#!/usr/bin/env python3
"""gen_x86.py -- circuit files -> x86 FMA3 kernels for bench_k0.c (22 Oct 2026).

Builds on ax-1's gen_kernels.py (parse / textbook).  Every circuit line becomes ONE instruction with its own signs
(x86 FMA3 has vfmadd / vfnmadd / vfmsub, so no sign tracking is needed):
    u + v, u - v   -> V_ADD / V_SUB                  (add pipes)
    u +- c*v       -> V_FMA / V_FMS (c a power of two) (FMA pipes)
    c*v - u        -> V_RFMS
    c*u            -> V_MUL
Two forms per circuit:
    NAME_nat : as above.
    NAME_bal : "pipe-balanced": pure add/sub lines are turned into FMAs by an opaque ONE (u +- 1*v), alternately,
               until half of all lines are FMA-form.  On cores whose adds and FMAs run on DIFFERENT pipes (AMD Zen 2-5:
               2 FADD + 2 FMA pipes; Intel Golden Cove and later: fast adders on extra ports) this lets a circuit use
               every FP pipe.  The textbook gets the same treatment: it is the fair rival (lesson 4).
               ONE is a register the compiler cannot see through (an empty asm), so fma(x, 1, y) is not folded back
               into an add.  u + 1*v is exact (the product 1*v is exact, one rounding), so results are identical.
    NAME_balS: NAME_bal with the same lines, operands and signs, only the ORDER changed (x86-hybrid, 22 Oct 2026): a
               converted FMA line that is followed by the plain line reading the same two inputs (the other half of its
               butterfly) is emitted AFTER that line.  With the FMA first both inputs are still live when the destructive
               3-operand vfmadd runs, so clang copies one (vmovapd) per butterfly; with the SUB first they are not.
Kernel signature:  static inline void NAME(V *v, V one)   v[0..n-1] in, v[j] = y_j out.
Usage:  gen_x86.py NAME FILE [NAME FILE] ...  > kernels_k0.h      (FILE may be textbookN)
"""
import sys
from fractions import Fraction
sys.path.insert(0, __import__('os').path.dirname(__file__))
from gen_kernels import load  # noqa: E402


def lines_of(n, gates):
    """-> list of (dst, kind, a, b, c)  kind in ADD SUB FMA FMS RFMS MUL"""
    out = []
    for w, terms in gates:
        if len(terms) == 1:
            c, u = terms[0]
            if c < 0:
                raise SystemExit(f'{w}: negative scaling not supported')
            out.append((w, 'MUL', u, None, c))
            continue
        (c1, u), (c2, v) = terms
        if abs(c1) != 1:
            (c1, u), (c2, v) = (c2, v), (c1, u)
        if abs(c1) != 1:
            raise SystemExit(f'{w}: no unit coefficient')
        if abs(c2) == 1:
            if c1 > 0 and c2 > 0:
                out.append((w, 'ADD', u, v, 1))
            elif c1 > 0:
                out.append((w, 'SUB', u, v, 1))
            elif c2 > 0:
                out.append((w, 'SUB', v, u, 1))
            else:
                raise SystemExit(f'{w}: -u-v')
        elif c1 > 0:
            out.append((w, 'FMA' if c2 > 0 else 'FMS', u, v, abs(c2)))
        else:
            if c2 < 0:
                raise SystemExit(f'{w}: -u-c*v')
            out.append((w, 'RFMS', u, v, c2))
    return out


def emit(name, spec, balanced, sub_first=False):
    n, gates, outs = load(spec)
    L = lines_of(n, gates)
    nfma = sum(1 for l in L if l[1] in ('FMA', 'FMS', 'RFMS', 'MUL'))
    conv = set()
    if balanced:
        want = (len(L) + 1) // 2
        pure = [i for i, l in enumerate(L) if l[1] in ('ADD', 'SUB')]
        need = max(0, want - nfma)
        # spread the converted lines evenly over the program
        if need:
            step = len(pure) / need
            conv = {pure[int(k * step)] for k in range(need)}
    kinds = {}
    body = []
    for i, (w, k, a, b, c) in enumerate(L):
        cs = repr(float(c))
        if i in conv:
            e = f'FMADD({b}, one, {a})' if k == 'ADD' else f'FNMADD({b}, one, {a})'
            k = 'FMA1'
        elif k == 'ADD':
            e = f'V_ADD({a}, {b})'
        elif k == 'SUB':
            e = f'V_SUB({a}, {b})'
        elif k == 'FMA':
            e = f'V_FMA({a}, {b}, {cs})'
        elif k == 'FMS':
            e = f'V_FMS({a}, {b}, {cs})'
        elif k == 'RFMS':
            e = f'V_RFMS({a}, {b}, {cs})'
        else:
            e = f'V_MUL({a}, {cs})'
        kinds[k] = kinds.get(k, 0) + 1
        body.append(f'  V {w} = {e};')
    if sub_first:  # the plain half of each converted butterfly first (it reads the same inputs, not the FMA's output)
        for i in sorted(conv):
            j = i + 1
            if j < len(L) and j not in conv and L[j][1] in ('ADD', 'SUB') and {L[j][2], L[j][3]} == {L[i][2], L[i][3]}:
                body[i], body[j] = body[j], body[i]
    head = [f'/* {name}: {n} points, {len(L)} lines {dict(sorted(kinds.items()))}'
            f'{" PIPE-BALANCED" if balanced else ""}{", SUB BEFORE FMA" if sub_first else ""}; from {spec.split("/")[-1]} */',
            f'static inline void {name}(V *v, V one) {{', '  (void)one;',
            '  ' + ' '.join(f'V x{i} = v[{i}];' for i in range(n))]
    tail = [f'  v[{j}] = {o};' for j, o in enumerate(outs)] + ['}', '']
    return '\n'.join(head + body + tail), n, len(L)


def main():
    a = sys.argv[1:]
    print('/* generated by gen_x86.py (22 Oct 2026); do not edit */')
    for name, spec in zip(a[0::2], a[1::2]):
        txt, n, nl = emit(name, spec, name.endswith(('_bal', '_balS')), name.endswith('_balS'))
        print(txt)
        sys.stderr.write(f'{name}: n={n} lines={nl}\n')


if __name__ == '__main__':
    main()
