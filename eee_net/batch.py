from netpyne import specs
from netpyne.batch import Batch 
import os

batchLabel = 'v01_batch57'

runType = 'hpc_slurm' # Either 'hpc_slurm' or 'mpi_bulletin'
#runType = 'mpi_bulletin' # Either 'hpc_slurm' or 'mpi_bulletin'

#runFolder = '/home/jwgraham/EEE_network/eee_net/'
runFolder = '/home1/06322/tg856217/EEE_network/eee_net'

#saveFolder = '/oasis/scratch/comet/jwgraham/temp_project/EEE_network/eee_net/'
saveFolder = '/scratch/06322/tg856217/'

#allocation = 'csd403'         # NSG on Comet
allocation = 'TG-IBN140002'   # NSG on Stampede


def batchRun():
    # Create variable of type ordered dictionary (NetPyNE's customized version) 
    params = specs.ODict()   

    # fill in with parameters to explore and range of values (key has to coincide with a variable in simConfig) 
    
    #params['EEconn'] = [0.05, 0.1, 0.2]
    #params['IEconn'] = [0.1, 0.2, 0.3]

    #params['numCells'] = [10, 100, 500, 1000, 5000, 10000]

    params['PT5_std_scaling'] = [0.0, 0.1]
    params['ampIClamp2'] = [0.3, 0.5, 0.7]
     
    
    # create Batch object with paramaters to modify, and specifying files to use
    b = Batch(params=params, cfgFile='cfg.py', netParamsFile='netParams.py')
    
    # Set output folder, grid method (all param combinations), and run configuration
    b.batchLabel = batchLabel 
    b.method = 'grid'
    
    if runType == 'hpc_slurm':
        b.saveFolder = saveFolder + b.batchLabel
        b.runCfg = {'type': 'hpc_slurm',
                    'allocation': allocation, 
                    'walltime': '00:30:00',
                    'nodes': 4,
                    'coresPerNode': 48,
                    'email': 'joe.w.graham@gmail.com',
                    'folder': runFolder,
                    'script': 'init.py', 
                    'mpiCommand': 'ibrun',
                    'skip': True,
                    'custom': '#SBATCH -p skx-normal'}
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



