#!/usr/bin/env python3
"""gen_kernels.py -- circuit files (the release format "w = a*u + b*v") -> C kernels for NEON / AVX.

Agent ax-1, 21-22 Oct 2026.  Standard library only.

Every circuit line becomes ONE vector instruction:
    w = u + v, u - v              -> ADD / SUB
    w = u + c*v, u - c*v          -> FMA(u, v, c) / FMS(u, v, c)  (NEON FMLA / FMLS by a constant)
    w = c*u                        -> MUL(u, c)
NEON has no vector form of "-u + c*v" (x86 has vfnmadd), and its FMLA overwrites its accumulator
(the compiler adds a register move when the accumulator is still live; Apple cores remove most of
these moves at rename).  So the generator keeps each value up to a sign: it stores s*w with s = +-1
and chooses s so that every line is one instruction with a +1 accumulator.  The free choices (lines
whose two coefficients are both +-1) are searched so that as many outputs as possible come out with
sign +1; an output left with sign -1 costs one NEG (reported).

Usage:
    gen_kernels.py stats  FILE...                 counts, depth, signs, live registers
    gen_kernels.py emit   NAME FILE [NAME FILE]... > kernels_gen.h
The emitted kernel is   static inline void NAME(V *v)   : v[0..n-1] in, v[j] = y_j out.
It uses the macros V_ADD, V_SUB, V_FMA(a,b,c) (= a + b*c), V_FMS(a,b,c) (= a - b*c), V_MUL(a,c),
V_NEG, V_CONST(c) that the including file defines for its type (fp32 / fp16 / fp64 / int16 / AVX).
"""
import itertools
import re
import sys
from fractions import Fraction

TERM = re.compile(r'\s*([+-]?)\s*(?:([0-9]+(?:/[0-9]+)?)\s*\*\s*)?([A-Za-z_][A-Za-z0-9_]*)')


def parse(path):
    gates, outs, n = [], {}, 0
    for line in open(path):
        line = line.split('#', 1)[0].strip()
        if not line:
            continue
        lhs, rhs = [s.strip() for s in line.split('=', 1)]
        terms, pos = [], 0
        while pos < len(rhs):
            m = TERM.match(rhs, pos)
            if not m:
                raise SystemExit(f'{path}: cannot parse {line!r}')
            sg, c, name = m.groups()
            c = Fraction(c) if c else Fraction(1)
            if sg == '-':
                c = -c
            terms.append((c, name))
            pos = m.end()
        for _, nm in terms:
            if re.fullmatch(r'x\d+', nm):
                n = max(n, int(nm[1:]) + 1)
        if re.fullmatch(r'y\d+', lhs) and len(terms) == 1 and terms[0][0] == 1:
            outs[int(lhs[1:])] = terms[0][1]
        else:
            gates.append((lhs, terms))
    for w, _ in gates:
        if re.fullmatch(r'y\d+', w):
            outs[int(w[1:])] = w
    return n, gates, [outs[j] for j in range(len(outs))]


def textbook(n):
    """the textbook as a circuit, stage by stage, in-place naming"""
    cur = [f'x{i}' for i in range(n)]
    gates, k = [], 0
    h = 1
    while h < n:
        new = list(cur)
        for i in range(0, n, 2 * h):
            for j in range(i, i + h):
                k += 1
                a, b = f't{k}a', f't{k}b'
                gates.append((a, [(Fraction(1), cur[j]), (Fraction(1), cur[j + h])]))
                gates.append((b, [(Fraction(1), cur[j]), (Fraction(-1), cur[j + h])]))
                new[j], new[j + h] = a, b
        cur = new
        h *= 2
    return n, gates, cur


