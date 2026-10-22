#!/usr/bin/env python3
"""tables.py -- re-derive every figure of measurements/2026-10-22/README.md from the raw files.

    python3 -B measurements/2026-10-22/tables.py

Reads only the files under this folder (x86/runs, gpu/runs, gpu/kpart/runs, fpga-xc7/results), plain or .gz.
Python 3 standard library only.  Writes nothing.

Definitions (the same as the README's):
  ratio          = a program's median time / the median time of the fastest rival.  Below 1: the circuit is faster.
  exact-output   = the circuits whose output is H x itself (g19, g20, g52 and, in the 512-bit runs, their "late"
                   forms).  h20half, whose output is H x divided by a power of two, is left out of every figure.
  across builds  = the fastest exact-output circuit over the gcc and the clang build / the fastest rival over the
                   same two builds, at the sizes both builds ran.  The two builds ran one after the other in
                   separate processes, minutes apart, on the same machine.
  per build      = the same inside one binary: every program takes turns in one process.
Each figure is printed with the README sentence or table row that quotes it, and the program checks that the
README holds exactly that text.  The last line is printed only if every figure is found there.
"""
import gzip
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
X86 = os.path.join(HERE, 'x86', 'runs')


def rd(path):
    if os.path.exists(path):
        with open(path, errors='replace') as f:
            return f.read()
    with gzip.open(path + '.gz', 'rt', errors='replace') as f:
        return f.read()


def rng(vals, nd=3):
    vals = list(vals)
    lo, hi = min(vals), max(vals)
    return ('%.*f' % (nd, lo)) if '%.*f' % (nd, lo) == '%.*f' % (nd, hi) else '%.*f-%.*f' % (nd, lo, nd, hi)


# ------------------------------------------------------------------------------------------- x86 whole transforms
RX_WHOLE = re.compile(r'^RESULT x86-hybrid(?:512)? whole (\S+) 2\^(\d+) (same|separate)\s+(\S+)\s+best\s+([\d.]+)'
                      r'\s+median\s+([\d.]+)\s+ns/point', re.M)


def whole(run, f):
    d = {}
    for m in RX_WHOLE.finditer(rd(os.path.join(X86, run, f))):
        d.setdefault(int(m.group(2)), {})[m.group(4)] = float(m.group(6))
    return d


H_CIRC = ['hyb8-g19', 'hyb8-g20', 'hyb16-g52']
H_RIVAL = ['FFHT', 'x86wht-tb', 'x86wht-tbbal', 'hyb8-tb8', 'hyb8-tb8bal', 'hyb16-tb16', 'hyb8-tb8balS']
H_TEXTBOOK_FFHT_STRUCTURE = ['hyb8-tb8', 'hyb8-tb8bal', 'hyb8-tb8balS', 'hyb16-tb16']
W_CIRC = ['h8-g19', 'h8-g20', 'h8-g20late', 'h16-g52', 'h16-g52late']
W_RIVAL = ['FFHT', 'x86wht-tb', 'x86wht-tbbal', 'x86wht-tbbalS', 'h8-tb', 'h8-tbbal', 'h8-tbbalS', 'h8-tbmix',
           'h16-tbmix']


def across(run, files, circ, rival, sizes=None):
    ds = [whole(run, f) for f in files]
    common = sorted(set.intersection(*[set(d) for d in ds]))
    out = {}
    for L in common:
        if sizes and L not in sizes:
            continue
        c = min(d[L][x] for d in ds for x in circ if x in d[L])
        r = min(d[L][x] for d in ds for x in rival if x in d[L])
        out[L] = c / r
    return out


def per_build(run, f, circ, rival, sizes=None):
    d = whole(run, f)
    out = {}
    for L in sorted(d):
        if sizes and L not in sizes:
            continue
        cc = [d[L][x] for x in circ if x in d[L]]
        rr = [d[L][x] for x in rival if x in d[L]]
        if cc and rr:
            out[L] = min(cc) / min(rr)
    return out


S10_16 = range(10, 17)
S10_20 = range(10, 21)
F64 = ['whole_same_gcc_avx2_f64.txt', 'whole_same_clang_avx2_f64.txt']
F32 = ['whole_same_gcc_avx2_f32.txt', 'whole_same_clang_avx2_f32.txt']

FIGS = []      # (key, value, README text that must contain it)


def fig(key, value, text):
    FIGS.append((key, value, text % {'v': value} if '%(v)s' in text else text))


