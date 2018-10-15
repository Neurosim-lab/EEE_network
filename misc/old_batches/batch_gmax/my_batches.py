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

#glutAmps = [0.007, 0.008, 0.009, 0.010, 0.012, 0.013, 0.014]
glutAmps = [0.004, 0.0045, 0.0050, 0.0055, 0.0060, 0.0065, 0.0070]

###############################################################################
# Batches 
# ------- 
# 
###############################################################################

batches = {}

# Varying glutamate stim amplitude (1D batch)
batch = {}
batch["label"] = "glutAmp"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["glutAmp"] = glutAmps
batch["params"] = params
batches[batch["label"]] = batch

# Varying glutamate stim location (1D batch)
batch = {}
batch["label"] = "glutLoc"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["glutLoc"] = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
batch["params"] = params
batches[batch["label"]] = batch

# Varying ratioAMPANMDA (1D batch)
batch = {}
batch["label"] = "ratioAMPANMDA"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["ratioAMPANMDA"] = [0.02, 0.2, 1.0, 2.0, 3.0, 4.0, 10.0]
batch["params"] = params
batches[batch["label"]] = batch

# Varying glutSpread -- default 10.0 microns, diameter of glutamate puff (1D batch)
batch = {}
batch["label"] = "glutSpread"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["glutSpread"] = [1.0, 2.5, 5.0, 10.0, 20.0]
batch["params"] = params
batches[batch["label"]] = batch

# Varying glutDelay -- default 1.0 ms/um delay in glutamate activation (1D batch)
batch = {}
batch["label"] = "glutDelay"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["glutDelay"] = [0.0, 1.0, 2.5, 5.0, 10.0]
batch["params"] = params
batches[batch["label"]] = batch

# Varying glutDecay -- default 10.0 %/um decrease in glutamate amplitude (1D batch)
batch = {}
batch["label"] = "glutDecay"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["glutDecay"] = [0.0, 5.0, 10.0, 15.0, 20.0]
batch["params"] = params
batches[batch["label"]] = batch

# Turning Na conductance on and off (TTX) (1D batch)
batch = {}
batch["label"] = "allNaScale"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["allNaScale"] = [0.0, 1.0]
batch["params"] = params
batches[batch["label"]] = batch

# Varying glutamate stim amplitude and location (2D batch)
batch = {}
batch["label"] = "glutAmp_glutLoc"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["glutAmp"] = glutAmps
params["glutLoc"] = [0.1, 0.3, 0.5, 0.7, 0.9]
batch["params"] = params
batches[batch["label"]] = batch









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
	print("Completed eee/sim/batches/batch_gmax/my_batches.py")
	print("Duration (s): " + str(stop-start))
	print("Please close this terminal and open another.")


