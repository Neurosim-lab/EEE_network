"""
batch_analysis.py
Functions to read and plot figures from the EEE batch simulation results.
"""

from cfg import cfg
import batch_utils
import json
import matplotlib.pyplot as plt
from pprint import pprint
import os
import numpy as np
from copy import deepcopy
from scipy.signal import argrelmax
from netpyne import sim

recstep      = 0.1    # ms/sample
spikethresh  = -20.0  # set in netParams.defaultThreshold
platthresh   = 10.0 #10.0 #5.0    # threshold for a plateau
stable       = 50     # ms required for trace to stabilize
syntime      = 200    # time in ms when glutamate is released (synapse time)
spikewidth   = 3.0
batchdatadir = "batch_data"


###############################################################################
# Measurements
# ------------
# This is the place to add new measurements.  The output should be a dictionary
# with a descriptive 'label' and an MxN array of measurements ('values'), where
# M is the number of Parameter 1 values and N is the number of Parameter 2 values.
###############################################################################

# Trace measurements

def clip_trace_spikes(trace, time=None, recstep=recstep, spikewidth=spikewidth, spikethresh=spikethresh, showwork=False):

    if time is None:
        timesteps = len(trace)
        time = recstep * np.arange(0, timesteps, 1)

    spike_times, spike_indices = meas_trace_spike_times(trace, time=time, recstep=recstep, spikethresh=spikethresh, showwork=False)

    spikewidth_ind = int((spikewidth/recstep)/2) # the radius of the clip in indices

    orig_trace = trace
    orig_time  = time

    if len(spike_times) > 0:

        remove_indices = []

        for spki in spike_indices:
            remove_indices.extend(range(spki - spikewidth_ind, spki + spikewidth_ind + 1))

        trace = [i for j, i in enumerate(trace) if j not in remove_indices]
        time = [i for j, i in enumerate(time) if j not in remove_indices]

    if showwork is not False:
        fig = plt.figure()
        plt.plot(orig_time, orig_trace, label="Original", linewidth=1)
        plt.plot(time, trace, 'k-', label="Clipped", linewidth=2)
        plt.ylabel("Membrane Potential (mv)")
        plt.xlabel("Time (ms)")
        plt.title("Trace Spike Times")
        plt.ylim([-90, 20])
        plt.legend()
        if type(showwork) == str:
            fig.savefig(showwork + ".png")
        if showwork is True:
            plt.show()
        else:
            plt.close(fig)

    return trace, time


def meas_trace_spike_times(trace, time=None, recstep=recstep, spikethresh=spikethresh, showwork=False):

    if time is None:
        timesteps = len(trace)
        time = recstep * np.arange(0, timesteps, 1)

    spike_times = []
    spike_indices = []

    for index, sample in enumerate(trace):
        if index > 0 and index < (len(trace)-1):
            if sample > spikethresh:
                if sample > trace[index-1] and sample > trace[index+1]:
                    spike_indices.append(index)
                    spike_times.append(time[index])

    if showwork is not False:
        fig = plt.figure()
        plt.plot(time, trace)
        for spktm in spike_times:
            plt.plot([spktm, spktm], plt.gca().get_ylim(), 'r-', alpha=0.75)
        plt.plot(plt.gca().get_xlim(), [spikethresh, spikethresh], 'g-')
        plt.figtext(0.5, 0.8, str(len(spike_times)) + " spikes", ha="center", fontweight='bold')
        plt.ylabel("Membrane Potential (mv)")
        plt.xlabel("Time (ms)")
        plt.title("Trace Spike Times")
        plt.ylim([-90, 20])
        if type(showwork) == str:
            fig.savefig(showwork + ".png")
        if showwork is True:
            plt.show()
        else:
            plt.close(fig)

    return spike_times, spike_indices


def meas_trace_plat_amp(trace, time=None, recstep=recstep, syntime=syntime, platthresh=platthresh, stable=stable, showwork=False, spikethresh=spikethresh):
    
    stable_index = int(stable / recstep)
    syntime_index = int(syntime / recstep) - 1

    if time is None:
        timesteps = len(trace)
        time = recstep * np.arange(0, timesteps, 1)
    
    baseline_trace, baseline_time = clip_trace_spikes(trace[stable_index:syntime_index], time=time[stable_index:syntime_index], recstep=recstep, spikethresh=spikethresh)
    baseline = np.mean(baseline_trace)
    
    above_index = [valind for valind, val in enumerate(trace) if (val > (baseline + platthresh) and (valind > syntime_index))]

    platamp = 0.0
    platvolt = 0.0

    if len(above_index) > 1:
        minind = np.min(above_index)
        maxind = np.max(above_index)
        v_above = trace[minind:maxind]
        v_above_clipped, v_above_time = clip_trace_spikes(v_above, recstep=recstep, spikethresh=spikethresh)

        platvolt = np.mean(v_above_clipped) #np.max(v_above)
        platamp = np.mean(v_above_clipped) - baseline #np.max(v_above) - baseline
    
    if showwork is not False:
        fig = plt.figure()
        plt.plot(time, trace)
        plt.plot([time[0], time[-1]], [baseline, baseline], 'g', label="Baseline")
        plt.plot([time[0], time[-1]], [baseline+platthresh, baseline+platthresh], 'r', label="Threshold")
        plt.plot([time[0], time[-1]], [baseline+platamp, baseline+platamp], '--k', label="Plat amp")
        plt.figtext(0.5, 0.8, "Plateau amplitude: " + str(platamp), ha="center", fontweight='bold')
        plt.ylabel("Membrane Potential (mv)")
        plt.xlabel("Time (ms)")
        plt.title("Trace Plateau Amplitude")
        plt.ylim([-90, 20])
        plt.legend()
        if type(showwork) == str:
            fig.savefig(showwork + ".png")
        if showwork is True:
            plt.show()
        else:
            plt.close(fig)

    if platamp < 0:
        print("plateau amplitude = " + str(platamp))
        
    return platamp, platvolt


def meas_trace_plat_dur(trace, time=None, recstep=recstep, syntime=syntime, platthresh=platthresh, stable=stable, showwork=False, spikethresh=spikethresh):

    stable_index = int(stable / recstep)
    syntime_index = int(syntime / recstep)

    if time is None:
        timesteps = len(trace)
        time = recstep * np.arange(0, timesteps, 1)

    baseline_trace, baseline_time = clip_trace_spikes(trace[stable_index:syntime_index], time=time[stable_index:syntime_index], recstep=recstep, spikethresh=spikethresh, showwork=False)
    baseline = np.mean(baseline_trace)

    platamp, platvolt = meas_trace_plat_amp(trace, time=time, recstep=recstep, syntime=syntime, platthresh=platthresh, stable=stable, showwork=False, spikethresh=spikethresh)

    plattime = [time[ind] for ind,val in enumerate(trace) if (val > (platvolt-platamp/2) and (ind > syntime_index))]
    if len(plattime) > 0:
        mintime = np.min(plattime)
        maxtime = np.max(plattime)
        platdur = maxtime - mintime
    else:
        platdur = 0.0
        mintime = 0.0
        maxtime = 0.0
    plattimes = (mintime, maxtime)

    if showwork is not False:
        fig = plt.figure()
        plt.plot(time, trace)
        plt.plot([time[0], time[-1]], [baseline, baseline], 'g', label="Baseline")
        plt.plot([time[0], time[-1]], [baseline+platthresh, baseline+platthresh], 'r', label="Threshold")
        plt.plot([time[0], time[-1]], [baseline+platamp, baseline+platamp], '--k', label="Plat amp")
        plt.plot([plattimes[0], plattimes[0]], [baseline, baseline+(platamp/2)], 'r-', linewidth=3.0)
        plt.plot([plattimes[1], plattimes[1]], [baseline, baseline+(platamp/2)], 'r-', linewidth=3.0)
        plt.figtext(0.3, 0.80, "Plateau amplitude: %.2f" % platamp, ha="left")
        plt.figtext(0.3, 0.75, "Plateau duration : %.2f" % platdur, ha="left")
        plt.figtext(0.3, 0.70, "  Baseline : %.2f" % baseline, ha="left")
        plt.ylabel("Membrane Potential (mv)")
        plt.xlabel("Time (ms)")
        plt.title("Trace Plateau Duration")
        plt.ylim([-90, 20])
        plt.legend()
        if type(showwork) == str:
            fig.savefig(showwork + ".png")
        if showwork is True:
            plt.show()
        else:
            plt.close(fig)
        
    return platdur, plattimes
    

def meas_trace_num_spikes(trace, time=None, recstep=recstep, spikethresh=spikethresh, showwork=False):
    
    spike_times, spike_inds = meas_trace_spike_times(trace, time=time, recstep=recstep, spikethresh=spikethresh, showwork=showwork)

    num_spikes = len(spike_times)

    return num_spikes
    

def meas_trace_spike_freq(trace, time=None, recstep=recstep, spikethresh=spikethresh, showwork=False):
    
    spike_times, spike_inds = meas_trace_spike_times(trace, time=time, recstep=recstep, spikethresh=spikethresh, showwork=False)

    if len(spike_times) > 1:
        spike_freq = 1000 * (len(spike_times)-1) / (spike_times[-1] - spike_times[0]) 
    else:
        spike_freq = 0

    return spike_freq


def meas_trace_time_to_spike(trace, time=None, recstep=recstep, syntime=syntime, showwork=False, spikethresh=spikethresh):

    spike_times, spike_inds = meas_trace_spike_times(trace, time=time, recstep=recstep, spikethresh=spikethresh, showwork=False)

    if len(spike_times) > 0:
        time_spike = spike_times[0] - syntime
    else:
        time_spike = 0

    return time_spike


def meas_trace_first_interspike(trace, time=None, recstep=recstep, syntime=syntime, showwork=False, spikethresh=spikethresh):

    spike_times, spike_inds = meas_trace_spike_times(trace, time=time, recstep=recstep, spikethresh=spikethresh, showwork=False)

    if len(spike_times) > 1:
        interspike = spike_times[1] - spike_times[0]
    else:
        interspike = 0

    return interspike


def meas_batch_plat_amp(params, data, cellID=0, platthresh=platthresh, stable=stable, syntime=syntime, recstep=recstep, showwork=False):
    """Measures plateau amplitude for a Netpyne batch"""

    cellLabel = "cell_" + str(cellID)
    stable_index = int(stable / recstep)
    syntime_index = int(syntime / recstep)

    p1vals = params[0]['values']
    p1valsdic = {val: i for i,val in enumerate(p1vals)}
    platamps = [0 for p1 in range(len(p1vals))] 
    if len(params) == 2:
        p2vals = params[1]['values']
        p2valsdic = {val: i for i,val in enumerate(p2vals)}
        platamps = [[0 for p1 in range(len(p1vals))] for p2 in range(len(p2vals))] 
    
    time = None

    for key, d in data.items():
        
        vsoma = d['simData']['V_soma'][cellLabel]
        if time is None:
            timesteps = len(vsoma)
            time = recstep * np.arange(0, timesteps, 1)
            
        platamp, platvolt = meas_trace_plat_amp(vsoma, time=None, recstep=recstep, syntime=syntime, platthresh=platthresh, stable=stable)

        p1index = p1valsdic[d['paramValues'][0]]
        if len(params) == 1:
            platamps[p1index] = platamp
        elif len(params) == 2:
            p2index = p2valsdic[d['paramValues'][1]]
            platamps[p2index][p1index] = platamp

        if showwork:
            
            baseline_trace, baseline_time = clip_trace_spikes(vsoma[stable_index:syntime_index], time=time[stable_index:syntime_index], recstep=recstep, spikethresh=spikethresh)
            baseline = np.mean(baseline_trace)

            vsoma = vsoma[stable_index:]
            if len(time) != len(vsoma):
                time = time[stable_index:]
            fig = plt.figure()
            plt.plot(time, vsoma)
            plt.plot([time[0], time[-1]], [baseline, baseline], 'g', label="Baseline")
            plt.plot([time[0], time[-1]], [baseline+platthresh, baseline+platthresh], 'r', label="Threshold")
            #plt.plot(tabove, baseline*np.ones(len(tabove)), 'rx')
            plt.plot([time[0], time[-1]], [baseline+platamp, baseline+platamp], '--k', label="Plat amp")
            #plt.plot([time[0], time[-1]], [baseline+platminima, baseline+platminima], 'k', label="Spike mins")
            #plt.plot(tminima, vminima, 'bo')
            plt.ylabel("Membrane Potential (mv)")
            plt.xlabel("Time (ms)")
            if len(params) > 1:
                plt.title(cellLabel + ": " + params[0]['label'] + "=" + str(d['paramValues'][0]) + ", " + params[1]['label'] + "=" + str(d['paramValues'][1]))
            else:
                plt.title(cellLabel + ": " + params[0]['label'] + "=" + str(d['paramValues'][0]))
            plt.ylim([-90, 20])
            plt.legend()

    output = {}
    output['label'] = "Plateau Amplitude (mV)"
    output['values'] = platamps
    output['params'] = params
    return output


