#!/usr/bin/env python3
"""lockwait.py -- take the lock of the FFHT timing jobs, then become the command that holds it.

    python3 -B lockwait.py sh locked_run.sh OUTFILE command [arguments]

The lock is the directory /tmp/ffht-timing.LOCK; making it is taking it.  Several jobs wait
for it, some of them looking many times a second, so a waiter that looks every few seconds
never gets a turn.  This one looks 50 times a second (one system call each time), takes the
lock, and replaces itself by the command with LOCK_HELD=1 in the environment.  locked_run.sh
then skips its own taking and does everything else as before: the wait for other benchmarks,
the pinning, the record of the load, and the release of the lock at its end.
"""
import os
import sys
import time

LOCK = os.environ.get('LOCK', '/tmp/ffht-timing.LOCK')
t0 = time.time()
while True:
    try:
        os.mkdir(LOCK)
        break
    except FileExistsError:
        time.sleep(0.02)
with open(os.path.join(LOCK, 'owner'), 'w') as f:
    f.write('label=%s pid=%d since=%s (lockwait.py, after %.0f s)\n' % (
        os.environ.get('LABEL', 'style-intrinsics'), os.getpid(),
        time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), time.time() - t0))
sys.stderr.write('%s lock taken after %.0f s\n' % (time.strftime('%H:%M:%S', time.gmtime()), time.time() - t0))
sys.stderr.flush()
os.environ['LOCK_HELD'] = '1'
os.execvp(sys.argv[1], sys.argv[1:])
