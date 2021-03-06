from netpyne import specs, sim
import numpy as np

# Show figures? Save figures?
showFig = False
saveFig = True

# Simulation options
cfg = specs.SimConfig()       
cfg.duration = 1000           
cfg.dt = 0.025                
cfg.verbose = True           
cfg.recordStep = 1             
cfg.simLabel = 'eee_net'
cfg.saveFolder = 'output'
cfg.savePickle = False         
cfg.saveMat = False
cfg.seeds = {'conn': 4123,
			 'stim': 1234, 
			 'loc' : 3214}  
cfg.hParams.celsius = 32.0
cfg.hParams.v_init  = -73.7

# Channel variables
cfg.ttx = False

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
cfg.NMDAweight      = 0.8
cfg.AMPAweight      = cfg.NMDAweight
cfg.GABAAfastWeight = 0.0001
cfg.GABAAslowWeight = 0.0001
cfg.GABAAfast_e     = -80
cfg.GABAAslow_e     = -90

# Noise variables
cfg.noisePT5 = True
cfg.noisePV5 = False

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

# Glutamate stim parameters
cfg.glutamate         = True

cfg.synTime           = 200.0
cfg.numSyns           = 24
cfg.numExSyns         = cfg.numSyns
cfg.glutAmp           = 2.0
cfg.glutAmpExSynScale = 1.0
cfg.glutAmpDecay      = 0.0 # percent/um
cfg.synLocMiddle      = 0.3 #0.45 
cfg.synLocRadius      = 0.15 
cfg.initDelay         = 10.0
cfg.synDelay          = 2.0 # ms/um
cfg.exSynDelay        = 4.0 # ms/um

cfg.glutPuffSyn = {'loc': list(np.linspace(cfg.synLocMiddle-cfg.synLocRadius, cfg.synLocMiddle+cfg.synLocRadius, cfg.numSyns)), 'sec': 'basal_8', 'synMech': ['NMDA','AMPA'], 'start': cfg.synTime, 'interval': 1000, 'noise': 0.0, 'number': 1, 'weight': cfg.glutAmp, 'delay': cfg.synDelay}

cfg.glutPuffExSyn = {'loc': list(np.linspace(cfg.synLocMiddle-cfg.synLocRadius, cfg.synLocMiddle+cfg.synLocRadius, cfg.numExSyns)), 'sec': 'basal_8', 'synMech': ['NMDA'], 'start': cfg.synTime, 'interval': 1000, 'noise': 0.0, 'number': 1, 'weight': cfg.glutAmp * cfg.glutAmpExSynScale, 'delay': cfg.exSynDelay}

# Recording options
cfg.recordTraces = {'V_soma': {'sec':'soma', 'loc':0.5, 'var':'v'}} 
#cfg.recordTraces['V_soma_0'] = {'sec':'soma_0', 'loc':0.5, 'var':'v'}
#cfg.recordTraces['V_dend_1'] = {'sec':'basal_1', 'loc':0.5, 'var':'v'}
#cfg.recordTraces['V_dend_2'] = {'sec':'basal_2', 'loc':0.5, 'var':'v'}
#cfg.recordTraces['V_dend_3'] = {'sec':'basal_3', 'loc':0.5, 'var':'v'}
#cfg.recordTraces['V_dend_4'] = {'sec':'basal_4', 'loc':0.5, 'var':'v'}
#cfg.recordTraces['V_dend_5'] = {'sec':'basal_5', 'loc':0.5, 'var':'v'}
#cfg.recordTraces['V_dend_6'] = {'sec':'basal_6', 'loc':0.5, 'var':'v'}
#cfg.recordTraces['V_dend_7'] = {'sec':'basal_7', 'loc':0.5, 'var':'v'}
cfg.recordTraces['V_dend_8'] = {'sec':'basal_8', 'loc':0.5, 'var':'v'}
cfg.recordTraces['V_dend_9'] = {'sec':'basal_9', 'loc':0.5, 'var':'v'}

cfg.printPopAvgRates = True

# Analysis options
#cfg.analysis['plotRaster'] = {'orderBy': 'y', 'orderInverse': True, 'saveFig': saveFig, 'showFig': showFig}
#cfg.analysis['plotRaster'] = {'orderBy': 'gid', 'orderInverse': True,'saveFig': saveFig, 'labels':'overlay','showFig': showFig} #'timeRange':[0,500], 'popColors': {'PT5':'red','PV5': 'blue'}}

#cfg.analysis['plotTraces'] = {'include': [('PT5_1',0), ('PT5_2', 0), ('PT5_3', 0), ('PT5_4', 0), ('PV5', 0)], 'saveFig': saveFig, 'showFig': showFig}  
#cfg.analysis['plotTraces'] = {'include': ['eeeD', 'eeeS'], 'saveFig': saveFig, 'showFig': showFig}  
cfg.analysis['plotTraces'] = {'include': ['eeeS'], 'saveFig': saveFig, 'showFig': showFig}    
#cfg.analysis['plot2Dnet'] = {'saveFig': saveFig, 'showFig': showFig}            
#cfg.analysis['plotConn'] = {'saveFig': saveFig, 'showFig': showFig}           


# Current clamps
cfg.addIClamp = False

cfg.delIClamp1 = 200
cfg.durIClamp1 = 10
cfg.ampIClamp1 = 1.0
cfg.popIClamp1 = ['PT5_2']
cfg.secIClamp1 = 'soma'
cfg.locIClamp1 = 0.5

cfg.IClamp1 = {'pop': cfg.popIClamp1, 'sec': cfg.secIClamp1, 'loc': cfg.locIClamp1, 'del': cfg.delIClamp1, 'dur': cfg.durIClamp1, 'amp': cfg.ampIClamp1}





#import pylab; pylab.show()  # this line is only necessary in certain systems where figures appear empty
