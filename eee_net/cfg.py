import netpyne
from netpyne import specs, sim
import numpy as np
import os

# Show figures? Save figures?
showFig = False
saveFig = True
saveData = False

# Simulation options
cfg = specs.SimConfig()
cfg.dummy    = 0       
cfg.duration = 2500
cfg.numCells = 5 #10000 
cfg.dt = 0.025                
cfg.verbose = False           
cfg.recordStep = 1             
cfg.simLabel = 'eee_net_80'

#baseFolder = '/scratch/06322/tg856217'
baseFolder = 'data'
cfg.saveFolder = os.path.join(baseFolder, cfg.simLabel)

cfg.savePickle = False
cfg.saveJson = True
cfg.saveDataInclude = ['simData', 'simConfig', 'netParams', 'net']         
cfg.saveMat = False
cfg.saveCellSecs = False
cfg.saveCellConns = True
cfg.seeds = {'conn': 4123,
			 'stim': 1234, 
			 'loc' : 3214}  
cfg.hParams.celsius = 32.0
cfg.hParams.v_init  = -73.7

# Cellular variables
cfg.PT5_epas = -85.0  # None or a value (default: -65)
cfg.dendRa   = 100.0  # Default: 100.0
cfg.somaNaScale = 1.0
cfg.dendNaScale = 1.0
cfg.axonNaScale = 1.0

# Network variables
cfg.sizeY       = 1600
cfg.sizeX       = 400
cfg.sizeZ       = 300
cfg.ynormRange  = [0.2, 0.623]

cfg.NMDAgmax        = 0.02 #0.01 #Penny has 0.005
cfg.AMPANMDAratio   = 10.0
cfg.AMPAgmax        = cfg.AMPANMDAratio * cfg.NMDAgmax 
cfg.NMDAweight      = 0.2
cfg.AMPAweight      = cfg.NMDAweight
cfg.GABAAfastWeight = 0.0001
cfg.GABAAslowWeight = cfg.GABAAfastWeight
cfg.GABAAfast_e     = -80.0
cfg.GABAAslow_e     = -90.0

# Noise variables
cfg.noise = True
cfg.noisePT5 = True
cfg.noisePV5 = True

cfg.noise_amp_scale = 1.0
cfg.noise_std_scale = 1.0

cfg.PT5_exc_noise_e   = cfg.PT5_epas + 65.0   # Default E_e : 0.0
cfg.PT5_exc_noise_amp = 1.0     # g_e0        : 0.0121 * cfg.PT5_exc_noise_amp
cfg.PT5_exc_noise_std = 1.0     # std_e       : (0.0030 / 0.0121) * cfg.PT5_exc_noise_amp * cfg.PT5_exc_noise_std
cfg.PT5_exc_noise_tau = 1.0     # tau_e       : 2.728 * cfg.PT5_exc_noise_tau
cfg.PT5_inh_noise_e   = cfg.PT5_epas - 10.0   # Default E_i : -75.0
cfg.PT5_inh_noise_amp = 1.0     # g_i0        : 0.0573 * cfg.PT5_inh_noise_amp
cfg.PT5_inh_noise_std = 1.0     # std_i       : (0.0066 / 0.0573) * cfg.PT5_inh_noise_amp * cfg.PT5_inh_noise_std
cfg.PT5_inh_noise_tau = 1.0     # tau_i       : 10.49 * cfg.PT5_inh_noise_tau

cfg.PV5_noise_amp = 0.25 #0.1 #1.0
cfg.PV5_noise_std = 0.25 #0.1 #1.0

cfg.PV5_exc_noise_amp = 1.0     # g_e0        : 0.0121 * cfg.PV5_exc_noise_amp
cfg.PV5_exc_noise_std = 1.0     # std_e       : 0.0030 * cfg.PV5_exc_noise_std
cfg.PV5_exc_noise_e   = 0.0     # Default E_e : 0.0
cfg.PV5_exc_noise_tau = 1.0     # tau_e       : 2.728 * cfg.PV5_exc_noise_tau
cfg.PV5_inh_noise_amp = 1.0     # g_i0        : 0.0573 * cfg.PV5_inh_noise_amp
cfg.PV5_inh_noise_std = 1.0     # std_i       : 0.0066 * cfg.PV5_inh_noise_std
cfg.PV5_inh_noise_e   = -75.0   # Default E_i : -75.0
cfg.PV5_inh_noise_tau = 1.0     # tau_i       : 10.49 * cfg.PV5_inh_noise_tau

