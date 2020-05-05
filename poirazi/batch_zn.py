from netpyne import specs
from netpyne.batch import Batch 
import os

batchLabel = 'batch_zn_01'

#runType = 'hpc_slurm' # Either 'hpc_slurm' or 'mpi_bulletin'
runType = 'mpi_bulletin' # Either 'hpc_slurm' or 'mpi_bulletin'

#runFolder = '/Users/graham/EEE_network/poirazi/'           # For local machine
runFolder = '/u/graham/EEE_network/poirazi/'                # For Neurosim machines
#runFolder = '/home/jwgraham/EEE_network/eee_net/'          # For Comet 
#runFolder = '/home1/06322/tg856217/EEE_network/eee_net/'   # For Stampede

saveFolder = 'output' 
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

    params['connProb'] = [0.0, 0.25, 0.5, 0.75, 1.0]
    params['noise'] = [False, True]

    #params['connProbPyrPyr'] = [0.1, 0.2, 0.3]
    #params['BkgPyrScale'] = [1.8, 2.0, 2.2]

    #params['BkgPyrScale'] = [1.8, 2.0, 2.2]
    #params['BkgInhScale'] = [1.8, 2.0, 2.2]

    #params['BkgScale'] = [1.25, 1.5, 1.75] 
    #params['noise'] = [False, True]
    
    #params['BkgPyrAMPAweight'] = [1.0, 2.0, 10.0] 
    #params['BkgPyrNMDAweight'] = [1.0, 2.0, 10.0]

    #params['numSynsInhPyr'] = [4, 3, 2, 1, 0]
    #params['noise'] = [False, True]

    #params['BkgPyrAMPAweight'] = [0.00019, 1.5*0.00019, 2.0*0.00019]
    #params['BkgPyrNMDAweight'] = [0.585, 1.5*0.585, 2.0*0.585]

    #params['pyrInjectAmp'] = [0.32, 0.33, 0.34]
    #params['stimScale'] = [50.0]

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
    import batch_analysis as ba
    ba.plot_vtraces(batchLabel)

    #batch = ba.plot_vtraces(batchLabel, batchdatadir=saveFolder, outputdir=os.path.join(saveFolder, b.batchLabel))
