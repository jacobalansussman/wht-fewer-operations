# u-4-zdz: run corn8 on every kind of triangular factor in kinds8.txt (L and its transpose), plain and with free row signs.
# usage: corn8_driver.py <signs 0|1> <parity 0|1|all>
import sys, subprocess
signs = sys.argv[1]; par = sys.argv[2]
for line in open('kinds8.txt'):
    if '|' not in line: continue
    idx, head, mat = [t.strip() for t in line.split('|')]
    if par != 'all' and int(idx) % 2 != int(par): continue
    v = list(map(int, mat.split())); L = [v[8 * i:8 * i + 8] for i in range(8)]
    for name, Mx in (('L', L), ('L^T', [[L[j][i] for j in range(8)] for i in range(8)])):
        out = subprocess.run(['./corn8', signs], input=' '.join(str(x) for row in Mx for x in row), capture_output=True, text=True).stdout.strip()
        print('kind %s (%s) %-3s : %s' % (idx, head, name, out), flush=True)
