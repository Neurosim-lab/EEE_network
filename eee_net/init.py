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

def initRand(): 
    for c in sim.net.cells:
        noise = c.secs['soma']['pointps']['noise']
        seed1 = noise['seed1']
        seed2 = noise['seed2']
        seed3 = noise['seed3']
        noise['hObj'].noiseFromRandom123(seed1, seed2, seed3)


sim.initialize(
    simConfig = cfg,    
    netParams = netParams)    # create network object and set cfg and net params
sim.net.createPops()          # instantiate network populations
sim.net.createCells()         # instantiate network cells based on defined populations
sim.net.connectCells()        # create connections between cells based on params
sim.net.addStims()            # add network stimulation

#initRand()                    # set the seeds for randomization of Gfluctp

sim.setupRecording()          # setup variables to record (spikes, V traces, etc)
sim.runSim()                  # run parallel Neuron simulation  
sim.gatherData()              # gather spiking data and cell info from each node
sim.saveData()                # save params, cell info and sim output to file
sim.analysis.plotData()       # plot spike raster etc

# Additional analyses

includePre  = ['PT5_1', 'PT5_2', 'PT5_3', 'PT5_4','PV5']
includePost = ['PT5_1', 'PT5_2', 'PT5_3', 'PT5_4','PV5']
feature     = 'numConns' #'divergence' #'convergence' #'strength' # 
groupBy     = 'pop' #'cell'
orderBy     = 'gid' #'y'
synOrConn   = 'conn' #'syn'

sim.analysis.plotConn(saveFig=True, showFig=False, saveData=True, includePre=includePre, includePost=includePost, feature=feature, groupBy=groupBy, orderBy=orderBy, synOrConn=synOrConn)




