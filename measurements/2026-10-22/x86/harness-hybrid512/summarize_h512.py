#!/usr/bin/env python3
"""summarize_h512.py OUTDIR -- SUMMARY.md for the x86-hybrid512 job (22 Oct 2026).  Standard library only.

Reads every RESULT line in OUTDIR/whole_<same|sep>_<binary>.txt and the tune choices in OUTDIR/tune_<binary>.txt.
For each binary, mode and n:
  ratio = program median / median of the BEST RIVAL (the fastest by median of FFHT, x86wht-tb, x86wht-tbbal,
          x86wht-tbbalS, h8-tb, h8-tbbal, h8-tbbalS, h8-tbmix, h16-tbmix), all in the same process; below 1 = faster.
          Best-of-repeats in brackets.  The *balS rivals are the twin review's copy-free balanced textbook (22 Oct 2026).
Track 2 decision rule (PLAN.md, Track 2, as x86-hybrid reads it): per (binary, circuit) on 2^10..2^16, same array:
  CONTINUE if its WORST ratio there is <= 0.90; CLOSE-LEVEL if its BEST ratio there is >= 0.95; otherwise BETWEEN.
Also: library sizes (2^8-2^9), large sizes (2^17-2^20), the best circuit across compilers against the best rival across
compilers (separate processes: flagged), each circuit against its textbook twin, and the structure effect.
"""
import glob
import os
import re
import sys

RX = re.compile(r'^RESULT x86-hybrid512 whole (\S+) 2\^(\d+) (same|separate)\s+(\S+)\s+best\s+([\d.]+)\s+median\s+([\d.]+)')
RIVALS = ['FFHT', 'x86wht-tb', 'x86wht-tbbal', 'x86wht-tbbalS', 'h8-tb', 'h8-tbbal', 'h8-tbbalS', 'h8-tbmix', 'h16-tbmix']
CIRCUITS = ['h8-g19', 'h8-g20', 'h8-h20half', 'h8-g20late', 'h16-g52', 'h16-g52late']
TWIN = {'h8-g19': 'h8-tb', 'h8-g20': 'h8-tb', 'h8-h20half': 'h8-tb', 'h8-g20late': 'h8-tbmix',
        'h16-g52': 'h16-tbmix', 'h16-g52late': 'h16-tbmix'}
H8TB = ['h8-tb', 'h8-tbbal', 'h8-tbbalS', 'h8-tbmix']
ORDER = RIVALS + CIRCUITS
FORMS = {0: 'F (shuffle + FMA)', 1: 'A (shuffle + xor + add)', 2: 'X (x86-wht: vpermps + add + sub + blend)'}

out = sys.argv[1] if len(sys.argv) > 1 else 'out'
data = {}   # (binary, mode) -> {L: {name: (best, median)}}
width = {}
for f in sorted(glob.glob(os.path.join(out, 'whole_*.txt'))):
    m = re.match(r'whole_(same|sep)_(.+)$', os.path.basename(f)[:-4])
    if not m:
        continue
    for line in open(f, errors='replace'):
        r = RX.match(line)
        if r:
            xname, L, mode, name, best, med = r.groups()
            key = (m.group(2), mode)
            width[key] = xname
            data.setdefault(key, {}).setdefault(int(L), {})[name] = (float(best), float(med))


def grab(path, pat):
    try:
        for line in open(path, errors='replace'):
            if re.search(pat, line):
                return line.strip()
    except OSError:
        pass
    return ''


def best_rival(d, names=RIVALS):
    riv = [(r, d[r]) for r in names if r in d]
    if not riv:
        return None, None
    return min(riv, key=lambda x: x[1][1])


print('# x86-hybrid512 summary: the best 512-bit textbook I could build, against the circuits in the same structure\n')
cpu = grab(os.path.join(out, 'machine.txt'), r'^Model name')
ua = grab(os.path.join(out, 'run.log'), r'^MICROARCHITECTURE')
print(f'- Machine: {cpu.split(":", 1)[-1].strip() or "?"}; {ua.split(":", 1)[-1].strip() or "?"}')
forced = grab(os.path.join(out, 'quiet.log'), r'BUSY but FORCE=1')
print(f'- Quiet gate: {"FORCED at least once (busy machine): treat the numbers as suspect" if forced else "every timing passed az_quiet (or see quiet.log)"}')
print('- Figure = program median / best rival median in the same process (best of repeats / best rival best in '
      'brackets); below 1 is faster.')
print('  Rivals: ' + ', '.join(RIVALS) + '. Circuits: ' + ', '.join(CIRCUITS) + '.')
print('  h8-h20half outputs H x / 2^p (p = 3-level steps per element; the gate checks the exact scale).')
print('- Structure tuned on the TEXTBOOK only (tune_<binary>.txt); every hybrid, circuit or not, runs the tuned form and '
      'thresholds.\n')

