# p-7-twoletters, experiment (a): how many LETTERS is a given gate list?   Pure Python, exact fractions.
# A letter = an "up" part (a laminar family of merges: every up gate adds two forms on disjoint sets of the letter's input
# wires, and the sets of all up gates are nested or disjoint) followed by a "down" part (a forest: every down gate adds
# to at most one down gate of the same letter, its "stream", forms that are up forms or input wires of the letter).
# A wire made in an earlier letter may be used as an input wire of any later letter at no cost (a pass-through).
# This is exactly "sum of tree rectangles": rectangles of a letter = (non-stream operands of its down gates) + pass-throughs.
# The program replays the gate list exactly, then looks for an assignment gate -> (letter, up/down) with the fewest letters
# by depth-first search (node limit; "exhaustive" is printed when the search space was finished).
import sys, re
from fractions import Fraction as Fr
sys.setrecursionlimit(10000)

def parse(path):
    gates = []
    for line in open(path):
        line = line.split('#')[0].strip()
        if '=' not in line: continue
        name, rhs = [t.strip() for t in line.split('=')]
        rhs = rhs.replace('*', ' ').replace('- ', '+ -').replace('+ -', '+ - ')
        toks = rhs.split()
        terms = []; sign = 1; coef = None
        for t in toks:
            if t == '+': continue
            if t == '-': sign = -sign; continue
            if re.fullmatch(r'-?\d+(/\d+)?', t): coef = Fr(t); continue
            if t.startswith('-'): sign = -sign; t = t[1:]
            terms.append((sign * (coef if coef is not None else Fr(1)), t)); sign = 1; coef = None
        assert len(terms) == 2, (line, terms)
        gates.append((name, terms[0][0], terms[0][1], terms[1][0], terms[1][1]))
    return gates
def replay(N, gates, outnames=None):
    vec = {'x%d' % i: [Fr(int(i == j)) for j in range(N)] for i in range(N)}
    for (n, a, u, b, v) in gates: vec[n] = list(vec[u]) if a is None else [a * p + b * q for p, q in zip(vec[u], vec[v])]
    rows = {tuple((-1) ** bin(y & x).count('1') for x in range(N)): y for y in range(N)}
    found = {}
    for n, w in vec.items():
        if tuple(w) in rows: found.setdefault(rows[tuple(w)], n)
    return len(found) == N, found
def letters(N, gates, outs, Lmax, limit=2000000):
    G = len(gates); let = {'x%d' % i: 0 for i in range(N)}; role = {'x%d' % i: 'in' for i in range(N)}; supp = {}
    ups = {l: [] for l in range(1, Lmax + 1)}; nodes = [0]; best = [None]
    def laminar(l, S):
        for T in ups[l]:
            if T == S: return False
            I = T & S
            if I and I != T and I != S: return False
        return True
    def rec(i):
        nodes[0] += 1
        if nodes[0] > limit: return False
        if i == G: best[0] = (dict(let), dict(role)); return True
        (n, a, u, b, v) = gates[i]; m = max(let[u], let[v], 1)
        if a is None:      # a free copy: a second leaf with the same value, same letter, an output of that letter
            let[n] = let[u]; role[n] = 'down' if role[u] != 'in' else 'in'
            if rec(i + 1): return True
            del let[n]; del role[n]; return False
        for l in (m, m + 1):
            if l > Lmax: break
            # up
            ok = True; S = frozenset()
            for o in (u, v):
                if let[o] == l and role[o] == 'up': So = supp[o]
                elif let[o] < l: So = frozenset([o])
                else: ok = False; break
                if S & So: ok = False; break
                S = S | So
            if ok and u != v and laminar(l, S):
                let[n] = l; role[n] = 'up'; supp[n] = S; ups[l].append(S)
                if rec(i + 1): return True
                ups[l].pop(); del supp[n]
            # down
            nd = sum(1 for o in (u, v) if let[o] == l and role[o] == 'down')
            if nd <= 1 and all((let[o] < l) or (let[o] == l) for o in (u, v)):
                let[n] = l; role[n] = 'down'
                if rec(i + 1): return True
            if n in let: del let[n]; del role[n]
        return False
    okk = rec(0)
    return okk, nodes[0], best[0]
