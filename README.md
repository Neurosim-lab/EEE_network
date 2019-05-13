# EEE_network

## Prepare for simulations

1. Clone the repo (`git clone https://github.com/Neurosim-lab/EEE_network.git`)
2. Compile the mod files (`cd EEE_network/mod ; nrnivmodl`)
3. Symlink the mod dir (`cd ../eee_net ; ln -s "../mod/x86_64" x86_64`)

Single line command:

`git clone https://github.com/Neurosim-lab/EEE_network.git ; cd EEE_network/mod ; nrnivmodl ; cd ../eee_net ; ln -s "../mod/x86_64" x86_64`
	


## Running simulations using MPI

### To run a single sim using MPI 

1. Change to the *eee_net* directory (`cd EEE_network/eee_net`)
2. Modify *cfg.py*
	1. Update sim label
	2. Set desired parameter values
3. Run the simulation (two options):
	1. Execute `runsim #processes` (e.g. `./runsim 4`)
	2. Execute `mpiexec -np #processes nrniv -python -mpi init.py` after replacing #processes with the number of processes you want to use (e.g. `mpiexec -np 4 nrniv -python -mpi init.py`)
	

### To run a batch of sims using MPI 

1. Change to the *eee_net* directory (`cd EEE_network/eee_net`)
2. Open *batch.py*
	1. Ensure `runType = mpi_bulletin`
	2. Update the `batchLabel`
3. Run the batch of sims (two options):
	1. Execute `runbatch #processes` (e.g. `./runbatch 4`)
	2. Execute `mpiexec -np #processes nrniv -python -mpi batch.py` (e.g. `mpiexec -np 4 nrniv -python -mpi batch.py`)




## Running simulations on Comet

### To run a single sim on Comet

1. Change to the *eee_net* directory (`cd EEE_network/eee_net`)
2. Modify *cfg.py*
	1. Update sim label
	2. Set desired parameter values
3. Modify the file *runsim_comet* to desired HPC settings
4. Execute `sbatch runsim_comet`

### To run a batch of simulations on Comet

1. Change to the *eee_net* directory (`cd EEE_network/eee_net`)
2. Open *batch.py*
	1. Ensure `runType = hpc_slurm`
	2. Update the `batchLabel`
	3. Set desired HPC settings in `runCfg`
5. Execute `python batch.py`


