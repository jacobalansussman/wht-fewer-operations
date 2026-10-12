"""k8kernel.py -- 8-point kernels across 8 registers, for FFHT's generator (gen.py).

This file is new and is not part of FFHT.  The patched gen.py imports it.  It changes one thing
in what gen.py writes: the block that takes 8 registers through 3 levels.  FFHT writes that block
as the textbook does, 12 additions and 12 subtractions.  With this file the block can be

  textbook   FFHT's own block; gen.py's output is then the same as without this file, byte for byte
  half20     the 20-operation circuit (circuits/h8_half_20ops.txt of the repository): 19 additions
             and subtractions and one multiplication by 1/2.  It gives (H_8 x) / 2, so every such
             pass halves the data.  SCALE says what happens to the halvings:
               raw     nothing: after P such passes the array holds H x / 2^P ("up to scale")
               exact   the last such pass of a helper multiplies its 8 results by 2^P before it
                       stores them (8 more multiplications in that one pass), so the helper
                       returns H x itself
  fma19      the 19-gate circuit (circuits/h8_19gates.txt): 7 additions and subtractions and 12
             lines "w + 2 p", "w - 2 p" or "2 p - w", each written as ONE multiply-add instruction
             (vfmadd132 / vfnmadd132 / vfmsub132, FMA3) with the constant 2.  It gives H_8 x
             itself; nothing to repair.  It needs a processor with FMA; FFHT itself needs AVX only.

The choice comes from the environment (or set the module variables before generating):

  FFHT_K8_KERNEL    textbook (default) | half20 | fma19
  FFHT_K8_SCALE     exact (default) | raw                (half20 only)
  FFHT_K8_FMACONST  mem (default) | reg                  (fma19 only: the constant 2 as a memory
                                                          operand of each multiply-add, or loaded
                                                          once per block into a 14th register)
  FFHT_K8_SCALECONST mem (default) | reg                 (half20, exact: the 2^P of the repairing pass
                                                          as a memory operand of each of its 8
                                                          multiplications, or loaded once into a
                                                          free register: one instruction more)
  FFHT_K8_MIN_BLOCK_BYTES  0 (default) | a number        the new kernel is used only in passes whose
                                                          block (the 8 rows together) is at least
                                                          that many bytes; smaller passes keep
                                                          FFHT's textbook block.  The first pass has
                                                          a block of 256 bytes.
  FFHT_PLAN         a hall-of-fame file: gen.py then writes exactly that plan and measures nothing
  FFHT_OUT          the folder for fht_avx.c and the tables (default: the current folder)

Registers.  gen.py hands over 8 registers that hold the 8 rows (ymm0..ymm7) and 8 free registers
(ymm8..ymm15).  The circuit is written out in the order of its file; every result gets the
lowest free register, and a register is free again after the last use of its value (AVX
instructions write to a third register, so no copy is needed).  If the 16 registers did not
suffice, emit() would stop with an error: nothing is ever spilled to memory.  stats() reports how
many registers were in use at most.

The constants are memory operands of the instructions ("m" operands of the assembly block, which
gcc addresses relative to the instruction pointer), so they take neither a vector register nor a
general register.

Every circuit is checked when this file is loaded: it is run on the 8 unit inputs in exact
fractions, and every output yJ must be factor * (row J of H_8).
"""
import os
import re
from fractions import Fraction

KERNEL = os.environ.get('FFHT_K8_KERNEL', 'textbook')
SCALE = os.environ.get('FFHT_K8_SCALE', 'exact')
FMA_CONST = os.environ.get('FFHT_K8_FMACONST', 'mem')
MIN_BLOCK_BYTES = int(os.environ.get('FFHT_K8_MIN_BLOCK_BYTES', '0'))
SCALE_CONST = os.environ.get('FFHT_K8_SCALECONST', 'mem')
MAX_HALVINGS = 10       # a helper has at most 9 passes of 8 registers (2^30 points)

# The gate lines of circuits/h8_half_20ops.txt
# (sha256 of that file 493b2cdb375e2b945956571c3637caf6a5774936b361cfd58e5bd505eed42f8e).
HALF20_TEXT = """
g1 = x0 + x7
g2 = x1 + x6
g3 = x2 - x5
g4 = x3 - x4
g5 = g1 - g2
g6 = g3 + g4
g7 = g5 - g6
m8 = 1/2*g7
g9 = m8 - x7
g10 = m8 - x5
g11 = g9 + x6
g12 = g10 - x4
g13 = g11 + g4
g14 = g10 + x3
g15 = g5 - g14
g16 = g11 + g3
g17 = g12 + g2
g18 = g9 + x1
g19 = g18 + g6
g20 = g1 - g12
y0 = g20
y1 = g16
y2 = g18
y3 = g14
y4 = g19
y5 = g15
y6 = g17
y7 = g13
"""