# Connectivity variables
cfg.connType = 'convergence'  # 'convergence', 'divergence', or 'probability'
cfg.EScale = 1.0
cfg.IScale = 1.0

cfg.EEconn = 1 #0.0005 # Will be multiplied by cfg.EScale
cfg.EIconn = 6 #4 #0.005 #0.0005 # Will be multiplied by cfg.EScale
cfg.IEconn = 1 #0.0005 # Will be multiplied by cfg.IScale
cfg.IIconn = 1 #0.0005 # Will be multiplied by cfg.IScale

cfg.EEspc = 1 
cfg.EIspc = 1
cfg.IEspc = 1
cfg.IIspc = 1


# Glutamate stim parameters
cfg.glutamate         = True
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
cfg.recordTraces['V_dend'] = {'sec':'basal_8', 'loc':0.5, 'var':'v'}

#cfg.recordCells = [('PT5_1', [0, 1, 2, 3]), ('PT5_2', [0, 1, 2, 3]), ('PT5_3', [0, 1, 2, 3]), ('PT5_4', [0, 1, 2, 3]), ('PV5', [0, 1, 2, 3])]

cfg.printPopAvgRates = True

# Analysis options
cfg.analysis['plotRaster'] = {'orderBy': 'gid', 'orderInverse': True, 'lw': 0.5, 'saveFig': saveFig, 'showFig': showFig, 'saveData': saveData}
#cfg.analysis['plotRaster'] = {'orderBy': 'gid', 'orderInverse': True, 'lw': 0.5, 'saveFig': saveFig, 'showFig': showFig, 'saveData': saveData, 'include': ['PT5_1', 'PT5_2', 'PT5_3', 'PT5_4']}

cfg.analysis['plotSpikeHist'] = {'saveFig': saveFig,'showFig': showFig, 'saveData': saveData}

#cfg.analysis['plotTraces'] = {'include': [('PT5_1', [0, 1, 2, 3]), ('PT5_2', [0, 1, 2, 3]), ('PT5_3', [0, 1, 2, 3]), ('PT5_4', [0, 1, 2, 3]), ('PV5', [0, 1, 2, 3])], 'saveFig': saveFig, 'showFig': showFig, 'ylim': [-80, 30]}  

include = list(range(0, 5))
include = include + list(range(2000, 2005))
include = include + list(range(4000, 4005))
include = include + list(range(6000, 6005))
include = include + list(range(8000, 8005))
include = include + list(range(9000, 9005))

include = ['allCells']

cfg.recordCells = include

cfg.analysis['plotTraces'] = {'include': include, 'saveFig': saveFig, 'showFig': showFig, 'ylim': [-100, 40]} 

#cfg.analysis['plot2Dnet'] = {'saveFig': saveFig, 'showFig': showFig}   

includePre  = ['PT5_1', 'PT5_2', 'PT5_3', 'PT5_4', 'PV5_1', 'PV5_2']
includePost = ['PT5_1', 'PT5_2', 'PT5_3', 'PT5_4', 'PV5_1', 'PV5_2']
feature     = 'numConns' #'divergence' #'convergence' #'strength' # 
groupBy     = 'pop' #'cell'
orderBy     = 'gid' #'y'
synOrConn   = 'conn' # 'syn' 

cfg.analysis['plotConn'] = {'saveFig': saveFig, 'showFig': showFig, 'includePre':includePre, 'includePost':includePost, 'feature':feature, 'groupBy':groupBy, 'orderBy':orderBy, 'saveData': saveData}


# Current clamps
cfg.addIClamp = False

cfg.delIClamp1 = 500
cfg.durIClamp1 = 500
cfg.ampIClamp1 = 0.3
cfg.popIClamp1 = ['PT5_1']
cfg.secIClamp1 = 'soma'
cfg.locIClamp1 = 0.5

cfg.IClamp1 = {'pop': cfg.popIClamp1, 'sec': cfg.secIClamp1, 'loc': cfg.locIClamp1, 'del': cfg.delIClamp1, 'dur': cfg.durIClamp1, 'amp': cfg.ampIClamp1}

cfg.delIClamp2 = 1500
cfg.durIClamp2 = 500
cfg.ampIClamp2 = 0.3125
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


