from neuron import h
import matplotlib.pyplot as plt
import numpy as np

seeds = np.arange(500,10000,173) 

h.load_file('stdrun.hoc')
secl=[h.Section(name='sec%d'%n) for n in range(1)]

gbar_nax = 0.0345117294903

for sec in secl:
  sec.insert('hh')
  sec.insert('na')
  sec.gnabar_hh = 0.0
  sec.gbar_na = gbar_nax

#gflold= h.Gfluct2(0.5,sec=secl[0])
#gflold.std_e = 0.012		
#gflold.std_i = 0.0264
#gflold.tau_e = 2.728 * 0.1
#gflold.tau_i = 10.49 * 0.1
#gflold.new_seed(seeds[0])

gflnew= h.Gfluctp(0.5,sec=secl[0])
gflnew.std_e = 0.012		
gflnew.std_i = 0.0264
gflnew.tau_e = 2.728 
gflnew.tau_i = 10.49 
n=0
gflnew.noiseFromRandom123(*seeds[3*n:3*n+3])

#gfl2old= h.Gfluct2OLD(0.5,sec=secl[2])
#gfl2old.std_e = 0.012		
#gfl2old.std_i = 0.0264
#gfl2old.tau_e = 2.728 * 0.1
#gfl2old.tau_i = 10.49 * 0.1

t_vec = h.Vector(1e4)
t_vec.record(h._ref_t)

#vecl = [h.Vector(1e4) for n in range(len(secl))]
#for v,s in zip(vecl,secl):
#  v.record(s(0.5)._ref_v)

vecl = h.Vector(1e4)
for v,s in zip(vecl,secl):
  vecl.record(s(0.5)._ref_v)

h.v_init = -65

h.init()
h.tstop = 200 
h.run()

for i in range(20):
  if not i==0:  
    print vecl[-i]

def plot ():
  plt.figure(figsize = (10, 8), dpi = 100)
  #plt.plot(t_vec, vecl[0], label = 'Gfluct', color = 'black')
  plt.plot(t_vec, vecl[0], label = 'Gfluctp', color = 'red')
  #plt.plot(t_vec, vecl[2], label = 'GfluctOLD', color = 'blue')
  plt.ylim([-70, -40])
  plt.xlim([0, 200])
  plt.ylabel('mV')
  plt.xlabel('Time (ms)')
  plt.legend()
  plt.savefig('noise.png')
  #plt.show()

#plot()