# The gate lines of circuits/h8_19gates.txt
# (sha256 of that file 85df5257d8d06c33f493a986f55c36d86c95549269f19e2c0e14b3eed69d2ccb).
FMA19_TEXT = """
g1  = x0 + x7
g2  = x1 + x6
g3  = x2 - x5
g4  = x3 - x4
g5  = g1 - g2
g6  = g3 + g4
g7  = g5 - g6
g8  = g7 - 2*x7
g9  = g7 - 2*x5
g10 = g8 + 2*x6
g11 = g9 - 2*x4
y7  = g10 + 2*g4
y3  = g9 + 2*x3
y5  = -y3 + 2*g5
y1  = g10 + 2*g3
y6  = g11 + 2*g2
y2  = g8 + 2*x1
y4  = y2 + 2*g6
y0  = -g11 + 2*g1
"""

# The textbook on 8 points (circuits/O_textbook_8.txt), only for stats(): FFHT writes its own.
TEXTBOOK_TEXT = """
t1 = x0 + x1
t2 = x0 - x1
t3 = x2 + x3
t4 = x2 - x3
t5 = x4 + x5
t6 = x4 - x5
t7 = x6 + x7
t8 = x6 - x7
t9 = t1 + t3
t10 = t1 - t3
t11 = t2 + t4
t12 = t2 - t4
t13 = t5 + t7
t14 = t5 - t7
t15 = t6 + t8
t16 = t6 - t8
t17 = t9 + t13
t18 = t9 - t13
t19 = t11 + t15
t20 = t11 - t15
t21 = t10 + t14
t22 = t10 - t14
t23 = t12 + t16
t24 = t12 - t16
y0 = t17
y1 = t19
y2 = t21
y3 = t23
y4 = t18
y5 = t20
y6 = t22
y7 = t24
"""

_TERM = re.compile(r'([+-]?)(?:(\d+(?:/\d+)?)\*)?([A-Za-z_]\w*)')


def parse(text):
    """The circuit text as (gates, outs): gates = [(name, [(coefficient, operand), ...])] with
    one or two terms; outs[J] = the name of the value that is output row J."""
    alias = {}
    gates = []
    outputs = {}
    for raw in text.splitlines():
        s = raw.split('#', 1)[0].strip()
        if not s:
            continue
        lhs, rhs = [t.strip() for t in s.split('=', 1)]
        rhs = rhs.replace(' ', '')
        terms = []
        pos = 0
        while pos < len(rhs):
            m = _TERM.match(rhs, pos)
            if not m or (pos > 0 and not m.group(1)):
                raise ValueError('cannot read: ' + raw)
            c = Fraction(m.group(2) or 1)
            if m.group(1) == '-':
                c = -c
            terms.append((c, alias.get(m.group(3), m.group(3))))
            pos = m.end()
        if len(terms) == 1 and terms[0][0] == 1:
            alias[lhs] = terms[0][1]            # a renaming: no gate
        elif len(terms) in (1, 2):
            gates.append((lhs, terms))
        else:
            raise ValueError('a line has one or two terms: ' + raw)
        if re.fullmatch(r'y\d+', lhs):
            outputs[int(lhs[1:])] = alias.get(lhs, lhs)
    return gates, [outputs[j] for j in range(8)]


def factor_of(gates, outs):
    """Run the circuit on the 8 unit inputs in exact fractions.  Returns f with
    output J = f * (row J of H_8) for every J, or raises."""
    vec = {}
    for i in range(8):
        e = [Fraction(0)] * 8
        e[i] = Fraction(1)
        vec['x%d' % i] = e
    for name, terms in gates:
        v = [Fraction(0)] * 8
        for c, u in terms:
            v = [p + c * q for p, q in zip(v, vec[u])]
        vec[name] = v
    f = vec[outs[0]][0]
    for j in range(8):
        want = [f * (-1 if bin(j & i).count('1') & 1 else 1) for i in range(8)]
        if f == 0 or vec[outs[j]] != want:
            raise AssertionError('output y%d is not a multiple of row %d of H_8' % (j, j))
    return f


