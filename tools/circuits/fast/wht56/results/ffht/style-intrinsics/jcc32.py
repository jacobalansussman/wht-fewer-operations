#!/usr/bin/env python3
"""jcc32.py -- which loop-closing jumps of the linked program cross a 32-byte boundary?

    python3 jcc32.py build/harness [name-pattern]

On Intel cores from Skylake to Cascade Lake with the microcode of late 2019, a jump (together
with a compare fused in front of it) that crosses a 32-byte boundary, or ends on one, is not
served from the cache of decoded instructions, and the loop it closes can run slower.  That has
nothing to do with the arithmetic in the loop, so it must not decide a comparison.  This lists,
for every function whose name matches the pattern (default: whti_ and fht_ and helper_), every
backward conditional jump with the length of its loop and whether it is such a jump.
"""
import re
import subprocess
import sys

pat = re.compile(sys.argv[2] if len(sys.argv) > 2 else r'^(whti_|fht_|helper_)')
out = subprocess.run(['objdump', '-d', sys.argv[1]], capture_output=True, text=True).stdout
fn, prev, rows = None, None, []
for line in out.splitlines():
    m = re.match(r'^[0-9a-f]+ <(.+)>:', line)
    if m:
        fn, prev = m.group(1), None
        continue
    m = re.match(r'^\s*([0-9a-f]+):\t((?:[0-9a-f]{2} )+)\s*\t(\S+)\s*(.*)', line)
    if not m or fn is None or not pat.search(fn):
        continue
    addr, nbytes, mn, ops = int(m.group(1), 16), len(m.group(2).split()), m.group(3), m.group(4)
    if re.match(r'^j[a-z]+$', mn) and mn != 'jmp':
        start = addr
        if prev and prev[2] in ('cmp', 'test', 'add', 'sub', 'dec', 'inc', 'and') and prev[0] + prev[1] == addr:
            start = prev[0]
        end = addr + nbytes
        bad = (start // 32 != (end - 1) // 32) or (end % 32 == 0)
        t = re.match(r'([0-9a-f]+)', ops)
        if t and int(t.group(1), 16) < addr:
            rows.append((fn, addr, end - int(t.group(1), 16), bad))
    prev = (addr, nbytes, mn)
nbad = sum(1 for r in rows if r[3])
for fn, addr, length, bad in rows:
    if len(sys.argv) > 3 or bad:
        print('%-28s jump at %x closes a loop of %4d bytes: %s' % (fn, addr, length, 'CROSSES or ends on a 32-byte boundary' if bad else 'inside one 32-byte block'))
print('# %d backward conditional jumps in the functions matching %s; %d cross or end on a 32-byte boundary' % (len(rows), pat.pattern, nbad))