def meas_batch_plat_dur(params, data, cellID=0, platthresh=platthresh, stable=stable, syntime=syntime, recstep=recstep, showwork=False):
    """Measures plateau duration (time volt trace is above baseline + platthresh)
       stable is time (ms) at which simulation stabilizes
       baselinedir is time length (ms) in which to calculate baseline (should be
            less than time at which stimulation occurs)
       platthresh is voltage (mv) above baseline to define plateau
       set show=True to see plots demonstrating plateau duration on voltage traces"""

    cellLabel = "cell_" + str(cellID)
    stable_index = int(stable / recstep)
    syntime_index = int(syntime / recstep)
    
    p1vals = params[0]['values']
    p1valsdic = {val: i for i,val in enumerate(p1vals)}
    platdurs = [0 for p1 in range(len(p1vals))]

    if len(params) == 2:
        p2vals = params[1]['values']
        p2valsdic = {val: i for i,val in enumerate(p2vals)}
        platdurs = [[0 for p1 in range(len(p1vals))] for p2 in range(len(p2vals))]
    
    time = None
    
    for key, d in data.items():
        
        vsoma = d['simData']['V_soma'][cellLabel]
        if time is None:
            timesteps = len(vsoma)
            time = recstep * np.arange(0, timesteps, 1)
            
        platdur, plattime = meas_trace_plat_dur(vsoma, time=None, recstep=recstep, syntime=syntime, platthresh=platthresh, stable=stable)

        p1index = p1valsdic[d['paramValues'][0]]
        if len(params) == 1:
            platdurs[p1index] = platdur
        elif len(params) == 2:
            p2index = p2valsdic[d['paramValues'][1]]
            platdurs[p2index][p1index] = platdur

        if showwork:

            baseline_trace, baseline_time = clip_trace_spikes(vsoma[stable_index:syntime_index], time=time[stable_index:syntime_index], recstep=recstep, spikethresh=spikethresh)
            baseline = np.mean(baseline_trace)

            platamp, platvolt = meas_trace_plat_amp(vsoma, time=None, recstep=recstep, syntime=syntime, platthresh=platthresh, stable=stable)

            fig = plt.figure()
            plt.plot(time, vsoma)
            plt.plot([time[0], time[-1]], [baseline, baseline], 'g', label="Baseline")
            plt.plot([time[0], time[-1]], [baseline+platthresh, baseline+platthresh], 'r', label="Threshold")
            plt.plot([time[0], time[-1]], [baseline+platamp, baseline+platamp], '--k', label="Plat amp")
            plt.plot([plattime[0], plattime[0]], [baseline, baseline+platthresh], 'r-', linewidth=3.0)
            plt.plot([plattime[1], plattime[1]], [baseline, baseline+platthresh], 'r-', linewidth=3.0)
            plt.figtext(0.3, 0.80, "Plateau amplitude: %.2f" % platamp, ha="left")
            plt.figtext(0.3, 0.75, "Plateau duration : %.2f" % platdur, ha="left")
            plt.ylabel("Membrane Potential (mv)")
            plt.xlabel("Time (ms)")
            plt.ylim([-90, 20])
            plt.legend()
            if len(params) > 1:
                plt.title(cellLabel + ": " + params[0]['label'] + "=" + str(d['paramValues'][0]) + ", " + params[1]['label'] + "=" + str(d['paramValues'][1]))
            else:
                plt.title(cellLabel + ": " + params[0]['label'] + "=" + str(d['paramValues'][0]))

    output = {}
    output['label'] = "Plateau Duration (ms)"
    output['values'] = platdurs
    output['params'] = params
    return output



def meas_batch_num_spikes(params, data, cellID=0, showwork=False):
    """Measures the number of spikes in the voltage trace."""

    p1vals = params[0]['values']
    p1valsdic = {val: i for i,val in enumerate(p1vals)}
    numspikes = [0 for p1 in range(len(p1vals))]

    if len(params) == 2:
        p2vals = params[1]['values']
        p2valsdic = {val: i for i,val in enumerate(p2vals)}
        numspikes = [[0 for p1 in range(len(p1vals))] for p2 in range(len(p2vals))]

    for key, d in data.items():
        
        cellLabel = "cell_" + str(cellID)
        spiketimes = d['simData']['spkt']
        spikeids = d['simData']['spkid']
        spiketimes_curcell = [val for ind,val in enumerate(spiketimes) if spikeids[ind] == cellID]
        numspike = len(spiketimes_curcell)
        
        p1index = p1valsdic[d['paramValues'][0]]
        if len(params) == 1:
            numspikes[p1index] = numspike
        elif len(params) == 2:
            p2index = p2valsdic[d['paramValues'][1]]
            numspikes[p2index][p1index] = numspike

        if showwork:
            fig = plt.figure()
            vsoma = d['simData']['V_soma'][cellLabel]
            time = recstep * np.arange(0, len(vsoma), 1)
            plt.plot(time, vsoma)
            for spktm in spiketimes_curcell:
                plt.plot([spktm, spktm], plt.gca().get_ylim(), 'r-', alpha=0.75)
            plt.plot(plt.gca().get_xlim(), [spikethresh, spikethresh], 'g-')
            plt.figtext(0.5, 0.8, str(numspike) + " spikes", ha="center", fontweight='bold')
            plt.ylabel("Membrane Potential (mv)")
            plt.xlabel("Time (ms)")
            if len(params) > 1:
                plt.title(cellLabel + ": " + params[0]['label'] + "=" + str(d['paramValues'][0]) + ", " + params[1]['label'] + "=" + str(d['paramValues'][1]))
            else:
                plt.title(cellLabel + ": " + params[0]['label'] + "=" + str(d['paramValues'][0]))            

    output = {}
    output['label'] = "Number of Spikes"
    output['values'] = numspikes
    return output


def meas_batch_freq(params, data, cellID=0, showwork=False):
    """Measures the overall frequency of spiking.  Calculated as:
    (number of spikes - 1) / (time of last spike - time of first spike)"""

    p1vals = params[0]['values']
    p1valsdic = {val: i for i,val in enumerate(p1vals)}
    freqs = [0 for p1 in range(len(p1vals))]

    if len(params) == 2:
        p2vals = params[1]['values']
        p2valsdic = {val: i for i,val in enumerate(p2vals)}
        freqs = [[0 for p1 in range(len(p1vals))] for p2 in range(len(p2vals))]

    for key, d in data.items():

        cellLabel = "cell_" + str(cellID)
        spiketimes = d['simData']['spkt']
        spikeids = d['simData']['spkid']
        spiketimes_curcell = [val for ind,val in enumerate(spiketimes) if spikeids[ind] == cellID]
        
        if len(spiketimes_curcell) > 1:
            freq = (len(spiketimes_curcell)-1) / (spiketimes_curcell[-1]-spiketimes_curcell[0])
            freq = freq * 1000 # Convert to Hz (1/ms to 1/s)
            
            p1index = p1valsdic[d['paramValues'][0]]
            if len(params) == 1:
                freqs[p1index] = freq
            elif len(params) == 2:
                p2index = p2valsdic[d['paramValues'][1]]
                freqs[p2index][p1index] = freq

        if showwork:
            fig = plt.figure()
            vsoma = d['simData']['V_soma'][cellLabel]
            time = recstep * np.arange(0, len(vsoma), 1)
            plt.plot(time, vsoma)
            plt.plot(plt.gca().get_xlim(), [spikethresh, spikethresh], 'g-')
            if len(spiketimes_curcell) > 1:
                for spktm in spiketimes_curcell:
                    plt.plot([spktm, spktm], plt.gca().get_ylim(), 'r-', alpha=0.75)
                plt.figtext(0.5, 0.8, str(len(spiketimes_curcell)) + " spikes in " + format(spiketimes_curcell[-1]-spiketimes_curcell[0], '.2f') + " ms =", ha="center", fontweight='bold')
                plt.figtext(0.5, 0.75, format(freq, '.2f') + " Hz spike frequency", ha="center", fontweight='bold')
            
            plt.ylabel("Membrane Potential (mv)")
            plt.xlabel("Time (ms)")
            if len(params) > 1:
                plt.title(cellLabel + ": " + params[0]['label'] + "=" + str(d['paramValues'][0]) + ", " + params[1]['label'] + "=" + str(d['paramValues'][1]))
            else:
                plt.title(cellLabel + ": " + params[0]['label'] + "=" + str(d['paramValues'][0]))

    output = {}
    output['label'] = "Spike Frequency (Hz)"
    output['values'] = freqs
    return output


def meas_batch_time_to_spike(params, data, cellID=0, platthresh=platthresh, stable=stable, syntime=syntime, recstep=recstep, showwork=False):
    """Measures the time to the first spike from the syntime"""

    cellLabel = "cell_" + str(cellID)
    stable_index = int(stable / recstep)
    syntime_index = int(syntime / recstep)

    p1vals = params[0]['values']
    p1valsdic = {val: i for i,val in enumerate(p1vals)}
    tm2sps = [0 for p1 in range(len(p1vals))]

    if len(params) == 2:
        p2vals = params[1]['values']
        p2valsdic = {val: i for i,val in enumerate(p2vals)}
        tm2sps = [[0 for p1 in range(len(p1vals))] for p2 in range(len(p2vals))]
    
    time = None
    
    for key, d in data.items():
        
        vsoma = d['simData']['V_soma'][cellLabel]
        if time is None:
            timesteps = len(vsoma)
            time = recstep * np.arange(0, timesteps, 1)

        tm2sp = meas_trace_time_to_spike(vsoma, time=time, recstep=recstep, syntime=syntime, showwork=showwork, spikethresh=spikethresh)

        p1index = p1valsdic[d['paramValues'][0]]
        if len(params) == 1:
            tm2sps[p1index] = tm2sp
        elif len(params) == 2:
            p2index = p2valsdic[d['paramValues'][1]]
            tm2sps[p2index][p1index] = tm2sp

    output = {}
    output['label'] = "Time to first spike (ms)"
    output['values'] = tm2sps
    output['params'] = params
    return output