CIRCUITS = {}
for _name, _text, _factor in (('half20', HALF20_TEXT, Fraction(1, 2)),
                              ('fma19', FMA19_TEXT, Fraction(1)),
                              ('textbook', TEXTBOOK_TEXT, Fraction(1))):
    _g, _o = parse(_text)
    if factor_of(_g, _o) != _factor:
        raise AssertionError('circuit %s has the wrong factor' % _name)
    CIRCUITS[_name] = (_g, _o)


def _regnum(r):
    return int(re.sub(r'\D', '', r))


def emit(gates, outs, sfx, in_regs, free_regs, const_operand, ident='', const_reg=None):
    """Write the circuit as AVX instructions (AT&T syntax, inside a C string, as gen.py does).

    in_regs[i] holds input x_i; free_regs are free.  const_operand is the text of the operand
    that holds the constant of the circuit (1/2 or 2), e.g. '%8'; with const_reg the constant is
    in that register (which must not be in free_regs).
    Returns (code, out_regs, st): out_regs[J] = the register that holds output row J;
    st = {'instructions': {mnemonic: count}, 'max_in_use': n, 'copies': n}."""
    last = {}
    for i, (_, terms) in enumerate(gates):
        for _, u in terms:
            last[u] = i
    for o in outs:
        last[o] = len(gates)                    # an output is alive to the end
    reg = dict(('x%d' % i, r) for i, r in enumerate(in_regs))
    free = list(free_regs)
    total = len(in_regs) + len(free_regs) + (1 if const_reg else 0)
    st = {'instructions': {}, 'max_in_use': total - len(free), 'copies': 0}
    code = []

    def line(mnemonic, a, b, c=None):
        st['instructions'][mnemonic] = st['instructions'].get(mnemonic, 0) + 1
        ops = [a, b] + ([c] if c is not None else [])
        code.append(ident + '"%s %s\\n"\n' % (mnemonic, ', '.join(ops)))

    def R(r):
        return '%%' + r                          # "%%ymm3" in the C text

    def take():
        if not free:
            raise Exception('k8kernel: the circuit does not fit in the registers')
        free.sort(key=_regnum)
        r = free.pop(0)
        st['max_in_use'] = max(st['max_in_use'], total - len(free))
        return r

    C = R(const_reg) if const_reg else const_operand
    for i, (name, terms) in enumerate(gates):
        dying = [u for _, u in terms if last[u] == i]
        if len(terms) == 1:
            (c, a), = terms                      # a multiplication by the constant
            ra = reg[a]
            for u in set(dying):
                free.append(reg.pop(u))
            rd = take()
            line('vmul' + sfx, C, R(ra), R(rd))
        else:
            (ca, a), (cb, b) = terms
            if abs(ca) == 1 and abs(cb) == 1:
                ra, rb = reg[a], reg[b]
                for u in set(dying):
                    free.append(reg.pop(u))
                rd = take()
                if ca == 1 and cb == 1:
                    line('vadd' + sfx, R(rb), R(ra), R(rd))      # rd = ra + rb
                elif ca == 1 and cb == -1:
                    line('vsub' + sfx, R(rb), R(ra), R(rd))      # rd = ra - rb
                elif ca == -1 and cb == 1:
                    line('vsub' + sfx, R(ra), R(rb), R(rd))      # rd = rb - ra
                else:
                    raise Exception('k8kernel: -a - b is not written')
            else:
                # w + 2 p, w - 2 p or 2 p - w: one multiply-add that overwrites p
                if abs(ca) == 2 and abs(cb) == 1:
                    (cp, p), (cw, w) = (ca, a), (cb, b)
                elif abs(cb) == 2 and abs(ca) == 1:
                    (cp, p), (cw, w) = (cb, b), (ca, a)
                else:
                    raise Exception('k8kernel: cannot write gate %s' % name)
                rw = reg[w]
                if last[p] == i and p != w:
                    rd = reg.pop(p)                              # p dies here: overwrite it
                else:
                    rd = take()                                  # p is needed later: copy it
                    line('vmova' + sfx, R(reg[p]), R(rd))
                    st['copies'] += 1
                if cw == 1 and cp == 2:
                    line('vfmadd132' + sfx, C, R(rw), R(rd))     # rd = rd * 2 + rw
                elif cw == 1 and cp == -2:
                    line('vfnmadd132' + sfx, C, R(rw), R(rd))    # rd = -(rd * 2) + rw
                elif cw == -1 and cp == 2:
                    line('vfmsub132' + sfx, C, R(rw), R(rd))     # rd = rd * 2 - rw
                else:
                    raise Exception('k8kernel: cannot write gate %s' % name)
                if last[w] == i and w in reg and w != p:
                    free.append(reg.pop(w))
        reg[name] = rd
        if name not in last:
            free.append(reg.pop(name))           # a result nobody uses (kloop's test kernels only)
    return ''.join(code), [reg[o] for o in outs], st


