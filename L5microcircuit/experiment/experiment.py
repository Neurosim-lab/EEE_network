from neuron import h
import numpy as np
import matplotlib.pyplot as plt
import pyspike as spk

plt.ion()

h.xopen('experiment.hoc')

time = np.array(h.PCt[0].to_python())

pyr_soma_traces = []
pyr_axon_traces = []
pyr_basal_traces = []
pyr_proxap_traces = []
pyr_distap_traces = []

for pyr_soma_trace in h.PCv:
    pyr_soma_traces.append(np.array(pyr_soma_trace.to_python()))

for pyr_axon_trace in h.PCvax:
    pyr_axon_traces.append(np.array(pyr_axon_trace.to_python()))

for pyr_basal_trace in h.PCvbd:
    pyr_basal_traces.append(np.array(pyr_basal_trace.to_python()))

for pyr_proxap_trace in h.PCvpa:
    pyr_proxap_traces.append(np.array(pyr_proxap_trace.to_python()))

for pyr_distap_trace in h.PCvda:
    pyr_distap_traces.append(np.array(pyr_distap_trace.to_python()))

inh_traces = []

for inh_trace in h.INv:
    inh_traces.append(np.array(inh_trace.to_python()))

for pyr_index, pyr_soma_trace in enumerate(pyr_soma_traces):
    
    plt.figure()
    plt.xlabel('Time (ms)')
    plt.ylabel('Membrane Potential (mV)')
    plt.title('Pyramidal cell ' + str(pyr_index))
    plt.plot(time, pyr_soma_trace, label='soma')
    #plt.plot(time, pyr_axon_traces[pyr_index], label='axon')
    plt.plot(time, pyr_basal_traces[pyr_index], label='basal')
    plt.plot(time, pyr_proxap_traces[pyr_index], label='prox ap')
    #plt.plot(time, pyr_distap_traces[pyr_index], label='dist ap')
    plt.legend()


for inh_index, inh_trace in enumerate(inh_traces):
    plt.figure()
    plt.plot(time, inh_trace)
    plt.xlabel('Time (ms)')
    plt.ylabel('Membrane Potential (mV)')
    plt.title('Inhibitory cell ' + str(inh_index))



plt.figure() 
for ind, spikes in zip(h.idvec.to_python(), h.timevec.to_python()):
    plt.vlines(spikes, ind - 0.5, ind + 0.5)
    









