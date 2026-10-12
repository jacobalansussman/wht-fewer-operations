/* engine.inc -- the check and the timing for one number type.  harness.c includes this file
 * twice, with these macros set:
 *
 *   T          float or double
 *   SUF        f or d
 *   TYPENAME   "float" or "double"
 *   VARIANT    variant_f or variant_d
 *   VARS, NVARS   the list and its length
 *   EXP_SAFE   a power of two that T holds with room to spare: 120 for float, 1000 for double
 *   EMPTY      the function that does nothing (harness_empty_f or harness_empty_d)
 */
#define CAT2(a, b) a##_##b
#define CAT(a, b) CAT2(a, b)

static T *CAT(alloc, SUF)(size_t n, int hugepages)
{
    size_t bytes = n * sizeof(T);
    size_t align = 64;
    if (hugepages && bytes >= ((size_t)2 << 20)) align = (size_t)2 << 20;
    bytes = (bytes + align - 1) / align * align;
    T *p = aligned_alloc(align, bytes);
    if (!p) { fprintf(stderr, "harness: no memory for %zu bytes\n", bytes); exit(2); }
#ifdef MADV_HUGEPAGE
    if (hugepages && align > 64) madvise(p, bytes, MADV_HUGEPAGE);
#endif
    memset(p, 0, bytes);                 /* touch every page now, outside every timing */
    return p;
}

/* integer-valued input: every number is an integer between -amp and amp */
static void CAT(fill, SUF)(T *x, size_t n, int amp, uint64_t seed)
{
    uint64_t s = seed * 0x9E3779B97F4A7C15ull + 0xD1B54A32D192ED03ull;
    for (size_t i = 0; i < n; i++) {
        s ^= s << 13; s ^= s >> 7; s ^= s << 17;
        x[i] = (T)((int)((s >> 20) % (uint64_t)(2 * amp + 1)) - amp);
    }
}

/* ------------------------------------------------------------------ check ---- */

static int CAT(check, SUF)(int kmin, int kmax, const char *sel)
{
    int failures = 0;
    for (int k = kmin; k <= kmax; k++) {
        const size_t n = (size_t)1 << k;
        /* Small enough that every sum, and every half of a sum, is held exactly: float holds
         * integers below 2^24, double below 2^53.  The check is the equality itself. */
        const int amp = AMP(k);       /* style-fused: the bound is a macro per type */
        T *src = CAT(alloc, SUF)(n, 0);
        T *ref = CAT(alloc, SUF)(n, 0);
        T *buf = CAT(alloc, SUF)(n + 16, 0);
        CAT(fill, SUF)(src, n, amp, (uint64_t)(1000 * k + (int)sizeof(T)));

        if (k < VARS[0].kmin || k > VARS[0].kmax) {
            printf("C type=%s k=%d variant=%s SKIPPED (size not accepted by the reference)\n", TYPENAME, k, VARS[0].name);
            free(src); free(ref); free(buf);
            continue;
        }
        memcpy(ref, src, n * sizeof(T));
        VARS[0].f(ref, k);

        /* the reference against the definition, in 64-bit integers: n^2 operations */
        if (k <= 12) {
            size_t bad = 0;
            for (size_t j = 0; j < n; j++) {
                int64_t s = 0;
                for (size_t i = 0; i < n; i++) {
                    const int64_t xi = (int64_t)src[i];
                    s += (__builtin_popcountll((unsigned long long)(i & j)) & 1) ? -xi : xi;
                }
                if ((T)s != ref[j]) bad++;
            }
            printf("C type=%s k=%d variant=%s against=definition amp=%d mismatches=%zu %s\n",
                   TYPENAME, k, VARS[0].name, amp, bad, bad ? "FAIL" : "OK");
            if (bad) failures++;
        }
        /* the reference on an array that is NOT aligned: one number past a 64-byte boundary */
        {
            T *u = buf + 1;
            memcpy(u, src, n * sizeof(T));
            VARS[0].f(u, k);
            size_t bad = 0;
            for (size_t i = 0; i < n; i++) if (u[i] != ref[i]) bad++;
            printf("C type=%s k=%d variant=%s against=itself-unaligned(address%%64=%d) mismatches=%zu %s\n",
                   TYPENAME, k, VARS[0].name, (int)((uintptr_t)u % 64), bad, bad ? "FAIL" : "OK");
            if (bad) failures++;
        }
        for (int v = 1; v < NVARS; v++) {
            if (!selected(sel, VARS[v].name)) continue;
            if (k < VARS[v].kmin || k > VARS[v].kmax) continue;
            memcpy(buf, src, n * sizeof(T));
            VARS[v].f(buf, k);
            const int s = VARS[v].scale_log2 ? VARS[v].scale_log2(k) : 0;
            size_t bad = 0;
            double worst = 0;
            for (size_t i = 0; i < n; i++) {
                const double got = ldexp((double)buf[i], s);     /* exact: a power of two */
                const double d = fabs(got - (double)ref[i]);
                if (!(d == 0)) { bad++; if (d > worst || d != d) worst = d; }
            }
            printf("C type=%s k=%d variant=%s against=%s amp=%d scale_log2=%d mismatches=%zu maxdiff=%g %s\n",
                   TYPENAME, k, VARS[v].name, VARS[0].name, amp, s, bad, worst, bad ? "FAIL" : "OK");
            if (bad) failures++;
        }
        fflush(stdout);
        free(src); free(ref); free(buf);
    }
    return failures;
}

