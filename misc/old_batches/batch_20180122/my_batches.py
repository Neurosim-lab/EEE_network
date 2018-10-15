"""
my_batches.py 
Batch simulations for EEE project
contact: joe.w.graham@gmail.com
"""

from neuron import h
from collections import OrderedDict
import numpy as np
import os
from cfg import cfg
from inspect import getsourcefile
import sys

try: 
	import batch_utils
except:
	curpath = os.getcwd()
	while os.path.split(curpath)[1] != "sim":
		curpath = os.path.split(curpath)[0]
	sys.path.append(curpath)
	import batch_utils
	
batchoutputdir = "batch_data"
if not os.path.exists(batchoutputdir):
	os.mkdir(batchoutputdir)


glutAmps = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
#glutAmps = [0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0, 1.05]


###############################################################################
# Batches 
# ------- 
# 
###############################################################################

batches = {}


# Varying glutSpread and glutAmp
batch = {}
batch["label"] = "glutSpread_glutAmp_dd_02"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["glutSpread"] = [10.0, 15.0] #[10.0, 15.0, 20.0]
#params["glutAmp"] = list(np.linspace(0.025, 0.075, 10).round(3))
#params["glutAmp"] = list(np.linspace(0.065, 0.115, 10).round(3))
params["glutAmp"] = [0.065]
batch["params"] = params
batches[batch["label"]] = batch

# Varying glutSpread
batch = {}
batch["label"] = "glutSpread_glutAmp_01"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["glutSpread"] = [0.7] #[0.7, 5.0, 10.0]
params["glutAmp"] = [1.3] #[1.3, 0.13, 0.013]
batch["params"] = params
batches[batch["label"]] = batch

# # Varying glutSpread
# batch = {}
# batch["label"] = "glutSpread01"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutSpread"] = [0.7, 1.5, 5.0, 10.0]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp and NMDAAlphaScale
# batch = {}
# batch["label"] = "glutAmp_NMDAAlphaScale_2"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# #params["glutAmp"] = list(np.linspace(0.2, 1.3, 5).round(2))
# params["glutAmp"] = list(np.linspace(0.2, 13, 2).round(2))
# params["NMDAAlphaScale"] = [1.0]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying NMDAAlphaScale and mgSlope
# batch = {}
# batch["label"] = "NMDAAlphaScale_mgSlope"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["NMDAAlphaScale"] = [1.0, 2.0, 5.0]
# params["mgSlope"] = [0.042, 0.062, 0.082]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp and mgSlope
# batch = {}
# batch["label"] = "glutAmp_mgSlope"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0.2, 1.3, 5).round(2))
# params["mgSlope"] = [0.042, 0.062, 0.082]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp
# batch = {}
# batch["label"] = "glutAmp"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0.2, 1.3, 10).round(2))
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying NMDAAlphaScale and mgSlope
# batch = {}
# batch["label"] = "NMDAAlphaScale_mgSlope_2"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["NMDAAlphaScale"] = [0.01, 0.1, 0.5, 1.0, 100.0]
# params["mgSlope"] = [0.022, 0.042, 0.062, 0.082, 0.102]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp and NMDAAlphaScale
# batch = {}
# batch["label"] = "glutAmp_NMDAAlphaScale"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0.2, 1.3, 10).round(2))
# params["NMDAAlphaScale"] = [0.01, 0.1, 1.0, 10.0, 100.0]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp and neck resistance
# batch = {}
# batch["label"] = "glutAmp_Rneck"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0.2, 1.3, 20).round(2))
# params["Rneck"] = [30.0, 90.0, 120.0]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp and glutLoc
# batch = {}
# batch["label"] = "glutAmp_glutLoc"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0.2, 1.3, 20).round(2))
# params["glutLoc"] = [0.25, 0.5, 0.75]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp and NMDAAlphaScale
# batch = {}
# batch["label"] = "glutAmp_NMDAAlphaScale"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0.2, 1.3, 20).round(2))
# params["NMDAAlphaScale"] = [3.0, 1.0, 0.33]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp and NMDABetaScale
# batch = {}
# batch["label"] = "glutAmp_NMDABetaScale"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0.2, 1.3, 20).round(2))
# params["NMDABetaScale"] = [3.0, 1.0, 0.33]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp with many samples
# batch = {}
# batch["label"] = "glutAmp_NMDARev_2"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0.2, 1.3, 20).round(2))
# params["NMDARev"] = [-5.0, 0.0, 5.0]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp with many samples
# batch = {}
# batch["label"] = "glutAmp_NMDARev"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0.2, 1.3, 20).round(2))
# params["NMDARev"] = [-10.0, 0.0, 10.0]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp with many samples
# batch = {}
# batch["label"] = "glutAmp_epas_4"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0.2, 1.3, 20).round(2))
# params["e_pas"] = [-85.0, -80.0, -75.0]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp with many samples
# batch = {}
# batch["label"] = "glutAmp_epas_3"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0.4, 1.1, 20).round(2))
# params["e_pas"] = [-75.0, -80.0]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp with many samples
# batch = {}
# batch["label"] = "glutAmp_epas_2"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0.3, 1.2, 20).round(2))
# params["e_pas"] = [-75.0, -80.0]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp with many samples
# batch = {}
# batch["label"] = "glutAmp_epas"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0.2, 1.3, 20).round(2))
# params["e_pas"] = [-75.0, -77.5, -80.0]
# batch["params"] = params
# batches[batch["label"]] = batch


