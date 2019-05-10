"""
batch_init.py
Script for use with EEE batch simulations

Originally from:
init.py
Starting script to run NetPyNE-based model.
Usage:  python init.py  # Run simulation, optionally plot a raster
MPI usage:  mpiexec -n 4 nrniv -python -mpi init.py
Contributors: salvadordura@gmail.com
"""

from netpyne import sim

# read cfg and netParams from command line arguments
# if there are no command line args, looks for cfg.py and netParams.py in curdir
# Reads command line arguments using syntax: python file.py [simConfig=filepath] [netParams=filepath]
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

# give different random seeds for Gfluctp in each cell
PT5 = ['PT5_0','PT5_1', 'PT5_2', 'PT5_3', 'PT5_4', 'PT5_5','PT5_6','PT5_7','PT5_8','PT5_9','PT5_10']

for i,v in enumerate(PT5):
    for c in sim.net.cells:
            if c.tags['pop'] in v:                  
                for isec,sec in c.secs.iteritems():
                    if isec == 'soma_2':
                        for ip, pointp in enumerate(sec.pointps.values()):
                            if pointp['mod'] == 'Gfluctp':
                                pointp.hPointp.noiseFromRandom123(c.gid, len(c.conns), ip)

# setup variables to record for each cell (spikes, V traces, etc)
sim.setupRecording()

# run parallel Neuron simulation 
sim.runSim()

# gather spiking data and cell info from each node
sim.gatherData()

# save params, cell info and sim output to file (pickle,mat,txt,etc)
sim.saveData()

# plot spike raster
sim.analysis.plotData()

