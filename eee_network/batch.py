"""
batch.py

Batch simulation for M1 model using NetPyNE

Contributors: salvadordura@gmail.com
"""
from netpyne.batch import Batch, specs
import numpy as np


# set configuration to run batch
def setRunCfg(b, type='mpi'):
	b.method = 'grid'

	if type=='mpi':
		b.runCfg = {'type': 'mpi',
			'script': 'init.py',
			'skip': True}

	elif type=='hpc_torque':
		b.runCfg = {'type': 'hpc_torque',
 			'script': 'init.py',
 			'nodes': 3,
 			'ppn': 8,
 			'walltime': "12:00:00",
 			'queueName': 'longerq',
 			'sleepInterval': 5,
 			'skip': True}

	elif type=='hpc_slurm':
		b.runCfg = {'type': 'hpc_slurm',
			'allocation': 'csd403',#'ib4iflp',# #'shs100',
			'walltime': '00:15:00',
			'nodes': 2,
			'coresPerNode': 24,
			'email': 'sergio.angulo@gmail.com',
			'folder': '/home/sangulo/projects/eee/sim/layersim/',
			'script': 'init.py',
			'mpiCommand': 'ibrun',
			'skip': True}


def EEbalance():
	params = specs.ODict()

	params["EEgain"] = [0.01, 0.1, 0.15, 0.2]
	params["glutAmp"] = [0.4,0.5,0.6]

	b = Batch(params=params, netParamsFile='netParams.py', cfgFile='cfg.py')

	grouped = []  # list of params that are grouped (vary together)
	for p in b.params:
		if p['label'] in grouped: p['group'] = True
	return b

def multi_params():
	params = specs.ODict()

	#params["EEgain"] = [0.0008, 0.001, 0.0012]
	params["IEgain"] = [0.035, 0.04, 0.045]#[0.04, 0.05, 0.06]
	params["EIgain"] = [0.8, 0.9, 1.0, 1.1, 1.2]#[0.15, 0.2, 0.25]
	#params["IIgain"] = [0.00005, 0.0001, 0.0002]#[0.00008, 0.0001, 0.00012]
	#params["exc_noise_amp"] = [0.18, 0.2, 0.22]
	#params["inh_noise_amp"] = [0.18, 0.2, 0.22]

	b = Batch(params=params, netParamsFile='netParams.py', cfgFile='cfg.py')#, groupedParams=grouped)

	grouped = []  # list of params that are grouped (vary together)
	for p in b.params:
		if p['label'] in grouped: p['group'] = True
	return b

def stim_batch():
	params = specs.ODict()

	params["glutAmp"] = [1.0, 1.5, 2.0]#, 2.0, 3.0]#, 4.0, 5.0]
	params["glutAmpExSynScale"] = [1.0, 1.5, 2.0]#, 2.0, 3.0]#, 4.0, 5.0] 
	#params["synLocMiddle"] = [0.2,0.5,0.8]
	#params["allNaScale"] = [1.0, 1.05, 1.1, 1.15, 1.2]
	#params["RaScale"] = [0.6, 0.65, 0.7]
	params['synTime2'] = [200, 250, 300, 350, 400, 500, 600]
	params['glutAmp2'] = [0.0, 1.0, 3.0, 5.0, 7.0]

	b = Batch(params=params, netParamsFile='netParams.py', cfgFile='cfg.py')#, groupedParams=grouped)

	grouped = ["glutAmp","glutAmpExSynScale"]  # list of params that are grouped (vary together)
	for p in b.params:
		if p['label'] in grouped: p['group'] = True
	return b



# ---------------------------------------------------------------------------------
# Main code
# ---------------------------------------------------------------------------------

b = stim_batch()

b.batchLabel = 'stim_batch6'

b.saveFolder = 'batch_data/'+b.batchLabel

setRunCfg(b, type='hpc_slurm')
#setRunCfg(b, type='mpi')

# run batch
b.run()
