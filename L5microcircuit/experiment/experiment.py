from neuron import h
import numpy as np
import matplotlib.pyplot as plt
import pyspike as spk

plt.ion()

h.xopen('experiment.hoc')

time = np.array(h.PCt[0].to_python())

pyr_traces = []

for pyr_trace in h.PCv:
    pyr_traces.append(np.array(pyr_trace.to_python()))

inh_traces = []

for inh_trace in h.INv:
    inh_traces.append(np.array(inh_trace.to_python()))

for pyr_index, pyr_trace in enumerate(pyr_traces):
    plt.figure()
    plt.plot(time, pyr_trace)
    plt.xlabel('Time (ms)')
    plt.ylabel('Membrane Potential (mV)')
    plt.title('Pyramidal cell ' + str(pyr_index))

for inh_index, inh_trace in enumerate(inh_traces):
    plt.figure()
    plt.plot(time, inh_trace)
    plt.xlabel('Time (ms)')
    plt.ylabel('Membrane Potential (mV)')
    plt.title('Inhibitory cell ' + str(inh_index))

    

plt.figure() 
for ind, spikes in zip(h.idvec.to_python(), h.timevec.to_python()):
    plt.vlines(spikes, ind - 0.5, ind + 0.5)
    









