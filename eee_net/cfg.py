from netpyne import specs, sim
import numpy as np
import os

# Show figures? Save figures?
showFig = False
saveFig = True
saveData = True

# Simulation options
cfg = specs.SimConfig()
cfg.dummy    = 0       
cfg.duration = 2400 #10000
cfg.numCells = 100 
cfg.dt = 0.025                
cfg.verbose = False           
cfg.recordStep = 1             
cfg.simLabel = 'eee_net_56'

baseFolder = '/scratch/06322/tg856217'
#baseFolder = 'data'
cfg.saveFolder = os.path.join(baseFolder, cfg.simLabel)

cfg.savePickle = False
cfg.saveJson = True
cfg.saveDataInclude = ['simData', 'simConfig', 'netParams', 'net']         
cfg.saveMat = False
cfg.saveCellSecs = False
cfg.saveCellConns = True #False
cfg.seeds = {'conn': 4123,
			 'stim': 1234, 
			 'loc' : 3214}  
cfg.hParams.celsius = 32.0
cfg.hParams.v_init  = -73.7

# Network variables
cfg.sizeY       = 1600
cfg.sizeX       = 400
cfg.sizeZ       = 300
cfg.ynormRange  = [0.2, 0.623]

cfg.NMDAgmax        = 0.005
cfg.AMPANMDAratio   = 10.0
cfg.AMPAgmax        = cfg.AMPANMDAratio * cfg.NMDAgmax 
cfg.NMDAweight      = 0.2 #0.4 #0.8
cfg.AMPAweight      = cfg.NMDAweight
cfg.GABAAfastWeight = 0.01 #0.0001
cfg.GABAAslowWeight = cfg.GABAAfastWeight #0.0001
cfg.GABAAfast_e     = -80
cfg.GABAAslow_e     = -90

# Noise variables
cfg.noisePT5 = False
cfg.noisePV5 = False

cfg.PT5_noise_scaling = 1.0
cfg.PT5_exc_noise_amp = 0.01 * cfg.PT5_noise_scaling
cfg.PT5_exc_noise_e   = 0.0
cfg.PT5_exc_noise_tau = 1.0
cfg.PT5_inh_noise_amp = 0.01 * cfg.PT5_noise_scaling
cfg.PT5_inh_noise_e   = -75.0
cfg.PT5_inh_noise_tau = 1.0

cfg.PV5_exc_noise_amp = 1.0
cfg.PV5_exc_noise_e   = 0.0
cfg.PV5_exc_noise_tau = 1.0
cfg.PV5_inh_noise_amp = 1.0
cfg.PV5_inh_noise_e   = -75.0
cfg.PV5_inh_noise_tau = 1.0

# Connectivity variables
cfg.connType = 'probability'  # 'convergence', 'divergence', or 'probability'
cfg.EEconn = 0.0005 #0.005 #0.05 #3.0
cfg.EIconn = cfg.EEconn #0.05 #3.0
cfg.IEconn = 0.002 #0.02 #0.2 #12.0
cfg.IIconn = cfg.IEconn #0.2 #12.0

# Glutamate stim parameters
cfg.glutamate         = False 
cfg.glutPops          = ['PT5_1', 'PT5_2']

cfg.glutTimes         = [800.0, 2000.0]
cfg.numSyns           = 24
cfg.numExSyns         = cfg.numSyns
cfg.glutAmp           = 2.0
cfg.glutAmpExSynScale = 1.0
cfg.glutAmpDecay      = 0.0 # percent/um
cfg.synLocMiddle      = 0.7
cfg.synLocRadius      = 0.15 
cfg.initDelay         = 10.0
cfg.synDelay          = 2.0 # ms/um
cfg.exSynDelay        = 4.0 # ms/um


# Recording options
cfg.recordTraces = {'V_soma': {'sec':'soma', 'loc':0.5, 'var':'v'}} 
#cfg.recordTraces['V_dend_8'] = {'sec':'basal_8', 'loc':0.5, 'var':'v'}

