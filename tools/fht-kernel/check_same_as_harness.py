#!/usr/bin/env python3
"""check_same_as_harness.py -- is the kernel's code the code that was timed on 22 October 2026?

    python3 -B tools/fht-kernel/check_same_as_harness.py

The timed program is measurements/2026-10-22/x86/harness-hybrid/ (bench_hyb.c, bench_k0.c and the generated
kernels_k0.h).  This kernel library takes from it, word for word: the 8-point steps (g20, the textbook, the balanced
textbook written subtraction first), the 4- and 2-point steps used at the ends, FFHT's thresholds and in-lane
instruction sequences, and the functions that walk FFHT's plan of passes.  This program cuts each of those blocks
out of the harness files and out of whtc_steps.h / whtc_ffht_plan.h and compares them line by line (trailing spaces
ignored).  Standard library only.  Writes nothing.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HARNESS = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'measurements', '2026-10-22', 'x86', 'harness-hybrid')

# (name, harness file, kernel file, kind, start pattern[, end pattern])
#   func:  from the start line to the first line that is exactly "}"
#   line:  the start line alone
#   until: from the start line to the first later line matching the end pattern
#   macro: from the start line to the end of the first #define after it (the first line not ending in a backslash)
#   plus1: as until, and one more line
BLOCKS = [
    ('tb2_nat', 'bench_hyb.c', 'whtc_steps.h', 'func', r'^static inline void tb2_nat\('),
    ('kid_nat', 'bench_hyb.c', 'whtc_steps.h', 'line', r'^static inline void kid_nat\('),
    ('tb4_nat', 'kernels_k0.h', 'whtc_steps.h', 'func', r'^static inline void tb4_nat\('),
    ('tb8_nat', 'kernels_k0.h', 'whtc_steps.h', 'func', r'^static inline void tb8_nat\('),
    ('tb8_balS', 'kernels_k0.h', 'whtc_steps.h', 'func', r'^static inline void tb8_balS\('),
    ('g20_nat', 'kernels_k0.h', 'whtc_steps.h', 'func', r'^static inline void g20_nat\('),
    ('FFHT thresholds', 'bench_hyb.c', 'whtc_ffht_plan.h', 'until', r'^static const int FFHT_THR_F\[31\]',
     r'^static int ffht_thr\('),
    ('FFHT in-lane sequences', 'bench_hyb.c', 'whtc_ffht_plan.h', 'until', r'^#if XT == 0$', r'^#endif$'),
    ('scalar_wht', 'bench_k0.c', 'whtc_ffht_plan.h', 'func', r'^static void scalar_wht\('),
    ('DEFHYB (one pass of the plan)', 'bench_hyb.c', 'whtc_ffht_plan.h', 'macro', r'^typedef void \(\*hfirst_fn\)'),
    ('hvar and HV8', 'bench_hyb.c', 'whtc_ffht_plan.h', 'plus1', r'^typedef struct \{$', r'^#define HV8\('),
    ('hyb_block', 'bench_hyb.c', 'whtc_ffht_plan.h', 'func', r'^static void hyb_block\('),
    ('hyb_rec', 'bench_hyb.c', 'whtc_ffht_plan.h', 'func', r'^static void hyb_rec\('),
    ('hyb', 'bench_hyb.c', 'whtc_ffht_plan.h', 'func', r'^static void hyb\(ET'),
]


def cut(lines, kind, start, end=None):
    rs = re.compile(start)
    for i, line in enumerate(lines):
        if rs.search(line):
            break
    else:
        return None
    if kind == 'line':
        return lines[i:i + 1]
    if kind == 'func':
        for j in range(i, len(lines)):
            if lines[j] == '}':
                return lines[i:j + 1]
    if kind in ('until', 'plus1'):
        re_ = re.compile(end)
        for j in range(i + 1, len(lines)):
            if re_.search(lines[j]):
                return lines[i:j + 1 + (kind == 'plus1')]
    if kind == 'macro':
        seen_define = False
        for j in range(i, len(lines)):
            seen_define |= lines[j].startswith('#define')
            if seen_define and not lines[j].endswith('\\'):
                return lines[i:j + 1]
    return None


def read_lines(path):
    with open(path) as f:
        return [line.rstrip() for line in f.read().split('\n')]


def main():
    bad = 0
    for spec in BLOCKS:
        name, hf, kf, kind, start = spec[:5]
        end = spec[5] if len(spec) > 5 else None
        a = cut(read_lines(os.path.join(HARNESS, hf)), kind, start, end)
        b = cut(read_lines(os.path.join(HERE, kf)), kind, start, end)
        if a is None or b is None:
            print('MISSING %-30s (harness %s: %s, kernel %s: %s)' % (name, hf, a is not None, kf, b is not None))
            bad += 1
        elif a != b:
            print('DIFFERENT %-28s %s vs %s' % (name, hf, kf))
            bad += 1
        else:
            print('same %-32s %3d lines   harness-hybrid/%s = %s' % (name, len(a), hf, kf))
    if bad:
        print('FAIL: %d block(s) differ from the timed harness' % bad)
        return 1
    print('OK: steps identical to the timed harness')
    return 0


if __name__ == '__main__':
    sys.exit(main())
