#!/usr/bin/env python3
"""diffcheck.py -- is the difference between two generated fht_avx.c files confined to the block
of 8 registers and 3 levels?

    python3 -B diffcheck.py gen/gT/fht_avx.c gen/g20s/fht_avx.c [more files]

Both files are cut into pieces: every assembly block (from "__asm__ volatile (" to its ");") is
one piece, the text between blocks is one piece.  The files must have the same number of pieces.
A piece may differ only if it is an assembly block that loads 8 registers; and inside such a
block only three things may differ: the lines between the last instruction of the levels inside
the registers and the first store (the three levels between the registers), the register names
in the 8 stores, and constants added at the end of the operand list.  The 8 loads, the levels
inside the registers, the 8 addresses and the list of changed registers must be the same.
The first piece (the top of the file) may gain the definitions of the constants.
"""
import re
import sys


def pieces(path):
    out = []
    cur = []
    inblock = False
    for line in open(path):
        if line.strip().startswith('__asm__ volatile'):
            out.append(('text', cur))
            cur = [line]
            inblock = True
        elif inblock and line.strip() == ');':
            cur.append(line)
            out.append(('asm', cur))
            cur = []
            inblock = False
        else:
            cur.append(line)
    out.append(('text', cur))
    return out


INSIDE = re.compile(r'\s*"v(permilp|perm2f128|blendp|xorp|addsubp)')


def split_block(lines):
    """-> (loads, inside-register lines, kernel lines, stores, operand line)"""
    body = lines[1:-2]
    ops = lines[-2]
    loads = [l for l in body if re.match(r'\s*"vmovup[sd] \(%\d+\), ', l)]
    stores = [l for l in body if re.match(r'\s*"vmovup[sd] %%ymm\d+, \(%\d+\)', l)]
    mid = body[len(loads):len(body) - len(stores)]
    last_inside = -1
    for i, l in enumerate(mid):
        if INSIDE.match(l):
            last_inside = i
    # the level inside a register ends with the addition that follows its last shuffle
    cut = last_inside + 2 if last_inside >= 0 else 0
    while cut < len(mid) and last_inside >= 0 and INSIDE.match(mid[cut - 1]):
        cut += 1
    return loads, mid[:cut], mid[cut:], stores, ops


def main():
    base = pieces(sys.argv[1])
    for other_path in sys.argv[2:]:
        other = pieces(other_path)
        if len(base) != len(other):
            print('%s: DIFFERENT STRUCTURE (%d pieces against %d)' % (other_path, len(other), len(base)))
            continue
        bad = 0
        changed = same = 0
        for i, ((ka, a), (kb, b)) in enumerate(zip(base, other)):
            if a == b:
                same += 1
                continue
            if ka == 'text':
                if i == 0 and b[:1] == a[:1] and b[-len(a) + 1:] == a[1:] and all(
                        l.startswith('static const') or l.startswith('  {') or l.startswith('};') for l in b[1:len(b) - len(a) + 1]):
                    continue
                bad += 1
                continue
            la, ia, ka_, sa, oa = split_block(a)
            lb, ib, kb_, sb, ob = split_block(b)
            ok = (len(la) == 8 and la == lb and ia == ib and a[0] == b[0] and a[-1] == b[-1]
                  and len(sa) == len(sb) == 8
                  and [re.sub(r'ymm\d+', 'R', l) for l in sa] == [re.sub(r'ymm\d+', 'R', l) for l in sb])
            addr_a, rest_a = oa.split(' : ')
            addr_b, rest_b = ob.split(' : ')
            ok = ok and rest_a == rest_b and addr_b.startswith(addr_a) and all(
                x.startswith('"m"(fht_k8_') for x in addr_b[len(addr_a):].split(', ')[1:])
            if ok:
                changed += 1
            else:
                bad += 1
        print('%s: %d pieces; %d the same; %d blocks of 8 registers differ in their three levels between registers '
              '(and in the registers stored, and by the constants); %d other differences%s'
              % (other_path, len(base), same, changed, bad, '' if bad == 0 else '  <-- NOT CONFINED'))


if __name__ == '__main__':
    main()
