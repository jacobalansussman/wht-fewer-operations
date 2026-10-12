#!/usr/bin/env python3
"""What the self-test image sends on the serial port, computed on the Mac.

Usage:
    python3 expected.py                 the lines for the first 10 seconds (11 lines: k=0..10)
    python3 expected.py --seconds 30    the lines up to second 30
    python3 expected.py --check         also recompute every vector the slow way, from the definition
                                        of the transform, and compare (about 20 times slower)
    python3 expected.py --pps 4         "seconds" of 4 periods, as the short simulation uses

The model needs only the Python standard library.  It is the definition of the design, not a copy of
the Verilog: the transform is computed from y_J = sum_i (-1)^popcount(J & i) * x_i.

THE DESIGN IT MODELS (selftest/selftest_top.v), 12 MHz clock, 8 points, 12-bit signed inputs
  Time is cut into periods of 32,000 clocks.  In the first 2,000 clocks of every period the design
  feeds one input vector per clock (back to back) to three circuits:
      the textbook 8-point transform       (24 adders, 3 levels, a register after every level)
      the 19-adder transform of this work  (19 adders, 6 levels, a register after every level)
      a broken copy of the 19-adder one    (the last adder of output y7 changed to a subtractor)
  Vectors 0..255 of each burst are extreme values: input i is -2048 if bit i of the position is 1,
  else +2047 (all 256 sign patterns).  Vectors 256..1999 are 96 fresh bits of a 521-bit shift
  register with feedback b[t] = b[t-521] xor b[t-353].  The register advances on every vector.
  The comparator counts
      n    vectors that left the 19-adder transform
      bad  vectors where the 19-adder transform differs from the textbook (expected 0)
      ctl  vectors where the broken copy differs from the textbook (expected: every vector with
           x3 != x4, because the broken output is y7 - 4*(x3 - x4))
      sum  running checksum of the 19-adder outputs: sum += fold(out) xor n, modulo 2^32, where out
           is the 120-bit output bus (y0 in bits 14..0, ... y7 in bits 119..105) and fold is the
           xor of its four 32-bit pieces
      ref  the same checksum taken from the textbook outputs
  375 periods are one second (12,000,000 clocks, 750,000 vectors).  At the end of every second the
  design sends one line at 115,200 baud (8 data bits, no parity, one stop bit):
      WHT8 k=KKKK n=NNNNNNNN bad=BBBBBBBB ctl=CCCCCCCC sum=SSSSSSSS ref=RRRRRRRR<CR><LF>
  all numbers in hexadecimal; k is the number of seconds finished.  One extra line with k=0000 is
  sent at the end of the very first period (after 2,000 vectors, 2.7 ms after the start), so that a
  short simulation of the real image has a line to check.  On the board that line is normally gone
  before the serial port is open.
"""
import argparse
import hashlib
import sys

N = 8                 # points
W = 12                # input bits, signed
OW = 15               # output bits, signed
CLK_HZ = 12000000
PERIOD = 32000        # clocks per period
BURST = 2000          # vectors per period
CORNER = 256          # extreme-value vectors at the start of each burst
PPS = 375             # periods per second
BAUD_DIV = 104        # clocks per serial bit
LFSR_P = 521
LFSR_Q = 353
L = N * W             # bits taken from the shift register per vector
TAG = "WHT8"
LINE_FMT = "{tag} k={k:04X} n={n:08X} bad={bad:08X} ctl={ctl:08X} sum={csum:08X} ref={ref:08X}\r\n"
TEMPLATE = "WHT8 k=#### n=######## bad=######## ctl=######## sum=######## ref=########\r\n"

M32 = 0xFFFFFFFF
ML = (1 << L) - 1
MP = (1 << LFSR_P) - 1
SEED_TEXT = b"wht41 fpga self-test seed, 11 October 2026"
SEED = int.from_bytes(hashlib.sha512(SEED_TEXT + b"/0").digest()
                      + hashlib.sha512(SEED_TEXT + b"/1").digest(), "big") & MP


def lfsr_step(s):
    """One advance of the 521-bit register by 96 bits.  Bit i of s is b[T-1-i]."""
    new = ((s >> (LFSR_P - L)) ^ (s >> (LFSR_Q - L))) & ML
    return ((s << L) | new) & MP


def signed(v, bits):
    v &= (1 << bits) - 1
    return v - (1 << bits) if v >> (bits - 1) else v


def corner_vector(ph):
    return [(-2048 if (ph >> i) & 1 else 2047) for i in range(N)]


def random_vector(s):
    return [signed(s >> (W * i), W) for i in range(N)]


def wht_definition(x):
    return [sum((-x[i] if bin(j & i).count("1") & 1 else x[i]) for i in range(N)) for j in range(N)]


def pack(y):
    o = 0
    for j in range(N):
        o |= (y[j] & 0x7FFF) << (OW * j)
    return o


def fold(o):
    return (o ^ (o >> 32) ^ (o >> 64) ^ (o >> 96)) & M32


