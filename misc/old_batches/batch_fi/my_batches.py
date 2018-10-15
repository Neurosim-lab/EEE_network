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
glut_stim_weight = [0.010, 0.011, 0.012, 0.013, 0.014]
#glut_stim_weight = [0.05, 0.06, 0.07, 0.08, 0.09]


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

# # Varying current clamp amplitude for fI calculation
# batch = {}
# batch["label"] = "fi_curve"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params[("IClamp1", "amp")] = [0.05, 0.15, 0.25, 0.35, 0.45]
# params[('NetStim1', 'weight', 0)] = [0.0]
# #params["dendNa"] = [0.000345, 0.00345, 0.0345]
# batch["params"] = params
# batches[batch["label"]] = batch

# Varying NMDA decay time constant and glutamate stim amplitude
batch = {}
batch["label"] = "NMDAdecay_glut"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["tau2NMDA"] = [150, 300, 600, 900, 1200]
params[('NetStim1', 'weight', 0)] = list(np.array(glut_stim_weight) * 1.0)
batch["params"] = params
batches[batch["label"]] = batch


# Varying NMDA rise time constant and glutamate stim amplitude
batch = {}
batch["label"] = "NMDArise_glut"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["tau1NMDA"] = [1, 5, 15, 30, 60]
params[('NetStim1', 'weight', 0)] = list(np.array(glut_stim_weight) * 1.0)
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
	print("Completed eee/sim/batches/batch_fi/my_batches.py")
	print("Duration (s): " + str(stop-start))
	print("Please close this terminal and open another.")

