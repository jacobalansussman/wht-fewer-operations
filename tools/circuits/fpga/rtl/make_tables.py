#!/usr/bin/env python3
"""make_tables.py -- the tables of the designs on paper (TABLES.md), written from designs.json so that no number is typed by hand.
USE (from fpga/rtl):  python3 -B make_tables.py  ->  TABLES.md"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = {'textbook': 'textbook', 'cfl1994': '1994 design', 'cfl1994b': '1994 design, other order',
         'ar2023': 'Alman and Rao step', 'ar2023l': 'Alman and Rao step, left to right', 'ours': 'this work'}


def pct(a, b):
    return '%+.1f %%' % (100.0 * (a - b) / b)


def main():
    with open(os.path.join(HERE, 'designs.json')) as f:
        rows = json.load(f)['designs']
    o = []
    for size, title in (('8', '8 points'), ('16', '16 points'), ('64', '64 points'),
                        ('8x8', '8 x 8 block (16 transforms of 8 points; the same function as 64 points)')):
        o.append('### ' + title)
        o.append('')
        o.append('| design | W | adders | depth | adder bits | vs textbook | chain bits | p: register bits (after adders + delay = total) | p: latency | p2: register bits | p2: latency | r: register bits |')
        o.append('|---|---|---|---|---|---|---|---|---|---|---|---|')
        for W in (8, 12, 16):
            tb = [r for r in rows if r['size'] == size and r['W'] == W and r['design'] == 'textbook'][0]
            for r in rows:
                if r['size'] != size or r['W'] != W:
                    continue
                o.append('| %s (`%s`) | %d | %d | %d | %d | %s | %d | %d + %d = %d | %d | %d | %d | %d |'
                         % (NAMES[r['design']], r['design'], W, r['adders'], r['depth'], r['adder_bits'],
                            '' if r is tb else pct(r['adder_bits'], tb['adder_bits']), r['chain_bits'],
                            r['reg_after_adders'], r['reg_delay'], r['reg_data'], r['latency'],
                            r['p2_reg_data'], r['p2_latency'], r['r_reg_data']))
        o.append('')
    o.append('### Widths of the adders, W = 8 (how many adders have each output width)')
    o.append('')
    o.append('| size | design | adders by output width |')
    o.append('|---|---|---|')
    for r in rows:
        if r['W'] == 8:
            o.append('| %s | %s | %s |' % (r['size'], NAMES[r['design']],
                     ', '.join('%s of %s bits' % (v, k) for k, v in sorted(r['width_histogram'].items(), key=lambda kv: int(kv[0])))))
    o.append('')
    txt = '\n'.join(o) + '\n'
    with open(os.path.join(HERE, 'TABLES.md'), 'w') as f:
        f.write(txt)
    print(txt)


if __name__ == '__main__':
    main()
