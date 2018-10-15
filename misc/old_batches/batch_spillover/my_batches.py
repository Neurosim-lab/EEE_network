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
glutAmps = [0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]

numsyns = cfg.glutSpread


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

# Varying glutamate stim amplitude and NMDAAlphaScale
batch = {}
batch["label"] = "glutAmp_NMDAAlphaScale"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["glutAmp"] = list(np.array(glutAmps) / numsyns)
params["NMDAAlphaScale"] = [0.1, 0.5, 1.0, 2.0, 10.0]
batch["params"] = params
batches[batch["label"]] = batch

# Varying glutamate stim amplitude
batch = {}
batch["label"] = "glutAmp"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["glutAmp"] = list(np.array(glutAmps) / numsyns)
batch["params"] = params
batches[batch["label"]] = batch

# Varying glutamate amplitude and Cdur in synaptic NMDA receptors
batch = {}
batch["label"] = "glutAmp_Cdur"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["glutAmp"] = list(np.array(glutAmps) / numsyns)
params["CdurNMDAScale"] = [0.01, 0.1, 1, 10, 100]
batch["params"] = params
batches[batch["label"]] = batch

# Varying Cdur in synaptic NMDA receptors
batch = {}
batch["label"] = "Cdur"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["CdurNMDAScale"] = [0.01, 0.1, 1, 10, 100]
batch["params"] = params
batches[batch["label"]] = batch

# Varying Cmax in synaptic NMDA receptors
batch = {}
batch["label"] = "Cmax"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["CmaxNMDAScale"] = [0.01, 0.1, 1, 10, 100]
batch["params"] = params
batches[batch["label"]] = batch

# Varying Cdur in synaptic and extrasynaptic NMDA receptors
batch = {}
batch["label"] = "Cdur_CdurES"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["CdurNMDAScale"] = [0.1, 1, 10, 100]
params["CdurNMDAesScale"] = [0.1, 1, 10, 100]
batch["params"] = params
batches[batch["label"]] = batch

# Varying Cmax in synaptic and extrasynaptic NMDA receptors
batch = {}
batch["label"] = "Cmax_CmaxES"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["CmaxNMDAScale"] = [0.1, 1, 10, 100]
params["CmaxNMDAesScale"] = [0.1, 1, 10, 100]
batch["params"] = params
batches[batch["label"]] = batch

# Varying glutamate stim amplitude (1D batch)
batch = {}
batch["label"] = "glutAmp"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["glutAmp"] = list(np.array(glut_stim_weight) * glut_stim_scale / numsyns)
batch["params"] = params
batches[batch["label"]] = batch

# Varying glutamate stim spine number (0 near soma)
batch = {}
batch["label"] = "glutSpine"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["glutSpine"] = [0, 50, 100, 150, 200, 250]
batch["params"] = params
batches[batch["label"]] = batch

# Varying glutamate spread (how many spines activated)
batch = {}
batch["label"] = "glutSpread"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["glutSpread"] = [1, 10, 20, 50, 100]
batch["params"] = params
batches[batch["label"]] = batch

# Varying glutamate spread smaller range (how many spines activated)
batch = {}
batch["label"] = "glutSpreadLow"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["glutSpread"] = [1, 2, 4, 8, 16]
batch["params"] = params
batches[batch["label"]] = batch

# Varying glutamate spill delay
batch = {}
batch["label"] = "spillDelay"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["spillDelay"] = [0., 5., 10., 15., 20.]
batch["params"] = params
batches[batch["label"]] = batch

# Varying glutamate spill fraction
batch = {}
batch["label"] = "spillFraction"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["spillFraction"] = [0.0, 0.05, 0.10, 0.15, 0.20]
batch["params"] = params
batches[batch["label"]] = batch

# Varying glutamate spill fraction, making it bigger
batch = {}
batch["label"] = "spillFractionBig"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["spillFraction"] = [0.0, 0.25, 0.50, 0.75, 1.0]
batch["params"] = params
batches[batch["label"]] = batch

# Varying glutamate stim amplitude and glutamate stim spine number (0 near soma)
batch = {}
batch["label"] = "glutAmp_glutSpine"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["glutAmp"] = list(np.array(glut_stim_weight) * glut_stim_scale / numsyns)
params["glutSpine"] = [0, 50, 100, 150, 200, 250]
batch["params"] = params
batches[batch["label"]] = batch

# Varying glutamate stim amplitude and glutamate spread
batch = {}
batch["label"] = "glutAmp_glutSpread"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["glutAmp"] = list(np.array(glut_stim_weight) * glut_stim_scale / numsyns)
params["glutSpread"] = [1, 10, 20, 50, 100]
batch["params"] = params
batches[batch["label"]] = batch

# Varying glutamate stim amplitude and glutamate spread (lower values)
batch = {}
batch["label"] = "glutAmp_glutSpreadLow"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["glutAmp"] = list(np.array(glut_stim_weight) * glut_stim_scale / numsyns)
params["glutSpread"] = [1, 2, 4, 8, 16]
batch["params"] = params
batches[batch["label"]] = batch

# Varying glutamate stim amplitude and glutamate spill delay
batch = {}
batch["label"] = "glutAmp_spillDelay"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["glutAmp"] = list(np.array(glut_stim_weight) * glut_stim_scale / numsyns)
params["spillDelay"] = [0., 5., 10., 15., 20.]
batch["params"] = params
batches[batch["label"]] = batch

# Varying glutamate stim amplitude and glutamate spill fraction
batch = {}
batch["label"] = "glutAmp_spillFraction"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["glutAmp"] = list(np.array(glut_stim_weight) * glut_stim_scale / numsyns)
params["spillFraction"] = [0.0, 0.05, 0.10, 0.15, 0.20]
batch["params"] = params
batches[batch["label"]] = batch

# Varying glutamate stim spine number and glutamate spread
batch = {}
batch["label"] = "glutSpine_glutSpread"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["glutSpine"] = [0, 50, 100, 150, 200]
params["glutSpread"] = [1, 10, 20, 50]
batch["params"] = params
batches[batch["label"]] = batch

# Varying glutamate stim spine number and spill delay
batch = {}
batch["label"] = "glutSpine_spillDelay"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["glutSpine"] = [0, 50, 100, 150, 200]
params["spillDelay"] = [0., 5., 10., 15., 20.]
batch["params"] = params
batches[batch["label"]] = batch

# Varying glutamate stim spine number and spill fraction
batch = {}
batch["label"] = "glutSpine_spillFraction"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["glutSpine"] = [0, 50, 100, 150, 200]
params["spillFraction"] = [0.0, 0.05, 0.10, 0.15, 0.20]
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
	print("Completed eee/sim/batches/batch_spillover/my_batches.py")
	print("Duration (s): " + str(stop-start))
	print("Please close this terminal and open another.")

