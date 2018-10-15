"""
Development code for the EEE project.
"""

import eee_utils as eee
from netpyne.batch import Batch
import matplotlib.pyplot as plt
import numpy as np
import os
import importlib
from neuron import h
from neuron import nrn
plt.ion()

h.load_file('stdrun.hoc')

sec = h.Section()
nmda=h.NMDA(sec(0.5))
print("nmda.mgSlope = " + str(nmda.mgSlope))




# Steepen the mgblock curve
def plot_mgBlock():
    voltrange = np.linspace(-80, 20, 100)

    def mgblock(slope, voltrange):
        voltrange = np.linspace(-80, 20, 100)
        block = 1 / (1 + np.exp(-slope*voltrange)*(1/3.57))
        return block

    # Default slope is 0.062
    slopes = [0.032, 0.042, 0.052, 0.062, 0.072, 0.082, 0.092]

    plt.figure()

    for slope in slopes:
        mgb = mgblock(slope, voltrange)
        plt.plot(voltrange, mgb, label=str(slope))

    plt.legend(loc="best")
    plt.title("Mg Block for various slopes")
    plt.ylabel('Mg Block')
    plt.xlabel('Membrane potential (mv)')



# Testing mgSlope in NMDAeee.mod
def initcell(modelname):
    """Imports a model cell ("SPI6" or "SPI7") and returns an instance."""
    cellclass = getattr(importlib.import_module("cells." + modelname), modelname)
    instance = cellclass()
    return instance



# Create plot to show all currents in dendrite during synaptic stimulation
def syn_stim():
    spi6 = initcell("SPI6")

    num_syns = 1
    factor = 3.0
    nclist = []
    synlist = []

    stim = h.NetStim() 
    stim.number = 1
    stim.interval = 0.0
    stim.start = 200
    h.tstop = 800

    time = h.Vector()
    time.record(h._ref_t)
    v_soma = h.Vector()
    v_soma.record(spi6.soma(0.5)._ref_v)
    v_bdend = h.Vector()
    v_bdend.record(spi6.Bdend1(0.5)._ref_v)

    # Currents in Bdend: ih, nax, kdr, kap, cal, can, kBk
    i_ih = h.Vector()
    i_ih.record(spi6.Bdend1(0.5).ih._ref_i)
    i_na = h.Vector()
    i_na.record(spi6.Bdend1(0.5)._ref_ina)
    i_k = h.Vector()
    i_k.record(spi6.Bdend1(0.5)._ref_ik)
    i_ca = h.Vector()
    i_ca.record(spi6.Bdend1(0.5)._ref_ica)

    for ind in range(num_syns):

        nmda_syn = h.NMDA(spi6.Bdend1(0.5))
        nc_nmda = h.NetCon(stim, nmda_syn)
        nc_nmda.weight[0] = 0.055 * factor
        nc_nmda.delay = 10
        synlist.append(nmda_syn)
        nclist.append(nc_nmda)

        ampa_syn = h.AMPA(spi6.Bdend1(0.5))
        nc_ampa = h.NetCon(stim, ampa_syn)
        nc_ampa.weight[0] = 0.0055 * factor
        nc_ampa.delay = 10
        synlist.append(ampa_syn)
        nclist.append(nc_ampa)


    i_nmda = h.Vector()
    i_nmda.record(synlist[0]._ref_i)
    i_ampa = h.Vector()
    i_ampa.record(synlist[1]._ref_i)

    h.run()

    plt.figure()
    ax1 = plt.subplot(311)
    plt.plot(time, v_soma, label = "Soma")
    plt.plot(time, v_bdend, label = "Bdend")
    plt.ylabel("Membrane Potential (mV)")
    plt.legend()

    ax2 = plt.subplot(312, sharex=ax1)
    plt.plot(time, i_nmda, label="NMDA (" + str(nc_nmda.weight[0]) + ")")
    plt.plot(time, i_ampa, label="AMPA (" + str(nc_ampa.weight[0]) + ")")
    plt.ylabel("Synaptic Currents (nA)")
    plt.legend()

    ax3 = plt.subplot(313, sharex=ax1)
    plt.plot(time, i_ih, label="H")
    plt.plot(time, i_na, label="Na")
    plt.plot(time, i_k, label="K")
    plt.plot(time, i_ca, label="Ca")
    plt.ylabel("Membrane Currents (nA)")
    plt.xlabel("Time (ms)")
    plt.xlim([200, 800])
    plt.legend()
    plt.show()







