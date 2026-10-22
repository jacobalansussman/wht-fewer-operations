#!/usr/bin/env python3
"""check_circuits.py -- replay every circuit file of the 22 October 2026 measurements in exact arithmetic.

    python3 -B measurements/2026-10-22/circuits/check_circuits.py

For each file in this folder it runs the checker of this repository, tools/circuits/slp.py, which computes the
program on all N unit vectors at once with exact integers (and, for N <= 64, entry by entry) and on random integer
vectors, and compares the result with the Walsh-Hadamard matrix H.  It prints the two counts of the repository
(count G: doublings free; count O: every operation charged), the factor of each output row, and, for the files
that were already published, the published file that is byte-identical.  It also checks that every copy of a
circuit file inside the harness folders (../x86/harness-*/circuits, ../gpu/harness-wht/circuits) is
byte-identical to the file here, so the harnesses timed exactly these circuits.

Standard library only.  Writes nothing.  A Python check, not a proof.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MEAS = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(MEAS))
sys.path.insert(0, os.path.join(REPO, 'tools', 'circuits'))
import slp  # noqa: E402

# the name each file has in the timing programs, and what it is
ROLE = {
    'h8_textbook_24.txt': ('tb8', 'the textbook 8-point step (24 additions and subtractions)'),
    'h16_textbook_64.txt': ('tb16', 'the textbook 16-point step (64)'),
    'h4_textbook_8.txt': ('tb4', 'the textbook 4-point step (8)'),
    'h8_G19.txt': ('g19', 'the 19-operation 8-point step of count G (the 5/6 construction)'),
    'h8_G20_family.txt': ('g20', 'the 20-operation 8-point step of the 3/4 family'),
    'h8_G22_depth4.txt': ('g22d4', 'a 22-operation 8-point step of depth 4 (new in these files)'),
    'h8_O20_half.txt': ('h20half', 'the 20-operation step whose output is H x / 2'),
    'h8_ar22.txt': ('ar22', "Alman and Rao's 8-point step, transcribed (new in these files)"),
    'h16_G52_family.txt': ('g52', 'the 52-operation 16-point step of the 3/4 family'),
    'h16_G54_depth7.txt': ('g54d7', 'a 54-operation 16-point step of depth 7 (new in these files)'),
    'h16_G56_depth6.txt': ('g56d6', 'a 56-operation 16-point step of depth 6 (new in these files)'),
    'h16_G60_depth5.txt': ('g60d5', 'a 60-operation 16-point step of depth 5 (new in these files)'),
}


def published_twin(path):
    data = open(path, 'rb').read()
    base = os.path.join(REPO, 'tools', 'circuits', 'programs')
    hits = []
    for root, _, files in os.walk(base):
        for f in files:
            q = os.path.join(root, f)
            if f.endswith('.txt') and open(q, 'rb').read() == data:
                hits.append(os.path.relpath(q, REPO))
    return sorted(hits)


def main():
    files = sorted(f for f in os.listdir(HERE) if f.endswith('.txt'))
    bad = 0
    print('%-22s %-8s %3s %4s %4s  %-9s  %s' % ('file', 'name', 'N', '(G)', '(O)', 'factor', 'already published as'))
    for f in files:
        p = slp.parse_file(os.path.join(HERE, f))
        try:
            r = slp.verify(p, labelled=True)
        except AssertionError as e:
            print('%-22s FAIL: %s' % (f, e))
            bad += 1
            continue
        twin = published_twin(os.path.join(HERE, f))
        name = ROLE.get(f, ('?', ''))[0]
        print('%-22s %-8s %3d %4d %4d  %-9s  %s' % (f, name, r['N'], r['G'], r['O'], slp.fmt_fac(r['factors']),
                                                   twin[0] if twin else '(new)'))
    # the copies inside the harness folders
    copies = 0
    for top in ('x86', 'gpu'):
        for d in sorted(os.listdir(os.path.join(MEAS, top))):
            cd = os.path.join(MEAS, top, d, 'circuits')
            if not os.path.isdir(cd):
                continue
            for f in sorted(os.listdir(cd)):
                if not f.endswith('.txt'):
                    continue
                copies += 1
                here = os.path.join(HERE, f)
                if not os.path.exists(here) or open(here, 'rb').read() != open(os.path.join(cd, f), 'rb').read():
                    print('COPY DIFFERS: %s/%s/circuits/%s' % (top, d, f))
                    bad += 1
    print('%d copies in the harness folders, each byte-identical to the file here' % copies if not bad else
          'some copies differ')
    if bad:
        print('FAIL: %d problem(s)' % bad)
        return 1
    print('OK: %d circuit files, each exact on every unit vector.' % len(files))
    return 0


if __name__ == '__main__':
    sys.exit(main())