#cfg.recordCells = [('PT5_1', [0, 1, 2, 3]), ('PT5_2', [0, 1, 2, 3]), ('PT5_3', [0, 1, 2, 3]), ('PT5_4', [0, 1, 2, 3]), ('PV5', [0, 1, 2, 3])]

cfg.printPopAvgRates = True

# Analysis options
cfg.analysis['plotRaster'] = {'orderBy': 'gid', 'orderInverse': True, 'saveFig': saveFig, 'showFig': showFig, 'saveData': saveData}

cfg.analysis['plotSpikeHist'] = {'saveFig': saveFig,'showFig': showFig, 'saveData': saveData}

#cfg.analysis['plotTraces'] = {'include': [('PT5_1', [0, 1, 2, 3]), ('PT5_2', [0, 1, 2, 3]), ('PT5_3', [0, 1, 2, 3]), ('PT5_4', [0, 1, 2, 3]), ('PV5', [0, 1, 2, 3])], 'saveFig': saveFig, 'showFig': showFig, 'ylim': [-80, 30]}  

include = list(range(0, 21))
include = include + list(range(2000, 2021))
include = include + list(range(4000, 4021))
include = include + list(range(6000, 6021))
include = include + list(range(8000, 8021))
include = include + list(range(9000, 9021))

include = 'allCells'


cfg.analysis['plotTraces'] = {'include': include, 'saveFig': saveFig, 'showFig': showFig, 'ylim': [-80, 30]}  

#cfg.analysis['plot2Dnet'] = {'saveFig': saveFig, 'showFig': showFig}   

includePre  = ['PT5_1', 'PT5_2', 'PT5_3', 'PT5_4', 'PV5_1', 'PV5_2']
includePost = ['PT5_1', 'PT5_2', 'PT5_3', 'PT5_4', 'PV5_1', 'PV5_2']
feature     = 'numConns' #'divergence' #'convergence' #'strength' # 
groupBy     = 'pop' #'cell'
orderBy     = 'gid' #'y'
synOrConn   = 'conn' # 'syn' 

cfg.analysis['plotConn'] = {'saveFig': saveFig, 'showFig': showFig, 'includePre':includePre, 'includePost':includePost, 'feature':feature, 'groupBy':groupBy, 'orderBy':orderBy, 'saveData': saveData}


# Current clamps
cfg.addIClamp = True

cfg.delIClamp1 = 200
cfg.durIClamp1 = 500
cfg.ampIClamp1 = 1.0
cfg.popIClamp1 = ['PT5_1']
cfg.secIClamp1 = 'soma'
cfg.locIClamp1 = 0.5

cfg.IClamp1 = {'pop': cfg.popIClamp1, 'sec': cfg.secIClamp1, 'loc': cfg.locIClamp1, 'del': cfg.delIClamp1, 'dur': cfg.durIClamp1, 'amp': cfg.ampIClamp1}

cfg.delIClamp2 = 1500
cfg.durIClamp2 = 500
cfg.ampIClamp2 = 1.0
cfg.popIClamp2 = ['PV5_1']
cfg.secIClamp2 = 'soma'
cfg.locIClamp2 = 0.5

cfg.IClamp2 = {'pop': cfg.popIClamp2, 'sec': cfg.secIClamp2, 'loc': cfg.locIClamp2, 'del': cfg.delIClamp2, 'dur': cfg.durIClamp2, 'amp': cfg.ampIClamp2}


# Common synaptic input
cfg.addCommonInput1 = False
cfg.popCommonInput1 = ['PT5_1', 'PT5_3']

cfg.secCommonInput1 = 'soma'
cfg.locCommonInput1 = 0.5
cfg.wgtCommonInput1 = 4.0
cfg.delCommonInput1 = 1400  # delay or start
cfg.numCommonInput1 = 10    # number
cfg.intCommonInput1 = 20   # interval


cfg.addCommonInput2 = False
cfg.popCommonInput2 = ['PT5_1', 'PT5_3']

cfg.secCommonInput2 = 'soma'
cfg.locCommonInput2 = 0.5
cfg.wgtCommonInput2 = 4.0
cfg.delCommonInput2 = 2000  # delay or start
cfg.numCommonInput2 = 10    # number
cfg.intCommonInput2 = 20   # interval