/* ----------------------------------------------------------------- timing ---- */

/* G groups; each group: copy the input back (the "reset"), then R transforms in place.
 * reset_timed = 1: one clock interval around everything (the resets are inside).
 * reset_timed = 0: the clock runs only while the R transforms run.
 * do_reset = 0: no copy at all (used for the empty function when the resets are not timed).
 * Returns seconds on the wall clock. */
static __attribute__((noinline, noclone)) double
CAT(run_loop, SUF)(void (*f)(T *, int), T *buf, const T *src, size_t bytes, int k,
                   long G, long R, int reset_timed, int do_reset)
{
    double t = 0;
    if (reset_timed) {
        const double t0 = now();
        for (long g = 0; g < G; g++) {
            memcpy(buf, src, bytes);
            for (long r = 0; r < R; r++) f(buf, k);
        }
        t = now() - t0;
    } else {
        for (long g = 0; g < G; g++) {
            if (do_reset) memcpy(buf, src, bytes);
            const double t0 = now();
            for (long r = 0; r < R; r++) f(buf, k);
            t += now() - t0;
        }
    }
    sink += (double)buf[0];
    return t;
}

static int CAT(cmp_double, SUF)(const void *a, const void *b)
{
    const double x = *(const double *)a, y = *(const double *)b;
    return (x > y) - (x < y);
}

