"""
Comparing and exploring different gflucts

Gfluct.mod --> Gfluct2
Gfluctp.mod --> Gfluctp
Gfluctp_old.mod --> Gfluctp_old
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from neuron import h
from neuron import nrn
from IPython import embed

from netpyne import specs
cfg = specs.SimConfig()

plt.ion()
h.load_file('stdrun.hoc')
h.tstop = 1000

h.load_file('FS3.hoc')

e_pas = -55.0
h.v_init = -73.0

time = h.Vector()
time.record(h._ref_t)

num_cells = 10


"""
From the network cfg.py file:

        netParams.cellParams['PV5']['secs']['soma']['pointps']= {'noise': {

          'loc': 0.5, 
          'std_e': 0.012*cfg.exc_noise_amp_icells,
          'g_e0' : 0.0121, 
          'tau_i': 10.49*cfg.noise_tau, 
          'tau_e': 2.728*cfg.noise_tau, 
          'std_i': 0.0264*cfg.inh_noise_amp_icells, 
          'g_i0' : 0.0573, 
          'E_e'  : cfg.e_exc_noise_icells, 
          'E_i'  : cfg.e_inh_noise_icells, 
          'mod'  : 'Gfluctp'}}
"""

# noise 
cfg.noise_tau = 1.0

# noise for exc
cfg.e_inh_noise = -75.0 #cfg.vinit_PT5 - 10.0 #-2
cfg.e_exc_noise = 0 #cfg.vinit_PT5 + 70.0 #80
cfg.exc_noise_amp = 0.22 #*6.0
cfg.inh_noise_amp = 0.22 #*4.0

# noise for inh cells
cfg.exc_noise_amp_icells = 1.0
cfg.inh_noise_amp_icells = 0.22
cfg.e_inh_noise_icells = -75.0 #cfg.vinit_PV5 - 5.0 
cfg.e_exc_noise_icells = 0.0 #cfg.vinit_PV5 + 95.0 

gfp = [x for x in range(num_cells)]
gfp_soma = [x for x in range(num_cells)]
noise_gfp = [x for x in range(num_cells)]

for cell_num in range(num_cells):

    gfp[cell_num] = h.FScell()
    gfp[cell_num].soma.e_pas = e_pas
    gfp[cell_num].axon.e_pas = e_pas
    gfp[cell_num].dend.e_pas = e_pas
    gfp_soma[cell_num] = h.Vector()
    gfp_soma[cell_num].record(gfp[cell_num].soma(0.5)._ref_v)
    noise_gfp[cell_num] = h.Gfluctp(gfp[cell_num].soma(0.5))

    # ic_gfp[cell_num] = h.IClamp(gfp.soma(0.5))
    # ic_gfp[cell_num].amp = 1.0
    # ic_gfp[cell_num].delay = 100.0
    # ic_gfp[cell_num].dur = 50.0

    noise_gfp[cell_num].std_e = 0.012 * cfg.exc_noise_amp_icells
    noise_gfp[cell_num].g_e0  = 0.0121
    noise_gfp[cell_num].tau_i = 10.49 * cfg.noise_tau 
    noise_gfp[cell_num].tau_e = 2.728 * cfg.noise_tau
    noise_gfp[cell_num].std_i = 0.0264 * cfg.inh_noise_amp_icells 
    noise_gfp[cell_num].g_i0  = 0.0573
    noise_gfp[cell_num].E_e   = cfg.e_exc_noise_icells 
    noise_gfp[cell_num].E_i   = cfg.e_inh_noise_icells

    if cell_num < 5:
       #noise_gfp[cell_num].noiseFromRandom123(0,0,0)
       print
       print("Cell number " + str(cell_num))
       print("seed1")
       print(noise_gfp[cell_num].seed1)
       noise_gfp[cell_num].seed1 = 1
    else:
       #noise_gfp[cell_num].noiseFromRandom123(cell_num,1,1)
       noise_gfp[cell_num].seed1 = cell_num
       print
       print("Cell number " + str(cell_num))
       print("seed1")
       print(noise_gfp[cell_num].seed1)

#embed()

h.run()

plt.figure()

ax = [x for x in range(num_cells)]

for ax_num in range(num_cells):

    ax[ax_num] = plt.subplot(num_cells, 1, ax_num + 1)
    plt.plot(time, gfp_soma[ax_num], label = "Cell_" + str(ax_num))
    #plt.ylabel("Membrane Potential (mV)")
    #plt.ylim([-90, 40])

plt.xlabel("Time (ms)")
#plt.legend(title="Gfluctp")