def table_row(cells):
    return '| ' + ' | '.join(cells) + ' |'


def chips():
    for chip, run in (('Zen 5', 'zen5-hybrid'), ('Zen 4', 'zen4-hybrid')):
        k = chip.replace(' ', '').lower()
        a64 = across(run, F64, H_CIRC, H_RIVAL, S10_16)
        g64 = per_build(run, F64[0], H_CIRC, H_RIVAL, S10_16)
        c64 = per_build(run, F64[1], H_CIRC, H_RIVAL, S10_16)
        fig(k + '.f64.across', rng(a64.values()), '%(v)s')
        fig(k + '.f64.gcc', rng(g64.values()), 'gcc %(v)s')
        fig(k + '.f64.clang', rng(c64.values()), 'clang %(v)s')
        g20g = per_build(run, F64[0], ['hyb8-g20'], H_RIVAL, S10_16)
        g20c = per_build(run, F64[1], ['hyb8-g20'], H_RIVAL, S10_16)
        fig(k + '.f64.g20.gcc', rng(g20g.values()), 'g20 alone: gcc %(v)s')
        fig(k + '.f64.g20.clang', rng(g20c.values()), 'clang %(v)s')
        a32 = across(run, F32, H_CIRC, H_RIVAL, S10_20)
        fig(k + '.f32.across', rng(a32.values()), '%(v)s')
        sep = per_build(run, 'whole_sep_gcc_avx2_f32.txt', H_CIRC, H_RIVAL)
        fig(k + '.f32.separate.gcc', rng(sep.values()), '%(v)s')
        # the per-size table of the README (double precision)
        for L in sorted(a64):
            fig('%s.f64.2^%d' % (k, L), '%.3f' % a64[L],
                table_row([chip, '2^%d' % L, '%.3f' % g64[L], '%.3f' % c64[L], '%.3f' % a64[L]]))
    # 19 operations against 20: is the step with fewer operations the faster one?
    slower, cases = 0, 0
    for run in ('zen5-hybrid', 'zen4-hybrid'):
        for f in F64:
            d = whole(run, f)
            for L in S10_16:
                if L in d:
                    cases += 1
                    slower += d[L]['hyb8-g19'] > d[L]['hyb8-g20']
    fig('g19-slower-than-g20', '%d of %d' % (slower, cases), '%(v)s')
    for chip, run in (('Zen 2', 'zen2-hybrid'), ('Intel', 'intel-hybrid')):
        k = chip.replace(' ', '').lower()
        for f, lab in (('whole_same_gcc_avx2_f64.txt', 'f64.gcc'), ('whole_same_gcc_avx2_f32.txt', 'f32.gcc'),
                       ('whole_same_clang_avx2_f32.txt', 'f32.clang')):
            v = per_build(run, f, ['hyb8-g20'], H_RIVAL, S10_16)
            fig('%s.g20.%s' % (k, lab), rng(v.values()), '%(v)s')


def overflow_share():
    """same array: one buffer transformed again and again inside each repeat (it is reset to the input before every
    repeat).  H H = n I, so the numbers grow by n = 2^L every two calls and overflow after about 2 E / L calls
    (E = 1024 in double, 128 in single).  Share of the timed calls made after that point, over every same-array
    RESULT line of the runs quoted in sections 3 and 4 of the README."""
    rx = re.compile(r'^RESULT x86-hybrid whole (\S+) 2\^(\d+) same\s+(\S+)\s+best .*\(calls/rep (\d+)\)', re.M)
    shares = []
    for run in ('zen5-hybrid', 'zen4-hybrid', 'zen2-hybrid', 'intel-hybrid', 'zen5-hybrid-retracted-1',
                'zen5-hybrid-retracted-2', 'zen5-hybrid-retracted-3'):
        for f in sorted(os.listdir(os.path.join(X86, run))):
            if f.startswith('whole_same'):
                for m in rx.finditer(rd(os.path.join(X86, run, f.replace('.gz', '')))):
                    e = 1024 if 'f64' in m.group(1) else 128
                    shares.append((int(m.group(2)), 1 - 2.0 * e / int(m.group(2)) / int(m.group(4))))
    main = [v for L, v in shares if L <= 16]
    fig('same-array.overflowed-share.2^10-2^16', '%.1f %%' % (100 * min(main) - 0.05), 'at least %(v)s')
    fig('same-array.overflowed-share.max', 'more than 99.9 %' if max(v for _, v in shares) > 0.999 else 'less', '%(v)s')
    fig('same-array.overflowed-share.all-sizes', '%.0f %%' % (100 * min(v for _, v in shares) - 0.5), '%(v)s')


