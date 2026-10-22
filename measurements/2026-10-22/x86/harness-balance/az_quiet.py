#!/usr/bin/env python3
"""az_quiet.py -- is this Linux machine quiet enough to time on?  (22 Oct 2026)

Usage:  python3 -I az_quiet.py --label NAME [--cpus 0,1] [--pct 5] [--window 3] [--wait 180] [--log out/quiet.log]

Measures for WINDOW seconds, from /proc/stat (every CPU) and /proc/<pid>/stat (every process):
  1. any process OUTSIDE this job's session using more than PCT % of one core  -> busy;
  2. any CPU the timing will use (--cpus; default: every CPU) more than PCT % busy -> busy;
  3. the whole machine busier than max(0.3, PCT/100 x nproc) cores (catches swarms of short processes such as an
     apt/pip install, which rule 1 can miss)                                       -> busy.
"busy" counts user + nice + system + irq + softirq + steal; idle and iowait are idle.  Steal (time the hypervisor
gave this VM's CPUs to someone else) therefore counts as busy, and above 2 % it is also printed as a warning.  Processes of this job's own session
(the job's shell, tee, tmux pane) are excluded from rule 1; the job is expected to be idle while this runs.
Re-measures every 10 s until quiet or WAIT seconds have passed.  Exit 0 = quiet, 6 = busy, 2 = not Linux.
Every measurement is appended to --log (one block per measurement) and printed.
Only the standard library; reads /proc only.
"""
import argparse, os, sys, time

def cpu_times():
    out = {}
    with open('/proc/stat') as f:
        for line in f:
            if not line.startswith('cpu'):
                break
            p = line.split()
            v = [int(x) for x in p[1:9]] + [0] * max(0, 8 - len(p[1:9]))
            out[p[0]] = v          # user nice system idle iowait irq softirq steal
    return out

def proc_times():
    out = {}
    for d in os.listdir('/proc'):
        if not d.isdigit():
            continue
        try:
            with open('/proc/%s/stat' % d) as f:
                s = f.read()
        except OSError:
            continue
        r = s.rfind(')')
        comm = s[s.find('(') + 1:r]
        f2 = s[r + 2:].split()
        # after ')': state ppid pgrp session tty tpgid flags minflt cminflt majflt cmajflt utime stime
        try:
            out[int(d)] = (comm, int(f2[3]), int(f2[11]) + int(f2[12]))
        except (IndexError, ValueError):
            continue
    return out

def cmdline(pid):
    try:
        with open('/proc/%d/cmdline' % pid, 'rb') as f:
            return f.read().replace(b'\0', b' ').decode('utf-8', 'replace').strip()[:120]
    except OSError:
        return ''

def measure(window, cpus, pct, mysid):
    hz = os.sysconf('SC_CLK_TCK')
    c0, p0, t0 = cpu_times(), proc_times(), time.time()
    time.sleep(window)
    c1, p1, t1 = cpu_times(), proc_times(), time.time()
    dt = t1 - t0
    names = sorted((k for k in c1 if k != 'cpu'), key=lambda k: int(k[3:]))
    per = {}
    steal = 0.0
    for k in names:
        a, b = c0.get(k), c1[k]
        if a is None:
            continue
        d = [y - x for x, y in zip(a, b)]
        tot = sum(d)
        busy = tot - d[3] - d[4]
        per[k] = 100.0 * busy / tot if tot > 0 else 0.0
        steal += d[7]
    a, b = c0['cpu'], c1['cpu']
    d = [y - x for x, y in zip(a, b)]
    tot = sum(d)
    ncpu = len(names) or 1
    total_cores = (tot - d[3] - d[4]) / tot * ncpu if tot > 0 else 0.0
    steal_pct = 100.0 * d[7] / tot if tot > 0 else 0.0
    procs = []
    for pid, (comm, sid, t) in p1.items():
        if pid not in p0:
            continue
        use = 100.0 * (t - p0[pid][2]) / hz / dt
        procs.append((use, pid, comm, sid))
    procs.sort(reverse=True)
    reasons = []
    for use, pid, comm, sid in procs:
        if use > pct and sid != mysid and pid != os.getpid():
            reasons.append('process %d (%s) at %.1f %% of a core: %s' % (pid, comm, use, cmdline(pid)))
    want = ['cpu%d' % c for c in cpus] if cpus else list(per)
    for k in want:
        if k in per and per[k] > pct:
            reasons.append('%s %.1f %% busy' % (k, per[k]))
    lim = max(0.3, pct / 100.0 * ncpu)
    if total_cores > lim:
        reasons.append('whole machine %.2f cores busy (limit %.2f)' % (total_cores, lim))
    top = ['%6.1f %%  pid %-7d %-16s %s' % (u, pid, comm, '(this job)' if sid == mysid else '')
           for u, pid, comm, sid in procs[:6]]
    return reasons, total_cores, per, steal_pct, top, ncpu

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--label', default='timing')
    ap.add_argument('--cpus', default='')
    ap.add_argument('--pct', type=float, default=float(os.environ.get('QUIET_PCT', '5')))
    ap.add_argument('--window', type=float, default=3.0)
    ap.add_argument('--wait', type=float, default=float(os.environ.get('QUIET_WAIT', '180')))
    ap.add_argument('--log', default='out/quiet.log')
    a = ap.parse_args()
    if not os.path.exists('/proc/stat'):
        print('az_quiet: no /proc/stat (not Linux): cannot judge; refusing'); return 2
    cpus = []
    for x in a.cpus.replace(' ', ',').split(','):      # accepts 3 / 3,7 / 2-3 (sysfs sibling lists)
        x = x.strip()
        if not x:
            continue
        if '-' in x:
            lo, hi = x.split('-', 1); cpus += list(range(int(lo), int(hi) + 1))
        else:
            cpus.append(int(x))
    cpus = sorted(set(cpus))
    mysid = os.getsid(0)
    end = time.time() + a.wait
    while True:
        reasons, tc, per, steal, top, ncpu = measure(a.window, cpus, a.pct, mysid)
        verdict = 'QUIET' if not reasons else 'BUSY'
        lines = ['== az_quiet %s %s: %s over %.0f s; whole machine %.2f of %d cores busy; steal %.1f %%; load %s'
                 % (time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()), a.label, verdict, a.window, tc, ncpu, steal,
                    open('/proc/loadavg').read().split()[0:3])]
        if cpus:
            lines.append('   CPUs the timing uses: ' + ', '.join('cpu%d %.1f %%' % (c, per.get('cpu%d' % c, -1)) for c in cpus))
        lines += ['   top: ' + t for t in top]
        lines += ['   BUSY because ' + r for r in reasons[:8]]
        if steal > 2.0:
            lines.append('   WARNING: steal %.1f %%: the hypervisor is taking CPU time from this VM; timings are suspect' % steal)
        txt = '\n'.join(lines)
        print(txt, flush=True)
        try:
            os.makedirs(os.path.dirname(a.log) or '.', exist_ok=True)
            with open(a.log, 'a') as f:
                f.write(txt + '\n')
        except OSError:
            pass
        if not reasons:
            return 0
        if time.time() + 10 > end:
            return 6
        time.sleep(10)

if __name__ == '__main__':
    sys.exit(main())
