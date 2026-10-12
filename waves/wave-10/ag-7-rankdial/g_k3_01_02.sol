p=2 n=6 rows=8 non-input distinct targets=7  intermediates allowed m=2  => gate budget 9
visited states by remaining budget: j=2:1 j=1:2
RESULT p=2: YES, circuit with 9 gates. points in order (after the 6 inputs):
  g6  TARGET = [1 1 0 0 0 0]  from #1 + 1*#0 (projectively)
  g7  TARGET = [1 0 1 0 0 0]  from #2 + 1*#0 (projectively)
  g8  TARGET = [1 0 0 1 0 0]  from #3 + 1*#0 (projectively)
  g9  TARGET = [1 0 1 1 0 0]  from #7 + 1*#3 (projectively)
  g10 inter  = [0 0 0 1 0 1]  from #5 + 1*#3 (projectively)
  g11 TARGET = [1 1 0 1 0 1]  from #10 + 1*#6 (projectively)
  g12 inter  = [1 0 1 0 1 0]  from #7 + 1*#4 (projectively)
  g13 TARGET = [1 1 1 0 1 0]  from #12 + 1*#1 (projectively)
  g14 TARGET = [1 1 1 1 1 1]  from #13 + 1*#10 (projectively)