static void CAT(timing, SUF)(int kmin, int kmax, int repeats, double loop_s, const char *sel, int hugepages)
{
    for (int k = kmin; k <= kmax; k++) {
        const size_t n = (size_t)1 << k;
        const size_t bytes = n * sizeof(T);
        T *src = CAT(alloc, SUF)(n, hugepages);
        T *buf = CAT(alloc, SUF)(n, hugepages);
        CAT(fill, SUF)(src, n, 1, (uint64_t)(77 * k + (int)sizeof(T)));
        memcpy(buf, src, bytes);

        /* the variants of this size; slot nv is the empty function */
        int idx[64], nv = 0;
        for (int v = 0; v < NVARS && nv < 63; v++)
            if (selected(sel, VARS[v].name) && k >= VARS[v].kmin && k <= VARS[v].kmax) idx[nv++] = v;
        if (nv == 0) { free(src); free(buf); continue; }

        /* Applying a transform twice multiplies the data by n, so the numbers grow.  R_over is
         * the largest even number of transforms after which nothing has left the range of T:
         * starting below 1 in size, after R transforms the size is below n^(R/2) <= 2^EXP_SAFE. */
        long R_over = 2 * (long)(EXP_SAFE / (k > 0 ? k : 1));
        if (R_over < 2) R_over = 2;

        /* A size is timed again, on the quietest core at that moment, when the hyper-thread sibling
         * of the timed processor was busy for more than sibling_limit per cent of the time. */
        for (int attempt = 1;; attempt++) {

        /* calibration (also the warm-up): seconds for one transform, each variant */
        double t1[64], t1min = 1e30;
        for (int a = 0; a < nv; a++) {
            long m = 1;
            double t;
            for (;;) {
                const long R = m < R_over ? m : R_over;
                const long G = (m + R - 1) / R;
                t = CAT(run_loop, SUF)(VARS[idx[a]].f, buf, src, bytes, k, G, R, 0, 1) / (double)(G * R);
                if (t * (double)m >= 0.02 || m >= ((long)1 << 40)) break;
                m *= 2;
            }
            t1[a] = t;
            if (t < t1min) t1min = t;
        }
        /* one R for all variants of this size; the resets are timed only when a group of
         * R_over transforms of the fastest variant is too short to stop the clock around it */
        const int reset_timed = ((double)R_over * t1min < 200e-6);
        long R = R_over;
        if (!reset_timed) {
            const long need = (long)ceil(loop_s / t1min);
            if (need < R) R = need < 1 ? 1 : need;
        }
        long G[64];
        for (int a = 0; a < nv; a++) {
            G[a] = (long)ceil(loop_s / ((double)R * t1[a]));
            if (G[a] < 1) G[a] = 1;
        }
        /* the empty function: same loop when the resets are timed; else no resets, one group */
        long Ge, Re;
        {
            const double te = CAT(run_loop, SUF)(EMPTY, buf, src, bytes, k, 1, 1000000, 0, 0) / 1e6;
            if (reset_timed) {
                const double tg = CAT(run_loop, SUF)(EMPTY, buf, src, bytes, k, 1000, R, 1, 1) / 1000.0;
                Re = R; Ge = (long)ceil(loop_s / tg); if (Ge < 1) Ge = 1;
            } else {
                Ge = 1; Re = (long)ceil(loop_s / te); if (Re < 1) Re = 1;
            }
        }

        char la[64];
        loadavg(la, sizeof la);
        printf("B type=%s k=%d n=%zu bytes=%zu R=%ld R_overflow=%ld reset=%s loop_s=%.2f repeats=%d cpu=%d sibling=%d hugepages=%d attempt=%d load=%s\n",
               TYPENAME, k, n, bytes, R, R_over, reset_timed ? "timed" : "untimed", loop_s, repeats,
               my_cpu, sibling_cpu, hugepages, attempt, la);
        fflush(stdout);

        cpustat s0_me, s0_sib, s0_all, s1_me, s1_sib, s1_all;
        read_stat(my_cpu, &s0_me); read_stat(sibling_cpu, &s0_sib); read_stat(-1, &s0_all);
        const double wall0 = now();
        static double tt[64][128];
        long sw[64];
        int redone[64];
        for (int a = 0; a <= nv; a++) { sw[a] = 0; redone[a] = 0; loop_seconds[a] = 1e30; }
        for (int r = 0; r < repeats; r++) {
            for (int q = 0; q <= nv; q++) {
                const int a = (q + r) % (nv + 1);          /* the order turns with every repeat */
                const long c0 = ivcsw();
                double t;
                /* A loop counts only if it ran for 0.8 * loop_s or longer (0.2 s with the default).
                 * The calibration can come out too slow (another process on the same core at that
                 * moment), and then the loop is too short: make it longer and run it again. */
                for (int tries = 0;; tries++) {
                    if (a == nv) {
                        t = CAT(run_loop, SUF)(EMPTY, buf, src, bytes, k, Ge, Re, reset_timed, reset_timed);
                        tt[a][r] = t * 1e9 / ((double)Ge * (double)Re * (double)n);
                    } else {
                        t = CAT(run_loop, SUF)(VARS[idx[a]].f, buf, src, bytes, k, G[a], R, reset_timed, 1);
                        tt[a][r] = t * 1e9 / ((double)G[a] * (double)R * (double)n);
                    }
                    if (t >= 0.8 * loop_s || tries >= 20) break;
                    const double grow = 1.1 * loop_s / (t > 1e-9 ? t : 1e-9);
                    if (a == nv && !reset_timed) Re = (long)ceil((double)Re * grow) + 1;
                    else if (a == nv) Ge = (long)ceil((double)Ge * grow) + 1;
                    else G[a] = (long)ceil((double)G[a] * grow) + 1;
                    redone[a]++;
                }
                if (t < loop_seconds[a]) loop_seconds[a] = t;
                sw[a] += ivcsw() - c0;
            }
        }
        const double wall1 = now();
        read_stat(my_cpu, &s1_me); read_stat(sibling_cpu, &s1_sib); read_stat(-1, &s1_all);
        if (busy_pct(&s0_sib, &s1_sib) > sibling_limit && attempt < max_attempts) {
            printf("D type=%s k=%d attempt=%d discarded: processor %d, the hyper-thread sibling of the timed processor %d, was busy for %.1f %% of the time (limit %.0f %%)\n",
                   TYPENAME, k, attempt, sibling_cpu, my_cpu, busy_pct(&s0_sib, &s1_sib), sibling_limit);
            fflush(stdout);
            repin_to_quietest_core();
            continue;
        }

        for (int a = 0; a <= nv; a++) qsort(tt[a], (size_t)repeats, sizeof(double), CAT(cmp_double, SUF));
        const double emin = tt[nv][0];
        for (int a = 0; a <= nv; a++) {
            const double mn = tt[a][0], md = tt[a][repeats / 2], mx = tt[a][repeats - 1];
            const int is_e = (a == nv);
            printf("%s type=%s k=%d variant=%s min=%.4f med=%.4f max=%.4f net_min=%.4f net_med=%.4f "
                   "spread_med_pct=%.1f spread_max_pct=%.1f ns_per_transform_min=%.2f G=%ld R=%ld "
                   "loop_s_min=%.3f redone=%d ivcsw=%ld\n",
                   is_e ? "E" : "T", TYPENAME, k, is_e ? "empty" : VARS[idx[a]].name,
                   mn, md, mx, is_e ? 0.0 : mn - emin, is_e ? 0.0 : md - emin,
                   mn > 0 ? 100.0 * (md - mn) / mn : 0.0, mn > 0 ? 100.0 * (mx - mn) / mn : 0.0,
                   mn * (double)n, is_e ? Ge : G[a], is_e ? Re : R,
                   loop_seconds[a], redone[a], sw[a]);
        }
        loadavg(la, sizeof la);
        printf("A type=%s k=%d mycpu_busy_pct=%.1f mycpu_steal_pct=%.2f sibling_busy_pct=%.1f allcpus_busy_pct=%.1f wall_s=%.1f attempt=%d cpu=%d load=%s\n",
               TYPENAME, k, busy_pct(&s0_me, &s1_me), steal_pct(&s0_me, &s1_me),
               busy_pct(&s0_sib, &s1_sib), busy_pct(&s0_all, &s1_all), wall1 - wall0, attempt, my_cpu, la);
        fflush(stdout);
        break;
        }   /* attempt */
        free(src); free(buf);
    }
}

#undef CAT
#undef CAT2
