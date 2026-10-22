#!/usr/bin/env python3
"""check_plan.py FHT_AVX_C TYPE BINARY [Lmin Lmax] -- does the hybrid run FFHT's structure? (x86-hybrid, 22 Oct 2026)

Reads FFHT's generated fht_avx.c (TYPE = float or double), expands each helper_TYPE_L by hand (its depth-first recursion
over the 'if (depth == D)' sections), and lists every composite step in execution order:
    offset, A, B, C, m, lanes   for (j = 0; j < A; j += B) for (k = 0; k < C; k += lanes) { m vectors at offset+j+k+l*C }
(lanes = 1 if the step's asm does in-lane levels: vpermilp* / vperm2f128).  Then runs `BINARY trace 3 L...` (the
hybrid's own plan code, the code that is timed, printing the same list) and compares the two lists exactly.
Also checks that every FFHT cross-vector step does exactly m*log2(m) vector adds/subs (the textbook in registers) and
that each in-lane step adds 2*w per vector (w = 3 float, 2 double): the instructions the hybrid replaces.
Standard library only.  Exit 0 = PLAN MATCH for every L, 1 = mismatch, 2 = usage / parse error.
"""
import re
import subprocess
import sys

R_ITER = r'^static inline void helper_%s_(\d+)\(%s \*buf\) \{$'
R_REC = r'^void helper_%s_(\d+)_recursive\(%s \*buf, int depth\) \{$'
R_J = re.compile(r'^\s*for \(int j = 0; j < (\d+); j \+= (\d+)\) \{$')
R_K = re.compile(r'^\s*for \(int k = 0; k < (\d+); k \+= (\d+)\) \{$')
R_KPLAIN = re.compile(r'^\s*for \(int k = 0; k < (\d+); \+\+k\) \{$')
R_CALL = re.compile(r'^\s*helper_\w+_(\d+)_recursive\(buf \+ (\d+), (\d+)\);$')
R_DEPTH = re.compile(r'^  if \(depth == (\d+)\) \{$')
ADDSUB = re.compile(r'"v(add|sub|addsub)p[sd] ')


def items(body, logw):
    """body lines -> list of ('S', A, B, C, m, lanes, addsub) | ('rec', off, depth) | ('plain',)"""
    out, i = [], 0
    while i < len(body):
        ln = body[i]
        mc = R_CALL.match(ln)
        if mc:
            out.append(('rec', int(mc.group(2)), int(mc.group(3))))
            i += 1
            continue
        mj = R_J.match(ln)
        if mj:
            A, B = int(mj.group(1)), int(mj.group(2))
            nxt = body[i + 1]
            if R_KPLAIN.match(nxt):
                out.append(('plain',))
                i += 2
                continue
            mk = R_K.match(nxt)
            C = int(mk.group(1)) if mk else B      # single-loop form (log_n == w): one vector per j
            # the asm block follows: instruction lines, then the operand line ':: "r"(...)'
            k = i + 1
            asm = []
            while '::' not in body[k]:
                asm.append(body[k])
                k += 1
            m = body[k].count('"r"(')
            lanes = int(any('vperm' in a for a in asm))
            addsub = sum(1 for a in asm if ADDSUB.search(a))
            out.append(('S', A, B, C, m, lanes, addsub))
            i = k + 1
            continue
        i += 1
    return out


def parse(path, t, logw):
    lines = open(path).read().split('\n')
    ri, rr = re.compile(R_ITER % (t, t)), re.compile(R_REC % (t, t))
    funcs, i = {}, 0
    while i < len(lines):
        m1, m2 = ri.match(lines[i]), rr.match(lines[i])
        if not (m1 or m2):
            i += 1
            continue
        L = int((m1 or m2).group(1))
        body = []
        i += 1
        while lines[i] != '}':
            body.append(lines[i])
            i += 1
        if m1:
            funcs[L] = ('iter', items(body, logw))
        else:
            secs, cur, buf = {}, None, []
            for ln in body:
                md = R_DEPTH.match(ln)
                if md:
                    cur, buf = int(md.group(1)), []
                    continue
                if ln.strip() == 'return;' and cur is not None:
                    secs[cur] = items(buf, logw)
                    cur = None
                    continue
                if cur is not None:
                    buf.append(ln)
            funcs[L] = ('rec', secs)
    return funcs


def expand(f, L):
    kind, data = f
    out = []
    if kind == 'iter':
        seq = [(0, it) for it in data]
    else:
        seq = []

        def run(d, base):
            if d not in data:
                raise KeyError(f'FFHT code for 2^{L} has no "if (depth == {d})" section')
            for it in data[d]:
                if it[0] == 'rec':
                    run(it[2], base + it[1])
                else:
                    seq.append((base, it))
        run(L, 0)
    for base, it in seq:
        if it[0] == 'plain':
            return None
        out.append((base,) + it[1:])
    return out


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(2)
    path, t, binary = sys.argv[1:4]
    lo, hi = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else (1, 20)
    logw = 3 if t == 'float' else 2
    funcs = parse(path, t, logw)
    Ls = [L for L in range(max(lo, logw), hi + 1)]
    run = subprocess.run([binary, 'trace', '3'] + [str(L) for L in Ls], capture_output=True, text=True)
    mine, cur = {}, None
    for ln in run.stdout.split('\n'):
        p = ln.split()
        if p[:1] == ['L']:
            cur = int(p[1])
            mine[cur] = []
        elif p[:1] == ['S'] and cur is not None:
            mine[cur].append(tuple(int(x) for x in p[1:7]))
    ok, nsteps, bad_arith = True, 0, 0
    for L in Ls:
        if L not in funcs:
            print(f'PLAN 2^{L}: helper_{t}_{L} not found in {path}')
            ok = False
            continue
        try:
            ff = expand(funcs[L], L)
        except KeyError as e:
            print(f'PLAN 2^{L}: MISMATCH: {e.args[0]}')
            ok = False
            continue
        if ff is None:
            continue
        for (base, A, B, C, m, lanes, addsub) in ff:
            lev = m.bit_length() - 1
            want = m * lev + (2 * logw * m if lanes else 0)
            if addsub != want:
                bad_arith += 1
                print(f'ARITH 2^{L}: FFHT step A={A} B={B} C={C} m={m} lanes={lanes}: {addsub} add/sub, expected {want}')
        ffs = [x[:6] for x in ff]
        mn = mine.get(L, [])
        if ffs != mn:
            ok = False
            j = next((k for k in range(min(len(ffs), len(mn))) if ffs[k] != mn[k]), min(len(ffs), len(mn)))
            print(f'PLAN 2^{L}: MISMATCH at step {j}: FFHT {ffs[j] if j < len(ffs) else "end"} vs hybrid '
                  f'{mn[j] if j < len(mn) else "end"} ({len(ffs)} vs {len(mn)} steps)')
        else:
            nsteps += len(ffs)
            first = ff[:4] if len(ff) > 4 else ff
            print(f'PLAN 2^{L}: {len(ffs)} steps identical (offset, span, j-step, stride, vectors, in-lane); '
                  f'first: {[x[1:6] for x in first]}')
    print(f'ARITH: every FFHT step does m*log2(m) cross-vector add/sub (+{2 * logw} per vector in its in-lane step): '
          + ('YES' if bad_arith == 0 else f'NO ({bad_arith} steps differ)'))
    print(('PLAN MATCH' if ok else 'PLAN MISMATCH') + f' ({t}, 2^{Ls[0]}..2^{Ls[-1]}, {nsteps} steps compared)')
    sys.exit(0 if ok and bad_arith == 0 else 1)


if __name__ == '__main__':
    main()
