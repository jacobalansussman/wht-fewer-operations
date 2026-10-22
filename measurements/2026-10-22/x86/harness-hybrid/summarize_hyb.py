#!/usr/bin/env python3
"""summarize_hyb.py OUTDIR -- SUMMARY.md for the x86-hybrid job (22 Oct 2026).  Standard library only.

Reads every RESULT line in OUTDIR/whole_<mode>_<binary>.txt.  For each binary, mode and n:
  ratio = program median / median of the BEST RIVAL (the fastest by median of FFHT, x86wht-tb, x86wht-tbbal, hyb8-tb8,
          hyb8-tb8bal, hyb16-tb16, hyb8-tb8balS), all in the same process; below 1 = faster.  The same with
          best-of-repeats in brackets.  hyb8-tb8balS (twin review, 22 Oct 2026) = hyb8-tb8bal with each butterfly
          emitted SUB before FMA (no register copies in clang).
Track 2 decision rule (PLAN.md, Track 2): a circuit continues at 0.90 or below on whole transforms 2^10-2^16, same array,
against the best rival; between 0.90 and 0.95 one more deciding host decides; 0.95 or above counts towards closing.
Read here per (binary, circuit): CONTINUE if its WORST ratio over the measured n in 2^10..2^16 is <= 0.90; CLOSE-LEVEL if
its BEST ratio there is >= 0.95; otherwise BETWEEN.
"""
import glob
import os
import re
import sys

RX = re.compile(r'^RESULT x86-hybrid whole (\S+) 2\^(\d+) (same|separate)\s+(\S+)\s+best\s+([\d.]+)\s+median\s+([\d.]+)')
RIVALS = ['FFHT', 'x86wht-tb', 'x86wht-tbbal', 'hyb8-tb8', 'hyb8-tb8bal', 'hyb16-tb16', 'hyb8-tb8balS']
CIRCUITS = ['hyb8-g19', 'hyb8-g20', 'hyb8-h20half', 'hyb16-g52']
TWIN = {'hyb8-g19': 'hyb8-tb8', 'hyb8-g20': 'hyb8-tb8', 'hyb8-h20half': 'hyb8-tb8', 'hyb16-g52': 'hyb16-tb16'}
ORDER = RIVALS + CIRCUITS

out = sys.argv[1] if len(sys.argv) > 1 else 'out'
data = {}   # (binary, mode) -> {L: {name: (best, median)}}
width = {}
for f in sorted(glob.glob(os.path.join(out, 'whole_*.txt'))):
    base = os.path.basename(f)[:-4]
    m = re.match(r'whole_(same|sep)_(.+)$', base)
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


print('# x86-hybrid summary: FFHT\'s structure with the circuits as its in-register kernels\n')
cpu = grab(os.path.join(out, 'machine.txt'), r'^Model name')
ua = grab(os.path.join(out, 'run.log'), r'^MICROARCHITECTURE')
print(f'- Machine: {cpu.split(":", 1)[-1].strip() or "?"}; {ua.split(":", 1)[-1].strip() or "?"}')
forced = grab(os.path.join(out, 'quiet.log'), r'BUSY but FORCE=1')
print(f'- Quiet gate: {"FORCED at least once (busy machine): treat the numbers as suspect" if forced else "every timing passed az_quiet (or see quiet.log)"}')
print('- Figure = program median / best rival median (best of repeats / best rival best in brackets); below 1 is faster.')
print('  Rivals: ' + ', '.join(RIVALS) + '. Circuits: ' + ', '.join(CIRCUITS) + '.')
print('  hyb8-h20half outputs H x / 2^p (p = 8-point steps per element; the gate checks the exact scale).\n')

