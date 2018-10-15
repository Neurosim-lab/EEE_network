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

glutAmps = [0.045, 0.050, 0.055, 0.060, 0.065, 0.070, 0.075]


###############################################################################
# Batches 
# -------
# 
###############################################################################

batches = {}

# Turning dendritic Na and K on and off for bAPs
batch = {}
batch["label"] = "bap"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams_bAP.py"
params = OrderedDict()
params['dendNaScale'] = [0.0, 1.0]
params['dendKScale']  = [0.0, 1.0]
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
	print("Completed eee/sim/batches/batch_bap/my_batches.py")
	print("Duration (s): " + str(stop-start))
	print("Please close this terminal and open another.")

