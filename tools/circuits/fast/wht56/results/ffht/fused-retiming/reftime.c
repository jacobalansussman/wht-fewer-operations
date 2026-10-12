/* reftime.c -- a second timer, written separately from the harness, for the re-timing of the fused form.
 *   reftime SIBLING k,k,.. name,name,..
 * For each size: the variants take turns inside one process; 9 repeats; each repeat of a variant is
 * G groups of (copy the input back, untimed; then R transforms in place, timed with the cycle
 * counter).  R is small enough that floats cannot overflow.  Figures: ns per point per transform. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <time.h>
#include <sched.h>
#include <x86intrin.h>
#include "fht.h"
#include "whtf.h"

typedef void (*fn)(float *, int);
static void ffht(float *b, int k) { (void)fht_float(b, k); }
void O2_wht_f_Tp(float *, int);  void O2_wht_f_G19p(float *, int);
void GEN_wht_f_Tp(float *, int); void GEN_wht_f_G19p(float *, int);
/* 32-bit integers through the same loop: the array is the same memory, read as int32 (the time of
 * integer additions does not depend on the values) */
static void iT(float *b, int k) { wht_i_Tp((int32_t *)(void *)b, k); }
static void iG19s(float *b, int k) { wht_i_G19p((int32_t *)(void *)b, k); }
static void sT(float *b, int k) { wht_s_T((int32_t *)(void *)b, k); }
static void sG19(float *b, int k) { wht_s_G19((int32_t *)(void *)b, k); }
static const struct { const char *name; fn f; } ALL[] = {
    {"ffht", ffht}, {"T", wht_f_Tp}, {"G19", wht_f_G19p}, {"G19a", wht_f_G19ap},
    {"T_O2", O2_wht_f_Tp}, {"G19_O2", O2_wht_f_G19p}, {"T_gen", GEN_wht_f_Tp}, {"G19_gen", GEN_wht_f_G19p},
    {"Tnp", wht_f_T}, {"G19np", wht_f_G19},
    {"iT", iT}, {"iG19s", iG19s}, {"sT", sT}, {"sG19", sG19},
};
#define NALL ((int)(sizeof ALL / sizeof ALL[0]))
#define REPS 9
#define TARGET 0.21

static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + 1e-9 * t.tv_nsec; }

static uint64_t loop(fn f, float *buf, const float *src, size_t bytes, int k, long G, long R, long M)
{
    /* M = 1: the same array again and again (each transform reads what the one before wrote).
     * M > 1: M separate arrays side by side, one after the other, R rounds (MBUF in the environment). */
    const size_t n = (size_t)1 << k;
    uint64_t tot = 0;
    for (long g = 0; g < G; g++) {
        memcpy(buf, src, bytes * (size_t)M);
        const uint64_t t0 = __rdtsc();
        for (long r = 0; r < R; r++) for (long m = 0; m < M; m++) f(buf + (size_t)m * n, k);
        tot += __rdtsc() - t0;
    }
    return tot;
}

static void cpustat(int c, double *busy, double *total)
{
    FILE *f = fopen("/proc/stat", "r"); char line[512], tag[32]; snprintf(tag, sizeof tag, "cpu%d ", c);
    *busy = *total = 0;
    while (f && fgets(line, sizeof line, f)) if (!strncmp(line, tag, strlen(tag))) {
        double v[8] = {0}; sscanf(line + strlen(tag), "%lf %lf %lf %lf %lf %lf %lf %lf", v, v+1, v+2, v+3, v+4, v+5, v+6, v+7);
        for (int i = 0; i < 8; i++) *total += v[i];
        *busy = *total - v[3] - v[4];
    }
    if (f) fclose(f);
}
static int cmpd(const void *a, const void *b) { double x = *(const double *)a, y = *(const double *)b; return (x > y) - (x < y); }
static void loadavg(char *s, size_t n) { FILE *f = fopen("/proc/loadavg", "r"); s[0] = 0; if (f) { if (fgets(s, (int)n, f)) s[strcspn(s, "\n")] = 0; fclose(f); } }

