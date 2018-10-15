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

#glutAmps = [0.007, 0.008, 0.009, 0.010, 0.012, 0.013, 0.014]
glutAmps = [0.004, 0.0045, 0.0050, 0.0055, 0.0060, 0.0065, 0.0070]
glutAmps = [0.02, 0.04, 0.06, 0.08, 0.10, 0.12]
glutAmps2 = [0.14, 0.16, 0.18, 0.20, 0.22, 0.24]

###############################################################################
# Batches 
# ------- 
# 
###############################################################################

batches = {}

# Varying epas
batch = {}
batch["label"] = "epas"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["e_pas"] = [-90.0, -85.0, -80.0, -75.0, -70.0, -65.0]
batch["params"] = params
batches[batch["label"]] = batch

# # Varying glutAmp
# batch = {}
# batch["label"] = "glutAmp"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(1.0 * np.array(glutAmps))
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp higher
# batch = {}
# batch["label"] = "glutAmp2"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(1.0 * np.array(glutAmps2))
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp_epas
# batch = {}
# batch["label"] = "epas_glutAmp"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(1.0 * np.array(glutAmps))
# params["e_pas"] = [-90.0, -80.0, -70.0, -60.0]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp2_epas
# batch = {}
# batch["label"] = "epas_glutAmp2"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(1.0 * np.array(glutAmps2))
# params["e_pas"] = [-90.0, -80.0, -70.0, -60.0]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp_RmScale 
# batch = {}
# batch["label"] = "RmScale_glutAmp"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(1.0 * np.array(glutAmps))
# params["RmScale"] = [1.0, 5.0, 10.0, 20.0]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp2_RmScale 
# batch = {}
# batch["label"] = "RmScale_glutAmp2"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(1.0 * np.array(glutAmps2))
# params["RmScale"] = [1.0, 5.0, 10.0, 20.0]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp_glutSpread
# batch = {}
# batch["label"] = "glutSpread_glutAmp"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(1.0 * np.array(glutAmps))
# params["glutSpread"] = [1.0, 5.0, 10.0, 25.0, 50.0]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp2_glutSpread
# batch = {}
# batch["label"] = "glutSpread_glutAmp2"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(1.0 * np.array(glutAmps2))
# params["glutSpread"] = [1.0, 5.0, 10.0, 25.0, 50.0]
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

# # Varying glutAmp2_glutLoc
# batch = {}
# batch["label"] = "glutLoc_glutAmp2"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(1.0 * np.array(glutAmps2))
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

# # Varying glutAmp2_glutDecay
# batch = {}
# batch["label"] = "glutDecay_glutAmp2"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(1.0 * np.array(glutAmps2))
# params["glutDecay"] = [0.0, 1.0, 5.0, 10.0, 20.0]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying IClamp1 amplitude
# batch = {}
# batch["label"] = "ampIClamp1"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["ampIClamp1"] = [-0.005, -0.0005, -0.00005]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying ih on/off and glutAmps
# batch = {}
# batch["label"] = "ih_glutAmp"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["ihScale"] = [0.0, 1.0]
# params["glutAmp"] = glutAmps
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
	print("Completed eee/sim/batches/batch_glutdyn/my_batches.py")
	print("Duration (s): " + str(stop-start))
	print("Please close this terminal and open another.")


