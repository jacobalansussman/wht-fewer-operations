/* harness.c -- check and time Walsh-Hadamard transforms of the form  void f(T *buf, int log_n).
 *
 *   ./harness list
 *   ./harness check [-t float|double|both] [-k KMIN KMAX] [-v name,name,...]
 *   ./harness time  [-t float|double|both] [-k KMIN KMAX] [-v name,name,...]
 *                   [-r REPEATS] [-l SECONDS] [-S PERCENT] [-H] [-P]
 *
 * The variants are listed in variants.c.  The first of each list is FFHT.
 *
 * CHECK.  For every size 2^k: an input of random integers; FFHT's output is compared with the
 * definition in 64-bit integers (k <= 12, n^2 operations) and with FFHT on an array that is not
 * aligned; then every other variant is compared with FFHT's output.  Equality must be exact,
 * number for number; an "up to scale" variant is multiplied by its power of two first.  The
 * program ends with exit code 1 if anything differs.
 *
 * TIME.  Run it pinned:  taskset -c CPU ./harness time ...   (it refuses otherwise; -P overrides).
 * For every type and size, on one array of 2^k numbers aligned to 64 bytes:
 *
 *   one loop of a variant  =  G groups; a group = copy the input back, then R transforms in
 *                             place, one after the other, on the same array;
 *   one repeat             =  one loop of every variant, one variant after the other (the order
 *                             turns by one place with every repeat);
 *   REPEATS repeats (default 9) after one calibration run that also warms up.
 *
 * G is chosen for each variant so that its loop takes SECONDS (default 0.25); a loop that comes
 * out shorter than 0.8 * SECONDS is run again, longer, and is not counted.  R is the same for all
 * variants of a size.  The copy is needed because two transforms multiply the data
 * by n: R is at most the number of transforms after which the numbers are still far inside the
 * range of the type (the input is -1, 0 or 1; no infinity, no NaN and no denormal number ever
 * occurs).  Where a group is long (200 microseconds or more for the fastest variant) the clock
 * is stopped during the copy ("reset=untimed").  Where it is shorter the copy is inside the
 * timed loop ("reset=timed"), for every variant alike, and the line of the variant "empty" (a
 * function that does nothing, run through the same loop) says how much the copy, the loop and
 * the call cost.  net = the variant's time minus the best time of "empty".
 *
 * Output, one line per variant (T), per size:
 *   min, med, max   nanoseconds per point for one transform, on the wall clock: the best, the
 *                   median and the worst of the repeats
 *   net_min, net_med   the same minus the best "empty" time
 *   spread_med_pct  (med - min) / min in per cent; spread_max_pct likewise with max
 *   ns_per_transform_min   min times 2^k
 *   G, R            the loop as it was last run
 *   loop_s_min      the seconds of the shortest loop that was counted.  A loop shorter than
 *                   0.8 * SECONDS (0.2 s with the default) is not counted: it is made longer and
 *                   run again, and "redone" says how often that happened
 *   ivcsw           how often the system took the processor away during this variant's loops
 * Line B (before) and line A (after) give the conditions: the processor, its hyper-thread
 * sibling, how busy both were during the size (from /proc/stat), and the load average.
 *
 * A second thread on the same core makes a loop up to twice as slow.  So a size is not kept when
 * the sibling was busy for more than PERCENT (default 25) of its time: a line D says so, the
 * process pins itself to the processor whose core is the least busy at that moment, and the size
 * is timed again, up to 4 attempts; the last attempt is kept whatever happened, and its line A
 * shows how busy the sibling was.  (Runs 1 and 2 of the baseline were made before this rule
 * existed; their lines A show a sibling busy for 4 to 36 per cent.)
 */
#define _GNU_SOURCE
#include <math.h>
#include <sched.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/resource.h>
#include <time.h>
#include <unistd.h>
#include "variants.h"

#ifndef HARNESS_FLAGS
#define HARNESS_FLAGS "?"
#endif
#ifndef FFHT_COMMIT
#define FFHT_COMMIT "?"
#endif
#ifndef FFHT_FLAGS
#define FFHT_FLAGS "?"
#endif
#ifndef NAIVE_FLAGS
#define NAIVE_FLAGS "?"
#endif

void harness_empty_f(float *buf, int log_n);      /* empty.c */
void harness_empty_d(double *buf, int log_n);

static volatile double sink;
static int my_cpu = -1, sibling_cpu = -1;
static double loop_seconds[64];
static double sibling_limit = 25.0;     /* per cent; option -S */
static const int max_attempts = 4;

static double now(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return (double)t.tv_sec + 1e-9 * (double)t.tv_nsec;
}

static long ivcsw(void)
{
    struct rusage u;
    getrusage(RUSAGE_SELF, &u);
    return u.ru_nivcsw;
}

static void loadavg(char *s, size_t len)
{
    FILE *f = fopen("/proc/loadavg", "r");
    double a = 0, b = 0, c = 0;
    if (f) { if (fscanf(f, "%lf %lf %lf", &a, &b, &c) != 3) a = b = c = -1; fclose(f); }
    snprintf(s, len, "%.2f,%.2f,%.2f", a, b, c);
}

