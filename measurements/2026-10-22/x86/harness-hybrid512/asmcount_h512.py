#!/usr/bin/env python3
"""asmcount_h512.py FILE.asm... -- per step function of x86-hybrid512 (hf<form>_<kernel>: a block's first step with the
in-lane levels in form 0 F / 1 A / 2 X; hs_<kernel>: a later step; pass_<textbook kernel>_1: x86-wht's passes), count the vector instructions in objdump output:
add/sub, FMA, mul, shuffles (vshufp*, vshuff*, vpermil*, vperm*), xor, blends, loads, stores, stack traffic (spills)
and register-to-register copies (vmovap*/vmovup*/vmovdq* %reg,%reg: each costs a front-end slot; the FMA-first
balanced textbook carried 12 per 8-point step in clang tonight).  Evidence that each circuit line is one instruction,
that the F form costs 1 shuffle + 1 FMA per in-lane level, and that the 16-vector steps do not spill with 32 registers.
Operand separators may be ',' (GNU objdump, the Colab) or ', ' (llvm-objdump, the Mac).  Standard library only."""
import re
import sys

FN = re.compile(r'^[0-9a-f]+ <_?((?:hf[012]|hs)_[\w.]+|pass_(?:tb16|tb8)_(?:nat|bal|balS)_1[\w.]*)>:')  # + x86wht's passes
KEYS = ['add', 'fma', 'mul', 'shuf', 'xor', 'blend', 'ld', 'st', 'spill', 'regmov', 'bcast']
for path in sys.argv[1:]:
    cur, res = None, {}
    for line in open(path, errors='replace'):
        m = FN.match(line)
        if m:
            cur = m.group(1)
            res[cur] = cnt = dict.fromkeys(KEYS, 0)
            continue
        if cur is None:
            continue
        if not line.strip() or re.match(r'^[0-9a-f]+ <', line):
            cur = None
            continue
        m2 = re.match(r'^\s*[0-9a-f]+:\s*(\S+)\s*(.*)$', line)
        if not m2:
            continue
        op, ops = m2.group(1), m2.group(2).split('#')[0].strip()  # drop objdump comments ('## zmm8 = (zmm0 * ...')
        ins = op + ' ' + ops
        mem = '(' in ops
        if op.startswith('v') and ('(%rsp)' in ops or '(%rbp)' in ops):  # any vector op touching the stack: a spill
            cnt['spill'] += 1
            if re.match(r'v(add|sub)p[sd]', op):
                cnt['add'] += 1
            elif re.match(r'vf(n?m(add|sub))\d+p[sd]', op):
                cnt['fma'] += 1
            continue
        if re.match(r'v(add|sub)p[sd]', op):
            cnt['add'] += 1
            cnt['ld'] += mem
        elif re.match(r'vf(n?m(add|sub))\d+p[sd]', op):
            cnt['fma'] += 1
            if mem and '{1to' in ops:
                cnt['bcast'] += 1
            elif mem:
                cnt['ld'] += 1
        elif re.match(r'vmulp[sd]', op):
            cnt['mul'] += 1
        elif re.match(r'v(shufp[sd]|shuff(32x4|64x2)|shufi(32x4|64x2)|pshuf(d|b|hw|lw)|permilp[sd]|perm(ps|pd|q|d|2f128|t2ps|t2pd|i2ps)|movs[lh]dup|movddup|unpck[lh]p[sd])', op):
            cnt['shuf'] += 1
        elif re.match(r'v(p?xor(p[sd]|d|q)?|pxor)', op):
            cnt['xor'] += 1
        elif re.match(r'v(p?blendm?(ps|pd|d|q)|blendp[sd])', op):
            cnt['blend'] += 1
        elif re.match(r'vbroadcast', op):
            cnt['bcast'] += 1
        elif re.match(r'vmov(u|a)p[sd]|vmovdq', op):
            if '(%rsp)' in ins or '(%rbp)' in ins:
                cnt['spill'] += 1
            elif re.search(r'\),\s*%[xyz]mm', ins):
                cnt['ld'] += 1
            elif re.search(r'%[xyz]mm\d+,.*\(', ins):
                cnt['st'] += 1
            elif re.match(r'%[xyz]mm\d+,\s*%[xyz]mm\d+', ops) and not mem:
                cnt['regmov'] += 1
    print(f'== {path.split("/")[-1]}')
    for fn in sorted(res):
        c = res[fn]
        print(f'  {fn:20s} ' + ' '.join(f'{k} {c[k]:3d}' for k in KEYS))