def meas_batch_first_interspike(params, data, cellID=0, platthresh=platthresh, stable=stable, syntime=syntime, recstep=recstep, showwork=False):
    """Measures the first interspike interval"""

    cellLabel = "cell_" + str(cellID)
    stable_index = int(stable / recstep)
    syntime_index = int(syntime / recstep)
    
    p1vals = params[0]['values']
    p1valsdic = {val: i for i,val in enumerate(p1vals)}
    inters = [0 for p1 in range(len(p1vals))]

    if len(params) == 2:
        p2vals = params[1]['values']
        p2valsdic = {val: i for i,val in enumerate(p2vals)}
        inters = [[0 for p1 in range(len(p1vals))] for p2 in range(len(p2vals))]

    time = None
    
    for key, d in data.items():
        
        vsoma = d['simData']['V_soma'][cellLabel]
        if time is None:
            timesteps = len(vsoma)
            time = recstep * np.arange(0, timesteps, 1)

        inter = meas_trace_first_interspike(vsoma, time=time, recstep=recstep, syntime=syntime, showwork=showwork, spikethresh=spikethresh)

        p1index = p1valsdic[d['paramValues'][0]]
        if len(params) == 1:
            inters[p1index] = inter
        elif len(params) == 2:
            p2index = p2valsdic[d['paramValues'][1]]
            inters[p2index][p1index] = inter

    output = {}
    output['label'] = "First Interspike Interval (ms)"
    output['values'] = inters
    output['params'] = params
    return output



def get_vtraces(params, data, cellID=0, section="soma", timerange=None, stable=None):
    """Gets the voltage traces for each batch for the chosen section.
    For use with plot_relation()."""

    seckey = "V_" + section
    if stable is not None: 
        stable = int(stable / recstep)

    paramnames = []
    paramvalues = []
    paramvaluedicts = []
    arrayshape = []
    grouped = False
    
    for param in params:
        paramnames.append(param['label'])
        paramvalues.append(param['values'])
        paramvaluedicts.append({val: ind for ind, val in enumerate(param['values'])})
        if 'group' not in param:
            arrayshape.append(len(param['values']))
        elif param['group'] is False:
            arrayshape.append(len(param['values']))
        elif param['group'] is True and grouped is False:
            arrayshape.append(len(param['values']))
            grouped = True

    traces = np.array([])
    timesteps = None

    cellPop = None

    for key, datum in data.items():
        grouped = False
        cellLabel = "cell_" + str(cellID)
        if not cellPop:
            cellPop = datum['net']['cells'][cellID]['tags']['pop']
        
        if cellLabel in datum['simData'][seckey].keys():
            vtrace = datum['simData'][seckey][cellLabel]
            if not timesteps:
                timesteps = len(vtrace)
            if timerange is not None:
                vtrace = vtrace[timerange[0]:timerange[1]]
            elif stable is not None:
                vtrace = vtrace[stable:]
            if traces.size == 0:
                traces = np.empty(shape=tuple(arrayshape)+(len(vtrace),))
            tracesindex = []

            for paramindex, param in enumerate(params):
                if 'group' not in param:
                    tracesindex.append(paramvaluedicts[paramindex][datum['paramValues'][paramindex]])
                elif param['group'] is False:
                    tracesindex.append(paramvaluedicts[paramindex][datum['paramValues'][paramindex]])
                elif param['group'] is True and grouped is False:
                    grouped = True
                    tracesindex.append(paramvaluedicts[paramindex][datum['paramValues'][paramindex]])

            traces[tuple(tracesindex)] = vtrace

    time = recstep * np.arange(0, timesteps, 1)
    if timerange is not None:
        time = time[timerange[0]:timerange[1]]
    elif stable is not None:
        time = time[stable:]

    output = {}
    output['yarray'] = traces
    output['xvector'] = time
    output['params'] = params
    output['autoylabel'] = "Membrane Potential (mV)"
    output['autoxlabel'] = "Time (ms)"
    output['autotitle'] = "Voltage Traces from " + cellLabel + " (" + cellPop + ")"
    output['legendlabel'] = section
    return output


def get_traces(params, data, cellID=0, trace="V_soma", tracename=None, stable=None):
    """Gets the voltage traces for each batch for the chosen section.
    For use with plot_relation()."""

    if tracename is None:
        tracename = trace

    if stable is not None: 
        stable = int(stable / recstep)

    paramnames = []
    paramvalues = []
    paramvaluedicts = []
    arrayshape = []
    grouped = False
    
    for param in params:
        paramnames.append(param['label'])
        paramvalues.append(param['values'])
        paramvaluedicts.append({val: ind for ind, val in enumerate(param['values'])})
        if 'group' not in param:
            arrayshape.append(len(param['values']))
        elif param['group'] is False:
            arrayshape.append(len(param['values']))
        elif param['group'] is True and grouped is False:
            arrayshape.append(len(param['values']))
            grouped = True

    traces = np.array([])
    timesteps = []

    cellPop = None

    for key, datum in data.items():
        grouped = False
        cellLabel = "cell_" + str(cellID)
        
        if not cellPop:
            cellPop = datum['net']['cells'][cellID]['tags']['pop']
        
        if cellLabel in datum['simData'][trace].keys():
            vtrace = datum['simData'][trace][cellLabel]
            if not timesteps:
                timesteps = len(vtrace)
            if stable is not None:
                vtrace = vtrace[stable:]
            if traces.size == 0:
                traces = np.empty(shape=tuple(arrayshape)+(len(vtrace),))
            tracesindex = []

            for paramindex, param in enumerate(params):
                if 'group' not in param:
                    tracesindex.append(paramvaluedicts[paramindex][datum['paramValues'][paramindex]])
                elif param['group'] is False:
                    tracesindex.append(paramvaluedicts[paramindex][datum['paramValues'][paramindex]])
                elif param['group'] is True and grouped is False:
                    grouped = True
                    tracesindex.append(paramvaluedicts[paramindex][datum['paramValues'][paramindex]])

            traces[tuple(tracesindex)] = vtrace

        else:
            raise Exception("Trace " + trace + " not found in " + cellLabel)

    time = recstep * np.arange(0, timesteps, 1)
    if stable is not None:
        time = time[stable:]

    output = {}
    output['yarray'] = traces
    output['xvector'] = time
    output['params'] = params
    output['autoylabel'] = tracename
    output['autoxlabel'] = "Time (ms)"
    output['autotitle'] = "Traces from " + cellLabel + " (" + cellPop + ")"
    output['legendlabel'] = tracename
    return output



def get_bapamp_distance(params, data, cellID=0, section="Bdend1", stimtime=200):
    """Gets the bAP amplitude versus distance along dendrite relation for each 
    batch for the chosen section. For use with plot_relation()."""

    cellLabel = "cell_" + str(cellID)

    p1vals = params[0]['values']
    p2vals = params[1]['values']
    p1valsdic = {val: i for i,val in enumerate(p1vals)}
    p2valsdic = {val: i for i,val in enumerate(p2vals)}

    bapamps = [[ [] for p1 in range(len(p1vals))] for p2 in range(len(p2vals))]
    stimtime = int(stimtime / recstep)

    for index, (key, d) in enumerate(data.items()):

        p1index = p1valsdic[d['paramValues'][0]]
        p2index = p2valsdic[d['paramValues'][1]]
        simdatadict = d['simData']
        tracesdict = d['simConfig']['recordTraces']
        tracenames = sorted(tracesdict.keys())
        cur_bapamps = []
        #traces = []
        if index == 0:
            names = []
            locs = []

        for tracename in tracenames:
            if str(tracesdict[tracename]['sec']) == section:
                trace = simdatadict[tracename][cellLabel]
                bapamp = max(trace[stimtime:]) - trace[stimtime-1]
                cur_bapamps.append(bapamp)
                #traces.append(simdatadict[tracename]["cell_0"])     
                if index == 0:
                    names.append(tracename)
                    locs.append(tracesdict[tracename]['loc'])

        bapamps[p2index][p1index] = cur_bapamps
        locs = np.around(locs, decimals=4)

    output = {}
    output['yarray'] = bapamps
    output['xvector'] = locs
    output['params'] = params
    output['autoylabel'] = "bAP amplitude (mV)"
    output['autoxlabel'] = "Location in: " + section + " (fraction along)"
    output['autotitle'] = "Backpropagating AP Amplitude vs Distance from Soma" 
    return output




###############################################################################
# Plotting
# ------------
# This is the place to add new plotting routines.
###############################################################################

def plot_measure(meas, params, title=None, measlabel=None, param_labels=None, legend_label=None, swapaxes=False, fig=None, figsize=(6, 4.5)):
    """Plots the measure against the parameter values."""
    
    measvals = meas['values']
    measautolabel = meas['label']

    param_vals = []
    param_autolabels = []

    for param in params:
        param_vals.append(param['values'])
        param_autolabel = param['label']
        if type(param_autolabel) == list:
            param_autolabel = param_autolabel[0] + " " + param_autolabel[1]
        param_autolabels.append(param_autolabel)

    if param_labels is None:
        param_labels = param_autolabels
    else:
        for ind, param_label in enumerate(param_labels):
            if param_label is None:
                param_labels[ind] = param_autolabels[ind]        

    if measlabel is None:
        ylabel = measautolabel
    else:
        ylabel = measlabel
    
    if len(params) == 1:
        xlabel = param_labels[0]
        xticks = param_vals[0]
        legendtitle = None
        legendvalues = None
        title = ylabel + " vs " + xlabel
        
    elif len(params) == 2:
        xlabel = param_labels[1]
        xticks = param_vals[1]
        legendtitle = param_labels[0]
        legendvalues = param_vals[0]
        
        if swapaxes:
            param_vals[0], param_vals[1] = param_vals[1], param_vals[0]
            param_labels[0], param_labels[1] = param_labels[1], param_labels[0]
            xlabel = param_labels[1]
            xticks = param_vals[1]
            legendtitle = param_labels[0]
            legendvalues = param_vals[0]
            measvals = np.swapaxes(measvals, 0, 1)
        
        title = ylabel + " vs " + xlabel + " by " + legendtitle

    else:
        print("batch_analysis.plot_scalar() currently only works with one or two parameters.")
        # Raise error

    if fig is None:
        figure = plt.figure(figsize=figsize)       
    else:
        figure = fig
    ax = figure.gca()

    if len(params) == 1:
        handles = ax.plot(xticks, measvals, marker='o', markersize=10, label=legend_label)
        ax.legend(title=legendtitle, loc="best")
    else:
        handles = ax.plot(xticks, measvals, marker='o', markersize=10, label=legend_label)
        ax.legend(handles, legendvalues, title=legendtitle, loc="best")
        #plt.xticks(range(len(xticks))[::2], xticks[::2])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    return figure


