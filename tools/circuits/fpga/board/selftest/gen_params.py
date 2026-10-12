#!/usr/bin/env python3
"""Write the two generated files of the self-test design.

  selftest_params.vh      the constants of ../expected.py (seed, line template), so that the
                          Verilog and the Python model cannot drift apart
  rtl/8_broken_p_w12.v    the 19-adder transform with ONE adder changed to a subtractor
                          (the last adder of output y7), as the control that the comparator can fail

Run:  python3 gen_params.py     (from this directory; it reads rtl/8_ours_p_w12.v and ../expected.py)
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import expected as E  # noqa: E402

GOOD = "    wire signed [14:0] n_y7 = n_g10_r5 + (n_g4_r5 <<< 1);   // level 6, stage 6\n"
BAD = "    wire signed [14:0] n_y7 = n_g10_r5 - (n_g4_r5 <<< 1);   // BROKEN ON PURPOSE: was '+'\n"


def main():
    tmpl = E.TEMPLATE.encode("ascii")
    assert len(tmpl) == len(E.line(0, 0, 0, 0, 0, 0)), "template and line format differ in length"
    assert tmpl.count(b"#") == 44, "expected 44 hexadecimal digits"
    with open(os.path.join(HERE, "selftest_params.vh"), "w") as f:
        f.write("// Written by gen_params.py from ../expected.py.  Do not edit by hand.\n")
        f.write("localparam integer LEN = %d;\n" % len(tmpl))
        f.write("// The line, one byte per character, first character in the top byte; '#' (8'h23) = next hex digit.\n")
        f.write("localparam [8*LEN-1:0] TMPL = %d'h%s;\n" % (8 * len(tmpl), tmpl.hex().upper()))
        f.write("// Start value of the 521-bit shift register.\n")
        f.write("localparam [520:0] SEED = 521'h%X;\n" % E.SEED)
        f.write("localparam integer LFSR_Q = %d;\n" % E.LFSR_Q)
    src = open(os.path.join(HERE, "rtl", "8_ours_p_w12.v")).read()
    assert src.count(GOOD) == 1, "the y7 line was not found exactly once"
    out = src.replace(GOOD, BAD)
    assert out.count("module wht_8_ours_p_w12 (") == 1
    out = out.replace("module wht_8_ours_p_w12 (", "module wht_8_broken_p_w12 (")
    out = out.replace("// Written by gen_rtl.py.  Do not edit by hand.\n",
                      "// Written by board/selftest/gen_params.py from rtl/8_ours_p_w12.v (sha256 %s).\n"
                      "// DELIBERATELY BROKEN: the adder of output y7 is a subtractor.  Control for the comparator only.\n"
                      % hashlib.sha256(src.encode()).hexdigest())
    with open(os.path.join(HERE, "rtl", "8_broken_p_w12.v"), "w") as f:
        f.write(out)
    print("selftest_params.vh: LEN = %d, seed %d bits" % (len(tmpl), E.SEED.bit_length()))
    print("rtl/8_broken_p_w12.v written: one '+' changed to '-' in the line of n_y7")


if __name__ == "__main__":
    main()