def retraction():
    v = []
    for i in (1, 2, 3):
        v += list(per_build('zen5-hybrid-retracted-%d' % i, F64[0], ['hyb8-g20'], H_RIVAL, S10_16).values())
    fig('retracted.g20.f64.gcc', rng(v), '%(v)s')
    # register copies per 8-point step (hstep_ = every step after the first of a block), from the run's own asm count
    txt = rd(os.path.join(X86, 'zen5-hybrid', 'asm_counts.txt'))
    cur, copies = None, {}
    for line in txt.splitlines():
        if line.startswith('=='):
            cur = line.split()[1].replace('.asm', '')
            continue
        m = re.match(r'^\s+hstep_(tb8_bal|tb8_balS|g20_nat)\s+.*regmov\s+(\d+)', line)
        if m and cur in ('gcc_avx2_f64', 'clang_avx2_f64'):
            copies[(cur.split('_')[0], m.group(1))] = int(m.group(2))
    for c in ('clang', 'gcc'):
        row = [copies[(c, n)] for n in ('tb8_bal', 'tb8_balS', 'g20_nat')]
        fig('retracted.register-copies.' + c, ' '.join(map(str, row)),
            table_row([c + ' 18.1.3' if c == 'clang' else c + ' 13.3.0'] + [str(x) for x in row]))
    il = rd(os.path.join(HERE, 'x86', 'retraction', 'innerloop_clang21.txt'))
    block = il.split('== clang_avx2_f64')[1].split('==')[0]
    n = {m.group(1): int(m.group(2)) for m in re.finditer(r'hstep_(\w+)\s+inner loop\s+(\d+) instructions', block)}
    fig('retracted.inner-loop', 'tb8bal %d, tb8balS %d, g20 %d instructions' % (n['tb8_bal'], n['tb8_balS'], n['g20_nat']),
        '%(v)s')


def copies_cost():
    for chip, run in (('Zen 5', 'zen5-hybrid'), ('Zen 4', 'zen4-hybrid')):
        k = chip.replace(' ', '').lower()
        v = []
        for f in F64:
            d = whole(run, f)
            v += [d[L]['hyb8-tb8balS'] / d[L]['hyb8-tb8bal'] for L in S10_16 if L in d]
        fig(k + '.tb8balS-vs-tb8bal', rng(v, 2), '%(v)s')


def wide512():
    for k, run in (('zen5', 'zen5-hybrid512'), ('zen4', 'zen4-hybrid512'), ('zen4r', 'zen4-hybrid512-repeat')):
        for p in ('f32', 'f64'):
            fs = ['whole_same_gcc_avx512_%s.txt' % p, 'whole_same_clang_avx512_%s.txt' % p]
            a = across(run, fs, W_CIRC, W_RIVAL)
            fig('%s.512.%s.across' % (k, p), rng(a.values()), '%(v)s')
            fig('%s.512.%s.sizes' % (k, p), '2^%d-2^%d' % (min(a), max(a)), '%(v)s')
            g = per_build(run, fs[0], W_CIRC, W_RIVAL)
            odd = [g[L] for L in g if L % 2]
            fig('%s.512.%s.gcc-odd-min' % (k, p), '%.3f' % min(odd), '%(v)s')


