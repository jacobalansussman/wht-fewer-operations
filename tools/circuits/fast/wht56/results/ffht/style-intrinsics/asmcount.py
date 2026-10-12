#!/usr/bin/env python3
"""asmcount.py -- count the instructions of every innermost loop of some functions of whti.o.

    python3 asmcount.py build/whti.dis [--md] [--show FUNCTION] [functions ...]

build/whti.dis is "objdump -d --no-show-raw-insn build/whti.o".  Without function names the
program takes, for every variant, the function of the base block of 2^14 numbers
(whti_<variant>_<f|d>_k14_d12): it holds the first pass and the 8-register passes of the base
block, each as one innermost loop.  One turn of such a loop handles 8 registers.

For each innermost loop (a backward jump whose range holds no other backward jump):
  load    vector moves from memory to a register
  store   vector moves from a register to memory
  add     vaddp*, vsubp*, vaddsubp*           mul   vmulp*          fma   vfmadd*, vfmsub*, vfnmadd*
  shuf    vpermilp*, vperm2f128, vblendp*, vshufp*, vunpck*          xor   vxorp*
  mem     of the add/mul/fma/shuf/xor instructions, those that read an operand from memory
  move    register-to-register vector moves
  stack   instructions that touch the stack (a value that did not fit in the 16 registers)
  other   everything else (addresses, counter, jump)
  total   all instructions of one turn; bytes = the length of the loop's code
"""
import re
import sys

RE_FUNC = re.compile(r'^([0-9a-f]+) <(\S+)>:$')
RE_INS = re.compile(r'^\s*([0-9a-f]+):\s+(\S+)\s*(.*)$')
RE_JMP = re.compile(r'^j\w+$')


def read(path):
    funcs, cur = {}, None
    for line in open(path):
        line = line.rstrip('\n')
        m = RE_FUNC.match(line)
        if m:
            cur = funcs.setdefault(m.group(2), [])
            continue
        m = RE_INS.match(line)
        if m and cur is not None:
            ops = m.group(3).split('#')[0].strip()
            cur.append((int(m.group(1), 16), m.group(2), ops))
    return funcs


def classify(mn, ops):
    mem = '(' in ops
    stack = '(%rsp' in ops or '(%rbp' in ops
    d = {'stack': 1 if stack else 0}
    first = ops.split(',')[0] if ops else ''
    if mn.startswith('vmov') and ('ymm' in ops or 'xmm' in ops):
        if not mem:
            d['move'] = 1
        elif '(' in first:
            d['load'] = 1
        else:
            d['store'] = 1
        return d
    if mn.startswith('vbroadcast'):
        d['load'] = 1
        return d
    for key, pre in (('add', ('vaddp', 'vsubp', 'vaddsubp')), ('mul', ('vmulp',)), ('fma', ('vfmadd', 'vfmsub', 'vfnmadd', 'vfnmsub')),
                     ('shuf', ('vpermilp', 'vperm2f128', 'vblendp', 'vshufp', 'vunpck', 'vinsertf', 'vextractf', 'vpermp')), ('xor', ('vxorp',))):
        if mn.startswith(pre):
            d[key] = 1
            if mem:
                d['mem'] = 1
            return d
    d['other'] = 1
    return d


def loops(ins):
    """innermost loops of one function: (first index, last index)"""
    addr = {a: i for i, (a, _, _) in enumerate(ins)}
    back = []
    for i, (a, mn, ops) in enumerate(ins):
        if RE_JMP.match(mn):
            m = re.match(r'^([0-9a-f]+)\b', ops)
            if m:
                t = int(m.group(1), 16)
                if t <= a and t in addr:
                    back.append((addr[t], i))
    inner = [(s, e) for (s, e) in back if not any((s2, e2) != (s, e) and s <= s2 and e2 <= e for (s2, e2) in back)]
    return sorted(set(inner))


COLS = ['load', 'store', 'add', 'mul', 'fma', 'shuf', 'xor', 'mem', 'move', 'stack', 'other', 'total']


def count(ins, s, e):
    c = {k: 0 for k in COLS}
    for a, mn, ops in ins[s:e + 1]:
        for k, v in classify(mn, ops).items():
            c[k] += v
        c['total'] += 1
    c['bytes'] = ins[e + 1][0] - ins[s][0] if e + 1 < len(ins) else 0
    return c


def main():
    args = sys.argv[1:]
    md = '--md' in args
    args = [a for a in args if a != '--md']
    show = None
    if '--show' in args:
        i = args.index('--show')
        show = args[i + 1]
        del args[i:i + 2]
    funcs = read(args[0])
    if show:
        ins = funcs[show]
        for n, (s, e) in enumerate(loops(ins)):
            print('; %s, innermost loop %d: %s' % (show, n + 1, count(ins, s, e)))
            for a, mn, ops in ins[s:e + 1]:
                print('  %6x:  %-12s %s' % (a, mn, ops))
        return
    names = args[1:]
    if not names:
        names = sorted(n for n in funcs if re.match(r'^whti_\w+_[fd]_k14_d12$', n))
    head = ['function', 'loop'] + COLS + ['bytes']
    if md:
        print('| ' + ' | '.join(head) + ' |')
        print('|' + '---|' * len(head))
    else:
        print(' '.join('%-26s' % h if i == 0 else '%5s' % h for i, h in enumerate(head)))
    for nm in names:
        if nm not in funcs:
            print('%s: not found' % nm)
            continue
        ins = funcs[nm]
        for n, (s, e) in enumerate(loops(ins)):
            c = count(ins, s, e)
            row = [nm, str(n + 1)] + [str(c[k]) for k in COLS] + [str(c['bytes'])]
            if md:
                print('| ' + ' | '.join(row) + ' |')
            else:
                print(' '.join('%-26s' % r if i == 0 else '%5s' % r for i, r in enumerate(row)))


if __name__ == '__main__':
    main()