typedef struct { double busy, total, steal; } cpustat;

/* cpu = -1: all processors together */
static void read_stat(int cpu, cpustat *s)
{
    char want[32], line[512];
    s->busy = s->total = s->steal = 0;
    if (cpu >= 0) snprintf(want, sizeof want, "cpu%d ", cpu); else snprintf(want, sizeof want, "cpu ");
    FILE *f = fopen("/proc/stat", "r");
    if (!f) return;
    while (fgets(line, sizeof line, f)) {
        if (strncmp(line, want, strlen(want)) != 0) continue;
        double v[10] = {0};
        sscanf(line + strlen(want), "%lf %lf %lf %lf %lf %lf %lf %lf", &v[0], &v[1], &v[2], &v[3], &v[4], &v[5], &v[6], &v[7]);
        for (int i = 0; i < 8; i++) s->total += v[i];
        s->busy = s->total - v[3] - v[4];          /* all but idle and iowait */
        s->steal = v[7];
        break;
    }
    fclose(f);
}

static double busy_pct(const cpustat *a, const cpustat *b)
{
    const double d = b->total - a->total;
    return d > 0 ? 100.0 * (b->busy - a->busy) / d : 0.0;
}

static double steal_pct(const cpustat *a, const cpustat *b)
{
    const double d = b->total - a->total;
    return d > 0 ? 100.0 * (b->steal - a->steal) / d : 0.0;
}

/* the other hyper-thread of the core of this processor, or -1 */
static int sibling_of(int cpu)
{
    char path[128];
    int a = -1, b = -1;
    snprintf(path, sizeof path, "/sys/devices/system/cpu/cpu%d/topology/thread_siblings_list", cpu);
    FILE *f = fopen(path, "r");
    if (f) { if (fscanf(f, "%d%*[,-]%d", &a, &b) < 1) a = b = -1; fclose(f); }
    return (a == cpu) ? b : a;
}

/* Look at every processor for one second (this thread sleeps meanwhile), take the one whose core,
 * both hyper-threads together, was the least busy, and pin this process to it. */
static void repin_to_quietest_core(void)
{
    enum { MAXC = 256 };
    static cpustat a[MAXC], b[MAXC];
    int n = (int)sysconf(_SC_NPROCESSORS_ONLN);
    if (n > MAXC) n = MAXC;
    for (int c = 0; c < n; c++) read_stat(c, &a[c]);
    sleep(1);
    for (int c = 0; c < n; c++) read_stat(c, &b[c]);
    int best = my_cpu;
    double bv = 1e30;
    for (int c = 0; c < n; c++) {
        const int s = sibling_of(c);
        const double v = busy_pct(&a[c], &b[c]) + ((s >= 0 && s < n) ? busy_pct(&a[s], &b[s]) : 0.0);
        if (v < bv) { bv = v; best = c; }
    }
    cpu_set_t set;
    CPU_ZERO(&set);
    CPU_SET(best, &set);
    if (sched_setaffinity(0, sizeof set, &set) == 0) {
        my_cpu = best;
        sibling_cpu = sibling_of(best);
    }
    printf("# pinned again: processor %d; its hyper-thread sibling %d (the two were busy for %.1f %% of one second, together)\n",
           my_cpu, sibling_cpu, bv);
    fflush(stdout);
}

/* sel = NULL: every variant; else a list "a,b,c" */
static int selected(const char *sel, const char *name)
{
    if (!sel) return 1;
    const size_t L = strlen(name);
    for (const char *p = sel; *p;) {
        const char *q = strchr(p, ',');
        const size_t len = q ? (size_t)(q - p) : strlen(p);
        if (len == L && strncmp(p, name, L) == 0) return 1;
        if (!q) break;
        p = q + 1;
    }
    return 0;
}

#define T float
#define SUF f
#define TYPENAME "float"
#define VARIANT variant_f
#define VARS variants_f
#define NVARS n_variants_f
#define EXP_SAFE 120
#define EMPTY harness_empty_f
#include "engine.inc"
#undef T
#undef SUF
#undef TYPENAME
#undef VARIANT
#undef VARS
#undef NVARS
#undef EXP_SAFE
#undef EMPTY

#define T double
#define SUF d
#define TYPENAME "double"
#define VARIANT variant_d
#define VARS variants_d
#define NVARS n_variants_d
#define EXP_SAFE 1000
#define EMPTY harness_empty_d
#include "engine.inc"

static void header(const char *mode)
{
    char host[128] = "?", la[64];
    time_t t = time(NULL);
    char when[64];
    gethostname(host, sizeof host);
    strftime(when, sizeof when, "%Y-%m-%d %H:%M:%S UTC", gmtime(&t));
    loadavg(la, sizeof la);
    printf("# harness %s; %s; host %s; load %s\n", mode, when, host, la);
    printf("# compiler: gcc %s\n", __VERSION__);
    printf("# harness, variants.c and our plain C built with: %s\n", HARNESS_FLAGS);
    printf("# naive.c built with: %s\n", NAIVE_FLAGS);
    printf("# FFHT commit %s; its fht.o built by its own Makefile with: %s\n", FFHT_COMMIT, FFHT_FLAGS);
}