def small():
    rx = re.compile(r'^RESULT x86-hybrid-small (\S+) 2\^(\d+) B=(\d+) (\S+)\s+best\s+([\d.]+)\s+median\s+([\d.]+)'
                    r' ns/vector.*finite (\S+) nonfinite (\d+)', re.M)
    rx_call = re.compile(r'^RESULT x86-hybrid-small .* ns/point \| ([\d.]+) us/call', re.M)
    circ = re.compile(r'-g\d')
    for k, run in (('zen4', 'zen4-small'), ('zen5', 'zen5-small')):
        data, n, fin, short = {}, 0, 0, 0
        d = os.path.join(X86, run)
        for f in sorted(os.listdir(d)):
            if not f.startswith('batch_'):
                continue
            b = f[len('batch_'):].split('.txt')[0]
            text = rd(os.path.join(d, f.replace('.gz', '')))
            for m in rx.finditer(text):
                n += 1
                fin += m.group(7) == 'yes' and m.group(8) == '0'
                data.setdefault(b, {}).setdefault(int(m.group(2)), {})[m.group(4)] = float(m.group(6))
            short += sum(float(m.group(1)) < 20 for m in rx_call.finditer(text))
        fig(k + '.small.finite', '%d of %d' % (fin, n), '%(v)s')
        lib, lib_wo = [], []
        for p, word in (('f32', 'single'), ('f64', 'double')):
            bs = [b for b in data if b.endswith(p)]
            for L in sorted(data[bs[0]]):
                c = min(data[b][L][x] for b in bs for x in data[b][L] if circ.search(x) and 'h20' not in x)
                r = min(data[b][L][x] for b in bs for x in data[b][L] if not circ.search(x) and 'h20' not in x)
                if L <= 9:
                    lib.append(c / r)
                    # 64 points in single precision: the fastest rival is a 512-bit layout with no circuit version
                    if not (p == 'f32' and L == 6):
                        lib_wo.append(c / r)
                else:
                    fig('%s.small.%s.%d' % (k, p, 2 ** L), '%.3f' % (c / r), '%(v)s')
        fig(k + '.small.64-512', rng(lib), '%(v)s')
        fig(k + '.small.64-512.without-64-single', rng(lib_wo), 'without it %(v)s')
        if k == 'zen5':
            fig(k + '.small.calls-under-20us', '%d of the %d timings' % (short, n), '%(v)s')


def repeat512():
    """Zen 4, 512-bit: the first run and its repeat on the same machine, across builds, size by size."""
    both = {}
    for run in ('zen4-hybrid512', 'zen4-hybrid512-repeat'):
        for p in ('f32', 'f64'):
            fs = ['whole_same_gcc_avx512_%s.txt' % p, 'whole_same_clang_avx512_%s.txt' % p]
            for L, v in across(run, fs, W_CIRC, W_RIVAL).items():
                both.setdefault((p, L), []).append(v)
    fig('zen4.512.both.f32.2^12-2^20', rng(v for (p, L), vs in both.items() if p == 'f32' and L >= 12 for v in vs),
        '%(v)s in single precision')
    fig('zen4.512.both.f64.2^10-2^20', rng(v for (p, L), vs in both.items() if p == 'f64' and L >= 10 for v in vs),
        '%(v)s in double')
    fig('zen4.512.both.f32.2^10', rng(both[('f32', 10)]), '%(v)s')
    fig('zen4.512.both.f32.2^18', rng(both[('f32', 18)]), '%(v)s in both runs')
    diff = max(abs(a - b) / a for a, b in both.values())
    fig('zen4.512.both.max-difference', '%.1f %%' % (100 * diff + 0.05), 'within %(v)s')


def byproducts():
    for chip, run in (('Zen 5', 'zen5-hybrid'), ('Zen 4', 'zen4-hybrid')):
        k = chip.replace(' ', '').lower()
        a = across(run, F64, H_TEXTBOOK_FFHT_STRUCTURE, ['FFHT'], S10_16)
        fig(k + '.textbook-vs-FFHT.across', rng(a.values()), '%(v)s')
        for c, f in (('gcc', F64[0]), ('clang', F64[1])):
            v = per_build(run, f, H_TEXTBOOK_FFHT_STRUCTURE, ['FFHT'], S10_16)
            fig('%s.textbook-vs-FFHT.%s' % (k, c), rng(v.values()), '%(v)s')
    for k, run in (('zen5', 'zen5-hybrid512'), ('zen4', 'zen4-hybrid512'), ('zen4r', 'zen4-hybrid512-repeat')):
        for p in ('f64', 'f32'):
            fs = ['whole_same_gcc_avx512_%s.txt' % p, 'whole_same_clang_avx512_%s.txt' % p]
            a = across(run, fs, [r for r in W_RIVAL if r != 'FFHT'], ['FFHT'], S10_20)
            fig('%s.512-textbook-vs-FFHT.%s' % (k, p), rng(a.values(), 2), '%(v)s')
    # the twin run: FFHT against the fastest 512-bit rival in the same 512-bit binary, and 512-bit against 256-bit
    d512 = whole('zen5-hybrid', 'whole_same_gcc_avx512_f64.txt')
    ffht = [d512[L]['FFHT'] / min(d512[L][r] for r in H_RIVAL if r != 'FFHT') for L in sorted(d512) if L <= 16]
    fig('zen5.FFHT-vs-512-textbook.twin', rng(ffht, 2), '%(v)s')
    d256 = [whole('zen5-hybrid', f) for f in F64]
    sp = [min(d[L][x] for d in d256 for x in H_RIVAL + H_CIRC) / min(d512[L][x] for x in H_RIVAL if x != 'FFHT')
          for L in sorted(d512) if L <= 16]
    fig('zen5.512-textbook-vs-best-256', rng(sp, 2), '%(v)s')