def assign_signs(n, gates, outs, choice):
    """choice: dict gate-index -> +-1 for free gates.  Returns (signs, ops) where ops are
    (kind, dst, acc, other, const)."""
    s = {f'x{i}': 1 for i in range(n)}
    ops = []
    for gi, (w, terms) in enumerate(gates):
        if len(terms) == 1:
            c, u = terms[0]
            sw = s[u] if c > 0 else -s[u]
            ops.append(('MUL', w, u, None, abs(c)))
            s[w] = sw
            continue
        (c1, u), (c2, v) = terms
        a1, a2 = c1 * s[u], c2 * s[v]
        unit = [i for i, a in enumerate((a1, a2)) if abs(a) == 1]
        if not unit:
            raise SystemExit(f'gate {w}: no unit coefficient')
        if len(unit) == 2:
            sw = choice.get(gi, 1)
            # accumulator = a term whose coefficient becomes +1
            i = 0 if sw * a1 == 1 else 1
            if sw * (a1, a2)[i] != 1:   # both -1 under sw: flip
                sw = -sw
                i = 0
        else:
            i = unit[0]
            sw = 1 if (a1, a2)[i] == 1 else -1
        acc, oth = (u, v) if i == 0 else (v, u)
        b = sw * (a2 if i == 0 else a1)
        if abs(b) == 1:
            ops.append(('ADD' if b > 0 else 'SUB', w, acc, oth, 1))
        else:
            ops.append(('FMA' if b > 0 else 'FMS', w, acc, oth, abs(b)))
        s[w] = sw
    return s, ops


def best_signs(n, gates, outs):
    free = []
    s = {f'x{i}': 1 for i in range(n)}
    # find free gates by a forward pass with default choices (freeness depends only on |coef|)
    for gi, (w, terms) in enumerate(gates):
        if len(terms) == 2 and all(abs(c) == 1 for c, _ in terms):
            free.append(gi)
    best = None
    # greedy improvement: start all +1, flip single gates while it helps (cheap, good enough here)
    choice = {g: 1 for g in free}
    def cost(ch):
        s, _ = assign_signs(n, gates, outs, ch)
        return sum(1 for o in outs if s[o] < 0)
    cur = cost(choice)
    improved = True
    while improved and cur > 0:
        improved = False
        for g in free:
            ch = dict(choice)
            ch[g] = -ch[g]
            c = cost(ch)
            if c < cur:
                choice, cur, improved = ch, c, True
    # pairs, if still not zero
    if cur > 0:
        for g1, g2 in itertools.combinations(free, 2):
            ch = dict(choice)
            ch[g1] = -ch[g1]
            ch[g2] = -ch[g2]
            c = cost(ch)
            if c < cur:
                choice, cur = ch, c
                if cur == 0:
                    break
    s, ops = assign_signs(n, gates, outs, choice)
    return s, ops, cur


def depth_live(n, gates, ops, outs, lat=None):
    lat = lat or {'ADD': 1, 'SUB': 1, 'FMA': 1, 'FMS': 1, 'MUL': 1}
    d = {f'x{i}': 0 for i in range(n)}
    for kind, w, a, b, _ in ops:
        d[w] = max(d[a], d[b] if b else 0) + lat[kind]
    # live registers in program order
    last = {}
    for idx, (kind, w, a, b, _) in enumerate(ops):
        last[a] = idx
        if b:
            last[b] = idx
    for o in outs:
        last[o] = len(ops)
    live, peak = set(f'x{i}' for i in range(n)), n
    for idx, (kind, w, a, b, _) in enumerate(ops):
        live.add(w)
        peak = max(peak, len(live))
        for u in (a, b):
            if u and last.get(u, -1) <= idx and u not in outs:
                live.discard(u)
    return max(d[o] for o in outs), peak


