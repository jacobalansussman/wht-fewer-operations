/* empty.c -- a "transform" that does nothing.  It is in its own file so that the compiler cannot
 * see through the call when it compiles the timing loop.  Its time is the cost of the loop, the
 * call and (where the copy is timed) the copy. */
void harness_empty_f(float *buf, int log_n);
void harness_empty_d(double *buf, int log_n);

void harness_empty_f(float *buf, int log_n) { (void)buf; (void)log_n; }
void harness_empty_d(double *buf, int log_n) { (void)buf; (void)log_n; }