def kernel_level():
    def ratio(path, key):
        for line in rd(os.path.join(X86, path)).splitlines():
            if line.startswith('RATIO') and (' %s ' % key) in line:
                return float(re.search(r'\| vs best textbook best [\d.]+ median ([\d.]+)', line).group(1))
        raise SystemExit('no %s in %s' % (key, path))
    fig('zen2.pass.g52', '%.3f / %.3f' % (ratio('zen2-wht/pass16_I1_gcc_avx2_f32.txt', 'g52/tb16'),
                                          ratio('zen2-wht/pass16_I1_gcc_avx2_f64.txt', 'g52/tb16')), '%(v)s')
    fig('zen2.pass.g20', '%.3f / %.3f' % (ratio('zen2-wht/pass8_I1_gcc_avx2_f32.txt', 'g20/tb8'),
                                          ratio('zen2-wht/pass8_I1_gcc_avx2_f64.txt', 'g20/tb8')), '%(v)s')
    g52 = [ratio('zen2-wht/pass16_I1_gcc_avx2_f32.txt', 'g52/tb16'), ratio('zen2-wht/pass16_I1_gcc_avx2_f64.txt', 'g52/tb16')]
    g20 = [ratio('zen2-wht/pass8_I1_gcc_avx2_f32.txt', 'g20/tb8'), ratio('zen2-wht/pass8_I1_gcc_avx2_f64.txt', 'g20/tb8')]
    fig('zen2.pass.g52.range', rng(g52), '%(v)s')
    fig('zen2.pass.g20.range', rng(g20), '%(v)s')
    fig('zen5.regs.g20', '%.2f' % ratio('zen5-wht/regs8_I1_gcc_avx2_f64.txt', 'g20/tb8'), '%(v)s')
    rx = re.compile(r'^RESULT (\S+)\s+best ([\d.]+) median ([\d.]+) ns/point', re.M)
    both = []
    for chip, run in (('Zen 5', 'zen5-balance'), ('Zen 4', 'zen4-balance')):
        k = chip.replace(' ', '').lower()
        got = {'G22_depth4': [], 'G52_family': [], 'G19': []}
        for r in (1, 2):
            d = {m.group(1): float(m.group(3)) for m in rx.finditer(rd(os.path.join(X86, run, 'res_avx512_r%d.txt' % r)))}
            for c, h, tb in (('G22_depth4', 'h8', 24), ('G19', 'h8', 24), ('G52_family', 'h16', 64)):
                t = min(d['k_%s_textbook_%d' % (h, tb)], d['k_%s_textbook_%d_bal' % (h, tb)])
                got[c].append(d['k_%s_%s' % (h, c)] / t)
        fig(k + '.balance512.g22d4', rng(got['G22_depth4']), '%(v)s')
        fig(k + '.balance512.g52', rng(got['G52_family']), '%(v)s')
        both.extend(got['G52_family'])
    fig('balance512.g52.both-chips', rng(both), '%(v)s')


def rounding():
    rx = re.compile(r'^CHECK (\S+) whole 2\^(\d+)\s+(\S+)\s+real inputs: rel err ([\d.e+-]+)', re.M)
    for p in ('f64', 'f32'):
        v = {}
        for run in ('zen5-hybrid', 'zen4-hybrid'):
            for f in sorted(os.listdir(os.path.join(X86, run))):
                if f.startswith('check_') and p in f:
                    for m in rx.finditer(rd(os.path.join(X86, run, f.replace('.gz', '')))):
                        v.setdefault(m.group(3), []).append(float(m.group(4)))
        circ = [x for n in H_CIRC for x in v[n]]
        tb = [x for n in H_RIVAL for x in v[n]]
        if p == 'f64':
            fig('rounding.f64.textbook-max', '%.1e' % max(tb), '%(v)s')
            fig('rounding.f64.circuits', '%.1e to %.1e' % (min(circ), max(circ)), '%(v)s')
            fig('rounding.f64.g20', '%.1e to %.1e' % (min(v['hyb8-g20']), max(v['hyb8-g20'])), '%(v)s')
        else:
            fig('rounding.f32.circuits', '%.1e to %.1e' % (min(circ), max(circ)), '%(v)s')
            fig('rounding.f32.textbook', '%.1e to %.1e' % (min(tb), max(tb)), '%(v)s')


