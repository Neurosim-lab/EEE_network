"""
my_batches.py 
Batch simulations for EEE project
contact: joe.w.graham@gmail.com
"""

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

# Varying glutAmp
batch = {}
batch["label"] = "glutAmp5"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["glutAmp"] = list(np.linspace(0.6, 0.9, 5))
batch["params"] = params
batches[batch["label"]] = batch

# # Varying glutAmp
# batch = {}
# batch["label"] = "glutAmp"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = [0.6, 0.8, 1.0]
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


# # Varying glutAmp and NMDABetaScale
# batch = {}
# batch["label"] = "NMDABetaScale_glutAmp"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = [0.5, 0.7, 0.9]
# params["NMDABetaScale"] = [0.25, 1.0, 4.0]
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

# # Varying glutAmp
# batch = {}
# batch["label"] = "glutAmp_Na"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(1.0 * np.array(glutAmps))
# params["allNaScale"] = [0.0, 1.0]
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
		print
		batch_utils.run_batch(**batch)

	stop = time.time()
	print
	print("Completed eee/sim/batches/batch_sfn2017/my_batches.py")
	print("Duration (s): " + str(stop-start))
	print("Please close this terminal and open another.")


