from netpyne import specs, sim

# Show figures? Save figures?
showFig = True
saveFig = True

# Simulation options
cfg = specs.SimConfig()       
cfg.duration = 1000           
cfg.dt = 0.025                
cfg.verbose = False           
cfg.recordStep = 1             
cfg.simLabel = 'eee_net'
cfg.saveFolder = 'output'
cfg.savePickle = False         
cfg.saveMat = False
cfg.seeds = {'conn': 4123,
			 'stim': 1234, 
			 'loc' : 3214}  

# Network variables
cfg.numPT5cells = 8
cfg.numPV5cells = 2
cfg.sizeY       = 1600
cfg.sizeX       = 400
cfg.sizeZ       = 300
cfg.ynormRange  = [0.2, 0.623]

cfg.NMDAgmax        = 0.005
cfg.AMPANMDAratio   = 10.0
cfg.AMPAgmax        = cfg.AMPANMDAratio * cfg.NMDAgmax 
cfg.NMDAweight      = 0 #0.8
cfg.AMPAweight      = 0 #cfg.NMDAweight
cfg.GABAAfastWeight = 0 #0.0001
cfg.GABAAslowWeight = 0 #0.0001
cfg.GABAAfast_e     = -80
cfg.GABAAslow_e     = -90

# Noise variables
cfg.noisePT5 = True
cfg.noisePV5 = True

cfg.PT5_exc_noise_amp = 0.0121
cfg.PT5_exc_noise_e   = 0.0
cfg.PT5_exc_noise_tau = 1.0
cfg.PT5_inh_noise_amp = 0.0573
cfg.PT5_inh_noise_e   = -75.0
cfg.PT5_inh_noise_tau = 1.0

cfg.PV5_exc_noise_amp = 0.0121
cfg.PV5_exc_noise_e   = 0.0
cfg.PV5_exc_noise_tau = 1.0
cfg.PV5_inh_noise_amp = 0.0573
cfg.PV5_inh_noise_e   = -75.0
cfg.PV5_inh_noise_tau = 1.0

# Connectivity variables
cfg.EEconv = 3.0
cfg.EIconv = 3.0
cfg.IEconv = 12.0
cfg.IIconv = 12.0

# Recording options
cfg.recordTraces = {'V_soma': {'sec':'soma', 'loc':0.5, 'var':'v'}}  
cfg.printPopAvgRates = True

# Analysis options
cfg.analysis['plotRaster'] = {'orderBy': 'y', 'orderInverse': True, 'saveFig': saveFig, 'showFig': showFig}

cfg.analysis['plotRaster'] = {'orderBy': 'gid', 'orderInverse': True,'saveFig': saveFig, 'labels':'overlay','showFig': showFig} #'timeRange':[0,500], 'popColors': {'PT5':'red','PV5': 'blue'}}

cfg.analysis['plotTraces'] = {'include': [('PT5_1',0), ('PT5_2', 0), ('PT5_3', 0), ('PT5_4', 0), ('PV5', 0)], 'saveFig': saveFig, 'showFig': showFig}      
cfg.analysis['plot2Dnet'] = {'saveFig': saveFig, 'showFig': showFig}            
cfg.analysis['plotConn'] = {'saveFig': saveFig, 'showFig': showFig}           







#import pylab; pylab.show()  # this line is only necessary in certain systems where figures appear empty