def gpu():
    g = os.path.join(HERE, 'gpu', 'runs', 'rtx6000-wht')
    txt = rd(os.path.join(g, 'wht_cuda_all.txt'))
    rows = re.findall(r'^RESULT row N=(\d+) radix=(\d+) rows=(\d+) (\S+)\s+best ([\d.]+) median ([\d.]+) ns/point '
                      r'ratio-vs-\S+ ([\d.]+)', txt, re.M)
    big = [float(r[6]) for r in rows if int(r[0]) * int(r[2]) * 4 == 256 << 20 and not r[3].startswith('tb')]
    fig('gpu.rows.256MiB', rng(big, 4), '%(v)s')
    small = [r for r in rows if r[0] == '4096' and r[2] == '256' and r[3] == 'g52'][0]
    fig('gpu.rows.4MiB.g52', '%.2f' % float(small[6]), '%(v)s')
    fig('gpu.rows.4MiB.call', '%.1f' % (float(small[5]) * 4096 * 256 / 1000), '%(v)s')
    tb = [r for r in rows if r[0] == '4096' and r[2] == '256' and r[3] == 'tb16'][0]
    fig('gpu.rows.4MiB.tb16.call', '%.1f' % (float(tb[5]) * 4096 * 256 / 1000), '%(v)s')
    other = [float(r[5]) * 256 * 4096 / 1000 for r in rows if r[0] == '256' and r[2] == '4096']
    fig('gpu.rows.4MiB.other-setting.call', rng(other, 1), '%(v)s')
    d = rd(os.path.join(g, 'bench_dao.txt'))
    pat = re.findall(r'^RESULT (\S+) n=(\d+) rows=\d+ (\S+)\s+best .*ratio-vs-dao ([\d.]+)', d, re.M)
    dg = [float(x[3]) for x in pat if x[2] == 'dao+g19g52']
    fig('gpu.dao-patched', rng(dg), '%(v)s')
    fig('gpu.dao-patched.settings', str(len(dg)), '%(v)s')
    hc = [(int(x[1]), float(x[3])) for x in pat if x[2] == 'hadacore']
    fig('gpu.hadacore', rng([r for n, r in hc if n != 512]), '%(v)s')
    fig('gpu.hadacore.512', rng([r for n, r in hc if n == 512]), '%(v)s')
    k = os.path.join(HERE, 'gpu', 'kpart', 'runs')
    o = json.loads(rd(os.path.join(k, 'dao-cse', 'res_orig.json')))
    c = json.loads(rd(os.path.join(k, 'dao-cse', 'res_cse.json')))
    oi = {(r['case'], r['d'], r['dtype'], r['B']): r['us'] for r in o['rows']}
    ci = {(r['case'], r['d'], r['dtype'], r['B']): r['us'] for r in c['rows']}
    for d_, lab in ((28672, '28x1024'), (14336, '28x512')):
        v = [ci[('28N', d_, t, 4096)] / oi[('28N', d_, t, 4096)] for t in ('torch.float16', 'torch.bfloat16')]
        fig('kpart.cse.' + lab, rng(v), '%(v)s')
    o3 = json.loads(rd(os.path.join(k, 'three-forms', 'res_orig.json')))
    g3 = json.loads(rd(os.path.join(k, 'three-forms', 'res_grp.json')))
    oi3 = {(r['case'], r['d'], r['dtype'], r['B']): r['us'] for r in o3['rows']}
    gi3 = {(r['case'], r['d'], r['dtype'], r['B']): r['us'] for r in g3['rows']}
    for d_, lab in ((28672, '28x1024'), (14336, '28x512')):
        v = [gi3[('28N', d_, t, 4096)] / oi3[('28N', d_, t, 4096)] for t in ('torch.float16', 'torch.bfloat16')]
        fig('kpart.groups-of-four.' + lab, rng(v), '%(v)s')
    for v in ('orig', 'cse'):  # the compiler's report: 28-point kernels that keep values on the stack (spills)
        n = st = 0
        on = False
        for line in rd(os.path.join(k, 'dao-cse', 'ptxas_%s.txt' % v)).splitlines():
            if 'Compiling entry function' in line:
                on = '28N' in line
            elif on and 'Used' in line:
                n += 1
                st += 'stack size' in line
        fig('kpart.28N-stack.' + v, '%d of %d' % (st, n), '%(v)s')
    counts = rd(os.path.join(k, 'three-forms', 'grp_counts.txt'))
    fig('kpart.groups-of-four.adds28', re.search(r'had_28_will: grouped\(4\) (\d+) additions', counts).group(1), '%(v)s')


