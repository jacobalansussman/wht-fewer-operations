#!/usr/bin/env python3
"""runq.py -- run the shell scripts in jobs/pending/ in name order, at most TWO at a time.
Each job runs in its own process group; the sum of the resident memory of the group is read
every 3 seconds and the job is stopped if it passes 2 GB (LIMIT_KB) or its time limit
(first line "# timeout=SECONDS", default 600).  A record goes to jobs/done/<name>.json.
Stops when the file jobs/STOP exists and nothing is running, or at the wall-clock time
given as argv[1] (HH:MM, today): after that time no new job is started.
"""
import json
import os
import signal
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PEND = os.path.join(HERE, 'jobs', 'pending')
DONE = os.path.join(HERE, 'jobs', 'done')
RUN = os.path.join(HERE, 'jobs', 'running')
LIMIT_KB = 2000000
WORKERS = 2
lock = threading.Lock()
os.makedirs(RUN, exist_ok=True)
deadline = None
if len(sys.argv) > 1:
    hh, mm = sys.argv[1].split(':')
    lt = time.localtime()
    deadline = time.mktime((lt.tm_year, lt.tm_mon, lt.tm_mday, int(hh), int(mm), 0, 0, 0, -1))


def group_rss(pgid):
    try:
        out = subprocess.run(['ps', '-axo', 'pgid=,rss='], capture_output=True, text=True).stdout
    except Exception:
        return 0
    tot = 0
    for ln in out.splitlines():
        p = ln.split()
        if len(p) == 2 and p[0] == str(pgid):
            tot += int(p[1])
    return tot


def take():
    with lock:
        if deadline and time.time() > deadline:
            return None
        names = sorted(n for n in os.listdir(PEND) if n.endswith('.sh'))
        if not names:
            return None
        n = names[0]
        os.rename(os.path.join(PEND, n), os.path.join(RUN, n))
        return n


def work(wid):
    idle = 0
    while True:
        if os.path.exists(os.path.join(HERE, 'jobs', 'STOP')):
            return
        if deadline and time.time() > deadline:
            return
        n = take()
        if n is None:
            time.sleep(2)
            continue
        path = os.path.join(RUN, n)
        tmo = 600
        with open(path) as f:
            first = f.readline()
        if first.startswith('# timeout='):
            tmo = int(first.split('=')[1])
        t0 = time.time()
        p = subprocess.Popen(['/bin/sh', path], cwd=HERE, start_new_session=True,
                             stdout=open(os.path.join(HERE, 'logs', n + '.out'), 'w'), stderr=subprocess.STDOUT)
        status, peak = 'ok', 0
        while True:
            try:
                p.wait(timeout=3)
                break
            except subprocess.TimeoutExpired:
                pass
            r = group_rss(p.pid)
            peak = max(peak, r)
            if r > LIMIT_KB:
                status = 'stopped: passed 2 GB (%d kB)' % r
            elif time.time() - t0 > tmo:
                status = 'stopped: time limit %d s' % tmo
            if status != 'ok':
                try:
                    os.killpg(p.pid, signal.SIGKILL)
                except Exception:
                    pass
                p.wait()
                break
        rec = dict(job=n, status=status, rc=p.returncode, seconds=round(time.time() - t0, 1), peak_rss_kb=peak,
                   started=time.strftime('%H:%M:%S', time.localtime(t0)), ended=time.strftime('%H:%M:%S'))
        with open(os.path.join(DONE, n + '.json'), 'w') as f:
            json.dump(rec, f)
        os.rename(path, os.path.join(DONE, n))
        with lock:
            with open(os.path.join(HERE, 'jobs', 'LOG.txt'), 'a') as f:
                f.write('%s %-48s %-28s rc=%s %7.1fs peak %d kB\n'
                        % (rec['ended'], n, status, p.returncode, rec['seconds'], peak))


ths = [threading.Thread(target=work, args=(i,)) for i in range(WORKERS)]
for t in ths:
    t.start()
for t in ths:
    t.join()
