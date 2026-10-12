import jspace
E=[1,2,4]; base=[("shift",w,None) for w in E]+[("sign",w,None) for w in E]
GL=[("map",[2,1,4],None),("map",[2,4,1],None),("map",[3,2,4],None)]
jspace.run(3,3,1,base+GL,"+ every address map (all of GL(3,2))")
jspace.run(3,3,7,base+GL,"+ every address map (all of GL(3,2))")
jspace.run(3,3,1,base+[("map",[2,1,4],None),("map",[1,4,2],None)],"+ every orthogonal map (all permutations of bits)")
jspace.run(2,4,1,[("shift",w,None) for w in (1,2)]+[("sign",w,None) for w in (1,2)]+[("map",[2,1],None),("map",[3,2],None)],"+ every address map (all of GL(2,2))")
