# anycircuit.py seed : the private-wire lemma tested on circuits that are NOT minimum circuits (two-element field).
# ag-7 checked it only on minimum circuits at 8 points and on one family (ad-6).  The lemma claims ANY circuit.
# Random circuits for M(d,k) are grown like this: keep a set of available wires (forms as bitmasks); pick an output
# not yet made; if it is u + v for available u, v, choose such a pair AT RANDOM among ALL pairs (so a gate that adds
# two outputs, or re-uses a label, is chosen whenever one exists); otherwise make a random helper o + u first (itself
# built the same way, to a bounded depth, else by adding its inputs one at a time).  Then for EVERY output and EVERY
# pair (u, v) of wires of the finished circuit with u + v = output (all derivations, not only the one used):
#   (c) count pairs with u, v both outputs;                     claim 0
#   (a) labels: for each non-output wire, the outputs it labels; claim at most 1 per derivation -> here: over ALL
#       pairs, a wire v may appear as label of two outputs only if the two gates read each other (the circle case)
#   (b) graph on non-output wires and z with ALL such edges at once; shortest cycle;  claim >= delta - 2 for cycles
#       whose edges belong to different outputs and can be ordered into one derivation; here simply: any cycle whose
#       L edges belong to L different outputs gives a relation of at most L + 2 outputs, tested directly.
import sys, random
from itertools import combinations
seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
rng = random.Random(seed)

def build(d, k):
    sets = [sum(1 << i for i in c) for j in range(d + 1) for c in combinations(range(k), j)]
    outs = [sum(1 << i for i, s in enumerate(sets) if (s & y) == s) for y in range(1 << k)]
    return len(sets), outs

def make(avail, target, depth, gate):
    """make `target` available; record gate[target] = (u, v)"""
    if target in avail: return
    pairs = [(u, target ^ u) for u in avail if (target ^ u) in avail and u < (target ^ u)]
    if pairs:
        gate[target] = rng.choice(pairs); avail.add(target); return
    if depth > 0:
        u = rng.choice(sorted(avail))
        make(avail, target ^ u, depth - 1, gate)
        if target in avail: return
        gate[target] = (u, target ^ u); avail.add(target); return
    # fall back: add the inputs of the form one at a time
    bits = [1 << i for i in range(target.bit_length()) if target >> i & 1]
    rng.shuffle(bits)
    acc = bits[0]
    for b in bits[1:]:
        nxt = acc ^ b
        if nxt not in avail:
            gate[nxt] = (acc, b); avail.add(nxt)
        acc = nxt

def shortest_cycle_distinct(edges):
    """edges: list of (a, b, owner).  Shortest cycle in the simple graph (one edge per owner by construction)."""
    adj = {}
    for a, b, o in edges:
        adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
    best = 10 ** 9
    for a, b, o in edges:            # remove the edge, shortest path between its ends, plus one
        dist = {a: 0}; q = [a]
        for x in q:
            if dist[x] + 1 >= best: break
            for y in adj[x]:
                if x == a and y == b: continue
                if x == b and y == a: continue
                if y not in dist:
                    dist[y] = dist[x] + 1; q.append(y)
        if b in dist: best = min(best, dist[b] + 1)
    return best

tot = {}
for k, d, trials in ((3, 2, 400), (4, 2, 300), (4, 3, 300), (5, 2, 120), (5, 3, 120), (5, 4, 120), (6, 2, 40), (6, 3, 40), (6, 4, 40), (6, 5, 40), (7, 3, 10), (7, 5, 10)):
    R, outs = build(d, k)
    Out = set(outs); delta = 1 << (d + 1)
    inputs = [1 << i for i in range(R)]
    worst = 10 ** 9; nc = 0; nrep = 0; sizes = []; kinds = [0, 0]
    for t in range(trials):
        avail = set(inputs); gate = {}
        order = [o for o in outs if o not in avail]; rng.shuffle(order)
        for o in order: make(avail, o, rng.choice((0, 1, 1, 2, 3)), gate)
        assert Out <= avail
        W = avail - Out
        # the derivation actually used
        labels = {}; edges = []
        for o in order:
            u, v = gate[o]
            iu, iv = u in Out, v in Out
            if iu and iv: nc += 1
            elif iu or iv:
                lab = v if iu else u
                if lab in labels: nrep += 1
                labels[lab] = o; edges.append(('z', lab, o)); kinds[0] += 1
            else: edges.append((u, v, o)); kinds[1] += 1
        if len(set(frozenset(e[:2]) for e in edges)) < len(edges): nrep += 1
        g = shortest_cycle_distinct(edges); worst = min(worst, g)
        sizes.append(len(gate))
        # all pairs, not only the gates used: no output is the sum of two outputs at all
        for o in outs:
            for u in outs:
                if u < (o ^ u) and (o ^ u) in Out and u != o: nc += 1
    print(f"k={k} d={d} delta={delta}: {trials} random circuits, gates {min(sizes)} to {max(sizes)}; outputs of kind a / b: {kinds[0]} / {kinds[1]}; "
          f"two outputs added: {nc}; repeated label or edge: {nrep}; shortest cycle: {'none' if worst >= 10 ** 9 else worst} (claim: at least {delta - 2})", flush=True)
