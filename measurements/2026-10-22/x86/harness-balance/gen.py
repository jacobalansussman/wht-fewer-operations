"""gen.py -- circuit file -> C kernel (NEON / AVX2 / AVX-512) with llvm-mca markers around one block.
# fix 22 Oct 2026 (orchestrator): the AVX-512 broadcast was _mm512_set1_ps(*%s), i.e. k[0]+N instead of k[N]; now *(%s).
ax-h0, wave 16.  Usage: gen.py ISA CIRCUIT [--interleave I] [--balance]  > kernel.c
--balance: every second plain add/sub is issued as an FMA with constant +-1 (the 'port-balanced
textbook' rival for cores whose FMA and FADD pipes differ, e.g. AMD Zen, Intel Haswell/Broadwell)."""
import re, sys
from fractions import Fraction as F

def parse(path):
    lines, outs = [], {}
    for raw in open(path):
        s = raw.split('#')[0].strip()
        if not s or '=' not in s: continue
        lhs, rhs = [t.strip() for t in s.split('=', 1)]
        terms = []
        for sign, coef, name in re.findall(r'([+-]?)\s*(?:([0-9/]+)\s*\*\s*)?([A-Za-z_]\w*)', rhs):
            c = F(coef) if coef else F(1)
            if sign == '-': c = -c
            terms.append((c, name))
        lines.append((lhs, terms))
    return lines

ISA = {
 'neon': dict(T='float32x4_t', VL=4, inc='#include <arm_neon.h>', ld='vld1q_f32(%s)', st='vst1q_f32(%s,%s)',
              add='vaddq_f32(%s,%s)', sub='vsubq_f32(%s,%s)', neg='vnegq_f32(%s)', mul='vmulq_f32(%s,%s)',
              fma='vfmaq_f32(%s,%s,%s)',           # acc + v*c
              fmsub='vfmaq_f32(vnegq_f32(%s),%s,%s)', # -acc + v*c
              bc='vld1q_dup_f32(%s)', mark='// LLVM-MCA-%s'),
 'avx2': dict(T='__m256', VL=8, inc='#include <immintrin.h>', ld='_mm256_loadu_ps(%s)', st='_mm256_storeu_ps(%s,%s)',
              add='_mm256_add_ps(%s,%s)', sub='_mm256_sub_ps(%s,%s)', neg='_mm256_xor_ps(%s,_mm256_set1_ps(-0.0f))',
              mul='_mm256_mul_ps(%s,%s)', fma='_mm256_fmadd_ps(%s2,%s3,%s1)', fmsub='_mm256_fmsub_ps(%s2,%s3,%s1)',
              bc='_mm256_broadcast_ss(%s)', mark='# LLVM-MCA-%s'),
 'avx512': dict(T='__m512', VL=16, inc='#include <immintrin.h>', ld='_mm512_loadu_ps(%s)', st='_mm512_storeu_ps(%s,%s)',
              add='_mm512_add_ps(%s,%s)', sub='_mm512_sub_ps(%s,%s)', neg='_mm512_castsi512_ps(_mm512_xor_si512(_mm512_castps_si512(%s),_mm512_set1_epi32(0x80000000)))',
              mul='_mm512_mul_ps(%s,%s)', fma='_mm512_fmadd_ps(%s2,%s3,%s1)', fmsub='_mm512_fmsub_ps(%s2,%s3,%s1)',
              bc='_mm512_set1_ps(*(%s))', mark='# LLVM-MCA-%s'),
}

def fmt3(tmpl, a, v, c):
    # templates with %s1/%s2/%s3 (x86) or positional (neon: acc, v, c)
    if '%s1' in tmpl:
        return tmpl.replace('%s1', a).replace('%s2', v).replace('%s3', c)
    return tmpl % (a, v, c)

def emit(isa, path, inter=1, balance=False):
    D = ISA[isa]; lines = parse(path)
    consts = {}
    def K(c):
        if c not in consts: consts[c] = 'k%d' % len(consts)
        return consts[c]
    body = []; cnt = 0
    for b in range(inter):
        P = 'b%d_' % b
        n = 1 + max(int(m) for _, t in lines for _, nm in t for m in re.findall(r'^x(\d+)$', nm))
        for i in range(n):
            body.append('%s %sx%d = %s;' % (D['T'], P, i, D['ld'] % ('p+(%d*%d+%d)*S' % (b, n, i))))
        nm = lambda s: P + s
        for lhs, terms in lines:
            if len(terms) == 1:
                c, u = terms[0]
                if c == 1: e = nm(u)
                elif c == -1: e = D['neg'] % nm(u)
                else: e = D['mul'] % (nm(u), K(c))
            else:
                (a, u), (bb, v) = terms
                if abs(a) != 1 and abs(bb) == 1: (a, u), (bb, v) = (bb, v), (a, u)
                if abs(a) == 1 and abs(bb) == 1:
                    cnt += 1
                    if balance and cnt % 2 == 0 and not (a == -1 and bb == -1):
                        if a == 1: e = fmt3(D['fma'], nm(u), nm(v), K(bb))
                        else: e = fmt3(D['fma'], nm(v), nm(u), K(a))
                    elif a == 1 and bb == 1: e = D['add'] % (nm(u), nm(v))
                    elif a == 1: e = D['sub'] % (nm(u), nm(v))
                    elif bb == 1: e = D['sub'] % (nm(v), nm(u))
                    else: e = D['neg'] % (D['add'] % (nm(u), nm(v)))
                elif abs(a) == 1:
                    e = fmt3(D['fma'] if a == 1 else D['fmsub'], nm(u), nm(v), K(bb))
                else: raise SystemExit('two constants: %s' % lhs)
            body.append('%s %s = %s;' % (D['T'], nm(lhs), e))
        outs = sorted([l for l, _ in lines if re.match(r'^y\d+$', l)], key=lambda s: int(s[1:]))
        for o in outs:
            body.append(D['st'] % ('p+(%d*%d+%s)*S' % (b, n, o[1:]), nm(o)) + ';')
    cdecl = ['%s %s = %s;' % (D['T'], v, D['bc'] % ('k+%d' % i)) for i, (c, v) in enumerate(consts.items())]
    cvals = ', '.join('%sf' % float(c) for c in consts)
    src = [D['inc'], '#define S 1024', 'const float KV[] = {%s};' % (cvals or '0'),
           'void kern(float *restrict p0, const float *restrict k, long cols) {'] + ['  ' + s for s in cdecl] + \
          ['  for (long j = 0; j < cols; j += %d) { float *p = p0 + j;' % D['VL'],
           '    __asm__ volatile("%s");' % (D['mark'] % 'BEGIN blk')] + ['    ' + s for s in body] + \
          ['    __asm__ volatile("%s");' % (D['mark'] % 'END'), '  }', '}']
    return '\n'.join(src)

if __name__ == '__main__':
    a = sys.argv[1:]
    inter = int(a[a.index('--interleave') + 1]) if '--interleave' in a else 1
    print(emit(a[0], a[1], inter, '--balance' in a))
