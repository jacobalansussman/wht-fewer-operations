#!/usr/bin/env python3
"""tables.py -- markdown tables from the harness output files.

    python3 tables.py out/time-float.txt out/time-double.txt out/time-int32.txt [...]

One table per number type.  Per size and variant: min and median of the 9 repeats in nanoseconds
per point for one transform; the ratios of the fused step to the textbook step and to FFHT, as
ratio of the minima and ratio of the medians; and the conditions of the size (attempt kept, how
busy the hyper-thread sibling of the timed processor was).
"""
import re
import sys
from collections import defaultdict, OrderedDict


def parse(paths):
    data = defaultdict(dict)      # (type, k) -> variant -> dict
    cond = {}
    order = defaultdict(list)
    for path in paths:
        pending = {}
        for line in open(path):
            if not line or line[0] not in 'TEA':
                continue
            kv = dict(re.findall(r'(\w+)=(\S+)', line))
            if 'type' not in kv or 'k' not in kv:
                continue
            key = (kv['type'], int(kv['k']))
            if line[0] in 'TE':
                pending.setdefault(key, {})[kv['variant']] = kv
            elif line[0] == 'A':
                # line A closes an attempt; a later attempt of the same size replaces an earlier one
                data[key].update(pending.pop(key, {}))
                cond[key] = kv
        for key, v in pending.items():
            data[key].update(v)
    return data, cond


def f(x, nd=3):
    return f'{float(x):.{nd}f}'


def main():
    data, cond = parse(sys.argv[1:])
    types = OrderedDict()
    for (t, k) in sorted(data):
        types.setdefault(t, []).append(k)
    for t, ks in types.items():
        names = []
        for k in ks:
            for v in data[(t, k)]:
                if v not in names and v != 'empty':
                    names.append(v)
        ref = 'Tp' if 'Tp' in names else ('T' if 'T' in names else names[0])
        fused = next((n for n in ('G19p', 'G19sp', 'G19', 'G19s', 'sG19') if n in names), None)
        ctrl = next((n for n in ('G19ap', 'G19a') if n in names), None)
        print(f'\n### {t}\n')
        head = ['k'] + [f'{n} min / med' for n in names]
        if fused:
            head.append(f'{fused}/{ref} (min; med)')
            if 'ffht' in names:
                head.append(f'{fused}/ffht (min; med)')
        if ctrl:
            head.append(f'{ctrl}/{ref} (min; med)')
        if 'sT' in names and 'sG19' in names:
            head.append('sG19/sT (min; med)')
        if 'Tfp' in names:
            head.append(f'Tfp/{ref} (min; med)')
        head += ['spread of the medians', 'sibling busy', 'attempt']
        print('| ' + ' | '.join(head) + ' |')
        print('|' + '---|' * len(head))
        for k in sorted(set(ks)):
            d = data[(t, k)]
            row = [str(k)]
            for n in names:
                row.append(f"{f(d[n]['min'])} / {f(d[n]['med'])}" if n in d else '')

            def ratio(a, b):
                if a in d and b in d:
                    return (f"{float(d[a]['min']) / float(d[b]['min']):.3f}; "
                            f"{float(d[a]['med']) / float(d[b]['med']):.3f}")
                return ''
            if fused:
                row.append(ratio(fused, ref))
                if 'ffht' in names:
                    row.append(ratio(fused, 'ffht'))
            if ctrl:
                row.append(ratio(ctrl, ref))
            if 'sT' in names and 'sG19' in names:
                row.append(ratio('sG19', 'sT'))
            if 'Tfp' in names:
                row.append(ratio('Tfp', ref))
            sp = [float(d[n]['spread_med_pct']) for n in names if n in d]
            row.append(f'{min(sp):.1f} to {max(sp):.1f} %')
            c = cond.get((t, k), {})
            row.append(f"{c.get('sibling_busy_pct', '?')} %")
            row.append(c.get('attempt', '?'))
            print('| ' + ' | '.join(row) + ' |')


if __name__ == '__main__':
    main()
