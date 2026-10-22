#!/usr/bin/env python3
"""summarize_small.py OUTDIR -- SUMMARY.md for the x86-hybrid-small job (22 Oct 2026).  Standard library only.

Reads every RESULT line in OUTDIR/batch_<binary>.txt (bench_small.c, batch mode: B vectors of n points per timed call).
Figures are ns per VECTOR (median of >= 9 repeats; best of repeats in brackets).  For each binary and n:
  circuit / best rival        = circuit median / median of the fastest rival in the same process (every program takes
                                turns in one process; below 1 = faster)
  circuit / plain twin        = against the same layout with the textbook kernel (hyb8-tb8, hyb16-tb16, sl8-tb8, sl16-tb16)
  circuit / balanced twin     = against the fastest pipe-balanced textbook in the same layout (tb8bal / tb8balS, ...)
Reading for the library sizes 2^6..2^9 (RESULT-X86.md, next run 4: "at 0.95 or above everywhere, the claim is limited to
1,024 points and up"), per binary, with the best circuit at each n:  GAIN-EVERYWHERE if every n is <= 0.90; NO-GAIN if
every n is >= 0.95; MIXED otherwise.  Picking the best of several circuits per n favours the circuits slightly (a
selection effect); the g20 rows are given separately.
"""
import glob
import os
import re
import sys

RX = re.compile(r'^RESULT x86-hybrid-small (\S+) 2\^(\d+) B=(\d+) (\S+)\s+best\s+([\d.]+)\s+median\s+([\d.]+) ns/vector'
                r' \| ([\d.]+) ns/point \| ([\d.]+) us/call \| calls/rep (\d+) K (\d+) B (\d+) \| finite (\S+)'
                r' nonfinite (\d+) subnormal (\d+)')
CIRC = re.compile(r'-(g\d|h20)')


def is_circuit(name):
    return bool(CIRC.search(name))


def layout(name):
    return name.split('-', 1)[0]  # hyb8, hyb16, sl8, sl16, sl4, x86wht, FFHT


PLAIN = {'hyb8': 'hyb8-tb8', 'hyb16': 'hyb16-tb16', 'sl8': 'sl8-tb8', 'sl16': 'sl16-tb16'}
BAL = {'hyb8': ['hyb8-tb8bal', 'hyb8-tb8balS'], 'hyb16': ['hyb16-tb16bal', 'hyb16-tb16balS'],
       'sl8': ['sl8-tb8bal', 'sl8-tb8balS'], 'sl16': ['sl16-tb16bal', 'sl16-tb16balS']}

out = sys.argv[1] if len(sys.argv) > 1 else 'out'
data = {}    # binary -> {L: {name: dict}}
width = {}
smoke = False
for f in sorted(glob.glob(os.path.join(out, 'batch_*.txt'))):
    b = os.path.basename(f)[len('batch_'):-4]
    for line in open(f, errors='replace'):
        r = RX.match(line)
        if not r:
            continue
        smoke |= 'SMOKE-TEST' in line
        xn, L, _, name, best, med, nspt, us, cpr, K, B, fin, nf, sub = r.groups()
        width[b] = xn
        data.setdefault(b, {}).setdefault(int(L), {})[name] = dict(
            best=float(best), med=float(med), nspt=float(nspt), us=float(us), K=int(K), B=int(B),
            finite=(fin == 'yes'), nf=int(nf), sub=int(sub))


def grab(path, pat):
    try:
        for line in open(path, errors='replace'):
            if re.search(pat, line):
                return line.strip()
    except OSError:
        pass
    return ''


def best_rival(d):
    riv = [(n, v) for n, v in d.items() if not is_circuit(n)]
    return min(riv, key=lambda x: x[1]['med']) if riv else (None, None)


def fmt(x):
    return f'{x:.3f}'


ORDER = ['gcc_avx2_f32', 'clang_avx2_f32', 'gcc_avx512_f32', 'clang_avx512_f32',
         'gcc_avx2_f64', 'clang_avx2_f64', 'gcc_avx512_f64', 'clang_avx512_f64']
