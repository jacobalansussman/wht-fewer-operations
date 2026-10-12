# census8.py : in every circuit printed by the walker tj (x-0's and ab-2's runs), which gates are deep?
# a gate is printed as "kind (a,b)/g": g*w = a*u + b*v on primitive wires.  deep = a or b divisible by 4, or g divisible by 4.
import sys, re, collections
tot = collections.defaultdict(lambda: [0, 0, 0, collections.Counter()])
for fn in sys.argv[1:]:
    cur = None
    for line in open(fn, errors='ignore'):
        if line.startswith('CIRCUIT'):
            m = re.search(r'N=(\d+) gates=(\d+)', line); cur = (int(m.group(1)), int(m.group(2))); st = {'deep': 0, 'half': 0}
            tot[cur][0] += 1; seen_deep = False; seen_half = False
        elif cur and 'kind (' in line:
            a, b, g = map(int, re.search(r'kind \((\d+),(\d+)\)/(\d+)', line).groups())
            tot[cur][3][(a, b, g)] += 1
            if (a % 4 == 0 or b % 4 == 0 or g % 4 == 0) and not seen_deep: seen_deep = True; tot[cur][1] += 1
            if g % 2 == 0 and not seen_half: seen_half = True; tot[cur][2] += 1
for key in sorted(tot):
    t = tot[key]; print('N=%d, %d gates: circuits printed %d; with a deep gate %d; with a halving %d; kinds %s' % (key[0], key[1], t[0], t[1], t[2], dict(t[3])))
