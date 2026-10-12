#!/usr/bin/env python3
"""lockwait.py -- take the lock of the FFHT timing job, then run a command that holds it.

    python3 -B lockwait.py COMMAND [ARGUMENTS]

The lock is the directory /tmp/ffht-timing.LOCK (mkdir is the taking).  The shared
locked_run.sh looks every 20 seconds whether the lock is free.  Another job runs its timings as a
chain, each of which takes the lock again a fraction of a second after the one before released
it, so a waiter that looks every 20 seconds never gets it.  This program looks 50 times a
second (one system call each time, no new process), takes the lock, and starts COMMAND with
LOCK_HELD=1 in the environment; the copy of locked_run.sh in harness/ then skips its own taking
and does everything else as before, including the release at its end.

A lock that is older than 30 minutes and whose owner process is gone is taken over, with a line
on stderr saying so.  That rule was added after the runs of 11 October 2026 and has been tried
only on a scratch directory, not on the Linux machine.
"""
import os
import re
import sys
import time

LOCK = os.environ.get('LOCK', '/tmp/ffht-timing.LOCK')
STALE_SECONDS = 1800


def stale():
    """The rule of the job: a lock older than 30 minutes whose owner process is gone may be taken.
    (Added after the runs of 11 October 2026: the version that ran that day waited for ever on such
    a lock.  The owner's pid is read from LOCK/owner, as the shared locked_run.sh does.)"""
    try:
        age = time.time() - os.stat(LOCK).st_mtime
        if age <= STALE_SECONDS:
            return False
        try:
            owner = open(os.path.join(LOCK, 'owner')).read()
        except OSError:
            owner = ''
        m = re.search(r'pid=(\d+)', owner)
        if m:
            try:
                os.kill(int(m.group(1)), 0)
                return False                     # the owner is alive: the lock is held, however old
            except ProcessLookupError:
                pass
            except PermissionError:
                return False
        sys.stderr.write('%s the lock is %.0f s old and its owner (%s) is gone: taking it\n'
                         % (time.strftime('%H:%M:%S', time.gmtime()), age, owner.strip()))
        for name in os.listdir(LOCK):
            os.unlink(os.path.join(LOCK, name))
        os.rmdir(LOCK)
        return True
    except OSError:
        return False


t0 = time.time()
looks = 0
while True:
    try:
        os.mkdir(LOCK)
        break
    except FileExistsError:
        looks += 1
        if looks % 500 == 0 and stale():         # about every 10 seconds
            continue
        time.sleep(0.02)
with open(os.path.join(LOCK, 'owner'), 'w') as f:
    f.write('label=%s pid=%d since=%s (taken by lockwait.py after %.0f s)\n' % (
        os.environ.get('LABEL', 'style-generator'), os.getpid(),
        time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), time.time() - t0))
sys.stderr.write('%s lock taken after waiting %.0f s\n' % (time.strftime('%H:%M:%S', time.gmtime()), time.time() - t0))
os.environ['LOCK_HELD'] = '1'
rc = 1
try:
    rc = os.spawnvp(os.P_WAIT, sys.argv[1], sys.argv[1:])
finally:
    try:                        # locked_run.sh removes the lock itself; this is for any other command
        if os.path.isdir(LOCK):
            for name in os.listdir(LOCK):
                os.unlink(os.path.join(LOCK, name))
            os.rmdir(LOCK)
    except OSError:
        pass
sys.exit(rc)