bins = sorted(data, key=lambda b: (ORDER.index(b) if b in ORDER else 99, b))

print('# x86-hybrid-small summary: the circuits at library sizes (64-512 points), many vectors per call\n')
if smoke:
    print('**SMOKE TEST: these lines come from a functional test (SMALL_SMOKE=1), not a measurement. No number here '
          'means anything.**\n')
cpu = grab(os.path.join(out, 'machine.txt'), r'^Model name')
ua = grab(os.path.join(out, 'run.log'), r'^MICROARCHITECTURE')
l2 = grab(os.path.join(out, 'run.log'), r'^BATCH:')
print(f'- Machine: {cpu.split(":", 1)[-1].strip() or "?"}; {ua.split(":", 1)[-1].strip() or "?"}')
print(f'- {l2 or "Batch footprint: see run.log"}')
forced = grab(os.path.join(out, 'quiet.log'), r'BUSY but FORCE=1')
print(f'- Quiet gate: {"FORCED at least once (busy machine): treat the numbers as suspect" if forced else "every timing passed az_quiet (or see quiet.log)"}')
allres = [v for b in data for L in data[b] for v in data[b][L].values()]
if allres:
    nfin = sum(1 for v in allres if not v['finite'])
    us = [v['us'] for v in allres]
    print(f'- Finite data: {len(allres) - nfin} of {len(allres)} timed (program, size) results ended every repeat finite '
          f'and free of subnormals{"" if not nfin else " -- " + str(nfin) + " DID NOT: see the tables (finite NO)"}.')
    short = sum(1 for u in us if u < 20)
    print(f'- One timed call (B vectors) took {min(us):.1f}-{max(us):.1f} us (median ns/vector x B); {short} of {len(us)} '
          f'results are below 20 us per call. Calls are timed in segments of K = 18-32 calls, so one clock read covers '
          f'at least {18 * min(us):.0f} us.')
print('- Figures: ns per vector, median of >= 9 repeats (best of repeats in brackets); ratios are medians; below 1 = '
      'faster. All programs of one binary and one n ran in one process, taking turns.')
print('- Layouts: hyb8 / hyb16 = FFHT\'s structure (8- or 16-vector steps), called once per vector like FFHT; '
      'sl4 / sl8 / sl16 = straight-line: one in-register step does the whole transform, one call runs it over the batch; '
      'x86wht = x86-wht\'s whole transform once per vector. h20half outputs H x / 2^p (p = its 8-point steps).\n')

# ---- the reading per binary ----
LIB = [6, 7, 8, 9]
print('## Reading per binary (best circuit / best rival at each n; the circuit in brackets)\n')
print('| binary | width | ' + ' | '.join(f'n={1 << L}' for L in [6, 7, 8, 9, 10, 12]) + ' | library sizes 2^6-2^9 |')
print('|---|---|' + '---|' * 7)
for b in bins:
    cells, lib = [], []
    for L in [6, 7, 8, 9, 10, 12]:
        d = data[b].get(L)
        if not d:
            cells.append('-')
            continue
        bn, bv = best_rival(d)
        cs = [(n, v['med'] / bv['med']) for n, v in d.items() if is_circuit(n)]
        if not cs:
            cells.append(f'no circuit layout (rival {bn})')
            continue
        cn, q = min(cs, key=lambda x: x[1])
        cells.append(f'**{q:.3f}** ({cn})' if q <= 0.90 else f'{q:.3f} ({cn})')
        if L in LIB:
            lib.append(q)
    if lib:
        v = 'GAIN-EVERYWHERE (<= 0.90 at every n)' if max(lib) <= 0.90 else (
            'NO-GAIN (>= 0.95 at every n)' if min(lib) >= 0.95 else 'MIXED')
    else:
        v = 'no library-size data'
    print(f'| {b} | {width[b]} | ' + ' | '.join(cells) + f' | {v} |')
