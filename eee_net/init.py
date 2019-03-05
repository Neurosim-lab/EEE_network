"""
init.py

Usage:
    python init.py # Run simulation, optionally plot a raster

MPI usage:
    mpiexec -n 4 nrniv -python -mpi init.py

Contributors: salvadordura@gmail.com
"""

#import matplotlib; matplotlib.use('Agg')  # to avoid graphics error in servers
from netpyne import sim

cfg, netParams = sim.readCmdLineArgs()

#sim.createSimulateAnalyze()

sim.initialize(
    simConfig = cfg,    
    netParams = netParams)    # create network object and set cfg and net params
sim.net.createPops()          # instantiate network populations
sim.net.createCells()         # instantiate network cells based on defined populations
sim.net.connectCells()        # create connections between cells based on params
sim.net.addStims()            # add network stimulation
sim.setupRecording()          # setup variables to record (spikes, V traces, etc)
sim.runSim()                  # run parallel Neuron simulation  
sim.gatherData()              # gather spiking data and cell info from each node
sim.saveData()                # save params, cell info and sim output to file
sim.analysis.plotData()       # plot spike raster etc

# How to plot more than one figure of same type?  
# (e.g. raster arranged by y-position and also by 
# cell gid)  -- Salva: add function call at end 
# of init.py , eg. sim.analysis.plotRaster(...)