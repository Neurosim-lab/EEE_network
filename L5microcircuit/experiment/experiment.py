from neuron import h
import numpy as np
import matplotlib.pyplot as plt
import pyspike as spk
from pyspike import SpikeTrain

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
    #plt.plot(time, pyr_proxap_traces[pyr_index], label='prox ap')
    #plt.plot(time, pyr_distap_traces[pyr_index], label='dist ap')
    plt.legend()


for inh_index, inh_trace in enumerate(inh_traces):
    plt.figure()
    plt.plot(time, inh_trace)
    plt.xlabel('Time (ms)')
    plt.ylabel('Membrane Potential (mV)')
    plt.title('Inhibitory cell ' + str(inh_index))

spike_ind = h.idvec.to_python()
spike_time = h.timevec.to_python()

plt.figure() 
for ind, spike in zip(spike_ind, spike_time):
    plt.vlines(spike, ind - 0.5, ind + 0.5)
    
spike_times = [ [] for i in range(len(pyr_soma_traces)) ]

for index, dummy in enumerate(spike_times):
    spike_times[index] = [time for ind, time in zip(spike_ind, spike_time) if ind==index]

def make_spike_trains(spike_times, time_range):

    spike_trains = [ [] for i in range(len(spike_times)) ]

    for index, times in enumerate(spike_times):

        spike_times[index] = [time for time in times if (time > time_range[0] and time < time_range[1])]
        spike_trains[index] = spk.SpikeTrain(np.array(spike_times[index]), edges=time_range)

    return spike_trains


spike_trains = make_spike_trains(spike_times, time_range=[500, 6000])

spike_trains = spike_trains[0:6]

sync_profile = spk.spike_sync_profile(spike_trains)
x, y = sync_profile.get_plottable_data()
plt.figure()
plt.plot(x, y)
plt.ylabel('Synchrony')
plt.xlabel('Time (ms)')
plt.title('Synchrony Profile (sync = %.4f)' % sync_profile.avrg())
print("Synchrony: %.8f" % sync_profile.avrg())


isi_profile = spk.isi_profile(spike_trains)
x, y = isi_profile.get_plottable_data()
plt.figure()
plt.plot(x, y)
plt.ylabel('ISI Distance')
plt.xlabel('Time (ms)')
plt.title('ISI Profile (ISI = %.4f)' % isi_profile.avrg())
print("ISI distance: %.8f" % isi_profile.avrg())


spike_profile = spk.spike_profile(spike_trains)
x, y = spike_profile.get_plottable_data()
plt.figure()
plt.plot(x, y)
plt.ylabel('Spike Distance')
plt.xlabel('Time (ms)')
plt.title('Spike Distance Profile (SD = %.4f)' % spike_profile.avrg())
print("SPIKE distance: %.8f" % spike_profile.avrg())


# for max_tau in [0.0, 0.1, 1.0, 10.0]:

#     sync_profile = spk.spike_sync_profile(spike_trains, max_tau=max_tau)
#     x, y = sync_profile.get_plottable_data()
#     plt.figure()
#     plt.plot(x, y)
#     plt.ylabel('Synchrony Profile for max_tau = ' + str(max_tau))
#     plt.xlabel('Time (ms)')
#     plt.title('Synchrony')
#     print("Synchrony: %.8f" % sync_profile.avrg())

    
     