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

numsyns = cfg.glutSpread

#glutAmps = [0.045, 0.050, 0.055, 0.060, 0.065, 0.070, 0.075]
glutAmps = [0.075]

###############################################################################
# Batches 
# -------
# 
###############################################################################

batches = {}

# Varying glutamate stim amplitude (1D batch)
batch = {}
batch["label"] = "Control"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["glutAmp"] = list(np.array(glutAmps) / numsyns)
batch["params"] = params
batches[batch["label"]] = batch


# # No mgblock, varying glutamate stim amplitude (1D batch)
# batch = {}
# batch["label"] = "NoMgBlock"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams_nomgb.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.array(glutAmps) / numsyns)
# batch["params"] = params
# batches[batch["label"]] = batch


# # Varying glutamate stim amplitude and ratioAMPANMDA
# batch = {}
# batch["label"] = "glutAmp_ratioAMPANMDA"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.array(glutAmps) / numsyns)
# params["ratioAMPANMDA"] = [0.2, 1.0, 10.0]
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
	print("Completed eee/sim/batches/batch_plat_overlay/my_batches.py")
	print("Duration (s): " + str(stop-start))
	print("Please close this terminal and open another.")