def emit_native(name, n, gates, outs):
    """x86 FMA3 form: every line is one instruction with its own signs; no sign tracking needed.
    V_FMA(a,b,c) = a + b*c, V_FMS(a,b,c) = a - b*c, V_RFMS(a,b,c) = b*c - a, V_NADD(a,b) = -a-b"""
    L = [f'/* {name}: {n} points, {len(gates)} lines, native FMA3 signs (x86) */',
         f'static inline void KN({name})(V *v) {{']
    L.append('  ' + ' '.join(f'V x{i} = v[{i}];' for i in range(n)))
    for w, terms in gates:
        if len(terms) == 1:
            c, u = terms[0]
            e = f'V_MUL({u}, {float(c)!r})'
        else:
            (c1, u), (c2, v) = terms
            if abs(c1) != 1:
                (c1, u), (c2, v) = (c2, v), (c1, u)
            # now |c1| == 1
            if abs(c2) == 1:
                if c1 > 0 and c2 > 0: e = f'V_ADD({u}, {v})'
                elif c1 > 0: e = f'V_SUB({u}, {v})'
                elif c2 > 0: e = f'V_SUB({v}, {u})'
                else: raise SystemExit('-u-v')
            elif c1 > 0:
                e = f'V_FMA({u}, {v}, {float(abs(c2))!r})' if c2 > 0 else f'V_FMS({u}, {v}, {float(abs(c2))!r})'
            else:
                if c2 > 0: e = f'V_RFMS({u}, {v}, {float(c2)!r})'
                else: raise SystemExit('-u-c*v')
        L.append(f'  V {w} = {e};')
    for j, o in enumerate(outs):
        L.append(f'  v[{j}] = {o};')
    L.append('}')
    return '\n'.join(L)


def load(spec):
    if spec.startswith('textbook'):
        return textbook(int(spec[8:]))
    return parse(spec)


def emit(name, n, gates, outs, signfree=False, level=False):
    s, ops, bad = best_signs(n, gates, outs)
    if level:
        d = {f'x{i}': 0 for i in range(n)}
        for kind, w, a, b, _ in ops:
            d[w] = max(d[a], d[b] if b else 0) + 1
        ops = sorted(ops, key=lambda o: d[o[1]])
    if signfree:
        s = {k: 1 for k in s}
    L = [f'/* {name}: {n} points, {len(ops)} lines + {0 if signfree else bad} negations'
         + (' (SIGN-FREE: output j is +-row j of H, fixed signs)' if signfree else '') + ' */',
         f'static inline void KN({name})(V *v) {{']
    L.append('  ' + ' '.join(f'V x{i} = v[{i}];' for i in range(n)))
    for kind, w, a, b, c in ops:
        if kind == 'ADD':
            e = f'V_ADD({a}, {b})'
        elif kind == 'SUB':
            e = f'V_SUB({a}, {b})'
        elif kind == 'FMA':
            e = f'V_FMA({a}, {b}, {float(c)!r})'
        elif kind == 'FMS':
            e = f'V_FMS({a}, {b}, {float(c)!r})'
        else:
            e = f'V_MUL({a}, {float(c)!r})'
        L.append(f'  V {w} = {e};')
    for j, o in enumerate(outs):
        L.append(f'  v[{j}] = {o};' if s[o] > 0 else f'  v[{j}] = V_NEG({o});')
    L.append('}')
    return '\n'.join(L), len(ops), bad


def main():
    if sys.argv[1] == 'stats':
        for spec in sys.argv[2:]:
            n, gates, outs = load(spec)
            s, ops, bad = best_signs(n, gates, outs)
            kinds = {}
            for k, *_ in ops:
                kinds[k] = kinds.get(k, 0) + 1
            d1, peak = depth_live(n, gates, ops, outs)
            d2, _ = depth_live(n, gates, ops, outs, {'ADD': 3, 'SUB': 3, 'FMA': 4, 'FMS': 4, 'MUL': 4})
            print(f'{spec.split("/")[-1]:28s} n={n:3d} lines={len(ops):4d} {kinds} neg_outputs={bad} '
                  f'depth={d1} latency(add3,fma4)={d2} peak_live={peak}')
    elif sys.argv[1] == 'emit':
        args = sys.argv[2:]
        print('/* generated by gen_kernels.py; do not edit */')
        for name, spec in zip(args[0::2], args[1::2]):
            n, gates, outs = load(spec)
            if name.endswith('_nat'):
                print(emit_native(name, n, gates, outs))
                print()
                continue
            txt, nops, bad = emit(name, n, gates, outs, signfree=('_sf' in name), level=name.endswith('_lv'))
            print(txt)
            print()


if __name__ == '__main__':
    main()
