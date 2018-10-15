"""
my_batches.py 
Batch simulations for EEE project
contact: joe.w.graham@gmail.com
"""

from collections import OrderedDict
import batch_utils
import numpy as np
import os
from cfg import cfg

batchoutputdir = "batch_data"
if not os.path.exists(batchoutputdir):
	os.mkdir(batchoutputdir)

exp_iclamp_amp = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6]
glut_stim_weight = [0.010, 0.011, 0.012, 0.013, 0.014, 0.015]
glut_stim_scale = 1.0
NMDAdecays = [75, 150, 300, 600, 1200]
NMDAlocs = [0.1, 0.3, 0.5, 0.7, 0.9]

numsyns = cfg.numsyns

# Get synapse locations for uniform and physiological distributions
usl = np.linspace(0.0, 1.0, num=numsyns+2).tolist()[1:-1]

def getspineLocs(numspines, spinedist=[1]):
	numsecs = len(spinedist)
	spineLocs = []
	my_dist = np.array(spinedist).astype(float)
	norm_dist = np.array(my_dist)/sum(my_dist)
	spines_dist = np.round((numspines + 2) * norm_dist)
	for ind, spinenum in enumerate(spines_dist):
		start = ind * (1./numsecs)
		stop = (ind + 1) * (1./numsecs)
		num = spines_dist[ind]
		spineLocs.extend(np.linspace(start, stop, num=num, endpoint=False).tolist())
	spineLocs = spineLocs[1:]
	if len(spineLocs) != numsyns:
		raise Error("Error: number of synapses not equal to desired number.")
	return(spineLocs)

psd = [0.982, 4.677, 10.91, 14.72, 18.24, 18.76, 19.05, 17.15, 17.38, 16.17, 15.36, 15.07, 15.24, 13.97, 12.53, 12.64, 11.84, 9.988, 11.43]

psl = getspineLocs(numsyns, spinedist=psd)


###############################################################################
# Batches 
# -------
# 
###############################################################################

batches = {}

# # Batch template
# batch = {}
# batch["label"] = "my_batch"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["param1_name"] = [0.0, 0.10, 0.50, 1.0, 10.0]
# params["param2_name"] = [0.0, 0.10, 0.50, 1.0, 10.0]
# batch["params"] = params
# batches[batch["label"]] = batch


# # Varying NMDA decay time constant and glutamate stim amplitude
# batch = {}
# batch["label"] = "NMDAdecay_glutAmp"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["tau2NMDA"] = NMDAdecays
# params[('NetStim1', 'weight', 0)] = list(np.array(glut_stim_weight) * glut_stim_scale / numsyns)
# batch["params"] = params
# batches[batch["label"]] = batch


# # Varying glutamate stim location and glutamate stim amplitude
# batch = {}
# batch["label"] = "glutLoc_glutAmp"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params[('NetStim1', 'loc')] = NMDAlocs
# params[('NetStim1', 'weight', 0)] = list(np.array(glut_stim_weight) * glut_stim_scale / numsyns)
# batch["params"] = params
# batches[batch["label"]] = batch


# # Varying glutamate stim amplitude (1D batch)
# batch = {}
# batch["label"] = "glutAmp"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params[('NetStim1', 'weight', 0)] = list(np.array(glut_stim_weight) * glut_stim_scale / numsyns)
# batch["params"] = params
# batches[batch["label"]] = batch


# # Varying glutamate stim location (1D batch)
# batch = {}
# batch["label"] = "glutLoc"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params[('NetStim1', 'loc')] = NMDAlocs
# batch["params"] = params
# batches[batch["label"]] = batch


# # Varying NMDA decay time constant (1D batch)
# batch = {}
# batch["label"] = "NMDAdecay"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["tau2NMDA"] = NMDAdecays
# batch["params"] = params
# batches[batch["label"]] = batch


# Varying synapse distribution (1D batch)
batch = {}
batch["label"] = "synDist"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["synlocs"] = [tuple(usl), tuple(psl)]
batch["params"] = params
batches[batch["label"]] = batch


# # Varying synapse distribution and glutamate stim amplitude
# batch = {}
# batch["label"] = "synDist_glutAmp"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["synlocs"] = [usl, psl]
# params[('NetStim1', 'weight', 0)] = list(np.array(glut_stim_weight) * glut_stim_scale / numsyns)
# batch["params"] = params
# batches[batch["label"]] = batch


###############################################################################
# Main code: runs all batches
###############################################################################

if __name__ == '__main__':
	
	import time
	start = time.time()

	# Run all batches
	for label, batch in batches.items():
		print("Running batch with label: " + label)
		print
		batch_utils.run_batch(**batch)

	stop = time.time()
	print
	print("Completed eee/sim/batches/batch_nospines_255syns/my_batches.py")
	print("Duration (s): " + str(stop-start))
	print("Please close this terminal and open another.")

