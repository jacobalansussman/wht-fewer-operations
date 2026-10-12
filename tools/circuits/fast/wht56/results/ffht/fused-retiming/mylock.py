#!/usr/bin/env python3
"""mylock.py -- take the shared lock /tmp/ffht-timing.LOCK, run one command, release.
Looks 50 times a second (one system call each, no new process), like ../style-generator/lockwait.py:
a waiter that looks every 20 s or every minute never gets the lock between two chained runs."""
import os, sys, time, subprocess
LOCK = '/tmp/ffht-timing.LOCK'
t0 = time.time()
while True:
    try:
        os.mkdir(LOCK); break
    except FileExistsError:
        time.sleep(0.02)
with open(os.path.join(LOCK, 'owner'), 'w') as f:
    f.write('label=fused-retiming pid=%d since=%s out=out (waited %.0f s)\n' % (os.getpid(), time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), time.time() - t0))
rc = 1
try:
    os.environ['WAITED'] = '%.0f' % (time.time() - t0)
    rc = subprocess.call(sys.argv[1:])
finally:
    try:
        own = open(os.path.join(LOCK, 'owner')).read()
        if 'label=fused-retiming pid=%d ' % os.getpid() in own:
            os.unlink(os.path.join(LOCK, 'owner')); os.rmdir(LOCK)
    except OSError:
        pass
sys.exit(rc)
