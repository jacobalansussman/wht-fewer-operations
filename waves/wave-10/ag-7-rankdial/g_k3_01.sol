p=2 n=6 rows=8 non-input distinct targets=7  intermediates allowed m=1  => gate budget 8
visited states by remaining budget: j=1:1
RESULT p=2: YES, circuit with 8 gates. points in order (after the 6 inputs):
  g6  TARGET = [1 1 0 0 0 0]  from #1 + 1*#0 (projectively)
  g7  TARGET = [1 0 1 0 0 0]  from #2 + 1*#0 (projectively)
  g8  TARGET = [1 0 0 1 0 0]  from #3 + 1*#0 (projectively)
  g9  TARGET = [1 1 0 1 0 0]  from #6 + 1*#3 (projectively)
  g10 TARGET = [1 0 1 1 0 0]  from #7 + 1*#3 (projectively)
  g11 inter  = [1 0 1 0 1 0]  from #7 + 1*#4 (projectively)
  g12 TARGET = [1 1 1 0 1 0]  from #11 + 1*#1 (projectively)
  g13 TARGET = [1 1 1 1 1 0]  from #12 + 1*#3 (projectively)
