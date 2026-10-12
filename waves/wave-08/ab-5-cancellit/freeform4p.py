# ab-5: census of single free forms at 4 points over the fields with 3 and 5 elements (forms up to scaling).
import subprocess, os, itertools, collections
here = os.path.dirname(os.path.abspath(__file__))
def run(p, m, free=None):
    args = [os.path.join(here, 'mincirc_free'), str(p), '4', str(m), os.path.join(here, 'rows_zeta2.txt')]
    if free is not None:
        fn = os.path.join(here, 'free4p_tmp.txt'); open(fn, 'w').write(' '.join(map(str, free)) + '\n'); args.append(fn)
    out = subprocess.run(args, capture_output=True, text=True).stdout
    return ('YES' in out), int(out.split('gate budget')[1].split()[0])
for p in (3, 5):
    assert run(p, 0)[0] is False and run(p, 1) == (True, 4)
    hist = collections.Counter(); best = []
    for w in itertools.product(range(p), repeat=4):
        nz = [c for c in w if c]
        if len(nz) < 2 or nz[0] != 1: continue          # skip zero, inputs, and all but one scaling of each form
        for m in range(0, 3):
            ok, b = run(p, m, w)
            if ok:
                hist[4 - b] += 1
                if 4 - b >= 2: best.append(w)
                break
    print('field with %d elements, 4 points: saving -> number of forms: %s ; forms saving 2: %s' % (p, dict(sorted(hist.items())), best))
