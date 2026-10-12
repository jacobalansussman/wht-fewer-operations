import re, sys
txt = open(sys.argv[1]).read()
for fn in ('t8', 'o8', 'o8s'):
    m = re.search(r'^%s:\n(.*?)\n\s*\.cfi_endproc' % fn, txt, re.S | re.M)
    body = m.group(1).split('\n')
    # find the loop made of ymm instructions: the longest run of lines between a label and a backward jump that uses ymm
    labels = {}
    for i, l in enumerate(body):
        mm = re.match(r'^(\.L\d+):', l)
        if mm: labels[mm.group(1)] = i
    best = None
    for i, l in enumerate(body):
        mm = re.match(r'\s+j\w+\s+(\.L\d+)', l)
        if mm and mm.group(1) in labels and labels[mm.group(1)] < i:
            seg = body[labels[mm.group(1)]:i + 1]
            ny = sum('ymm' in x for x in seg)
            if best is None or ny > best[0]:
                best = (ny, seg)
    seg = best[1]
    ins = [x.split()[0] for x in seg if x.startswith('\t') and not x.strip().startswith('.')]
    arith = sum(1 for x in seg if re.match(r'\s+v(add|sub|mul)pd', x))
    fma = sum(1 for x in seg if 'vfm' in x or 'vfnm' in x)
    loads = sum(1 for x in seg if re.match(r'\s+vmov[au]pd\s+[^%]*\(', x))
    stores = sum(1 for x in seg if re.match(r'\s+vmov[au]pd\s+%ymm\d+,\s*[^%]*\(', x))
    stack = sum(1 for x in seg if '(%rsp)' in x or '(%rbp)' in x)
    memop = sum(1 for x in seg if re.match(r'\s+v(add|sub|mul)pd\s+[^%]*\(', x))
    print('%-4s widest loop: %d instructions; add/sub/mul on ymm: %d (of which with a memory operand: %d); fma: %d; vmov loads: %d; vmov stores: %d; lines touching the stack: %d'
          % (fn, len(ins), arith, memop, fma, loads, stores, stack))
