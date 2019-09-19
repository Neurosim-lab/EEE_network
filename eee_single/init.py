# nrniv -python init.py

#import matplotlib; matplotlib.use('Agg')  # to avoid graphics error in servers
from neuron import h
from netpyne import sim

cfg, netParams = sim.readCmdLineArgs()

sim.initialize(simConfig = cfg,netParams = netParams)
sim.net.createPops()          # instantiate network populations
sim.net.createCells()         # instantiate network cells based on defined populations
sim.net.connectCells()        # create connections between cells based on params
sim.net.addStims()            # add network stimulation
sim.setupRecording()          # setup variables to record (spikes, V traces, etc)
sim.runSim()                  # run parallel Neuron simulation  
sim.gatherData()              # gather spiking data and cell info from each node
sim.saveData()                # save params, cell info and sim output to file
sim.analysis.plotData()       # plot spike raster etc

print("================ SEEDS ================: ",h.Gfluctp[0].seed1, h.Gfluctp[0].seed2, h.Gfluctp[0].seed3)
print("Final voltage in soma: ",sim.net.cells[0].secs.soma.hObj(0.5).v)

# How to plot more than one figure of same type?  
# (e.g. raster arranged by y-position and also by 
# cell gid)  -- Salva: add function call at end 
# of init.py , eg. sim.analysis.plotRaster(...)
