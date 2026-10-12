#!/usr/bin/env python3
"""Compare bytes received from the self-test (simulated or from the board) with expected.py.

    python3 compare.py CAPTURE [--pps 375] [--min-lines 3] [--max-k 600]

CAPTURE is a file of raw bytes as they came off the serial port.  The first and the last piece may
be incomplete (the port was opened or closed in the middle of a line); they are reported and not
counted.  Every complete line must be exactly the line expected.py gives for its number k.
Exit status 0: at least --min-lines complete lines and every one equal to the expected line, the
k values consecutive, bad = 0.  Exit status 1 otherwise.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import expected as E  # noqa: E402

RX = re.compile(r"^WHT8 k=([0-9A-F]{4}) n=([0-9A-F]{8}) bad=([0-9A-F]{8}) ctl=([0-9A-F]{8}) "
                r"sum=([0-9A-F]{8}) ref=([0-9A-F]{8})$")


def judge(data, pps=E.PPS, min_lines=3, max_k=600, out=sys.stdout):
    text = data.decode("latin-1")
    pieces = text.split("\n")
    tail = pieces.pop()            # after the last line feed: empty or an unfinished line
    notes = []
    if tail:
        notes.append("unfinished last piece ignored: %r" % tail[:80])
    lines = []
    for i, p in enumerate(pieces):
        if not p.endswith("\r"):
            notes.append("piece %d has no carriage return: %r" % (i, p[:80]))
            lines.append((p, False))
            continue
        lines.append((p[:-1], True))
    if lines and not RX.match(lines[0][0]):
        notes.append("unfinished first piece ignored: %r" % lines[0][0][:80])
        lines.pop(0)
    ok = True
    parsed = []
    for s, cr in lines:
        m = RX.match(s)
        if not m or not cr:
            ok = False
            out.write("NOT A REPORT LINE: %r\n" % s[:100])
            continue
        parsed.append((int(m.group(1), 16), s, int(m.group(3), 16)))
    if not parsed:
        out.write("no complete report line in %d bytes\n" % len(data))
        for nt in notes:
            out.write("note: %s\n" % nt)
        out.write("RESULT: FAIL\n")
        return False
    kmax = max(k for k, _, _ in parsed)
    if kmax > max_k:
        out.write("k = %d is beyond --max-k %d (the model takes about 1.2 s per second of board time); "
                  "raise --max-k or load the image again and read sooner\n" % (kmax, max_k))
        out.write("RESULT: FAIL\n")
        return False
    exp = {}
    for ln in E.run(max(kmax, 1), pps):
        s = ln.rstrip("\r\n")
        exp[int(RX.match(s).group(1), 16)] = s
    prev = None
    nmatch = 0
    for k, s, bad in parsed:
        good = (exp.get(k) == s)
        nmatch += good
        if not good:
            ok = False
        if bad != 0:
            ok = False
        if prev is not None and k != prev + 1:
            ok = False
            out.write("k jumps from %d to %d\n" % (prev, k))
        prev = k
        out.write("%s  %s\n" % ("same " if good else "DIFF ", s))
        if not good:
            out.write("       expected: %s\n" % exp.get(k, "(no such k)"))
    for nt in notes:
        out.write("note: %s\n" % nt)
    if len(parsed) < min_lines:
        ok = False
        out.write("only %d complete lines, at least %d wanted\n" % (len(parsed), min_lines))
    out.write("%d complete lines, %d equal to the model, k = %d..%d\n"
              % (len(parsed), nmatch, parsed[0][0], parsed[-1][0]))
    out.write("RESULT: %s\n" % ("PASS" if ok else "FAIL"))
    return ok


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("capture")
    ap.add_argument("--pps", type=int, default=E.PPS)
    ap.add_argument("--min-lines", type=int, default=3)
    ap.add_argument("--max-k", type=int, default=600)
    a = ap.parse_args()
    data = open(a.capture, "rb").read()
    sys.exit(0 if judge(data, a.pps, a.min_lines, a.max_k) else 1)


if __name__ == "__main__":
    main()