static void usage(void)
{
    fprintf(stderr,
            "usage: harness list\n"
            "       harness check [-t float|double|both] [-k KMIN KMAX] [-v a,b,...]\n"
            "       taskset -c CPU harness time [-t ...] [-k KMIN KMAX] [-v a,b,...] [-r REPEATS] [-l SECONDS] [-S PERCENT] [-H] [-P]\n"
            "       -H: ask for 2 MB pages (madvise) for arrays of 2 MB or more   -P: run although not pinned\n"
            "       -S: time a size again when the hyper-thread sibling was busy for more than PERCENT of it (default 25; 100 = never)\n");
    exit(2);
}

int main(int argc, char **argv)
{
    if (argc < 2) usage();
    const char *mode = argv[1];
    const char *type = "both", *sel = NULL;
    int kmin = 3, kmax = 20, repeats = 9, huge = 0, nopin = 0, kset = 0;
    double loop_s = 0.25;
    for (int i = 2; i < argc; i++) {
        if (!strcmp(argv[i], "-t") && i + 1 < argc) type = argv[++i];
        else if (!strcmp(argv[i], "-k") && i + 2 < argc) { kmin = atoi(argv[++i]); kmax = atoi(argv[++i]); kset = 1; }
        else if (!strcmp(argv[i], "-v") && i + 1 < argc) sel = argv[++i];
        else if (!strcmp(argv[i], "-r") && i + 1 < argc) repeats = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-l") && i + 1 < argc) loop_s = atof(argv[++i]);
        else if (!strcmp(argv[i], "-S") && i + 1 < argc) sibling_limit = atof(argv[++i]);
        else if (!strcmp(argv[i], "-H")) huge = 1;
        else if (!strcmp(argv[i], "-P")) nopin = 1;
        else usage();
    }
    const int do_f = !strcmp(type, "float") || !strcmp(type, "both");
    const int do_d = !strcmp(type, "double") || !strcmp(type, "both");
    if (!do_f && !do_d) usage();
    if (kmin < 0 || kmax > 30 || kmin > kmax) { fprintf(stderr, "harness: sizes are 2^0 .. 2^30\n"); return 2; }
    if (repeats < 1 || repeats > 127) { fprintf(stderr, "harness: 1 to 127 repeats\n"); return 2; }

    if (!strcmp(mode, "list")) {
        header("list");
        for (int v = 0; v < n_variants_f; v++)
            printf("float  %-10s %s  2^%d..2^%d  %s\n", variants_f[v].name, variants_f[v].scale_log2 ? "up to scale" : "exact      ",
                   variants_f[v].kmin, variants_f[v].kmax, variants_f[v].what);
        for (int v = 0; v < n_variants_d; v++)
            printf("double %-10s %s  2^%d..2^%d  %s\n", variants_d[v].name, variants_d[v].scale_log2 ? "up to scale" : "exact      ",
                   variants_d[v].kmin, variants_d[v].kmax, variants_d[v].what);
        return 0;
    }
    if (!strcmp(mode, "check")) {
        if (!kset) { kmin = 1; kmax = 20; }
        header("check");
        int bad = 0;
        if (do_f) bad += check_f(kmin, kmax, sel);
        if (do_d) bad += check_d(kmin, kmax, sel);
        printf("# check: %s (%d failing lines)\n", bad ? "FAILED" : "all equal", bad);
        return bad ? 1 : 0;
    }
    if (!strcmp(mode, "time")) {
        cpu_set_t set;
        CPU_ZERO(&set);
        sched_getaffinity(0, sizeof set, &set);
        my_cpu = sched_getcpu();
        if (CPU_COUNT(&set) != 1) {
            if (!nopin) { fprintf(stderr, "harness: not pinned to one processor; run under taskset -c CPU (or give -P)\n"); return 2; }
        }
        sibling_cpu = sibling_of(my_cpu);
        header("time");
        printf("# pinned: %s; processor %d; its hyper-thread sibling %d; processors allowed %d\n",
               CPU_COUNT(&set) == 1 ? "yes" : "NO", my_cpu, sibling_cpu, CPU_COUNT(&set));
        printf("# times: nanoseconds per point for one transform, wall clock; %d repeats; a loop aims at %.2f s and counts only from %.2f s\n",
               repeats, loop_s, 0.8 * loop_s);
        printf("# a size is timed again (up to %d attempts) when the hyper-thread sibling was busy for more than %.0f %% of it\n",
               max_attempts, sibling_limit);
        fflush(stdout);
        if (do_f) timing_f(kmin, kmax, repeats, loop_s, sel, huge);
        if (do_d) timing_d(kmin, kmax, repeats, loop_s, sel, huge);
        printf("# done\n");
        return 0;
    }
    usage();
    return 2;
}
