#!/usr/bin/env python3
"""kloop_table.py -- the table of one 8-register pass alone, from the output of kloop.

    python3 -B kloop_table.py out/kloop-1.txt [out/kloop-2.txt ...]
"""
import re
import sys

INFO = {    # kernel: (what, operations, longest chain, vector instructions between loads and stores)
    'T': ('FFHT\'s textbook block', '24 add/sub', 3, 24),
    'S20': ('test only: textbook block without 4 of its last operations', '20 add/sub', 3, 20),
    'H20': ('20-operation block', '19 add/sub, 1 mul', 7, 20),
    'D24': ('test only: 20-operation block with an addition for its halving and 4 unused additions', '24 add/sub', 7, 24),
    'H20x': ('20-operation block with the 8 repairing multiplications, constant in memory', '19 add/sub, 9 mul', 8, 28),
    'H20xr': ('the same, constant loaded into a register', '19 add/sub, 9 mul, 1 load', 8, 29),
    'F19m': ('19-gate block, constant 2 in memory', '7 add/sub, 12 multiply-add', 6, 19),
    'F19r': ('19-gate block, constant 2 in a register', '7 add/sub, 12 multiply-add, 1 load', 6, 20),
}
ORDER = ['T', 'S20', 'H20', 'D24', 'H20x', 'H20xr', 'F19m', 'F19r']

for path in sys.argv[1:]:
    rows = {}
    for line in open(path):
        if not line.startswith('K '):
            continue
        kv = dict(m.groups() for m in re.finditer(r'(\w+)=(\S+)', line))
        rows.setdefault((kv['type'], int(kv['log_n'])), {})[kv['kernel']] = kv
    print('### %s\n' % path)
    for (typ, L) in sorted(rows, key=lambda x: (x[0] != 'float', x[1])):
        r = rows[(typ, L)]
        any_k = next(iter(r.values()))
        short = float(any_k['shortest_loop_s'])
        cyc_ns = float(any_k['ns_per_cycle'])
        ok = short >= 0.2 and cyc_ns < 0.40 and any_k.get('cycle_ok', '1') == '1'
        print('%ss, 2^%d numbers (%s bytes), %s repeats, one cycle = %s ns, shortest loop %.3f s: %s\n' % (
            typ, L, any_k['bytes'], any_k['repeats'], any_k['ns_per_cycle'], short,
            'COUNTS' if ok else 'DOES NOT COUNT (%s)' % '; '.join(
                [x for x in ['a loop shorter than 0.2 s' if short < 0.2 else '',
                             'the cycle measurement was disturbed' if not (cyc_ns < 0.40 and any_k.get('cycle_ok', '1') == '1') else ''] if x])))
        print('| kernel | what | operations | longest chain | instructions in the loop | ns per block: best (median, worst) | '
              'cycles per block, without the copy: best (median) | against T | instructions per cycle |')
        print('|---|---|---|---|---|---|---|---|---|')
        base = float(r['T']['cycles_per_block_net_min'])
        for k in ORDER:
            if k not in r:
                continue
            kv = r[k]
            what, ops, chain, n = INFO[k]
            cyc = float(kv['cycles_per_block_net_min'])
            loop = 16 + n + 10
            print('| `%s` | %s | %s | %d | %d | %.3f (%.3f, %.3f) | %.2f (%.2f) | %+.1f %% | %.2f |' % (
                k, what, ops, chain, loop, float(kv['min']) if 'min' in kv else float(kv['ns_per_block_min']),
                float(kv['med']), float(kv['max']), cyc, float(kv['net_med']), 100 * (cyc - base) / base, loop / cyc))
        if 'copy' in r:
            print('\nThe copy and the loop around the passes cost %.3f ns per block (taken off above).\n' % float(r['copy']['ns_per_block_min']))
