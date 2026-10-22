#!/usr/bin/env python3
"""asmcount_hyb.py FILE.asm... -- per hybrid step function (hfirst_<kernel>, hstep_<kernel>; x86-hybrid, from x86-wht/asmcount.py),
count vector instructions in objdump output:
adds/subs, FMAs, muls, loads/stores, and stack traffic (spills).  Evidence that each circuit line is one instruction.
regmov (twin review, 22 Oct 2026): register-to-register copies vmovap[sd] / vmovup[sd] / vmovdq[au](32|64) %reg,%reg
(masked forms included).  They are not arithmetic but each costs a front-end slot (and, where the copy is not eliminated
at rename, a pipe slot): the FMA-first balanced textbook carried 12 per 8-point step in clang, the circuits 0.
Operand separators may be ',' (GNU objdump, the Colab) or ', ' (llvm-objdump, the Mac)."""
import re, sys
FN = re.compile(r'^[0-9a-f]+ <_?((?:hfirst|hstep)_[\w.]+)>:')
for path in sys.argv[1:]:
    cur, cnt = None, {}
    res = {}
    for line in open(path, errors='replace'):
        m = FN.match(line)
        if m:
            cur = m.group(1)
            res[cur] = cnt = {'add': 0, 'fma': 0, 'mul': 0, 'ld': 0, 'st': 0, 'spill': 0, 'perm': 0, 'regmov': 0}
            continue
        if cur is None:
            continue
        if not line.strip():
            cur = None; continue
        m2 = re.match(r'^\s*[0-9a-f]+:\s*(\S+)\s*(.*)$', line)
        if not m2:
            continue
        op, ops = m2.group(1), m2.group(2)
        ins = op + ' ' + ops
        if re.match(r'v(add|sub)p[sd]', op): cnt['add'] += 1
        elif re.match(r'vf(n?m(add|sub))\d+p[sd]', op): cnt['fma'] += 1
        elif re.match(r'vmulp[sd]', op): cnt['mul'] += 1
        elif re.match(r'vmov(u|a)p[sd]|vmovdq', op):
            if '(%rsp)' in ins or '(%rbp)' in ins: cnt['spill'] += 1
            elif re.search(r'\),\s*%[xyz]mm', ins): cnt['ld'] += 1
            elif re.search(r'%[xyz]mm\d+,.*\(', ins): cnt['st'] += 1
            elif re.match(r'%[xyz]mm\d+,\s*%[xyz]mm\d+', ops) and '(' not in ops: cnt['regmov'] += 1
        elif re.match(r'vperm|vshuf|vblend|vbroadcast', op): cnt['perm'] += 1
    print(f'== {path.split("/")[-1]}')
    for fn in sorted(res):
        c = res[fn]
        if fn != "hstep_kid_nat":
            print(f'  {fn:22s} add/sub {c["add"]:4d} fma {c["fma"]:4d} mul {c["mul"]:3d} ld {c["ld"]:4d} st {c["st"]:4d} '
                  f'stack {c["spill"]:4d} bcast/perm {c["perm"]:3d} regmov {c["regmov"]:3d}')
