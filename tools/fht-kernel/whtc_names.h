/* whtc_names.h -- internal.  whtc_impl.h is included twice in one file (float, then double), so every name it defines
 * gets the suffix of the precision being compiled: WHTC_SUFFIX is set to f or d just before each inclusion, and these
 * macros, expanded lazily, turn for example g20_nat into g20_nat_f or g20_nat_d.  This keeps the text of
 * whtc_steps.h and whtc_ffht_plan.h word for word the text that was timed.  It also chooses the step (WHTC_STEP). */
#ifndef WHTC_NAMES_H
#define WHTC_NAMES_H

#define WHTC_PASTE_(a, b) a##_##b
#define WHTC_PASTE(a, b) WHTC_PASTE_(a, b)
#define WHTC_SFX(name) WHTC_PASTE(name, WHTC_SUFFIX)

#define kid_nat WHTC_SFX(kid_nat)
#define tb2_nat WHTC_SFX(tb2_nat)
#define tb4_nat WHTC_SFX(tb4_nat)
#define tb8_nat WHTC_SFX(tb8_nat)
#define tb8_balS WHTC_SFX(tb8_balS)
#define g20_nat WHTC_SFX(g20_nat)
#define g20_broken WHTC_SFX(g20_broken)
#define hfirst_kid_nat WHTC_SFX(hfirst_kid_nat)
#define hfirst_tb2_nat WHTC_SFX(hfirst_tb2_nat)
#define hfirst_tb4_nat WHTC_SFX(hfirst_tb4_nat)
#define hfirst_tb8_nat WHTC_SFX(hfirst_tb8_nat)
#define hfirst_tb8_balS WHTC_SFX(hfirst_tb8_balS)
#define hfirst_g20_nat WHTC_SFX(hfirst_g20_nat)
#define hfirst_g20_broken WHTC_SFX(hfirst_g20_broken)
#define hstep_kid_nat WHTC_SFX(hstep_kid_nat)
#define hstep_tb2_nat WHTC_SFX(hstep_tb2_nat)
#define hstep_tb4_nat WHTC_SFX(hstep_tb4_nat)
#define hstep_tb8_nat WHTC_SFX(hstep_tb8_nat)
#define hstep_tb8_balS WHTC_SFX(hstep_tb8_balS)
#define hstep_g20_nat WHTC_SFX(hstep_g20_nat)
#define hstep_g20_broken WHTC_SFX(hstep_g20_broken)
#define ffht_inlane WHTC_SFX(ffht_inlane)
#define inlane_all WHTC_SFX(inlane_all)
#define ffht_thr WHTC_SFX(ffht_thr)
#define FFHT_THR_F WHTC_SFX(FFHT_THR_F)
#define FFHT_THR_D WHTC_SFX(FFHT_THR_D)
#define scalar_wht WHTC_SFX(scalar_wht)
#define hfirst_fn WHTC_SFX(hfirst_fn)
#define hstep_fn WHTC_SFX(hstep_fn)
#define hvar WHTC_SFX(hvar)
#define hyb_block WHTC_SFX(hyb_block)
#define hyb_rec WHTC_SFX(hyb_rec)
#define hyb WHTC_SFX(hyb)
#define whtc_hv WHTC_SFX(whtc_hv)
#define whtc_run WHTC_SFX(whtc_run)

/* the step: -DWHTC_STEP=G20 (default), TB8BALS or TB8 */
#define WHTC_STEP_ID_G20 1
#define WHTC_STEP_ID_TB8BALS 2
#define WHTC_STEP_ID_TB8 3
#ifndef WHTC_STEP
#define WHTC_STEP G20
#endif
#define WHTC_ID_(s) WHTC_STEP_ID_##s
#define WHTC_ID(s) WHTC_ID_(s)
#define WHTC_STEP_ID WHTC_ID(WHTC_STEP)
#if WHTC_STEP_ID == 1
#define WHTC_STEP_NAME "g20"
#elif WHTC_STEP_ID == 2
#define WHTC_STEP_NAME "tb8balS"
#elif WHTC_STEP_ID == 3
#define WHTC_STEP_NAME "tb8"
#else
#error "WHTC_STEP must be G20, TB8BALS or TB8"
#endif

#endif /* WHTC_NAMES_H */