# # Varying glutAmp with many samples
# batch = {}
# batch["label"] = "glutAmp_epas"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0.2, 1.3, 5).round(2))
# params["e_pas"] = [-75.0, -80.0]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp with many samples
# batch = {}
# batch["label"] = "glutAmp_srdjan_6"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0.1, 1.2, 20).round(2))
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp with many samples
# batch = {}
# batch["label"] = "glutAmp_srdjan_5"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0.2, 1.3, 20).round(2))
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp with many samples
# batch = {}
# batch["label"] = "glutAmp_srdjan_4"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0.3, 1.3, 20).round(2))
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp with many samples
# batch = {}
# batch["label"] = "glutAmp_srdjan_3"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0.3, 1.6, 20).round(2))
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp with many samples
# batch = {}
# batch["label"] = "glutAmp_srdjan_2"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0.2, 1.8, 20).round(2))
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp with many samples
# batch = {}
# batch["label"] = "glutAmp_srdjan"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0.0, 1.6, 20).round(2))
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp
# batch = {}
# batch["label"] = "glutAmp"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0.0, 1.2, 10).round(2))
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp
# batch = {}
# batch["label"] = "glutAmp2"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0.2, 1.4, 10).round(2))
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp
# batch = {}
# batch["label"] = "glutAmp3"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0.4, 1.6, 10).round(2))
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp
# batch = {}
# batch["label"] = "glutAmp4"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0.6, 1.8, 10).round(2))
# batch["params"] = params
# batches[batch["label"]] = batch



# # Varying glutAmp and allNaScale (TTX)
# batch = {}
# batch["label"] = "glutAmp_allNaScale"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0.1, 1.2, 10).round(2))
# params["allNaScale"] = [0.0, 1.0]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp and NMDABetaScale
# batch = {}
# batch["label"] = "glutAmp_NMDABetaScale"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0.55, 0.9, 10).round(2))
# params["NMDABetaScale"] = [3.0, 1.0, 0.33]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp and neck resistance
# batch = {}
# batch["label"] = "Rneck_glutAmp"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = [0.6, 0.8, 1.0]
# params["Rneck"] = [30.0, 90.0, 120.0]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp and dendRmScale
# batch = {}
# batch["label"] = "dendRmScale_glutAmp"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = [0.6, 0.8, 1.0]
# params["dendRmScale"] = [0.25, 1.0, 4.0] 
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp and ratioAMPANMDA
# batch = {}
# batch["label"] = "ratioAMPANMDA_glutAmp"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = glutAmps
# params["ratioAMPANMDA"] = [0.1, 0.5, 1.0, 2.0, 10.0] 
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp and dendRaScale
# batch = {}
# batch["label"] = "dendRaScale_glutAmp"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = [0.6, 0.8, 1.0]
# params["dendRaScale"] = [0.25, 1.0, 4.0] 
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp and neck resistance
# batch = {}
# batch["label"] = "Rneck_glutAmp"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = [0.6, 0.8, 1.0]
# params["Rneck"] = [30.0, 90.0, 120.0]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Turning dendritic Na and K on and off for bAPs
# batch = {}
# batch["label"] = "bAP"
# batch["cfgFile"] = "cfg_bAP.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params[('dendNaScale')] = [0.0, 0.1] 
# params[('dendKScale')]  = [0.0, 1.0] 
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp_glutSpread
# batch = {}
# batch["label"] = "glutAmp_glutSpread"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = [1.0, 1.2, 1.4, 1.6, 1.8] #list(1.0 * np.array(glutAmps))
# params["glutSpread"] = [1.0, 5.0]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutSpread
# batch = {}
# batch["label"] = "glutSpread_glutDecay"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutDecay"] = [1.0, 5.0, 10.0]
# params["glutSpread"] = [1.0, 5.0, 10.0, 20.0]
# batch["params"] = params
# batches[batch["label"]] = batch


# # Varying glutAmp_glutLoc
# batch = {}
# batch["label"] = "glutLoc_glutAmp"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(1.0 * np.array(glutAmps))
# params["glutLoc"] = [0.2, 0.4, 0.6, 0.8]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp_glutDecay
# batch = {}
# batch["label"] = "glutDecay_glutAmp"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(1.0 * np.array(glutAmps))
# params["glutDecay"] = [0.0, 1.0, 5.0, 10.0, 20.0]
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
		batch_utils.run_batch(**batch)

	stop = time.time()
	print
	print("Completed my_batches.py")
	print("Duration (s): " + str(stop-start))
	print
	
	import psutil
	print("Current process:")
	print(psutil.Process())
	
	if 'python' not in psutil.Process().name():
		print("Parent process:")
		print(psutil.Process().parent())
		print("Attempting to terminate grandparent process:")
		print(psutil.Process().parent().parent())
		psutil.Process().parent().parent().terminate()


