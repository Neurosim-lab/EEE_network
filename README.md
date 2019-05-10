# EEE_network

## Prepare for simulations

1. Clone the repo (`git clone https://github.com/Neurosim-lab/EEE_network.git`)
2. Compile the mod files (`cd EEE_network/mod ; nrnivmodl`)
3. Symlink the mod dir (`cd ../eee_net ; ln -s "../mod/x86_64" x86_64`)
	


## Running simulations using MPI

### To run a single sim using MPI 

1. Change to the 'eee_net' directory (`cd EEE_network/eee_net`)
2. Two options to run sim:
	1. Execute `mpiexec -np #processes nrniv -python -mpi init.py` after replacing #processes with the number of processes you want to use (e.g. `mpiexec -np 4 nrniv -python -mpi init.py`)
	2. Execute `runsim #processes` (e.g. `./runsim 4`)

### To run a batch of sims using MPI 

1. Change to the 'eee_net' directory (`cd EEE_network/eee_net`)
2. Open 'batch.py'
3. Ensure `runType = mpi_bulletin`
4. Update the `batchLabel`
5. Two options to run batch:
	1. Execute `mpiexec -np #processes nrniv -python -mpi batch.py` (e.g. `mpiexec -np 4 nrniv -python -mpi batch.py`)
	2. Execute `runbatch #processes` (e.g. `./runbatch 4`)



## Running simulations on Comet

### To run a single sim on Comet

1. Change to the 'eee_net' directory (`cd EEE_network/eee_net`)
2. Modify the file `runsim_comet` to your settings
3. Execute `sbatch runsim_comet`

### To run a batch of simulations on Comet

1. Change to the 'eee_net' directory (`cd EEE_network/eee_net`)
2. Open 'batch.py'
3. Ensure `runType = hpc_slurm`
4. Update the `batchLabel`
5. Execute `python batch.py`


