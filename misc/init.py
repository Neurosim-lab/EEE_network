"""
init.py : Initialization for EEE model
path    : eee/sim/
author  : Joe Graham <joe.w.graham@gmail.com>

Initializes models and functions for the EEE project.
Include "compile" to compile mod files before initialization.
Include "sim" to run a complete simulation set.

Usage examples:
	eee/sim% python init.py compile sim
	eee/sim% ipython -i init.py sim
"""

import os
import sys
from neuron import h
from neuron import nrn
import matplotlib.pyplot as plt
import numpy as np
import importlib
from inspect import getsourcefile
import shutil

h.load_file('stdrun.hoc')

simdir = os.path.dirname(os.path.abspath(getsourcefile(lambda:0)))
eeedir = os.path.abspath(os.path.join(simdir, os.pardir))
outputdir = os.path.join(eeedir, "output")
if not os.path.exists(outputdir):
	os.mkdir(outputdir)
batchdatadir = os.path.join(simdir, "batches", "batch_data")
if not os.path.exists(batchdatadir):
	os.mkdir(batchdatadir)
batchfigdir = os.path.join(simdir, "batches", "batch_figs")
if not os.path.exists(batchfigdir):
	os.mkdir(batchfigdir)

from batches.batch_analysis import *
from batches.batch_utils import *

markers = ('o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd')



def initcell(modelname):
	"""Imports a model cell ("SPI6" or "SPI7") and returns an instance."""

	cellclass = getattr(importlib.import_module("cells." + modelname), modelname)
	instance = cellclass()

	return instance


def fixsecname(stringlist):
	"""Fix for section names which include their cell instance:
	   <cell instance info>.secname --> secname"""

	if type(stringlist) == str:
		if stringlist.find(">") != -1:
			stringlist = stringlist[stringlist.find(">")+2:]
	for i, string in enumerate(stringlist):
		if string.find(">") != -1:
			string = string[string.find(">")+2:]
			stringlist[i] = string
			#print("Fixing name to: " + string)
	return stringlist


def record_spike_times(cell):
	"""Prepares a cell to record spike times, saved in cell._spike_times as a 
	   hoc vector."""
	cell._nc = h.NetCon(cell.soma(0.5)._ref_v, None, sec=cell.soma)
	cell._nc.threshold = 0.0
	cell._spike_times = h.Vector()
	cell._nc.record(cell._spike_times)


def get_spike_times(trace, samprate, threshold=0.0):
	"""Returns a list of lists of spike times for experimental voltage traces.
	   Samprate is in kHz. Hat tip to Sam Nemoytin."""
	
	spike_times = []

	dt = (1.0/samprate) # dt in ms, samprate in kHz
	idx = 1
	while idx < len(trace):

		if trace[idx] >= threshold and trace[idx-1] < threshold:
			t1 = (idx-1) * dt
			t2 = idx * dt
			v1 = trace[idx-1]
			v2 = trace[idx]
			spike_time = t1
	  
			if v2 != v1: 
				spike_time += ((threshold-v1)/(v2-v1))*(t2-t1) # linear interpolation
				
			spike_times.append(spike_time)

		idx += 1
	return spike_times


def get_exp_spike_freq(traces, samprate, dur, threshold=0.0):
	"""Given exp trace data in columns, return the spike frequency for each trace.
	   (samprate in kHz, dur in ms)"""

	spike_freqs = []

	if traces.ndim == 1:
		traces = np.expand_dims(traces, axis=2)

	for col in range(np.shape(traces)[1]):
		st = get_spike_times(traces[:,col], samprate=samprate, threshold=threshold)
		spike_freqs.append(float(len(st))/(dur)*1000)

	return spike_freqs


