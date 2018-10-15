from neuron import h
import matplotlib.pyplot as plt
import numpy as np

plt.ion()

h.load_file('stdrun.hoc')

sec = h.Section(name="sec")

gfold = h.Gfluctp(sec(0.5))

time = h.Vector()
time.record(h._ref_t)

h.tstop = 1000

v_soma = h.Vector()
v_soma.record(sec(0.5)._ref_v)

h.run()

plt.plot(time, v_soma, label="old_nocall", linewidth=2)

#gfold.noiseFromRandom123(0,0,0)
gfold.seed1, gfold.seed2, gfold.seed3 = 0, 0, 0
h.run()
plt.plot(time, v_soma, label="old_0_0_0", linewidth=2)

#gfold.noiseFromRandom123(0,0,1)
gfold.seed1, gfold.seed2, gfold.seed3 = 0, 0, 1
h.run()
plt.plot(time, v_soma, label="old_0_0_1")

#ld.noiseFromRandom123(0,0,0)
gfold.seed1, gfold.seed2, gfold.seed3 = 0, 0, 0
h.run()
plt.plot(time, v_soma, "-", label="old_0_0_0", linewidth=0.5)

plt.legend()
