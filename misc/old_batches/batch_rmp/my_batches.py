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

glutAmps = [0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
NMDAlocs = [0.1, 0.3, 0.5, 0.7, 0.9]


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
params["glutAmp"] = list(np.array(glutAmps) / numsyns)
batch["params"] = params
batches[batch["label"]] = batch

# Varying e_pas (passive reversal potential)
batch = {}
batch["label"] = "epas"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["epas"] = [-100.0, -90.0, -80.0, -70.0, -60.0, -50.0]
batch["params"] = params
batches[batch["label"]] = batch

# Varying glutamate stim amplitude and e_pas (passive reversal potential)
batch = {}
batch["label"] = "glutAmp_epas"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["glutAmp"] = list(np.array(glutAmps) / numsyns)
params["epas"] = [-100.0, -90.0, -80.0, -70.0, -60.0, -50.0]
batch["params"] = params
batches[batch["label"]] = batch















# # Varying glutamate stim location and glutamate stim amplitude
# batch = {}
# batch["label"] = "glutLoc_glutAmp"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params[('NetStim1', 'loc')] = NMDAlocs
# params["glutAmp"] = list(np.array(glutAmps) / numsyns)
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutamate stim spine number (0 near soma)
# batch = {}
# batch["label"] = "glutSpine"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutSpine"] = [0, 50, 100, 150, 200, 250]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutamate spread (how many spines activated)
# batch = {}
# batch["label"] = "glutSpread"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutSpread"] = [1, 10, 20, 50, 100]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutamate spread smaller range (how many spines activated)
# batch = {}
# batch["label"] = "glutSpreadLow"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutSpread"] = [1, 2, 4, 8, 16]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutamate stim amplitude and glutamate spread
# batch = {}
# batch["label"] = "glutAmp_glutSpread"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.array(glutAmps) / numsyns)
# params["glutSpread"] = [1, 10, 20, 50, 100]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutamate stim amplitude and glutamate spread (lower values)
# batch = {}
# batch["label"] = "glutAmp_glutSpreadLow"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.array(glutAmps) / numsyns)
# params["glutSpread"] = [1, 2, 4, 8, 16]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutamate stim spine number and glutamate spread
# batch = {}
# batch["label"] = "glutSpine_glutSpread"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutSpine"] = [0, 50, 100, 150, 200]
# params["glutSpread"] = [1, 10, 20, 50]
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
	print("Completed eee/sim/batches/batch_rmp/my_batches.py")
	print("Duration (s): " + str(stop-start))
	print("Please close this terminal and open another.")

