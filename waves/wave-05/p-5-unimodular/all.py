import subprocess, sys
for cmd, out in [(["floor.py"], "floor.out"), (["k19.py"], "k19.out"), (["inplace.py", "6"], "inplace.out")]:
    with open(out, "w") as fh: subprocess.run([sys.executable, "-B"] + cmd, stdout=fh, stderr=subprocess.STDOUT)
