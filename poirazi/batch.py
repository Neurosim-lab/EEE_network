from netpyne import specs
from netpyne.batch import Batch 
import os

batchLabel = 'batch43'

#runType = 'hpc_slurm' # Either 'hpc_slurm' or 'mpi_bulletin'
runType = 'mpi_bulletin' # Either 'hpc_slurm' or 'mpi_bulletin'

runFolder = '/Users/graham/EEE_network/poirazi/'
#runFolder = '/home/jwgraham/EEE_network/eee_net/'
#runFolder = '/home1/06322/tg856217/EEE_network/eee_net/'

saveFolder = 'output' # For running on a local machine
dataFolder = 'batch_data'
figFolder  = 'batch_figures'
#saveFolder = '/oasis/scratch/comet/jwgraham/temp_project/EEE_network/eee_net/'  # Comet
#saveFolder = '/scratch/06322/tg856217/'  # Stampede

#allocation = 'csd403'         # NSG on Comet
#allocation = 'TG-IBN140002'   # NSG on Stampede

batchSaveFolder = os.path.join(saveFolder, batchLabel, dataFolder)
if not os.path.isdir(batchSaveFolder):
    os.makedirs(batchSaveFolder, exist_ok=True)


def batchRun():
    # Create variable of type ordered dictionary (NetPyNE's customized version) 
    params = specs.ODict()   

    # fill in with parameters to explore and range of values (key has to coincide with a variable in simConfig) 

    params['pyrInjectAmp'] = [0.32, 0.33, 0.34]
    params['stimScale'] = [50.0]

    #params['noise'] = [False, True]

    #params['numSynsPyrInh'] = [2, 4, 6, 8]  # Default: 2
    #params['pyrInjectAmp'] = [0.8, 1.0, 1.2, 1.4]
    


    # create Batch object with paramaters to modify, and specifying files to use
    b = Batch(params=params, cfgFile='cfg.py', netParamsFile='netParams.py')
    
    # Set output folder, grid method (all param combinations), and run configuration
    b.batchLabel = batchLabel 
    b.method = 'grid'
    b.saveFolder = batchSaveFolder
    
    if runType == 'hpc_slurm':
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
    import batch_analysis as bp
    bp.plot_vtraces(batchLabel)

    #import batch_analysis as ba
    #batch = ba.plot_vtraces(batchLabel, batchdatadir=saveFolder, outputdir=os.path.join(saveFolder, b.batchLabel))


