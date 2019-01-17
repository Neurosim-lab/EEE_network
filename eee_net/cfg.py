from netpyne import specs, sim

# Simulation options
cfg = specs.SimConfig()        # object of class SimConfig to store simulation configuration
cfg.duration = 1000           # Duration of the simulation, in ms
cfg.dt = 0.025                # Internal integration timestep to use
cfg.verbose = False            # Show detailed messages 
cfg.recordTraces = {'V_soma':{'sec':'soma','loc':0.5,'var':'v'}}  # Dict with traces to record
cfg.recordStep = 1             # Step size in ms to save data (eg. V traces, LFP, etc)
cfg.filename = 'model_output'  # Set file output name
cfg.savePickle = False         # Save params, network and sim output to pickle file
cfg.saveMat = False         # Save params, network and sim output to pickle file


cfg.analysis['plotRaster'] = {'orderBy': 'y', 'orderInverse': True}      # Plot a raster
cfg.analysis['plotTraces'] = {'include': [('PT5_1',0), ('PT5_2', 0), ('PT5_3', 0), ('PT5_4', 0), ('PV5', 0)]}      # Plot recorded traces for this list of cells
cfg.analysis['plot2Dnet'] = True            # plot 2D visualization of cell positions and connections
cfg.analysis['plotConn'] = True             # plot connectivity matrix

# Create network and run simulation
#sim.createSimulateAnalyze(netParams = netParams, simConfig = simConfig)    

#import pylab; pylab.show()  # this line is only necessary in certain systems where figures appear empty

# check model output
#sim.checkOutput('tut5')