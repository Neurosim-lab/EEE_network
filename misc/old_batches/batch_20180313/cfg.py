"""
cfg.py 

Simulation configuration 

Contributors: salvadordura@gmail.com
"""

from netpyne import specs
import numpy as np

cfg = specs.SimConfig()  

###############################################################################
#
# SIMULATION CONFIGURATION
#
###############################################################################

cfg.checkErrors = True

###############################################################################
# Run parameters
###############################################################################
cfg.duration = 1000 
cfg.dt = 0.05
cfg.seeds = {'conn': 4321, 'stim': 1234, 'loc': 4321} 
cfg.hParams = {'celsius': 32}  
cfg.verbose = 0
cfg.cvode_active = False
cfg.printRunTime = 0.1
cfg.printPopAvgRates = True


###############################################################################
# Recording 
###############################################################################
cfg.recordTraces = {'V_soma': {'sec': 'soma', 'loc': 0.5, 'var': 'v'}}

cfg.bap = True

if cfg.bap:
    for loc in np.arange(0.0, 1.1, 0.1):
        locstr = str(loc).replace(".","")
        cfg.recordTraces['V_Bdend1_' + locstr] = {'sec': 'Bdend1', 'loc': loc, 'var': 'v'}
else:
    cfg.recordTraces['V_Bdend1_03'] = {'sec': 'Bdend1', 'loc': 0.3, 'var': 'v'}
    cfg.recordTraces['V_Bdend1_05'] = {'sec': 'Bdend1', 'loc': 0.5, 'var': 'v'}
    cfg.recordTraces['V_Bdend1_08'] = {'sec': 'Bdend1', 'loc': 0.8, 'var': 'v'}

cfg.recordCells = ['eee7']
cfg.recordStims = False  
cfg.recordStep = 0.1 


###############################################################################
# Saving
###############################################################################
cfg.simLabel = 'batch_20180313'
cfg.saveFolder = 'batch_data'
cfg.savePickle = False
cfg.saveJson = True
cfg.saveDataInclude = ['simData', 'simConfig', 'netParams', 'net']


###############################################################################
# Analysis and plotting 
###############################################################################
cfg.analysis['plotTraces'] = {'include': ['all'], 'oneFigPer': 'cell', 'saveFig': True, 
                              'showFig': False, 'figSize': (10,8), 'timeRange': [0,cfg.duration]}


###############################################################################
# Parameters
###############################################################################

# Sodium and potassium conductance scaling
cfg.dendNaScale = 1.0 # Scales dendritic Na conductance
cfg.dendKScale  = 1.0 # Scales dendritic K  conductance
#cfg.allNaScale  = 1.0 # Scales all Na conductances (overrides dendNaScale if not commented)
#cfg.allKScale   = 1.0 # Scales all K  conductances (overrides dendKScale  if not commented)

# DMS NMDA params
cfg.NMDAAlphaScale = 1.0 # Scales original value of 4.0
cfg.NMDABetaScale  = 4.5 #3.0 # Scales original value of 0.0015
cfg.CdurNMDAScale  = 1.0 # Scales original value of 1.0
#cfg.CmaxNMDAScale  = 1.0 # Scales original value of 1.0
cfg.NMDAgmax       = 0.05
cfg.ratioAMPANMDA  = 2.0

# glutamate stim parameters
cfg.synTime           = 200.0
cfg.numSyns           = 9
cfg.numExSyns         = cfg.numSyns
cfg.glutAmp           = 0.2
cfg.glutAmpExSynScale = 1.0
cfg.glutAmpDecay      = 5.0 # percent/um
cfg.synLocMiddle      = 0.45 
cfg.synLocRadius      = 0.15 
cfg.initDelay         = 10.0
cfg.synDelay          = 0.5 # ms/um
cfg.exSynDelay        = 1.0 # ms/um

# other params
cfg.e_pas         = -70.0 # resting membrane potential
cfg.ihScale       = 1.0   # Scales ih conductance
#cfg.gpasSomaScale = 1.0 # Scales soma g_pas
#cfg.dendRaScale   = 1.0
#cfg.dendRmScale   = 1.0
cfg.RaScale       = 1.0  # Scales axial resistance in all secs
cfg.RmScale       = 1.0  # Scales membrane resistance in all secs

cfg.ampIClamp1    = 5.0 # amplitude of current clamp
cfg.durIClamp1    = 0.5 # 1.0

###############################################################################
# NetStim inputs 
###############################################################################
cfg.addNetStim = False

cfg.NetStimSyn = {'pop': ['eee7'], 'loc': list(np.linspace(cfg.synLocMiddle-cfg.synLocRadius, cfg.synLocMiddle+cfg.synLocRadius, cfg.numSyns)), 'sec': 'Bdend1', 'synMech': ['NMDA','AMPA'], 'start': cfg.synTime, 'interval': 1000, 'noise': 0.0, 'number': 1, 'weight': cfg.glutAmp, 'delay': cfg.synDelay}

cfg.NetStimExSyn = {'pop': ['eee7'], 'loc': list(np.linspace(cfg.synLocMiddle-cfg.synLocRadius, cfg.synLocMiddle+cfg.synLocRadius, cfg.numExSyns)), 'sec': 'Bdend1', 'synMech': ['NMDA'], 'start': cfg.synTime, 'interval': 1000, 'noise': 0.0, 'number': 1, 'weight': cfg.glutAmp * cfg.glutAmpExSynScale, 'delay': cfg.exSynDelay}


###############################################################################
# Current inputs 
###############################################################################
cfg.addIClamp = False

if cfg.bap:
    cfg.addIClamp = True
    cfg.IClamp1 = {'pop': 'eee7', 'sec': 'soma', 'loc': 0.5, 'start': 200, 'dur': cfg.durIClamp1, 'amp': cfg.ampIClamp1}


