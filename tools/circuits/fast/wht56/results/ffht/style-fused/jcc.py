#!/usr/bin/env python3
"""jcc.py -- for every conditional jump of the transform functions in a linked program: does the
jump (with a compare or test fused in front of it) cross a 32-byte boundary or end on one?  On
Skylake-type cores with the 2019 microcode such a jump keeps its 32 bytes out of the decoded-
instruction cache, and a loop closed by it runs slower for a reason that has nothing to do with
its arithmetic.     python3 jcc.py build/harness"""
import re, subprocess, sys
out = subprocess.run(["objdump", "-d", sys.argv[1]], capture_output=True, text=True).stdout
fn = None
prev = None
for line in out.splitlines():
    m = re.match(r"^[0-9a-f]+ <(.+)>:", line)
    if m:
        fn = m.group(1); prev = None; continue
    m = re.match(r"^\s*([0-9a-f]+):\t((?:[0-9a-f]{2} )+)\s*\t(\S+)\s*(.*)", line)
    if not m or fn is None:
        continue
    addr = int(m.group(1), 16); nbytes = len(m.group(2).split()); mn = m.group(3); ops = m.group(4)
    if re.match(r"^j[a-z]+$", mn) and mn != "jmp" and (True):
        start = addr
        if prev and prev[2] in ("cmp", "test", "add", "sub", "dec", "inc", "and") and prev[0] + prev[1] == addr:
            start = prev[0]
        end = addr + nbytes      # one past the last byte
        bad = (start // 32 != (end - 1) // 32) or (end % 32 == 0)
        tgt = re.match(r"([0-9a-f]+)", ops)
        back = tgt and int(tgt.group(1), 16) < addr
        if back:
            print(f"{fn:22s} backward {mn} at {addr:x} (with its compare from {start:x}, {end - start} bytes): "
                  + ("CROSSES or ends on a 32-byte boundary" if bad else "inside one 32-byte block"))
    prev = (addr, nbytes, mn)
