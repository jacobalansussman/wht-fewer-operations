# u-3-zletter/bylevel.py : for a replayed design (output of zreplay_tree.py on stdin), the number of nodes of each row's step,
# by the size of the row's subset, and whether the step comes from a smaller row, a larger row, an incomparable row or from 0.
import sys, re, collections
cost = collections.defaultdict(list); kind = collections.Counter()
for l in sys.stdin:
    m = re.match(r"\s+y\[(\w+)\] = (0|y\[(\w+)\]) (.*)", l)
    if not m: continue
    S = set() if m.group(1) == 'e' else set(m.group(1))
    n = len(re.findall(r"\{", m.group(4)))
    cost[len(S)].append(n)
    if m.group(2) == '0': kind['from 0'] += 1
    else:
        P = set() if m.group(3) == 'e' else set(m.group(3))
        kind['from a smaller row' if P < S else 'from a larger row' if S < P else 'from an incomparable row'] += 1
for sz in sorted(cost): print('  size', sz, 'rows', len(cost[sz]), 'nodes per step', sorted(cost[sz]), 'mean %.2f' % (sum(cost[sz]) / len(cost[sz])))
print('  ', dict(kind))