# ---- tune choices ----
print('## Structure chosen by the textbook (tune)\n')
print('| binary | in-lane form (score: sum of the best textbook median at 2^10 and 2^14, ns/point) | thresholds 8-vector '
      '(n:thr) | thresholds 16-vector |')
print('|---|---|---|---|')
for f in sorted(glob.glob(os.path.join(out, 'tune_*.txt'))):
    b = os.path.basename(f)[5:-4]
    form, score, t0, t1 = None, '', [], []
    for line in open(f, errors='replace'):
        p = line.split()
        if p[:1] == ['FORM'] and len(p) > 1:
            form = int(p[1])
        elif line.startswith('TUNEFORM score'):
            score = line.split(':', 1)[1].split('->')[0].strip()
        elif p[:1] == ['THR'] and len(p) == 4:
            (t0 if p[1] == '0' else t1).append(f'{p[2]}:{p[3]}')
    print(f'| {b} | {FORMS.get(form, "?")} ({score}) | {" ".join(t0)} | {" ".join(t1)} |')
print()

# ---- the question ----
print('## Does a circuit beat the best 512-bit code? (same array, best circuit / best rival, same process)\n')
print('| binary | n | best rival (ns/point) | best circuit | ratio | runner-up rival / best rival |')
print('|---|---|---|---|---|---|')
for (b, mode), rows in sorted(data.items()):
    if mode != 'same':
        continue
    for L in sorted(rows):
        d = rows[L]
        bn, bv = best_rival(d)
        if bn is None:
            continue
        circ = [(c, d[c]) for c in CIRCUITS if c in d]
        if not circ:
            continue
        cn, cv = min(circ, key=lambda x: x[1][1])
        others = sorted(d[r][1] for r in RIVALS if r in d and r != bn)
        ru = f'{others[0] / bv[1]:.3f}' if others else '-'
        q = cv[1] / bv[1]
        s = f'{q:.3f}'
        print(f'| {b} | 2^{L} | {bn} {bv[1]:.4f} | {cn} | {"**" + s + "**" if q <= 0.90 else s} | {ru} |')
print()

# ---- Track 2 ----
print('## Track 2 decision (same array, 2^10-2^16, against the best 512-bit rival in the same binary)\n')
print('| binary | width | circuit | sizes measured | worst ratio (n) | best ratio (n) | verdict |')
print('|---|---|---|---|---|---|---|')
verdicts = []
for (b, mode), rows in sorted(data.items()):
    if mode != 'same':
        continue
    Ls = [L for L in sorted(rows) if 10 <= L <= 16]
    for c in CIRCUITS:
        rs = []
        for L in Ls:
            d = rows[L]
            bn, bv = best_rival(d)
            if c in d and bn:
                rs.append((d[c][1] / bv[1], L))
        if not rs:
            continue
        worst, best = max(rs), min(rs)
        v = 'CONTINUE' if worst[0] <= 0.90 else ('CLOSE-LEVEL' if best[0] >= 0.95 else 'BETWEEN')
        verdicts.append((b, c, v))
        print(f'| {b} | {width[(b, mode)]} | {c} | {",".join(str(x[1]) for x in rs)} | '
              f'{worst[0]:.3f} (2^{worst[1]}) | {best[0]:.3f} (2^{best[1]}) | **{v}** |')
cont = [x for x in verdicts if x[2] == 'CONTINUE']
betw = [x for x in verdicts if x[2] == 'BETWEEN']
print()
if not verdicts:
    print('No same-array rows: nothing to decide.\n')
elif cont:
    print('**Host verdict: CONTINUE** (' + '; '.join(f'{b} {c}' for b, c, _ in cont) + '). Check the per-n table, the '
          'cross-compiler rows and the twin rows before believing it; h20half counts only if a scaled transform is '
          'acceptable.\n')
elif betw:
    print('**Host verdict: BETWEEN 0.90 and 0.95 for at least one circuit** (' +
          '; '.join(f'{b} {c}' for b, c, _ in betw) + '): one more deciding host decides.\n')
else:
    print('**Host verdict: every circuit at 0.95 or above at its best on 2^10-2^16 (CLOSE-LEVEL on this host): at 512 '
          'bits the circuit does not beat the best textbook here.**\n')

# ---- library and large sizes ----
print('## Outside 2^10-2^16 (same array): best circuit / best rival\n')
for (b, mode), rows in sorted(data.items()):
    if mode != 'same':
        continue
    xs = []
    for L in sorted(rows):
        if 10 <= L <= 16:
            continue
        d = rows[L]
        bn, bv = best_rival(d)
        circ = [(c, d[c]) for c in CIRCUITS if c in d]
        if bn and circ:
            cn, cv = min(circ, key=lambda x: x[1][1])
            xs.append(f'2^{L} {cv[1] / bv[1]:.3f} ({cn} vs {bn})')
    if xs:
        print(f'- {b}: ' + '; '.join(xs))
