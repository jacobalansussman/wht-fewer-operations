# ab-5: the same census at 4 points (two-element field): gates for Z_4 when one form w is free.  Known answer without w: 4.
import subprocess, os, collections
here = os.path.dirname(os.path.abspath(__file__))
def run(m, free=None):
    args = [os.path.join(here, 'mincirc_free'), '2', '4', str(m), os.path.join(here, 'rows_zeta2.txt')]
    if free is not None:
        fn = os.path.join(here, 'free_tmp4.txt'); open(fn, 'w').write(' '.join(str((free >> i) & 1) for i in range(4)) + '\n'); args.append(fn)
    out = subprocess.run(args, capture_output=True, text=True).stdout
    return ('YES' in out), int(out.split('gate budget')[1].split()[0])
assert run(0)[0] is False and run(1) == (True, 4)
print('check: Z_4 without free form: 4 gates, not 3  OK')
for w in range(1, 16):
    if bin(w).count('1') == 1: continue
    for m in range(0, 3):
        ok, b = run(m, w)
        if ok: print('saving %d  gates %d  w = %s' % (4 - b, b, '+'.join('x%d' % i for i in range(4) if (w >> i) & 1))); break