def report(label, N, gates):
    ok, found = replay(N, gates)
    print("%s: %d points, %d gates (G) and %d free copies; exact replay: every row of the transform is a wire: %s" % (label, N, sum(1 for g in gates if g[1] is not None), sum(1 for g in gates if g[1] is None), ok))
    if not ok: return
    outs = set(found.values())
    for Lmax in range(1, 8):
        good, nn, best = letters(N, gates, outs, Lmax)
        if good: break
        print("   %d letter(s): no assignment; search %s (%d nodes)" % (Lmax, "EXHAUSTIVE" if nn <= 2000000 else "stopped at the node limit, not a proof", nn))
    let, role = best
    used_later = {}
    for (n, a, u, b, v) in gates:
        for o in (u, v):
            if let[o] < let[n]: used_later.setdefault(o, set()).add(let[n])
    print("   fewest letters found: %d" % Lmax)
    for l in range(1, Lmax + 1):
        gl = [g for g in gates if let[g[0]] == l and g[1] is not None]
        up = [g for g in gl if role[g[0]] == 'up']; dn = [g for g in gl if role[g[0]] == 'down']
        rect = sum(sum(1 for o in (g[2], g[4]) if not (let[o] == l and role[o] == 'down')) for g in dn)
        # wires leaving letter l towards later letters or the output
        leave = set()
        for w in list(let):
            if let[w] <= l and (any(t > l for t in used_later.get(w, ())) or (w in outs)): leave.add(w)
        passthrough = [w for w in leave if not (let[w] == l and role[w] == 'down')]
        print("   letter %d: %d gates (%d up, %d down); rectangles %d + %d pass-throughs = %d; wires leaving it: %d" % (l, len(gl), len(up), len(dn), rect, len(passthrough), rect + len(passthrough), len(leave)))
    return Lmax

if __name__ == '__main__':
    I = 'waves/wave-05'
    g19 = parse(I + '/g-1-tightwires/h8_19gates.txt')
    report("g-1's 19", 8, g19)
    for N in (4, 8, 16, 32, 64):
        report("e2-0 slp_%d" % N, N, parse(I + '/e2-0-pieces/slp_%d.txt' % N))
    # bricks at 16 points: (H4 x I)(I x H4), each H4 the 7-gate brick
    def brick(pre, ins, outs_):
        x0, x1, x2, x3 = ins
        return [(pre + 'a', Fr(1), x0, Fr(1), x1), (pre + 'b', Fr(-1), x2, Fr(1), x3), (pre + 'h', Fr(1), pre + 'a', Fr(1), pre + 'b'),
                (outs_[0], Fr(1), pre + 'h', Fr(2), x2), (outs_[1], Fr(-1), pre + 'h', Fr(2), x0), (outs_[2], Fr(1), pre + 'h', Fr(-2), x3), (outs_[3], Fr(1), pre + 'h', Fr(-2), x1)]
    gb = []
    for b in range(4): gb += brick('L%d' % b, ['x%d' % (4 * b + i) for i in range(4)], ['m%d_%d' % (b, c) for c in range(4)])
    for c in range(4): gb += brick('T%d' % c, ['m%d_%d' % (b, c) for b in range(4)], ['o%d_%d' % (c, t) for t in range(4)])
    report("two layers of bricks", 16, gb)
    # tensored 19: pairs first, then g-1's 19 on the sums and on the differences
    gt = []
    for j in range(8): gt += [('s%d' % j, Fr(1), 'x%d' % (2 * j), Fr(1), 'x%d' % (2 * j + 1)), ('d%d' % j, Fr(1), 'x%d' % (2 * j), Fr(-1), 'x%d' % (2 * j + 1))]
    for fam in 'sd':
        ren = lambda t: (fam + t[1:]) if t.startswith('x') else (fam.upper() + t)
        gt += [(ren(n), a, ren(u), b, ren(v)) for (n, a, u, b, v) in g19]
    report("pairs, then the 19 twice", 16, gt)
    # the 52 with its four doubly used hubs duplicated: is THAT two letters?
    g52 = parse(I + '/e2-0-pieces/slp_16.txt'); dup = []
    hubs = {'hub11': 'p13', 'hub14': 'p16', 'hub27': 'p29', 'hub30': 'p32'}     # hub -> the second form built on it
    for (n, a, u, b, v) in g52:
        if n in hubs:
            dup.append((n, a, u, b, v))
            dup.append((u + 'c', None, u, None, u)); dup.append((v + 'c', None, v, None, v))
            dup.append((n + 'copy', a, u + 'c', b, v + 'c'))
        elif n in hubs.values():
            h = [k for k in hubs if hubs[k] == n][0]
            dup.append((n, a, (u + 'copy') if u == h else u, b, (v + 'copy') if v == h else v))
        else: dup.append((n, a, u, b, v))
    report("e2-0's 52 with four middle hubs computed twice on copied wires", 16, dup)