def plot_relation(yarray, xvector, params, swapaxes=False, param_labels=None, title=None, xlabel=None, ylabel=None, marker=None, shareyall=True, color=None, fig=None, **kwargs):
    """Given a 2D array of vectors (y values), the x-values, and the Netpyne params, 
    plots the relation for each parameter combination."""

    param_vals = []
    param_autolabels = []

    for param in params:
        param_vals.append(param['values'])
        param_autolabel = param['label']
        if type(param_autolabel) == list:
            param_autolabel = param_autolabel[0] + " " + param_autolabel[1]
        param_autolabels.append(param_autolabel)

    if param_labels is None:
        param_labels = param_autolabels
    else:
        for ind, param_label in enumerate(param_labels):
            if param_label is None:
                param_labels[ind] = param_autolabels[ind]     
        
    if fig is None:
        if title is None and "autotitle" in kwargs:
            title = kwargs["autotitle"]
        if xlabel is None and "autoxlabel" in kwargs:
            xlabel = kwargs['autoxlabel']
        if ylabel is None and "autoylabel" in kwargs:
            ylabel = kwargs['autoylabel']


    if swapaxes:
        param_vals[0], param_vals[1] = param_vals[1], param_vals[0]
        param_labels[0], param_labels[1] = param_labels[1], param_labels[0]
        yarray = np.swapaxes(yarray, 0, 1)

    if fig is None:
        figure = plt.figure(figsize=(12, 8))
        axes = []

    rows = len(param_vals[0])
    cols = len(param_vals[1])

    
    toprow = np.arange(1, cols+1, 1)
    bottomrow = np.arange(rows*cols, rows*cols-cols, -1)
    leftcolumn = np.arange(1, rows*cols, cols)
    subplotind = 0

    if "legendlabel" in kwargs:
        legendlabel = kwargs['legendlabel']
    else:
        legendlabel = None

    for p1ind, p1val in enumerate(param_vals[0]):

        for p2ind, p2val in enumerate (param_vals[1]):
        
            if fig is None:

                subplotind += 1
                if subplotind == 1:
                    ax = plt.subplot(rows, cols, subplotind)
                    ax_share = ax
                else:
                    ax = plt.subplot(rows, cols, subplotind, sharex=ax_share, sharey=ax_share)
                axes.append(ax)

                plt.plot(xvector, yarray[p1ind][p2ind], marker=marker, color=color, label=legendlabel)
                
                plt.setp(ax.get_xticklabels()[0], visible=False)
                plt.setp(ax.get_xticklabels()[-1], visible=False)
                plt.setp(ax.get_yticklabels()[0], visible=False)
                plt.setp(ax.get_yticklabels()[-1], visible=False)
               
                if (subplotind) not in bottomrow:
                    plt.setp(ax.get_xticklabels(), visible=False)
                if (subplotind) not in leftcolumn:
                    plt.setp(ax.get_yticklabels(), visible=False)
                else:
                    plt.ylabel(param_labels[0] + " = " + str(p1val), fontsize="x-small")
                if subplotind in toprow:
                    plt.title(param_labels[1] + " = " + str(p2val), fontsize="x-small")
                plt.tick_params(labelsize='xx-small')

            else:

                axes = fig.get_axes()
                axes[subplotind].plot(xvector, yarray[p1ind][p2ind], marker=marker, color=color, alpha=0.75, label=legendlabel)
                subplotind += 1


    # Make all plots on the same row use the same y axis limits
    for row in np.arange(rows):
        rowax = axes[row*cols : row*cols+cols]
        ylims = []
        for ax in rowax:
            ylims.extend(list(ax.get_ylim()))
        ylim = (min(ylims), max(ylims))
        for ax in rowax:
            ax.set_ylim(ylim)

    # Make all plots use the same y axis limits, if shareyall option is True
    if shareyall:
        ylims = []
        for row in np.arange(rows):
            rowax = axes[row*cols : row*cols+cols]
            for ax in rowax:
                ylims.extend(list(ax.get_ylim()))
        ylim = (min(ylims), max(ylims))
        for row in np.arange(rows):
            rowax = axes[row*cols : row*cols+cols]
            for ax in rowax:
                ax.set_ylim(ylim)

    # Remove space between subplots
    if fig is None:
        figure.subplots_adjust(hspace=0, wspace=0)

    # Create axis labels and title across all subplots
    if xlabel:
        figure.text(0.5, 0.04, xlabel, ha="center")
    if ylabel:
        figure.text(0.04, 0.5, ylabel, va="center", rotation="vertical")
    if title:
        figure.text(0.5, 0.95, title, ha="center")
    if legendlabel:
        axes[0].legend(fontsize="x-small")

    if fig is None:
        return figure
    else:
        return fig


def plot_vtraces(batchname, cellIDs=None, secs=None, timerange=None, param_labels=None, title=None, filename=None, save=True, outputdir="batch_figs"):
    """If secs is None, all compartment voltage traces are plotted. secs can also be a list of compartment names, e.g. secs=['soma', 'Bdend1'].
    If cellID is None, all cells will be plotted (individually).  cellID can also be a list of cell IDs or an integer value."""

    print("Plotting voltage traces...")

    if type(batchname) == str:
        params, data = batch_utils.load_batch(batchname)
    elif type(batchname) == tuple:
        batchname, params, data = batchname
    else:
        raise Exception()

    if secs is None:
        sim_data = data[list(data.keys())[0]]['simData']
        simdata_keys = data[list(data.keys())[0]]['simData'].keys()
        secs_all = [d for d in simdata_keys if str(d[0:2]) == "V_"]

    if type(cellIDs) is int:
        cellIDs = [cellIDs]
    elif cellIDs is None:
        cellLabels = []
        for sec_ind in secs_all:
            cellLabels += list(sim_data[sec_ind].keys())
        cellLabels = sorted(list(set(cellLabels)))
        cellIDs = [int(cL[5:]) for cL in cellLabels]
        
    for cellID in cellIDs:
        cellLabel = "cell_" + str(cellID)

        print("  " + cellLabel)
                
        secs_present = [sec for sec in secs_all if cellLabel in sim_data[sec].keys()]
        secs = [sec[2:] for sec in secs_present if len(sim_data[sec].keys()) > 0]
        secs.sort()
        
        if "soma" in secs:
            secs.insert(0, secs.pop(secs.index("soma")))

        for ind, sec in enumerate(secs):
            output = get_vtraces(params, data, cellID=cellID, section=sec, timerange=timerange)
            if ind == 0:
                fig1 = plot_relation(param_labels=param_labels, title=title, swapaxes=False, **output)
                fig2 = plot_relation(param_labels=param_labels, title=title, swapaxes=True, **output)
            else:
                fig1 = plot_relation(param_labels=param_labels, swapaxes=False, fig=fig1, **output)
                fig2 = plot_relation(param_labels=param_labels, swapaxes=True, fig=fig2, **output)
        
        if save:
            if not os.path.isdir(outputdir):
                os.mkdir(outputdir)
            if filename is None:
                print(str(os.path.join(outputdir, batchname + "_" + cellLabel + "_vtrace_1.png")))
                fig1.savefig(os.path.join(outputdir, batchname + "_" + cellLabel + "_vtrace_1.png"))
                fig2.savefig(os.path.join(outputdir, batchname + "_" + cellLabel + "_vtrace_2.png"))
            else:
                fig1.savefig(os.path.join(outputdir, batchname + "_" + cellLabel + "_vtrace_1_" + filename + ".png"))
                fig2.savefig(os.path.join(outputdir, batchname + "_" + cellLabel + "_vtrace_2_" + filename + ".png"))



def plot_traces(batchname, traces, cellIDs=None, param_labels=None, title=None, filename=None, save=True, outputdir="batch_figs"):
    """If secs is None, all compartment voltage traces are plotted. secs can also be a list of compartment names, e.g. secs=['soma', 'Bdend1'].
    If cellID is None, all cells will be plotted (individually).  cellID can also be a list of cell IDs or an integer value."""

    params, data = batch_utils.load_batch(batchname)

    if type(cellIDs) is int:
        cellIDs = [cellIDs]
    elif cellIDs is None:
        cellIDs = []
        for cell in data[list(data.keys())[0]]['net']['cells']:
            cellIDs.append(cell['gid'])

    if type(traces) is str:
        tracename = traces
        traces = [traces]
    elif type(traces) is list:
        tracename = "_".join(traces)


    for cellID in cellIDs:
        cellLabel = "cell_" + str(cellID)

        for ind, trace in enumerate(traces):
            output = get_traces(params, data, cellID=cellID, trace=trace)
            if ind == 0:
                fig1 = plot_relation(param_labels=param_labels, title=title, swapaxes=False, **output)
                fig2 = plot_relation(param_labels=param_labels, title=title, swapaxes=True, **output)
            else:
                fig1 = plot_relation(param_labels=param_labels, swapaxes=False, fig=fig1, **output)
                fig2 = plot_relation(param_labels=param_labels, swapaxes=True, fig=fig2, **output)
        
        if save:
            if not os.path.isdir(outputdir):
                os.mkdir(outputdir)
            if filename is None:
                fig1.savefig(os.path.join(outputdir, batchname + "_" + cellLabel + "_" + tracename + "_trace_1.png"))
                fig2.savefig(os.path.join(outputdir, batchname + "_" + cellLabel + "_" + tracename + "_trace_2.png"))
            else:
                fig1.savefig(os.path.join(outputdir, batchname + "_" + cellLabel + "_trace_1_" + filename + ".png"))
                fig2.savefig(os.path.join(outputdir, batchname + "_" + cellLabel + "_trace_2_" + filename + ".png"))



def plot_vtraces_multicell(batchname, cellIDs=None, secs=None, param_labels=None, celllabel=None, title=None, filename=None, save=True, outputdir="batch_figs"):
    """For use with 1D batches (vary only one parameter)
    If secs is None, all compartment voltage traces are plotted. secs can also be a list of compartment names, e.g. secs=['soma', 'Bdend1'].
    If cellID is None, all cells will be plotted on one figure.  cellID can also be a list of cell IDs or an integer value."""

    params, data = batch_utils.load_batch(batchname)

    if secs is None:
        sim_data = data[list(data.keys())[0]]['simData']
        simdata_keys = data[list(data.keys())[0]]['simData'].keys()
        v_secs = [d for d in simdata_keys if str(d[0:2]) == "V_"]
        secs = [sec[2:] for sec in v_secs if len(sim_data[sec].keys()) > 0]
        secs.sort()
        if "soma" in secs:
            secs.insert(0, secs.pop(secs.index("soma")))

    if type(cellIDs) is int:
        cellIDs = [cellIDs]
    elif cellIDs is None:
        cellIDs = []
        for cell in data[list(data.keys())[0]]['net']['cells']:
            cellIDs.append(cell['gid'])

    sec0cells = sim_data[v_secs[0]].keys()
    #traceshape = np.shape(sim_data[v_secs[0]][sec0cells[0]])
    traceshape = (len(params[0]['values']), len(sim_data[v_secs[0]][sec0cells[0]]))
    nanarray = np.empty(traceshape)
    nanarray.fill(np.NaN)

    cellparams = {}
    cellparams['values'] = []

    for cellindex, cellID in enumerate(cellIDs):
        if celllabel is None or "cell" in celllabel:
            cellparams['label'] = "Cell"
            cellType = data[list(data.keys())[0]]['net']['cells'][cellID]['tags']['cellType']
            cellparams['values'].append(cellType + "_" + str(cellID))
        elif "pop" in celllabel:
            cellparams['label'] = "Pop"
            cellPop = data[list(data.keys())[0]]['net']['cells'][cellID]['tags']['pop']
            cellparams['values'].append(cellPop)

    for secindex, sec in enumerate(secs):
        output = []
        secLabel = "V_" + sec
        cellTraces = []

        for cellindex, cellID in enumerate(cellIDs):
            cellLabel = "cell_" + str(cellID)
            
            if cellLabel in sim_data[secLabel].keys():
                temp_output = get_vtraces(params, data, cellID=cellID, section=sec)
                cellTraces.append(temp_output['yarray'])
            else:
                cellTraces.append(nanarray)

        output = deepcopy(temp_output)
        output['autotitle'] = 'Multicell Voltage Traces'
        output['yarray'] = np.stack(cellTraces, axis=1)
        output['params'].append(cellparams)
    
        if secindex == 0:
            fig1 = plot_relation(param_labels=param_labels, title=title, swapaxes=False, **output)
            fig2 = plot_relation(param_labels=param_labels, title=title, swapaxes=True, **output)
        else:
            fig1 = plot_relation(param_labels=param_labels, swapaxes=False, fig=fig1, **output)
            fig2 = plot_relation(param_labels=param_labels, swapaxes=True, fig=fig2, **output)
        
        if save:
            if not os.path.isdir(outputdir):
                os.mkdir(outputdir)
            if filename is None:
                fig1.savefig(os.path.join(outputdir, batchname + "_" + "_multicell_vtrace_1.png"))
                fig2.savefig(os.path.join(outputdir, batchname + "_" + "_multicell_vtrace_2.png"))
            else:
                fig1.savefig(os.path.join(outputdir, batchname + "_" + "_multicell_vtrace_1_" + filename + ".png"))
                fig2.savefig(os.path.join(outputdir, batchname + "_" + "_multicell_vtrace_2_" + filename + ".png"))



