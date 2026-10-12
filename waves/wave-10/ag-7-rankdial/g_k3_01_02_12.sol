p=2 n=8 rows=8 non-input distinct targets=7  intermediates allowed m=4  => gate budget 11
visited states by remaining budget: j=4:1 j=3:8 j=2:315 j=1:9474
RESULT p=2: YES, circuit with 11 gates. points in order (after the 8 inputs):
  g8  TARGET = [1 1 0 0 0 0 0 0]  from #1 + 1*#0 (projectively)
  g9  TARGET = [1 0 1 0 0 0 0 0]  from #2 + 1*#0 (projectively)
  g10 TARGET = [1 0 0 1 0 0 0 0]  from #3 + 1*#0 (projectively)
  g11 inter  = [0 0 0 1 0 0 1 0]  from #6 + 1*#3 (projectively)
  g12 TARGET = [1 0 1 1 0 0 1 0]  from #11 + 1*#9 (projectively)
  g13 inter  = [0 0 0 1 0 1 0 0]  from #5 + 1*#3 (projectively)
  g14 TARGET = [1 1 0 1 0 1 0 0]  from #13 + 1*#8 (projectively)
  g15 inter  = [0 0 0 1 0 1 1 0]  from #11 + 1*#5 (projectively)
  g16 inter  = [1 0 1 0 1 0 0 0]  from #9 + 1*#4 (projectively)
  g17 TARGET = [1 1 1 0 1 0 0 0]  from #16 + 1*#1 (projectively)
  g18 TARGET = [1 1 1 1 1 1 1 0]  from #17 + 1*#15 (projectively)