print()
print('g20 alone (the 3/4 family\'s 8-point step; hyb8-g20, and sl8-g20 where n is 8 vectors), circuit / best rival:\n')
for b in bins:
    xs = []
    for L in sorted(data[b]):
        d = data[b][L]
        bn, bv = best_rival(d)
        for c in ('sl8-g20', 'hyb8-g20', 'sl16-g20x2'):
            if c in d:
                xs.append(f'n={1 << L} {c} {d[c]["med"] / bv["med"]:.3f}')
    if xs:
        print(f'- {b}: ' + '; '.join(xs))
print()

# ---- per binary ----
for b in bins:
    rows = data[b]
    print(f'## {b} ({width[b]})\n')
    print('| n | B | best rival (ns/vector) | circuit | ns/vector | / best rival | / plain twin | / balanced twin | finite |')
    print('|---|---|---|---|---|---|---|---|---|')
    for L in sorted(rows):
        d = rows[L]
        bn, bv = best_rival(d)
        bbest = min(v['best'] for n, v in d.items() if not is_circuit(n))
        noisy = any((v['med'] - v['best']) / v['best'] > 0.05 for v in d.values())
        Bv = next(iter(d.values()))['B']
        cs = [n for n in d if is_circuit(n)]
        head = f'| {1 << L}{" (noisy)" if noisy else ""} | {Bv} | {bn} {bv["med"]:.2f} ({bv["us"]:.0f} us/call) |'
        if not cs:
            print(head + ' (no circuit layout at this n) | | | | | ' + ('yes' if all(v['finite'] for v in d.values()) else 'NO') + ' |')
            continue
        for c in cs:
            v = d[c]
            lay = layout(c)
            pt = PLAIN.get(lay)
            bal = [d[t] for t in BAL.get(lay, []) if t in d]
            q = v['med'] / bv['med']
            qp = f'{v["med"] / d[pt]["med"]:.3f}' if pt in d else '-'
            qb = f'{v["med"] / min(x["med"] for x in bal):.3f}' if bal else '-'
            s = f'{q:.3f} ({v["best"] / bbest:.3f})'
            print(f'{head} {c} | {v["med"]:.2f} ({v["best"]:.2f}) | {"**" + s + "**" if q <= 0.90 else s} | {qp} | {qb} | '
                  f'{"yes" if v["finite"] else "NO"} |')
            head = '| | | |'
    print()
    print('Every program at each n (ns/vector, median):\n')
    for L in sorted(rows):
        d = rows[L]
        print(f'- n={1 << L}: ' + ', '.join(f'{n} {v["med"]:.2f}' for n, v in sorted(d.items(), key=lambda kv: kv[1]['med'])))
    print()

# ---- across binaries (separate processes) ----
print('## Fastest code on this machine per precision and n (across binaries: SEPARATE processes, minutes apart)\n')
print('| precision | n | fastest rival (binary, program, ns/vector) | fastest circuit (binary, program, ns/vector) | circuit / rival |')
print('|---|---|---|---|---|')
for prec in ('f32', 'f64'):
    Ls = sorted({L for b in bins if b.endswith(prec) for L in data[b]})
    for L in Ls:
        riv, cir = [], []
        for b in bins:
            if not b.endswith(prec) or L not in data[b]:
                continue
            for n, v in data[b][L].items():
                (cir if is_circuit(n) else riv).append((v['med'], b, n))
        if not riv:
            continue
        r = min(riv)
        if cir:
            c = min(cir)
            print(f'| {prec} | {1 << L} | {r[1]} {r[2]} {r[0]:.2f} | {c[1]} {c[2]} {c[0]:.2f} | {c[0] / r[0]:.3f} |')
        else:
            print(f'| {prec} | {1 << L} | {r[1]} {r[2]} {r[0]:.2f} | none | - |')
print()
skipped = [ln.strip() for ln in open(os.path.join(out, 'run.log'), errors='replace') if 'SKIPPED' in ln] \
    if os.path.exists(os.path.join(out, 'run.log')) else []
if skipped:
    print('## Runs skipped by the time budget\n')
    for s in skipped:
        print(f'- {s}')
