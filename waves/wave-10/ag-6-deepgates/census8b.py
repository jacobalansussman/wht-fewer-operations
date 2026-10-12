# census8b.py : per circuit with a deep gate: how many gates of each kind, and the deep gate itself with its two parents
import sys, re, collections
prof = collections.Counter(); shown = 0
for fn in sys.argv[1:]:
    cur = None; lines = []
    def flush():
        global shown
        if not cur: return
        k = collections.Counter(); deep = []
        for l in lines:
            a, b, g = map(int, re.search(r'kind \((\d+),(\d+)\)/(\d+)', l).groups()); k[(a, b, g)] += 1
            if a % 4 == 0 or b % 4 == 0 or g % 4 == 0: deep.append(l.strip())
        if deep:
            prof[(cur, tuple(sorted(k.items())))] += 1
            if shown < 3 and cur[0] == 8:
                shown += 1; print('--- %s N=%d gates=%d' % (fn.split('/')[-1], cur[0], cur[1]))
                for l in lines: print('   ', l.strip()[:110])
    for line in open(fn, errors='ignore'):
        if line.startswith('CIRCUIT'):
            flush(); m = re.search(r'N=(\d+) gates=(\d+)', line); cur = (int(m.group(1)), int(m.group(2))); lines = []
        elif cur and 'kind (' in line: lines.append(line)
    flush()
for (cur, k), c in sorted(prof.items()): print('N=%d gates=%d: %d circuits with kinds %s' % (cur[0], cur[1], c, dict(k)))