_TYPES = {'vmovups': ('ps', 'float', 8), 'vmovupd': ('pd', 'double', 4)}
_OP_MARK = '@@K8OP@@'
_MUL_MARK = re.compile(r'^( *)@@K8MUL (\w+) (\d+) (\w+) ([\w ]+)@@\n', re.M)


def active(move_instruction, to_it=None):
    """True when gen.py is to call block() for a pass of 8 registers and 3 levels.
    to_it: the pass does the levels to_it - 3 .. to_it - 1, on blocks of 2^to_it numbers."""
    if KERNEL not in CIRCUITS:
        raise ValueError('FFHT_K8_KERNEL must be textbook, half20 or fma19')
    if KERNEL == 'textbook' or move_instruction not in _TYPES:
        return False
    if to_it is not None and MIN_BLOCK_BYTES:
        size = 4 if _TYPES[move_instruction][1] == 'float' else 8
        if (size << to_it) < MIN_BLOCK_BYTES:
            return False
    return True


def block(move_instruction, in_regs, free_regs, ident=''):
    """The three levels between 8 registers.  Returns (code, out_regs, extra_operands):
    out_regs[J] is stored to the address of row J by gen.py; extra_operands are added to the
    operand list of the assembly block after its 8 addresses (so they are %8, %9)."""
    sfx, type_name, _ = _TYPES[move_instruction]
    if len(in_regs) != 8 or len(free_regs) != 8:
        raise Exception('k8kernel: 8 registers of data and 8 free registers expected')
    gates, outs = CIRCUITS[KERNEL]
    if KERNEL == 'half20':
        code, out_regs, _ = emit(gates, outs, sfx, in_regs, free_regs, '%8', ident)
        # finish() turns this line into the 8 multiplications by 2^P, or removes it
        spare = [r for r in sorted(list(in_regs) + list(free_regs), key=_regnum) if r not in out_regs][-1]
        code += ident + '@@K8MUL %s 9 %s %s@@\n' % (sfx, spare, ' '.join(out_regs))
        return code, out_regs, ['"m"(fht_k8_half_%s)%s' % (type_name, _OP_MARK)]
    if KERNEL != 'fma19':
        # a kernel without a constant: only the timing-only test kernels of kloop_gen.py
        code, out_regs, _ = emit(gates, outs, sfx, in_regs, free_regs, None, ident)
        return code, out_regs, []
    if FMA_CONST == 'reg':
        creg = sorted(free_regs, key=_regnum)[-1]
        rest = [r for r in free_regs if r != creg]
        code = ident + '"vbroadcasts%s %%8, %%%%%s\\n"\n' % (sfx[1], creg)
        body, out_regs, _ = emit(gates, outs, sfx, in_regs, rest, None, ident, const_reg=creg)
        return code + body, out_regs, ['"m"(fht_k8_two_%s)' % type_name]
    code, out_regs, _ = emit(gates, outs, sfx, in_regs, free_regs, '%8', ident)
    return code, out_regs, ['"m"(fht_k8_two_%s)' % type_name]


halvings = {}       # (type_name, log_n) -> the number P of half20 passes in that helper


def finish(res, type_name, log_n):
    """The text of one helper, as gen.py's greedy_merged / greedy_merged_recursive built it.
    Every point goes through every pass of a helper once, so a helper with P half20 passes
    returns H x / 2^P.  SCALE = exact: the last of them (the outermost one) multiplies by 2^P."""
    marks = list(_MUL_MARK.finditer(res))
    p = len(marks)
    if KERNEL == 'half20':
        halvings[(type_name, log_n)] = p
    if p > MAX_HALVINGS:
        raise Exception('k8kernel: more than %d halvings' % MAX_HALVINGS)
    out = []
    pos = 0
    for idx, m in enumerate(marks):
        out.append(res[pos:m.start()])
        pos = m.end()
        if idx == p - 1 and SCALE == 'exact':
            ident, sfx, opno, spare, regs = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5).split()
            if SCALE_CONST == 'reg':
                out.append(ident + '"vbroadcasts%s %%%s, %%%%%s\\n"\n' % (sfx[1], opno, spare))
                for r in regs:
                    out.append(ident + '"vmul%s %%%%%s, %%%%%s, %%%%%s\\n"\n' % (sfx, spare, r, r))
            else:
                for r in regs:
                    out.append(ident + '"vmul%s %%%s, %%%%%s, %%%%%s\\n"\n' % (sfx, opno, r, r))
            rest = res[pos:].replace(_OP_MARK, ', "m"(fht_k8_pow2_%s[%d])' % (type_name, p), 1)
            out.append(rest)
            pos = len(res)
    out.append(res[pos:])
    return ''.join(out).replace(_OP_MARK, '')