def plot_antic_plateaus(batch="glutAmp", cellIDs=None, syntime=syntime, section="soma", voffset=20, hoffset=400, savefig=True, vertfig=False, outputdir="batch_figs"):
    """Plots figure like file:gif/20161230_PlateauFunction.jpg
    Requires batch_glutAmp be run in advance."""

    # The following two lines change the font to Arial, as required by CNS for the abstract
    #import matplotlib as mpl
    #mpl.rc('font',family='Arial')

    params, data = batch_utils.load_batch(batch)

    if type(cellIDs) is int:
        cellIDs = [cellIDs]
    elif cellIDs is None:
        cellIDs = []
        for cell in data[list(data.keys())[0]]['net']['cells']:
            cellIDs.append(cell['gid'])

    keys = sorted(data.keys(), key=lambda x: int(x[1:])) #sorts numerically instead of alphabetically

    tracename = "V_" + section
    start = int((syntime - 50) / recstep)

    for cellID in cellIDs:
        cellLabel = "cell_" + str(cellID)

        vtraces = []
        for index, key in enumerate(keys):  
            if index == 0:
                try:
                    time = recstep * np.arange(len(data[key]['simData'][tracename][cellLabel]))
                except:
                    print(data[key]['simData'][tracename])
                    time = recstep * np.arange(len(data[key]['simData'][tracename][cellLabel]))
            vtraces.append(data[key]['simData'][tracename][cellLabel][start:])

        vtraces = np.swapaxes(vtraces, 0, 1)
        time = time[start:]

        if vertfig:
            fig = plt.figure(figsize = (4.5,7))
            plt.subplot(2,1,1)
        else:
            fig = plt.figure(figsize = (9, 4))
            plt.subplot(1,2,1)
        
        plots = plt.plot(time, vtraces)
        leg = plt.legend(plots, params[0]['values'], fontsize="small", title="'Glutamate' Stim")
        plt.setp(leg.get_title(), fontsize='small')
        plt.xlabel("Time (ms)", fontsize="small")
        plt.ylabel("Membrane Potential (mV)", fontsize="small")
        #plt.title("Voltage traces at " + section, fontsize="medium")
        plt.tick_params(labelsize='small')

        if vertfig:
            plt.subplot(2,1,2)
        else:
            plt.subplot(1,2,2)
        plt.hold(True)
        voff = 0
        hoff = 0
        for index in np.arange(len(vtraces[0])):
            plt.plot(time + hoff, vtraces[:,index] + voff)
            voff += voffset
            hoff += hoffset
        plt.xticks([])
        plt.yticks([])

        if savefig:
            if not os.path.isdir(outputdir):
                os.mkdir(outputdir)
            fig.savefig(os.path.join(outputdir, batch + "_" + cellLabel + "_plateau_overlay.png"), dpi=600)

    return fig


def plot_overlay_data(data, syntime=syntime, section="soma", voffset=20, hoffset=400, linewidth=1.0, savefig=True, vertfig=False, name="overlay_01", outputdir="../output"):
    """Uses output from batch_utils.import_excel (Pandas dataFrame)"""

    start = int((syntime - 50) / recstep)
    
    if vertfig:
        fig = plt.figure(figsize = (4.5,7))
        plt.subplot(2,1,1)
    else:
        fig = plt.figure(figsize = (9, 4))
        plt.subplot(1,2,1)
    
    plots = plt.plot(data.index, data)
    #leg = plt.legend(plots, params[0]['values'], fontsize="small", title="'Glutamate' Stim")
    #plt.setp(leg.get_title(), fontsize='small')
    plt.xlabel("Time (ms)", fontsize="small")
    plt.ylabel("Membrane Potential (mV)", fontsize="small")
    #plt.title("Voltage traces at " + section, fontsize="medium")
    plt.tick_params(labelsize='small')

    if vertfig:
        plt.subplot(2,1,2)
    else:
        plt.subplot(1,2,2)
    
    plt.hold(True)
    voff = 0
    hoff = 0
    for index in np.arange(data.shape[1]):
        plt.plot(data.index.values + hoff, data.iloc[:,index].values + voff, linewidth=0.5)
        voff += voffset
        hoff += hoffset
    plt.xticks([])
    plt.yticks([])

    if savefig:
        if not os.path.isdir(outputdir):
            os.mkdir(outputdir)
        fig.savefig(os.path.join(outputdir, name + "_overlay_data.png"), dpi=600)

    return fig


def plot_plat_dur(batchname, cellIDs=None, platthresh=platthresh, stable=stable, syntime=syntime, recstep=recstep, param_labels=None, legend_label=None, title=None, savefig=True, swapaxes=False, showwork=False, outputdir="batch_figs", fig=None):

    if type(batchname) == tuple:
        params, data, batchname = batchname
    else:
        params, data = batch_utils.load_batch(batchname)

    ind_plots = True
    if type(cellIDs) is int:
        cellIDs = [cellIDs]
    elif cellIDs is None or cellIDs == "all":
        if cellIDs == "all":
            ind_plots = False
        cellIDs = []
        for cell in data[list(data.keys())[0]]['net']['cells']:
            cellIDs.append(cell['gid'])
    elif type(cellIDs) is list and len(cellIDs) > 1:
        ind_plots = False

    orig_legend_label = legend_label
    
    for cellID in cellIDs:

        if ind_plots and fig is None:
            fig = None
        else:
            fig = fig
        
        cellLabel = "cell_" + str(cellID)
        if not ind_plots:
            if orig_legend_label is None:
                legend_label = cellLabel
            else: 
                legend_label = orig_legend_label + " " + cellLabel
        
        meas = meas_batch_plat_dur(params, data, cellID=cellID, platthresh=platthresh, stable=stable, syntime=syntime, recstep=recstep, showwork=showwork)
    
        fig = plot_measure(meas, params, title=title, measlabel=None, param_labels=param_labels, legend_label=legend_label, swapaxes=swapaxes, fig=fig)

        if savefig and ind_plots:
            batch_dir = os.path.join(outputdir, batchname + "_" + cellLabel)
            if not os.path.isdir(batch_dir):
                os.mkdir(batch_dir)
            if not swapaxes:
                fig.savefig(os.path.join(batch_dir, batchname + "_" + cellLabel + "_plat_dur.png"))
            else:
                fig.savefig(os.path.join(batch_dir, batchname + "_" + cellLabel + "_plat_dur_2.png"))

        if savefig and not ind_plots:
            cellLabels = str(cellIDs).strip("[]").replace(", ", "&")
            if not swapaxes:
                fig.savefig(os.path.join(outputdir, batchname + "_" + cellLabels + "_plat_dur.png"))
            else:
                fig.savefig(os.path.join(outputdir, batchname + "_" + cellLabels + "_plat_dur_2.png"))

    return fig


def plot_plat_amp(batchname, cellIDs=None, platthresh=platthresh, stable=stable, syntime=syntime, recstep=recstep, param_labels=None, legend_label=None, title=None, savefig=True, swapaxes=False, showwork=False, outputdir="batch_figs", fig=None):

    if type(batchname) == tuple:
        params, data, batchname = batchname
    else:
        params, data = batch_utils.load_batch(batchname)

    ind_plots = True
    if type(cellIDs) is int:
        cellIDs = [cellIDs]
    elif cellIDs is None or cellIDs == "all":
        if cellIDs == "all":
            ind_plots = False
        cellIDs = []
        for cell in data[list(data.keys())[0]]['net']['cells']:
            cellIDs.append(cell['gid'])
    elif type(cellIDs) is list and len(cellIDs) > 1:
        ind_plots = False

    orig_legend_label = legend_label
    
    for cellID in cellIDs:

        if ind_plots and fig is None:
            fig = None
        else:
            fig = fig
        
        cellLabel = "cell_" + str(cellID)
        if not ind_plots:
            if orig_legend_label is None:
                legend_label = cellLabel
            else: 
                legend_label = orig_legend_label + " " + cellLabel
        
        meas = meas_batch_plat_amp(params, data, cellID=cellID, platthresh=platthresh, stable=stable, syntime=syntime, recstep=recstep, showwork=showwork)

        fig = plot_measure(meas, params, title=title, measlabel=None, param_labels=param_labels, legend_label=legend_label, swapaxes=swapaxes, fig=fig)      

        if savefig and ind_plots:
            batch_dir = os.path.join(outputdir, batchname + "_" + cellLabel)
            if not os.path.isdir(batch_dir):
                os.mkdir(batch_dir)
            if not swapaxes:
                fig.savefig(os.path.join(batch_dir, batchname + "_" + cellLabel + "_plat_amp.png"))
            else:
                fig.savefig(os.path.join(batch_dir, batchname + "_" + cellLabel + "_plat_amp_2.png"))

        if savefig and not ind_plots:
            cellLabels = str(cellIDs).strip("[]").replace(", ", "&")
            if not swapaxes:
                fig.savefig(os.path.join(outputdir, batchname + "_" + cellLabels + "_plat_amp.png"))
            else:
                fig.savefig(os.path.join(outputdir, batchname + "_" + cellLabels + "_plat_amp_2.png"))

    return fig


def plot_num_spikes(batchname, cellIDs=None, platthresh=platthresh, stable=stable, syntime=syntime, recstep=recstep, param_labels=None, legend_label=None, title=None, savefig=True, swapaxes=False, showwork=False, outputdir="batch_figs", fig=None):

    if type(batchname) == tuple:
        params, data, batchname = batchname
    else:
        params, data = batch_utils.load_batch(batchname)

    ind_plots = True
    if type(cellIDs) is int:
        cellIDs = [cellIDs]
    elif cellIDs is None or cellIDs == "all":
        if cellIDs == "all":
            ind_plots = False
        cellIDs = []
        for cell in data[list(data.keys())[0]]['net']['cells']:
            cellIDs.append(cell['gid'])
    elif type(cellIDs) is list and len(cellIDs) > 1:
        ind_plots = False

    orig_legend_label = legend_label
    
    for cellID in cellIDs:

        if ind_plots and fig is None:
            fig = None
        else:
            fig = fig
        
        cellLabel = "cell_" + str(cellID)
        if not ind_plots:
            if orig_legend_label is None:
                legend_label = cellLabel
            else: 
                legend_label = orig_legend_label + " " + cellLabel
        
        meas = meas_batch_num_spikes(params, data, cellID=cellID, showwork=showwork)
        
        fig = plot_measure(meas, params, title=title, measlabel=None, param_labels=param_labels,  legend_label=legend_label, swapaxes=swapaxes, fig=fig)         

        if savefig and ind_plots:
            batch_dir = os.path.join(outputdir, batchname + "_" + cellLabel)
            if not os.path.isdir(batch_dir):
                os.mkdir(batch_dir)
            if not swapaxes:
                fig.savefig(os.path.join(batch_dir, batchname + "_" + cellLabel + "_numspikes.png"))
            else:
                fig.savefig(os.path.join(batch_dir, batchname + "_" + cellLabel + "_numspikes_2.png"))

        if savefig and not ind_plots:
            cellLabels = str(cellIDs).strip("[]").replace(", ", "&")
            if not swapaxes:
                fig.savefig(os.path.join(outputdir, batchname + "_" + cellLabels + "_numspikes.png"))
            else:
                fig.savefig(os.path.join(outputdir, batchname + "_" + cellLabels + "_numspikes_2.png"))

    return fig