def stim_pulse(stimsec, stimseg=0.5, delay=500, dur=1000, amp=0.1, tstop=2000, recsec="soma", recseg=0.5, inctime=True, plot=False, save=False):
	"""Stimulates cell section with pulse current. 
	   Returns names and time/voltage vectors in a list. 
	   Option recsec is section to record from and can be 
	   "soma" (default), "all", or the name of a section."""

	cell       = stimsec.cell()
	stim       = h.IClamp(stimsec(stimseg))
	stim.delay = delay
	stim.dur   = dur
	stim.amp   = amp
	h.tstop    = tstop
	names      = []
	traces     = []
	
	# Option to not create a time vector, e.g. multiple runs with same settings
	if inctime:
		t_vec = h.Vector()
		t_vec.record(h._ref_t)
		names.append("time")
		traces.append(t_vec)

	if recsec == "soma":
		names.append(cell.soma.name())
		hvec = h.Vector()
		hvec.record(cell.soma(recseg)._ref_v)
		traces.append(hvec)
	elif recsec == "all":
		for i, cursec in enumerate(cell.all_sec):
			names.append(cursec.name())
			hvec = h.Vector()
			hvec.record(cursec(recseg)._ref_v)
			traces.append(hvec)
	else:
		sec = getattr(cell, recsec)
		names.append(recsec.name())
		hvec = h.Vector()
		hvec.record(recsec(recseg)._ref_v)
		traces.append(hvec)

	h.run()	

	fixsecname(names)
	out = [names, traces]
	
	if plot:
		fig = plt.figure()
		time = out[1][0]
		for i, data in enumerate(out[0]):
			if i > 0:
				name = out[0][i]
				trace = out[1][i]
				plt.plot(time, trace, label=name, linewidth=2)
		plt.xlabel("Time (ms)")
		plt.ylabel("Membrane Potential (mV)")
		plt.title("Cell ID: " + str(cell.ID) + " Current Clamp: " + str(amp) + " nA into: " + fixsecname(stimsec.name()))
		plt.legend()

		if save:
			plt.savefig(os.path.join(outputdir, "Stim_pulse_" + cell.name + "_" + str(amp) + "_nA.png"))	

	return out


