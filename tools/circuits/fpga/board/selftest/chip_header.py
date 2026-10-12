#!/usr/bin/env python3
"""Make the netlist written by icebox_vlog acceptable to Icarus Verilog.

icebox_vlog declares the ports in the module header (input clk, output ...) and then declares the
same names again as wire or reg, which Icarus rejects.  This rewrites ONLY the header line into the
older form (names in the header, directions on separate lines).  Every other line is copied.
    python3 chip_header.py build/selftest_chip.v build/selftest_chip_sim.v
"""
import re
import sys

src = open(sys.argv[1]).read().split("\n")
out = []
done = 0
for ln in src:
    m = re.match(r"^module (\w+) \((.*)\);$", ln)
    if m and done == 0:
        ports = [p.strip() for p in m.group(2).split(",")]
        names = []
        decl = []
        for p in ports:
            d, name = p.split(" ", 1)
            assert d in ("input", "output", "inout"), p
            names.append(name.strip())
            decl.append("%s %s ;" % (d, name.strip()))
        out.append("module %s (%s );" % (m.group(1), " , ".join(names)))
        out.extend(decl)
        done += 1
    else:
        out.append(ln)
assert done == 1, "module header not found exactly once"
open(sys.argv[2], "w").write("\n".join(out))
print("header rewritten: %d ports" % len(names))
