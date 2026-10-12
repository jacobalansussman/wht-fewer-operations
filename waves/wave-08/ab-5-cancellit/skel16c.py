# ab-5: skeleton A' at 16 points (two-element field): the lower half complete (12 gates, Yates) and the upper half
# without the chain of its total (9 gates) are fixed; can the 8 mixed outputs be finished with 10 gates (total 31)?
import subprocess, os
here = os.path.dirname(os.path.abspath(__file__))
def vec(idx): return ' '.join('1' if i in idx else '0' for i in range(16))
def zrow(S, off): return [off + T for T in range(8) if (T & S) == T]
lower9 = [zrow(1, 0), zrow(2, 0), [2, 3], zrow(3, 0), [4, 5], [4, 6], zrow(4, 0), zrow(5, 0), zrow(6, 0)]
lower12 = lower9 + [[6, 7], [4, 5, 6, 7], zrow(7, 0)]
upper9 = [[i + 8 for i in f] for f in lower9]
fn = os.path.join(here, 'free16_Ap.txt'); open(fn, 'w').write('\n'.join(vec(f) for f in lower12 + upper9) + '\n')
for m in (1, 2, 3):
    out = subprocess.run([os.path.join(here, 'mincirc_free'), '2', '16', str(m), os.path.join(here, 'rows_zeta4.txt'), fn], capture_output=True, text=True).stdout
    budget = int(out.split('gate budget')[1].split()[0])
    print("skeleton A' (lower half complete, upper half without the chain of its total): built in advance 21 gates; remaining budget %d -> total %d : %s" % (budget, 21 + budget, 'YES' if 'YES' in out else 'NO (exhaustive)'), flush=True)
