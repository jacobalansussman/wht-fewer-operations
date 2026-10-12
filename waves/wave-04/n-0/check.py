#!/usr/bin/env python3
"""n-0 check.py: an independent exact replay of count-(O) programs (one addition, subtraction or
multiplication by a constant per line).  Written by the critic n-0; shares no code with orec.py or ocheck.py.

usage: check.py <file> [<file> ...]

Two separate methods per file.
 A. all N unit vectors at once (plain Python, 64-bit arrays): every wire is the integer vector of its coefficients times 2^E (E = 24);
    a multiplication by p/q must divide exactly, or the file is rejected.  Proves the matrix.
 B. three random integer vectors in Python fractions against a direct sum over the definition
    out_j = sum_i (-1)^popcount(i & j) x_i  (no fast transform used).  Sizes up to 4096 only.
"""
import sys, re, random
from fractions import Fraction
from array import array

LINE = re.compile(r"^(\w+)\s*=\s*(\S+)\s*([+\-*])\s*(\S+)$")

def parse(path):
    ops, outs, defined = [], None, set()
    for raw in open(path):
        s = raw.strip()
        if not s:
            continue
        if s.startswith("# OUT"):
            outs = s.split()[2:]
            continue
        if s.startswith("#"):
            continue
        m = LINE.match(s)
        if not m:
            raise SystemExit(f"{path}: cannot read line: {s}")
        name, a, op, b = m.groups()
        if name in defined or re.fullmatch(r"x\d+", name):
            raise SystemExit(f"{path}: {name} defined twice")
        defined.add(name)
        if op == "*":
            ops.append((name, "*", Fraction(a), b))      # constant * wire
        else:
            ops.append((name, op, a, b))
    return ops, outs

def last_use(ops, outs):
    last = {}
    for t, (name, op, a, b) in enumerate(ops):
        for w in ((b,) if op == "*" else (a, b)):
            last[w] = t
    for w in outs:
        last[w] = len(ops) + 1
    return last

def method_a(ops, outs, N, E=24):
    """returns (factor, kinds, consts) or stops"""
    last = last_use(ops, outs)
    val = {}
    one = 1 << E
    for i in range(N):
        v = array("q", [0]) * N; v[i] = one
        val[f"x{i}"] = v
    kinds = {"+": 0, "-": 0, "*": 0}
    consts = {}
    for t, (name, op, a, b) in enumerate(ops):
        kinds[op] += 1
        if op == "*":
            c = a
            consts[c] = consts.get(c, 0) + 1
            p, q = c.numerator, c.denominator
            u = val[b]
            if q != 1 and any((e * p) % q for e in u):
                raise SystemExit(f"line {t}: {name}: division not exact at 2^{E}")
            val[name] = array("q", [(e * p) // q for e in u])
            used = (b,)
        elif op == "+":
            val[name] = array("q", map(int.__add__, val[a], val[b])); used = (a, b)
        else:
            val[name] = array("q", map(int.__sub__, val[a], val[b])); used = (a, b)
        for w in used:
            if last.get(w, -1) <= t and w in val:
                del val[w]
    par = [bin(i).count("1") & 1 for i in range(N)]
    factor = None
    for j, w in enumerate(outs):
        row = val[w]
        r0 = row[0]
        f = Fraction(r0, one)
        if factor is None:
            factor = f
        # Sylvester row j: (-1)^popcount(i & j)
        if f != factor or f == 0 or any(row[i] != (-r0 if par[i & j] else r0) for i in range(N)):
            raise SystemExit(f"output {j} ({w}) is not {factor} times row {j} of H")
    return factor, kinds, consts

def method_b(ops, outs, N, factor, trials=3, seed=20261011):
    rng = random.Random(seed)
    if N > 1024:
        trials = 1
    for _ in range(trials):
        x = [rng.randint(-10**6, 10**6) for _ in range(N)]
        val = {f"x{i}": Fraction(x[i]) for i in range(N)}
        for name, op, a, b in ops:
            if op == "*":
                val[name] = a * val[b]
            elif op == "+":
                val[name] = val[a] + val[b]
            else:
                val[name] = val[a] - val[b]
        for j, w in enumerate(outs):
            s = 0
            for i in range(N):
                s += -x[i] if bin(i & j).count("1") & 1 else x[i]
            if val[w] != factor * s:
                return False
    return True

if __name__ == "__main__":
    for path in sys.argv[1:]:
        ops, outs = parse(path)
        N = len(outs)
        k = N.bit_length() - 1
        assert 1 << k == N and len(set(outs)) == N
        # every name used is an input or defined on an earlier line
        seen = {f"x{i}" for i in range(N)}
        for name, op, a, b in ops:
            for w in ((b,) if op == "*" else (a, b)):
                if w not in seen:
                    raise SystemExit(f"{path}: {name} uses {w} before it exists")
            seen.add(name)
        factor, kinds, consts = method_a(ops, outs, N)
        b = method_b(ops, outs, N, factor) if N <= 4096 else None
        cs = ", ".join(f"{c}: {n}" for c, n in sorted(consts.items()))
        print(f"{path.split('/')[-1]:14s} N={N:<6d} operations={len(ops):<7d} (+ {kinds['+']}, - {kinds['-']}, * {kinds['*']}; constants {{{cs}}})  "
              f"textbook={N*k:<7d} outputs = {factor} * (row j of H), j in Sylvester order: A OK"
              f"{'' if b is None else ', B OK' if b else ', B FAIL'}", flush=True)
