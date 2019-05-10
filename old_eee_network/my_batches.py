"""
batches.py 
Batch simulations for EEE project
contact: joe.w.graham@gmail.com
"""

from collections import OrderedDict
import os
from cfg import cfg
from netpyne.batch import Batch

batchoutputdir = "batch_data"
if not os.path.exists(batchoutputdir):
	os.mkdir(batchoutputdir)

def run_batch(label, params, cfgFile, netParamsFile, batchdatadir="batch_data", grouped=None):
    """Runs a batch of simulations."""

    b = Batch(cfgFile=cfgFile, netParamsFile=netParamsFile)
    for k,v in params.iteritems():
        b.params.append({'label': k, 'values': v})
    if grouped is not None:
        for p in b.params:
            if p['label'] in grouped: 
                p['group'] = True
    b.batchLabel = label
    b.saveFolder = os.path.join(batchdatadir, b.batchLabel)
    b.method = 'grid'
    b.runCfg = {'type': 'mpi', 
                'script': 'init.py', #'batch_init.py', 
                'skip': True}
    b.run()


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


# Varying vinit_PV5
batch = {}
batch["label"] = "vinit_PV5_nonoise"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["vinit_PV5"] = [-85.0, -75.0, -65.0, -55.0, -45.0]
batch["params"] = params
batches[batch["label"]] = batch

# # Varying Gfluctp excitatory noise amp
# batch = {}
# batch["label"] = "exc_noise_amp_4"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["exc_noise_amp"] = list(0.22 * np.array([100.0, 200.0]))
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
		run_batch(**batch)

	stop = time.time()
	print
	print("Completed my_batches.py")
	print("Duration (s): " + str(stop-start))