def stim_pulse_series(cells, amps=None, delay=500, dur=1000, tstop=2000, plotind=False, plotall=True, plotfi=True, cols=2, expname=None, expdata=None, samprate=None, save=False):
	"""Repeats a series of stim pulses on a model cell and plots the comparisons.
	   Optionally compares with given experimental data.
	   If "cells" is a list of cells, all are compared."""

	if expname is not None:
		if expname == "BS0284":
			amps = np.load("../data/BS0284_lstimamp.npy")
			expdata = np.load("../data/BS0284_tracedata_10KHz.npy")
			samprate = 10
		# Create a time vector in ms for the experimental data (samprate in kHz)
		exptime = np.linspace(0, len(expdata)/(samprate), num=len(expdata))
	else:
		expname = "" # An empty string for titling purposes
	
	# Allow function to accept a cell as well as a list of cells
	if type(cells) != list:
		cells = [cells]

	# First assemble the trace data in tempsimdata and the spike frequency data in tempfreq
	simname = ""
	for cell in cells:
		tempsimfreq = []	
		simname = simname + "_" + cell.name
		inctime = True # Only record the time vector the first time through
		for indexamp, amp in enumerate(amps):
			[names, traces] = stim_pulse(cell.soma, delay=delay, dur=dur, amp=amp, tstop=tstop, inctime=inctime, plot=False)
			tempsimfreq.append(len(cell._spike_times)/(dur / 1000)) # dur is in ms
			if inctime:
				simtime = traces[0].to_python()
				tempsimdata = traces[1].to_python()
			else: # After the first time through, stack new data as new columns
				tempsimdata = np.column_stack((tempsimdata,traces[0].to_python()))
			inctime = False

		# First time through a cell, make the trace data 3d and freq data 2d
		if not "simdata" in locals():
			simdata = np.expand_dims(tempsimdata, axis=3)
			simfreq = np.expand_dims(tempsimfreq, axis=2)
		else: # After that, stack the trace data in dim 3 and freq in dim 2
			simdata = np.dstack((simdata, tempsimdata))
			simfreq = np.column_stack((simfreq, tempsimfreq))
		tempsimdata = None

	# Plot the trace data with a separate figure for each amplitude
	if plotind:
		for ampindex, amp in enumerate(amps):
			
			fig = plt.figure()
			if expdata is not None:
				plt.plot(exptime, expdata[:,ampindex], label=expname, linewidth=1.5, alpha=0.5)
			
			for cellindex, cell in enumerate(cells):
				plt.plot(simtime, simdata[:,ampindex,cellindex], label=cell.name, linewidth=1.5, alpha=0.5)
			
			plt.title("Stim Amplitude: " + str(amp) + " nA")
			plt.xlabel("Time (ms)")
			plt.ylabel("Membrane Potential (mV)")
			plt.legend()

			if save:
				plt.savefig(os.path.join(outputdir, "Stim_pulse_series_" + expname + simname + "_" + str(ampindex+1) + ".png"))
	
	# Plot the trace data for every amplitude on one figure
	if plotall:
		fig = plt.figure() #figsize=(8,12))
		numplots = len(amps)
		cols = cols
		rows = int(np.ceil(float(numplots)/cols))
		bottomrow = np.arange(len(amps), len(amps)-cols, -1)
		leftcolumn = np.arange(1, numplots, cols)

		axes = []
		for ampindex, amp in enumerate(amps):

			ax = plt.subplot(rows, cols, ampindex+1)
			axes.append(ax)
			if expdata is not None:
				plt.plot(exptime, expdata[:,ampindex], label=expname, linewidth=1.5, alpha=0.5)
			for cellindex, cell in enumerate(cells):
				plt.plot(simtime, simdata[:,ampindex,cellindex], label=cell.name, linewidth=1.5, alpha=0.5)
			
			# Improve plot appearance
			plt.xlim(min(simtime), max(simtime))
			plt.setp(ax.get_xticklabels()[0], visible=False)
			plt.setp(ax.get_xticklabels()[-1], visible=False)
			plt.setp(ax.get_yticklabels()[0], visible=False)
			plt.setp(ax.get_yticklabels()[-1], visible=False)
			if (ampindex+1) not in bottomrow:
				ax.set_xticks([])
			if (ampindex+1) not in leftcolumn:
				ax.set_yticks([])
			plt.tick_params(labelsize='xx-small')
			if ampindex == 0:
				plt.legend(fontsize = 'xx-small')

		# Make all plots on the same row use the same y axis limits
		for row in np.arange(rows):
			rowax = axes[row*cols : row*cols+cols]
			ylims = []
			for ax in rowax:
				ylims.extend(list(ax.get_ylim()))
			ylim = (min(ylims), max(ylims))
			for ax in rowax:
				ax.set_ylim(ylim)

		# Remove space between subplots
		fig.subplots_adjust(hspace=0, wspace=0)

		# Create axis labels across all subplots
		fig.add_subplot(111, frameon=False)
		plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
		plt.xlabel("Time (ms)")
		plt.ylabel("Membrane Potential (mV)")
		plt.title("Stim Pulse Series")

		if save:
			plt.savefig(os.path.join(outputdir, "Stim_pulse_series_" + expname + simname + ".png"))

	# Plot the frequency/current data 
	if plotfi:
		fig = plt.figure()
		
		if expdata is not None:
			expfreq = get_exp_spike_freq(expdata, samprate, dur, threshold=0.0)
			plt.plot(amps, expfreq, label=expname, marker=markers[0])

		for cellind, cell in enumerate(cells):
			plt.plot(amps, simfreq[:,cellind], label=cell.name, marker=markers[cellind+1], linewidth=2)

		plt.legend(loc="upper left")
		plt.xlabel("Current Amplitude (nA)")
		plt.ylabel("Spike Frequency (Hz)")
		plt.title("Frequency-Current Relationship")

		if save:
			plt.savefig(os.path.join(outputdir, "Frequency_Current_" + expname + simname + ".png"))
		
	return [[simtime, simdata], [amps, simfreq], [exptime, expdata], [amps, expfreq]]


def delete_batchdata(deletefigs=True):
    """Deletes the directory eee/sim/batch_data/. If deletefigs==True, also
    deletes eee/sim/batch_figs/."""
    
    batchdatadir = os.path.join(simdir, "batch_data")
    batchfigdir = os.path.join(simdir, "batch_figs")

    if os.path.isdir(batchdatadir):
        print("Removing directory: " + batchdatadir)
        if (os.path.realpath(batchdatadir) != batchdatadir):
            os.remove(os.path.join(os.curdir, batchdatadir))
        else:
            shutil.rmtree(batchdatadir, ignore_errors=True)
    if deletefigs:
        if os.path.isdir(batchfigdir):
            print("Removing directory: " + batchfigdir)
            if (os.path.realpath(batchfigdir) != batchfigdir):
                os.remove(batchfigdir)
            else:
                shutil.rmtree(batchfigdir, ignore_errors=True)


if __name__ == "__main__":

	print
	print("Initialized EEE simulations from init.py")

	if "compile" in sys.argv:
		execfile("compile.py")

	if "sim" in sys.argv:
		execfile("sim.py")