print()

# ---- across compilers ----
print('## Across compilers (separate processes, same machine): best circuit over gcc and clang / best rival over gcc '
      'and clang\n')
bywidth = {}
for (b, mode), rows in data.items():
    if mode == 'same':
        bywidth.setdefault(width[(b, mode)], []).append((b, rows))
for w, lst in sorted(bywidth.items()):
    if len(lst) < 2:
        continue
    Ls = sorted(set.intersection(*[set(rows) for _, rows in lst]))
    xs = []
    for L in Ls:
        riv = [(f'{b}:{r}', rows[L][r][1]) for b, rows in lst for r in RIVALS if r in rows[L]]
        cir = [(f'{b}:{c}', rows[L][c][1]) for b, rows in lst for c in CIRCUITS if c in rows[L]]
        if riv and cir:
            br, cr = min(riv, key=lambda x: x[1]), min(cir, key=lambda x: x[1])
            xs.append(f'2^{L} {cr[1] / br[1]:.3f} ({cr[0]} vs {br[0]})')
    if xs:
        print(f'- {w}: ' + '; '.join(xs))
print()

# ---- per binary and mode ----
for (b, mode), rows in sorted(data.items(), key=lambda kv: (kv[0][1] != 'same', kv[0][0])):
    names = [n for n in ORDER if any(n in rows[L] for L in rows)]
    print(f'## {b} ({width[(b, mode)]}), {mode} array\n')
    print('| n | best rival (ns/point) | ' + ' | '.join(names) + ' |')
    print('|---|---|' + '---|' * len(names))
    for L in sorted(rows):
        d = rows[L]
        bn, bv = best_rival(d)
        if bn is None:
            continue
        bbest = min(d[r][0] for r in RIVALS if r in d)
        noisy = any((v[1] - v[0]) / v[0] > 0.05 for v in d.values())
        cells = []
        for n in names:
            if n not in d:
                cells.append('-')
                continue
            q, qb = d[n][1] / bv[1], d[n][0] / bbest
            s = f'{q:.3f} ({qb:.3f})'
            cells.append(f'**{s}**' if n in CIRCUITS and q <= 0.90 else s)
        print(f'| 2^{L}{" (noisy)" if noisy else ""} | {bn} {bv[1]:.4f} | ' + ' | '.join(cells) + ' |')
    print()
    print('Circuit effect inside the same structure (circuit median / its textbook twin median; then / the best h8 '
          'textbook twin):')
    for c in CIRCUITS:
        t = TWIN[c]
        xs = [f'2^{L} {rows[L][c][1] / rows[L][t][1]:.3f}' for L in sorted(rows) if c in rows[L] and t in rows[L]]
        if xs:
            print(f'- {c} / {t}: ' + ', '.join(xs))
        if c in ('h8-g19', 'h8-g20'):  # against the balanced twins (FMA first as generated; SUB first, copy-free)
            for t2 in ('h8-tbbal', 'h8-tbbalS'):
                zs = [f'2^{L} {rows[L][c][1] / rows[L][t2][1]:.3f}' for L in sorted(rows) if c in rows[L] and t2 in rows[L]]
                if zs:
                    print(f'- {c} / {t2}: ' + ', '.join(zs))
        if c.startswith('h8-'):
            ys = []
            for L in sorted(rows):
                tw = [rows[L][x][1] for x in H8TB if x in rows[L]]
                if c in rows[L] and tw:
                    ys.append(f'2^{L} {rows[L][c][1] / min(tw):.3f}')
            if ys:
                print(f'- {c} / best of {"/".join(H8TB)}: ' + ', '.join(ys))
    print('\nStructure effect (textbook kernels throughout):')
    for a, z in (('h8-tbmix', 'x86wht-tbbal'), ('h8-tb', 'x86wht-tb'), ('h8-tbmix', 'FFHT'), ('h16-tbmix', 'h8-tbmix'),
                 ('h8-tbbalS', 'h8-tbbal'), ('h8-tbmix', 'h8-tbbalS'), ('x86wht-tbbalS', 'x86wht-tbbal')):
        xs = [f'2^{L} {rows[L][a][1] / rows[L][z][1]:.3f}' for L in sorted(rows) if a in rows[L] and z in rows[L]]
        if xs:
            print(f'- {a} / {z}: ' + ', '.join(xs))
    print()
skipped = [ln.strip() for ln in open(os.path.join(out, 'run.log'), errors='replace') if 'SKIPPED' in ln] \
    if os.path.exists(os.path.join(out, 'run.log')) else []
if skipped:
    print('## Runs skipped by the time budget\n')
    for s in skipped:
        print(f'- {s}')
