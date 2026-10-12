#!/usr/bin/env python3
"""asmcount.py -- count instructions, from the generated C and from the compiled object.

  python3 -B asmcount.py VARIANT [VARIANT ...]        (run in the style-generator folder)

Part 1, from gen/V/fht_avx.c (the text the generator wrote): for every helper, every assembly
block with the number of registers it loads and its instructions by kind.  Every point goes
through every block of its helper exactly once per transform, and one instruction works on one
register (8 floats or 4 doubles), so

    vector instructions per point = sum over the blocks of (instructions / (registers * W)).

Part 2, from the disassembly of build/V/fht.o (objdump -d): every innermost loop that holds
vector instructions, with all its instructions by kind, the general-register instructions that
gcc put around the assembly block included, and whether anything in the loop touches the stack
(%rsp): that would be a spilled address or counter.  The loops are grouped by shape.
"""
import collections
import re
import subprocess
import sys

W = {'float': 8, 'double': 4}


def kind(mn):
    if mn.startswith('vmovup'):
        return 'load/store'
    if re.match(r'v(add|sub)p[sd]$', mn):
        return 'add/sub'
    if mn.startswith('vmulp'):
        return 'mul'
    if re.match(r'vfn?m(add|sub)\d+p[sd]$', mn):
        return 'fma'
    if mn.startswith('vbroadcast'):
        return 'const load'
    if mn.startswith('v'):
        return 'shuffle/sign'       # vpermil, vperm2f128, vblend, vxor, vaddsub
    return 'general'


def helpers_from_c(path):
    """{(type, log_n): [block, ...]}, block = {'regs': n, 'ins': Counter of kinds, 'n': total}"""
    res = collections.OrderedDict()
    cur = None
    block = None
    for raw in open(path):
        m = re.match(r'(?:static inline )?void helper_(float|double)_(\d+)(?:_recursive)?\(.*\) \{', raw)
        if m:
            cur = (m.group(1), int(m.group(2)))
            res.setdefault(cur, [])
            continue
        s = raw.strip()
        if s.startswith('__asm__ volatile'):
            block = {'regs': 0, 'ins': collections.Counter(), 'n': 0, 'mn': collections.Counter()}
            continue
        if block is not None and s.startswith('"'):
            mn = s[1:].split()[0]
            block['mn'][mn] += 1
            block['n'] += 1
            if mn.startswith('vmovup') and re.match(r'"vmovup[sd] \(%\d+\)', s):
                block['regs'] += 1
            else:
                block['ins'][kind(mn)] += 1
            continue
        if block is not None and s.startswith('::'):
            res[cur].append(block)
            block = None
    return res


def per_point(blocks, type_name):
    tot = collections.Counter()
    for b in blocks:
        per = 1.0 / (b['regs'] * W[type_name])
        tot['all'] += b['n'] * per
        for k, v in b['ins'].items():
            tot[k] += v * per
        tot['load/store'] += 2 * b['regs'] * per - b['ins'].get('load/store', 0) * per
    return tot


def loops_from_object(path):
    """innermost loops with vector instructions: list of (function, Counter by kind, uses_stack, n)"""
    dis = subprocess.run(['objdump', '-d', '--no-show-raw-insn', path], capture_output=True, text=True, check=True).stdout
    funcs = collections.OrderedDict()
    cur = None
    for raw in dis.splitlines():
        m = re.match(r'[0-9a-f]+ <(\w+)>:', raw)
        if m:
            cur = m.group(1)
            funcs[cur] = []
            continue
        m = re.match(r'\s*([0-9a-f]+):\s+(\S+)\s*(.*)$', raw)
        if m and cur:
            funcs[cur].append((int(m.group(1), 16), m.group(2), m.group(3)))
    loops = []
    for f, ins in funcs.items():
        addr_index = dict((a, i) for i, (a, _, _) in enumerate(ins))
        spans = []
        for i, (a, mn, ops) in enumerate(ins):
            if mn.startswith('j') and mn != 'jmp':
                m = re.match(r'([0-9a-f]+)', ops)
                if m:
                    t = int(m.group(1), 16)
                    if t <= a and t in addr_index:
                        spans.append((addr_index[t], i))
        for (s, e) in spans:
            if any(s2 >= s and e2 <= e and (s2, e2) != (s, e) for (s2, e2) in spans):
                continue                        # not innermost
            body = ins[s:e + 1]
            if not any(mn.startswith('v') for _, mn, _ in body):
                continue
            c = collections.Counter()
            for _, mn, ops in body:
                k = kind(mn)
                if k == 'load/store':
                    k = 'store' if re.search(r',\(?%r\w+\)?$|,\(%r\w+\)$', ops) and ops.split(',')[0].startswith('%ymm') else 'load'
                c[k] += 1
            stack = any('%rsp' in ops for _, _, ops in body)
            loops.append((f, c, stack, len(body)))
    return loops


