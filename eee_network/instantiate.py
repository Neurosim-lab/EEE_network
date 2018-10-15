"""
instantiate.py
Script for use with EEE batch simulations

Originally from:
init.py
Starting script to run NetPyNE-based model.
Usage:  python init.py  # Run simulation, optionally plot a raster
MPI usage:  mpiexec -n 4 nrniv -python -mpi init.py
"""

from netpyne import sim

# read cfg and netParams from command line arguments
# if there are no command line args, looks for cfg.py and netParams.py in curdir
cfg, netParams = sim.readCmdLineArgs()

# create network object and set cfg and net params	
sim.initialize(simConfig = cfg, netParams = netParams)

# instantiate network populations 
sim.net.createPops()

# instantiate network cells based on defined populations
sim.net.createCells()

# create connections between cells based on params
sim.net.connectCells()

# add network stimulation
sim.net.addStims()

# setup variables to record for each cell (spikes, V traces, etc)								
sim.setupRecording()

# run parallel Neuron simulation 
#sim.runSim()

# gather spiking data and cell info from each node
#sim.gatherData()

# save params, cell info and sim output to file (pickle,mat,txt,etc)
#sim.saveData()

# plot spike raster
#sim.analysis.plotData()

