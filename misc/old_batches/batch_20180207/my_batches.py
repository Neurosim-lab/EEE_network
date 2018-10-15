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

# Varying glutAmp
batch = {}
batch["label"] = "glutAmp"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["glutAmp"] = list(np.linspace(0.0, 2.0, 20).round(2))
batch["params"] = params
batches[batch["label"]] = batch

# # Turning dendritic Na and K on and off for bAPs
# batch = {}
# batch["label"] = "bap"
# batch["cfgFile"] = "cfg_bAP.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params[('dendNaScale')] = [0.0, 1.0] 
# params[('dendKScale')]  = [0.0, 1.0] 
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