def main():
    variants = sys.argv[1:] or ['gT', 'g20x', 'g20s', 'g19f', 'g19r']
    data = dict((v, helpers_from_c('gen/%s/fht_avx.c' % v)) for v in variants)

    print('## Part 1: the assembly blocks the generator wrote (gen/V/fht_avx.c)\n')
    print('The distinct blocks of 8 registers that do 3 levels between registers and nothing else, per variant:\n')
    print('| variant | type | instructions in the block | of them | such blocks in the file |')
    print('|---|---|---|---|---|')
    for v in variants:
        for t in ('float', 'double'):
            shapes = collections.Counter()
            for (tt, k), blocks in data[v].items():
                if tt != t:
                    continue
                for b in blocks:
                    if b['regs'] == 8 and b['ins'].get('shuffle/sign', 0) == 0:
                        shapes[(b['n'], tuple(sorted(b['mn'].items())))] += 1
            for (n, mn), cnt in sorted(shapes.items()):
                print('| %s | %s | %d | %s | %d |' % (v, t, n, ', '.join('%d `%s`' % (c, m) for m, c in mn), cnt))
    print()
    for t in ('float', 'double'):
        print('Vector instructions per point for one transform, %ss (one instruction works on %d numbers), '
              'and the change against the textbook block:\n' % (t, W[t]))
        print('| k | 8-register passes | ' + ' | '.join(variants) + ' |')
        print('|---|---|' + '---|' * len(variants))
        for k in range(3, 31):
            base = None
            cells = []
            for v in variants:
                blocks = data[v].get((t, k), [])
                p = per_point(blocks, t)['all']
                if base is None:
                    base = p
                    cells.append('%.3f' % p)
                else:
                    cells.append('%.3f (%+.1f %%)' % (p, 100.0 * (p - base) / base))
            n8 = sum(1 for b in data[variants[0]].get((t, k), []) if b['regs'] == 8)
            print('| %d | %d | %s |' % (k, n8, ' | '.join(cells)))
        print()

    print('## Part 2: the innermost loops gcc built around the blocks (build/V/fht.o, objdump -d)\n')
    print('| variant | loops of this shape | instructions in the loop | load | store | add/sub | mul | fma | const load | '
          'shuffle/sign | general (lea, add, cmp, jump) | touches the stack |')
    print('|---|---|---|---|---|---|---|---|---|---|---|---|')
    for v in variants:
        loops = loops_from_object('build/%s/fht.o' % v)
        shapes = collections.Counter()
        for f, c, stack, n in loops:
            shapes[(n, c['load'], c['store'], c['add/sub'], c['mul'], c['fma'], c['const load'],
                    c['shuffle/sign'], c['general'], stack)] += 1
        for sh, cnt in sorted(shapes.items(), key=lambda x: (x[0][1], x[0][7], x[0][0])):
            print('| %s | %d | %s | %s |' % (v, cnt, ' | '.join(str(x) for x in sh[:-1]), 'YES' if sh[-1] else 'no'))
    print()


if __name__ == '__main__':
    main()