def broken_y7(x):
    """Output y7 of the broken copy, following the generated Verilog line by line with its widths.

    rtl/v/8_ours_p_w12.v:  n_g4 = x3 - x4 (13 bits);  n_g1 = x0 + x7;  n_g2 = x1 + x6;  n_g3 = x2 - x5
    (13 bits);  n_g5 = n_g1 - n_g2;  n_g6 = n_g3 + n_g4 (14 bits);  n_g7 = n_g5 - n_g6;
    n_g8 = n_g7 - 2*x7;  n_g10 = n_g8 + 2*x6 (15 bits);  n_y7 = n_g10 + 2*n_g4 (15 bits).
    The broken copy has n_y7 = n_g10 - 2*n_g4.
    """
    g1 = signed(x[0] + x[7], 13)
    g2 = signed(x[1] + x[6], 13)
    g3 = signed(x[2] - x[5], 13)
    g4 = signed(x[3] - x[4], 13)
    g5 = signed(g1 - g2, 14)
    g6 = signed(g3 + g4, 14)
    g7 = signed(g5 - g6, 15)
    g8 = signed(g7 - 2 * x[7], 15)
    g10 = signed(g8 + 2 * x[6], 15)
    good = signed(g10 + 2 * g4, 15)
    broken = signed(g10 - 2 * g4, 15)
    return good, broken


def slow_vector(x):
    """(fold of the true outputs, 1 if the broken copy differs) from the definition."""
    y = wht_definition(x)
    for v in y:
        assert -(1 << (OW - 1)) <= v < (1 << (OW - 1)), "output does not fit 15 bits"
    good, broken = broken_y7(x)
    assert good == y[7], "the 19-adder line for y7 does not give row 7 of the transform"
    differs = 1 if broken != y[7] else 0
    assert differs == (1 if x[3] != x[4] else 0)
    return fold(pack(y)), differs


def line(k, n, bad, ctl, csum, ref):
    return LINE_FMT.format(tag=TAG, k=k & 0xFFFF, n=n & M32, bad=bad & M32, ctl=ctl & M32,
                           csum=csum & M32, ref=ref & M32)


def run(seconds, pps=PPS, check=False, progress=None):
    """Return the list of lines (with CR LF) the design sends: k = 0, 1, ..., seconds."""
    corner = [slow_vector(corner_vector(ph)) for ph in range(CORNER)]
    cfold = [c[0] for c in corner]
    cdiff = [c[1] for c in corner]
    bias = 0
    for i in range(N):
        bias |= 0x800 << (W * i)
    sh1 = LFSR_P - L
    sh2 = LFSR_Q - L
    s = SEED
    n = 0
    ctl = 0
    csum = 0
    out = []
    for p in range(seconds * pps):
        # extreme-value vectors; the register still advances
        for ph in range(CORNER):
            csum = (csum + (cfold[ph] ^ (n & M32))) & M32
            ctl += cdiff[ph]
            n += 1
            s = ((s << L) | (((s >> sh1) ^ (s >> sh2)) & ML)) & MP
        for ph in range(CORNER, BURST):
            d = s & ML
            s = ((s << L) | (((s >> sh1) ^ (s >> sh2)) & ML)) & MP
            # x_i + 2048 for every input, then the fast transform; only y0 carries the offset 8*2048
            v = d ^ bias
            a0 = v & 4095
            a1 = (v >> 12) & 4095
            a2 = (v >> 24) & 4095
            a3 = (v >> 36) & 4095
            a4 = (v >> 48) & 4095
            a5 = (v >> 60) & 4095
            a6 = (v >> 72) & 4095
            a7 = v >> 84
            b0 = a0 + a1; b1 = a0 - a1; b2 = a2 + a3; b3 = a2 - a3
            b4 = a4 + a5; b5 = a4 - a5; b6 = a6 + a7; b7 = a6 - a7
            c0 = b0 + b2; c2 = b0 - b2; c1 = b1 + b3; c3 = b1 - b3
            c4 = b4 + b6; c6 = b4 - b6; c5 = b5 + b7; c7 = b5 - b7
            o = (((c0 + c4 - 16384) & 32767)
                 | (((c1 + c5) & 32767) << 15)
                 | (((c2 + c6) & 32767) << 30)
                 | (((c3 + c7) & 32767) << 45)
                 | (((c0 - c4) & 32767) << 60)
                 | (((c1 - c5) & 32767) << 75)
                 | (((c2 - c6) & 32767) << 90)
                 | (((c3 - c7) & 32767) << 105))
            f = (o ^ (o >> 32) ^ (o >> 64) ^ (o >> 96)) & M32
            if check:
                sf, sd = slow_vector(random_vector(d))
                assert sf == f and sd == (1 if a3 != a4 else 0)
            csum = (csum + (f ^ (n & M32))) & M32
            if a3 != a4:
                ctl += 1
            n += 1
        if p == 0:
            out.append(line(0, n, 0, ctl, csum, csum))
        if (p + 1) % pps == 0:
            out.append(line((p + 1) // pps, n, 0, ctl, csum, csum))
            if progress:
                progress((p + 1) // pps)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--seconds", type=int, default=10)
    ap.add_argument("--pps", type=int, default=PPS, help="periods per second (375 on the board)")
    ap.add_argument("--check", action="store_true", help="recompute every vector from the definition")
    ap.add_argument("--quiet", action="store_true", help="no progress on stderr")
    a = ap.parse_args()
    prog = None
    if not a.quiet and a.pps * a.seconds > 400:
        prog = lambda k: sys.stderr.write("  second %d of %d done\n" % (k, a.seconds))
    for ln in run(a.seconds, a.pps, a.check, prog):
        sys.stdout.write(ln.rstrip("\r\n") + "\n")


if __name__ == "__main__":
    main()