# ---- the decision ----
print('## Track 2 decision (same array, 2^10-2^16, against the best rival in the same binary)\n')
print('| binary | width | circuit | sizes measured | worst ratio (n) | best ratio (n) | verdict |')
print('|---|---|---|---|---|---|---|')
verdicts = []
for (b, mode), rows in sorted(data.items()):
    if mode != 'same':
        continue
    Ls = [L for L in sorted(rows) if 10 <= L <= 16]
    if not Ls:
        continue
    for c in CIRCUITS:
        rs = []
        for L in Ls:
            d = rows[L]
            riv = [d[r] for r in RIVALS if r in d]
            if c not in d or not riv:
                continue
            br = min(riv, key=lambda x: x[1])
            rs.append((d[c][1] / br[1], L))
        if not rs:
            continue
        worst, best = max(rs), min(rs)
        v = 'CONTINUE' if worst[0] <= 0.90 else ('CLOSE-LEVEL' if best[0] >= 0.95 else 'BETWEEN')
        verdicts.append((b, c, v))
        print(f'| {b} | {width[(b, mode)]} | {c} | {",".join(str(L) for L in Ls)} | {worst[0]:.3f} (2^{worst[1]}) '
              f'| {best[0]:.3f} (2^{best[1]}) | **{v}** |')
cont = [x for x in verdicts if x[2] == 'CONTINUE']
betw = [x for x in verdicts if x[2] == 'BETWEEN']
print()
if not verdicts:
    print('No same-array rows: nothing to decide.\n')
elif cont:
    print('**Host verdict: CONTINUE** (' + '; '.join(f'{b} {c}' for b, c, _ in cont) + '). '
          'Check the per-n table and the circuit-vs-twin rows before believing it; h20half counts only if a scaled '
          'transform is acceptable.\n')
elif betw:
    print('**Host verdict: BETWEEN 0.90 and 0.95 for at least one circuit** (' + '; '.join(f'{b} {c}' for b, c, _ in betw)
          + '): one more deciding host decides.\n')
else:
    print('**Host verdict: every circuit at 0.95 or above at its best on 2^10-2^16 (CLOSE-LEVEL on this host).**\n')

# ---- per binary and mode ----
for (b, mode), rows in sorted(data.items(), key=lambda kv: (kv[0][1] != 'same', kv[0][0])):
    names = [n for n in ORDER if any(n in rows[L] for L in rows)]
    print(f'## {b} ({width[(b, mode)]}), {mode} array\n')
    print('| n | best rival (ns/point) | ' + ' | '.join(names) + ' |')
    print('|---|---|' + '---|' * len(names))
    for L in sorted(rows):
        d = rows[L]
        riv = [(r, d[r]) for r in RIVALS if r in d]
        if not riv:
            continue
        bn, bv = min(riv, key=lambda x: x[1][1])
        bbest = min(v[0] for _, v in riv)
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
    print('Circuit effect inside the same structure (circuit median / its textbook twin median): ')
    for c in CIRCUITS:
        t = TWIN[c]
        xs = [f'2^{L} {rows[L][c][1] / rows[L][t][1]:.3f}' for L in sorted(rows) if c in rows[L] and t in rows[L]]
        if xs:
            print(f'- {c} / {t}: ' + ', '.join(xs))
    for c in ('hyb8-g19', 'hyb8-g20'):  # against the balanced twins (FMA first as generated; SUB first, copy-free)
        for t in ('hyb8-tb8bal', 'hyb8-tb8balS'):
            xs = [f'2^{L} {rows[L][c][1] / rows[L][t][1]:.3f}' for L in sorted(rows) if c in rows[L] and t in rows[L]]
            if xs:
                print(f'- {c} / {t}: ' + ', '.join(xs))
    print('\nStructure effect (textbook kernels throughout):')
    for a, z in (('hyb8-tb8', 'FFHT'), ('x86wht-tb', 'FFHT'), ('hyb16-tb16', 'hyb8-tb8'), ('hyb8-tb8bal', 'hyb8-tb8'),
                 ('hyb8-tb8balS', 'hyb8-tb8bal')):
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