def plot_freq(batchname, cellIDs=None, platthresh=platthresh, stable=stable, syntime=syntime, recstep=recstep, param_labels=None, legend_label=None, title=None, savefig=True, swapaxes=False, showwork=False, outputdir="batch_figs", fig=None):

    if type(batchname) == tuple:
        params, data, batchname = batchname
    else:
        params, data = batch_utils.load_batch(batchname)

    ind_plots = True
    if type(cellIDs) is int:
        cellIDs = [cellIDs]
    elif cellIDs is None or cellIDs == "all":
        if cellIDs == "all":
            ind_plots = False
        cellIDs = []
        for cell in data[list(data.keys())[0]]['net']['cells']:
            cellIDs.append(cell['gid'])
    elif type(cellIDs) is list and len(cellIDs) > 1:
        ind_plots = False

    orig_legend_label = legend_label
    
    for cellID in cellIDs:

        if ind_plots and fig is None:
            fig = None
        else:
            fig = fig
        
        cellLabel = "cell_" + str(cellID)
        if not ind_plots:
            if orig_legend_label is None:
                legend_label = cellLabel
            else: 
                legend_label = orig_legend_label + " " + cellLabel
        
        meas = meas_batch_freq(params, data, cellID=cellID, showwork=showwork)
        
        fig = plot_measure(meas, params, title=title, measlabel=None, param_labels=param_labels, legend_label=legend_label, swapaxes=swapaxes, fig=fig)   

        if savefig and ind_plots:
            batch_dir = os.path.join(outputdir, batchname + "_" + cellLabel)
            if not os.path.isdir(batch_dir):
                os.mkdir(batch_dir)
            if not swapaxes:
                fig.savefig(os.path.join(batch_dir, batchname + "_" + cellLabel + "_freq.png"))
            else:
                fig.savefig(os.path.join(batch_dir, batchname + "_" + cellLabel + "_freq_2.png"))

        if savefig and not ind_plots:
            cellLabels = str(cellIDs).strip("[]").replace(", ", "&")
            if not swapaxes:
                fig.savefig(os.path.join(outputdir, batchname + "_" + cellLabels + "_freq.png"))
            else:
                fig.savefig(os.path.join(outputdir, batchname + "_" + cellLabels + "_freq_2.png"))

    return fig


def plot_time_to_spike(batchname, cellIDs=None, platthresh=platthresh, stable=stable, syntime=syntime, recstep=recstep, param_labels=None, legend_label=None, title=None, savefig=True, swapaxes=False, showwork=False, outputdir="batch_figs", fig=None):

    if type(batchname) == tuple:
        params, data, batchname = batchname
    else:
        params, data = batch_utils.load_batch(batchname)

    ind_plots = True
    if type(cellIDs) is int:
        cellIDs = [cellIDs]
    elif cellIDs is None or cellIDs == "all":
        if cellIDs == "all":
            ind_plots = False
        cellIDs = []
        for cell in data[list(data.keys())[0]]['net']['cells']:
            cellIDs.append(cell['gid'])
    elif type(cellIDs) is list and len(cellIDs) > 1:
        ind_plots = False

    orig_legend_label = legend_label
    
    for cellID in cellIDs:

        if ind_plots and fig is None:
            fig = None
        else:
            fig = fig
        
        cellLabel = "cell_" + str(cellID)
        if not ind_plots:
            if orig_legend_label is None:
                legend_label = cellLabel
            else: 
                legend_label = orig_legend_label + " " + cellLabel
        
        meas = meas_batch_time_to_spike(params, data, cellID=cellID, showwork=showwork)
        
        fig = plot_measure(meas, params, title=title, measlabel=None, param_labels=param_labels, legend_label=legend_label, swapaxes=swapaxes, fig=fig)

        if savefig and ind_plots:
            batch_dir = os.path.join(outputdir, batchname + "_" + cellLabel)
            if not os.path.isdir(batch_dir):
                os.mkdir(batch_dir)
            if not swapaxes:
                fig.savefig(os.path.join(batch_dir, batchname + "_" + cellLabel + "_tm2sp.png"))
            else:
                fig.savefig(os.path.join(batch_dir, batchname + "_" + cellLabel + "_tm2sp_2.png"))

        if savefig and not ind_plots:
            cellLabels = str(cellIDs).strip("[]").replace(", ", "&")
            if not swapaxes:
                fig.savefig(os.path.join(outputdir, batchname + "_" + cellLabels + "_tm2sp.png"))
            else:
                fig.savefig(os.path.join(outputdir, batchname + "_" + cellLabels + "_tm2sp_2.png"))

    return fig


def plot_first_interspike(batchname, cellIDs=None, platthresh=platthresh, stable=stable, syntime=syntime, recstep=recstep, param_labels=None, legend_label=None, title=None, savefig=True, swapaxes=False, showwork=False, outputdir="batch_figs", fig=None):

    if type(batchname) == tuple:
        params, data, batchname = batchname
    else:
        params, data = batch_utils.load_batch(batchname)

    ind_plots = True
    if type(cellIDs) is int:
        cellIDs = [cellIDs]
    elif cellIDs is None or cellIDs == "all":
        if cellIDs == "all":
            ind_plots = False
        cellIDs = []
        for cell in data[list(data.keys())[0]]['net']['cells']:
            cellIDs.append(cell['gid'])
    elif type(cellIDs) is list and len(cellIDs) > 1:
        ind_plots = False

    orig_legend_label = legend_label
    
    for cellID in cellIDs:

        if ind_plots and fig is None:
            fig = None
        else:
            fig = fig
        
        cellLabel = "cell_" + str(cellID)
        if not ind_plots:
            if orig_legend_label is None:
                legend_label = cellLabel
            else: 
                legend_label = orig_legend_label + " " + cellLabel
        
        meas = meas_batch_first_interspike(params, data, cellID=cellID, showwork=showwork)

        fig = plot_measure(meas, params, title=title, measlabel=None, param_labels=param_labels, legend_label=legend_label, swapaxes=swapaxes, fig=fig)

        if savefig and ind_plots:
            batch_dir = os.path.join(outputdir, batchname + "_" + cellLabel)
            if not os.path.isdir(batch_dir):
                os.mkdir(batch_dir)
            if not swapaxes:
                fig.savefig(os.path.join(batch_dir, batchname + "_" + cellLabel + "_inter.png"))
            else:
                fig.savefig(os.path.join(batch_dir, batchname + "_" + cellLabel + "_inter_2.png"))

        if savefig and not ind_plots:
            cellLabels = str(cellIDs).strip("[]").replace(", ", "&")
            if not swapaxes:
                fig.savefig(os.path.join(outputdir, batchname + "_" + cellLabels + "_inter.png"))
            else:
                fig.savefig(os.path.join(outputdir, batchname + "_" + cellLabels + "_inter_2.png"))

    return fig


def plot_baps(batchname, cellIDs=None, section="basal_34", outputdir="batch_figs", savefig=True):
    """Requires batch_bap be run in advance."""

    params, data = batch_utils.load_batch(batchname)
    
    if type(cellIDs) is int:
        cellIDs = [cellIDs]
    elif cellIDs is None:
        cellIDs = []
        for cell in data[list(data.keys())[0]]['net']['cells']:
            cellIDs.append(cell['gid'])

    for cellID in cellIDs:
        cellLabel = "cell_" + str(cellID)

        output = get_bapamp_distance(params, data, cellID=cellID, section=section, stimtime=200)

        xvector = output['xvector']
        yarray = output['yarray']

        control = yarray[1][1]
        kblock = yarray[0][1]
        nablock = yarray[1][0]
        bothblock = yarray[0][0]

        fig = plt.figure(figsize = (7,8))

        plt.subplot(2,1,1)
        plt.plot(xvector, control, '-ks', label="Control", linewidth=2) 
        plt.plot(xvector, nablock, '-ro', label="Na Block", linewidth=2) 
        plt.plot(xvector, kblock, '-gd', label="K Block", linewidth=2)
        #plt.plot(xvector, bothblock, '-bs', label="Na/K Block", linewidth=2)
        plt.legend(loc='lower left')
        #plt.ylim([20, 100])
        plt.ylabel("AP amplitude (mV)")
        plt.title("Backpropagating AP Amplitude vs Distance from Soma")
        plt.tick_params(labelsize='small')

        plt.subplot(2,1,2)
        plt.plot(xvector, np.array(nablock)/np.array(control), '-ro', label="Na Block", linewidth=2)
        plt.plot(xvector, np.array(kblock)/np.array(control), '-gd', label="K Block", linewidth=2)
        plt.legend(loc='upper left')
        plt.xlabel("Distance (fraction along basal dendrite)")
        plt.ylabel("Amplitude Ratios")
        #plt.ylim([0.6, 1.6])
        plt.tick_params(labelsize='small')

        if savefig:
            if not os.path.isdir(outputdir):
                os.mkdir(outputdir)

            batch_dir = os.path.join(outputdir, batchname + "_" + cellLabel)
            if not os.path.isdir(batch_dir):
                os.mkdir(batch_dir)

            fig.savefig(os.path.join(batch_dir, batchname + "_" + cellLabel + "_bap_amps.png"))

        controld = data['_1_1']['simData']
        nablockd = data['_0_1']['simData']
        kblockd = data['_1_0']['simData']

        controltraces = []
        kblocktraces = []
        nablocktraces = []

        for key in controld.keys():
            print
            print("======================")
            print(key)
            if section in key:
                controltraces.append(controld[key][cellLabel])

        for key in kblockd.keys():
            if section in key:
                kblocktraces.append(kblockd[key][cellLabel])

        for key in nablockd.keys():
            if section in key:
                nablocktraces.append(nablockd[key][cellLabel])

        time = recstep * np.arange(0, len(controltraces[0]), 1)

        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, sharey=True, figsize = (7,8))
        
        ax1.plot(time, np.swapaxes(controltraces, 0, 1), 'k', label="Control", alpha=1.0, linewidth=1.0)
        ax1.plot(time, np.swapaxes(nablocktraces, 0, 1), 'r', label="Na Block", alpha=0.6, linewidth=1.5)
        ax1.set_ylabel("Membrane Potential (mV)")
        ax1.tick_params(labelsize='small')

        handles, labels = ax1.get_legend_handles_labels()
        newLabels, newHandles = [], []
        for handle, label in zip(handles, labels):
          if label not in newLabels:
            newLabels.append(label)
            newHandles.append(handle)
        ax1.legend(newHandles, newLabels)

        ax2.plot(time, np.swapaxes(controltraces, 0, 1), 'k', label="Control", alpha=1.0, linewidth=1.0)
        ax2.plot(time, np.swapaxes(kblocktraces, 0, 1), 'g', label="K Block", alpha=0.6, linewidth=1.5)
        ax2.set_ylabel("Membrane Potential (mV)")
        ax2.tick_params(labelsize='small')

        handles, labels = ax2.get_legend_handles_labels()
        newLabels, newHandles = [], []
        for handle, label in zip(handles, labels):
          if label not in newLabels:
            newLabels.append(label)
            newHandles.append(handle)
        ax2.legend(newHandles, newLabels)
        
        ax1.set_xlim(198, 206)
        ax1.set_title("Backpropagating AP Traces")
        plt.xlabel("Time (ms)")

        if savefig:
            if not os.path.isdir(outputdir):
                os.mkdir(outputdir)

            batch_dir = os.path.join(outputdir, batchname + "_" + cellLabel)
            if not os.path.isdir(batch_dir):
                os.mkdir(batch_dir)

            fig.savefig(os.path.join(batch_dir, batchname + "_" + cellLabel + "_bap_traces.png"))