int main(int argc, char **argv)
{
    if (argc < 4) { fprintf(stderr, "usage: reftime SIBLING k,k,.. name,name,..\n"); return 2; }
    const int sib = atoi(argv[1]);
    const long M = getenv("MBUF") ? atol(getenv("MBUF")) : 1;
    int ks[16], nk = 0, vi[16], nv = 0;
    for (char *t = strtok(argv[2], ","); t && nk < 16; t = strtok(NULL, ",")) ks[nk++] = atoi(t);
    for (char *t = strtok(argv[3], ","); t && nv < 16; t = strtok(NULL, ",")) {
        int j; for (j = 0; j < NALL; j++) if (!strcmp(ALL[j].name, t)) break;
        if (j == NALL) { fprintf(stderr, "unknown variant %s\n", t); return 2; }
        vi[nv++] = j;
    }
    const double w0 = now(); const uint64_t c0 = __rdtsc();
    static uint64_t ticks[16][16][REPS]; static long Gs[16], Rs[16]; static double sibbusy[16]; static int cpus[16];
    static char la[16][64];
    for (int a = 0; a < nk; a++) {
        const int k = ks[a]; const size_t n = (size_t)1 << k, bytes = n * sizeof(float);
        const size_t tot = (bytes * (size_t)M + 4095) / 4096 * 4096;
        float *src = aligned_alloc(4096, tot), *buf = aligned_alloc(4096, tot);
        if (!src || !buf) { fprintf(stderr, "no memory\n"); return 1; }
        uint64_t s = 0x9E3779B97F4A7C15ull ^ (uint64_t)k;
        for (size_t i = 0; i < n * (size_t)M; i++) { s ^= s << 13; s ^= s >> 7; s ^= s << 17; src[i] = (float)((int)(s % 3) - 1); }
        memcpy(buf, src, bytes * (size_t)M);
        long Rover = 200 / k - 1; if (Rover < 1) Rover = 1;
        /* calibrate: the fastest variant's time for one transform */
        double t1 = 1e30;
        for (int v = 0; v < nv; v++) {
            const double a1 = now(); (void)loop(ALL[vi[v]].f, buf, src, bytes, k, 1, 1, M); double d = (now() - a1) / M;
            if (d * Rover < 0.02) for (int w = 0; w < 3; w++) {     /* small sizes: a longer look */
                const double a0 = now(); (void)loop(ALL[vi[v]].f, buf, src, bytes, k, 1, Rover, M); const double e = (now() - a0) / (Rover * M);
                if (w == 0 || e < d) d = e;
            }
            if (d < t1) t1 = d;
        }
        long R, G;
        if (Rover * M * t1 >= TARGET) { R = (long)ceil(1.3 * TARGET / (M * t1)); if (R > Rover) R = Rover; G = 1;  /* 1.3: the first look can be slow; keeps the loop above 0.2 s */ }
        else { R = Rover; G = (long)ceil(TARGET / (R * M * t1)); }   /* M was missing here until 17:09 UTC: the loops of the separate-arrays runs before that were M times longer than needed */
        Gs[a] = G; Rs[a] = R;
        double b0, tt0, b1, tt1; cpustat(sib, &b0, &tt0);
        loadavg(la[a], sizeof la[a]);
        for (int r = 0; r < REPS; r++)
            for (int j = 0; j < nv; j++) { const int v = (j + r) % nv; ticks[a][v][r] = loop(ALL[vi[v]].f, buf, src, bytes, k, G, R, M); }
        cpustat(sib, &b1, &tt1);
        sibbusy[a] = tt1 > tt0 ? 100.0 * (b1 - b0) / (tt1 - tt0) : -1;
        cpus[a] = sched_getcpu();
        free(src); free(buf);
    }
    const double hz = (double)(__rdtsc() - c0) / (now() - w0);
    printf("# cycle counter: %.4f GHz against the monotonic clock over the run of %.1f s\n", hz / 1e9, now() - w0);
    for (int a = 0; a < nk; a++) {
        const int k = ks[a]; const double pts = (double)Gs[a] * Rs[a] * (double)M * (double)((size_t)1 << k);
        printf("S k=%d arrays=%ld bytes=%zu G=%ld R=%ld cpu=%d sibling=%d sibling_busy=%.0f%% loadavg_at_start=[%s]\n", k, M, ((size_t)4) << k, Gs[a], Rs[a], cpus[a], sib, sibbusy[a], la[a]);
        double ns[16][REPS], sorted[REPS];
        for (int v = 0; v < nv; v++) {
            double loopmin = 1e30;
            for (int r = 0; r < REPS; r++) { ns[v][r] = ticks[a][v][r] / hz * 1e9 / pts; sorted[r] = ns[v][r]; if (ticks[a][v][r] / hz < loopmin) loopmin = ticks[a][v][r] / hz; }
            qsort(sorted, REPS, sizeof(double), cmpd);
            printf("V k=%d %-8s min=%.4f med=%.4f max=%.4f ns/point  shortest_loop=%.3fs  all:", k, ALL[vi[v]].name, sorted[0], sorted[REPS / 2], sorted[REPS - 1], loopmin);
            for (int r = 0; r < REPS; r++) printf(" %.4f", ns[v][r]);
            printf("\n");
        }
        for (int v = 0; v < nv; v++) for (int u = 0; u < nv; u++) {
            if (u == v) continue;
            const char *nu = ALL[vi[u]].name, *nvn = ALL[vi[v]].name;
            int want = 0;
            if (!strcmp(nvn, "G19") && (!strcmp(nu, "T") || !strcmp(nu, "ffht"))) want = 1;
            if (!strcmp(nvn, "G19a") && !strcmp(nu, "T")) want = 1;
            if (!strcmp(nvn, "T") && !strcmp(nu, "ffht")) want = 1;
            if (!strcmp(nvn, "G19_O2") && !strcmp(nu, "T_O2")) want = 1;
            if (!strcmp(nvn, "G19_gen") && !strcmp(nu, "T_gen")) want = 1;
            if (!strcmp(nvn, "G19np") && !strcmp(nu, "Tnp")) want = 1;
            if (!strcmp(nvn, "iG19s") && !strcmp(nu, "iT")) want = 1;
            if (!strcmp(nvn, "sG19") && !strcmp(nu, "sT")) want = 1;
            if (!want) continue;
            double q[REPS], mv = 1e30, mu = 1e30, sv[REPS], su[REPS];
            for (int r = 0; r < REPS; r++) { q[r] = ns[v][r] / ns[u][r]; sv[r] = ns[v][r]; su[r] = ns[u][r]; if (ns[v][r] < mv) mv = ns[v][r]; if (ns[u][r] < mu) mu = ns[u][r]; }
            qsort(q, REPS, sizeof(double), cmpd); qsort(sv, REPS, sizeof(double), cmpd); qsort(su, REPS, sizeof(double), cmpd);
            printf("P k=%d %s/%s best/best=%.4f med/med=%.4f  repeat-by-repeat: min=%.4f med=%.4f max=%.4f\n", k, nvn, nu, mv / mu, sv[REPS / 2] / su[REPS / 2], q[0], q[REPS / 2], q[REPS - 1]);
        }
    }
    return 0;
}
