import json
from pprint import pprint
import matplotlib.pyplot as plt
import os
import sys
import numpy as np

try: 
    import batch_analysis as ba
except:
    curpath = os.getcwd()
    while os.path.split(curpath)[1] != "sim":
        curpath = os.path.split(curpath)[0]
    sys.path.append(curpath)
    import batch_analysis as ba

data_file = "batch_data/network_jwg_003/network_jwg_003.json"

plot_depol = True
plot_plats = True
plot_non_plats = True

output_dir = os.path.join(os.path.split(data_file)[0], "plat_analysis")
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)


def load_json(filename, show=False):
    """Loads a json file into Python and pretty prints it."""
    with open(filename) as data_file:
        data = json.load(data_file)
        if show: pprint(data)
        return data


def detectDepolBlock(volt, minSamples=200, vRange=[-50, -10]):
    cumm = 0
    for v in volt:
        if v >= vRange[0] and v<= vRange[1]:
            cumm += 1
            if cumm > minSamples:
                return 1
        else:
            cumm = 0

    return 0 


def list_all_dbs():
    dbs = []
    for cell in cells:
        trace = data['simData']['v_soma'][cell]
        db = detectDepolBlock(trace)
        if db == 1:
            dbs.append(cell)   
    return dbs

    
data = load_json(data_file)
time = data['simData']['t']
cells = data['simData']['v_soma'].keys()
traces = [data['simData']['v_soma'][cell] for cell in cells]

db_cells = list_all_dbs()         
db_cells.sort()

print
print("Number of Depol Block cells: " + str(len(db_cells)))
print("Depol block cells:")
print(db_cells)

if plot_depol:
    for cell in db_cells:
        trace = data['simData']['v_soma'][cell]
        fig = plt.figure()
        plt.plot(trace)
        plt.figtext(0.5, 0.80, "Depolarization Blockade", ha="center", fontweight="bold")
        plt.ylabel("Membrane Potential (mv)")
        plt.xlabel("Time (ms)")
        plt.title(cell + " Depolarization Blockade")
        plt.ylim([-80, 20])
        fig.savefig(os.path.join(output_dir, "depol_block_" + cell))
        plt.close(fig)

good_cells = [cell for cell in cells if cell not in db_cells]
good_traces = [data['simData']['v_soma'][cell] for cell in good_cells]

plat_cells = range(0, 125)
plat_cells.extend(range(250, 375))
plat_cells.extend(range(500, 625))
plat_cells.extend(range(750, 875))
plat_cells = ["cell_" + str(cell) for cell in plat_cells]

non_plat_cells = range(125, 250)
non_plat_cells.extend(range(375, 500))
non_plat_cells.extend(range(625, 750))
non_plat_cells.extend(range(875, 1000))
non_plat_cells = ["cell_" + str(cell) for cell in non_plat_cells]

num_spikes = []
plat_amps  = []
plat_durs  = []
spk_freqs  = []

print
print("Plateau Cells")
print("=============")

for cell in plat_cells:

    print(cell)

    num_spike = ba.meas_trace_num_spikes(data['simData']['v_soma'][cell], showwork=False)
    num_spikes.append(num_spike)
    
    plat_amp, plat_volt = ba.meas_trace_plat_amp(data['simData']['v_soma'][cell], showwork=False)
    plat_amps.append(plat_amp)

    if plot_plats:
        plat_dur, plat_time = ba.meas_trace_plat_dur(data['simData']['v_soma'][cell], showwork=os.path.join(output_dir, "plat_durs_" + cell))
    else:
        plat_dur, plat_time = ba.meas_trace_plat_dur(data['simData']['v_soma'][cell], showwork=False)
    plat_durs.append(plat_dur)

    spk_freq = ba.meas_trace_spike_freq(data['simData']['v_soma'][cell])
    spk_freqs.append(spk_freq)

num_spikes_non_plat = []
plat_amps_non_plat  = []
plat_durs_non_plat  = []
spk_freqs_non_plat  = []

print
print("Non-plateau cells")
print("=================")
print

for cell in non_plat_cells:

    print(cell)

    num_spike = ba.meas_trace_num_spikes(data['simData']['v_soma'][cell], showwork=False)
    num_spikes_non_plat.append(num_spike)
    
    plat_amp, plat_volt = ba.meas_trace_plat_amp(data['simData']['v_soma'][cell], showwork=False)
    plat_amps_non_plat.append(plat_amp)

    if plot_non_plats:
        plat_dur, plat_time = ba.meas_trace_plat_dur(data['simData']['v_soma'][cell], showwork=os.path.join(output_dir, "no_plat_plat_durs_" + cell))
    else:
        plat_dur, plat_time = ba.meas_trace_plat_dur(data['simData']['v_soma'][cell], showwork=False)
    plat_durs_non_plat.append(plat_dur)

    spk_freq = ba.meas_trace_spike_freq(data['simData']['v_soma'][cell])
    spk_freqs_non_plat.append(spk_freq)

bins = 15
hist_output_dir = os.path.split(output_dir)[0]

fig = plt.figure()
plt.hist([num_spikes, num_spikes_non_plat], normed=True, bins=bins, label=['Plats', 'Non-Plats'])
plt.title("Number of Spikes")
plt.xlabel("Number of Spikes")
plt.ylabel("Fraction of Cells")
plt.legend()
fig.savefig(os.path.join(hist_output_dir, "hist_numspikes.png"))
plt.yscale('log', nonposy='clip')
fig.savefig(os.path.join(hist_output_dir, "hist_numspikes_log.png"))


fig = plt.figure()
plt.hist([plat_amps, plat_amps_non_plat], normed=True, bins=bins, label=['Plats', 'Non-Plats'])
plt.title("Plateau Amplitudes")
plt.xlabel("Plateau Amplitude (mV)")
plt.ylabel("Fraction of Cells")
plt.legend()
fig.savefig(os.path.join(hist_output_dir, "hist_platamps.png"))
plt.yscale('log', nonposy='clip')
fig.savefig(os.path.join(hist_output_dir, "hist_platamps_log.png"))


fig = plt.figure()
plt.hist([plat_durs, plat_durs_non_plat], normed=True, bins=bins, label=['Plats', 'Non-Plats'])
plt.title("Plateau Durations")
plt.xlabel("Plateau Duration (ms)")
plt.ylabel("Fraction of Cells")
plt.legend()
fig.savefig(os.path.join(hist_output_dir, "hist_platdurs.png"))
plt.yscale('log', nonposy='clip')
fig.savefig(os.path.join(hist_output_dir, "hist_platdurs_log.png"))


fig = plt.figure()
plt.hist([spk_freqs, spk_freqs_non_plat], normed=True, bins=bins, label=['Plats', 'Non-Plats'])
plt.title("Spike Frequencies")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Fraction of Cells")
plt.legend()
fig.savefig(os.path.join(hist_output_dir, "hist_spkfreqs.png"))
plt.yscale('log', nonposy='clip')
fig.savefig(os.path.join(hist_output_dir, "hist_spkfreqs_log.png"))
















