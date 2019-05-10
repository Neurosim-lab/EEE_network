from netpyne import specs
from netpyne.batch import Batch 
import os

runType = 'mpi_bulletin' # Either 'hpc_slurm' or 'mpi_bulletin'
batchLabel = 'v01_batch10_local'

def batchRun():
	# Create variable of type ordered dictionary (NetPyNE's customized version) 
	params = specs.ODict()   

	# fill in with parameters to explore and range of values (key has to coincide with a variable in simConfig) 
	
	params['EEconv'] = [1.5, 3.0, 6.0] # Default 3.0
	params['IEconv'] = [6.0, 12.0, 24.0] # Default 12.0

	#params['ampIClamp1'] = [0.1, 0.5, 1.0]
	#params['GABAAfastWeight'] = [0.0001, 0.01, 1.0]   
	#params['GABAAslowWeight'] = [0.0001, 0.001, 0.01]

	# create Batch object with paramaters to modify, and specifying files to use
	b = Batch(params=params, cfgFile='cfg.py', netParamsFile='netParams.py')
	
	# Set output folder, grid method (all param combinations), and run configuration
	b.batchLabel = batchLabel 
	b.method = 'grid'
	
	if runType == 'hpc_slurm':
		b.saveFolder = '/oasis/scratch/comet/jwgraham/temp_project/EEE_network/eee_net/' + b.batchLabel
		b.runCfg = {'type': 'hpc_slurm',
					'allocation': 'shs100', 
					'walltime': '03:00:00',
					'nodes': 10,
					'coresPerNode': 24,
					'email': 'joe.w.graham@gmail.com',
					'folder': '/home/jwgraham/EEE_network/eee_net/',
					'script': 'init.py', 
					'mpiCommand': 'ibrun',
					'skip': True}
	elif runType == 'mpi_bulletin':
		if not os.path.isdir('batch_data'):
			os.mkdir('batch_data')
		b.saveFolder = 'batch_data/' + b.batchLabel
		b.runCfg = {'type': 'mpi_bulletin', 
					'script': 'init.py', 
					'skip': True}
	else:
		raise Exception("Problem in batch file: runType must be either 'hpc_slurm' or 'mpi_bulletin'.")

	# Run batch simulations
	b.run()

# Main code
if __name__ == '__main__':
	batchRun() 



