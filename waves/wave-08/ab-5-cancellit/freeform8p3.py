# ab-5: 8 points, field with 3 elements: which single free forms (up to scaling) bring Z_8 down to 10 gates or fewer?
# Only budgets up to 10 are searched, so the output lists the forms that save 2 or more; the rest save 0 or 1.
import subprocess, os, itertools, collections, sys, time
here = os.path.dirname(os.path.abspath(__file__))
def run(m, free):
    fn = os.path.join(here, 'free8p3_tmp.txt'); open(fn, 'w').write(' '.join(map(str, free)) + '\n')
    out = subprocess.run([os.path.join(here, 'mincirc_free'), '3', '8', str(m), os.path.join(here, 'rows_zeta3.txt'), fn], capture_output=True, text=True).stdout
    return ('YES' in out), int(out.split('gate budget')[1].split()[0])
t0 = time.time(); hist = collections.Counter(); tried = 0
for w in itertools.product(range(3), repeat=8):
    nz = [c for c in w if c]
    if len(nz) < 2 or nz[0] != 1: continue
    tried += 1; got = None
    for m in range(0, 5):
        ok, b = run(m, w)
        if b > 10: break
        if ok: got = b; break
    if got is not None:
        hist[12 - got] += 1
        if 12 - got >= 3 or (12 - got == 2 and 2 in w): print('saving %d  w = %s' % (12 - got, w), flush=True)
    if time.time() - t0 > 520: print('STOPPED EARLY after %d forms' % tried, flush=True); break
print('forms tried: %d ; saving -> number of forms (2 or more only): %s ; the others save 0 or 1  (%.0f s)' % (tried, dict(sorted(hist.items())), time.time() - t0), flush=True)