def preamble():
    """The constants, as C definitions for the top of fht_avx.c (nothing for the textbook)."""
    if KERNEL == 'textbook':
        return ''
    res = ''
    for type_name, width, suffix in (('float', 8, 'f'), ('double', 4, '')):
        def row(v):
            return '{' + ', '.join(['%s%s' % (v, suffix)] * width) + '}'
        if KERNEL == 'half20':
            res += 'static const %s fht_k8_half_%s[%d] __attribute__((aligned(32))) = %s;\n' % (
                type_name, type_name, width, row('0.5'))
            if SCALE == 'exact':
                res += 'static const %s fht_k8_pow2_%s[%d][%d] __attribute__((aligned(32))) = {\n' % (
                    type_name, type_name, MAX_HALVINGS + 1, width)
                for p in range(MAX_HALVINGS + 1):
                    res += '  %s,\n' % row('%d.0' % (1 << p))
                res += '};\n'
        else:
            res += 'static const %s fht_k8_two_%s[%d] __attribute__((aligned(32))) = %s;\n' % (
                type_name, type_name, width, row('2.0'))
    return res


def read_plan(path=None):
    """FFHT's hall-of-fame file as {(type_name, log_n): description}; None if no file is named."""
    path = path or os.environ.get('FFHT_PLAN')
    if not path:
        return None
    plan = {}
    with open(path) as f:
        for raw in f:
            m = re.match(r'type_name = (\w+); log_n = (\d+); best_time = \S+; best_desc = (.+)$', raw.strip())
            if not m:
                raise ValueError('cannot read the plan line: ' + raw)
            plan[(m.group(1), int(m.group(2)))] = m.group(3)
    return plan


def write_tables(out_dir='.'):
    """k8_scale.inc: for every size, the power of two by which the output of fht_float /
    fht_double is divided (0 everywhere except for half20 with SCALE = raw)."""
    with open(os.path.join(out_dir, 'k8_scale.inc'), 'w') as f:
        f.write('/* written by k8kernel.py: kernel %s, scale %s.  fht_T(buf, log_n) returns\n'
                ' * H x / 2^k8_scale_T[log_n];  k8_passes_T[log_n] = passes with the half20 kernel. */\n'
                % (KERNEL, SCALE if KERNEL == 'half20' else '-'))
        for type_name in ('float', 'double'):
            p = [halvings.get((type_name, k), 0) for k in range(31)]
            s = p if (KERNEL == 'half20' and SCALE == 'raw') else [0] * 31
            f.write('static const int k8_scale_%s[31] = {%s};\n' % (type_name, ', '.join(map(str, s))))
            f.write('static const int k8_passes_%s[31] = {%s};\n' % (type_name, ', '.join(map(str, p))))


def stats():
    """What each kernel costs, from the emitter itself (for the report)."""
    regs_in = ['ymm%d' % i for i in range(8)]
    regs_free = ['ymm%d' % i for i in range(8, 16)]
    rows = []
    for name in ('textbook', 'half20', 'fma19'):
        gates, outs = CIRCUITS[name]
        _, out_regs, st = emit(gates, outs, 'ps', regs_in, regs_free, '%8')
        depth = {}
        for g, terms in gates:
            depth[g] = 1 + max(depth.get(u, 0) for _, u in terms)
        rows.append((name, st, out_regs, max(depth[o] for o in outs)))
    gates, outs = CIRCUITS['fma19']
    _, out_regs, st = emit(gates, outs, 'ps', regs_in, regs_free[:-1], None, const_reg=regs_free[-1])
    rows.append(('fma19, constant in a register', st, out_regs, rows[-1][3]))
    return rows


if __name__ == '__main__':
    for name, st, out_regs, depth in stats():
        ins = st['instructions']
        print('%-30s %2d instructions (%s); registers in use at most %d of 16; copies %d; '
              'longest chain %d operations; outputs in %s'
              % (name, sum(ins.values()), ', '.join('%d %s' % (ins[k], k) for k in sorted(ins)),
                 st['max_in_use'], st['copies'], depth, ' '.join(out_regs)))
