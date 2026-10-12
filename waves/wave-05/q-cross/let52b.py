# q-cross hybrid 3: p-7's exact letter counter run on h-1's SECOND 52-gate circuit (the one with wires entangled on four bits),
# on h-8's three-hub 21 and on h-1's seeds.  Tool: p-7-twoletters/letters.py (imported, unchanged).
import sys
sys.path.insert(0, 'waves/wave-05/p-7-twoletters')
import letters as L
I = 'waves/wave-05'
for label, N, path in (("h-1 second 52 (slp16_52_from54)", 16, I + '/h-1-staircase3/slp16_52_from54.txt'),
                       ("h-8 three-hub 21", 8, I + '/h-8-provethewrongthi/h8_21_three_hubs.txt')):
    try:
        L.report(label, N, L.parse(path))
    except Exception as e:
        print(label, "FAILED:", repr(e)[:300])
    sys.stdout.flush()