def xilinx():
    rows = [json.loads(line) for line in rd(os.path.join(HERE, 'fpga-xc7', 'results', 'xc7', 'farm.jsonl')).splitlines()
            if line.strip()]
    s = {r['tag']: r['stats'] for r in rows if r.get('summary') and 'stats' in r}

    def med(tag, field):
        return s[tag][field]['med']

    def pct(a, b):
        return '%+.1f %%' % (100.0 * (a / b - 1))
    fig('xc7.carry4.8', '%d against %d (%s)' % (med('ax7_o19_d2', 'dut_carry4'), med('ax7_tb8_d2', 'dut_carry4'),
                                               pct(med('ax7_o19_d2', 'dut_carry4'), med('ax7_tb8_d2', 'dut_carry4'))), '%(v)s')
    fig('xc7.carry4.16', '%d against %d (%s)' % (med('ax7_o52_d2', 'dut_carry4'), med('ax7_tb16_d2', 'dut_carry4'),
                                                pct(med('ax7_o52_d2', 'dut_carry4'), med('ax7_tb16_d2', 'dut_carry4'))), '%(v)s')
    for a, b in (('ax7_o19_d3', 'ax7_tb8_d3'), ('ax7_o19_d2', 'ax7_tb8_d2'), ('ax7_o52_d2', 'ax7_tb16_d2'),
                 ('ax7_o52_d4', 'ax7_tb16_d4'), ('ax7_o19_d2', 'ax7_ar8_d2')):
        x, y = med(a, 'dut_slices_touched'), med(b, 'dut_slices_touched')
        fig('xc7.slices.%s-vs-%s' % (a[4:], b[4:]), '%d against %d (%s)' % (x, y, pct(x, y)), '%(v)s')
    x, y = med('ax7_o19_d3', 'dut_lut'), med('ax7_tb8_d3', 'dut_lut')
    fig('xc7.lut-cells.o19_d3-vs-tb8_d3', '%d against %d (%s)' % (x, y, pct(x, y)), '%(v)s')
    # the size of the device is not in the raw files: XC7A100T has 15,850 slices (Xilinx, 7 Series FPGAs Data Sheet:
    # Overview, DS180, table 3)
    slices_xc7a100t = 15850
    most = max(r['dut_slices_touched'] for r in rows if not r.get('summary') and r.get('tag', '').startswith('ax7_'))
    fig('xc7.most-slices', '%d of the chip\'s %s slices (%.1f %%)' % (most, '{:,}'.format(slices_xc7a100t),
                                                                     100.0 * most / slices_xc7a100t), '%(v)s')
    fig('xc7.ternary.carry4', '%d against %d' % (med('aj5_tern8_hand_p', 'dut_carry4'), med('ax7_o19_d2', 'dut_carry4')),
        '%(v)s')


def main():
    for f in (chips, overflow_share, retraction, copies_cost, wide512, repeat512, small, byproducts, kernel_level, rounding, gpu, xilinx):
        f()
    readme = rd(os.path.join(HERE, 'README.md')) if os.path.exists(os.path.join(HERE, 'README.md')) else ''
    missing = 0
    for key, value, text in FIGS:
        ok = text in readme
        missing += not ok
        print('%-40s %-48s %s' % (key, value, 'in README' if ok else 'NOT IN README: ' + text))
    print('%d figures re-derived; %d of them not found in README.md as printed' % (len(FIGS), missing))
    if missing:
        print('FAIL: README.md and the raw files disagree (or README.md quotes a figure differently)')
        return 1
    print('OK: every figure of measurements/2026-10-22/README.md re-derived from the raw files.  Measurements, not proofs.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
