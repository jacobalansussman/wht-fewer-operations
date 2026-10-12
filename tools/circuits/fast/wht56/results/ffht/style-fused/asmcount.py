#!/usr/bin/env python3
"""asmcount.py -- count the instructions in the hot loop of each pass3 function of a gcc listing.

    python3 asmcount.py build/whtf.s [--print NAME]

The hot loop of FUNC_pass3 is the innermost loop: the shortest stretch between a label and a
backward conditional jump to it that contains at least 8 stores.  Per turn of that loop (8
registers) it prints: arithmetic instructions by name, loads, stores, register copies, anything
that touches the stack (spills), and the instructions of the loop itself.
"""
import re
import sys
from collections import Counter

ARITH = re.compile(r'^(vadd|vsub|vfmadd|vfnmadd|vfmsub|vfnmsub|vmul|vpadd|vpsub|vpsll|add[lq]?$|sub[lq]?$|lea|neg|sal|shl|imul)')


def functions(text):
    out, name, body = {}, None, []
    for line in text.splitlines():
        m = re.match(r'^([A-Za-z_][\w.]*):', line)
        if m and not line.startswith('.'):
            if name:
                out[name] = body
            name, body = m.group(1), []
        elif name is not None:
            body.append(line)
    if name:
        out[name] = body
    return out


def hot_loop(body):
    labels = {}
    ins = []
    for line in body:
        s = line.strip()
        if not s or s.startswith('#'):
            continue
        m = re.match(r'^(\.L\d+):', s)
        if m:
            labels[m.group(1)] = len(ins)
            continue
        if s.startswith('.'):
            continue
        ins.append(s)
    best = None
    for i, s in enumerate(ins):
        m = re.match(r'^j[a-z]+\s+(\.L\d+)', s)
        if m and not s.startswith('jmp') and m.group(1) in labels and labels[m.group(1)] <= i:
            seg = ins[labels[m.group(1)]:i + 1]
            stores = sum(1 for t in seg if is_store(t))
            if stores >= 8 and (best is None or len(seg) < len(best)):
                best = seg
    return best


def split_ops(s):
    parts = s.split(None, 1)
    mn = parts[0]
    ops, depth, cur = [], 0, ''
    for ch in (parts[1] if len(parts) > 1 else ''):
        if ch == '(':
            depth += 1
        if ch == ')':
            depth -= 1
        if ch == ',' and depth == 0:
            ops.append(cur.strip())
            cur = ''
        else:
            cur += ch
    if cur.strip():
        ops.append(cur.strip())
    return mn, ops


def is_mem(op):
    return '(' in op


def is_store(s):
    mn, ops = split_ops(s)
    return bool(ops) and is_mem(ops[-1]) and (mn.startswith('vmov') or mn.startswith('mov'))


def count(seg):
    c = Counter()
    arith = Counter()
    for s in seg:
        mn, ops = split_ops(s)
        mem = [o for o in ops if is_mem(o)]
        stack = any('%rsp' in o or '%rbp' in o for o in mem)
        if is_store(s):
            c['spill stores' if stack else 'stores'] += 1
        elif mn.startswith('vmov') or (mn.startswith('mov') and mem):
            if mem:
                c['spill loads' if stack else 'loads'] += 1
            else:
                c['register copies'] += 1
        elif mn.startswith('mov'):
            c['register copies (general)'] += 1
        elif ARITH.match(mn) and any('ymm' in o for o in ops):
            arith[re.sub(r'(132|213|231)', '', mn)] += 1
            if mem and not mn.startswith('lea'):
                c['spill loads (inside an arithmetic instruction)' if stack else 'loads (inside an arithmetic instruction)'] += 1
        elif ARITH.match(mn):
            # general-register arithmetic: data arithmetic in the scalar functions, address arithmetic in the vector ones
            arith[mn + ' (general register)'] += 1
            if mem and not mn.startswith('lea'):
                c['loads (inside an arithmetic instruction)'] += 1
        elif mn.startswith('j') or mn.startswith('cmp') or mn.startswith('test'):
            c['loop (compare, jump)'] += 1
        else:
            c['other: ' + mn] += 1
    return c, arith


def main():
    path = sys.argv[1]
    want = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '--print' else None
    fns = functions(open(path).read())
    for name in sorted(fns):
        if not name.endswith('_pass3'):
            continue
        seg = hot_loop(fns[name])
        if seg is None:
            print(f'{name}: no loop with 8 stores found')
            continue
        c, arith = count(seg)
        na = sum(arith.values())
        print(f'{name}: {len(seg)} instructions in the loop; arithmetic {na}: ' +
              ', '.join(f'{k} {v}' for k, v in sorted(arith.items())) + ' | ' +
              ', '.join(f'{k} {v}' for k, v in sorted(c.items())))
        if want and name.startswith(want):
            for s in seg:
                print('      ' + s)


if __name__ == '__main__':
    main()
