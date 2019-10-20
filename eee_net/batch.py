from netpyne import specs
from netpyne.batch import Batch 
import os

batchLabel = 'v02_batch05'

runType = 'hpc_slurm' # Either 'hpc_slurm' or 'mpi_bulletin'
#runType = 'mpi_bulletin' # Either 'hpc_slurm' or 'mpi_bulletin'

#runFolder = '/u/graham/EEE_network/eee_net/'
#runFolder = '/home/jwgraham/EEE_network/eee_net/'
runFolder = '/home1/06322/tg856217/EEE_network/eee_net/'

#saveFolder = '/u/graham/EEE_network/eee_net/data/'
#saveFolder = '/oasis/scratch/comet/jwgraham/temp_project/EEE_network/eee_net/'
saveFolder = '/scratch/06322/tg856217/'

#allocation = 'csd403'         # NSG on Comet
allocation = 'TG-IBN140002'   # NSG on Stampede


def batchRun():
    # Create variable of type ordered dictionary (NetPyNE's customized version) 
    params = specs.ODict()   

    # fill in with parameters to explore and range of values (key has to coincide with a variable in simConfig) 

    #params[''] = []
    #params[''] = []
    
    #params['EEconn'] = [0.05, 0.1, 0.2]
    #params['IEconn'] = [0.1, 0.2, 0.3]

    #params['numCells'] = [10, 100, 500, 1000, 5000, 10000]

    #params['ampIClamp2'] = [0.24, 0.25, 0.26] 
    #params['noisePV5'] = [True, False]

    #params['PT5_noise_amp'] = [0.1, 0.25, 0.5, 0.75, 1.0]
    #params['PT5_noise_std'] = [0.1, 0.25, 0.5, 0.75, 1.0]

    #params['ampIClamp1'] = [0.3, 0.4, 0.5, 0.6]
    #params['ampIClamp2'] = [0.3, 0.3125, 0.325, 0.375]

    #params['GABAAfastWeight'] = [0.01, 0.001, 0.0001, 0.00001]
    #params['NMDAweight'] = [0.02, 0.2, 2.0, 10.0]

    #params['EScale'] = [0.1, 0.5, 1.0, 5.0, 10.0]
    #params['IScale'] = [0.1, 0.5, 1.0, 5.0, 10.0]

    #params['glutAmp'] = [1.5, 2.0, 2.5]
    #params['noise_scale'] = [0.25, 1.0, 4.0]

    #params["seeds['stim']"] = [1234, 2345, 3456, 4567, 5678] # Didn't work

    params['seeds'] = [{'conn': 4123, 'stim': 1234, 'loc' : 3214}, 
                        {'conn': 4123, 'stim': 2345, 'loc' : 3214}, 
                        {'conn': 4123, 'stim': 3456, 'loc' : 3214}, 
                        {'conn': 4123, 'stim': 4567, 'loc' : 3214}, 
                        {'conn': 4123, 'stim': 5678, 'loc' : 3214}]



    
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
        if not os.path.isdir('data'):
            os.mkdir('data')
        b.saveFolder = 'data/' + b.batchLabel
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

    #import batch_analysis as ba
    #batch = ba.plot_vtraces(batchLabel, batchdatadir=saveFolder, outputdir=saveFolder + batchLabel)


