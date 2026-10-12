#!/usr/bin/env python3
# h-5 / hyperdet.py : for each wire of an 8-point program, Cayley's hyperdeterminant D of the 2x2x2 tensor.
# width 3 and D != 0  <=>  the wire is a sum of TWO product wires (over the reals when D > 0, only over the complex numbers when D < 0);
# width 3 and D = 0   <=>  it needs three product wires (the "W" kind).   Exact integers.
import sys
sys.argv = [sys.argv[0]] + sys.argv[1:]
import importlib.util, io, contextlib
spec = importlib.util.spec_from_file_location('m2', 'meters2.py'); m2 = importlib.util.module_from_spec(spec)
argv = sys.argv; sys.argv = [argv[0]]
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m2)
def hd(a):
    return (a[0]**2*a[7]**2 + a[1]**2*a[6]**2 + a[2]**2*a[5]**2 + a[4]**2*a[3]**2
            - 2*(a[0]*a[1]*a[6]*a[7] + a[0]*a[2]*a[5]*a[7] + a[0]*a[4]*a[3]*a[7] + a[1]*a[2]*a[5]*a[6] + a[1]*a[4]*a[3]*a[6] + a[2]*a[4]*a[3]*a[5])
            + 4*(a[0]*a[3]*a[5]*a[6] + a[1]*a[2]*a[4]*a[7]))
for path in argv[1:]:
    env, gates = m2.load(path); print('==', path)
    for name, par, w in gates:
        b = m2.B(w)
        if len(b) == 3:
            d = hd(w); print('  %-5s %-26s width 3, hyperdeterminant %5d : %s' % (name, ' '.join('%2d' % x for x in w), d,
                  'sum of two product wires' if d > 0 else 'sum of two products only with complex numbers' if d < 0 else 'needs three product wires'))
