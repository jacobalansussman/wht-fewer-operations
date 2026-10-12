# u-4-zdz: the same gate-list files under m-cross's own meter (meter2.py, unchanged functions), to check zdz.py's meter against it.
import sys, re
src = open('../m-cross/meter2.py').read().split("for N in (4, 8, 16, 32)")[0]
exec(src)
for path in sys.argv[1:]:
    g = parse(path)
    N = 1 + max(int(t[1:]) for (_, _, u, _, v) in g for t in (u, v) if re.fullmatch(r'x\d+', t))
    print(meter(path, g, N))
