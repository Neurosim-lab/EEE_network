from netpyne import specs, sim

# Show figures? Save figures?
showFig = True
saveFig = True

# Simulation options
cfg = specs.SimConfig()       # object of class SimConfig to store simulation configuration
cfg.duration = 1000           # Duration of the simulation, in ms
cfg.dt = 0.025                # Internal integration timestep to use
cfg.verbose = False           # Show detailed messages 
cfg.recordStep = 1             # Step size in ms to save data (eg. V traces, LFP, etc)
cfg.filename = 'model_output'  # Set file output name
cfg.savePickle = False         # Save params, network and sim output to pickle file
cfg.saveMat = False  

# Network variables
cfg.numPT5cells = 80 #800
cfg.numPV5cells = 20 #200
cfg.ynormRange = [0.2, 0.623]

cfg.NMDAgmax        = 0.005
cfg.NMDA2AMPA       = 0.1
cfg.AMPAgmax        = cfg.NMDAgmax / cfg.NMDA2AMPA
cfg.NMDAweight      = 0.8
cfg.AMPAweight      = cfg.NMDAweight
cfg.GABAAfastWeight = 0.0001
cfg.GABAAslowWeight = 0.0001
cfg.GABAAfast_e     = -80
cfg.GABAAslow_e     = -90



# Recording options
cfg.recordTraces = {'V_soma': {'sec':'soma', 'loc':0.5, 'var':'v'}}  

# Analysis options
cfg.analysis['plotRaster'] = {'orderBy': 'y', 'orderInverse': True, 'saveFig': saveFig, 'showFig': showFig}
cfg.analysis['plotTraces'] = {'include': [('PT5_1',0), ('PT5_2', 0), ('PT5_3', 0), ('PT5_4', 0), ('PV5', 0)], 'saveFig': saveFig, 'showFig': showFig}      
cfg.analysis['plot2Dnet'] = {'saveFig': saveFig, 'showFig': showFig}            
cfg.analysis['plotConn'] = {'saveFig': saveFig, 'showFig': showFig}           







#import pylab; pylab.show()  # this line is only necessary in certain systems where figures appear empty