def plot_plat_comps(batchname, cellIDs=None, expdata=False, platthresh=platthresh, stable=stable, syntime=syntime, recstep=recstep, outputdir="batch_figs", swapaxes=False, savefig=True):

    params, data = batch_utils.load_batch(batchname)
    batchname = (params, data, batchname)

    if not expdata:

        plot_plat_amp(batchname, cellIDs=cellIDs, swapaxes=swapaxes, platthresh=platthresh, stable=stable, syntime=syntime, recstep=recstep)
        plot_plat_dur(batchname, cellIDs=cellIDs, swapaxes=swapaxes, platthresh=platthresh, stable=stable, syntime=syntime, recstep=recstep)
        plot_num_spikes(batchname, cellIDs=cellIDs, swapaxes=swapaxes, platthresh=platthresh, stable=stable, syntime=syntime, recstep=recstep)
        plot_freq(batchname, cellIDs=cellIDs, swapaxes=swapaxes, platthresh=platthresh, stable=stable, syntime=syntime, recstep=recstep)
        plot_time_to_spike(batchname, cellIDs=cellIDs, swapaxes=swapaxes, platthresh=platthresh, stable=stable, syntime=syntime, recstep=recstep)
        plot_first_interspike(batchname, cellIDs=cellIDs, swapaxes=swapaxes, platthresh=platthresh, stable=stable, syntime=syntime, recstep=recstep)

    else:

        for param in params:
            if "glutAmp" in param['label']:
                sim_glutAmps = param['values']

        # Find path to data directory
        curpath = os.getcwd()
        while os.path.split(curpath)[1] != "eee":
            oldpath = curpath
            curpath = os.path.split(curpath)[0]
            if oldpath == curpath:
                raise Exception("Couldn't find data directory. Try running from within eee/sim file tree.")
        datapath = os.path.join(curpath, "data")
        expdata = batch_utils.import_excel(os.path.join(datapath, "srdjan_20171017/B_73_004.xlsx"))

        expparam1 = {}
        expparam1['label'] = 'glutAmp'
        expparam1['values'] = np.linspace(min(sim_glutAmps), max(sim_glutAmps), 10).round(2)
        expdata_params = [expparam1]

        time = np.array(expdata.index.tolist())

        platamps = []
        platdurs = []
        numspikes = []
        spikefreqs = []
        timetospikes = []
        interspikes = []

        for column in np.arange(0, len(expdata.columns)):
            
            cur_data = np.array(expdata.iloc[:,column].tolist())
            
            platamp, platvolt = meas_trace_plat_amp(cur_data, time=time, recstep=0.2, stable=0.0)
            platamps.append(platamp)

            platdur, plattimes = meas_trace_plat_dur(cur_data, time=time, recstep=0.2, stable=0.0)
            platdurs.append(platdur)

            numspike = meas_trace_num_spikes(cur_data, time=time, recstep=0.2, showwork=False)
            numspikes.append(numspike)

            spikefreq = meas_trace_spike_freq(cur_data, time=time, recstep=0.2)
            spikefreqs.append(spikefreq)

            time_to_spike = meas_trace_time_to_spike(cur_data, time=time, recstep=0.2, syntime=100.0, showwork=False)
            timetospikes.append(time_to_spike)

            interspike = meas_trace_first_interspike(cur_data, time=time, recstep=0.2, showwork=False)
            interspikes.append(interspike)

        expdata_platamps = {}
        expdata_platamps['label'] = 'Plateau Amplitude (mV)'
        expdata_platamps['values'] = platamps
        fig1 = plot_measure(expdata_platamps, expdata_params, title=None, measlabel=None, param_labels=None, legend_label="Exp Data")

        expdata_platdurs = {}
        expdata_platdurs['label'] = 'Plateau Duration (ms)'
        expdata_platdurs['values'] = platdurs 
        fig2 = plot_measure(expdata_platdurs, expdata_params, title=None, measlabel=None, param_labels=None, legend_label="Exp Data")

        expdata_numspikes = {}
        expdata_numspikes['label'] = 'Number of Spikes'
        expdata_numspikes['values'] = numspikes 
        fig3 = plot_measure(expdata_numspikes, expdata_params, title=None, measlabel=None, param_labels=None, legend_label="Exp Data")

        expdata_spikefreq = {}
        expdata_spikefreq['label'] = 'Spike Frequency (Hz)'
        expdata_spikefreq['values'] = spikefreqs 
        fig4 = plot_measure(expdata_spikefreq, expdata_params, title=None, measlabel=None, param_labels=None, legend_label="Exp Data")

        expdata_timetospike = {}
        expdata_timetospike['label'] = 'Time to first spike (ms)'
        expdata_timetospike['values'] = timetospikes 
        fig5 = plot_measure(expdata_timetospike, expdata_params, title=None, measlabel=None, param_labels=None, legend_label="Exp Data")

        expdata_interspike = {}
        expdata_interspike['label'] = 'First interspike interval (ms)'
        expdata_interspike['values'] = interspikes 
        fig6 = plot_measure(expdata_interspike, expdata_params, title=None, measlabel=None, param_labels=None, legend_label="Exp Data")

        plot_plat_amp(batchname, cellIDs=cellIDs, fig=fig1, legend_label="Sim Data", swapaxes=swapaxes, platthresh=platthresh, stable=stable, syntime=syntime, recstep=recstep)
        plot_plat_dur(batchname, cellIDs=cellIDs, fig=fig2, legend_label="Sim Data", swapaxes=swapaxes, platthresh=platthresh, stable=stable, syntime=syntime, recstep=recstep)
        plot_num_spikes(batchname, cellIDs=cellIDs, fig=fig3, legend_label="Sim Data", swapaxes=swapaxes, platthresh=platthresh, stable=stable, syntime=syntime, recstep=recstep)
        plot_freq(batchname, cellIDs=cellIDs, fig=fig4, legend_label="Sim Data", swapaxes=swapaxes, platthresh=platthresh, stable=stable, syntime=syntime, recstep=recstep)
        plot_time_to_spike(batchname, cellIDs=cellIDs, fig=fig5, legend_label="Sim Data", swapaxes=swapaxes, platthresh=platthresh, stable=stable, syntime=syntime, recstep=recstep)
        plot_first_interspike(batchname, cellIDs=cellIDs, fig=fig6, legend_label="Sim Data", swapaxes=swapaxes, platthresh=platthresh, stable=stable, syntime=syntime, recstep=recstep)


def plot_all(redoall=False):
    """The following code is run on all existing batches (i.e. on all directories 
        in the directory "batch_data"  If redoall is False, only plots new batches."""

    for batch in list_batches():
        
        print(batch)

        batch_plotted = os.path.isfile(os.path.join(batchfigdir, batch + "_platdur.png"))

        params, data = load_batch(batch) 
        
        if redoall or not batch_plotted:

            params, data = load_batch(batch)

            # Plateau duration
            meas = meas_platdur(params, data, platthresh=platthresh)
            fig = plot_measure(meas, params, title=None, measlabel=None, param_labels=None)
            fig.savefig(os.path.join(batchfigdir, batch + "_platdur.png"))

            # Plateau amplitude
            meas = meas_plat_amp(params, data, platthresh=platthresh)
            fig = plot_measure(meas, params, title=None, measlabel=None, param_labels=None)
            fig.savefig(os.path.join(batchfigdir, batch + "_platamp.png"))

            # Number of spikes
            meas = meas_num_spikes(params, data)
            fig = plot_measure(meas, params, title=None, measlabel=None, param_labels=None)
            fig.savefig(os.path.join(batchfigdir, batch + "_numspikes.png"))

            # Somatic EPSP
            meas = meas_epsp(params, data, syntime=syntime)
            fig = plot_measure(meas, params, title=None, measlabel=None, param_labels=None)
            fig.savefig(os.path.join(batchfigdir, batch + "_soma_epsp.png"))

            # Overall spike frequency
            meas = meas_freq(params, data)
            fig = plot_measure(meas, params, title=None, measlabel=None, param_labels=None)
            fig.savefig(os.path.join(batchfigdir, batch + "_freq.png"))

            # Voltage traces
            try:
                vtraces = get_vtraces(params, data)
                fig = plot_relation(**vtraces)
                fig.savefig(os.path.join(batchfigdir, batch + "_vtrace_soma.png"))
                fig = plot_relation(swapaxes=True, **vtraces)
                fig.savefig(os.path.join(batchfigdir, batch + "_vtrace_soma_2.png"))

                vtraces = get_vtraces(params, data, section="Bdend1")
                fig = plot_relation(**vtraces)
                fig.savefig(os.path.join(batchfigdir, batch + "_vtrace_Bdend1.png"))
                fig = plot_relation(swapaxes=True, **vtraces)
                fig.savefig(os.path.join(batchfigdir, batch + "_vtrace_Bdend1_2.png"))

            except:
                print("plot_all() failed during in vtraces in batch: " + batch)




