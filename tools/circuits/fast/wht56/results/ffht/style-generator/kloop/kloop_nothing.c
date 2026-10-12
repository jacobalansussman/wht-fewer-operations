/* kloop_nothing.c -- functions that do nothing, in their own file so that the compiler cannot
 * see through the call: their loop time is the cost of the copy, the loop and the call. */
void kloop_nothing_f(float *buf);
void kloop_nothing_d(double *buf);
void kloop_nothing_f(float *buf) { (void)buf; }
void kloop_nothing_d(double *buf) { (void)buf; }
