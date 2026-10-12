#!/usr/bin/env python3
"""Read the pin settings back out of the image and check them against the pin file.

  <suite>/bin/tabbypy3 check_bitstream.py build/selftest_unpacked.asc hx8k.pcf

The input is the text form that iceunpack makes from the very .bin that would be loaded.
For every ball of the CT256 package this prints nothing unless the pin is in use; at the end it
prints the totals and fails (exit 1) if
  - any pin other than those in the pin file has its output driver or its input buffer switched on,
  - an output of the pin file is not an output in the image, or the clock is not an input.

Meaning of the bits (IceStorm documentation, "IO Tile", copy in ../docs/icestorm/icestorm-io.html):
  PINTYPE_5..2 = 0000  no output driver;   IE bit (8k devices: active high) = input buffer on;
  REN bit (active low) = 0 means the weak pull-up is ON.  "An unused IO tile on an 8k chip has all
  bits cleared": output off, input buffer off, pull-up on.
"""
import os
import re
import sys

SUITE = os.environ.get("OSS_CAD_SUITE", "/opt/oss-cad-suite")      # the unpacked oss-cad-suite
sys.path.insert(0, os.path.join(SUITE, "libexec"))
import icebox  # noqa: E402


def main():
    asc, pcf = sys.argv[1], sys.argv[2]
    want = {}
    for ln in open(pcf):
        m = re.match(r"\s*set_io\s+(\S+)\s+(\S+)", ln)
        if m:
            want[m.group(2)] = m.group(1)
    ic = icebox.iceconfig()
    ic.read_file(asc)
    assert ic.device == "8k", ic.device
    ieren = {(e[0], e[1], e[2]): (e[3], e[4], e[5]) for e in ic.ieren_db()}
    pins = ic.pinloc_db("ct256")
    rows = []
    for pin, x, y, z in pins:
        tc = icebox.tileconfig(ic.tile(x, y))
        ptype = ["0"] * 6
        for entry in ic.tile_db(x, y):
            if entry[1] == "IOB_%d" % z and entry[2].startswith("PINTYPE_") and tc.match(entry[0]):
                ptype[int(entry[2][8:])] = "1"
        # PINTYPE string in the order 5..0
        pt = "".join(reversed(ptype))
        ie = ren = None
        if (x, y, z) in ieren:
            ix, iy, iz = ieren[(x, y, z)]
            tci = icebox.tileconfig(ic.tile(ix, iy))
            for entry in ic.tile_db(ix, iy):
                if entry[1] == "IoCtrl" and entry[2] == "IE_%d" % iz:
                    ie = tci.match(entry[0])
                if entry[1] == "IoCtrl" and entry[2] == "REN_%d" % iz:
                    ren = tci.match(entry[0])
        rows.append((pin, x, y, z, pt, ie, ren))
    bad = 0
    n_out = n_in = n_pull = n_quiet = 0
    print("ball  tile      PINTYPE(5..0)  output  input-buffer  pull-up  signal")
    for pin, x, y, z, pt, ie, ren in sorted(rows, key=lambda r: (r[0][0], int(r[0][1:]))):
        out_on = pt[0:4] != "0000"
        in_on = bool(ie)
        pull_on = (ren is False)
        name = want.get(pin, "")
        n_out += out_on
        n_in += in_on
        n_pull += pull_on
        if not out_on and not in_on:
            n_quiet += 1
        if out_on or in_on or name:
            print("%-5s (%2d,%2d,%d) %s         %-6s  %-12s  %-7s  %s" % (
                pin, x, y, z, pt, "ON" if out_on else "off", "ON" if in_on else "off",
                "on" if pull_on else ("off" if ren else "?"), name or "** NOT IN THE PIN FILE **"))
        if (out_on or in_on) and not name:
            bad += 1
        if name == "clk":
            if out_on or not in_on:
                bad += 1
                print("   ** clk must be an input only")
        elif name:
            if not out_on:
                bad += 1
                print("   ** %s must be an output" % name)
    # pins wired to the FT2232H on the board (guide pp. 13, 14, 17): the image must not drive them
    quiet = [("B10", "RS232_Rx_TTL, driven by the FT2232H (BDBUS0)"), ("B13", "RTSn, FT2232H output (BDBUS2)"),
             ("A16", "DTRn, FT2232H output (BDBUS4)"), ("A15", "CTSn, FT2232H input"),
             ("B14", "DSRn, FT2232H input"), ("B15", "DCDn, FT2232H input"),
             ("P12", "SPI_SO, net iCE_MISO"), ("P11", "SPI_SI, net iCE_MOSI"),
             ("R11", "SPI_SCK, net iCE_SCK"), ("R12", "SPI_SS_B, net iCE_SS_B")]
    byname = {r[0]: r for r in rows}
    print()
    print("pins wired to the FT2232H that the design does not use:")
    for pin, what in quiet:
        if pin not in byname:
            bad += 1
            print("  %-4s ** not found in the package list" % pin)
            continue
        r = byname[pin]
        out_on = r[4][0:4] != "0000"
        print("  %-4s output %s, input buffer %s, pull-up %s   (%s)" % (
            pin, "ON **" if out_on else "off", "ON" if r[5] else "off",
            "on" if r[6] is False else "off", what))
        if out_on:
            bad += 1
    unused = [r for r in rows if r[0] not in want]
    unused_pull = sum(1 for r in unused if r[6] is False)
    unused_nodata = sum(1 for r in unused if r[6] is None)
    print()
    print("package balls with an I/O cell: %d" % len(rows))
    print("output driver on: %d   input buffer on: %d" % (n_out, n_in))
    print("pins in the pin file: %d   all other pins: %d" % (len(want), len(unused)))
    print("of the other pins: output off and input buffer off: %d;  weak pull-up on: %d;  "
          "no pull-up bit known to icebox: %d" % (
              sum(1 for r in unused if r[4][0:4] == "0000" and not r[5]), unused_pull, unused_nodata))
    missing = sorted(set(want) - set(r[0] for r in rows))
    if missing:
        bad += 1
        print("** pins of the pin file not found in the package: %s" % missing)
    print("RESULT: %s" % ("PASS" if bad == 0 else "FAIL (%d problems)" % bad))
    sys.exit(0 if bad == 0 else 1)


if __name__ == "__main__":
    main()
