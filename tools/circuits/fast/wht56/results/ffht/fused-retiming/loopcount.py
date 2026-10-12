import re, subprocess, sys, collections
out = subprocess.run(['objdump', '-d', '--no-show-raw-insn', sys.argv[1]], capture_output=True, text=True).stdout
funcs = {}; cur = None
for line in out.splitlines():
    m = re.match(r'^[0-9a-f]+ <(.+)>:$', line)
    if m: cur = m.group(1); funcs[cur] = []; continue
    m = re.match(r'^\s*([0-9a-f]+):\s+(\S+)\s*(.*)$', line)
    if m and cur: funcs[cur].append((int(m.group(1), 16), m.group(2), m.group(3)))
show = '-v' in sys.argv
for name in [a for a in sys.argv[2:] if a != '-v']:
    ins = funcs[name]
    loops = []
    for a, mn, ops in ins:
        if mn.startswith('j'):
            m = re.match(r'([0-9a-f]+) <', ops)
            if m and int(m.group(1), 16) <= a: loops.append((a - int(m.group(1), 16), int(m.group(1), 16), a))
    loops.sort()
    print('==', name, ':', len(ins), 'instructions in the function; backward jumps (loops):', [(hex(t), hex(a)) for _, t, a in loops])
    for span, t, a in loops[:1] if not show else loops[:1]:
        body = [(x, mn, ops) for x, mn, ops in ins if t <= x <= a]
        c = collections.Counter(mn for _, mn, _ in body)
        arith = {k: v for k, v in c.items() if re.match(r'v(add|sub|mul|fmadd|fnmadd|fmsub|fnmsub|padd|psub|psll)', k)}
        mem_src = sum(1 for _, mn, ops in body if '(' in ops.split(',')[0] and not mn.startswith(('lea', 'nop', 'j')))
        mem_dst = sum(1 for _, mn, ops in body if '(' in ops.split(',')[-1] and ',' in ops and '(' not in ops.split(',')[0] and not mn.startswith(('lea', 'nop', 'j')))
        print('   innermost loop: %d instructions; arithmetic %d %s' % (len(body), sum(arith.values()), dict(sorted(arith.items()))))
        print('   all mnemonics:', dict(sorted(c.items())))
        print('   instructions reading memory: %d; writing memory: %d' % (mem_src, mem_dst))
        if show:
            for x, mn, ops in body: print('      %x: %-14s %s' % (x, mn, ops))