def plot_batch_raster(batchname, batchdatadir=batchdatadir, swapaxes=False, param_labels=None, title=None, xlabel=None, ylabel=None, include =['allCells'], timeRange=None, maxSpikes=1e8, orderBy='gid', orderInverse=True, syncLines=False, figSize=(10,8), fig=None, lw=2, marker='|', markerSize=2, save=True, outputdir="batch_figs", filename=None, **kwargs):
    """Plots raster plots for each parameter combination."""

    if type(batchname) == str:
        params, data = batch_utils.load_batch(batchname, batchdatadir=batchdatadir)
    elif type(batchname) == tuple:
        batchname, params, data = batchname
    else:
        raise Exception()

    param_vals = []
    param_autolabels = []

    for param in params:
        param_vals.append(param['values'])
        param_autolabel = param['label']
        if type(param_autolabel) == list:
            param_autolabel = param_autolabel[0] + " " + param_autolabel[1]
        param_autolabels.append(param_autolabel)

    if param_labels is None:
        param_labels = param_autolabels
    else:
        for ind, param_label in enumerate(param_labels):
            if param_label is None:
                param_labels[ind] = param_autolabels[ind]     

    if title is None and "autotitle" in kwargs:
        title = kwargs["autotitle"]
    if xlabel is None and "autoxlabel" in kwargs:
        xlabel = kwargs['autoxlabel']
    if ylabel is None and "autoylabel" in kwargs:
        ylabel = kwargs['autoylabel']

    if swapaxes:
        param_vals[0], param_vals[1] = param_vals[1], param_vals[0]
        param_labels[0], param_labels[1] = param_labels[1], param_labels[0]

    if fig is None:
        figure = plt.figure(figsize=figSize)
        axes = []
    
    rows = len(param_vals[0])
    cols = len(param_vals[1])
    
    toprow = np.arange(1, cols+1, 1)
    bottomrow = np.arange(rows*cols, rows*cols-cols, -1)
    leftcolumn = np.arange(1, rows*cols, cols)
    subplotind = 0

    if "legendlabel" in kwargs:
        legendlabel = kwargs['legendlabel']
    else:
        legendlabel = None

    for p1ind, p1val in enumerate(param_vals[0]):

        for p2ind, p2val in enumerate (param_vals[1]):

            subplotind += 1
            if subplotind == 1:
                ax = plt.subplot(rows, cols, subplotind)
                ax_share = ax
            else:
                ax = plt.subplot(rows, cols, subplotind, sharex=ax_share, sharey=ax_share)
            axes.append(ax)

            if not swapaxes:
                dataKey = '_' + str(p1ind) + '_' + str(p2ind)
            else:
                dataKey = '_' + str(p2ind) + '_' + str(p1ind)

            sim.load(batchdatadir + '/' + batchname + '/' + batchname + dataKey + '.json', instantiate=False)

            if subplotind == 1:
                sim.analysis.plotRaster(altAx=ax, include=include, timeRange=timeRange, maxSpikes=maxSpikes, orderBy=orderBy, orderInverse=orderInverse, syncLines=syncLines, labels='legend', lw=lw, marker=marker, markerSize=markerSize)
            else:
                sim.analysis.plotRaster(altAx=ax, include=include, timeRange=timeRange, maxSpikes=maxSpikes, orderBy=orderBy, orderInverse=orderInverse, syncLines=syncLines, labels=False, lw=lw, marker=marker, markerSize=markerSize)

            # print('dataKey: %s' % dataKey)
            # print('p1ind: %s' % str(p1ind))
            # print('p1val: %s' % str(p1val))
            # print('p2ind: %s' % str(p2ind))
            # print('p2val: %s' % str(p2val))
            # print
            
            plt.setp(ax.get_xticklabels()[0], visible=False)
            plt.setp(ax.get_xticklabels()[-1], visible=False)
            plt.setp(ax.get_yticklabels()[0], visible=False)
            plt.setp(ax.get_yticklabels()[-1], visible=False)
           
            if (subplotind) not in bottomrow:
                plt.setp(ax.get_xticklabels(), visible=False)
            if (subplotind) not in leftcolumn:
                plt.setp(ax.get_yticklabels(), visible=False)
            else:
                plt.ylabel(param_labels[0] + " = " + str(p1val), fontsize="x-small")
            if subplotind in toprow:
                plt.title(param_labels[1] + " = " + str(p2val), fontsize="x-small")
            plt.tick_params(labelsize='xx-small')

    # # Make all plots on the same row use the same y axis limits
    # for row in np.arange(rows):
    #     rowax = axes[row*cols : row*cols+cols]
    #     ylims = []
    #     for ax in rowax:
    #         ylims.extend(list(ax.get_ylim()))
    #     ylim = (min(ylims), max(ylims))
    #     for ax in rowax:
    #         ax.set_ylim(ylim)

    # # Make all plots use the same y axis limits, if shareyall option is True
    # if shareyall:
    #     ylims = []
    #     for row in np.arange(rows):
    #         rowax = axes[row*cols : row*cols+cols]
    #         for ax in rowax:
    #             ylims.extend(list(ax.get_ylim()))
    #     ylim = (min(ylims), max(ylims))
    #     for row in np.arange(rows):
    #         rowax = axes[row*cols : row*cols+cols]
    #         for ax in rowax:
    #             ax.set_ylim(ylim)

    # Remove space between subplots
    if fig is None:
        figure.subplots_adjust(hspace=0, wspace=0)

    # Create axis labels and title across all subplots

    xlabel = 'Time (ms)'
    ylabel = 'Cells (ordered by %s)' % (orderBy)
    title = 'Raster plots for batch: ' + batchname 

    if xlabel:
        figure.text(0.5, 0.04, xlabel, ha="center")
    if ylabel:
        figure.text(0.04, 0.5, ylabel, va="center", rotation="vertical")
    if title:
        figure.text(0.5, 0.95, title, ha="center")
    if legendlabel:
        axes[0].legend(fontsize="x-small")

    if fig is None:
        if save:
            if filename is None:
                if not swapaxes:
                    figure.savefig(os.path.join(outputdir, batchname + "_raster_1.png"))
                else:
                    figure.savefig(os.path.join(outputdir, batchname + "_raster_2.png"))
        return figure
    else:
        if save:
            if filename is None:
                if not swapaxes:
                    fig.savefig(os.path.join(outputdir, batchname + "_raster_1_" + filename + ".png"))
                else:
                    fig.savefig(os.path.join(outputdir, batchname + "_raster_2_" + filename + ".png"))
        return fig


def plot_batch_conn(batchname, batchdatadir=batchdatadir, swapaxes=False, param_labels=None, title=None, xlabel=None, ylabel=None, includePre = ['all'], includePost = ['all'], feature = 'strength', orderBy = 'gid', figSize = (10,10), groupBy = 'pop', groupByIntervalPre = None, groupByIntervalPost = None, graphType = 'matrix', synOrConn = 'syn', synMech = None, connsFile = None, tagsFile = None, clim = None, fontSize = 12, saveData = None, saveFig = None, showFig = True, save=True, outputdir="batch_figs", filename=None, **kwargs):
    """Plots raster plots for each parameter combination."""

    if type(batchname) == str:
        params, data = batch_utils.load_batch(batchname, batchdatadir=batchdatadir)
    elif type(batchname) == tuple:
        batchname, params, data = batchname
    else:
        raise Exception()

    param_vals = []
    param_autolabels = []

    for param in params:
        param_vals.append(param['values'])
        param_autolabel = param['label']
        if type(param_autolabel) == list:
            param_autolabel = param_autolabel[0] + " " + param_autolabel[1]
        param_autolabels.append(param_autolabel)

    if param_labels is None:
        param_labels = param_autolabels
    else:
        for ind, param_label in enumerate(param_labels):
            if param_label is None:
                param_labels[ind] = param_autolabels[ind]     

    if title is None and "autotitle" in kwargs:
        title = kwargs["autotitle"]
    if xlabel is None and "autoxlabel" in kwargs:
        xlabel = kwargs['autoxlabel']
    if ylabel is None and "autoylabel" in kwargs:
        ylabel = kwargs['autoylabel']

    if swapaxes:
        param_vals[0], param_vals[1] = param_vals[1], param_vals[0]
        param_labels[0], param_labels[1] = param_labels[1], param_labels[0]

    # if fig is None:
    #     figure = plt.figure(figsize=figSize)
    #     axes = []
    figure = plt.figure(figsize=figSize)
    axes = []
    
    rows = len(param_vals[0])
    cols = len(param_vals[1])
    
    toprow = np.arange(1, cols+1, 1)
    bottomrow = np.arange(rows*cols, rows*cols-cols, -1)
    leftcolumn = np.arange(1, rows*cols, cols)
    subplotind = 0

    if "legendlabel" in kwargs:
        legendlabel = kwargs['legendlabel']
    else:
        legendlabel = None

    for p1ind, p1val in enumerate(param_vals[0]):

        for p2ind, p2val in enumerate (param_vals[1]):

            subplotind += 1
            if subplotind == 1:
                ax = plt.subplot(rows, cols, subplotind)
                ax_share = ax
            else:
                ax = plt.subplot(rows, cols, subplotind, sharex=ax_share, sharey=ax_share)
            axes.append(ax)

            if not swapaxes:
                dataKey = '_' + str(p1ind) + '_' + str(p2ind)
            else:
                dataKey = '_' + str(p2ind) + '_' + str(p1ind)

            sim.load(batchdatadir + '/' + batchname + '/' + batchname + dataKey + '.json', instantiate=False)

            if subplotind == 1:
                sim.analysis.plotConn(altAx=ax, includePre=includePre, includePost=includePost, feature=feature, orderBy=orderBy, figSize=figSize, groupBy=groupBy, groupByIntervalPre=groupByIntervalPre, groupByIntervalPost=groupByIntervalPost, graphType=graphType, synOrConn=synOrConn, synMech=synMech, connsFile=connsFile, tagsFile=tagsFile, clim=clim, fontSize=fontSize, saveData=saveData, saveFig=saveFig, showFig=showFig)
            else:
                sim.analysis.plotConn(altAx=ax, includePre=includePre, includePost=includePost, feature=feature, orderBy=orderBy, figSize=figSize, groupBy=groupBy, groupByIntervalPre=groupByIntervalPre, groupByIntervalPost=groupByIntervalPost, graphType=graphType, synOrConn=synOrConn, synMech=synMech, connsFile=connsFile, tagsFile=tagsFile, clim=clim, fontSize=fontSize, saveData=saveData, saveFig=saveFig, showFig=showFig)

            #def plotConn (includePre = ['all'], includePost = ['all'], feature = 'strength', orderBy = 'gid', figSize = (10,10), groupBy = 'pop', groupByIntervalPre = None, groupByIntervalPost = None, graphType = 'matrix', synOrConn = 'syn', synMech = None, connsFile = None, tagsFile = None, clim = None, fontSize = 12, saveData = None, saveFig = None, showFig = True, altAx = None)

            # print('dataKey: %s' % dataKey)
            # print('p1ind: %s' % str(p1ind))
            # print('p1val: %s' % str(p1val))
            # print('p2ind: %s' % str(p2ind))
            # print('p2val: %s' % str(p2val))
            # print
            
            plt.setp(ax.get_xticklabels()[0], visible=False)
            plt.setp(ax.get_xticklabels()[-1], visible=False)
            plt.setp(ax.get_yticklabels()[0], visible=False)
            plt.setp(ax.get_yticklabels()[-1], visible=False)
           
            if (subplotind) not in bottomrow:
                plt.setp(ax.get_xticklabels(), visible=False)
            if (subplotind) not in leftcolumn:
                plt.setp(ax.get_yticklabels(), visible=False)
            else:
                plt.ylabel(param_labels[0] + " = " + str(p1val), fontsize="x-small")
            if subplotind in toprow:
                plt.title(param_labels[1] + " = " + str(p2val), fontsize="x-small")
            plt.tick_params(labelsize='xx-small')

    # # Make all plots on the same row use the same y axis limits
    # for row in np.arange(rows):
    #     rowax = axes[row*cols : row*cols+cols]
    #     ylims = []
    #     for ax in rowax:
    #         ylims.extend(list(ax.get_ylim()))
    #     ylim = (min(ylims), max(ylims))
    #     for ax in rowax:
    #         ax.set_ylim(ylim)

    # # Make all plots use the same y axis limits, if shareyall option is True
    # if shareyall:
    #     ylims = []
    #     for row in np.arange(rows):
    #         rowax = axes[row*cols : row*cols+cols]
    #         for ax in rowax:
    #             ylims.extend(list(ax.get_ylim()))
    #     ylim = (min(ylims), max(ylims))
    #     for row in np.arange(rows):
    #         rowax = axes[row*cols : row*cols+cols]
    #         for ax in rowax:
    #             ax.set_ylim(ylim)

    # Remove space between subplots
    # if fig is None:
    #     figure.subplots_adjust(hspace=0, wspace=0)

    # Create axis labels and title across all subplots

    xlabel = 'Time (ms)'
    ylabel = 'Cells (ordered by %s)' % (orderBy)
    title = 'Connectivity plots for batch: ' + batchname 

    if xlabel:
        figure.text(0.5, 0.04, xlabel, ha="center")
    if ylabel:
        figure.text(0.04, 0.5, ylabel, va="center", rotation="vertical")
    if title:
        figure.text(0.5, 0.95, title, ha="center")
    if legendlabel:
        axes[0].legend(fontsize="x-small")

    if fig is None:
        if save:
            if filename is None:
                if not swapaxes:
                    figure.savefig(os.path.join(outputdir, batchname + "_conn_1.png"))
                else:
                    figure.savefig(os.path.join(outputdir, batchname + "_conn_2.png"))
        return figure
    else:
        if save:
            if filename is None:
                if not swapaxes:
                    fig.savefig(os.path.join(outputdir, batchname + "_conn_1_" + filename + ".png"))
                else:
                    fig.savefig(os.path.join(outputdir, batchname + "_conn_2_" + filename + ".png"))
        return fig





###############################################################################
# Main code: runs all batches
###############################################################################

if __name__ == '__main__':

    import time
    start = time.time()
    
    plot_all()

    import matplotlib.backends.backend_pdf
    pdf = matplotlib.backends.backend_pdf.PdfPages(os.path.join(batchfigdir, "batch_figures.pdf"))
    for i in plt.get_fignums():
        fig = plt.figure(i)
        pdf.savefig(fig)
    pdf.close()

    stop = time.time()
    print
    print("Completed eee/sim/batch_analysis.py")
    print("Duration (s): " + str(stop-start))
    
