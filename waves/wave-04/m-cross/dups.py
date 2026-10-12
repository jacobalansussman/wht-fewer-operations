# m-cross: which gates of a circuit are "duplicate joins" (parents in two different classes modulo 2, result in a class already held)?
import sys
src = open(sys.argv[1]).read().split("for N in (4, 8, 16, 32)")[0]
exec(src)
for path in sys.argv[2:]:
    g = parse(path); N = 1 + max(int(t[1:]) for (_, _, u, _, v) in g for t in (u, v) if t[0] == 'x' and t[1:].isdigit())
    W = {'x%d' % i: [F(int(i == j)) for j in range(N)] for i in range(N)}; first = {canon(W[n], 1): n for n in W}
    print(path, 'N =', N)
    for (name, a, u, b, v) in g:
        w = [a * p + b * q for p, q in zip(W[u], W[v])]; W[name] = w
        cu, cv, cw = canon(prim(W[u]), 1), canon(prim(W[v]), 1), canon(prim(w), 1)
        if cw in first and cw not in (cu, cv):
            print('   duplicate join: %-6s = %s*%s + %s*%s   support %2d, wire %s ; same class as %s = %s' % (name, a, u, b, v, sum(cw), ' '.join(str(int(t)) for t in w), first[cw], ' '.join(str(int(t)) for t in W[first[cw]])))
        first.setdefault(cw, name)
