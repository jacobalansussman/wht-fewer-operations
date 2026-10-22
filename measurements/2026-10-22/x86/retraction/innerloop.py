"""innerloop.py FILE.asm FN... -- instructions in the innermost loop (first backward branch) of each function, by kind."""
import re, sys
path, fns = sys.argv[1], sys.argv[2:]
cur, body = None, {}
for line in open(path, errors='replace'):
    m = re.match(r'^[0-9a-f]+ <_?([\w.]+)>:', line)
    if m:
        cur = m.group(1) if m.group(1) in fns else None
        if cur: body[cur] = []
        continue
    if cur is None: continue
    m2 = re.match(r'^\s*([0-9a-f]+):\s*(\S+)\s*(.*)$', line)
    if m2: body[cur].append((int(m2.group(1), 16), m2.group(2), m2.group(3)))
for fn in fns:
    ins = body.get(fn, [])
    for i, (a, op, ops) in enumerate(ins):
        t = re.match(r'(?:0x)?([0-9a-f]+)\b', ops)
        if op.startswith('j') and t and int(t.group(1), 16) < a:
            lo = int(t.group(1), 16); loop = [x for x in ins if lo <= x[0] <= a]
            k = {'load': 0, 'store': 0, 'regmov': 0, 'fma': 0, 'add/sub': 0, 'other': 0}
            for _, o, s in loop:
                if re.match(r'vmov', o):
                    if '(' not in s: k['regmov'] += 1
                    elif re.search(r'\),\s*%[xyz]mm', s): k['load'] += 1
                    else: k['store'] += 1
                elif o.startswith('vf'): k['fma'] += 1
                elif re.match(r'v(add|sub)p', o): k['add/sub'] += 1
                else: k['other'] += 1
            print(f'{fn:18s} inner loop {len(loop):3d} instructions  ' + '  '.join(f'{x} {y}' for x, y in k.items()))
            break
